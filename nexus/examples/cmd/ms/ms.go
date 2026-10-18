package main

import (
	"context"
	"errors"
	"fmt"
	"time"
)

// -----------------------------------------------------------------------------
// 1. Domain Models & Context
// -----------------------------------------------------------------------------

type UserProfile struct {
	UserID   string
	Email    string
	IsActive bool
}

type OrderContext struct {
	OrderID  string
	UserID   string
	ItemID   string
	Quantity int
	Amount   float64

	// Intermediate values passed between dependent stages
	User             *UserProfile
	ReservationID    string
	PaymentTxnID     string
	ConfirmationSent bool
	StockCommitted   bool
}

type CompensationStep func(ctx context.Context) error

// -----------------------------------------------------------------------------
// 2. Service Interfaces
// -----------------------------------------------------------------------------

type UserService interface {
	ValidateUser(ctx context.Context, userID string) (*UserProfile, error)
}

type InventoryService interface {
	CheckAndHold(ctx context.Context, itemID string, qty int) (string, error)
	ReleaseHold(ctx context.Context, reservationID string) error
	CommitStock(ctx context.Context, reservationID, paymentTxnID string) error
}

type PaymentService interface {
	ProcessPayment(ctx context.Context, userID string, amount float64, reservationID string) (string, error)
	RefundPayment(ctx context.Context, paymentTxnID string) error
}

type NotificationService interface {
	SendConfirmation(ctx context.Context, email, orderID, txnID string) error
}

// -----------------------------------------------------------------------------
// 3. Centralized Orchestrator
// -----------------------------------------------------------------------------

type OrderFulfillmentOrchestrator struct {
	user      UserService
	inventory InventoryService
	payment   PaymentService
	notify    NotificationService
}

func NewOrderFulfillmentOrchestrator(
	u UserService,
	inv InventoryService,
	p PaymentService,
	n NotificationService,
) *OrderFulfillmentOrchestrator {
	return &OrderFulfillmentOrchestrator{
		user:      u,
		inventory: inv,
		payment:   p,
		notify:    n,
	}
}

func (o *OrderFulfillmentOrchestrator) Execute(ctx context.Context, order *OrderContext) error {
	var compensations []CompensationStep

	// Rollback unrolls successfully executed mutations in LIFO order
	rollback := func() {
		if len(compensations) == 0 {
			return
		}
		fmt.Println("[Orchestrator] Step failed. Executing compensations...")
		for i := len(compensations) - 1; i >= 0; i-- {
			// Detach cleanup timeout from parent context cancellation
			cleanCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
			if err := compensations[i](cleanCtx); err != nil {
				fmt.Printf("  [Alert] Rollback step failed: %v\n", err)
			}
			cancel()
		}
	}

	// -------------------------------------------------------------------------
	// Step 1: Validate User
	// -------------------------------------------------------------------------
	fmt.Printf("[Step 1] Validating user: %s...\n", order.UserID)
	userProfile, err := o.user.ValidateUser(ctx, order.UserID)
	if err != nil {
		return fmt.Errorf("user validation failed: %w", err)
	}
	order.User = userProfile
	fmt.Printf("  User %s valid (Email: %s)\n", userProfile.UserID, userProfile.Email)

	// -------------------------------------------------------------------------
	// Step 2: Check & Hold Inventory (Depends on valid user)
	// -------------------------------------------------------------------------
	fmt.Printf("[Step 2] Checking stock & holding %d unit(s) of %s...\n", order.Quantity, order.ItemID)
	resID, err := o.inventory.CheckAndHold(ctx, order.ItemID, order.Quantity)
	if err != nil {
		return fmt.Errorf("inventory check failed: %w", err)
	}
	order.ReservationID = resID
	fmt.Printf("  Stock reserved. ReservationID: %s\n", resID)

	// Register compensation to release hold if downstream steps fail
	compensations = append(compensations, func(c context.Context) error {
		return o.inventory.ReleaseHold(c, resID)
	})

	// -------------------------------------------------------------------------
	// Step 3: Process Payment (Depends on User + ReservationID + Amount)
	// -------------------------------------------------------------------------
	fmt.Printf("[Step 3] Processing charge of $%.2f for user %s...\n", order.Amount, order.User.UserID)
	txnID, err := o.payment.ProcessPayment(ctx, order.User.UserID, order.Amount, order.ReservationID)
	if err != nil {
		rollback()
		return fmt.Errorf("payment processing failed: %w", err)
	}
	order.PaymentTxnID = txnID
	fmt.Printf("  Payment authorized. TransactionID: %s\n", txnID)

	// Register compensation to refund payment if subsequent steps fail
	compensations = append(compensations, func(c context.Context) error {
		return o.payment.RefundPayment(c, txnID)
	})

	// -------------------------------------------------------------------------
	// Step 4: Send Confirmation (Depends on PaymentTxnID + User Email)
	// -------------------------------------------------------------------------
	fmt.Printf("[Step 4] Sending confirmation receipt to %s...\n", order.User.Email)
	if err := o.notify.SendConfirmation(ctx, order.User.Email, order.OrderID, order.PaymentTxnID); err != nil {
		rollback()
		return fmt.Errorf("notification failed: %w", err)
	}
	order.ConfirmationSent = true
	fmt.Println("  Confirmation sent successfully.")

	// -------------------------------------------------------------------------
	// Step 5: Update/Commit Inventory (Depends on ReservationID + PaymentTxnID)
	// -------------------------------------------------------------------------
	fmt.Printf("[Step 5] Finalizing stock deduction for reservation %s...\n", order.ReservationID)
	if err := o.inventory.CommitStock(ctx, order.ReservationID, order.PaymentTxnID); err != nil {
		rollback()
		return fmt.Errorf("inventory final commit failed: %w", err)
	}
	order.StockCommitted = true
	fmt.Println("  Inventory ledger updated permanently.")

	return nil
}

