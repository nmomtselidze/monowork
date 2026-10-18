package main

import (
	"errors"
	"fmt"
	"strings"
	"sync"
	"time"
)

// -----------------------------------------------------------------------------
// 1. Workflow States & Domain Models
// -----------------------------------------------------------------------------

type WorkflowState string

const (
	StateSubmitted        WorkflowState = "SUBMITTED"
	StateDocProcessed     WorkflowState = "DOC_PROCESSED"
	StatePendingManager   WorkflowState = "PENDING_MANAGER"
	StatePendingFinance   WorkflowState = "PENDING_FINANCE"
	StatePendingExecutive WorkflowState = "PENDING_EXECUTIVE"
	StateApproved         WorkflowState = "APPROVED"
	StateRejected         WorkflowState = "REJECTED"
	StateCompleted        WorkflowState = "COMPLETED"
)

type Document struct {
	FileName      string
	RawPayload    string
	ExtractedData map[string]string // Key-value pairs parsed from OCR
	Validated     bool
}

type ApprovalRecord struct {
	Role      string
	Approver  string
	Approved  bool
	Comment   string
	Timestamp time.Time
}

type ExpenseRequest struct {
	RequestID   string
	SubmitterID string
	Department  string
	Amount      float64
	Currency    string
	Document    Document
	State       WorkflowState
	AuditTrail  []ApprovalRecord
	mu          sync.Mutex
}

func (r *ExpenseRequest) AddAudit(role, approver string, approved bool, comment string) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.AuditTrail = append(r.AuditTrail, ApprovalRecord{
		Role:      role,
		Approver:  approver,
		Approved:  approved,
		Comment:   comment,
		Timestamp: time.Now(),
	})
}

// -----------------------------------------------------------------------------
// 2. Services & Processors
// -----------------------------------------------------------------------------

// DocumentProcessor handles OCR extraction and validation
type DocumentProcessor struct{}

func (dp *DocumentProcessor) Process(doc *Document) error {
	if doc.RawPayload == "" {
		return errors.New("document body is empty")
	}

	// Simulated OCR / Key-Value Extraction
	doc.ExtractedData = make(map[string]string)
	lines := strings.Split(doc.RawPayload, ";")
	for _, line := range lines {
		parts := strings.SplitN(line, "=", 2)
		if len(parts) == 2 {
			key := strings.TrimSpace(parts[0])
			val := strings.TrimSpace(parts[1])
			doc.ExtractedData[key] = val
		}
	}

	// Validate presence of essential invoice metadata
	if _, ok := doc.ExtractedData["TAX_ID"]; !ok {
		return errors.New("OCR validation failed: TAX_ID missing from document")
	}
	if _, ok := doc.ExtractedData["INVOICE_TOTAL"]; !ok {
		return errors.New("OCR validation failed: INVOICE_TOTAL missing from document")
	}

	doc.Validated = true
	return nil
}

// NotificationService informs stakeholders of status changes
type NotificationService struct{}

func (ns *NotificationService) Notify(recipient, subject, message string) {
	fmt.Printf("  [Notification -> %s] Subject: %s | %s\n", recipient, subject, message)
}

// -----------------------------------------------------------------------------
// 3. Approval Workflow Engine
// -----------------------------------------------------------------------------

type ApprovalEngine struct {
	docProcessor *DocumentProcessor
	notifier     *NotificationService
}

func NewApprovalEngine() *ApprovalEngine {
	return &ApprovalEngine{
		docProcessor: &DocumentProcessor{},
		notifier:     &NotificationService{},
	}
}

// Step 1: Ingest and process documents
func (ae *ApprovalEngine) IngestAndProcess(req *ExpenseRequest) error {
	fmt.Printf("[Step 1] Ingesting Request %s and processing document: %s\n", req.RequestID, req.Document.FileName)

	if err := ae.docProcessor.Process(&req.Document); err != nil {
		req.State = StateRejected
		req.AddAudit("SYSTEM", "OCR_ENGINE", false, err.Error())
		ae.notifier.Notify(req.SubmitterID, "Submission Rejected", "Invalid document: "+err.Error())
		return err
	}

	req.State = StateDocProcessed
	fmt.Println("  Document processed successfully. Extracted fields:")
	for k, v := range req.Document.ExtractedData {
		fmt.Printf("   - %s: %s\n", k, v)
	}

	// Route to first approval stage
	req.State = StatePendingManager
	ae.notifier.Notify("manager@company.com", "Action Required", fmt.Sprintf("Request %s awaiting manager review", req.RequestID))
	return nil
}

// Step 2: Line Manager Approval
func (ae *ApprovalEngine) ReviewByManager(req *ExpenseRequest, approver string, approve bool, comment string) error {
	if req.State != StatePendingManager {
		return fmt.Errorf("invalid transition: request is not in PENDING_MANAGER (current: %s)", req.State)
	}

	req.AddAudit("MANAGER", approver, approve, comment)

	if !approve {
		req.State = StateRejected
		ae.notifier.Notify(req.SubmitterID, "Request Rejected", "Manager rejected request: "+comment)
		return nil
	}

	req.State = StatePendingFinance
	ae.notifier.Notify("finance@company.com", "Action Required", fmt.Sprintf("Request %s passed manager, needs finance audit", req.RequestID))
	return nil
}

