#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
KIND_CLUSTER_NAME="ai-scheduler"

kubectl config use-context "kind-$KIND_CLUSTER_NAME" >/dev/null 2>&1 || true

# Apply Postgres manifests
kubectl apply -f "$ROOT_DIR/k8s/postgres/secret.yaml"
kubectl apply -f "$ROOT_DIR/k8s/postgres/service.yaml"
kubectl apply -f "$ROOT_DIR/k8s/postgres/statefulset.yaml"

echo "Waiting for Postgres to be ready..."
kubectl rollout status statefulset/postgres --timeout=120s

# Apply backend manifests
kubectl apply -f "$ROOT_DIR/k8s/backend/deployment.yaml"
kubectl apply -f "$ROOT_DIR/k8s/backend/service.yaml"

echo "Waiting for backend to be ready..."
kubectl rollout status deployment/scheduler-backend --timeout=120s

echo "Backend should be reachable at http://localhost:8080/health"
