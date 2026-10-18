package main

import (
	"context"
	"fmt"
	"sort"
	"strconv"
	"strings"
	"time"
)

// -----------------------------------------------------------------------------
// 1. Domain Models
// -----------------------------------------------------------------------------

type LogEntry struct {
	Timestamp  time.Time
	Service    string
	Level      string
	StatusCode int
	LatencyMs  int
	Message    string
}

type AnalysisReport struct {
	TotalRequests int
	TotalErrors   int
	ErrorRate     float64
	AvgLatencyMs  float64
	P95LatencyMs  int
	ServiceErrors map[string]int
	GeneratedAt   time.Time
}

// -----------------------------------------------------------------------------
// 2. Batch Pipeline Stages
// -----------------------------------------------------------------------------

// Step 1: Collect raw logs from files, S3 buckets, or log aggregators
type LogCollector struct{}

func (c *LogCollector) CollectLogs(ctx context.Context, targetDate string) ([]string, error) {
	fmt.Printf("[1. Collect] Gathering raw log files for batch date: %s...\n", targetDate)

	// Simulated log records from distributed application nodes
	rawLogs := []string{
		"2026-10-16T02:00:10Z | auth-service | INFO | 200 | 45 | User authenticated",
		"2026-10-16T02:00:12Z | payment-api | INFO | 200 | 120 | Payment processed",
		"2026-10-16T02:01:05Z | payment-api | ERROR | 500 | 450 | Database connection timeout",
		"2026-10-16T02:01:18Z | order-service | INFO | 201 | 85 | Order created",
		"2026-10-16T02:02:40Z | auth-service | WARN | 401 | 30 | Invalid credentials",
		"2026-10-16T02:03:15Z | order-service | ERROR | 503 | 1200 | Upstream inventory down",
		"2026-10-16T02:03:50Z | payment-api | ERROR | 500 | 800 | Gateway unreachable",
		"2026-10-16T02:04:10Z | order-service | INFO | 200 | 65 | Order details retrieved",
		"2026-10-16T02:04:30Z | catalog-api | INFO | 200 | 18 | Product list cached",
	}

	return rawLogs, nil
}

// Step 2: Parse raw string logs into structured LogEntry structs
type LogParser struct{}

func (p *LogParser) Parse(rawLines []string) []LogEntry {
	fmt.Printf("[2. Parse] Parsing %d raw log entries...\n", len(rawLines))
	var entries []LogEntry

	for _, line := range rawLines {
		parts := strings.Split(line, " | ")
		if len(parts) != 6 {
			continue // Skip malformed lines
		}

		t, err := time.Parse(time.RFC3339, strings.TrimSpace(parts[0]))
		if err != nil {
			continue
		}

		status, err := strconv.Atoi(strings.TrimSpace(parts[3]))
		if err != nil {
			continue
		}

		latency, err := strconv.Atoi(strings.TrimSpace(parts[4]))
		if err != nil {
			continue
		}

		entries = append(entries, LogEntry{
			Timestamp:  t,
			Service:    strings.TrimSpace(parts[1]),
			Level:      strings.TrimSpace(parts[2]),
			StatusCode: status,
			LatencyMs:  latency,
			Message:    strings.TrimSpace(parts[5]),
		})
	}

	return entries
}

// Step 3: Analyze entries and calculate aggregate health metrics
type LogAnalyzer struct{}

func (a *LogAnalyzer) Analyze(entries []LogEntry) AnalysisReport {
	fmt.Println("[3. Analyze] Computing latency distribution and error breakdown...")

	var totalLatency int
	var latencies []int
	serviceErrors := make(map[string]int)
	totalErrors := 0

	for _, entry := range entries {
		totalLatency += entry.LatencyMs
		latencies = append(latencies, entry.LatencyMs)

		if entry.StatusCode >= 500 || entry.Level == "ERROR" {
			totalErrors++
			serviceErrors[entry.Service]++
		}
	}

	totalCount := len(entries)
	var avgLatency float64
	var p95Latency int
	var errorRate float64

	if totalCount > 0 {
		avgLatency = float64(totalLatency) / float64(totalCount)
		errorRate = (float64(totalErrors) / float64(totalCount)) * 100

		sort.Ints(latencies)
		p95Index := int(float64(totalCount) * 0.95)
		if p95Index >= totalCount {
			p95Index = totalCount - 1
		}
		p95Latency = latencies[p95Index]
	}

	return AnalysisReport{
		TotalRequests: totalCount,
		TotalErrors:   totalErrors,
		ErrorRate:     errorRate,
		AvgLatencyMs:  avgLatency,
		P95LatencyMs:  p95Latency,
		ServiceErrors: serviceErrors,
		GeneratedAt:   time.Now(),
	}
}

// Step 4: Generate a formatted textual report
type ReportGenerator struct{}

