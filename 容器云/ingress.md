基本步骤

```
1. 安装部署ingress controller Pod
2. 部署Ingress-controller的service，以实现接入集群外部流量
3. 测试代理 后端服务
	1. 部署后端服务，并通过service进行暴露
		1. 我这里的案例是 myapp 
	2. 部署ingress，进行定义规则，使Ingress-controller和后端服务的Pod组进行关联
```

安装ingress-controller

```
ingress.tar.gz

kubectl get pod -n ingress-nginx 
```

详情见（ingress nginx构建和使用）

