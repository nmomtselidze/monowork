package main

import (
	"context"
	"flag"
	"log"
	"os"
	"os/signal"
	"syscall"

	"kafka-go-project/config"
	"kafka-go-project/consumer"
)

func main() {
	// Parse command line flags
	topic := flag.String("topic", "", "Override the default topic")
	groupID := flag.String("group", "", "Override the default consumer group ID")
	flag.Parse()

	cfg := config.Load()

	// Override config with command line flags if provided
	if *topic != "" {
		cfg.Topic = *topic
	}
	if *groupID != "" {
		cfg.GroupID = *groupID
	}

	c, err := consumer.NewConsumer(cfg.Brokers, cfg.Topic, cfg.GroupID)
	if err != nil {
		log.Fatalf("Failed to create consumer: %v", err)
	}
	defer c.Close()

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sigterm := make(chan os.Signal, 1)
	signal.Notify(sigterm, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		<-sigterm
		log.Println("Received termination signal, shutting down...")
		cancel()
	}()

	log.Printf("Starting consumer for topic: %s, group: %s", cfg.Topic, cfg.GroupID)

	if err := c.Consume(ctx); err != nil {
		log.Fatalf("Consumer error: %v", err)
	}

	log.Println("Consumer shutdown complete")
}
