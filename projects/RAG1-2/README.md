# AI-Sanatorium Scheduler (RAG1)

A modular Python 3.12+ project with:
- FastAPI backend (`ai_sanatorium_scheduler/api/main.py`)
- OR-Tools CP-SAT-based scheduler
- Optional Tkinter desktop UI (`ui_tk/app.py`)
- Docker image and KinD/Kubernetes manifests

## Prerequisites
- Python 3.12+
- Make
- (Optional) Docker
- (Optional) KinD and kubectl

## How to Run (using the Makefile)

The `Makefile` provides convenient targets for common tasks. The following sections describe the step-by-step process for different environments.

### 1) Local Development

This workflow runs both the backend API and the Tkinter UI directly on your local machine.

**Step 1: Install dependencies**

This will create a Python virtual environment in `.venv/` (if it doesn't exist) and install the required packages from `requirements.txt`.

```bash
make install
```

**Step 2: Run the backend API**

In your first terminal, run the FastAPI backend. It will be accessible at `http://localhost:8080`.

(lsof -i :8080; kill -9 <PID>)

```bash
make run-backend
```

You can check if it's running correctly by accessing the health check endpoint:
```bash
curl http://localhost:8080/health
```

**Step 3: Run the Tkinter UI**

In a second terminal, run the Tkinter UI. It will automatically connect to the local backend.

```bash
make run-ui
```

### 2) Docker

This workflow runs the backend inside a Docker container.

**Step 1: Build the Docker Image**

```bash
make docker-build
```

**Step 2: Run the Backend Container**

This command runs the backend container and maps port `8081` on your host to port `8080` inside the container. We use port 8081 to avoid conflicts with the local development setup.

```bash
make docker-run
```

**Step 3: Run the UI**

Run the UI locally, configured to connect to the Dockerized backend at `http://localhost:8081`.

```bash
make run-ui-docker
```

### 3) KinD/Kubernetes

This workflow deploys the entire application stack, including a PostgreSQL database, to a local Kubernetes cluster using KinD.

**Step 1: Create the KinD cluster**

This sets up a local Kubernetes cluster. You only need to do this once.

```bash
make kind-create
```

**Step 2: Build and Load the Backend Image**

This builds the backend Docker image and loads it directly into the KinD cluster, making it available for deployment.

```bash
make kind-build-load
```

**Step 3: Apply Kubernetes Manifests**

This deploys the backend, PostgreSQL, and all necessary services and secrets to the cluster.

```bash
make k8s-apply
```

**Step 4: Run the UI**

Run the UI locally, configured to connect to the backend running in the KinD cluster.

```bash
make run-ui-kind
```

**Tearing Down the KinD Environment**

To delete all the Kubernetes resources and the KinD cluster itself, run:

```bash
make k8s-teardown
```

## Endpoints
- GET `http://localhost:8080/health`
- POST `http://localhost:8080/schedule/run`

## Project structure (top-level)
- `ai_sanatorium_scheduler/` — backend service and solver
- `ui_tk/` — Tkinter UI
- `docker/` — Dockerfile(s)
- `scripts/` — DevOps scripts (KinD build/apply/teardown)
- `k8s/` — Kubernetes manifests
- `requirements.txt` — Python deps
