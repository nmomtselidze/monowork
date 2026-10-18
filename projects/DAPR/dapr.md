//Dapr Docs
https://docs.dapr.io/getting-started/install-dapr-cli/
//Quickstarts
https://github.com/dapr/quickstarts/tree/master
//Getting started
https://docs.dapr.io/getting-started/
// project=noetl-demo-19700101
"""
Project name=PubSubProject
Project number=472501976777
Project ID=bold-rain-341712
"""

//Getting started       --Documentation
https://docs.dapr.io/getting-started/
user@user:~$ source venv/bin/activate
(venv) user@user:~$ cd /media/user/dsk64/monowork/DAPR
(venv) user@user:/media/user/dsk64/DAPR$ cd quickstarts/service_invocation/python/http
 

wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

dapr uninstall --all
docker stop $(docker ps -q)
docker rm -f $(docker ps -aq)

dapr init

dapr -h

(venv) user@user:/media/user/dsk64/DAPR$ dapr init
⌛  Making the jump to hyperspace...
ℹ️  Container images will be pulled from Docker Hub
ℹ️  Installing runtime version 1.17.3
↙  Downloading binaries and setting up components...
Dapr runtime installed to /home/user/.dapr/bin, you may run the following to add it to your path if you want to run daprd directly:
    export PATH=$PATH:/home/user/.dapr/bin
✅  Downloading binaries and setting up components...
✅  Downloaded binaries and completed components set up.
ℹ️  daprd binary has been installed to /home/user/.dapr/bin.
ℹ️  dapr_placement container is running.
ℹ️  dapr_redis container is running.
ℹ️  dapr_zipkin container is running.
ℹ️  dapr_scheduler container is running.
ℹ️  Use `docker ps` to check running containers.
✅  Success! Dapr is up and running. To get started, go here: https://docs.dapr.io/getting-started

dapr --version      or dapr -v
CLI version: 1.17.0 
Runtime version: 1.17.3

docker ps