// -----------------------------------------------------------------------------
// 4. Mock Microservices
// -----------------------------------------------------------------------------

type mockUserService struct{}

func (m *mockUserService) ValidateUser(ctx context.Context, userID string) (*UserProfile, error) {
	if userID == "usr_suspended" {
		return nil, errors.New("user account is suspended")
	}
	return &UserProfile{
		UserID:   userID,
		Email:    fmt.Sprintf("%s@example.com", userID),
		IsActive: true,
	}, nil
}

type mockInventoryService struct{}

func (m *mockInventoryService) CheckAndHold(ctx context.Context, itemID string, qty int) (string, error) {
	if itemID == "sku_out_of_stock" {
		return "", errors.New("insufficient inventory")
	}
	return fmt.Sprintf("hold_%s_%d", itemID, qty), nil
}

func (m *mockInventoryService) ReleaseHold(ctx context.Context, reservationID string) error {
	fmt.Printf("  [Compensate] Released inventory hold: %s\n", reservationID)
	return nil
}

func (m *mockInventoryService) CommitStock(ctx context.Context, reservationID, paymentTxnID string) error {
	return nil
}

type mockPaymentService struct{}

func (m *mockPaymentService) ProcessPayment(ctx context.Context, userID string, amount float64, resID string) (string, error) {
	if amount > 1000.00 {
		return "", errors.New("insufficient credit limit")
	}
	return fmt.Sprintf("txn_charge_%s_%.0f", userID, amount), nil
}

func (m *mockPaymentService) RefundPayment(ctx context.Context, paymentTxnID string) error {
	fmt.Printf("  [Compensate] Refunded payment: %s\n", paymentTxnID)
	return nil
}

type mockNotificationService struct{}

func (m *mockNotificationService) SendConfirmation(ctx context.Context, email, orderID, txnID string) error {
	if email == "usr_bounce@example.com" {
		return errors.New("SMTP mailbox unavailable")
	}
	return nil
}

// -----------------------------------------------------------------------------
// 5. Execution Runner
// -----------------------------------------------------------------------------

func main() {
	orchestrator := NewOrderFulfillmentOrchestrator(
		&mockUserService{},
		&mockInventoryService{},
		&mockPaymentService{},
		&mockNotificationService{},
	)

	// Scenario 1: Successful end-to-end execution
	fmt.Println("=== Scenario 1: All 5 Dependent Steps Succeed ===")
	order1 := &OrderContext{
		OrderID:  "ORD-901",
		UserID:   "usr_sarah",
		ItemID:   "sku_macbook",
		Quantity: 1,
		Amount:   899.00,
	}

	if err := orchestrator.Execute(context.Background(), order1); err != nil {
		fmt.Printf("Order 1 failed: %v\n", err)
	} else {
		fmt.Println("Order 1 finished successfully!")
	}

	// Scenario 2: Payment fails after Inventory Hold -> Triggers Hold Release
	fmt.Println("\n=== Scenario 2: Payment Step Fails (Triggers Hold Rollback) ===")
	order2 := &OrderContext{
		OrderID:  "ORD-902",
		UserID:   "usr_sarah",
		ItemID:   "sku_macbook",
		Quantity: 1,
		Amount:   2500.00, // Exceeds payment limit
	}

	if err := orchestrator.Execute(context.Background(), order2); err != nil {
		fmt.Printf("Order 2 aborted: %v\n", err)
	}

	// Scenario 3: Notification fails after Payment -> Triggers Payment Refund + Hold Release
	fmt.Println("\n=== Scenario 3: Notification Step Fails (Triggers Multi-Step Rollback) ===")
	order3 := &OrderContext{
		OrderID:  "ORD-903",
		UserID:   "usr_bounce", // Triggers notification failure
		ItemID:   "sku_headphones",
		Quantity: 1,
		Amount:   150.00,
	}

	if err := orchestrator.Execute(context.Background(), order3); err != nil {
		fmt.Printf("Order 3 aborted: %v\n", err)
	}
}
