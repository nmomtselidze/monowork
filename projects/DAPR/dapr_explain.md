Dapr is a runtime for building distributed applications without wiring all the distributed-systems plumbing directly into your app code.

In practice, it gives your app a sidecar process and a standard HTTP/gRPC API for common platform problems such as state storage, pub/sub messaging, service-to-service calls, secrets, bindings, workflows, and observability. Instead of writing custom code for Redis, Kafka, service discovery, retries, tracing, or cloud-specific SDKs everywhere, your app talks to Dapr and Dapr talks to those backend components.

What it is for:

Simplifying microservices. It standardizes things like invoking another service, saving state, or publishing an event.
Reducing vendor lock-in. Your app code can stay mostly the same while you swap components underneath, like Redis to Cosmos DB or RabbitMQ to Kafka.
Adding distributed-system features safely. Dapr includes retries, mTLS support in some environments, tracing, metrics, and resiliency features.
Speeding up local development. You can run services locally with Dapr and test APIs like state store or pub/sub without deploying to Kubernetes first.
How to think about it:

Your app stays focused on business logic.
Dapr handles the infrastructure-facing concerns.
You interact with Dapr through sidecar APIs and component config files.
A simple example:

Without Dapr: your app imports a Redis client, connects, handles auth, retries, and storage logic itself.
With Dapr: your app sends a request to Dapr’s state API like POST /v1.0/state/statestore, and Dapr writes to Redis based on its configured component.
So the short version is: Dapr is for making distributed apps easier to build, run, and move between environments by abstracting common infrastructure concerns behind a consistent runtime API.

If you want, I can explain it next in one of these ways:

“Dapr in plain beginner terms”
“How Dapr compares to Docker/Kubernetes”
“What each command you ran is doing”
