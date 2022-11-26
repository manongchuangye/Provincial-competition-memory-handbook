### Docker安装mysql

```sh
docker run -p 3306:3306 --name mysql \
-v /mydata/mysql/log:/var/log/mysql \
-v /mydata/mysql/data:/var/lib/mysql \
-v /mydata/mysql/conf:/etc/mysql \
-e MYSQL_ROOT_PASSWORD=root \
-d mysql:5.7
```

![img](D:\疯狂内卷文件\云计算省赛准备\省赛记忆手册github\Provincial-competition-memory-handbook\容器云\Docker.assets\20210612125342610.png)

### docker安装redis

```bash
docker run -p 6379:6379 --name redis \
-v /mydata/redis/data:/data \
-v /mydata/redis/conf/redis.conf:/etc/redis/redis.conf \
-d redis redis-server /etc/redis/redis.conf    #-d 后面咋还有个redis，那是镜像服了也
```

### docker安装elastisearch与kibana

```bash

docker run --name elasticsearch -p 9200:9200 -p 9300:9300 \
-e "discovery.type=single-node" \
-e ES_JAVA_OPTS="-Xms64m -Xmx128m" \
-v /mydata/elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
-v /mydata/elasticsearch/data:/usr/share/elasticsearch/data \
-v /mydata/elasticsearch/plugins:/usr/share/elasticsearch/plugins \
-d elasticsearch:7.4.2

chmod -R 777 /mydata/elasticsearch/


docker run --name kibana --link=elasticsearch:es -p 5601:5601  -d kibana:7.4.2
##--link:是两个容器之间可以互相进行通信，elasticsearch:要链接的容器名称，es:链接别名

##修改kibana为中文
docker exec -it kibana sh
vi /usr/share/kibana/config/kibana.yml
##添加内容
i18n.locale: "zh-CN"
#退出容器
exit
#重启容器
docker restart kibana
#查看日志
docker logs -f kibana
```

### docker安装nginx

```
随便启动一个nginx实例，为了复制出配置
docker run -p80:80 --name nginx -d nginx:1.10   
将容器内的配置文件拷贝到/mydata/nginx/conf/ 下
docker container cp nginx:/etc/nginx/  /mydata/nginx/conf/ 
终止原容器：
docker stop nginx
执行命令删除原容器：
docker rm nginx

创建新的Nginx，执行以下命令
docker run -p 80:80 --name nginx \
 -v /mydata/nginx/html:/usr/share/nginx/html \
 -v /mydata/nginx/logs:/var/log/nginx \
 -v /mydata/nginx/conf/:/etc/nginx \
 -d nginx:1.10
```

### docker安装nacos 2.x

```
docker run -d \
-e MODE=standalone \
-e SPRING_DATASOURCE_PLATFORM=mysql \
-e MYSQL_SERVICE_HOST=172.17.0.5 \
-e MYSQL_SERVICE_PORT=3306 \
-e MYSQL_SERVICE_USER=root \
-e MYSQL_SERVICE_PASSWORD=root \
-e MYSQL_SERVICE_DB_NAME=ry-config \
-p 8848:8848 \
-p 9848:9848 \
-p 9849:9849 \
--restart=always \
--name nacos \
nacos/nacos-server
```

### docker安装gitlab

```
# -d：后台运行
# -p：将容器内部端口向外映射
# --name：命名容器名称
# -v：将容器内数据文件夹或者日志、配置等文件夹挂载到宿主机指定目录
#-p 8090:8090 这一块端口需要一致，不然gitlab的无法正常通信

docker run \
-p 443:443 \
-p 8090:8090 \
-p 222:22 \
--name gitlab \
--restart always \
-v /mydata/gitlab/config:/etc/gitlab \
-v /mydata/gitlab/logs:/var/log/gitlab \
-v /mydata/gitlab/data:/var/opt/gitlab \
-d gitlab/gitlab-ce

#修改配置文件
vim /mydata/gitlab/config/gitlab.rb
 
# 配置http协议所使用的访问地址,不加端口号默认为80
external_url 'http://192.168.15.55:8090'

# 配置ssh协议所使用的访问地址和端口
gitlab_rails['gitlab_ssh_host'] = '192.168.15.55'
gitlab_rails['gitlab_shell_ssh_port'] = 222 # 此端口是run时22端口映射的222端口
nginx['redirect_http_to_https_port'] = 8090  #web页面端口
:wq #保存配置文件并退出

初始化root用户密码
#进入目录
cd /opt/gitlab/bin
# 命令 开始初始化密码
./gitlab-rails console
```

