import json,requests

url=f"http://192.168.1.214:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}
token = requests.post(url,data=json.dumps(body)).headers['X-Subject-Token']
print(token)
headers={'X-Auth-Token':token}

class group_api:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def create_group(self,name):
  body = {
   "group": {
    "description": "contract deveplopers",
    "domain_id": "154d544429224953b8908224d737d352",
    "name": name
}
}
  status_code = requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).text
  print(status_code)

group_api=group_api(headers,f"http://192.168.1.214:5000/v3/groups")
group_api.create_group(name="pvm_group")
print("创建成功")
