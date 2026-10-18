import json
from dapr.clients import DaprClient

with DaprClient() as client:
    order = {"orderId": "123", "item": "Shoes", "amount": 99.00}
    
    # Save it as a JSON string
    client.save_state(store_name="statestore", key="order1", value=json.dumps(order))
    
    # Immediately try to get it back to confirm
    result = client.get_state(store_name="statestore", key="order1")
    print(f"✅ Retrieved Order: {result.data.decode('utf-8')}")