在irb(main):001:0> 后面通过 **u=User.where(id:1).first** 来查找与切换账号（User.all 可以查看所有用户）

![img](D:\疯狂内卷文件\云计算省赛准备\省赛记忆手册github\Provincial-competition-memory-handbook\容器云\Docker.assets\70.png)

通过***\*u.password='12345678'\****设置密码为12345678(这里的密码看自己喜欢)：![img](D:\疯狂内卷文件\云计算省赛准备\省赛记忆手册github\Provincial-competition-memory-handbook\容器云\Docker.assets\70-16693429045755.png)

通过**\u.password_confirmation='12345678'**再次确认密码

通过 **u.save!**进行保存（切记切记 后面的 !）

### docker安装jenkins

```
#创建映射目录
mkdir -p /mydata/jenkins/config
mkdir -p /mydata/jenkins/data
 
 
#启动Jenkins镜像
docker run \
-u root \
-d \
-p 8080:8080 \
-p 50000:50000 \
-v /mydata/jenkins/config:/var/jenkins_home \
-v /mydata/jenkins/data:/var/run/docker.sock \
--name jenkins jenkinsci/blueocean
```

![img](D:\疯狂内卷文件\云计算省赛准备\省赛记忆手册github\Provincial-competition-memory-handbook\容器云\Docker.assets\watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4Mjc5ODMz,size_16,color_FFFFFF,t_70.png)

### docker安装registry

```
docker run \
 -p 5000:5000 \
 --restart=always \
 --name registry \
 -v /mydata/registry:/var/lib/registry \
 -d registry
 
 vim /etc/docker/daemon.json
 
{
"registry-mirrors": ["https://livzx7fm.mirror.aliyuncs.com"],
"log-driver":"json-file",
##设置日志大小限制 max-size=500m，意味着一个容器日志大小上限是500M， 
## max-file=3，意味着一个容器有三个日志，分别是id+.json、id+1.json、id+2.json
"log-opts": {"max-size":"500m", "max-file":"3"},
"insecure-registries":["192.168.15.59:5000"]
}
```

### docker安装rabbitmq

