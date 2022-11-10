基本用法

```
解压安装包并导入镜像
```

```
创建一个chart
[root@k8s-master-node1 ~]# helm create mychart
Creating mychart
```

chart基本元素释义如下：

```sh
[root@k8s-master-node1 ~]# tree mychart/
mychart/
├── charts                #可选:本chart依赖的其他chart；
├── Chart.yaml             #必选:描述chart相关信息，包括名称、描述等信息；
├── templates              #必选:作用于kubernetes资源的yaml模版；
│   ├── deployment.yaml   # deployment的yaml模版，发布应用的基本元素；
│   ├── _helpers.tpl        #用于定义一些可重用的模板片断；
│   ├── hpa.yaml          #用于生成hpa的yaml模版；
│   ├── ingress.yaml       #用于生成ingress的yaml模版；
│   ├── NOTES.txt        #必选:用于介绍chart部署后的一些信息；
│   ├── serviceaccount.yaml  #用于生成serviceaccount资源的yaml模版
│   ├── service.yaml        #用于生成service资源的yaml模版；
│   └── tests               #helm的测试钩子
│       └── test-connection.yaml
└── values.yaml           #必选:用于存储要渲染至templates/下模版文件中的值
```

自定义YAML文件

```
删除templates目录下面所有文件：
[root@k8s-master-node1 ~]# rm -rfv mychart/templates/*

自定义Deployment模板文件

是一个可安装的chart包了，通过helm install命令来进行安装
部署与直接使用“kubectl apply”部署差别不大

使用如下命令可以看到实际的模板被渲染过后的资源文件：
[root@k8s-master-node1 ~]# helm get manifest web

删除当前release：
[root@k8s-master-node1 ~]# helm delete web
release "web" uninstalled
```

****

helm部署nginx应用

```yaml
#使用helm工具创建nginx项目
helm create nginx
rm -rf  nginx/templates/*

#创建deployment模板
kubectl create deployment nginx -oyaml --image=nginx:latest --replicas=1  --dry-run --port=80 > /root/nginx/templates/deployment.yaml

cat > /root/nginx/templates/deployment <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx
  name: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 80
EOF

#创建helm应用的文档简介
cat > /root/nginx/templates/NOTES.txt <<EOF
name: nginx
EOF

#部署以Release为web命名的helm任务
cd /root
helm install web nginx
helm uninstall web 
```

编辑Deployment模板：

```
[root@k8s-master-node1 ~]# cat mychart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
creationTimestamp: null
labels:
  chart: {{ .Chart.Name }}
  app: {{ .Release.Name }}
name: {{ .Release.Name }}
spec:
replicas: {{ .Values.replicas}}
selector:
  matchLabels:
    app: {{ .Values.label }}
strategy: {}
template:
  metadata:
    creationTimestamp: null
    labels:
      app: {{ .Values.label }}
  spec:
    containers:
     - image: {{ .Values.image }}:{{ .Values.imageTag }}
      name: {{ .Release.Name }}
      resources: {}
status: {}


{{ .Release.Name }}为helm安装时的名称
```

```
调试
helm install web01 --dry-run mychart

安装
helm instrall web01 mychart
```

内置对象

```
刚刚使用{{.Release.Name}}将release的名称插入到模板中。这里的Release就是Helm的内置对象，下面是一些常用的内置对象：

● Release.Name：release名称；

● Release.Time：release的时间；

● Release.Namespace：release的namespace（如果清单未覆盖）；

● Release.Service：release服务的名称（始终是Tiller）；

● Release.Revision：此release的修订版本号，从1开始累加；

● Release.IsUpgrade：如果当前操作是升级或回滚，则将其设置为true；

● Release.IsInstall：如果当前操作是安装，则设置为true。

上面这些值可用于任何顶级模板，要注意内置对象始终以大写字母开头。这也符合Go的命名约定。
```

更新

```
[root@k8s-master-node1 ~]# helm upgrade web01 mychart
```

Values

```
Values对象是为Chart模板提供值，这个对象的值有4个来源：

● chart包中的values.yaml文件

● 父chart包的values.yaml文件

● 通过helm install或helm upgrade的-f或者--values参数传入的自定义的yaml文件

● 通过--set参数传入的值

chart的values.yaml提供的值可以被用户提供的values文件覆盖，而该文件同样可以被--set提供的参数所覆盖。

例如新建一个应用，副本数只有1个：
[root@k8s-master-node1 ~]# helm install web02 --set replicas=1 mychart
```

Chart的管道与函数

