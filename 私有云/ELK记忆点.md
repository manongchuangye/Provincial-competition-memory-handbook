

配置/etc/logstash/logstash.yml,修改增加第190行如下

```
[root@elk-2 ~]# vi /etc/logstash/logstash.yml
http.host: "172.128.11.17"   //第二台主机名称
```

配置logstash收集syslog日志：

```sh
[root@elk-2 ~]# vi /etc/logstash/conf.d/syslog.conf
#　输入
input {
  file {
   	  #path含义是标明需要读取的文件位置
      path => "/var/log/messages"
      # type字段，可表明导入的日志类型
      type => "systemlog"
      #logstash 从什么 位置开始读取文件数据， 默认是结束位置 也可以设置为：beginning 从头开始
      start_position => "beginning"
      #logstash 每隔多 久检查一次被监听文件状态（ 是否有更新） ， 默认是 1 秒。
      stat_interval => "3"
  }
}
#　输出
output {
   if [type] == "systemlog" {
   
#输入到es集群中，当hosts 参数列出多个IP地址时，Logstash会在地址列表中对请求进行负载平衡。另请注意，Elasticsearch的默认端口是9200并且可以在上面的配置中省略。
      elasticsearch {
          hosts => ["172.128.11.10:9200"]   # elasticsearch 地址 端口 端口可省略
          index => "system-log-%{+YYYY.MM.dd}"   # 索引名称
      }
  }
}
```

```
[root@elk-2 ~]# chmod 644 /var/log/messages   //给这个文件赋权限，如果不给权限，则无法读取日志
```

```
[root@elk-2 ~]# ln -s /usr/share/logstash/bin/logstash /usr/bin
```

```sh
[root@elk-2 ~]# logstash --path.settings /etc/logstash/ -f /etc/logstash/conf.d/syslog.conf --config.test_and_exit

● --path.settings 用于指定logstash的配置文件所在的目录

● -f 指定需要被检测的配置文件的路径

● --config.test_and_exit 指定检测完之后就退出，不然就会直接启动了
```

启动服务后，有进程但是没有9600端口

```sh
[root@elk-2 ~]# ll /var/lib/logstash/
total 0
drwxr-xr-x. 2 root root 6 Feb 10 09:00 dead_letter_queue
drwxr-xr-x. 2 root root 6 Feb 10 09:00 queue
[root@elk-2 ~]# chown -R logstash /var/lib/logstash/
[root@elk-2 ~]# ll /var/lib/logstash/
total 0
drwxr-xr-x. 2 logstash root 6 Feb 10 09:00 dead_letter_queue
drwxr-xr-x. 2 logstash root 6 Feb 10 09:00 queue
[root@elk-2 ~]# systemctl restart logstash
```