// Step 3: Finance Audit & Policy Enforcement
func (ae *ApprovalEngine) ReviewByFinance(req *ExpenseRequest, auditor string, approve bool, comment string) error {
	if req.State != StatePendingFinance {
		return fmt.Errorf("invalid transition: request is not in PENDING_FINANCE (current: %s)", req.State)
	}

	req.AddAudit("FINANCE", auditor, approve, comment)

	if !approve {
		req.State = StateRejected
		ae.notifier.Notify(req.SubmitterID, "Request Rejected", "Finance rejected request: "+comment)
		return nil
	}

	// Policy Rule: Expenses over $5,000 escalate to Executive Approval
	if req.Amount > 5000.00 {
		req.State = StatePendingExecutive
		ae.notifier.Notify("vp_finance@company.com", "High-Value Approval Required", fmt.Sprintf("Request %s ($%.2f) requires executive clearance", req.RequestID, req.Amount))
	} else {
		req.State = StateApproved
		ae.completeWorkflow(req)
	}

	return nil
}

// Step 4: Final Executive Approval (for high-value purchases)
func (ae *ApprovalEngine) ReviewByExecutive(req *ExpenseRequest, exec string, approve bool, comment string) error {
	if req.State != StatePendingExecutive {
		return fmt.Errorf("invalid transition: request is not in PENDING_EXECUTIVE (current: %s)", req.State)
	}

	req.AddAudit("EXECUTIVE", exec, approve, comment)

	if !approve {
		req.State = StateRejected
		ae.notifier.Notify(req.SubmitterID, "Request Rejected", "Executive rejected request: "+comment)
		return nil
	}

	req.State = StateApproved
	ae.completeWorkflow(req)
	return nil
}

// Step 5: Finalization & Notification
func (ae *ApprovalEngine) completeWorkflow(req *ExpenseRequest) {
	req.State = StateCompleted
	fmt.Printf("[Finalize] Request %s approved. Initiating payment disbursement.\n", req.RequestID)
	ae.notifier.Notify(req.SubmitterID, "Request Approved", fmt.Sprintf("Your request %s for $%.2f has been fully approved.", req.RequestID, req.Amount))
	ae.notifier.Notify("erp_sync@internal", "ERP Ingestion", fmt.Sprintf("Syncing request %s into Ledger", req.RequestID))
}

// -----------------------------------------------------------------------------
// 4. Execution Examples
// -----------------------------------------------------------------------------

func main() {
	engine := NewApprovalEngine()

	// Scenario 1: Standard High-Value Expense Request (Passes all 4 approval stages)
	fmt.Println("=== Scenario 1: High-Value Request Flow ($7,500) ===")
	order1 := &ExpenseRequest{
		RequestID:   "REQ-2026-001",
		SubmitterID: "alice@company.com",
		Department:  "Engineering",
		Amount:      7500.00,
		Currency:    "USD",
		Document: Document{
			FileName:   "cloud_services_invoice.txt",
			RawPayload: "VENDOR=CloudCorp;TAX_ID=98-7654321;INVOICE_TOTAL=7500.00;DUE_DATE=2026-11-01",
		},
		State: StateSubmitted,
	}

	// 1. Process Document
	if err := engine.IngestAndProcess(order1); err != nil {
		fmt.Printf("Ingestion failed: %v\n", err)
		return
	}

	// 2. Manager signs off
	fmt.Println("\n[Action] Manager Reviews...")
	_ = engine.ReviewByManager(order1, "bob_mgr@company.com", true, "Budget verified for Q4 infra")

	// 3. Finance signs off (routes to executive because Amount > $5,000)
	fmt.Println("\n[Action] Finance Reviews...")
	_ = engine.ReviewByFinance(order1, "charlie_fin@company.com", true, "PO matches billing address")

	// 4. Executive final sign-off
	fmt.Println("\n[Action] Executive Reviews...")
	_ = engine.ReviewByExecutive(order1, "diana_vp@company.com", true, "Approved expenditure")

	// Print Audit Trail
	printAudit(order1)

	// Scenario 2: Document Processing Failure
	fmt.Println("\n=== Scenario 2: Document Validation Rejection ===")
	order2 := &ExpenseRequest{
		RequestID:   "REQ-2026-002",
		SubmitterID: "mark@company.com",
		Department:  "Marketing",
		Amount:      1200.00,
		Currency:    "USD",
		Document: Document{
			FileName:   "unreadable_receipt.txt",
			RawPayload: "VENDOR=AdAgency;NOTE=Incomplete scan", // Missing TAX_ID and INVOICE_TOTAL
		},
		State: StateSubmitted,
	}

	_ = engine.IngestAndProcess(order2)
	printAudit(order2)
}

func printAudit(req *ExpenseRequest) {
	fmt.Printf("\n--- Audit Log for %s (Final State: %s) ---\n", req.RequestID, req.State)
	for i, a := range req.AuditTrail {
		fmt.Printf(" %d. [%s] by %s (Decision: %t) -> Comment: \"%s\"\n",
			i+1, a.Role, a.Approver, a.Approved, a.Comment)
	}
}
