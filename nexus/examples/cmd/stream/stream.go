package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// -----------------------------------------------------------------------------
// 1. Domain Event Models
// -----------------------------------------------------------------------------

type RawEvent struct {
	ID        string
	UserID    string
	Amount    float64
	Type      string // "TRANSACTION", "PING", "REFUND"
	Timestamp time.Time
}

type EnrichedEvent struct {
	RawEvent
	Country   string
	Tier      string
	RiskScore int // 0 (safe) to 100 (critical risk)
}

type AggregatedRecord struct {
	Event          EnrichedEvent
	WindowSpend    float64 // Cumulative spend in sliding window
	WindowCount    int     // Transaction count in sliding window
	WindowDuration time.Duration
}

// -----------------------------------------------------------------------------
// 2. Stage 1: Ingest
// -----------------------------------------------------------------------------

func Ingest(ctx context.Context, events []RawEvent) <-chan RawEvent {
	out := make(chan RawEvent)
	go func() {
		defer close(out)
		for _, evt := range events {
			select {
			case <-ctx.Done():
				return
			case out <- evt:
				fmt.Printf("[1. Ingest] Event %s | User: %s | Amount: $%.2f | Type: %s\n",
					evt.ID, evt.UserID, evt.Amount, evt.Type)
				time.Sleep(30 * time.Millisecond) // Simulated stream ingestion delay
			}
		}
	}()
	return out
}

// -----------------------------------------------------------------------------
// 3. Stage 2: Filter
// -----------------------------------------------------------------------------

// Filter drops non-actionable heartbeats and malformed zero/negative amounts
func Filter(ctx context.Context, in <-chan RawEvent) <-chan RawEvent {
	out := make(chan RawEvent)
	go func() {
		defer close(out)
		for evt := range in {
			if evt.Type == "PING" || evt.Amount <= 0 {
				fmt.Printf("  [2. Filter] Dropping noise/invalid event: %s (%s, $%.2f)\n",
					evt.ID, evt.Type, evt.Amount)
				continue
			}
			select {
			case <-ctx.Done():
				return
			case out <- evt:
			}
		}
	}()
	return out
}

// -----------------------------------------------------------------------------
// 4. Stage 3: Enrich
// -----------------------------------------------------------------------------

type UserProfile struct {
	Country   string
	Tier      string
	RiskScore int
}

// Enrich decorates raw events with user tier, country, and risk profile
func Enrich(ctx context.Context, in <-chan RawEvent) <-chan EnrichedEvent {
	out := make(chan EnrichedEvent)

	// Simulated fast in-memory user cache
	cache := map[string]UserProfile{
		"usr_101": {Country: "US", Tier: "VIP", RiskScore: 12},
		"usr_102": {Country: "DE", Tier: "Standard", RiskScore: 35},
		"usr_103": {Country: "NG", Tier: "Standard", RiskScore: 88},
	}

	go func() {
		defer close(out)
		for evt := range in {
			profile, exists := cache[evt.UserID]
			if !exists {
				profile = UserProfile{Country: "Unknown", Tier: "Standard", RiskScore: 50}
			}

			enriched := EnrichedEvent{
				RawEvent:  evt,
				Country:   profile.Country,
				Tier:      profile.Tier,
				RiskScore: profile.RiskScore,
			}

			fmt.Printf("  [3. Enrich] Event %s -> Country: %s | Tier: %s | Risk: %d\n",
				enriched.ID, enriched.Country, enriched.Tier, enriched.RiskScore)

			select {
			case <-ctx.Done():
				return
			case out <- enriched:
			}
		}
	}()
	return out
}

// -----------------------------------------------------------------------------
// 5. Stage 4: Aggregate (Sliding Window Velocity)
// -----------------------------------------------------------------------------

type windowItem struct {
	amount    float64
	timestamp time.Time
}

