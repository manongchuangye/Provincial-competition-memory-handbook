基于LNMP环境搭建zabbix

```
安装nginx
yum install -y nginx
systemctl enable --now nginx
netstat -natp | grep 80
```

```
安装mariadb
yum -y install mariadb-server mariadb
systemctl enable --now mariadb.service
netstat -natp | grep 3306
初始化mysql
```

```
安装php
yum install -y php72w php72w-devel php72w-fpm php72w-gd php72w-mbstring php72w-mysql			#安装环境依赖包
systemctl enable --now php-fpm 
```

```
建立数据库及用户并授权
```

```
安装zabbix
yum -y install zabbix-server-mysql zabbix-web-mysql zabbix-agents
```

```
导入数据库脚本
zcat /usr/share/doc/zabbix-server-mysql*/create.sql.gz | mysql -uzabbix -padmin123 zabbix
修改zabbix配置文件
```

