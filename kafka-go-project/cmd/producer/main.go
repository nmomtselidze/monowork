package main

import (
	"bufio"
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"kafka-go-project/config"
	"kafka-go-project/producer"
)

func main() {
	cfg := config.Load()

	p, err := producer.NewProducer(cfg.Brokers, cfg.Topic)
	if err != nil {
		log.Fatalf("Failed to create producer: %v", err)
	}
	defer func() { _ = p.Close() }()

	ctx := context.Background()

	// Read messages from file (can be changed via command line argument)
	filename := "messages.txt"
	if len(os.Args) > 1 {
		filename = os.Args[1]
	}

	messages, err := readMessagesFromFile(filename)
	if err != nil {
		log.Fatalf("Failed to read messages file: %v", err)
	}

	if len(messages) == 0 {
		log.Println("No messages found in messages.txt")
		return
	}

	// Convert to producer messages
	var producerMessages []producer.Message
	for i, content := range messages {
		producerMessages = append(producerMessages, producer.Message{
			ID:        fmt.Sprintf("msg-%d", i+1),
			Content:   content,
			Timestamp: time.Now(),
		})
	}

	// Send all messages as a batch
	if err := p.SendBatch(ctx, producerMessages); err != nil {
		log.Fatalf("Failed to send batch: %v", err)
	}

	log.Printf("Successfully sent %d messages!", len(producerMessages))
}

func readMessagesFromFile(filename string) ([]string, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, fmt.Errorf("failed to open file: %w", err)
	}
	defer func() { _ = file.Close() }()

	var messages []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		// Skip empty lines
		if line != "" {
			messages = append(messages, line)
		}
	}

	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("error reading file: %w", err)
	}

	return messages, nil
}
