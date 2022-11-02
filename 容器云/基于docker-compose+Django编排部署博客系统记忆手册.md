```sh
FROM centos:centos7.9.2009
MAINTAINER Chinaskills
RUN rm -rf /etc/yum.repos.d/*
COPY local.repo /etc/yum.repos.d/
COPY yum /root/yum
RUN yum install -y libevent libevent-devel
RUN yum -y install memcached
EXPOSE 11211         #此端口是干什么的          
#memcached的端口
ENTRYPOINT /usr/bin/memcached  -u root    #这是什么意思
#以root身份后台启动memcached
```

```sh
#!/bin/bash
mysql_install_db --user=root
mysqld_safe --user=root &       #后台运行 mysqld安全模式用于修改密码
sleep 8
mysqladmin -u root password 'root'
mysql -uroot -proot -e "grant all on *.* to 'root'@'%' identified by 'root'; flush privileges;"
mysql -uroot -proot -e "create database djangoblog;use djangoblog;source /opt/sqlfile.sql;"
```

```sh
FRON centos:centos7.9.2009
MAINTAINER Yan
RUN rm -rf /etc/yum.repos.d/*
COPY local.repo /etc/yum.repos.d/
COPY yum /root/yum
ENV LC_ALL en_US.UTF-8
RUN yum install -y mariadb-server
COPY mysql_init.sh /opt/
COPY sqlfile.sql /opt/
RUN bash /opt/mysql_init.sh
EXPOSE 3306
CMD ["mysqld_safe","--user=root"]
```

```sh
[root@k8s-master-node1 ~]# locale
LANG=en_US.utf8
LC_CTYPE="en_US.utf8"
LC_NUMERIC="en_US.utf8"
LC_TIME="en_US.utf8"
LC_COLLATE="en_US.utf8"
LC_MONETARY="en_US.utf8"
LC_MESSAGES="en_US.utf8"
LC_PAPER="en_US.utf8"
LC_NAME="en_US.utf8"
LC_ADDRESS="en_US.utf8"
LC_TELEPHONE="en_US.utf8"
LC_MEASUREMENT="en_US.utf8"
LC_IDENTIFICATION="en_US.utf8"
LC_ALL=
```

```dockerfile
[root@k8s-worker-node1 DjangoBlog]# cat Dockerfile-nginx
FROM centos:centos7.9.2009
MAINTAINER Chinaskills
RUN rm -rf /etc/yum.repos.d/*
COPY local.repo /etc/yum.repos.d/
COPY yum /root/yum
RUN yum -y install nginx
ADD nginx.conf /etc/nginx/nginx.conf
RUN /bin/bash -c 'echo init ok'          #有什么用
EXPOSE 80
CMD ["nginx","-g","daemon off;"]         #关闭守护进程
# 确保nginx为pid 1 运行状态 
```

```sh
FROM centos:centos7.9.2009
MAINTAINER Chinaskills
RUN rm -rfv /etc/yum.repos.d/*
COPY local.repo /etc/yum.repos.d/
COPY yum /root/yum
RUN yum install -y make openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel gcc gcc-devel python-devel mysql-devel
COPY Python-3.6.5.tgz /opt                 #这里要使用COPY 不能用ADD
RUN tar -zxvf /opt/Python-3.6.5.tgz
RUN mv Python-3.6.5 /usr/local
RUN cd /usr/local/Python-3.6.5/ && ./configure && make && make install
RUN ln -s /usr/local/python3/bin/python3 /usr/bin/python3
RUN ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
ADD requirements.txt requirements.txt
COPY Python-pip /opt
RUN pip3 install --upgrade pip --no-index --find-links=/opt   
#--no-index --find-links选项进行离线安装
#--no-index 代表忽视pip 忽视默认的依赖包索引
#--find-links= 代表从你指定的目录寻下找离线包
#-r、 --requirement<file>从给定的需求文件安装。此选项可以多次使用。
RUN pip3 install -r requirements.txt --no-index --find-links=/opt
RUN pip3 install gunicorn[gevent] --no-index --find-links=/opt
RUN pip3 cache purge
RUN mkdir -p /code/djangoBlog
ADD . /code/djangoBlog/
RUN chmod +x /code/djangoBlog/bin/docker_start.sh
ENTRYPOINT ["/code/djangoBlog/bin/docker_start.sh"]
```

```yaml
version: '3'
services:
  memcached:
    restart: always
    image: blog-memcached:v1.0
    container_name: blog-memcached
    ports:
      - "11211:11211"
  db:
    image: blog-mysql:v1.0
    restart: always
    environment:
      - MYSQL_DATABASE=djangoblog
      - MYSQL_ROOT_PASSWORD=root
    ports:
      - 3306:3306
    depends_on:
      - memcached
    container_name: blog-mysql
  djangoblog:
    image: blog-service:v1.0
    restart: always
    ports:
      - "8000:8000"
    environment:
      - DJANGO_MYSQL_DATABASE=djangoblog
      - DJANGO_MYSQL_USER=root
      - DJANGO_MYSQL_PASSWORD=root
      - DJANGO_MYSQL_HOST=db
      - DJANGO_MYSQL_PORT=3306
      - DJANGO_MEMCACHED_LOCATION=memcached:11211
    volumes:
      - ./collectedstatic:/code/djangoBlog/collectedstatic
    links:
      - db
      - memcached
    depends_on:
      - db
    container_name: blog-service
  nginx:
    restart: always
    image: blog-nginx:v1.0
    volumes:
      - ./collectedstatic:/code/djangoblog/collectedstatic
    ports:
      - "8888:80"
      - "443:443"
    links:
      - djangoblog:djangoblog
    container_name: blog-nginx
```

```
docker-compose up -d
docker-compose ps
```

