#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

KIND_CLUSTER_NAME="ai-scheduler"
CONFIG_FILE="$ROOT_DIR/k8s/kind-config.yaml"

if ! command -v kind >/dev/null 2>&1; then
  echo "ERROR: kind not found. Install from https://kind.sigs.k8s.io/" >&2
  exit 1
fi

kind create cluster --name "$KIND_CLUSTER_NAME" --config "$CONFIG_FILE" || true

kubectl cluster-info --context "kind-$KIND_CLUSTER_NAME"
