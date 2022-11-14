Kubevirt 主要实现了下面几种资源，以实现对[虚拟机](https://so.csdn.net/so/search?q=虚拟机&spm=1001.2101.3001.7020)的管理：

- `VirtualMachineInstance（VMI）` : 类似于 kubernetes Pod，是**管理虚拟机的最小资源**。一个 `VirtualMachineInstance` 对象即表示一台正在运行的虚拟机实例，包含一个虚拟机所需要的各种配置。通常情况下用户不会去直接创建 VMI 对象，而是创建更高层级的对象，即 VM 和 VMRS。
- `VirtualMachine（VM）` : 为集群内的 `VirtualMachineInstance` 提供管理功能，例如开机/关机/重启虚拟机，确保虚拟机实例的启动状态，与虚拟机实例是 1:1 的关系，类似与 `spec.replica` 为 1 的 StatefulSet。
- `VirtualMachineInstanceReplicaSet（VMIS）` : 类似 `ReplicaSet`，可以启动指定数量的 `VirtualMachineInstance`，并且保证指定数量的 `VirtualMachineInstance` 运行，可以配置 HPA。

查看kubevirt组件

```
kubectl get pod -n kubevirt
```

![image-20221114144322448](D:\疯狂内卷文件\云计算省赛准备\省赛记忆手册github\Provincial-competition-memory-handbook\容器云\Kubevirt\kubevirt.assets\image-20221114144322448.png)

启动虚拟机

部署VirtualMachineInstance

kubectl apply -f vmi.yaml

```yaml
# $ cat vmi.yaml
apiVersion: kubevirt.io/v1alpha3
kind: VirtualMachineInstance
metadata:
  name: testvmi-nocloud
spec:
  terminationGracePeriodSeconds: 30
  domain:
    resources:
      requests:
        memory: 1024M
    devices:
      disks:
      - name: containerdisk
        disk:
          bus: virtio
      - name: emptydisk
        disk:
          bus: virtio
      - disk:
          bus: virtio
        name: cloudinitdisk
  volumes:
  - name: containerdisk
    containerDisk:
      image: kubevirt/fedora-cloud-container-disk-demo:latest
  - name: emptydisk
    emptyDisk:
      capacity: "2Gi"
  - name: cloudinitdisk
    cloudInitNoCloud:
      userData: |-
        #cloud-config
        password: fedora
        chpasswd: { expire: False }
```

通过console访问vmi

![在这里插入图片描述](D:\疯狂内卷文件\云计算省赛准备\省赛记忆手册github\Provincial-competition-memory-handbook\容器云\Kubevirt\kubevirt.assets\cd4628b85a8c4ac5bb39ef669fa7604a.png)

开启快照功能和迁移功能

```

kubectl create   configmap kubevirt-config -n kubevirt --from-literal=debug.useEmulation=true --from-literal=feature-gates=Macvtap,LiveMigration,Snapshot
# LiveMigration 开启迁移功能                  #虚拟机必须开
# Snapshot 开启快照功能
```

基本命令

```
# 查看虚拟机模板
kubectl get vm

# 启动虚拟机
virtctl start test-vm

# 查看虚拟机实例
kubectl get vmi

# 连接实例
virtctl console test-vm
```

模板

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: testvm
spec:
  running: false
  template:
    metadata:
      labels:
        kubevirt.io/size: small
        kubevirt.io/domain: testvm
    spec:
      domain:
        devices:
          disks:
            - name: containerdisk
              disk:
                bus: virtio
            - name: cloudinitdisk
              disk:
                bus: virtio
          interfaces:
          - name: default
            masquerade: {}
        resources:
          requests:
            memory: 64M
      networks:
      - name: default
        pod: {}
      volumes:
        - name: containerdisk
          containerDisk:
            image: quay.io/kubevirt/cirros-container-disk-demo
        - name: cloudinitdisk
          cloudInitNoCloud:
            userDataBase64: SGkuXG4=
```

创建VirtualMachine（(vm)类似于docker镜像一个模板可以启动很多运行实例vmi）

```yaml
[root@master kubevirt]# cat test.yaml
apiVersion: kubevirt.io/v1alpha3
kind: VirtualMachine
metadata:
  labels:
    kubevirt.io/vm: vm-cirros
  name: vm-cirros
spec:
  running: false
  template:
    metadata:
      labels:
        kubevirt.io/vm: vm-cirros
    spec:
      domain:
        devices:
          disks:
          - disk:
              bus: virtio
            name: containerdisk
          - disk:
              bus: virtio
            name: cloudinitdisk
        machine:
          type: ""
        resources:
          requests:
            memory: 64M
      terminationGracePeriodSeconds: 0
      volumes:
      - name: containerdisk
        containerDisk:
          image: kubevirt/cirros-container-disk-demo:latest
      - cloudInitNoCloud:
          userDataBase64: IyEvYmluL3NoCgplY2hvICdwcmludGVkIGZyb20gY2xvdWQtaW5pdCB1c2VyZGF0YScK
        name: cloudinitdisk
[root@master kubevirt]# kubectl apply -f test.yaml
virtualmachine.kubevirt.io/vm-cirros created

[root@master kubevirt]# kubectl get vm
NAME        AGE   VOLUME
vm-cirros   21m
```

启动VirtualMachineInstance（（vmi）类似于docker镜像的运行实例容器）

```bash
[root@master kubevirt]# virtctl start vm-cirros
VM vm-cirros was scheduled to start
[root@master kubevirt]# kubectl get vmi
NAME        AGE   PHASE     IP            NODENAME
vm-cirros   62s   Running   10.244.0.15   master

[root@master kubevirt]# virtctl console vm-cirros  # 进入虚拟机
Successfully connected to vm-cirros console. The escape sequence is ^]

