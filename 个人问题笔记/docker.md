```bash
$ docker --help

管理命令:
  container   管理容器
  image       管理镜像
  network     管理网络
命令：
  attach      介入到一个正在运行的容器
  build       根据 Dockerfile 构建一个镜像
  commit      根据容器的更改创建一个新的镜像
  cp          在本地文件系统与容器中复制 文件/文件夹
  create      创建一个新容器
  exec        在容器中执行一条命令
  images      列出镜像
  kill        杀死一个或多个正在运行的容器    
  logs        取得容器的日志
  pause       暂停一个或多个容器的所有进程
  ps          列出所有容器
  pull        拉取一个镜像或仓库到 registry
  push        推送一个镜像或仓库到 registry
  rename      重命名一个容器
  restart     重新启动一个或多个容器
  rm          删除一个或多个容器
  rmi         删除一个或多个镜像
  run         在一个新的容器中执行一条命令
  search      在 Docker Hub 中搜索镜像
  start       启动一个或多个已经停止运行的容器
  stats       显示一个容器的实时资源占用
  stop        停止一个或多个正在运行的容器
  tag         为镜像创建一个新的标签
  top         显示一个容器内的所有进程
  unpause     恢复一个或多个容器内所有被暂停的进程
```

```
service docker start       # 启动 docker 服务，守护进程
service docker stop        # 停止 docker 服务
service docker status      # 查看 docker 服务状态
chkconfig docker on        # 设置为开机启动
```

```
docker pull centos:latest  # 从docker.io中下载centos镜像到本地
docker images              # 查看已下载的镜像
docker rmi [image_id]      # 删除镜像，指定镜像id

# 删除所有镜像
# none 默认为 docker.io
docker rmi $(docker images | grep none | awk '{print $3}' | sort -r)

# 连接进行进入命令行模式，exit命令退出。
docker run -t -i nginx:latest /bin/bash
```

### 通过容器创建镜像

我们可以通过以下两种方式对镜像进行更改。

1. 从已经创建的容器中更新镜像，并且提交这个镜像
2. 使用 Dockerfile 指令来创建一个新的镜像

下面通过已存在的容器创建一个新的镜像。

```
docker commit -m="First Docker" -a="wcjiang" a6b0a6cfdacf wcjiang/nginx:v1.2.1
```

上面命令参数说明：

- `-m` 提交的描述信息
- `-a` 指定镜像作者
- `a6b0a6cfdacf` 记住这个是容器id，不是镜像id
- `wcjiang/nginx:v1.2.1` 创建的目标镜像名

### 通过Dockerfile创建镜像

假设创建一个 node.js 镜像，首先在 node.js 项目根目录创建文件。

```
touch Dockerfile .dockerignore
```

`.dockerignore` 文件内容，下面代码表示，这三个路径要排除，不要打包进入 image 文件。如果你没有路径要排除，这个文件可以不新建。

```
.git
node_modules
npm-debug.log
```

Dockerfile 文件内容

```
FROM node:8.4
COPY . /app
WORKDIR /app
RUN npm install --registry=https://registry.npm.taobao.org
EXPOSE 3000
```

- `FROM node:8.4`：该 `image` 文件继承官方的 `node image`，冒号表示标签，这里标签是`8.4`，即`8.4`版本的 `node`。
- `COPY . /app`：将当前目录下的所有文件（除了 `.dockerignore` 排除的路径），都拷贝进入 `image` 文件的 `/app` 目录。
- `WORKDIR /app`：指定接下来的工作路径为`/app`。
- `RUN npm install`：在/app目录下，运行 `npm install` 命令安装依赖。注意，安装后所有的依赖，都将打包进入 `image` 文件。
- `EXPOSE 3000`：将容器 `3000` 端口暴露出来， 允许外部连接这个端口。

有了 `Dockerfile` 文件以后，就可以使用 `docker image build` 命令创建 `image` 文件了。

```
$ docker image build -t koa-demo .
# 或者
$ docker image build -t koa-demo:0.0.1 .
```

上面命令，`-t` 参数用来指定 `image` 文件的名字，后面还可以用冒号指定标签。如果不指定，默认的标签就是 `latest`。注意后面有个 `.`，表示 Dockerfile 文件所在的路径为当前路径

```
docker run --name koa-demo-name --rm -d -p 9066:3000 koa-demo:latest
# 或者
docker run --name koa-demo-name --rm -d -p 9066:3000 koa-demo:0.0.1
```

上面命令，将刚创建的 koa-demo 景象跑起来。

### 发布自己的镜像

