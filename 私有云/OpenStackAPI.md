# Keystone

所用的api调用都需要keystone的支持，我们获取keystone的令牌才可以进行其他操作

## URL

```http
http://<ip>:5000/v3/auth/tokens
```

## 获取token

Post

```python
{
    "auth":{
        "identity":{	#认证对象
            "methods":["password"],	#表示使用何种方式鉴权，这里使用账户名+密码的方式
            "password":{	#鉴权方式
                "user":{	#用户对象
                    "name":<用户名>,	#用户对象的用户名
                    "password":<密码>,	#用户对象的密码
                    "domain":{"name":<域>}	#用户的域
                }
            }
        },
    	"scope":{	#指定权限的范围
            "project":{	#表示在这个项目下权限才有效
                "name":<项目名>,	#项目名称
                "domain":{"name":<域>}	#项目的域
            }
        }
    }
}
```

响应数据

获取令牌的请求中，最重要的就是header里的信息的

header头部信息里包括`X-Subject-Token`就是令牌，之后调用其他api需要在头部指定token信息`X-Auth-Token`

```python
{
    "X-Subject-Token": <token>
}
```

## python演示

```python
import requests,json #调用api需要的包，requests用来发送http请求，json用来解析json数据格式

url = "http://10.0.0.10:5000/v3/auth/tokens"
body = {
    "auth":{
        "identity":{
            "methods":["password"],
            "password":{
                "user":{
                    "name":"admin",
                    "password":"000000",
                    "domain":{"name":"demo"}
                }
            }
        },
        "scope":{
            "project":{
                "name":"demo",
                "domain":"demo"
            }
        }
    }
}
token = requests.post(url,json.dumps(body)).headers["X-Subject-Token"]
```

>   Json.dumps	将字典类型的格式转换为json字符串格式

# Neutron

## URL

网络

```http
http://<ip>:9696/v2.0/networks
```

子网

```http
http://<ip>:9696/v2.0/subnets
```

路由

```http
http://<ip>:9696/v2.0/routers
```

## 创建网络

Post

```python
{
    "network":{
        "name":<网络名>,
        "provider:network_type": <网络类型(flat/vxlan)>,
        "provider:pyhsical_network" <物理网络名称>, #当网络类型为flat时需要指定物理网络名称
        "provider:segmentation_id": <段ID>, #当网络类型为vxlan时需要指定段ID
        "router:external": <("true"/"false")>, #设置网络是否是外部网络，一般指定flat网络为外部网络
        "shared": <("true"/"false")>, #设置网络是否是共享在多个项目中，如果为false则改网络只在当前项目中
        "is_default": <("true"/"false")> #指定这个网络是否是默认网络
    }
}
```

## 删除网络

Delete

```http
http://<ip>:9696/v2.0/networks/<被删除的网络ID>
```

## 修改网络

put

```http
http://<ip>:9696/v2.0/networks/<被修改的网络ID>
```

```python
{
    "network":{
        <修改项>: <值>
    }
}
```

## 获取网络列表

get

```http
http://<ip>:9696/v2.0/networks
```



## 创建子网

Post

```python
{
    "subnet":{
        "name": <子网名称>,
        "network_id": <网络ID>,	#与之绑定的网络ID
        "ip_version": <(4/6)>,	#IP协议版本 ipv4 ipv6
        "cidr": <子网范围>,	#子网的范围格式为 x.x.x.x/x
        "gateway_ip": <网关ip>
        "allocation_pools":[	#可供分配的ip(可选)
            {
                "start": <启始ip>,
                "end": <结束ip>
            }
        ]
    }
}
```

## 删除子网

Delete

```http
http://<ip>:9696/v2.0/subnets/<被删除的子网ID>
```

## 修改子网

put

```http
http://<ip>:9696/v2.0/subnets/<被修改的子网ID>
```

```python
{
    "subnet":{
        <修改项>: <值>
    }
}
```

## 获取子网列表

get

```http
http://<ip>:9696/v2.0/subnets
```

## 创建路由

post

```python
{
    "router":{
        "name":<路由名>,
        "external_gateway_info":{	#指定外部网络信息,路由需要先连接到外部网络上,在将其他网络添加进来
            "network_id": <外部网络ID>      #外部网络
        }
    }
}
```

## 删除路由

delete

```http
http://<ip>:9696/v2.0/routers/<被删除的路由id>
```

## 修改路由

put

```http
http://<ip>:9696/v2.0/routers/<被修改的路由id>
```

```python
{
    "routers":{
        <修改项>: <值>
    }
}
```

## 连接/断开路由

put 连接网络

```http
http://<ip>:9696/v2.0/routers/<路由id>/add_router_interface
```

```python
{
	"subnet_id": <待连接的子网id>
}
```

put 断开网络

```http
http//<ip>:9696/v2.0/routers/<路由id>/remove_router_interface
```

```python
{
    "subnet_id": <待断开的子网id>
}
```

## 获取路由列表

get

```http
http://<ip>:9696/v2.0/routers
```



## python演示

### 创建私有网络

```python
import requests,json
# 获取Token
authUrl = "http://10.0.0.10:5000/v3/auth/token"
authBody = {
    "auth":{
        "identity":{
            "methods": ["password"],
            "password":{
                "user":{
                    "name":"admin",
                    "password": "000000",
                    "domain": {"name": "demo"}
                }
            }
        },
        "scope":{
            "project":{
                "name":"admin",
                "domain":{"name":"demo"}
            }
        }
    }
}
token = requests.post(authUrl,json.dumps(authBody)).headers["X-Subject-Token"]

netUrl = "http://10.0.0.10:9696/v2.0/networks"
netHeader = {
    "X-Auth-Token": token
}
netBody = {
    "network":{
        "name": "internal_net",
        "provider:network_type": "vxlan",
        "provider:segmentation_id": "100",
    }
}
requests.post(netUrl,json.dumps(netBody),headers=netHeader)
```

