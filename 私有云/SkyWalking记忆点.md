

```sh
#配置elasticsearch
[root@node-1 elasticsearch-7.17.0]# vi config/elasticsearch.yml
…
cluster.name: my-application             #集群名称
node.name: node-1                        #当前节点名称
path.data: /opt/elasticsearch-7.17.0/data          # 索引文件存储目录
path.logs: /opt/elasticsearch-7.17.0/logs          # 日志文件存储目录
network.host: 0.0.0.0                       #对外提供服务的IP地址
cluster.initial_master_nodes: ["node-1"]        #
… 
http.cors.enabled: true                     #开启跨域访问       记
http.cors.allow-origin: "*"                 #跨域访问允许的域名地址       记
http.cors.allow-headers: Authorization,X-Requested-With,Content-Length,Content-Type
#允许HTTP请求头返回类型       记
```

```

```

```
不能使用root进行启动，创建新用户并授权elasticsearch

需要修改资源限制及内核配置
nofile 65536
nproc 4096+

vm.max_map_count=262144
```

```sh
[root@mall ~]# vi /etc/my.cnf        #有必要写吗
[mysqld]
…
init_connect='SET collation_connection = utf8_unicode_ci'
init_connect='SET NAMES utf8'           #初始字符集
character-set-server=utf8               #中文乱码
collation-server=utf8_unicode_ci        
skip-character-set-client-handshake     #此处是忽略客户端的字符集，使用服务器的设置
```

```
修改SElinux策略内各项规则的布尔值
 setsebool -P httpd_can_network_connect 1  #httpd可以连接到网络
```

```
 mysqladmin -uroot password 123456
 设置root用户密码为123456
 
 grant all privileges on *.* to root@localhost identified by '123456' with grant option;
 
grant all privileges on *.* to root@"%" identified by '123456' with grant option;
```

```sh
[root@mall ~]# vi agent/config/agent.config
…
agent.service_name=${SW_AGENT_NAME:my-application}    
# 展示界面中现实服务名称
agent.sample_n_per_3_secs=${SW_AGENT_SAMPLE:1}
…
# 每3秒采样道数默认情况下，负或零表示关闭

collector.backend_service=${SW_AGENT_COLLECTOR_BACKEND_SERVICES:172.128.11.32:11800}
…
# skywalking后端服务地址
```

```
Java1.8 之后要用java -version 
[root@node-1 jdk1.8.0_144]# java -v      #报错
Unrecognized option: -v
Error: Could not create the Java Virtual Machine.
Error: A fatal exception has occurred. Program will exit.
[root@node-1 jdk1.8.0_144]# java -version     #不报错
java version "1.8.0_144"
Java(TM) SE Runtime Environment (build 1.8.0_144-b01)
Java HotSpot(TM) 64-Bit Server VM (build 25.144-b01, mixed mode)
```

```
./kafka-server-start.sh -daemon ../config/server.properties 
```

```
journalctl -xe
查看详细日志
```

