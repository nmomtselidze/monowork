(venv) user@user:/media/user/dsk64/monowork/DAPR/quickstarts$ cd actors/csharp/sdk/service
pip3 install dapr dapr-ext-fastapi uvicorn
dapr run \
  --app-id actorservice \
  --app-port 5001 \
  --app-protocol http \
  --dapr-http-port 56001 \
  --resources-path ../../../resources \
  -- python3 demo_actor_service.py
