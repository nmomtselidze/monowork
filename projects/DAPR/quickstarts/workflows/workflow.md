

#===workflow order-processor===
ℹ️  Validating config and starting app "order-processor"
ℹ️  Started Dapr with app id "order-processor". HTTP Port: 37669. gRPC Port: 33097
ℹ️  Writing log files to directory : /media/user/dsk64/monowork/DAPR/quickstarts/workflows/python/sdk/order-processor/.dapr/logs
== APP - order-processor == *** Welcome to the Dapr Workflow console app sample!
== APP - order-processor == *** Using this app, you can place orders that start workflows.
== APP - order-processor == item: InventoryItem(item_name=Paperclip, per_item_cost=5, quantity=100)
== APP - order-processor == item: InventoryItem(item_name=Cars, per_item_cost=5000, quantity=10)
== APP - order-processor == item: InventoryItem(item_name=Computers, per_item_cost=500, quantity=100)
== APP - order-processor == ==========Begin the purchase of item:==========
== APP - order-processor == Starting order workflow, purchasing 1 of cars
== APP - order-processor == Received order b1f84972d17f4d77b12a74ce46c470a8 for 1 cars at $5000 !
== APP - order-processor == Verifying inventory for order b1f84972d17f4d77b12a74ce46c470a8 of 1 cars
== APP - order-processor == There are 10 Cars available for purchase
== APP - order-processor == Processing payment: b1f84972d17f4d77b12a74ce46c470a8 for 1 cars at 5000 USD
== APP - order-processor == Payment for request ID b1f84972d17f4d77b12a74ce46c470a8 processed successfully
== APP - order-processor == Checking inventory for order b1f84972d17f4d77b12a74ce46c470a8 for 1 cars
== APP - order-processor == There are now 9 cars left in stock
== APP - order-processor == Order b1f84972d17f4d77b12a74ce46c470a8 has completed!
== APP - order-processor == Workflow completed! Result: {"processed": true, "__durabletask_autoobject__": true}
Exited App successfully

#=== (Optional) Step 4: View in Zipkin ===
docker run -d -p 9411:9411 openzipkin/zipkin
Zipkin UI is available at: http://localhost:9411

#=== history ===
dapr workflow history e4d3807c --app-id order-processor
dapr workflow list --app-id order-processor

user@user:~$ docker exec dapr_redis redis-cli KEYS "*"
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000006
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000011
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000000
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||customStatus
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000012
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000009
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000010
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000008
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000007
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000001
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000005
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000013
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000015
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000003
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||metadata
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000013
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000004
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000002
order-processor||computers
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||metadata
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||customStatus
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000016
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000006
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000015
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000000
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000009
order-processor||paperclip
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000014
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000016
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000017
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000004
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000005
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000002
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000014
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000011
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000017
order-processor||cars
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000012
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000007
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000001
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000010
order-processor||dapr.internal.default.order-processor.workflow||8cef1a78f28246728f114d8795dc1da5||history-000003
order-processor||dapr.internal.default.order-processor.workflow||b1f84972d17f4d77b12a74ce46c470a8||history-000008
orders

