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
