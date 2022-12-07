import json,requests

url=f"http://192.168.1.214:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}
token = requests.post(url,data=json.dumps(body)).headers['X-Subject-Token']
headers={
'X-Auth-Token':token,
"Content-Type": "application/json"
}

class role_api:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def create_role(self,name):
  body = {
   "role": {
    "description": "my new role",
    "domain_id": "154d544429224953b8908224d737d352",
    "name": "admin"
}
}
  status_code = requests.post(self.resUrl,data=json.dumps(headers),headers=self.headers).text
  print(status_code)
role_api=role_api(headers,f"http://192.168.1.214:5000/v3/roles")
role_api.create_role(name="admin")
print("创建成功")
