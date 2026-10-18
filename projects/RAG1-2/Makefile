SHELL := /bin/bash

VENV ?= /home/user/venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn

.PHONY: help install run-backend run-ui run-ui-docker run-ui-kind docker-build docker-run kind-create kind-build-load k8s-apply k8s-teardown clean

help:
	@echo "Targets:"
	@echo "  make install         # create venv (if missing) and install deps"
	@echo "  make run-backend     # run FastAPI backend on :8080"
	@echo "  make run-ui          # run Tkinter UI (reads $$API_BASE, default http://localhost:8080)"
	@echo "  make run-ui-docker   # run Tkinter UI targeting Dockerized backend (http://localhost:8081)"
	@echo "  make run-ui-kind     # run Tkinter UI targeting KinD (http://localhost:8080)"
	@echo "  make docker-build    # build backend Docker image"
	@echo "  make docker-run      # run backend container mapping :8081->:8080"
	@echo "  make kind-create     # create KinD cluster"
	@echo "  make kind-build-load # build and load image into KinD"
	@echo "  make k8s-apply       # apply k8s manifests"
	@echo "  make k8s-teardown    # delete manifests and cluster"
	@echo "  make clean           # remove virtual enviroment and cached files"

$(VENV)/bin/activate:
	python3 -m venv $(VENV)

install: $(VENV)/bin/activate
	$(PIP) install --upgrade pip
	$(PIP) install -r RAG1-2/requirements.txt

run-backend:
	$(UVICORN) ai_sanatorium_scheduler.api.main:app --host 0.0.0.0 --port 8080 --reload


# UI defaults to local backend (8080). Override with: make run-ui API_BASE=http://localhost:8081
API_BASE ?= http://localhost:8080
run-ui:
	API_BASE=$(API_BASE) $(PYTHON) ui_tk/app.py

# Run UI targeting Dockerized backend on host port 8081
run-ui-docker:
	API_BASE=http://localhost:8081 $(PYTHON) ui_tk/app.py

# Run UI targeting KinD (NodePort 30080 mapped to host 8080)
run-ui-kind:
	API_BASE=http://localhost:8080 $(PYTHON) ui_tk/app.py

docker-build:
	docker build -f docker/backend.Dockerfile -t scheduler-backend:latest .

# Map host 8081 to container 8080 to avoid conflict with local dev on 8080
docker-run:
	docker run --rm -p 8081:8080 scheduler-backend:latest

kind-create:
	bash scripts/create_kind_cluster.sh

kind-build-load:
	bash scripts/build_and_load_backend.sh

k8s-apply:
	bash scripts/apply_infra.sh

k8s-teardown:
	bash scripts/teardown.sh

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache .mypy_cache
