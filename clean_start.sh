kubectl delete namespaces flask-app || echo "flask-app namespaces is not present"

echo "create flask app"
kubectl create -f flask_namespace.yaml
kubectl create -f flask_deployment.yaml
kubectl create -f flask_ingress.yaml
kubectl create -f redis_deployment.yaml

echo "show the token"