### 查看APIs的网站与端口

```
 openstack endpoint list -c "Service Name"  -c "Enabled"  -c "URL"  
```



### list_roles

```python
import requests,json
controller_ip="10.26.28.100"
url=f"http://{controller_ip}:5000/v3/auth/tokens"
body={
  "auth":{
    "identity":{
      "methods":["password"],
      "password":{
        "user":{
          "domain":{"name":"demo"},
          "password":"000000",
          "name":"admin"
}
}
},
    "scope":{
      "project":{
        "domain":{"name":"demo"},
        "name":"admin"
}
}
}
}
headers={
"Content-Type":"application/json"
}
Token=requests.post(url=url,headers=headers,data=json.dumps(body)).headers["X-Subject-Token"]
headers={
"X-Auth-Token":Token
}
role_url=f"http://{controller_ip}:5000/v3/roles"
def list_role():
 status = requests.get(url=role_url,headers=headers,data=json.dumps(body)).text
 return status
print(list_role())
```

#### create_flavor

```python
import requests,json

auth_url = f"http://10.26.28.75:5000/v3/auth/tokens"
body = {
                    "auth": {
                        "identity": {
                            "methods": [
                                "password"
                            ],
                            "password": {
                                "user": {
                                    "domain": {
                                        "name": "demo"
                                    },
                                    "name": "admin",
                                    "password": "000000"
                                }
                            }
                        },
                        "scope": {
                            "project": {
                                "domain": {
                                    "name": "demo"
                                },
                                "name": "admin"
                            }
                        }
                    }
                }
Token = requests.post(url=auth_url, data=json.dumps(body)).headers['X-Subject-Token']
print(Token)
headers = {
         "X-Auth-Token":Token,
         "Content-Type":"application/json"
       }
nova_url="http://10.26.28.75:8774/v2.1/flavors"
def create_flavor(name,id,ram,vcpus,disk):
  body={
    "flavor":{
        "name":name,
        "id":id,
        "ram":ram,
        "disk":disk,
        "vcpus":vcpus
    }
  }
  status=requests.post(url=nova_url,headers=headers,data=json.dumps(body)).status_code
  return status
print(create_flavor(name="api_flavor",ram=2,disk=10,vcpus=1,id="1234"))
```

#### delete_flavor

```

```









```python
import requests,json,time

controller_ip='192.168.1.107'

url=f"http://{controller_ip}:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}

headers = {"Content-Type": "application/json"}

Token = requests.post(url,data=json.dumps(body),headers=headers).headers['X-Subject-Token']

headers={'X-Auth-Token' : Token}

class flavor_api:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def create_flavor(self,flavor_name):
  body = {
   "flavor": {
    "name": flavor_name,
    "ram": 2048,
    "disk": 20,
    "id": 12345,
    "vcpus": 2
}
}
  status_code=requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).status_code
 def get_id(self,flavor_name):
  result = json.loads(requests.get(self.resUrl,headers=self.headers).text)
  for item in result['flavors']:
   if [ item['name'] == flavor_name]:
    return item['id']
flavor_api=flavor_api(headers,f"http://192.168.1.107:8774/v2.1/flavors")
flavor_api.create_flavor(flavor_name="pvm_flavor")
flavor_api.get_id(flavor_name="pvm_flavor")
name = "pvm_flavor"
print("云主机类型创建成功ID为"+flavor_api.get_id(flavor_name="pvm_flavor"))
status_code=requests.get(f"http://192.168.1.107:8774/v2.1/flavors/12345",data=json.dumps(body),headers=headers).text
print(status_code)

```

#### 创建用户

