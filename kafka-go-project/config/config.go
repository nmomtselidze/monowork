package config

import (
	"log"
	"os"
)

type Config struct {
	Brokers  []string
	Topic    string
	GroupID  string
}

func Load() *Config {
	brokers := getEnv("KAFKA_BROKERS", "localhost:9092")
	topic := getEnv("KAFKA_TOPIC", "example-topic")
	groupID := getEnv("KAFKA_GROUP_ID", "example-group")

	return &Config{
		Brokers:  []string{brokers},
		Topic:    topic,
		GroupID:  groupID,
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	log.Printf("Using default value for %s: %s", key, defaultValue)
	return defaultValue
}
