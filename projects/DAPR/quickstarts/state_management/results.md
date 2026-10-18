
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

#===run===
cd state_management/python/sdk/order-processor
pip3 install -r requirements.txt

dapr run --app-id order-processor --resources-path ../../../resources/ -- python3 app.py

ℹ️  Starting Dapr with id order-processor. HTTP Port: 37749. gRPC Port: 39073
ℹ️  Checking if Dapr sidecar is listening on HTTP port 37749
== APP - order-processor == Saving Order: {'orderId': '1'}
== APP - order-processor == Result after get: b"{'orderId': '1'}"
== APP - order-processor == Deleting Order: {'orderId': '1'}
== APP - order-processor == Saving Order: {'orderId': '2'}
== APP - order-processor == Result after get: b"{'orderId': '2'}"
== APP - order-processor == Deleting Order: {'orderId': '2'}
== APP - order-processor == Saving Order: {'orderId': '3'}
== APP - order-processor == Result after get: b"{'orderId': '3'}"
== APP - order-processor == Deleting Order: {'orderId': '3'}
== APP - order-processor == Saving Order: {'orderId': '4'}
== APP - order-processor == Result after get: b"{'orderId': '4'}"
== APP - order-processor == Deleting Order: {'orderId': '4'}
== APP - order-processor == Saving Order: {'orderId': '5'}
== APP - order-processor == Result after get: b"{'orderId': '5'}"
== APP - order-processor == Deleting Order: {'orderId': '5'}
== APP - order-processor == Saving Order: {'orderId': '6'}
== APP - order-processor == Result after get: b"{'orderId': '6'}"
== APP - order-processor == Deleting Order: {'orderId': '6'}
== APP - order-processor == Saving Order: {'orderId': '7'}
== APP - order-processor == Result after get: b"{'orderId': '7'}"
== APP - order-processor == Deleting Order: {'orderId': '7'}
== APP - order-processor == Saving Order: {'orderId': '8'}
== APP - order-processor == Result after get: b"{'orderId': '8'}"
== APP - order-processor == Deleting Order: {'orderId': '8'}
== APP - order-processor == Saving Order: {'orderId': '9'}
== APP - order-processor == Result after get: b"{'orderId': '9'}"
== APP - order-processor == Deleting Order: {'orderId': '9'}
.......................
== APP - order-processor == Result after get: b"{'orderId': '99'}"
== APP - order-processor == Deleting Order: {'orderId': '99'}
Exited App successfully
