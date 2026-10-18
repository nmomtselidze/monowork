
#===state-management===
== APP - order-processor == Result after get: b"{'orderId': '97'}"
== APP - order-processor == Deleting Order: {'orderId': '97'}
== APP - order-processor == Saving Order: {'orderId': '98'}
== APP - order-processor == Result after get: b"{'orderId': '98'}"
== APP - order-processor == Deleting Order: {'orderId': '98'}
== APP - order-processor == Saving Order: {'orderId': '99'}
== APP - order-processor == Result after get: b"{'orderId': '99'}"
== APP - order-processor == Deleting Order: {'orderId': '99'}
Exited App successfully

#===
cd state_management/python/sdk/order-processor
pip3 install -r requirements.txt
dapr run --app-id order-processor --resources-path ../../../resources/ -- python3 app.py
