import requests,json

controller_ip = '192.168.1.107'

url = f"http://{controller_ip}:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}

headers = { "Content-Type" : "application/json" }

Token = requests.post(url,data=json.dumps(body),headers=headers).headers[ 'X-Subject-Token' ]

headers = { 'X-Auth-Token': Token }

class neutron_api:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def create_neutron(self,name):
  body = {
   "network": {
    "name": name,
    "tenant_id": "fd2a6ec468b340b286d477beae651c32"
}
}
  status_code = requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).status_code
  print(status_code)

 def get_id(self,name):
  result = json.loads(requests.get(self.resUrl,headers=self.headers).text)
  for item in result['networks']:
   if [ item['name'] == name ]:
    return item['id']

 def subnet_create(self,resUrl,name,id):
  body = {
   "subnet": {
    "name": name,
    "ip_version": 4,
    "cidr": "192.168.1.0/24",
    "network_id": id,
    "gateway_ip": "192.168.1.1"
}
}
  status_code = requests.post(resUrl,data=json.dumps(body),headers=self.headers).status_code

neutron_api=neutron_api(headers,f"http://192.168.1.107:9696/v2.0/networks")
neutron_api.create_neutron(name="pvm_int")
id = neutron_api.get_id(name="pvm_int")
status_code =requests.get("http://192.168.1.107:9696/v2.0/networks/"+id,headers=headers).text
neutron_api.subnet_create(resUrl=f"http://192.168.1.107:9696/v2.0/subnets",name="pvm_int",id=id)
print("内网创建成功")
print("内网名称为:"+"pvm_int"+id)
print(status_code)