login as 'cirros' user. default password: 'gocubsgo'. use 'sudo' for root.
vm-cirros login: cirros
Password:
$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc pfifo_fast qlen 1000
    link/ether 2e:3e:2a:46:29:94 brd ff:ff:ff:ff:ff:ff
    inet 10.244.0.16/24 brd 10.244.0.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::2c3e:2aff:fe46:2994/64 scope link tentative flags 08
       valid_lft forever preferred_lft forever
       
$    #  按 ctrl+]  退出虚拟机
$ [root@master kubevirt]#

```

启动和停止命令

```sh
spec.running 字段如果设置为true为启动、false为停止
# Start the virtual machine:  启动虚拟机
virtctl start vm   

# Stop the virtual machine:  停止虚拟机
virtctl stop vm

#kubectl也可以使用：   启动虚拟机
kubectl patch virtualmachine vm --type merge -p \
    '{"spec":{"running":true}}'
# 停止虚拟机
kubectl patch virtualmachine vm --type merge -p \
    '{"spec":{"running":false}}'
```

![image-20221114185520002](D:\疯狂内卷文件\云计算省赛准备\省赛记忆手册github\Provincial-competition-memory-handbook\容器云\Kubevirt\kubevirt.assets\image-20221114185520002.png)

vm作为服务公开

```sh
VirtualMachine可以作为服务公开。实际服务将在 VirtualMachineInstance 启动后可用
在创建VirtualMachine 后，将 SSH端口 (22) 公开为NodePort服务
[root@master kubevirt]# virtctl expose virtualmachine  vm-cirros --name vmiservice-node  --target-port 22  --port 24 --type NodePort
Service vmiservice-node successfully exposed for virtualmachine vm-cirros
[root@master kubevirt]# kubectl get svc
NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes        ClusterIP   10.96.0.1       <none>        443/TCP        95d
vmiservice-node   NodePort    10.106.62.191   <none>        24:31912/TCP   3s
```

最后使用**远程工具连接**即可：

** **注意** 端口使用svc **`NodePort端口`**，如图所示：

![255qE5oqA5pyvTG9ncw==,size_20,color_FFFFFF,t_70,g_se,x_16)](D:\疯狂内卷文件\云计算省赛准备\省赛记忆手册github\Provincial-competition-memory-handbook\容器云\Kubevirt\kubevirt.assets\watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP5Y-255qE5oqA5pyvTG9ncw==,size_20,color_FFFFFF,t_70,g_se,x_16.png)

![在这里插入图片描述](D:\疯狂内卷文件\云计算省赛准备\省赛记忆手册github\Provincial-competition-memory-handbook\容器云\Kubevirt\kubevirt.assets\watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP5Y-255qE5oqA5pyvTG9ncw==,size_20,color_FFFFFF,t_70,g_se,x_16-16684151617465.png)

![在这里插入图片描述](D:\疯狂内卷文件\云计算省赛准备\省赛记忆手册github\Provincial-competition-memory-handbook\容器云\Kubevirt\kubevirt.assets\watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP5Y-255qE5oqA5pyvTG9ncw==,size_20,color_FFFFFF,t_70,g_se,x_16-16684151690288.png)