// Aggregate tracks rolling spend and event frequency per user across windowDuration
func Aggregate(ctx context.Context, windowDuration time.Duration, in <-chan EnrichedEvent) <-chan AggregatedRecord {
	out := make(chan AggregatedRecord)
	windows := make(map[string][]windowItem)

	go func() {
		defer close(out)
		for evt := range in {
			now := evt.Timestamp
			cutoff := now.Add(-windowDuration)

			// Evict expired entries outside the sliding time frame
			var active []windowItem
			var windowSpend float64
			for _, item := range windows[evt.UserID] {
				if item.timestamp.After(cutoff) {
					active = append(active, item)
					windowSpend += item.amount
				}
			}

			// Add current event to state
			active = append(active, windowItem{amount: evt.Amount, timestamp: now})
			windowSpend += evt.Amount
			windows[evt.UserID] = active

			record := AggregatedRecord{
				Event:          evt,
				WindowSpend:    windowSpend,
				WindowCount:    len(active),
				WindowDuration: windowDuration,
			}

			fmt.Printf("  [4. Aggregate] User %s: Rolling %v spend = $%.2f (%d txns)\n",
				evt.UserID, windowDuration, record.WindowSpend, record.WindowCount)

			select {
			case <-ctx.Done():
				return
			case out <- record:
			}
		}
	}()
	return out
}

// -----------------------------------------------------------------------------
// 6. Stages 5 & 6: Store and Alert
// -----------------------------------------------------------------------------

type StorageSink struct {
	mu      sync.Mutex
	records []AggregatedRecord
}

func (s *StorageSink) Save(rec AggregatedRecord) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.records = append(s.records, rec)
	fmt.Printf("  [5. Store] Saved %s to persistence sink (Total stored: %d)\n",
		rec.Event.ID, len(s.records))
}

// StoreAndAlert persists records and dispatches alerts on anomaly triggers
func StoreAndAlert(in <-chan AggregatedRecord, sink *StorageSink) {
	for rec := range in {
		// Stage 5: Store
		sink.Save(rec)

		// Stage 6: Alert Rules
		// Rule A: Velocity spike — user spend exceeds $4,000 within the rolling window
		if rec.WindowSpend > 4000.00 {
			fmt.Printf("  [6. ALERT ⚠️] Velocity Spike! User %s spent $%.2f within %v (Threshold: $4,000.00)\n",
				rec.Event.UserID, rec.WindowSpend, rec.WindowDuration)
		}

		// Rule B: High-Risk outlier — RiskScore > 80 with single transaction > $1,000
		if rec.Event.RiskScore > 80 && rec.Event.Amount > 1000.00 {
			fmt.Printf("  [6. ALERT 🚨] Fraud Risk! User %s (RiskScore: %d, Origin: %s) charged $%.2f\n",
				rec.Event.UserID, rec.Event.RiskScore, rec.Event.Country, rec.Event.Amount)
		}
	}
}

// -----------------------------------------------------------------------------
// 7. Pipeline Orchestration
// -----------------------------------------------------------------------------

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	now := time.Now()

	// Simulated live stream containing valid transactions, noise, and suspicious bursts
	streamInput := []RawEvent{
		{ID: "evt_001", UserID: "usr_101", Amount: 250.00, Type: "TRANSACTION", Timestamp: now},
		{ID: "evt_002", UserID: "usr_102", Amount: 0.00, Type: "PING", Timestamp: now.Add(1 * time.Second)},
		{ID: "evt_003", UserID: "usr_102", Amount: 850.00, Type: "TRANSACTION", Timestamp: now.Add(2 * time.Second)},
		{ID: "evt_004", UserID: "usr_103", Amount: 1400.00, Type: "TRANSACTION", Timestamp: now.Add(3 * time.Second)},
		{ID: "evt_005", UserID: "usr_101", Amount: 4200.00, Type: "TRANSACTION", Timestamp: now.Add(4 * time.Second)},
	}

	storage := &StorageSink{}
	slidingWindow := 10 * time.Second

	fmt.Println("=== Starting Real-Time Event Processing Pipeline ===")

	// Connect pipeline stages
	rawStream := Ingest(ctx, streamInput)
	filteredStream := Filter(ctx, rawStream)
	enrichedStream := Enrich(ctx, filteredStream)
	aggregatedStream := Aggregate(ctx, slidingWindow, enrichedStream)

	// Consume, persist, and alert
	StoreAndAlert(aggregatedStream, storage)

	fmt.Println("\n=== Pipeline Execution Completed ===")
}
