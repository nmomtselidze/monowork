//dapr-agents   --with
https://github.com/dapr/dapr-agents
//quickstarts   -- Dapr- Workflow
https://github.com/dapr/quickstarts
#------------------
Build reliable, stateful Retrieval-Augmented Generation (RAG) pipelines and multi-agent AI systems using Dapr Agents and Dapr Workflows 
to guarantee execution across services and handle interruptions.
#------------------

//Dapr Tutorials
https://docs.dapr.io/getting-started/tutorials/
//Concepts
https://docs.dapr.io/concepts/


# This kills the processes on the Dapr port and the App port
fuser -k 3500/tcp
fuser -k 3000/tcp
#-----
lsof -i :<PID>
kill -9 <PID>
#-----
# Kills all processes named daprd (the sidecar)
pkill -9 daprd
# Kills all processes named uvicorn (your app server)
pkill -9 uvicorn
# Check if the port is clear:
netstat -tulpn | grep :<PID>  or  netstat -tulpn | grep :
#================================
cd /media/user/dsk64/monowork/DAPR/
source ~/venv/bin/activate
deactivate
#================================
docker stop $(docker ps -q)
docker start $(docker ps -aq)   or docker start dapr_redis dapr_placement dapr_scheduler
docker ps
#================================
dapr uninstall
dapr init
dapr list
#================================================================================
# Move to your main DAPR directory
cd /media/user/dsk64/monowork/DAPR/

# Clone the quickstarts repo if you don't have it (or just pull the python part)
git clone https://github.com/dapr/quickstarts.git dapr-samples

# Navigate to the Python Actor Service
cd dapr-samples/actors/python/sdk/service
#==========================================
# Go to your main DAPR folder
cd /media/user/dsk64/monowork/DAPR/

# Clone the full repository (it's small)
git clone https://github.com/dapr/quickstarts.git official-quickstarts

# Now navigate to the Python actor service
cd official-quickstarts/actors/python/sdk/service
#==========================================
dapr run \
  --app-id demo-actor \
  --app-port 3000 \
  --app-protocol http \
  --dapr-http-port 3500 \
  -- uvicorn --port 3000 demo_actor_service:app
# From anoter terminal
cd /media/user/dsk64/monowork/DAPR/python-sdk/examples/demo_actor/demo_actor
python3 demo_actor_client.py

docker exec -it dapr_redis redis-cli HGETALL "demo-actor||DemoActor||1||mydata"

#===Done Apr.29 2026============================
(venv) user@user:~$ cd /media/user/dsk64/monowork/DAPR
(venv) user@user:/media/user/dsk64/monowork/DAPR$ 
(venv) user@user:/media/user/dsk64/monowork/DAPR$ git add .

(venv) user@user:/media/user/dsk64/monowork/DAPR$ 
# 1. Commit the changes
git commit -m "Add Dapr quickstarts and samples to monobox"

# 2. Add the remote (if not already done)
git remote add origin https://github.com/cybxlib/monobox.git

# 3. Push to GitHub
git push -u origin main
#===========================================
