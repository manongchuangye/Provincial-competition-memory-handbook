istio边车代理

```
自动注入sidecar在exam命名空间下
kubectl create namespace exam
kubectl label namespace exam istio-injection=enabled

```

helm

```
部署helm，定义一个chart	，名称为web，deployment为nginx，副本为1，默认命名空间
docker load -i Helm/images.tar
helm create mychart
rm -rfv mychart/templates/*       #为什么要删了
[root@k8s-master-node1 ~]# cat mychart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
name: {{ .Release.Name }}
spec:
replicas: {{ .Values.replicas}}
selector:
    matchLabels:
      app: {{ .Values.label }}
strategy: {}
template:
      metadata:
      labels:
        app: {{ .Values.label }}
  spec:
    containers:
     - image: {{ .Values.image }}:{{ .Values.imageTag }}
      name: {{ .Release.Name }}

cat mychart/values.yaml
replicas: 3
image: nginx
imageTag: 1.17
label: nginx


helm install web mychart/
```

