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

 def create_heat(self,name):
  body = {
   "stack_name": "dad",
   "template": {
    "heat_template_version": "2016-10-14",
    "resources": {
     "pvm_heat": { 
      "type": "OS::Nova::Flavor",
      "properties": {
       "name": "pvm_heat",
       "ram": 1024,
       "disk": 20,
       "vcpus": 1,
}
 }
}

}
}
  status_code = requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).text
  print(status_code)

neutron_api=neutron_api(headers,f"http://192.168.1.107:8004/v1/fd2a6ec468b340b286d477beae651c32/stacks")
neutron_api.create_heat(name="test1")
print("创建成功")