```python
openstack token issue

import requests,json
Token ="gAAAAABjZi6o5xYvzBlxjHBCBOZinXgBLTDjpQPh2RxzXxnh8-4ssqs07Io5j1NpXjIZNQ8e3g16emrVUIzQ7eD_3yzraOLKSEbPnkLGABsIOqIXOdMw-1rituAuJa3yZUwm0V-VOPlMn0ouXL8Kp9AkiCZbVGc6ibS_A1VIEQRkTnzEn4QMK3g"

headers = {
         "X-Auth-Token":Token,
         "Content-Type":"application/json"
       }
print(headers)
user_url=f"http://controller:5000/v3/users"
def create_user(name,password):
    body = { 
        "user": {    #注意这里是user
            "name": name,
            "password": password,
        }
    }
    status=requests.post(url=user_url,headers=headers,data=json.dumps(body)).text
    return status


print(create_user(name="jjj",password="123123"))
```

#### 创建云主机

```python
import requests,json

Token =

headers = {
    "X-Auth-Token":Token,
    "Content-Type":"application/json"
}
server_url = "http://controller:8774/v2.1/servers"
def create_server():
    body = {
        "server": {
            "name": "auto-allocate-network",
            "imageRef": image,
            "flavorRef": "12345",
            "networks": [{
              'uuid': "761c9d2b-da8b-4bbe-8339-a6a1b785794d"
      }],
    }
}
    status_code = requests.post(url=server_url,data=json.dumps(body),headers=headers).text
    return  status_code
print(create_server(image=""))
```



#### create_user

```python
import json,requests

url=f"http://192.168.1.214:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}
token = requests.post(url,data=json.dumps(body)).headers['X-Subject-Token']

headers={
'X-Auth-Token':token,
"Content-Type": "application/json"
}

class user_api:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def create_user(self,name):
  body = {
   "user": {
    "name": name,
    "domain_id": "154d544429224953b8908224d737d352",
    "password": "000000"
}
}
  status_code = requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).text
  print(status_code)

user_api=user_api(headers,f"http://192.168.1.214:5000/v3/users")
user_api.create_user(name="admin")
print("创建成功")
```

#### create_VM

```python
import requests,json,time

controller_ip='192.168.1.107'

url=f"http://{controller_ip}:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}

headers = {"Content-Type":"application/json"}

Token = requests.post(url,data=json.dumps(body),headers=headers).headers['X-Subject-Token']

headers={'X-Auth-Token':Token}
print(headers)
class server_api:
 def __init__(self,resUrl,headers):
  self.headers=headers
  self.resUrl=resUrl
 def create_server(self,image):
  body = {
    "server": {
        "name": "auto-allocate-network",
        "imageRef": image,
        "flavorRef": "12345",
        "networks": [{
          'uuid': "761c9d2b-da8b-4bbe-8339-a6a1b785794d"
      }],
        "security_group": "id"
    }
}
  status_code = requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).text
  print(status_code)

server_api=server_api(f"http://192.168.1.107:8774/v2.1/servers",headers)
server_api.create_server(image="8b25e8d3-754e-4cd2-9cd0-448fa30e873e")
print("云主机创建成功")
```







#### create_flavor

```python
import requests,json,time

controller_ip='192.168.1.107'

url=f"http://{controller_ip}:5000/v3/auth/tokens"

#这是干啥的


body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}

headers = {"Content-Type": "application/json"}

#表头格式


Token = requests.post(url,data=json.dumps(body),headers=headers).headers['X-Subject-Token']

#这里看不懂

headers={'X-Auth-Token' : Token}

class flavor_api:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def create_flavor(self,flavor_name):
  body = {
   "flavor": {
    "name": flavor_name,
    "ram": 2048,
    "disk": 20,
    "id": 12345,
    "vcpus": 2
}
}
  status_code=requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).status_code
    #这是什么意思
    
    
 def get_id(self,flavor_name):
  result = json.loads(requests.get(self.resUrl,headers=self.headers).text)
  for item in result['flavors']:
   if [ item['name'] == flavor_name ]:
    return item['id']
#循环遍历加条件语句


flavor_api=flavor_api(headers,f"http://192.168.1.107:8774/v2.1/flavors")
flavor_api.create_flavor(flavor_name="pvm_flavor")
flavor_api.get_id(flavor_name="pvm_flavor")

print("云主机类型创建成功ID为"+flavor_api.get_id(flavor_name="pvm_flavor"))
status_code = requests.get(f"http://192.168.1.107:8774/v2.1/flavors/12345",data=json.dumps(body),headers=headers).text

print(status_code)
```

