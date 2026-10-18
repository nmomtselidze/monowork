include ../../../docker.mk
include ../../../validate.mk

# Variables specific to this sample
APP_NAME=python-bindings-sample
DAPR_APP_ID=python-bindings
COMPONENTS_PATH=../../components
PYTHON_APP=batch/app.py
APP_PORT=5001

.PHONY: all install run stop

all: install

install: ## Install requirements
	pip3 install --break-system-packages -r batch/requirements.txt

run: ## Run the Python application with Dapr
	dapr run --app-id $(DAPR_APP_ID) \
		 --app-protocol http \
		 --app-port $(APP_PORT) \
		 --resources-path $(COMPONENTS_PATH) \
		 python3 $(PYTHON_APP)

stop: ## Stop the Dapr application
	dapr stop --app-id $(DAPR_APP_ID)		# pkill daprd;  pkill python3

# These targets are often expected by the included docker.mk
build:
	docker build -t $(APP_NAME):latest .

test:
	# Add your python test command here, e.g., pytest
	python3 -m pytest

