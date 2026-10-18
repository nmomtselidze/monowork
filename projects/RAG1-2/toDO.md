# RAG Just Got Its Biggest Upgrade That Will Change AI Development in 2026
# https://medium.com/@CodingWithAbhi/graphrag-biggest-upgrade-ai-development-2026-33366891525d
#===============================================================
make help:
    @echo "Targets:"
    @echo "  make install         # create venv (if missing) and install deps"
    @echo "  make run-backend     # run FastAPI backend on :8080"
    @echo "  make run-ui          # run Tkinter UI (reads $$API_BASE, default http://localhost:8080)"
    @echo "  make run-ui-docker   # run Tkinter UI targeting Dockerized backend (http://localhost:8081)"
    @echo "  make run-ui-kind     # run Tkinter UI targeting KinD (http://localhost:8080)"
    @echo "  make docker-build    # build backend Docker image"
    @echo "  make docker-run      # run backend container mapping :8081->:8080"
    @echo "  make kind-create     # create KinD cluster"
    @echo "  make kind-build-load # build and load image into KinD"
    @echo "  make k8s-apply       # apply k8s manifests"
    @echo "  make k8s-teardown    # delete manifests and cluster"
#===============================================================
1. Go to directory and activate ~/venv/bin/
user@user:~$ python3 -m venv venv
user@user:~$ source venv/bin/activate
user@user:~$ cd /media/user/dsk64/monowork/RAG1-2
(venv) user@user:/media/user/dsk64/monowork/RAG1-2$ 
(venv) user@user:/media/user/dsk64/monowork/RAG1-2$ pip install -r requirements.txt

2. Stop port:8080 and All docker's containers
sudo fuser -k 8080/tcp       --kill port:8080 Linux Alternative
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)

3. run FastAPI backend on :8080
make run-backend
#--- In New Terminal---
4. Check heals of localhost:8080
curl http://localhost:8080/health

5. Go to docker, kill port:5432; Then run postgres database
cd /media/user/dsk64/monowork/RAG1-2/docker
sudo kill -9 $(sudo lsof -t -i:5432)  or  pkill 5432 or pkill samples/postgres:latest
docker run -d --name rag-db -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=orders \
  a3ce54f7c0e2

6. Start plsql and see \dt;
docker exec -it rag-db psql -U postgres -d orders -c "\dt"
           List of tables
 Schema |  Name  | Type  |  Owner   
--------+--------+-------+----------
 public | orders | table | postgres
(1 row)

7. Run Tkinter UI (reads $$API_BASE, default http://localhost:8080)"
cd ../
make run-ui
    Health: {'status': 'ok'}
    Schedule: {'status': 4, 'assignments': [{'patient_id': 1, 'procedure_id': 1, 'room_id': 101, 'staff_id': 1001, 'start': '09:00', 'end': '09:30'}]}

8. Crean
make clean