### 创建外部网络

```python
import requests,json
authUrl = "http://10.0.0.10:5000/v3/auth/tokens"
authBody = {
    "auth":{
        "identity":{
            "methods":["password"],
            "password":{
                "user":{
                    "name":"admin",
                    "password":"000000",
                    "domain":{"name":"demo"}
                }
            }
        },
        "scope":{
            "project":{
                "name":"admin",
                "domain":{"name","demo"}
            }
        }
    }
}
token = requests.post(url,json.dumps(authBody)).headers["X-Subject-Token"]

netUrl = "http://10.0.0.10:9696/v2.0/networks"
netHeader = {
    "X-Auth-Token":token
}
netBody = {
    "network":{
        "name":"external_net",
        "provider:network_type":"flat",
        "provider:physical_network":"provider"
    }
}
requests.post(authUrl,json.dumps(netBoyd),headers=netHeader)
```

### 创建子网

```python
import requests,json
authUrl = "http://10.0.0.10:5000/v3/auth/tokens"
authBody = {
    "auth":{
        "identity":{
            "methods":["password"],
            "password":{
                "user":{
                    "name":"admin",
                    "password":"000000",
                    "domain":{"name":"demo"}
                }
            }
        },
        "scope":{
            "project":{
                "name":"admin",
                "domain":{"name","demo"}
            }
        }
    }
}
token = requests.post(authUrl,json.dumps(authUrl)).headers["X-Subject-Token"]

subnetUrl = "http://10.0.0.10:9696/v2.0/subnets"
subnetHeader = {
    "X-Auth-Token":token
}
subnetBody = {
    "subnet":{
        "name":"internal_subnet",
        "network_id": "d32019d3-bc6e-4319-9c1d-6722fc136a22",
        "ip_version": 4,
        "cidr":"10.4.7.0/24",
        "gateway_ip":"10.4.7.1"
    }
}
requests.post(subnetUrl,json.dumps(subnetBody),headers=subnetHeader)
```

### 创建路由

```python
import requests,json
authUrl = "http://10.0.0.10:5000/v3/auth/tokens"
authBody = {
    "auth":{
        "identity":{
            "methods":["password"],
            "password":{
                "user":{
                    "name":"admin",
					"password":"000000",
                    "domain":{"name":"demo"}
                }
            }
        },
        "scope":{
            "project":{
                "name":"admin",
                "domain":{"name":"demo"}
            }
        }
    }
}
token = requests.post(authUrl,json.dumps(authBody)).headers["X-Subject-Token"]

routerUrl = "http://10.0.0.10:5000/v2.0/routers"
routerHeader = {
    "X-Auth-Token":token
}
routerBody = {
    "router":{
        "name":"router",
        "external_network_info":{
            "network_id":"04b1f8d9-bf7f-4f0d-bb98-6c467f395add"
        }
    }
}
requests.post(routerUrl,json.dumps(routerBody),headers=authHeader)
```

### 连接路由

```python
import requests,json
authUrl = "http://10.0.0.10:5000/v3/auth/tokens"
authBody = {
    "auth":{
        "identity":{
            "methods":["password"],
            "password":{
                "user":{
                    "name":"admin",
                    "password":"000000",
                    "domain":{"name":"demo"}
                }
            }
        },
        "scope":{
            "project":{
                "name":"admin",
                "domain":{"name":"demo"}
            }
        }
    }
}
token = requests.post(authUrl,json.dumps(authBody))

routerUrl = "http://10.0.0.10:9696/v2.0/routers/2a7c7f8c-e678-49ae-83d4-1124c264a1c5/add_router_interface"
routerHeader = {
    "X-Auth-Token"
}
routerBody = {
    "subnet_id":"f6f91747-f1d7-4b16-ae03-832d5101b392"
}
requests.post(routerUrl,json.dumps(routerBody),headers=routerHeader)
```

# Nova

## URL

云主机类型

```http
http://<ip>:8774/v2.1/flavors
```

云主机

```http
http://<ip>:8774/v2.1/server
```

## 创建类型

post

```python
{
    "flavor":{
        "name":<类型名称>,	#类型名称
        "id":<类型id>,	#类型id,可选,默认为自动生成
        "ram":<内存大小/mb>,	#类型的内存大小
		"disk":<磁盘/gb>,	#类型的磁盘大小
        "vcpus":<cpu数量>	#cpu的数量
    }
}
```

## 删除类型

delete

```http
http://<ip>:8774/v2.1/flavors/<被删除的类型ID>
```

## 修改类型

put

```http
http://<ip>:8774/v2.1/flavors/<被修改的类型ID>
```

## 列出类型列表

get

```http
http:/<ip>:8774/v2.1/flavors/
```

## 创建主机

post

```python
{
    "server":{
        "name":<云主机名>,	#云主机名
        "imageRef":<镜像ID>,	#使用的镜像ID
        "flavorRef":<类型ID>,	#使用的类型ID
        "networks":[	#使用的网络
           	{
                "uuid":<网络ID>	#网络id
            }
        ],
        "security_groups":[	#安全组,可选
            {
                "name":<安全组名称>	#安全组名
            }
        ]
    }
}
```

## 删除云主机

delete

```http
http://<ip>:8774/v2.1/server/<被删除的云主机id>
```

## 

