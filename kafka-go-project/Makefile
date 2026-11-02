.PHONY: help start-kafka stop-kafka create-topic run-producer run-consumer build tidy clean

help:
	@echo "Available commands:"
	@echo "  make start-kafka               - Start Kafka and Zookeeper with Docker Compose"
	@echo "  make stop-kafka                - Stop Kafka and Zookeeper"
	@echo "  make create-topic              - Create the default topic (example-topic)"
	@echo "  make create-custom-topic       - Create custom topic (my-topic)"
	@echo "  make create-ecommerce-topics   - Create e-commerce topics (orders, payments, inventory)"
	@echo ""
	@echo "Producer commands:"
	@echo "  make run-producer              - Run producer (uses messages.txt to example-topic)"
	@echo "  make run-producer-ecommerce    - Run producer with e-commerce messages"
	@echo "  make run-producer-custom       - Run producer sending to my-topic"
	@echo "  make run-producer-orders       - Run producer sending to orders topic"
	@echo "  make run-producer-payments     - Run producer sending to payments topic"
	@echo "  make run-producer-inventory    - Run producer sending to inventory topic"
	@echo ""
	@echo "Consumer commands:"
	@echo "  make run-consumer              - Run consumer (example-topic, example-group)"
	@echo "  make run-consumer-ecommerce    - Run consumer with ecommerce group"
	@echo "  make run-consumer-custom       - Run consumer for my-topic with my-group"
	@echo "  make run-consumer-orders       - Run consumer for orders topic"
	@echo "  make run-consumer-payments     - Run consumer for payments topic"
	@echo "  make run-consumer-inventory    - Run consumer for inventory topic"
	@echo ""
	@echo "Other:"
	@echo "  make build                      - Build the producer and consumer"
	@echo "  make tidy                       - Tidy Go modules"
	@echo "  make clean                      - Clean build artifacts"

start-kafka:
	docker compose up -d

stop-kafka:
	docker compose down

create-topic:
	docker exec -it kafka kafka-topics --create --topic example-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

create-custom-topic:
	docker exec -it kafka kafka-topics --create --topic my-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

create-ecommerce-topics:
	docker exec -it kafka kafka-topics --create --topic orders --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
	docker exec -it kafka kafka-topics --create --topic payments --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
	docker exec -it kafka kafka-topics --create --topic inventory --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

run-producer:
	go run cmd/producer/main.go

run-producer-ecommerce:
	go run cmd/producer/main.go messages_ecommerce.txt

run-producer-custom:
	KAFKA_TOPIC=my-topic go run cmd/producer/main.go

# E-commerce producer commands
run-producer-orders:
	KAFKA_TOPIC=orders go run cmd/producer/main.go

run-producer-payments:
	KAFKA_TOPIC=payments go run cmd/producer/main.go

run-producer-inventory:
	KAFKA_TOPIC=inventory go run cmd/producer/main.go

run-consumer:
	go run cmd/consumer/main.go

run-consumer-ecommerce:
	go run cmd/consumer/main.go -topic example-topic -group ecommerce-group

run-consumer-custom:
	go run cmd/consumer/main.go -topic my-topic -group my-group

# E-commerce consumer commands
run-consumer-orders:
	go run cmd/consumer/main.go -topic orders -group order-processor

run-consumer-payments:
	go run cmd/consumer/main.go -topic payments -group payment-service

run-consumer-inventory:
	go run cmd/consumer/main.go -topic inventory -group stock-updater

build:
	go build -o bin/producer cmd/producer/main.go
	go build -o bin/consumer cmd/consumer/main.go

tidy:
	go mod tidy

clean:
	rm -rf bin/
