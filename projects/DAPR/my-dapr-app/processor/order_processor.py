from fastapi import FastAPI
from dapr.ext.fastapi import DaprApp
import uvicorn

app = FastAPI()
dapr_app = DaprApp(app)

# Dapr pushes messages to this endpoint
@dapr_app.subscribe(pubsub='order-pubsub', topic='new-orders')
def order_subscriber(event):
    print(f"Subscriber received: {event.data}")
    return {"success": True}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
