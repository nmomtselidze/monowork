cd /media/user/dsk64/monowork/DAPR/dapr-samples/bindings/$
""" 
======================================================
# Dapr Bindings (HTTP)

In this quickstart, you'll create a microservice to demonstrate Dapr's bindings API to work with external systems as inputs and outputs. The service listens to input binding events from a system CRON and then outputs the contents of local data to a PostgreSQL output binding.

Visit [this](https://docs.dapr.io/developing-applications/building-blocks/bindings/) link for more information about Dapr and Bindings.

> **Note:** This example leverages only HTTP REST. If you are looking for the example using the Dapr SDK [click here](../sdk).
=======================================================
"""
cd ../../db
#-----
sudo apt-get remove docker-compose
sudo apt-get update
sudo apt-get install docker-compose-plugin
#-----
docker compose up -d
# 2. Open a new terminal window, change directories to `./batch` in the quickstart directory and run:
cd /media/user/dsk64/monowork/DAPR/dapr-samples/bindings/
cd python/http
pip3 install -r requirements.txt
dapr run -f .
#=== From other terminals===========
user@user:/media/user/dsk64/monowork/DAPR$ source ~/venv/bin/activate
(venv) user@user:/media/user/dsk64/monowork/DAPR$ cd dapr-samples/bindings/db
docker exec postgres psql -U postgres -d orders -c "SELECT * FROM orders;"
# - 'orderid |  customer  | price'

#========================================================================
1. Stop everything
cd /media/user/dsk64/monowork/DAPR/dapr-samples/bindings/python/http
make stop
lsof -ti :5001 | xargs -r kill

2. Start everything
make run

3. Show results
# Open a second terminal and run:
dapr logs --app-id python-bindings
# --Or watch the running terminal — every 5 seconds you'll see:


Processing batch..insert into orders (orderid, customer, price) values (1, 'John Smith', 100.32)insert into orders (orderid, customer, price) values (2, 'Jane Bond', 15.4)insert into orders (orderid, customer, price) values (3, 'Tony James', 35.56)Finished processing batch

