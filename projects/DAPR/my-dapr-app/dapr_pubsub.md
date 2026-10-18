To build a Python project using Dapr and Pub/Sub, the most modern approach is to use the Dapr Python SDK with FastAPI.

Here is a complete "Order Management" example consisting of two services: a Publisher (Checkout) and a Subscriber (Order Processor).

1. The Dapr Component (pubsub.yaml)
First, define your message broker. For local development, Redis is the standard, but you can swap type: pubsub.redis for pubsub.kafka or pubsub.gcp.pubsub later without changing your code.

YAML
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: order-pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
2. The Subscriber (order_processor.py)
This service uses the Dapr FastAPI extension. It automatically handles the /dapr/subscribe endpoint for you so Dapr knows which topics to push to your app.

Install requirements: pip install fastapi uvicorn dapr-ext-fastapi

Python
from fastapi import FastAPI
from dapr.ext.fastapi import DaprApp

app = FastAPI()
dapr_app = DaprApp(app)

# Dapr will POST messages to this endpoint automatically
@dapr_app.subscribe(pubsub='order-pubsub', topic='orders')
def order_handler(event_data: dict):
    print(f"Received order: {event_data['order_id']} for {event_data['item']}")
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6001)
3. The Publisher (checkout.py)
This script uses the DaprClient to send an event. It doesn't need to be a web server; it can be a background worker or a simple script.

Install requirements: pip install dapr

Python
import time
from dapr.clients import DaprClient

def publish_orders():
    with DaprClient() as client:
        for i in range(1, 6):
            order = {"order_id": i, "item": "Laptop"}
            
            # Publish the event
            client.publish_event(
                pubsub_name='order-pubsub',
                topic_name='orders',
                data=order,
                data_content_type='application/json'
            )
            print(f"Published order {i}")
            time.sleep(1)

if __name__ == "__main__":
    publish_orders()
4. How to Run It
You need the Dapr CLI installed and initialized (dapr init). Open two terminal windows:

Terminal 1: Start the Subscriber

Bash
dapr run --app-id processor --app-port 6001 --resources-path ./components -- python order_processor.py
Terminal 2: Start the Publisher

Bash
dapr run --app-id checkout --resources-path ./components -- python checkout.py
Why this is better than "Standard" Python:
Retries: If your order_processor is down, Dapr will automatically retry delivering the message based on your resiliency policy.

Tracing: If you have Zipkin or Jaeger running, you will see a full trace showing the jump from checkout.py to order_processor.py.

Portability: To move this to Google Cloud, you just update the pubsub.yaml to use pubsub.gcp.pubsub. You do not have to rewrite the Python code to use the Google Cloud SDK.

Are you planning to deploy this on Kubernetes or keep it in a local Docker environment?
#=== keep it in a local Docker environment ============================================
Running Dapr in a local Docker environment is actually the most common way to develop, as it mirrors how Dapr operates in Kubernetes. In this setup, your Python applications and the Dapr sidecars run as containers, usually managed by Docker Compose.

Here is how to structure your local Docker environment for the Python Pub/Sub project.

1. Project Structure
Organize your files like this:

Plaintext
my-dapr-app/
├── components/
│   └── pubsub.yaml
├── checkout/
│   ├── checkout.py
│   └── requirements.txt
├── processor/
│   ├── order_processor.py
│   └── requirements.txt
└── docker-compose.yml
#--------------------------------------------------------------
2. The Docker Compose File
This file is the "brain" of your local environment. It defines your Python apps, their corresponding Dapr sidecars, and the Redis state store/pubsub broker.

YAML
version: '3.8'
services:
  # 1. Redis (Our message broker)
  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"

  # 2. The Order Processor App
  processor:
    build: ./processor
    ports:
      - "6001:6001"
    depends_on:
      - redis

  # 3. The Processor's Dapr Sidecar
  processor-dapr:
    image: "daprio/daprd:latest"
    command: [
      "./daprd",
      "-app-id", "processor",
      "-app-port", "6001",
      "-components-path", "/components"
    ]
    volumes:
      - "./components:/components"
    depends_on:
      - processor
    network_mode: "service:processor"

  # 4. The Checkout App (Publisher)
  checkout:
    build: ./checkout
    depends_on:
      - redis

  # 5. The Checkout's Dapr Sidecar
  checkout-dapr:
    image: "daprio/daprd:latest"
    command: [
      "./daprd",
      "-app-id", "checkout",
      "-components-path", "/components"
    ]
    volumes:
      - "./components:/components"
    depends_on:
      - checkout
    network_mode: "service:checkout"
Wait, why network_mode: "service:..."? > In Docker Compose, Dapr sidecars need to talk to your app via localhost. By using this network mode, the Dapr container and your Python container share the same network stack, making them effectively the same "host."
#--------------------------------------------------------------
3. The Component File (components/pubsub.yaml)
Since everything is inside Docker, we point the Redis host to the service name defined in the compose file.

YAML
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: order-pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis:6379 # Points to the 'redis' service in docker-compose
  - name: redisPassword
    value: ""
#--------------------------------------------------------------
4. Dockerfiles
You’ll need a simple Dockerfile for each Python service.

Example for ./processor/Dockerfile:

Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "order_processor.py"]
(Repeat a similar one for the checkout service.)
#--------------------------------------------------------------
5. Running the Environment
From your project root, simply run:

Bash
docker-compose up --build
What happens next?
Redis starts up.

The Processor App starts and waits for requests on port 6001.

The Processor Dapr Sidecar connects to Redis and registers the subscription for the "orders" topic.

The Checkout App sends an order to its Checkout Dapr Sidecar.

The sidecar pushes that message into Redis.

The Processor Dapr Sidecar sees the new message and sends a POST request to your Processor App at http://localhost:6001/orders.

Pro-Tip for Local Dev
If you want to see exactly what is happening inside the message broker, you can add Dapr Dashboard to your docker-compose.yml. It provides a web UI to see your components and their health!

