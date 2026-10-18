cd ~
user@user:~$ source venv/bin/activate
(venv) user@user:~$ cd /media/user/dsk64/monowork/DAPR
//Step 2: Set up the environment
(venv) user@user:/media/user/dsk64/monowork/DAPR$ cd quickstarts/service_invocation/python/http
cd ./order-processor
pip3 install -r requirements.txt
cd ../checkout
pip3 install -r requirements.txt
cd ..
//Step 3: Run the order-processor and checkout services (The order-processor service; The checkout service)
dapr run -f .
== APP - order-processor == Order received : Order { orderId = 1 }
== APP - checkout == Order passed: Order { OrderId = 1 }
....................................
== APP - order-processor == Order received : Order { orderId = 20 }
== APP - checkout == Order passed: Order { OrderId = 20 }
Exited App successfully
--from other terminal
cd ~
user@user:~$ source venv/bin/activate
cd quickstarts/service_invocation/python/http/order-processor
pip install -r requirements.txt 
--reed] Running dapr run -f . in this Quickstart started both the subscriber and publisher applications using the dapr.yaml Multi-App Run template file.  dapr.yaml Multi-App Run template file
cd /media/user/dsk64/monowork/DAPR/quickstarts/service_invocation/python/http/order-processor && source ~/venv/bin/activate && dapr run --app-port 8001 --app-id order-processor --app-protocol http --dapr-http-port 3501 -- python3 app.py

r start the server with a different port.
❌  The App process exited with error code: 1
ℹ️  Updating metadata for appPID: 46518
ℹ️  Updating metadata for app command: python3 app.py
✅  You're up and running! Both Dapr and your app logs will appear here.
ℹ️  
terminated signal received: shutting down
✅  Exited Dapr successfully
❌  Error exiting App: app exited with status 1 
dapr stop -f .
dapr run -f .

