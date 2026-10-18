# https://gemini.google.com/app/6a4c5d2ce090e438?utm_source=app_launcher&utm_medium=owned&utm_campaign=base_all
# Include your standard rules
include ../../../docker.mk
include ../../../validate.mk

.PHONY: dev
dev: ## Full launch of the local development environment
	@echo "--- Starting infrastructure ---"
	$(MAKE) docker-up  # Assuming this command exists in docker.mk
	@echo "--- Checking dependencies ---"
	pip install -r requirements.txt
	@echo "--- Running migrations ---"
	python manage.py migrate

PHONY: help
help: ## Show help for all commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Example command with a description (using ##)
test: ## Run tests with code coverage
	pytest --cov=src