"""
xdg-open ~/.dapr
ls -la ~/.dapr
total 32
drwxr-xr-x  4 user user  4096 Apr 10 10:04 .
drwxr-x--- 77 user user 16384 Apr 10 10:04 ..
drwxr-xr-x  3 user user  4096 Apr 10 10:04 bin
drwxr-xr-x  2 user user  4096 Apr 10 10:04 components
-rw-r--r--  1 user user   187 Apr 10 10:04 config.yaml
"""
(venv) user@user:/media/user/dsk64/DAPR$ docker ps
CONTAINER ID   IMAGE                COMMAND                  CREATED         STATUS                   PORTS                                                                                                                                                                                        NAMES
063d3ed132aa   redis:6              "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes             0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp                                                                                                                                                  dapr_redis
413118cd6f5b   daprio/dapr:1.17.3   "./placement"            2 minutes ago   Up 2 minutes             0.0.0.0:50005->50005/tcp, [::]:50005->50005/tcp, 0.0.0.0:58080->8080/tcp, [::]:58080->8080/tcp, 0.0.0.0:59090->9090/tcp, [::]:59090->9090/tcp                                                dapr_placement
f75570eb21be   openzipkin/zipkin    "start-zipkin"           2 minutes ago   Up 2 minutes (healthy)   9410/tcp, 0.0.0.0:9411->9411/tcp, [::]:9411->9411/tcp                                                                                                                                        dapr_zipkin
705988b33a47   daprio/dapr:1.17.3   "./scheduler --etcd-…"   2 minutes ago   Up 2 minutes             0.0.0.0:2379->2379/tcp, [::]:2379->2379/tcp, 0.0.0.0:50006->50006/tcp, [::]:50006->50006/tcp, 0.0.0.0:58081->8080/tcp, [::]:58081->8080/tcp, 0.0.0.0:59091->9090/tcp, [::]:59091->9090/tcp   dapr_scheduler
(

# docker run

--In new window
curl -X POST http://localhost:41481/v1.0/state/statestore \
  -H "Content-Type: application/json" \
  -d '[{ "key": "name", "value": "Bruce Wayne" }]'
curl http://localhost:41481/v1.0/state/statestore/name
"Bruce Wayne"
Ctrl-C
--You are in first window
Ctrl-C
# dapr run --app-id myapp --dapr-http-port 3500 --enable-api-logging
docker run ubuntu echo "Hello" 2>&1 | cat

Digest: sha256:84e77dee7d1bc93fb029a45e3c6cb9d8aa4831ccfcc7103d36e876938d28895b
Status: Downloaded newer image for ubuntu:latest

Hello

dapr stop -f .
#======================================================

cd DAPR/quickstarts/order-processor
pip3 install -r requirements.txt
cd ../checkout
pip3 install -r requirements.txt
cd ..
pip install --upgrade "protobuf>=6.31.1"

dapr run -f .
..............
== APP - checkout == Order passed: {"orderId": 19}
Exited App successfully
Ctrl-C

git clone https://github.com/dapr/quickstarts.git
cd service_invocation/python/http/order-processor
pip3 install -r requirements.txt 

dapr run --app-port 8001 --app-id order-processor --app-protocol http --dapr-http-port 3501 -- python3 app.py
#-------------------------------
user@user:~$ source venv/bin/activate
(venv) user@user:~$ cd /media/user/dsk64/DAPR/quickstarts/pub_sub/python/http/checkout
(venv) user@user:/media/user/dsk64/DAPR/quickstarts/pub_sub/python/http/checkout$ pip3 install -r requirements.txt
dapr run --app-id checkout --app-protocol http --dapr-http-port 3500 -- python3 app.py

#-+-+-+-+-+-+
Publisher is in checkout service
1. In your app.py (The Publisher)
You typically place this inside a loop or an API endpoint.

Python
from dapr.clients import DaprClient

# Use a context manager to manage the connection to the Dapr sidecar
with DaprClient() as client:
    # This is the data you want to send
    order = {"orderId": "123", "item": "Shoes", "amount": 99.00}

    # This is the "Publish" command
    client.publish_event(
        pubsub_name='orderpubsub', # Must match the 'name' in your pubsub.yaml
        topic_name='new-orders',   # The "Channel" name
        data=order,                # The actual message
        data_content_type='application/json' 
    )
    
    print(f"Published order: {order}")

#+-+-+-+-
2. How the Subscriber receives it
You don't "pull" the message in the subscriber. Instead, you write a POST handler in your subscriber's code (e.g., using Flask or FastAPI). Dapr will "push" the message to this endpoint.

Python
from flask import Flask, request, jsonify

app = Flask(__name__)

# This is where the message "lands"
@app.route('/new-orders', methods=['POST'])
def my_subscriber():
    # Dapr sends the message in the request body
    content = request.json
    print(f"Subscriber received: {content['data']}")
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(port=8001)
#--------------------------
mportant: The "Glue" (The YAML file)For the code above to work, Dapr needs a configuration file (usually in a folder called components) that tells it what orderpubsub actually is (e.g., Redis, RabbitMQ, or Kafka).YAMLapiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: orderpubsub  # <--- This must match your Python code!
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
Summary of where to write what:ActionWhere to write itFile ExamplePublishingInside the app that starts the event.checkout/app.pySubscribingInside the app that reacts to the event.order-processor/app.pyConfiguringIn a standalone YAML file.components/pubsub.yaml
#=== Dapr workflows =====================================================================
cd /media/user/dsk64/DAPR/quickstarts/workflows/python/sdk/order-processor
dapr init
# cd ./order-processor
pip3 install -r requirements.txt
cd ..
#docker stop $(docker ps -q)
#ps ax | grep -E 'dapr|daprd|python3' | grep -v grep | awk '{print $1}' | xargs kill -9

(venv) user@user:/media/user/dsk64/DAPR/quickstarts/workflows/python/sdk$ dapr run -f .
ℹ️  Validating config and starting app "order-processor"
ℹ️  Started Dapr with app id "order-processor". HTTP Port: 37715. gRPC Port: 38313
ℹ️  Writing log files to directory : /media/user/dsk64/DAPR/quickstarts/workflows/python/sdk/order-processor/.dapr/logs
== APP - order-processor == *** Welcome to the Dapr Workflow console app sample!
== APP - order-processor == *** Using this app, you can place orders that start workflows.
== APP - order-processor == item: InventoryItem(item_name=Paperclip, per_item_cost=5, quantity=100)
== APP - order-processor == item: InventoryItem(item_name=Cars, per_item_cost=5000, quantity=10)
== APP - order-processor == item: InventoryItem(item_name=Computers, per_item_cost=500, quantity=100)
== APP - order-processor == ==========Begin the purchase of item:==========
== APP - order-processor == Starting order workflow, purchasing 1 of cars
== APP - order-processor == Received order 42a077f3316a45748e0db01c0e0abe8d for 1 cars at $5000 !
== APP - order-processor == Verifying inventory for order 42a077f3316a45748e0db01c0e0abe8d of 1 cars
== APP - order-processor == There are 10 Cars available for purchase
== APP - order-processor == Processing payment: 42a077f3316a45748e0db01c0e0abe8d for 1 cars at 5000 USD
== APP - order-processor == Payment for request ID 42a077f3316a45748e0db01c0e0abe8d processed successfully
== APP - order-processor == Checking inventory for order 42a077f3316a45748e0db01c0e0abe8d for 1 cars
== APP - order-processor == There are now 9 cars left in stock
== APP - order-processor == Order 42a077f3316a45748e0db01c0e0abe8d has completed!
== APP - order-processor == Workflow completed! Result: {"processed": true, "__durabletask_autoobject__": true}
Exited App successfully
Ctrl-C

View Traces in Zipkin UI - In your browser go to http://localhost:9411 to view the workflow trace spans in the Zipkin web UI.
The order-processor workflow should be viewable with the following output in the Zipkin web UI. Note: the openzipkin/zipkin docker container is launched on running dapr init.

#=== 🧠 Agentic Human-In-The-Loop — Durable Workflows with Dapr (+ OpenAI, Gemini, Anthropic) ========================================
cd /media/user/dsk64/DAPR/quickstarts/AI/workflows/external_system_interaction
cd gemini
pip install -r requirements.txt
GEMINI_API_KEY = "AIzaSyBYugvV9-NqtgI0uxCaciBwUZKrgMHAyDo"
(venv) user@user:/media/user/dsk64/DAPR/quickstarts/AI/workflows/external_system_interaction/gemini$ dapr run --app-id contract-review --app-port 8000 -- uvicorn app:app --reload
ℹ️  Starting Dapr with id contract-review. HTTP Port: 35719. gRPC Port: 46757
Flag --components-path has been deprecated, use --resources-path
.................
ℹ️  Updating metadata for appPID: 56034
ℹ️  Updating metadata for app command: uvicorn app:app --reload
✅  You're up and running! Both Dapr and your app logs will appear here.

INFO:     Started server process [56046]
INFO:     Waiting for application startup.
..................
INFO:     Started server process [56046]
INFO:     Waiting for application startup.
INFO[0002] work item stream established by user-agent: [grpc-python/1.80.0 grpc-c/53.0.0 (linux; chttp2)]  app_id=contract-review instance=user scope=dapr.runtime.wfengine type=log ver=1.17.4
== Dapr Workflow Runtime started ==
INFO:     Application startup complete.
