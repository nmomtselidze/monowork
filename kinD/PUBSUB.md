# Google Pub/Sub with kind

This setup supports two independent development paths:

- A local Pub/Sub emulator running inside the kind cluster. It does not create
  or access Google Cloud resources.
- A client pod in kind that authenticates to real Google Cloud Pub/Sub.

## Prerequisites

Install Docker, kind, kubectl, and gcloud CLI. Create or select a kind cluster
before applying the manifests:

```sh
kind create cluster --name kind
kubectl config use-context kind-kind
```

The manifests live under `k8s/pubsub/` and are intentionally separate from the
basic example manifests.

## Local emulator

Deploy the emulator, a publisher pod, and a consumer pod. A small curl client
pod is also deployed for administration:

```sh
make pubsub-emulator-up
kubectl get pods -l 'app in (pubsub-emulator,pubsub-publisher,pubsub-consumer)'
```

### Create a topic and subscription

A topic is where publishers send messages. Consumers receive messages from a
subscription attached to that topic; Pub/Sub does not create a publisher or
consumer resource. The publisher and consumer are clients (pods in this demo).

Create a topic, then create a subscription that connects the consumer to it:

```sh
kubectl exec pubsub-emulator-client -- curl -sS -X PUT \
  'http://pubsub-emulator:8085/v1/projects/kind-pubsub/topics/demo'

kubectl exec pubsub-emulator-client -- curl -sS -X PUT \
  'http://pubsub-emulator:8085/v1/projects/kind-pubsub/subscriptions/demo-sub' \
  -H 'Content-Type: application/json' \
  -d '{"topic":"projects/kind-pubsub/topics/demo"}'
```

### Publish and consume a message

The publisher sends a base64-encoded message to the topic:

```sh
kubectl exec pubsub-publisher -- curl -sS -X POST \
  'http://pubsub-emulator:8085/v1/projects/kind-pubsub/topics/demo:publish' \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"data":"SGVsbG8gZnJvbSB0aGUgcHVibGlzaGVyIQ=="}]}'
```

The example message decodes to `Hello from the publisher!`. The consumer pulls
messages from its subscription:

```sh
kubectl exec pubsub-consumer -- curl -sS -X POST \
  'http://pubsub-emulator:8085/v1/projects/kind-pubsub/subscriptions/demo-sub:pull' \
  -H 'Content-Type: application/json' \
  -d '{"maxMessages":10}'
```

The response contains the message data (base64-encoded) and an `ackId`. A
consumer acknowledges a message after processing it, replacing
`ACK_ID_FROM_PULL_RESPONSE` with the returned value:

```sh
kubectl exec pubsub-consumer -- curl -sS -X POST \
  'http://pubsub-emulator:8085/v1/projects/kind-pubsub/subscriptions/demo-sub:acknowledge' \
  -H 'Content-Type: application/json' \
  -d '{"ackIds":["ACK_ID_FROM_PULL_RESPONSE"]}'
```

Acknowledged messages are not delivered again. If a message is not
acknowledged before its acknowledgement deadline, it can be delivered again.
For independent fan-out, create one subscription per consumer; consumers
sharing one subscription compete to receive messages.

The emulator stores state only for the lifetime of its pod. To use it from the
host, forward the service port in a separate terminal:

```sh
kubectl port-forward service/pubsub-emulator 8085:8085
```

Then set `PUBSUB_EMULATOR_HOST=localhost:8085` for a supported Google Cloud
client library. Client libraries use `PUBSUB_PROJECT_ID` as the project ID.

Remove the emulator and all demo client pods with `make pubsub-emulator-down`.

## Real Google Cloud Pub/Sub from kind

kind runs outside Google Cloud and does not provide Google workload identity.
For a local test, use a dedicated service account with only the permissions
needed by the application (for example, Pub/Sub Publisher), and a service
account key. Do not commit the key or grant broad project roles. For production
on GKE, use Workload Identity Federation instead of a service-account key.

Create or select a Google Cloud project, enable the Pub/Sub API, and create a
topic. Create a dedicated service account and grant it only the Pub/Sub
Publisher role for this local publishing example:

```sh
gcloud config set project YOUR_PROJECT_ID
gcloud services enable pubsub.googleapis.com
gcloud pubsub topics create demo
gcloud pubsub subscriptions create demo-sub --topic=demo

PROJECT_ID="$(gcloud config get-value project)"
SERVICE_ACCOUNT="kind-pubsub-client@${PROJECT_ID}.iam.gserviceaccount.com"
gcloud iam service-accounts create kind-pubsub-client --project="$PROJECT_ID"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/pubsub.publisher"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/pubsub.subscriber"
gcloud iam service-accounts keys create "$HOME/kind-pubsub-credentials.json" \
  --iam-account="$SERVICE_ACCOUNT" \
  --project="$PROJECT_ID"
```

Create the Kubernetes ConfigMap and Secret from local values. Set
`GOOGLE_APPLICATION_CREDENTIALS` to `$HOME/kind-pubsub-credentials.json` before
running the commands:

```sh
kubectl create configmap pubsub-gcp-config \
  --from-literal=project-id="$(gcloud config get-value project)"
kubectl create secret generic gcp-pubsub-credentials \
  --from-file=credentials.json="$GOOGLE_APPLICATION_CREDENTIALS"
```

Deploy the authenticated client pod and confirm it is ready:

```sh
make pubsub-gcp-client
kubectl get pod pubsub-gcp-client
```

The pod authenticates on startup. Publish a message to the real topic:

```sh
kubectl exec pubsub-gcp-client -- gcloud pubsub topics publish demo \
  --message="hello from kind" \
  --project="$(gcloud config get-value project)"
```

Pull and acknowledge messages from the subscription:

```sh
kubectl exec pubsub-gcp-client -- gcloud pubsub subscriptions pull demo-sub \
  --auto-ack --limit=10 \
  --project="$(gcloud config get-value project)"
```

Delete the client pod and credentials after testing:

```sh
kubectl delete -f k8s/pubsub/gcp-client.yaml
kubectl delete secret gcp-pubsub-credentials
kubectl delete configmap pubsub-gcp-config
```

Deleting the pod does not delete the Google Cloud topic. Manage cloud resources
separately with gcloud and the project's normal change controls.
