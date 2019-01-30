## Step for deploying in Kub cluster
1. Copy config to your kube config **only if your using digital ocean managed cluster**
```bash
cp config.yaml ~/.kube/config 
```

2. Always make news new namespace

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
          - name: ELASTICSEARCH_URL
            value: http://elasticsearch:9200
        ports:
        - containerPort: 5000

```

4. check deplopment 
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
  name: flask-ingress
  namespace: flask-app
  annotations:
    ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
        - path: /api
          backend:
            serviceName: flask
            servicePort: 5000
```

8. Make change using yaml edit
```bash
kubectl apply -f flask_deployment.yaml   
```

9. [Kubernetes cheat sheets](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

10. Delete the namespace ( deletes all resources on that namespace)

```bash
kubectl delete namespaces flask-app   
```