#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
KIND_CLUSTER_NAME="ai-scheduler"
IMAGE_NAME="scheduler-backend:local"

# Build image
DOCKER_BUILDKIT=1 docker build -t "$IMAGE_NAME" -f "$ROOT_DIR/docker/backend.Dockerfile" "$ROOT_DIR"

# Load to kind
kind load docker-image "$IMAGE_NAME" --name "$KIND_CLUSTER_NAME"

echo "Loaded $IMAGE_NAME into kind cluster $KIND_CLUSTER_NAME"
