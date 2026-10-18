from dapr.clients import DaprClient

with DaprClient() as client:
    result = client.get_state(store_name="statestore", key="order1")
    print(f"Retrieved Order: {result.data.decode('utf-8')}")
