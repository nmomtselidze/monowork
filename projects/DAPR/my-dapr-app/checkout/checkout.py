import time
from dapr.clients import DaprClient

with DaprClient() as client:
    for i in range(1, 11):
        order = {"orderId": i, "item": "Shoes", "amount": 99.00}

        client.publish_event(
            pubsub_name='order-pubsub',  # Matches 'name' in components/pubsub.yaml
            topic_name='new-orders',     # The channel name
            data=order,
            data_content_type='application/json',
        )

        print(f"Published order: {order}")
        time.sleep(1)
