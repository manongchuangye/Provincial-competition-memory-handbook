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
   if [ item['name'] == flavor_name ]:
    return item['id']
flavor_api=flavor_api(headers,f"http://192.168.1.107:8774/v2.1/flavors")
flavor_api.create_flavor(flavor_name="pvm_flavor")
flavor_api.get_id(flavor_name="pvm_flavor")
name = "pvm_flavor"
print("云主机类型创建成功ID为"+flavor_api.get_id(flavor_name="pvm_flavor"))
status_code = requests.get(f"http://192.168.1.107:8774/v2.1/flavors/12345",data=json.dumps(body),headers=headers).text
print(status_code)
