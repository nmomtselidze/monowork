# Kafka Go Project

A comprehensive Kafka project with Go, demonstrating producer and consumer patterns using the Sarama library.

## Project Structure

```
kafka-go-project/
├── cmd/
│   ├── producer/    # Producer application
│   └── consumer/    # Consumer application
├── config/          # Configuration management
├── producer/        # Producer implementation
├── consumer/        # Consumer implementation
├── docker-compose.yml
├── Makefile
└── go.mod
```

## Features

- **Producer**: Sync producer that reads messages from a simple text file
- **Consumer**: Consumer group implementation with automatic rebalancing
- **Configuration**: Environment-based configuration with defaults
- **Docker Support**: Easy Kafka setup with Docker Compose
- **Best Practices**: Proper error handling, context support, and graceful shutdown
- **Non-programmer friendly**: Just edit `messages.txt` to change what gets sent

## Prerequisites

- Go 1.21 or higher
- Docker and Docker Compose

## Quick Start

### 1. Start Kafka

```bash
make start-kafka
```

This starts Zookeeper and Kafka using Docker Compose.

### 2. Create Topic

```bash
make create-topic
```

This creates a topic named `example-topic` with 3 partitions.

### 3. Install Dependencies

```bash
make tidy
```

### 4. Run Consumer

In one terminal:

```bash
make run-consumer
```

### Consumer Options

The consumer supports command-line flags to customize behavior:

```bash
# Use default topic and group
make run-consumer

# Specify a different topic
go run cmd/consumer/main.go -topic my-topic

# Specify a different consumer group
go run cmd/consumer/main.go -group my-group

# Combine both
go run cmd/consumer/main.go -topic my-topic -group my-group
```

**Why different consumer groups?**
- Each consumer group gets its own copy of messages
- Multiple groups can read the same topic independently
- Useful for different processing pipelines (analytics, logging, etc.)

### 5. Run Producer

In another terminal:

```bash
make run-producer
```

The producer reads messages from `messages.txt` (one message per line) and sends them all as a batch.

## Customizing Messages

Edit `messages.txt` to change what messages get sent. Each line becomes one message:

```
Your first message here
Your second message here
Your third message here
```

Empty lines are automatically skipped. No programming required!

### Using Different Message Files

You can create multiple message files and use them:

```bash
# Use default messages.txt
make run-producer

# Use a different file
go run cmd/producer/main.go messages_ecommerce.txt

# Or use the convenience command
make run-producer-ecommerce
```

### Example: E-commerce Messages

The project includes `messages_ecommerce.txt` with realistic e-commerce events:
- Order placements and confirmations
- Shipping notifications
- Inventory alerts
- Customer registrations
- Promo code usage
- Reviews and refunds

## Configuration

You can configure the application using environment variables:

- `KAFKA_BROKERS`: Kafka broker addresses (default: `localhost:9092`)
- `KAFKA_TOPIC`: Topic name (default: `example-topic`)
- `KAFKA_GROUP_ID`: Consumer group ID (default: `example-group`)

Example:

```bash
export KAFKA_BROKERS="localhost:9092"
export KAFKA_TOPIC="my-topic"
export KAFKA_GROUP_ID="my-group"
make run-consumer
```

## Building

Build the binaries:

```bash
make build
```

This creates `bin/producer` and `bin/consumer` executables.

## Cleanup

Stop Kafka:

```bash
make stop-kafka
```

Clean build artifacts:

```bash
make clean
```

## Architecture

### Producer

The producer uses Sarama's SyncProducer for reliable message delivery:
- `WaitForAll` acks for durability
- Automatic retries (max 5)
- Returns partition and offset on success
- Supports batch sending with goroutines

### Consumer

The consumer uses Sarama's ConsumerGroup for scalable consumption:
- Automatic partition assignment and rebalancing
- Round-robin balance strategy
- Offset management (starts from newest)
- Graceful shutdown with signal handling

## Learning Points

This project demonstrates:
1. Kafka producer/consumer patterns in Go
2. Sarama library usage
3. Consumer groups and partition assignment
4. Message serialization with JSON
5. Concurrent message sending
6. Graceful shutdown handling
7. Environment-based configuration
8. Docker Compose for Kafka setup

## Additional Commands

List topics:

```bash
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
```

Describe topic:

```bash
docker exec -it kafka kafka-topics --describe --topic example-topic --bootstrap-server localhost:9092
```

Read messages from console:

```bash
docker exec -it kafka kafka-console-consumer --topic example-topic --from-beginning --bootstrap-server localhost:9092
```

## Resources

- [Sarama Documentation](https://pkg.go.dev/github.com/IBM/sarama)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Confluent Platform](https://docs.confluent.io/)