```
docker run -d --name rabbitmq \
-p 5672:5672 \               #5672，5671	AMQP 0-9-1 without and with TLSclient端通信口
-p 15672:15672 \             #15672	管理界面ui使用的端口    15671	管理监听端口
-v /mydata/rabbitmq/data:/var/lib/rabbitmq \
--hostname myRabbit \
-e RABBITMQ_DEFAULT_VHOST=my_vhost \
-e RABBITMQ_DEFAULT_USER=admin \
-e RABBITMQ_DEFAULT_PASS=admin \
-d rabbitmq:3.7.7

#开启web插件
docker exec -it rabbitmq sh
rabbitmq-plugins enable rabbitmq_management
exit 
docker restart rabbitmq 
#访问http://linuxip地址:15672，这里的用户名和密码默认都是admin

[root@localhost ~]# rabbitmq-plugins -h
Error: could not recognise command
Usage:
rabbitmq-plugins <command> [<command options>] 

Commands:
    list [-v] [-m] [-E] [-e] [<pattern>]
    enable <plugin> ...
    disable <plugin> ...
[root@localhost ~]# rabbitmq-plugins list 
[ ] amqp_client                       3.3.5
[ ] cowboy                            0.5.0-rmq3.3.5-git4b93c2d
[ ] eldap                             3.3.5-gite309de4
[ ] mochiweb                          2.7.0-rmq3.3.5-git680dba8
[ ] rabbitmq_amqp1_0                  3.3.5
[ ] rabbitmq_auth_backend_ldap        3.3.5
[ ] rabbitmq_auth_mechanism_ssl       3.3.5
[ ] rabbitmq_consistent_hash_exchange 3.3.5
[ ] rabbitmq_federation               3.3.5
[ ] rabbitmq_federation_management    3.3.5
[ ] rabbitmq_management               3.3.5
[ ] rabbitmq_management_agent         3.3.5
[ ] rabbitmq_management_visualiser    3.3.5
[ ] rabbitmq_mqtt                     3.3.5
[ ] rabbitmq_shovel                   3.3.5
[ ] rabbitmq_shovel_management        3.3.5
[ ] rabbitmq_stomp                    3.3.5
[ ] rabbitmq_test                     3.3.5
[ ] rabbitmq_tracing                  3.3.5
[ ] rabbitmq_web_dispatch             3.3.5
[ ] rabbitmq_web_stomp                3.3.5
[ ] rabbitmq_web_stomp_examples       3.3.5
[ ] sockjs                            0.3.4-rmq3.3.5-git3132eb9
[ ] webmachine                        1.10.3-rmq3.3.5-gite9359c7

rabbitmq有一个默认的账号密码guest，但该情况仅限于本机localhost进行访问，所以需要添加一个远程登录的用户
# 添加用户
rabbitmqctl add_user 用户名 密码

# 设置用户角色,分配操作权限
rabbitmqctl set_user_tags 用户名 角色

# 为用户添加资源权限(授予访问虚拟机根节点的所有权限)
rabbitmqctl set_permissions -p / 用户名 ".*" ".*" ".*"

```

### docker安装zookeeper与kafka

```
#启动镜像生成容器
docker run -p 2181:2181 --name zookeeper \
-v /etc/localtime:/etc/localtime \
-d --restart=always --log-driver json-file \
--log-opt max-size=100m --log-opt max-file=2 \
wurstmeister/zookeeper
 
#4、启动kafka镜像生成容器
docker run -p 9092:9092 --name kafka \
-v /etc/localtime:/etc/localtime \
-d --restart=always --log-driver json-file \
--log-opt max-size=100m --log-opt max-file=2 \
-e KAFKA_BROKER_ID=0 \
-e KAFKA_ZOOKEEPER_CONNECT=192.168.15.55:2181/kafka \
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://192.168.15.55:9092 \
-e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 \
wurstmeister/kafka
 
# 参数说明：
#192.168.15.55为服务器的ip，因为zookeeper的docker容器ip映射了服务器的ip，所以可以直接用服务器ip代理到容器
# -e KAFKA_BROKER_ID=0  在kafka集群中，每个kafka都有一个BROKER_ID来区分自己
# -e KAFKA_ZOOKEEPER_CONNECT=192.168.15.55:2181/kafka 配置zookeeper管理kafka的路径172.16.0.13:2181/kafka
# -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://192.168.15.55:9092  把kafka的地址端口注册给zookeeper，如果是远程访问要改成外网IP,类如Java程序访问出现无法连接。
# -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 配置kafka的监听端口
# -v /etc/localtime:/etc/localtime 容器时间同步虚拟机的时间
 
#5开机自启kafka
sudo docker update kafka--restart=always
 
# 6、验证kafka是否可以使用
 
# 6.1、进入容器
$ docker exec -it kafka sh
 
# 6.2、进入 /opt/kafka_2.12-2.3.0/bin/ 目录下
$ cd /opt/kafka_2.12-2.3.0/bin/
 
# 6.3、运行kafka生产者发送消息
$ ./kafka-console-producer.sh --broker-list localhost:9092 --topic sun
 
# 发送消息
> {"datas":[{"channel":"","metric":"temperature","producer":"ijinus","sn":"IJA0101-00002245","time":"1543207156000","value":"80"}],"ver":"1.0"}
 
# 6.4、运行kafka消费者接收消息
$ ./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic sun --from-beginning
 
```