1. 在[Docker](https://www.docker.com/) 注册账户，发布的镜像都在[这个页面里](https://cloud.docker.com/repository/list)展示
2. 将上面做的镜像`nginx`，起个新的名字`nginx-test`

```
docker tag wcjiang/nginx:v1.2.1 wcjiang/nginx-test:lastest
```

1. 登录docker

```
docker login
```

1. 上传`nginx-test`镜像

```
docker push wcjiang/nginx-test:lastest
# The push refers to a repository [docker.io/wcjiang/nginx-test]
# 2f5c6a3c22e3: Mounted from wcjiang/nginx
# cf516324493c: Mounted from wcjiang/nginx
# lastest: digest: sha256:73ae804b2c60327d1269aa387cf782f664bc91da3180d10dbd49027d7adaa789 size: 736
```

### 镜像中安装软件

通常情况下，使用docker官方镜像，如 mysql镜像，默认情况下镜像中啥软件也没有，通过下面命令安装你所需要的软件：

```
# 第一次需要运行这个命令，确保源的索引是最新的
# 同步 /etc/apt/sources.list 和 /etc/apt/sources.list.d 中列出的源的索引
apt-get update
# 做过上面更新同步之后，可以运行下面的命令了
apt-get install vim
```

如果你安装了CentOS或者Ubuntu系统可以进入系统安装相关软件

```
# 进入到centos7镜像系统
docker run -i -t centos:7 /bin/bash
yum update
yum install vim
```

## 容器管理

容器就像一个类的实例

```
# 列出本机正在运行的容器
docker container ls
# 列出本机所有容器，包括终止运行的容器
docker container ls --all
docker start [containerID/Names] # 启动容器
docker stop [containerID/Names]  # 停止容器
docker rm [containerID/Names]    # 删除容器
docker logs [containerID/Names]  # 查看日志
docker exec -it [containerID/Names] /bin/bash  # 进入容器

# 从正在运行的 Docker 容器里面，将文件拷贝到本机，注意后面有个【点】拷贝到当前目录
docker container cp [containID]:[/path/to/file] .

docker run centos echo "hello world"  # 在docker容器中运行hello world!
docker run centos yum install -y wget # 在docker容器中，安装wget软件
docker ps                             # 列出包括未运行的容器
docker ps -a                          # 查看所有容器(包括正在运行和已停止的)
docker logs my-nginx                  # 查看 my-nginx 容器日志

docker run -i -t centos /bin/bash     # 启动一个容器
docker inspect centos                 # 检查运行中的镜像
docker commit 8bd centos              # 保存对容器的修改
docker commit -m "n changed" my-nginx my-nginx-image # 使用已经存在的容器创建一个镜像
docker inspect -f {{.State.Pid}} 44fc0f0582d9        # 获取id为 44fc0f0582d9 的PID进程编号
# 下载指定版本容器镜像
docker pull gitlab/gitlab-ce:11.2.3-ce.0
```

### 容器服务管理

```
docker run -itd --name my-nginx2 nginx  # 通过nginx镜像，【创建】容器名为 my-nginx2 的容器
docker start my-nginx --restart=always  # 【启动策略】一个已经存在的容器启动添加策略
    # no - 容器不重启
    # on-failure - 容器推出状态非0时重启
    # always - 始终重启
docker start my-nginx             # 【启动】一个已经存在的容器
docker restart my-nginx           # 【重启】容器
docker stop my-nginx              # 【停止运行】一个容器
docker kill my-nginx              # 【杀死】一个运行中的容器
docker rename my-nginx new-nginx  # 【重命名】容器
docker rm new-nginx               # 【删除】容器
```

### 进入容器

1. 创建一个守护状态的 Docker 容器

```
docker run -itd my-nginx /bin/bash
```

1. 使用`docker ps`查看到该容器信息

```
docker ps
# CONTAINER ID  IMAGE  COMMAND      CREATED          STATUS          PORTS    NAMES
# 6bd0496da64f  nginx  "/bin/bash"  20 seconds ago   Up 18 seconds   80/tcp   high_shirley
```

1. 使用`docker exec`命令进入一个已经在运行的容器

```
docker exec -it 6bd0496da64f /bin/bash
```

通常有下面几种方式进入Docker的容器，推荐使用 `exec`，使用 `attach` 一直进入失败。

- 使用`docker attach`
- 使用`SSH` [为什么不需要在 Docker 容器中运行 sshd](http://www.oschina.net/translate/why-you-dont-need-to-run-sshd-in-docker?cmp)
- 使用`nsenter`进入Docker容器，[nsenter官方仓库](https://github.com/jpetazzo/nsenter)
- 使用`docker exec`，在`1.3.*`之后提供了一个新的命令`exec`用于进入容器

## 文件拷贝

从主机复制到容器 `sudo docker cp host_path containerID:container_path`
从容器复制到主机 `sudo docker cp containerID:container_path host_path`

## Docker私有仓库搭建

通过官方提供的私有仓库镜像`registry`来搭建私有仓库。通过 [humpback](https://humpback.github.io/) 快速搭建轻量级的Docker容器云管理平台。关于仓库配置说明请参见[configuration.md](https://github.com/docker/distribution/blob/master/docs/configuration.md)

> ⚠️ 注意：也可以通过部署管理工具 `Harbor` 来部署 `registry`

除了 [Harbor](https://github.com/goharbor/harbor) 还有 [humpback](https://github.com/humpback/humpback) 和 [rancher](https://github.com/rancher/rancher)

### `registry`

```
docker pull registry:2.6.2
```

创建容器并运行，创建成功之后，可访问 `http://192.168.99.100:7000/v2/`，来检查仓库是否正常运行，当返回 `{}` 时，表示部署成功。

```
docker run -d \
  -p 5000:5000 \
  --restart=always \
  --name registry \
  registry:2

# 自定义存储位置
docker run -d \
  -p 5000:5000 \
  --restart=always \
  --name registry \
  -v $HOME/_docker/registry:/var/lib/registry \
  registry:2

docker run -d -p 5000:5000 --restart=always --name registry \
    -v `pwd`/config.yml:/etc/docker/registry/config.yml \
    registry:2
```

推送镜像到私有仓库

```
# 从官方仓库拉取一个镜像
docker pull nginx:1.13
# 为镜像 `nginx:1.13` 创建一个新标签 `192.168.31.69:7000/test-nginx:1.13`
docker tag nginx:latest 192.168.31.69:7000/test-nginx:1.13
# 推送到私有仓库中
docker push 192.168.31.69:5000/test-nginx:1.13
# The push refers to a repository [192.168.99.100:7000/test-nginx]
# Get https://192.168.99.100:7000/v1/_ping: http: server gave HTTP response to HTTPS client
```

在推送到的时候报错误，默认是使用 `https` 提交，这个搭建的默认使用的是 `http`，解决方法两个：

1. 创建一个 `https` 映射
2. 将仓库地址加入到不安全的仓库列表中

我们使用第二种方法，加入到不安全的仓库列表中，修改docker配置文件 `vi /etc/docker/daemon.json` 添加 `insecure-registries` 配置信息，如果 [daemon.json](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file) 文件不存在可以创建，关键配置项，将仓库将入到不安全的仓库列表中。

```
{
  "insecure-registries":[
    "192.168.31.69:5000"
  ]
}
```

重启服务 `service docker restart`，默认情况下 push 是会报如下错误的：

```
docker push 192.168.99.100:7000/test-nginx:1.13
# The push refers to a repository [192.168.99.100:7000/test-nginx]
# a1a53f8d99b5: Retrying in 1 second
# ...
# received unexpected HTTP status: 500 Internal Server Error
```

上面错误是 `SELinux` 强制访问控制安全系统，阻止导致的错误，通过下面方法禁用 SELinux 之后就可以 push 了。

```
setenforce 0  
getenforce   
# Permissive  
```

```
# 停止本地 registry
docker container stop registry
# 要删除容器，请使用 docker container rm
docker container stop registry && docker container rm -v registry
# 自定义存储位置
```

### `Harbor`

[部署 registry 管理工具 Harbor](https://github.com/jaywcjlove/docker-tutorial/blob/master/docs/harbor.md)

## Docker REST API

`Docker` 不仅可以通过本地命令行 `docker` 命令进行调用，还可以通过开启远程控制 `API`，使用 `HTTP` 调用接口来进行访问，远程控制 `Docker Daemon` 来做很多操作。`Docker` 的远程 `API` 服务默认监听的是 TCP `2375` 端口，为了保证安全，Docker 安装后默认不会启用远程 `API` 服务，因为这个服务默认不做权限认证。

### CentOS

CentOS 的开启方法比较简单，先修改配置：

```
vim /usr/lib/systemd/system/docker.service

# 修改 `ExecStart` 配置项，默认如下：
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock

# 增加一个 `-H tcp://0.0.0.0:2375` 选项
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2375 --containerd=/run/containerd/containerd.sock
```

如果是内网生产环境，也可以将 `0.0.0.0` 改为内网 IP。同样的，`2375` 端口也可以修改。但是这样可能还有一个问题，无法在命令行使用 `docker` 命令了，还需要添加 `sock` 选项：`-H unix:///var/run/docker.sock`，最后为：

```bash
ExecStart=/usr/bin/dockerd -H fd:// -H unix:///var/run/docker.sock -H tcp://10.105.3.115:2375 --containerd=/run/containerd/containerd.sock
```

修改完配置之后需要重启 Docker 服务：

```
systemctl daemon-reload
systemctl restart docker
sudo service docker restart
```

重启完成后，可以使用 netstat 查看端口是否监听来确认是否成功：

```
[root@VM-3-115-centos ~]# netstat -nutlp | grep 2375
tcp   0   0 10.105.3.115:2375   0.0.0.0:*     LISTEN    32316/dockerd
```

### MacOS

在 Mac 下无法直接修改配置文件来开启远程 API 服务，后来在 [`docker/for-mac`](https://github.com/docker/for-mac) 的 [`issue`](https://github.com/docker/for-mac/issues/770) 中得到了解决方案。

可以运行一个 [`bobrik/socat`](https://hub.docker.com/r/bobrik/socat) 容器，将 `unix socket` 上的 Docker API 转发到 MacOS 上指定的端口中：

```
docker run -d -v /var/run/docker.sock:/var/run/docker.sock -p 127.0.0.1:2375:2375 bobrik/socat TCP-LISTEN:2375,fork UNIX-CONNECT:/var/run/docker.sock
```

### 测试

启用成功后，可以进行一些测试，例如直接使用浏览器访问 info 和 version 等页面获取信息。

```
http://127.0.0.1:2375/info
http://127.0.0.1:2375/version
```

下面可测试 docker 是否启动了

```
curl -s --unix-socket /var/run/docker.sock http://dummy/containers/json
## 或者使用下面命令
docker info
```

## 使用Docker实战

> ⚠文件挂载注意：docker 禁止用主机上不存在的文件挂载到 container 中已经存在的文件

```
-d, --detach=false      # 指定容器运行于前台还是后台，默认为false   
-i, --interactive=false # 打开STDIN，用于控制台交互  
-t, --tty=false         # 分配tty设备，该可以支持终端登录，默认为false  
-u, --user=""           # 指定容器的用户  
-a, --attach=[]         # 登录容器（必须是以docker run -d启动的容器）
-w, --workdir=""        # 指定容器的工作目录 
-c, --cpu-shares=0      # 设置容器CPU权重，在CPU共享场景使用  
-e, --env=[]            # 指定环境变量，容器中可以使用该环境变量  
-m, --memory=""         # 指定容器的内存上限  
-P, --publish-all=false # 指定容器暴露的端口  
-p, --publish=[]        # 指定容器暴露的端口 
-h, --hostname=""       # 指定容器的主机名  
-v, --volume=[]         # 给容器挂载存储卷，挂载到容器的某个目录  
--volumes-from=[]       # 给容器挂载其他容器上的卷，挂载到容器的某个目录
--cap-add=[]            # 添加权限，权限清单详见：http://linux.die.net/man/7/capabilities  
--cap-drop=[]           # 删除权限，权限清单详见：http://linux.die.net/man/7/capabilities  
--cidfile=""            # 运行容器后，在指定文件中写入容器PID值，一种典型的监控系统用法  
--cpuset=""             # 设置容器可以使用哪些CPU，此参数可以用来容器独占CPU  
--device=[]             # 添加主机设备给容器，相当于设备直通  
--dns=[]                # 指定容器的dns服务器  
--dns-search=[]         # 指定容器的dns搜索域名，写入到容器的/etc/resolv.conf文件  
--entrypoint=""         # 覆盖image的入口点  
--env-file=[]           # 指定环境变量文件，文件格式为每行一个环境变量  
--expose=[]             # 指定容器暴露的端口，即修改镜像的暴露端口  
--link=[]               # 指定容器间的关联，使用其他容器的IP、env等信息  
--lxc-conf=[]           # 指定容器的配置文件，只有在指定--exec-driver=lxc时使用  
--name=""               # 指定容器名字，后续可以通过名字进行容器管理，links特性需要使用名字  
--net="bridge"          # 容器网络设置:
                            # bridge 使用docker daemon指定的网桥     
                            # host 	//容器使用主机的网络  
                            # container:NAME_or_ID  >//使用其他容器的网路，共享IP和PORT等网络资源  
                            # none 容器使用自己的网络（类似--net=bridge），但是不进行配置 
--privileged=false      # 指定容器是否为特权容器，特权容器拥有所有的capabilities  
--restart="no"          # 指定容器停止后的重启策略:
                            # no：容器退出时不重启  
                            # on-failure：容器故障退出（返回值非零）时重启 
                            # always：容器退出时总是重启  
--rm=false              # 指定容器停止后自动删除容器(不支持以docker run -d启动的容器)  
--sig-proxy=true        # 设置由代理接受并处理信号，但是SIGCHLD、SIGSTOP和SIGKILL不能被代理
```

## 卸载旧的版本

移除旧的版本

```
$ sudo yum remove docker \
  docker-client \
  docker-client-latest \
  docker-common \
  docker-latest \
  docker-latest-logrotate \
  docker-logrotate \
  docker-selinux \
  docker-engine-selinux \
  docker-engine
```

**镜像拉不下来**

修改 Docker `daemon.json` 配置 macOS: `/etc/docker/daemon.json`，Linux: `~/.docker/daemon.json`

```
{
  "registry-mirrors":[
     "https://docker.mirrors.ustc.edu.cn",
     "https://hub-mirror.c.163.com",
     "https://mirror.baidubce.com",
     "https://registry.docker-cn.com"
  ],
  "insecure-registries": [
     "192.168.188.111:2021"
  ]
}
```

## Docker数据卷

挂载数据卷

Docker 提供了 3 种不同的方式将数据从宿主机挂载到容器中。![Docker 挂载数据卷](docker.assets/165795626005770.png)

### volume (最常用的方式)

volume : Docker 管理宿主机文件系统的一部分，默认位于 `/var/lib/docker/volumes` 目录下, 也是最常用的方式。![Docker 查看本地数据卷](docker.assets/165795655125558.jpeg)

看上图，所有的 Docker 容器数据都保存在 `/var/lib/docker/volumes` 目录下。若容器运行时未指定数据卷， Docker 创建容器时会使用默认的匿名卷（名称为一堆很长的 ID）。

#### 创建一个数据卷

执行如下命令创建数据卷：

```
docker volume create test-vol
```

#### 查看所有的数据卷

```
docker volume ls
```

#### 查看数据卷信息

执行如下命令，可以查看指定的数据卷信息

```
# 查看数据卷名为 test-vol 的信息
docker volume inspect test-vol
```

#### 运行容器时挂载数据卷

数据卷 `test-vol`创建成功后，我们运行一个 Nginx 容器，并尝试挂载该数据卷，挂载命令支持两种：

1. `-v`

```BASH
docker run -d -it --name=test-nginx -p 8011:80 -v test-vol:/usr/share/nginx/html nginx:1.1
```

参数说明：

- `-d` : 后台运行容器；
- `--name=test-nginx` : 指定容器名为 test-nginx;
- `-p 8011:80` : 将容器的 80 端口挂载到宿主机的 8011 端口；
- `-v test-vol:/usr/share/nginx/html` : 将 `test-vol` 数据卷挂载到容器中的 /usr/share/nginx/html 目录上；

1. `--mount`

```
docker run -d -it --name=test-nginx -p 8011:80 --mount source=test-vol,target=/usr/share/nginx/html nginx:1.13.12
```

参数说明：

- `--mount source=test-vol,target=/usr/share/nginx/html` : 将 `test-vol` 数据卷挂载到容器中的 /usr/share/nginx/html 目录上；

#### `-v` 和 `--mount` 有什么区别？

都是挂载命令，使用 `-v` 挂载时，如果宿主机上没有指定文件不会报错，会自动创建指定文件；当使用 `--mount`时，如果宿主机中没有这个文件会报错找不到指定文件，不会自动创建指定文件。

容器运行成功后，进入到 `/var/lib/docker/volumes` 目录下，验证数据是否挂载成功：

![验证数据卷是否挂载成功](docker.assets/165796047624428.jpeg)

可以看到已经有了 `50x.html` 、 `index.html` 两个 Nginx 页面相关数据，说明数据卷挂载成功了。挂载成功后，我们不论是修改 `/var/lib/docker/volumes` 下的数据，还是进入到容器中修改 `/usr/share/nginx/html` 下的数据，都会同步修改对应的挂载目录，类似前端开发中双向绑定的作用。

下面，我们停止并删除刚刚运行的 Nginx 容器, 看看数据卷中的数据是否会跟着被删除：

下面，我们停止并删除刚刚运行的 Nginx 容器, 看看数据卷中的数据是否会跟着被删除：

![删除容器，验证数据卷是否还存在](docker.assets/165796382593092.jpeg)删除容器，验证数据卷是否还存在

可以发现数据卷相关数据都还在，表明数据卷的生命周期独立于容器。另外，若下次再创建 Nginx 容器，还可以复用这个数据卷，复用性以及扩张性都非常不错。

### 删除数据卷

由于数据卷的生命期独立于容器，想要删除数据卷，就需要我们手动来操作, 执行命令如下：

```
docker volume rm test-vol
```

1. 如果你需要在删除容器的同时移除数据卷，请使用 `docker rm -v` 命令。
2. 对于那些没有被使用的数据卷，可能会占用较多的磁盘空间，你可以通过如下命令统一删除：

```
docker volume prune
```

### bind mount（**比较常用的方式**）

bind mount: 意为可以存储在宿主机中的任意位置。需要注意的是，bind mount 在不同的宿主机系统时不可移植的，比如 Windows 和 Linux 的目录结构是不一样的，bind mount 所指向的 host 目录也不一样。这也是为什么 bind mount 不能出现在 Dockerfile 中的原因所在，因为这样 Dockerfile 就不可移植了。

#### bind mount 使用

```
docker run -d -it --name=test-nginx -p 8011:80 -v /docker/nginx1:/usr/share/nginx/html nginx:1.13.12
```

参数说明：

- `-v /docker/nginx1:/usr/share/nginx/html` : 将宿主机中的 `/docker/nginx1` 目录挂载到容器中的 `/usr/share/nginx/html` 目录；

容器运行成功后，进入容器中：

```
docker exec -it test-nginx /bin/bash
```

![docker 进入容器](docker.assets/165796623336460.jpeg)

从上图可以看到，与 volume 不同，bind mount 这种方式会隐藏目录中的内容（非空情况下），这里的 `/usr/share/nginx/html` 目录下的 html 文件被隐藏了，所以我们看不到。

但是，我们可以将宿主机中该目录中的文件立刻挂载到容器中，下面验证一下：

1. 新建一个 `index.html`:

   ![创建 index.html 文件](docker.assets/165796671029332.jpeg)

2. 再次进入容器，查看挂载目录内容：

   ![进入 docker 容器](docker.assets/165796684481635.jpeg)

### tmpfs mount (一般不用这种方式)

tmpfs mount : 挂载存储在宿主机的内存中，而不会写入宿主机的文件系统，一般不用此种方式。

## Docker 数据卷容器

如果你有一些需要持续更新的数据需要在容器之间共享，最佳实践是创建数据卷容器。**数据卷容器，其实就是一个正常的 Docker 容器，专门用于提供数据卷供其他容器挂载的**。

### 创建数据卷容器

运行一个容器，并创建一个名为 `dbdata` 的数据卷：

```
docker run -d -v /dbdata --name dbdata training/postgres echo Data-only container for postgres
```

容器运行成功后，会发现该数据卷容器处于停止运行状态，这是因为数据卷容器并不需要处于运行状态，只需用于提供数据卷挂载即可。

![Docker 创建数据卷容器](docker.assets/165804090120953.jpeg)

## 挂载数据卷

`--volumes-from` 命令支持从另一个容器挂载容器中已创建好的数据卷。

```
docker run -d --volumes-from dbdata --name db1 training/postgres
docker run -d --volumes-from dbdata --name db2 training/postgres
docker ps
CONTAINER ID       IMAGE                COMMAND                CREATED             STATUS              PORTS               NAMES
7348cb189292       training/postgres    "/docker-entrypoint.   11 seconds ago      Up 10 seconds       5432/tcp            db2
a262c79688e8       training/postgres    "/docker-entrypoint.   33 seconds ago      Up 32 seconds       5432/tcp            db1
```

还可以使用多个 `--volumes-from` 参数来从多个容器挂载多个数据卷。 也可以从其他已经挂载了数据卷的容器来挂载数据卷。

如果删除了挂载的容器（包括 dbdata、db1 和 db2），数据卷并不会被自动删除。如果想要删除一个数据卷，必须在删除最后一个还挂载着它的容器时使用 `docker rm -v` 命令来指定同时删除关联的容器。

## Docker 使用数据卷容器备份、恢复、迁移数据卷

### 备份

首先使用 `--volumes-from` 命令创建一个加载 dbdata 的容器卷容器，并将宿主机当前目录挂载到容器的 /backup 目录，命令如下：

```
sudo docker run --volumes-from dbdata -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata
```

容器启动后，使用了 `tar` 命令来将 dbdata 数据卷备份为容器中 /backup/backup.tar 文件，因为挂载了的关系，宿主机的当前目录下也会生成 `backup.tar` 备份文件。

### 恢复/迁移

如果要恢复数据到一个容器，首先创建一个带有空数据卷的容器 dbdata2

```
$ sudo docker run -v /dbdata --name dbdata2 ubuntu /bin/bash
```

然后创建另一个容器，挂载 dbdata2 容器卷中的数据卷，并使用 `untar` 解压备份文件到挂载的容器卷中。

```
$ sudo docker run --volumes-from dbdata2 -v $(pwd):/backup busybox tar xvf
/backup/backup.tar
```

为了查看/验证恢复的数据，可以再启动一个容器挂载同样的容器卷来查看：

```
$ sudo docker run --volumes-from dbdata2 busybox /bin/ls /dbdata
```

## Dockerfile制作镜像

编辑 `Dockerfile`，添加如下指令：

```
FROM nginx
RUN echo '<h1>Hello, Nginx by Docker!</h1>' > /usr/share/nginx/html/index.html
```

这个 `Dockerfile` 非常简单，总共也就运用了两条指令：`FROM` 和 `RUN`

## FROM 指定基础镜像

制作镜像必须要先声明一个基础镜像，基于基础镜像，才能在上层做定制化操作。

通过 **`FROM`指令可以指定基础镜像**，在 Dockerfile 中，`FROM` 是必备指令，且必须是第一条指令。比如，上面编写的 Dockerfile 文件第一行就是 `FROM nginx`, 表示后续操作都是基于 Ngnix 镜像之上。

### 特殊的镜像：scratch

通常情况下，基础镜像在 DockerHub 都能找到，如：

- **中间件相关**：`nginx`、`kafka`、`mongodb`、`redis`、`tomcat` 等；
- **开发语言环境** ：`openjdk`、`python`、`golang` 等；
- **操作系统**：`centos` 、`alpine` 、`ubuntu` 等；

除了这些常用的基础镜像外，还有个比较特殊的镜像 : `scratch` 。它表示一个空白的镜像：

```
FROM scratch
...
```

以 `scratch` 为基础镜像，表示你不以任何镜像为基础。

## RUN 执行命令

`RUN` 指令用于执行终端操作的 shell 命令，另外，`RUN` 指令也是编写 Dockerfile 最常用的指令之一。它支持的格式有如下两种：

- **1、`shell` 格式**: `RUN <命令>`，这种格式好比在命令行中输入的命令一样。举个栗子，上面编写的 Dockerfile 中的 `RUN` 指令就是使用的这种格式：

```
RUN echo '<h1>Hello, Nginx by Docker!</h1>' > /usr/share/nginx/html/index.html
```

- **2、`exec` 格式**: `RUN ["可执行文件", "参数1", "参数2"]`, 这种格式好比编程中调用函数一样，指定函数名，以及传入的参数。

```
RUN ["./test.php", "dev", "offline"] 等价于 RUN ./test.php dev offline
```

### 新手构建镜像的体积太大？太臃肿？

初学 Docker 的小伙伴往往构建出来的镜像体积非常臃肿，这是什么原因导致的？

我们知道，Dockerfile 中每一个指令都会新建一层，过多无意义的层导致很多运行时不需要的东西，都被打包进了镜像内，比如编译环境、更新的软件包等，这就导致了构建出来的镜像体积非常大。

举个例子：

```
FROM centos
RUN yum -y install wget
RUN wget -O redis.tar.gz "http://download.redis.io/releases/redis-5.0.3.tar.gz"
RUN tar -xvf redis.tar.gz
```

执行以上 Dockerfile 会创建 3 层，另外，下载的 `redis.tar.gz`也没有删除掉，可优化成下面这样：

```
FROM centos
RUN yum -y install wget \
    && wget -O redis.tar.gz "http://download.redis.io/releases/redis-5.0.3.tar.gz" \
    && tar -xvf redis.tar.gz \
    && rm redis.tar.gz
```

如上，仅仅使用了一个 `RUN` 指令，并使用 `&&` 将各个命令串联起来。之前的 3 层被简化为了 1 层，同时删除了无用的压缩包。

Dockerfile 支持 shell 格式命令末尾添加 `\` 换行，以及行首通过 `#` 进行注释。保持良好的编写习惯，如换行、注释、缩进等，可以让 Dockerfile 更易于维护。

## 构建镜像

Dockerfile 文件编写好了以后，就可以通过它构建镜像了。接下来，我们来构建前面定制的 nginx 镜像，首先，进入到该 Dockerfile 所在的目录下，执行如下命令：

```
docker build -t nginx:test .
```

注意：命令的最后有个点 `.` , 很多小伙伴不注意会漏掉，`.`指定**上下文路径**，也表示在当前目录下。

构建命令执行完成后，执行 `docker images` 命令查看本地镜像是否构建成功

镜像构建成功后，运行 Nginx 容器：

```
docker run -d -p 80:80 --name nginx nginx:test
```

容器运行成功后，访问 `localhost:80`, 可以看到首页已经被成功修改了

## 

前面的构建命令最后有一个 `.`, 它表示上下文路径，它又是个啥？

```
docker build -t nginx:test .
```

理解它之前，我们要知道 Docker 在运行时分为 Docker 引擎和客户端工具，是一种 C/S 架构。看似我们在命令收入了一行 Docker 命令，立即就执行了，背后其实是将命令提交给了客户端，然后客户端通过 API 与 Docker 引擎交互，真正干活的其实是 Docker 引擎。

话说回来，在构建镜像时，经常会需要通过 `COPY` 、`ADD` 指令将一些本地文件复制到镜像中。而刚才我们也说到了，执行 `docker build` 命令并非直接在本地构建，而是通过 Docker 引擎来完成的，那么要如何解决 Docker 引擎获取本地文件的问题呢？

于是引入了上下文的概念。构建镜像时，指定上下文路径，客户端会将路径下的所有内容打包，并上传给 Docker 引擎，这样它就可以获取构建镜像所需的一切文件了。

> 注意：上下文路径下不要放置一些无用的文件，否则会导致打包发送的体积过大，速度缓慢而导致构建失败。当然，我们也可以想编写 `.gitignore` 一样的语法写一个 `.dockerignore`, 通过它可以忽略上传一些不必要的文件给 Docker 引擎。

## `docker build` 的其他用法

### 通过 Git repo 构建镜像

除了通过 Dockerfile 来构建镜像外，还可以直接通过 URL 构建，比如从 Git repo 中构建：

```bash
# $env:DOCKER_BUILDKIT=0
# export DOCKER_BUILDKIT=0

$ docker build -t hello-world https://github.com/docker-library/hello-world.git#master:amd64/hello-world

Step 1/3 : FROM scratch
 --->
Step 2/3 : COPY hello /
 ---> ac779757d46e
Step 3/3 : CMD ["/hello"]
 ---> Running in d2a513a760ed
Removing intermediate container d2a513a760ed
 ---> 038ad4142d2b
Successfully built 038ad4142d2b
```

上面的命令指定了构建所需的 Git repo, 并且声明分支为 `master`, 构建目录为 `amd64/hello-world`。运行命令后，Docker 会自行 `git clone` 这个项目，切换分支，然后进入指定目录开始构建。

### 通过 tar 压缩包构建镜像

```
$ docker build http://server/context.tar.gz
```

如果给定的 URL 是个 `tar` 压缩包，那么 Docker 会自动下载这个压缩包，并自动解压，以其作为上下文开始构建。

### 从标准输入中读取 Dockerfile 进行构建

```
docker build - < Dockerfile
```

或

```
cat Dockerfile | docker build -
```

标准输入模式下，如果传入的是文本文件，Docker 会将其视为 `Dockerfile`，并开始构建。需要注意的是，这种模式是没有上下文的，它无法像其他方法那样将本地文件通过 `COPY` 指令打包进镜像。

### **从标准输入中读取上下文压缩包进行构建**

```
$ docker build - < context.tar.gz
```

标准输入模式下，如果传入的是压缩文件，如 `tar.gz` 、`gzip` 、 `bzip2` 等，Docker 会解压该压缩包，并进入到里面，将里面视为上下文，然后开始构建。

# Dockerfile 常用指令汇总

 更新时间 2022-08-31 22:00:39

想要熟练使用 [Dockerfile 制作构建镜像](https://www.quanxiaoha.com/docker/dockerfile-build-image.html) ，就需要熟悉 Dockerfile 常用的一些指令，除了前面小节中提到的 `COPY` 、`ADD` 指令外，Dockerfile 还额外提供了十多个指令。下面是 Dockerfile 常用指令汇总：

- [COPY 复制文件](https://www.quanxiaoha.com/docker/dockerfile-copy-file.html) ；
- [ADD 更高级的复制文件](https://www.quanxiaoha.com/docker/dockerfile-add-file.html) ；
- [CMD 容器启动命令](https://www.quanxiaoha.com/docker/dockerfile-cmd.html) ；
- [ENTRYPOINT 入口点](https://www.quanxiaoha.com/docker/dockerfile-entrypoint.html) ；
- [ENV 设置环境变量](https://www.quanxiaoha.com/docker/dockerfile-env.html) ；
- [ARG 构建参数](https://www.quanxiaoha.com/docker/dockerfile-arg.html) ；
- [VOLUMN 定义匿名数](https://www.quanxiaoha.com/docker/dockerfile-volumn.html) ；
- [EXPOSE 暴露端口](https://www.quanxiaoha.com/docker/dockerfile-expose.html) ；
- [WORKDIR 指定工作目录](https://www.quanxiaoha.com/docker/dockerfile-workdir.html) ；
- [USER 指定当前用户](https://www.quanxiaoha.com/docker/dockerfile-user.html) ；
- [HEALTHCHECK 健康检查](https://www.quanxiaoha.com/docker/dockerfile-healthcheck.html) ；
- [ONBUILD 二次构建](https://www.quanxiaoha.com/docker/dockerfile-onbuild.html) ；
- [LABEL 为镜像添加元数据](https://www.quanxiaoha.com/docker/dockerfile-label.html) ；
- [SHELL 指令](https://www.quanxiaoha.com/docker/dockerfile-shell.html) ；

# Docker Compose 安装

### 通过二进制包安装

从 [官方 GitHub Release](https://github.com/docker/compose/releases) 直接下载编译好的二进制文件即可，例如，在 Linux 64 位系统上直接下载对应的二进制包：

```
$ sudo curl -L https://github.com/docker/compose/releases/download/1.27.4/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose

# 国内用户可以使用以下方式加快下载
$ sudo curl -L https://download.fastgit.org/docker/compose/releases/download/1.27.4/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose

$ sudo chmod +x /usr/local/bin/docker-compose
```

### 通过 PIP 安装

> 注意：`x86_64` 架构的 Linux 建议按照上边的方法下载二进制包进行安装，如果您计算机的架构是 `ARM` (例如，树莓派)，再使用 `pip` 安装。

如果你的机器安装了 Python 环境，还可以将 Compose 当作一个 Python 应用来从 pip 源中安装，安装命令如下：

```
$ sudo pip install -U docker-compose
```

# Docker Compose 实战 web 服务

## 技术选型

- Web 应用：Spring Boot
- Redis 缓存（用于计数用户访问次数）

## 开始

### web 应用

新建一个 Spring Boot 项目， 主代码如下：

```java
package com.example.dockerdemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@SpringBootApplication
@Controller
public class DockerDemoApplication {

    private final RedisTemplate redisTemplate;

    public static void main(String[] args) {
        SpringApplication.run(DockerDemoApplication.class, args);
    }

    public DockerDemoApplication(RedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    @GetMapping("/")
    @ResponseBody
    public String index() {
    	// 对 redis 里面的被访问数执行 +1 操作
        Long viewNum = redisTemplate.opsForValue().increment("view_num");
        return String.format("<h1>页面总访问次数: %s</h1>", viewNum);
    }

}
```

Spring Boot 的 `application.yml` 配置文件如下：

```
spring:
  redis:
    host: redis
    port: 6379
```

### Dockerfile

为 Spring Boot 编写 Dockerfile :

```
# FROM 指定使用哪个镜像作为基准
FROM openjdk:8-jdk-alpine
# 数据卷
VOLUME /tmp
# 复制文件到镜像中
COPY docker-demo-0.0.1-SNAPSHOT.jar app.jar
# 指定容器内的时区
RUN echo "Asia/Shanghai" > /etc/timezone;
# ENV为设置环境变量
ENV JAVA_OPTS=""
# ENTRYPOINT 为启动时运行的命令
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -Djava.security.egd=file:/dev/./urandom -jar /app.jar"]
```

编译打包 Spring Boot, 然后将 Dockerfile 文件放置在 `jar` 包的同级目录下，执行如下命令开始构建 `web` 镜像：

```
docker build -t web:test .
```

执行成功后，通过 `docker images` 可以看到构建成功的本地镜像:

![构建 Spring Boot Docker 镜像](docker.assets/166467690411164.png)

### docker-compose.yml

编写 `docker-compose.yml` 文件：

```
version: '3'
services:
  web:
    image: "web:test"
    ports:
      - "8080:8080"

  redis:
    image: "redis:latest"
```

### 运行 compose 项目

在 `docker-compose.yml` 文件的同级目录下，执行运行命令：

```
docker-compose up
```

![运行 compose 项目](docker.assets/166467800825395.png)运行 compose 项目

`compose` 项目运行成功后，访问 web 服务，可以看到访问次数 `+1` 功能成功实现：

![web 服务被访问次数+1](docker.assets/166467848358134.gif)web 服务被访问次数+1

# Docker Compose 命令大全

```
docker-compose [-f=<arg>...] [options] [COMMAND] [ARGS...]
```

**提示**：执行 `docker-compose [COMMAND] --help` 或者 `docker-compose help [COMMAND]` 可查看具体某个命令的使用格式。

**支持的选项：**

- `-f, --file FILE` 指定使用的 Compose 模板文件，默认为 `docker-compose.yml`，可以多次指定。
- `-p, --project-name NAME` 指定项目名称，默认将使用所在目录名称作为项目名。
- `--verbose` 输出更多调试信息。
- `-v, --version` 打印版本并退出。

## `docker-compose build` 命令

**使用格式：**

```
docker-compose build [options] [SERVICE...]
```

构建（重新构建）项目中的服务容器。

服务容器一旦构建后，将会带上一个标记名，例如对于 web 项目中的一个 db 容器，可能是 web_db。

可以随时在项目目录下运行 `docker-compose build` 来重新构建服务。

**支持的选项：**

- `--force-rm` 删除构建过程中的临时容器。
- `--no-cache` 构建镜像过程中不使用 cache（这将加长构建过程）。
- `--pull` 始终尝试通过 pull 来获取更新版本的镜像。

## `docker-compose config` 命令

验证 Compose 文件格式是否正确，若正确则显示配置，若格式错误显示错误原因。

**使用格式：**

```
docker-compose config [选项]
```

**支持的选项：**

- `-q, --quiet` 只验证配置，不输出。 当配置正确时，不输出任何内容，当文件配置错误，输出错误信息。
- `--services` 打印服务名，一行一个验证和查看compose文件配置。

## `docker-compose down` 命令

此命令将会停止 `up` 命令所启动的容器，并移除网络。

**使用格式：**

```
docker-compose down [选项]
```

**支持的选项：**

- --rmi type 删除镜像，类型必须是:

'all': 删除compose文件中定义的所以镜像。

'local': 删除镜像名为空的镜像

- -v, --volumes 删除卷
- --remove-orphans 删除Compose文件中未定义的服务。

停止和删除容器、网络、卷、镜像，这些是通过docker-compose up命令创建的. 默认值删除 容器 网络，可以通过指定 rmi volumes参数删除镜像和卷

## `docker-compose exec` 命令

进入指定的容器。

**使用格式：**

```
docker-compose exec [选项] [-e KEY=VAL...] SERVICE COMMAND [ARGS...]
```

**支持的选项：**

- `-d` 分离模式，后台运行命令.
- `--privileged` 获取特权.
- `--user USER` 指定运行的用户.
- `-T` 禁用分配TTY.`docker-compose exec`默认分配 a TTY.
- `--index=index` 当一个服务拥有多个容器时，可通过该参数登陆到该服务下的任何服务，例如：docker-compose exec --index=1 web /bin/bash ，web服务中包含多个容服务实例 [default: 1]和docker exec命令功能相同，可以通过service name登陆到容器中。

## `docker-compose help` 命令

获得一个命令的帮助信息。

## `docker-compose images` 命令

列出 Compose 文件中包含的镜像。

**使用格式：**

```
docker-compose images [选项] [SERVICE...]
```

**支持的选项：**

- `-q, --quiet` 只显示id

## `docker-compose kill` 命令

通过发送 `SIGKILL` 信号来强制停止服务容器。

**使用格式：**

```
docker-compose kill [options] [SERVICE...]
```

**支持的选项：**

- `-s SIGNAL` 支持通过 `-s` 参数来指定发送的信号，例如通过如下指令发送 `SIGINT` 信号。

```
$ docker-compose kill -s SIGINT
```

## `docker-compose logs` 命令

查看服务容器的输出。默认情况下，docker-compose 将对不同的服务输出使用不同的颜色来区分。可以通过 `--no-color` 来关闭颜色。该命令在调试问题的时候十分有用。

**使用格式：**

```
docker-compose logs [options] [SERVICE...]
```

**支持的选项：**

- `--no-color` 单色输出，不显示其他颜.
- `-f, --follow` 跟踪日志输出，就是可以实时查看日志
- `-t, --timestamps` 显示时间戳
- `--tail` 从日志的结尾显示，--tail=200，显示日志输出。

## `docker-compose pause` 命令

暂停一个正在运行的服务容器。

**使用格式：**

```
docker-compose pause [SERVICE...]
```

> 可以使用 `docker-compose unpause` 进行恢复。

## `docker-compose port` 命令

打印某个容器端口所映射的公共端口。

**使用格式：**

```
docker-compose port [options] SERVICE PRIVATE_PORT
```

**支持的选项：**

- `--protocol=proto` 指定端口协议，tcp（默认值）或者 udp。
- `--index=index` 如果同一服务存在多个容器，指定命令对象容器的序号（默认为 1）。

## `docker-compose ps` 命令

列出项目中目前的所有容器。

**使用格式：**

```
docker-compose ps [options] [SERVICE...]
```

**支持的选项：**

- `-q` 只打印容器的 ID 信息。

## `docker-compose pull` 命令

拉取服务依赖的镜像。

**使用格式：**

```
docker-compose pull [options] [SERVICE...]
```

**支持的选项：**

- `--ignore-pull-failures` 忽略拉取镜像过程中的错误。

## `docker-compose push` 命令

推送服务依赖的镜像到 Docker 镜像仓库。

**使用格式：**

```
docker-compose push [选项] [SERVICE...]
```

**支持的选项：**

- `--ignore-push-failures` 忽略错误。

## `docker-compose restart` 命令

重启项目中的服务。

**使用格式：**

```
docker-compose restart [options] [SERVICE...]
```

**支持的选项：**

- `-t, --timeout TIMEOUT` 指定重启前停止容器的超时（默认为 10 秒）。

## `docker-compose rm` 命令

删除所有（停止状态的）服务容器。推荐先执行 `docker-compose stop` 命令来停止容器。

**使用格式：**

```
docker-compose rm [options] [SERVICE...]
```

**支持的选项：**

- `-f, --force` 强制直接删除，包括非停止状态的容器。一般尽量不要使用该选项。
- `-v` 删除容器所挂载的数据卷。

## `docker-compose run` 命令

在指定服务上执行一个命令。

**使用格式：**

```
docker-compose run [options] [-p PORT...] [-e KEY=VAL...] SERVICE [COMMAND] [ARGS...]
```

例如：

```
$ docker-compose run ubuntu ping docker.com
```

将会启动一个 ubuntu 服务容器，并执行 `ping docker.com` 命令。

默认情况下，如果存在关联，则所有关联的服务将会自动被启动，除非这些服务已经在运行中。

该命令类似启动容器后运行指定的命令，相关卷、链接等等都将会按照配置自动创建。

两个不同点：

- 给定命令将会覆盖原有的自动运行命令；
- 不会自动创建端口，以避免冲突。

如果不希望自动启动关联的容器，可以使用 `--no-deps` 选项，例如

```
$ docker-compose run --no-deps web python manage.py shell
```

将不会启动 web 容器所关联的其它容器。

**支持的选项：**

- `-d` 后台运行容器。
- `--name NAME` 为容器指定一个名字。
- `--entrypoint CMD` 覆盖默认的容器启动指令。
- `-e KEY=VAL` 设置环境变量值，可多次使用选项来设置多个环境变量。
- `-u, --user=""` 指定运行容器的用户名或者 uid。
- `--no-deps` 不自动启动关联的服务容器。
- `--rm` 运行命令后自动删除容器，`d` 模式下将忽略。
- `-p, --publish=[]` 映射容器端口到本地主机。
- `--service-ports` 配置服务端口并映射到本地主机。
- `-T` 不分配伪 tty，意味着依赖 tty 的指令将无法运行。

## `docker-compose scale` 命令

设置指定服务运行的容器个数。

**使用格式：**

```
docker-compose scale [options] [SERVICE=NUM...]
```

通过 `service=num` 的参数来设置数量。例如：

```
$ docker-compose scale web=3 db=2
```

将启动 3 个容器运行 web 服务，2 个容器运行 db 服务。

一般的，当指定数目多于该服务当前实际运行容器，将新创建并启动容器；反之，将停止容器。

**支持的选项：**

- `-t, --timeout TIMEOUT` 停止容器时候的超时（默认为 10 秒）。

## `docker-compose start` 命令

启动已经存在的服务容器。

**使用格式：**

```
docker-compose start [SERVICE...]
```

## `docker-compose stop` 命令

停止已经处于运行状态的容器，但不删除它。通过 `docker-compose start` 可以再次启动这些容器。

**使用格式：**

```
docker-compose stop [options] [SERVICE...]
```

**支持的选项：**

- `-t, --timeout TIMEOUT` 停止容器时候的超时（默认为 10 秒）。

## `docker-compose top` 命令

查看各个服务容器内运行的进程。

**使用格式：**

```
docker-compose top [SERVICE...]
```

## `docker-compose unpause` 命令

恢复处于暂停状态中的服务。

使用格式：

```
docker-compose unpause [SERVICE...]
```

## `docker-compose up` 命令

该命令十分强大，它将尝试自动完成包括构建镜像，（重新）创建服务，启动服务，并关联服务相关容器的一系列操作。

链接的服务都将会被自动启动，除非已经处于运行状态。

可以说，大部分时候都可以直接通过该命令来启动一个项目。

默认情况，`docker-compose up` 启动的容器都在前台，控制台将会同时打印所有容器的输出信息，可以很方便进行调试。

当通过 `Ctrl-C` 停止命令时，所有容器将会停止。

如果使用 `docker-compose up -d`，将会在后台启动并运行所有的容器。一般推荐生产环境下使用该选项。

默认情况，如果服务容器已经存在，`docker-compose up` 将会尝试停止容器，然后重新创建（保持使用 `volumes-from` 挂载的卷），以保证新启动的服务匹配 `docker-compose.yml` 文件的最新内容。如果用户不希望容器被停止并重新创建，可以使用 `docker-compose up --no-recreate`。这样将只会启动处于停止状态的容器，而忽略已经运行的服务。如果用户只想重新部署某个服务，可以使用 `docker-compose up --no-deps -d <SERVICE_NAME>` 来重新创建服务并后台停止旧服务，启动新服务，并不会影响到其所依赖的服务。

**使用格式：**

```
docker-compose up [options] [SERVICE...]
```

**支持的选项：**

- `-d` 在后台运行服务容器。
- `--no-color` 不使用颜色来区分不同的服务的控制台输出。
- `--no-deps` 不启动服务所链接的容器。
- `--force-recreate` 强制重新创建容器，不能与 `--no-recreate` 同时使用。
- `--no-recreate` 如果容器已经存在了，则不重新创建，不能与 `--force-recreate` 同时使用。
- `--no-build` 不自动构建缺失的服务镜像。
- `-t, --timeout TIMEOUT` 停止容器时候的超时（默认为 10 秒）。

