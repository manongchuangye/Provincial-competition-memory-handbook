#### 创建云主机类型

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





```

```

```

```



```

```







```python
# Copyright 2021~2022 The Cloud Computing support Teams of ChinaSkills.  
import requests,json,time  
import logging  
#-----------logger-----------  
#get logger  用logging.getLogger(name)方法进行模块初始化
logger = logging.getLogger(__name__)  
# level     #设置日志等级    DEBUG全部输出
logger.setLevel(logging.DEBUG)  
# format  设置日志输出格式
format = logging.Formatter('%(asctime)s %(message)s')  
# to console  使用Handler可以向类似与
stream_handler = logging.StreamHandler()  
#使用这个Handler可以向类似与sys.stdout或者sys.stderr的任何文件对象(file object)输出信息
stream_handler .setFormatter(format)  
#setFormatter()方法输出具有格式化
logger.addHandler(stream_handler )  
#addHandler() 方法添加多个handler
#-----------logger-----------  
def get_auth_token(controller_ip, domain, user, password):  
    
   '''  
  :param controller_ip: openstack master ip address  
  :param domain: current user's domain  
  :param user: user name  
  :param password: user password  
  :return: keystoen auth Token for current user.  
  '''

   try:  
       url = f"http://{controller_ip}:5000/v3/auth/tokens"  
    #登录模块
       body = {  
                   "auth": {  
                       "identity": {  
                           "methods": [  
                               "password"  
                          ],  
                           "password": {  
                               "user": {  
                                   "domain": {  
                                       "name": domain  
                                  },  
                                   "name": user,  
                                   "password": password  
                              }  
                          }  
                      },  
                       "scope": {  
                           "project": {  
                               "domain": {  
                                   "name": domain  
                              },  
                               "name": user  
                          }  
                      }  
                  }  
              }  
       #模拟浏览器表头
       headers = {  
           "Content-Type": "application/json",  
      }  
       print(body)  
       Token = requests.post(url, data=json.dumps(body), headers=headers).headers['X-Subject-Token']  
       headers = {  
           "X-Auth-Token": Token  
      }  
       logger.debug(f"获取Token值：{str(Token)}")  
       return headers  
   except Exception as e:  
       logger.error(f"获取Token值失败，请检查访问云主机控制节点IP是否正确？输出错误信息如下：{str(e)}")  
       exit(0)  
#用户管理  
# https://docs.openstack.org/api-ref/identity/v3/index.html#users  
class user_manager:  
   def __init__(self, handers: dict, resUrl: str):  
       self.headers = handers  
       self.resUrl = resUrl  
   #     POST /v3/users Create user  
   def create_users(self, user_name, password:str, desc:str): 
        
       """  
      create a user with name and password and description.  
      :param user_name:  
      :param password:  
      :param desc:  
      :return:  
      """  
    
       body = {  
           "user": {  
               "name": user_name,  
               "password": password,  
               "description": desc,  
          }  
      }  
       status_code = requests.post(self.resUrl, data=json.dumps(body), headers=self.headers).text  
       logger.debug(f"返回状态:{str(status_code)}")  
       return status_code  
   # /v3/users   # List all users  
   def get_users(self):  
    
       """  
      :return:  
      """  
        
       status_code =  requests.get(self.resUrl, headers=self.headers).text  
       logger.debug(f"返回状态:{str(status_code)}")  
       return status_code  
   def get_user_id(self, user_name):  
        
       """  
      get user id by name.  
      :param user_name:  
      :return:  
      """  
    
       result = json.loads(requests.get(self.resUrl, headers=self.headers).text)  
       user_name = user_name  
       for item in result['users']:  
           if item['name'] == user_name:  
               return item['id']  
       return "NONE"  
   def get_user(self, id:str):  
        
       """  
      get a flavor by id.  
      :return:  
      """  
    
       api_url = self.resUrl + "/"+id  
       result = json.loads(requests.get(api_url, headers=self.headers).text)  
       logger.debug(f"返回信息:{str(result)}")  
       return result  
   def delete_user(self, id:str):  
        
       """  
        delete a user by id.  
        :return:  
        """  
    
       api_url = self.resUrl + "/" + id  
       response = requests.delete(api_url, headers=self.headers)  
       # 204 - No ContentThe server has fulfilled the request.  
       if response.status_code == 204:  
           return {"User itemDeletedSuccess": response.status_code}  
       result = json.loads(response.text)  
       logger.debug(f"返回信息:{str(result)}")  
       return result  
       # http://192.168.200.226:8774/v2.1/ get apis version infomation.  
   def update_User_password(self, id: str, original_password: str, new_password : str):  
    
       """  
      update a flavor desc by id.  
      :return:  
      """  
        
       self.headers['Content-Type'] = "application/json"  
       body = {  
           "user": {  
               "password": new_password,  
               "original_password": original_password  
          }  
      }  
       api_url = self.resUrl + "/" + id + "/password"  
       response = requests.post(api_url, data=json.dumps(body), headers=self.headers)  
       # Normal response codes: 204 without return text  
       if response.status_code == 204 :  
           return {"item Update Password Success": response.status_code}  
       result = json.loads(response.text)  
       logger.debug(f"返回信息:{str(result)}")  
       return result  
    
#传参
if __name__ == '__main__':  
   # 1. openstack allinone （controller ) credentials  
   # host ip address  
   controller_ip = "192.168.200.226"  
   # domain name  
   domain = "demo"  
   # user name  
   user = "admin"  
   # user password  
   password = "000000"  
   headers = get_auth_token(controller_ip,domain,user,password)  
   print("headers:", headers)  
   #get all user  
   user_m = user_manager(headers, f"http://{controller_ip}:5000/v3/users")  







#验证代码

   # 1 查询所有  
   users = user_m.get_users()  
   print("查询所有users:", users)  
    
   # 2 创建  
   user = user_m.create_users("user_demo", "passw0rd","A user created by python code.")  
   print("创建用户:", user)  
   # get user id by name  
   id = user_m.get_user_id("user_demo")  
   print("User user_demo Id is:", id)  
    
   #3. 使用ID查询  
   user = user_m.get_user(id)  
   print(f"查询{id}用户:", user)  

   # 4. 更新密码  
   result = user_m.update_User_password(id, "passw0rd", "8assw52d")  
   print(f"更新密码{id}用户:", result)  
    
   #5. 删除新建用户  
   result = user_m.delete_user(id)  
   print(f"删除{id}用户:", result)  
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
    "password": "000000",
    
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
name = "pvm_flavor"
#这里是什么意思


print("云主机类型创建成功ID为"+flavor_api.get_id(flavor_name="pvm_flavor"))
status_code = requests.get(f"http://192.168.1.107:8774/v2.1/flavors/12345",data=json.dumps(body),headers=headers).text

print(status_code)
```







#### SDK

```python
import json,requests
auth_url=f"http://{controller_ip}:5000/v3/auth/tokens"
body={
    "auth":{
        "identity":{
            
        }
    }
}
    
    
    
if __name__ == '__main__':  
   # Initialize connection(通过配置文件）  
  auth_url = "http://172.128.11.18:5000/v3/"  
  username = "admin"  
  password = "000000"  
  user_domain_name = 'demo' 
```

```

```

```

```

