#encoding:utf-8
import os,click
@click.command()
@click.option('-c', '--command',default="server",prompt='--c Choose Openstack Manager Resource Types [flavor]flavor manager [server]server manager [image]image manager',help='Choose number')
@click.option('-a', '--action',prompt='action name',help='input your Action Name')
@click.option('-n', '--name',default="", required=False,prompt_required=False,prompt='Resource name',help='input your choose Resource Name')

def open_stack(command,action,name):
    if command == "flavor":
        click.echo("openstack flavor %s" %action)
        click.echo("openstack name %s" % name)
        cmd = "source /etc/keystone/admin-openrc.sh && " + "openstack flavor " + action + " " +  name
        print("cmd:", cmd)

        os.system(cmd)
    if command == "server":
        click.echo("openstack server %s" %action)
        click.echo("openstack name %s" % name)
        cmd = "source /etc/keystone/admin-openrc.sh && " + "openstack server " + action + " " +  name
        print("cmd:", cmd)

        os.system(cmd)

    if command == "image":
        click.echo("openstack image %s" %action)
        click.echo("openstack name %s" % name)
        cmd = "source /etc/keystone/admin-openrc.sh && " + "openstack image " + action + " " +  name
        print("cmd:", cmd)
        os.system(cmd)
if __name__ == "__main__":
    open_stack()

# 【题目4】基于Python click模块，实现OpenStack主机类型、主机与镜像的资源查询的命令行工具 [3分]
# 使用已建好的OpenStack Python运维开发环境，在/root目录下创建manager_openstack.py脚本。使用Python语言，基于Python click框架，对接云主机类型管理、云主机管理、镜像“查询”的程序，实现自定义的命令行管理工具，命令同openstack命令保持一致，并完成单元测试python代码编写，完成后提交实现代码文件。支持的参数要求如下：
# （1）参数“-c或--command”支持指定查询资源类型，类型为string。
# （2）参数“-a或--action”支持指定查询资源操作，类型为string。
# （3）参数“-n或--name”支持指定查询资源操作具体名称，类型为string。
#
# （3）支撑云主机类、镜像、云主机的资源的操作，命令同openstack命令保持一致。
# 命令行案例如下：
# 查询所有云主机类型：
# python3 manager_openstack.py -c flavor -a list
# 查询名称为flavor01的云主机类型：
# python3 manager_openstack.py -c flavor -a show -n flavor01
# 查询所有镜像：
# python3 manager_openstack.py -c image -a list
# 查询名称为cirros0001的镜像：
# python3 manager_openstack.py -c image -a show -n cirros0001
# 查询所有云主机：
# python3 manager_openstack.py -c server -a list
# 查询名称为server001的云主机：
# python3 manager_openstack.py -c server -a show -n server001

