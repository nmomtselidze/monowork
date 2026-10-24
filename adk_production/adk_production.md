//adk developer   --python
https://adk.dev/get-started/python/


source .venv/bin/activate

cd /media/user/dsk64/Multi_ADK/adk_production/my_agent
cd /mnt/usb-Seagate_BUP_Slim_BL_NA9DEHY2-0:0-part1/pendrive/01_Projects/adk_production

cd my_agent && go test ./..

kill -9 $(lsof -t -i:8000)
go run agent.go web -port 8000 api webui -api_server_address http://localhost:8000/api

lsof -t -i:8000
kill -9 <PID>

cd my_agent
adk web --port 8000

http://127.0.0.1:8000

#======================================================

go mod init my-agent/main
go get google.golang.org/adk/v2
go mod tidy

#=====================================================
cd /mnt/usb-Seagate_BUP_Slim_BL_NA9DEHY2-0:0-part1/pendrive/01_Projects/adk_production/my_agent