func (g *ReportGenerator) Generate(metrics AnalysisReport) string {
	fmt.Println("[4. Generate] Compiling daily health report...")

	var sb strings.Builder
	sb.WriteString("====================================================\n")
	sb.WriteString("             NIGHTLY SYSTEM HEALTH REPORT           \n")
	sb.WriteString(fmt.Sprintf("             Generated: %s\n", metrics.GeneratedAt.Format("2006-01-02 15:04:05 MST")))
	sb.WriteString("====================================================\n\n")

	sb.WriteString("SUMMARY METRICS:\n")
	sb.WriteString(fmt.Sprintf(" - Total Requests Processed : %d\n", metrics.TotalRequests))
	sb.WriteString(fmt.Sprintf(" - Total Server Errors (5xx): %d\n", metrics.TotalErrors))
	sb.WriteString(fmt.Sprintf(" - Overall Error Rate       : %.2f%%\n", metrics.ErrorRate))
	sb.WriteString(fmt.Sprintf(" - Average Latency          : %.1f ms\n", metrics.AvgLatencyMs))
	sb.WriteString(fmt.Sprintf(" - 95th Percentile Latency  : %d ms\n\n", metrics.P95LatencyMs))

	sb.WriteString("SERVICE ERROR BREAKDOWN:\n")
	if len(metrics.ServiceErrors) == 0 {
		sb.WriteString(" - None. All services healthy.\n")
	} else {
		for svc, count := range metrics.ServiceErrors {
			sb.WriteString(fmt.Sprintf(" - %-18s : %d error(s)\n", svc, count))
		}
	}
	sb.WriteString("\n====================================================\n")

	return sb.String()
}

// Step 5: Notify / Email stakeholders
type EmailService struct{}

func (e *EmailService) SendReport(recipients []string, subject, body string) error {
	fmt.Printf("[5. Email] Dispatching report to stakeholders: %s\n", strings.Join(recipients, ", "))
	fmt.Println("----------------- DISPATCHED EMAIL -----------------")
	fmt.Printf("Subject: %s\n", subject)
	fmt.Println(body)
	return nil
}

// -----------------------------------------------------------------------------
// 3. Batch Job Runner & Scheduler
// -----------------------------------------------------------------------------

type NightlyJobCoordinator struct {
	collector *LogCollector
	parser    *LogParser
	analyzer  *LogAnalyzer
	reporter  *ReportGenerator
	mailer    *EmailService
}

func NewNightlyJobCoordinator() *NightlyJobCoordinator {
	return &NightlyJobCoordinator{
		collector: &LogCollector{},
		parser:    &LogParser{},
		analyzer:  &LogAnalyzer{},
		reporter:  &ReportGenerator{},
		mailer:    &EmailService{},
	}
}

// Run executes the complete batch pipeline once
func (c *NightlyJobCoordinator) Run(ctx context.Context, batchDate string, recipients []string) error {
	startTime := time.Now()
	fmt.Printf("\n>>> Starting Batch Job for date: %s <<<\n", batchDate)

	// Step 1: Collect
	rawLogs, err := c.collector.CollectLogs(ctx, batchDate)
	if err != nil {
		return fmt.Errorf("collection failed: %w", err)
	}

	// Step 2: Parse
	entries := c.parser.Parse(rawLogs)

	// Step 3: Analyze
	metrics := c.analyzer.Analyze(entries)

	// Step 4: Generate Report
	reportContent := c.reporter.Generate(metrics)

	// Step 5: Email
	subject := fmt.Sprintf("[Nightly Report] System Health & Latency - %s", batchDate)
	if err := c.mailer.SendReport(recipients, subject, reportContent); err != nil {
		return fmt.Errorf("notification failed: %w", err)
	}

	fmt.Printf(">>> Batch Job Finished in %v <<<\n\n", time.Since(startTime).Round(time.Millisecond))
	return nil
}

// ScheduleCron simulates a cron scheduler running at periodic intervals or specific times
func (c *NightlyJobCoordinator) ScheduleCron(ctx context.Context, interval time.Duration, recipients []string) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			fmt.Println("[Scheduler] Stopped batch schedule listener.")
			return
		case t := <-ticker.C:
			dateStr := t.Format("2006-01-02")
			_ = c.Run(ctx, dateStr, recipients)
		}
	}
}

// -----------------------------------------------------------------------------
// 4. Main Runner
// -----------------------------------------------------------------------------

func main() {
	coordinator := NewNightlyJobCoordinator()
	stakeholders := []string{"sre-team@company.com", "ops-lead@company.com"}

	// 1. Immediate Execution (Manual or triggered by orchestrator/Airflow)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	currentBatchDate := time.Now().Format("2006-01-02")
	if err := coordinator.Run(ctx, currentBatchDate, stakeholders); err != nil {
		fmt.Printf("Batch job aborted: %v\n", err)
	}

	// 2. Demonstration of the Periodic / Cron Scheduler (Runs every 2 seconds for demo)
	fmt.Println("--- Starting Simulated Cron Scheduler (Runs every 2s, press Ctrl+C to stop) ---")
	cronCtx, cronCancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cronCancel()

	coordinator.ScheduleCron(cronCtx, 2*time.Second, stakeholders)
}
