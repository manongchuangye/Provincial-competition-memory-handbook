```
导入基本镜像 Centos7.9.2009
```

``` bash
#!/bin/bash
mysql_install_db --user=root
mysqld_safe --user=root &
sleep 8
mysqladmin -u root password 'root'
mysql -uroot -proot -e "grant all on *.* to 'root'@'%' iaentified by 'root';flush privileges;"
mysql -uroot -proot -e "source /opt/pig.sql;source /opt/pig_codegen.sql;source /opt/pig_config.sql;source /opt/pig_job.sql;"
```



```dockerfile
FROM centos:centos7.9.2009
MAINTAINER Yan
RUN rm -rf /etc/yum.repos.d/*
COPY local.repo /etc/yum.repos.d/
COPY yum /root/yum
ENV LC_ALL en_US.UTF-8
RUN yum install -y mariadb-server      #不加server会默认安装客户端,会报错
COPY mysql /opt/
COPY mysql_init.sh /opt/
RUN bash /opt/mysql_init.sh
EXPOSE 3306
CMD ["mysqld_safe","--user=root"]
```



```dockerfile
FROM centos:centos7.9.2009
MAINTAINER Chinaskills
RUN rm -rf /etc/yum.repos.d/*
COPY local.repo /etc/yum.repos.d/
COPY yum /root/yum
RUN yum -y install redis
RUN sed -i 's/127.0.0.1/0.0.0.0/g' /etc/redis.conf && \
     sed -i 's/protected-mode yes/protected-mode no/g' /etc/redis.conf
EXPOSE 6379
CMD ["/usr/bin/redis-server","/etc/redis.conf"]
```

```bash
#!/bin/bash
sleep 20
nohup java -jar /root/pig-register.jar  $JAVA_OPTS  >/dev/null 2>&1 &
sleep 20
nohup java -jar /root/pig-gateway.jar  $JAVA_OPTS >/dev/null 2>&1 &
sleep 20
nohup java -jar /root/pig-auth.jar  $JAVA_OPTS >/dev/null 2>&1 &
sleep 20
nohup java -jar /root/pig-upms-biz.jar  $JAVA_OPTS >/dev/null 2>&1


$JAVA_OPTS 必须写，不写登录不进去
```



```dockerfile
FROM centos:centos7.9.2009
MAINTAINER Yan
RUN rm -rf /etc/yum.repos.d/*
COPY yum /root/yum
COPY local.repo /etc/yum.repos.d/*
COPY service /root/
RUN yum install -y java*
COPY pig_init.sh /root/
RUN chmod +x /root/pig_init.sh
EXPOSE 8848 9999 3000 4000
CMD ["/bin/bash","/root/pig_init.sh"]
```

```dockerfile
FROM centos:centos7.9.2009
MAINTAINER Yan
COPY yum /root/yum
RUN rm -rf /etc/yum.repos.d/*
COPY local.repo /etc/yum.repos.d/
RUN yum isntall -y nginx
COPY nginx/dist /data
ADD nginx/pig-ui.conf /etc/nginx/conf.d/
RUN /bin/bash -c 'echo init OK'
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
```

```dockerfile
FROM centos:centos7.9.2009
MAINTAINER Yan
RUN rm -rf /etc/yum.repos.d/*
COPY yum /root/yum
COPY local.repo /etc/yum.repos.d/
```

```yaml
version: '2'
services:
  pig-mysql:
    environment:
      MYSQL_ROOT_PASSWORD: root
    restart: always
    container_name: pig-mysql
    image: pig-mysql:v1.0
    ports:
      - 3306:3306
  pig-redis:
    image: pig-redis:v1.0
    ports:
      - 6379:6379
    restart: always
    container_name: pig-redis
    hostname: pig-redis
  pig-service:
    ports:
      - 8848:8848
      - 9999:9999
    restart: always
    container_name: pig-service
    hostname: pig-service
    image: pig-service:v1.0
    extra_hosts:
      - pig-register:127.0.0.1
      - pig-upms:127.0.0.1
      - pig-gateway:127.0.0.1
      - pig-auth:127.0.0.1
      - pig-hou:127.0.0.1
    stdin_open: true
    tty: true
    privileged: true
  pig-ui:
    restart: always
    container_name: pig-ui
    image: pig-ui:v1.0
    ports:
      - 8888:80
    links:
      - pig-service:pig-gateway   #其他links可以省略，没有此links这个容器会一直重启
```

```
[root@k8s-master-node1 Pig]# docker-compose down
[+] Running 5/4
 ⠿ Container pig-redis    Removed                                                   0.2s
 ⠿ Container pig-service  Removed                                                  10.3s
 ⠿ Container pig-ui       Removed                                                   0.1s
 ⠿ Container pig-mysql    Removed                                                  10.3s
 ⠿ Network pig_default    Removed                                                   0.0s
```

