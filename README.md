## Step for deploy in Kub cluster
1. Copy config to your kube config 
```bash
cp config.yaml ~/.kube/config 
```

2. Always make new namespace

```yaml
kind: Namespace
apiVersion: v1
metadata:
  name: flask-app
```

3. Make a deployment

```yaml

apiVersion: v1
kind: Service
metadata:
  name: flask
  namespace: flask-app
  labels:
    app: flask
spec:
  ports:
  - port: 5000
  selector:
    app: flask
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask
  namespace: flask-app
  labels:
    app: flask
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask
  template:
    metadata:
      labels:
        app: flask
    spec:
      containers:
      - name: flask
        image: bkrmdahal/flask_app:latest
        resources:
          limits:
            cpu: 1000m
          requests:
            cpu: 100m
        env:
          - name: REDIS_HOST
            value: http://redis:6378
        ports:
        - containerPort: 5000

```

4. check deployment 
```bash
echo "check all resource"
kubectl get all --namespace flask-app 

echo "check only the requirment"
kubectl rollout status deployment/flask --namespace=flask-app
```

5. port forwarding 

```bash
kubectl port-forward <<POD_NMAE>> 5000:5000 --namespace flask-app  

```

6. setup ingress

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/mandatory.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/provider/cloud-generic.yaml
```

7. Added Ingress

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: echo-ingress
  annotations:  
    kubernetes.io/ingress.class: nginx
spec:

  tls:
  - hosts:
    - test.rpy3.com
    secretName: secret/custom-tls-certs
  rules:
  - host: test.rpy3.com
    http:
      paths:
      - backend:
          serviceName: flask
          servicePort: 5000
        path: /api
```

8. apply changes to nod using yaml edit
```bash
kubectl apply -f flask_deployment.yaml   
```

9. [Kubernetes cheat sheets](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

10. Delete the namespace ( deletes all resources on that namespace)

```bash
kubectl delete namespaces flask-app   
```

11. Make secrets from files

```bash
kubectl create secret tls custom-tls-cert --key /Users/bikramdahal/Arch/kub_cluster/tls.key --cert /Users/bikramdahal/Arch/kub_cluster/tls.crt
```

12. Make secrets from token

```bash
kubectl create secret generic aws --from-literal=key=AWS_ACCESS_KEY_ID=xxx --from-literal=region=us-east-1 --from-literal=env=xxxx --from-literal=access=Xxxxx
```

13. Make repo secrets
```bash
kubectl create secret docker-registry regcred --namespace flask-app --docker-server=https://registry.gitlab.com --docker-username=XXXX --docker-password=XXXXXX --docker-email=XXXX
```
__add pull image from private repo__

```yaml
spec:
      containers:
      - name: flask
        image: registry.gitlab.com/experiment-devops/flask_app/flask_app:1.0.0
        resources:
          limits:
            cpu: 1000m
          requests:
            cpu: 100m
        env:
          - name: REDIS_HOST
            value: redis
        ports:
        - containerPort: 5000
      imagePullSecrets:
      - name: regcred
```


## Helm
1. Start the helm
```bash
helm init

echo "sleep for 10 sec to start tiller"
sleep 10
kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'

```