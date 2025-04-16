#!/bin/bash

export IMAGE_NAME=yakiradela/rickmorty-api:latest

echo "Pulling image..."
docker pull $IMAGE_NAME

echo "Applying Kubernetes manifests..."
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

echo "Deployment done."