```
模板函数
app: {{ quote .Values.label }}
app: "nginx"

管道（使用管道重写上面的Deployment模板）
app: {{ .Values.label | quote }}
app: "nginx"

default函数（允许在模板内部指定默认值，以防止该值被忽略掉了）
test: {{ default "demotest" .Values.test }}
test: demotest
因为没有在values.yaml中定义test的值，所以默认其值为demotest。如果在values.yaml中定义了，其值就以values.yaml中的值为准。
```

控制流程

```
控制流程为提供了控制模板生成流程的一种能力，Helm的模板语言提供了以下几种流程控制：

● if/else条件块

● with指定范围

● range循环块

除此之外，它还提供了一些声明和使用命名模板段的操作：

● define在模板中声明一个新的命名模板

● template导入一个命名模板

● block声明了一种特殊的可填写的模板区域
```

if/else

```
{{ if PIPELINE }}
 # Do something
{{ else if OTHER PIPELINE }}
 # Do something else
{{ else }}
 # Default case
{{ end }}


实例
app: {{ quote .Values.label }}
{{- if eq .Values.test "devops"}}
devops: k8s
{{- else }}
devops: docker
{{- end }}

[root@k8s-master-node1 ~]# cat mychart/values.yaml
replicas: 3
image: nginx
imageTag: 1.18
label: nginx
test: devops

[root@k8s-master-node1 ~]# helm install web03 --dry-run mychart/
……
template:
  metadata:
    creationTimestamp: null
    labels:
      app: "nginx"
      devops: k8s

其中运算符eq是判断是否相等的操作，除此之外，还有 ne、 lt、 gt、 and、 or等运算符。
其中渲染出来会有多余的空行，这是因为当模板引擎运行时，会将控制指令删除，所有之前占的位置也就空白了，所以需要使用{undefined{- if …}} 的方式消除此空行
```

with

```
控制变量的作用域范围
{{ with PIPELINE }}
# restricted scope
{{ end }}

[root@k8s-master-node1 ~]# cat mychart/values.yaml
replicas: 3
image: nginx
imageTag: 1.18
label: nginx
test: devops
nodeSelector:
team: chongqing
gpu: ok

在Deployment模板中containers字段前面加入if判断内容
[root@k8s-master-node1 ~]# cat mychart/templates/deployment.yaml
……
  spec:
    {{- if .Values.nodeSelector }}
    nodeSelector:
      team: {{ .Values.nodeSelector.team }}
      gpu: {{ .Values.nodeSelector.gpu }}
    {{- end }}
    containers:
……
运行结果
helm install web --dry-run mychart/
……
  spec:
    nodeSelector:
      team: chongqing
      gpu: ok
    containers:
……
改为使用with：
[root@k8s-master-node1 ~]# cat mychart/templates/deployment.yaml
……
  spec:
    {{- with .Values.nodeSelector }}
    nodeSelector:
      team: {{ .team }}
      gpu: {{ .gpu }}
    {{- end }}
    containers:
……
调试查看运行结果：
[root@k8s-master-node1 ~]# helm install web --dry-run mychart/
……
  spec:
    nodeSelector:
      team: chongqing
      gpu: ok
    containers:
……

简化   使用toYaml函数
[root@k8s-master-node1 ~]# cat mychart/templates/deployment.yaml
……
  spec:
    {{- with .Values.nodeSelector }}
    nodeSelector:
      {{- toYaml . | nindent 8 }}
    {{- end }}
    containers:
……
 toYaml之后的点是循环中.Values.nodeSelector的当前值。使用nindent 8是因为用toYaml函数得到的值都是顶格，需要缩进8个字符，保持语法正确，并且每缩进一行都需要换行
```

range

```
在Helm模板语言中，range用于进行循环操作
在values.yaml文件中添加上一个变量列表：
[root@k8s-master-node1 ~]# cat mychart/values.yaml
replicas: 3
image: nginx
imageTag: 1.18
label: nginx
test: devops
nodeSelector:
team: chongqing
gpu: ok
ceshi:
 - 1
 - 2
 - 3

在templates目录下面新建一个configmap.yaml文件：
[root@k8s-master-node1 ~]# cat mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
name: {{ .Release.Name }}
data:
test: |
{{- range .Values.ceshi }}
  {{ . }}
{{- end }}

调试运行查看结果：
[root@k8s-master-node1 ~]# helm install web --dry-run mychart/
……
data:
test: |
   1
   2
   3
……

```

打包chart

```
helm package mychart/
```

ELK

```
EFK是三个开源软件的缩写，分别表示：Elasticsearch、FileBeat和Kabana。其中ELasticsearch负责日志保存和搜索，FileBeat负责收集日志，Kibana负责界面。EFK和ELK的区别在于EFK把ELK的Logstash替换成了FileBeat，因为Filebeat相对于Logstash来说侵入低，无需修改程序目前任何代码和配置，且性能更高。
```

