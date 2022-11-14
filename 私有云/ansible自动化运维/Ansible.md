1. 建立免密通信

2. 测试连通信

```
 ansible all -i 172.18.0.3,172.18.0.4 -m ping
 -i  指定资产 参数后⾯接的是⼀个列表(List)
```

3. 发送文件

```
 ansible all -i 172.18.0.3,172.18.0.4 -m copy -a "src=/tmp/a.conf dest=/tmp/a.conf"
-m 指定模块
-a 指定命令参数
```

4. 资产

```
静态资产
位于/ect/ansible/hosts
以IP地址的形式或者主机名的形式存在
若连续，可以使⽤[stat:end] 的形式去表达
定义成组，组和组之间可以存在继承关系

验证资产
  ansible all -i hosts --list-hosts
列举出选定资产
  ansible web_servers -i hosts --list-hosts
```

5. Ansible Ad-Hoc命令

```
ansible pattern [-i inventory] -m module -a argument
pattern 资产选择器
-i 指定资产清单⽂件的位置或直接指定资产
-m 指定本次Ansible ad-hoc 要执⾏的模块。可以类别成SHELL中的命令。
-a 模块的参数. 可以类⽐成SHELL 中的命令参数

ansible-doc -l 列出所有模块
ansible-doc modulename 查询某个模块使用方法
ansible-doc -s modulename 查询某个模块简洁使用方法

常用模块
1.
command & shell 模块
command模块是ad-hoc的默认模块,在执⾏ad-hoc时,若不指定模块的名字则默认使⽤此模块
shell 模块可以执⾏SHELL 的内置命令和 特性（⽐如管道符）
command 模块⽆法执⾏SHELL 的内置命令和特性
2.
script 模块
将管理节点上的脚本传递到被管理节点(远程服务器)上进⾏执⾏
ansible webservers -i hosts -m script -a "/root/a.sh"
3.
copy 模块
⽤于管理节点和被管理节点之间的⽂件拷⻉
ansible webservers -i hosts -m copy -a "src=./nginx.repo dest=/etc/yum.repos.d/nginx.repo backup=yes owner=nobody group=nobody mode=0755" 
backup=yes 在被管理节点上对原⽂件进⾏备份
owner=nobody group=nobody 对⽂件进⾏⽤户及⽤户组设置
mode=755 对⽂件进⾏权限设置
4.
yum_repsitory
添加 YUM 仓库
5.
yum
name 要安装的软件包名
state 对当前指定的软件安装、移除操作(present installed latest absent removed)
- present 确认已经安装，但不升级 - installed 确认已经安装 - latest 确保安装，且升级为最新 -absent 和 removed 确认已移除
 ansible webservers -i hosts -m yum -a "name=nginx state=present"
 ansible webservers -i hosts -m yum -a "name=nginx state=absent"
6.
systemd 模块
daemon_reload 重新载⼊ systemd
enabled 是否开机⾃启动 yes|no
name 必选项，服务名称
state 对当前服务执⾏启动，停⽌、重启、重新加载等操作(started,stopped,restarted,reloaded)
重载
  ansible webservers -i hosts -m systemd -a "daemon_reload=yes"
开机自启
  ansible webservers -i hosts -m systemd -a "name=nginx enabled=yes"
7.
file 模块
⽤于远程主机上的⽂件操作
path 必选项，定义⽂件/⽬录的路径
state (directory 如果⽬录不存在，创建⽬录
       file ⽂件不存在，则不会被创建
       link 创建软链接
       hard 创建硬链接
       touch 如果⽂件不存在，则会创建⼀个新的⽂件
       absent 删除⽬录、⽂件或者取消链接⽂件)
  ansible all -i hosts -m file -a "path=/tmp/foo.conf state=touch"
8.
template 模块
可以进⾏⽂档内变量的替换,⽂件以 .j2 结尾
    执⾏命令，并且设置变量 var 的值为 world
 ansible all -i hosts -m template -a "src=hello_world.j2 dest=/tmp/hello_world.world" -e "var=world"
```

6. Ansible Playbook

```
语法检测
--syntax-check
测试运⾏
-C
变量
{{ user }} 报错时加双引号

通过变量确认状态
- name: check nginx syntax
  shell: /usr/sbin/nginx -t
  register: nginxsyntax
- name: print nginx syntax
  debug: var=nginxsyntax
- name: start nginx server
  service: name=nginx state=started
  when: nginxsyntax.rc == 0

with_items 循环遍历变量
- name: create user
  user: name={{ item }} state=present
  with_items: "{{ createuser }}"
  
JinJa2必知必会
注释: {# 注释内容 #}
变量引⽤: {{ var }}
逻辑表达: {% %}
```

