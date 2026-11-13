package consumer

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/signal"
	"sync"
	"syscall"

	"github.com/IBM/sarama"
)

type Consumer struct {
	consumer sarama.ConsumerGroup
	handler  *ConsumerHandler
	topic    string
	groupID  string
}

type Message struct {
	ID        string `json:"id"`
	Content   string `json:"content"`
	Timestamp string `json:"timestamp"`
}

type ConsumerHandler struct {
	ready chan bool
}

func NewConsumerHandler() *ConsumerHandler {
	return &ConsumerHandler{
		ready: make(chan bool),
	}
}

func (h *ConsumerHandler) Setup(sarama.ConsumerGroupSession) error {
	close(h.ready)
	return nil
}

func (h *ConsumerHandler) Cleanup(sarama.ConsumerGroupSession) error {
	return nil
}

func (h *ConsumerHandler) ConsumeClaim(session sarama.ConsumerGroupSession, claim sarama.ConsumerGroupClaim) error {
	for msg := range claim.Messages() {
		var message Message
		if err := json.Unmarshal(msg.Value, &message); err != nil {
			log.Printf("Failed to unmarshal message: %v", err)
			continue
		}

		log.Printf("Message consumed - Partition: %d, Offset: %d, ID: %s, Content: %s",
			msg.Partition, msg.Offset, message.ID, message.Content)

		session.MarkMessage(msg, "")
	}
	return nil
}

func NewConsumer(brokers []string, topic, groupID string) (*Consumer, error) {
	config := sarama.NewConfig()
	config.Version = sarama.V2_5_0_0
	config.Consumer.Group.Rebalance.Strategy = sarama.NewBalanceStrategyRoundRobin()
	config.Consumer.Offsets.Initial = sarama.OffsetNewest

	consumer, err := sarama.NewConsumerGroup(brokers, groupID, config)
	if err != nil {
		return nil, fmt.Errorf("failed to create consumer group: %w", err)
	}

	handler := NewConsumerHandler()

	return &Consumer{
		consumer: consumer,
		handler:  handler,
		topic:    topic,
		groupID:  groupID,
	}, nil
}

func (c *Consumer) Consume(ctx context.Context) error {
	wg := &sync.WaitGroup{}
	wg.Add(1)

	go func() {
		defer wg.Done()
		for {
			if err := c.consumer.Consume(ctx, []string{c.topic}, c.handler); err != nil {
				if err == sarama.ErrClosedConsumerGroup {
					break
				}
				log.Printf("Error from consumer: %v", err)
			}

			if ctx.Err() != nil {
				return
			}
		}
	}()

	<-c.handler.ready
	log.Printf("Consumer up and running for topic: %s, group: %s", c.topic, c.groupID)

	sigterm := make(chan os.Signal, 1)
	signal.Notify(sigterm, syscall.SIGINT, syscall.SIGTERM)

	select {
	case <-ctx.Done():
		log.Println("Terminating: context cancelled")
	case <-sigterm:
		log.Println("Terminating: via signal")
	}

	wg.Wait()
	return c.consumer.Close()
}

func (c *Consumer) Close() error {
	return c.consumer.Close()
}
