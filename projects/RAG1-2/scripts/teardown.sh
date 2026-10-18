#!/usr/bin/env bash
set -euo pipefail

KIND_CLUSTER_NAME="ai-scheduler"

# Delete resources if cluster exists
if kubectl config get-contexts | grep -q "kind-$KIND_CLUSTER_NAME"; then
  kubectl config use-context "kind-$KIND_CLUSTER_NAME" >/dev/null 2>&1 || true
  kubectl delete deployment scheduler-backend --ignore-not-found
  kubectl delete service scheduler-backend --ignore-not-found
  kubectl delete statefulset postgres --ignore-not-found
  kubectl delete service postgres --ignore-not-found
  kubectl delete secret postgres-secret --ignore-not-found
  kubectl delete pvc postgres-pvc --ignore-not-found
fi

# Delete the kind cluster
if kind get clusters | grep -q "$KIND_CLUSTER_NAME"; then
  kind delete cluster --name "$KIND_CLUSTER_NAME"
fi

echo "Teardown complete."
