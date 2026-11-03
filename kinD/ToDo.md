https://kind.sigs.k8s.io/

user@user:~$ source venv/bin/activate
1.Make directory --kinD
mkdir kinD
cd kinD                 or cd media/user/pendrive/kinD

2.Create Dockerfile 
cat <<EOF > Dockerfile
FROM busybox
CMD ["echo", "Hello from my custom image!"]
EOF

3.Run the docker build
docker build -t my-custom-app:1.0 .

4.Create cluster
kind create cluster # Default cluster context name is `kind`
    Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.27.3) 🖼 
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
    Set kubectl context to "kind-kind"

5.Load image into claster kind
kind load docker-image my-custom-app:1.0

6.Create a Pod Manifest  --pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
  - name: my-test-container
    # Use the exact image name you loaded into KinD
    image: my-custom-app:1.0
    # This is critical for using local images
    imagePullPolicy: Never

7.Execute the Pod Manifest  --https://greenwebpage.com/community/how-to-install-kubectl-on-ubuntu-24-04/
kubectl apply -f pod.yaml
    pod/test-pod created

8.Verify the Execution
kubectl get pods
NAME       READY   STATUS      RESTARTS      AGE
test-pod   0/1     Completed   2 (24s ago)   26s

9.View the container's logs
kubectl logs test-pod
    Hello from my custom image!

10.Drop cluster
kind delete cluster
    Deleted nodes: ["kind-control-plane"]
---------------------------
user@user:~$ kubectl version --client
Client Version: v1.33.4
Kustomize Version: v5.6.0
---------------------------

https://docs.pytorch.org/vision/main/tv_tensors.html


