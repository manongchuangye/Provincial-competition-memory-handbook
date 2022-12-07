import json,requests

url = f"http://192.168.1.214:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}

token=requests.post(url,data=json.dumps(body)).headers['X-Subject-Token']
print(token)
headers={
 'X-Auth-Token': token,
 "Content-Type": "application/json"
}
class cinder_api:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def mount_cinder(self,name):
  body = {
   "os-attach": {
    "instance_uuid": "86f36dc1-94d9-4fff-8693-c1e120e1e2f3",
    "mountpoint": "/dev/vdb"
}
}
  status_code = requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).text
  print(status_code)

cinder_api=cinder_api(headers,f"http://192.168.1.214:8776/v3/16b4119244d647539143f7a0c23c91dd/volumes/7e1a677e-cc70-4824-ad7e-3a81be1a5075/action")
cinder_api.mount_cinder(name="123")
print("创建成功")
