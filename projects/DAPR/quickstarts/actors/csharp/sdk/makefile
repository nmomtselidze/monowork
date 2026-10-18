include ../../../docker.mk
include ../../../validate.mk

.PHONY: help
help:
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z_-]+:.*## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(firstword $(MAKEFILE_LIST))

start-checkout:		# From http
	dapr run --app-id checkout --app-port 5001 -- python checkout/app.py

start-processor:
	dapr run --app-id order-processor --app-port 5002 -- python order-processor/app.py

# Example command with a description (using ##)
test: ## Run tests with code coverage
	curl http://localhost:5001/health || true
	curl http://localhost:5002/health || true

c