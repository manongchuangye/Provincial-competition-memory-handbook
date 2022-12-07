import json,requests

controller_ip='172.129.1.10'

url = f"http://172.129.1.10:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}

Token = requests.post(url,data=json.dumps(body)).headers['X-Subject-Token']
headers = {
 'X-Auth-Token': Token,
 "Content-Type": "application/json"
}
class cinder_api:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def create_cinder(self,name):
  body = {
   "volume": {
    "size": 1,
    "name": name,
}
}
  status_code = requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).text
  print(status_code)
cinder_api=cinder_api(headers,f"http://172.129.1.10:8776/v3/944e124e5e554651ae2a2e9b41474ef9/volumes")
cinder_api.create_cinder(name="pvm_cinder")
status_code=requests.get(f"http://192.168.1.214:8776/v3/16b4119244d647539143f7a0c23c91dd/volumes/detail",headers=headers).text
print(status_code)
print("创建成功")