【实操题】OpenStack Python运维脚本开发：使用Restful API方式创建用户 （3分）

```
在提供的OpenStack私有云平台上，使用T版本的“openstack- python-dev ”镜像创建1台云主机，云主机类型使用4vCPU/12G内存/100G硬盘。该主机中已经默认安装了所需的开发环境，登录默认账号密码为“root/Abc@1234”。使用python request库和OpenStack Restful APIs，在/root目录下，创建api_manager_identity.py文件，编写python代码，代码实现以下任务：
（1）首先实现查询用户，如果用户名称“user_demo”已经存在，先删除。
（2）如果不存在“user_demo”，创建该用户，密码设置为“1DY@2022”。
（3）创建完成后，查询该用户信息，查询的body部分内容控制台输出，同时json格式的输出到文件当前目录下的user_demo.json文件中，json格式要求indent=4。
编写完成后，提交allinone节点的用户名、密码（默认Abc@1234）和IP地址到答题框。


import json, requests, logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
format = logging.Formatter('%(asctime)s %(message)s')
stream_headler = logging.StreamHandler()
stream_headler.setFormatter(format)
logger.addHandler(stream_headler)


def get_token(controller_ip, domain, user, password):
    try:
        url = f"http://{controller_ip}:5000/v3/auth/tokens"
        body = {"auth": {"identity": {"methods": ["password"], "password": {
            "user": {"domain": {"name": domain}, "name": user, "password": password}}},
                         "scope": {"project": {"domain": {"name": domain}, "name": user, "password": password}}}}
        headers = {
            "Content-Type": "application/json"
        }
        Token = requests.post(url, data=json.dumps(body), headers=headers).headers['X-Subject-Token']
        headers = {
            "X-Auth-Token": Token
        }
        logger.debug(f"获取token为: {str(Token)}")
        return headers
    except Exception as e:
        logger.error(f"token错误: {str(e)}")
        exit(0)


class user_manager:
    def __init__(self, handers: dict, resUrl: str):
        self.headers = handers
        self.resUrl = resUrl

    def get_user_id(self, user_name):
        result = json.loads(requests.get(self.resUrl, headers=self.headers).text)
        user_name = user_name
        for item in result['users']:
            if item['name'] == user_name:
                return item['id']
        return "NONE"

    def delete_user(self, id: str):
        api_url = self.resUrl + "/" + id
        response = requests.delete(api_url, headers=self.headers)
        if response.status_code == 204:
            return {"User itemDeletedSuccess": response.status_code}
        result = json.loads(response.text)
        logger.debug(f"返回信息:{str(result)}")
        return result

    def create_users(self, user_name, password: str):
        body = {
            "user": {
                "name": user_name,
                "password": password,
            }
        }
        status_code = requests.post(self.resUrl, data=json.dumps(body), headers=self.headers).text
        logger.debug(f"返回状态:{str(status_code)}")
        return status_code


if __name__ == '__main__':
    controller_ip = "192.168.100.10"
    domain = "demo"
    user = "admin"
    password = "000000"
    headers = get_token(controller_ip, domain, user, password)

    print("headers:", headers)
    user_m = user_manager(headers, f"http://{controller_ip}:5000/v3/users")
    user = user_m.get_user_id("user_demo")
    print(f"查询{id}用户:", user)

    id = user_m.get_user_id("user_demo")
    result = user_m.delete_user(id)
    print(f"删除{id}用户:", result)

    user = user_m.create_users("user_demo", "1DY@2022")
    print("创建用户:", user)
```

