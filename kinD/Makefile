# Makefile for Kubernetes Management with kind

# ============== Variables ==============
# Define your application name, docker image, and kubernetes details here.
# These variables can be overridden from the command line.
# Example: make docker-build DOCKER_IMAGE=my-new-app

APP_NAME ?= my-app
DOCKER_IMAGE ?= my-app
DOCKER_TAG ?= latest
KIND_CLUSTER_NAME ?= kind
KUBE_CONTEXT ?= kind-$(KIND_CLUSTER_NAME)
KUBE_NAMESPACE ?= default
KUBE_DEPLOYMENT ?= $(APP_NAME)-deployment
KUBE_SERVICE ?= $(APP_NAME)-service
KUBE_POD ?= $(shell kubectl get pods -n $(KUBE_NAMESPACE) -l app=$(APP_NAME) -o jsonpath="{.items[0].metadata.name}")

# ============== Docker Commands ==============

.PHONY: docker-build
docker-build:
	@echo "Building Docker image: $(strip $(DOCKER_IMAGE)):$(strip $(DOCKER_TAG))..."
	docker build -t $(strip $(DOCKER_IMAGE)):$(strip $(DOCKER_TAG)) .
# ============== kind Commands ==============

.PHONY: kind-cluster-up
kind-cluster-up:
	@echo "Creating kind cluster '$(KIND_CLUSTER_NAME)'..."
	kind create cluster --name $(KIND_CLUSTER_NAME)

.PHONY: kind-cluster-down
kind-cluster-down:
	@echo "Deleting kind cluster '$(KIND_CLUSTER_NAME)'..."
	kind delete cluster --name $(KIND_CLUSTER_NAME)

.PHONY: kind-load-image
kind-load-image:
	@echo "Loading Docker image '$(DOCKER_IMAGE):$(DOCKER_TAG)' into kind cluster..."
	kind load docker-image $(strip $(DOCKER_IMAGE)):$(strip $(DOCKER_TAG)) --name $(KIND_CLUSTER_NAME)

# ============== Kubernetes Commands ==============

.PHONY: k-set-context
k-set-context:
	@echo "Setting Kubernetes context to $(KUBE_CONTEXT)..."
	kubectl config use-context $(KUBE_CONTEXT)

.PHONY: k-apply
k-apply:
	@echo "Applying Kubernetes manifests recursively..."
	kubectl apply -f k8s/ --recursive

.PHONY: k-deploy
k-deploy: docker-build kind-load-image k-apply
	@echo "Deployment pipeline for kind finished."

.PHONY: k-status
k-status:
	@echo "Checking deployment status for $(KUBE_DEPLOYMENT)..."
	kubectl get deployment $(KUBE_DEPLOYMENT) -n $(KUBE_NAMESPACE)
	kubectl get pods -n $(KUBE_NAMESPACE) -l app=$(APP_NAME)

.PHONY: k-logs
k-logs:
	@echo "Tailing logs for pod $(KUBE_POD)..."
	kubectl logs -f $(KUBE_POD) -n $(KUBE_NAMESPACE)

.PHONY: k-describe-pod
k-describe-pod:
	@echo "Describing pod $(KUBE_POD)..."
	kubectl describe pod $(KUBE_POD) -n $(KUBE_NAMESPACE)

.PHONY: k-port-forward
k-port-forward:
	@echo "Forwarding port from service $(KUBE_SERVICE) to localhost:8080..."
	kubectl port-forward svc/$(KUBE_SERVICE) 8080:80 -n $(KUBE_NAMESPACE)

.PHONY: k-exec
k-exec:
	@echo "Executing a shell in pod $(KUBE_POD)..."
	kubectl exec -it $(KUBE_POD) -n $(KUBE_NAMESPACE) -- /bin/sh

.PHONY: k-delete
k-delete:
	@echo "Deleting Kubernetes resources..."
	kubectl delete -f k8s/

# ============== Pub/Sub Commands ==============

.PHONY: pubsub-emulator-up
pubsub-emulator-up:
	kubectl apply -f k8s/pubsub/emulator.yaml
	kubectl rollout status --timeout=120s deployment/pubsub-emulator
	kubectl apply -f k8s/pubsub/emulator-client.yaml
	kubectl apply -f k8s/pubsub/emulator-publisher-consumer.yaml

.PHONY: pubsub-emulator-down
pubsub-emulator-down:
	kubectl delete -f k8s/pubsub/emulator-publisher-consumer.yaml --ignore-not-found=true
	kubectl delete -f k8s/pubsub/emulator-client.yaml --ignore-not-found=true
	kubectl delete -f k8s/pubsub/emulator.yaml --ignore-not-found=true

.PHONY: pubsub-gcp-client
pubsub-gcp-client:
	kubectl apply -f k8s/pubsub/gcp-client.yaml

# ============== Helper Commands ==============

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  docker-build        Build the Docker image"
	@echo "  kind-cluster-up     Create the kind cluster"
	@echo "  kind-cluster-down   Delete the kind cluster"
	@echo "  kind-load-image     Load the Docker image into the kind cluster"
	@echo "  k-set-context       Set the Kubernetes context"
	@echo "  k-apply             Apply Kubernetes manifests"
	@echo "  k-deploy            Run the full deployment pipeline for kind (build, load, apply)"
	@echo "  k-status            Check the status of the deployment"
	@echo "  k-logs              Tail the logs of the application pod"
	@echo "  k-describe-pod      Describe the application pod"
	@echo "  k-port-forward      Forward a local port to the service"
	@echo "  k-exec              Execute a shell inside the application pod"
	@echo "  k-delete            Delete all Kubernetes resources for the application"
	@echo "  pubsub-emulator-up  Deploy the emulator, publisher, and consumer pods"
	@echo "  pubsub-emulator-down Remove the local Pub/Sub emulator and client pods"
	@echo "  pubsub-gcp-client   Deploy a client pod for real Google Cloud Pub/Sub"
	@echo "  help                Show this help message"
