import requests,json,time

controller_ip='192.168.1.107'

url=f"http://{controller_ip}:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}

headers = {"Content-Type": "application/json"}

Token = requests.post(url,data=json.dumps(body),headers=headers).headers['X-Subject-Token']

headers={'X-Auth-Token' : Token}

class router_api:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def create_router(self,name,id):
  body = {
   "router": { 
    "admin_state_up": "true",
    "name": name,
    "external_gateway_info": {
      "network_id": "07106af5-8fc2-4dcf-919a-c19dbd19a6bb",
  }
 }
}
  status_code = requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).status_code
  print(status_code)

 def get_exid(self,resUrl,name):
  result = json.loads(requests.get(resUrl,headers=self.headers).text)
  for item in result['networks']:
   if(item['name']==name):
     return item['id']
 def router_interface(self,router_id,subnet_id):
  self.resUrl=self.resUrl+"/"+self.router_id(name="pvm_router")+"/add_router_interface"
  body = {
   "subnet_id": subnet_id
}
  status_code = requests.put(self.resUrl,data=json.dumps(body),headers=self.headers).status_code
  print(status_code)

 def router_id(self,name):
  result = json.loads(requests.get(self.resUrl,headers=self.headers).text)
  for item in result['routers']:
   if ( item['name']==name ):
    return item['id']
 def subnet_id(self,resUrl,name):
  result = json.loads(requests.get(resUrl,headers=self.headers).text)
  for item in result['subnets']:
   if ( item['name']==name ):
    return item['id']

router_api = router_api(headers,f"http://192.168.1.107:9696/v2.0/routers")
id = router_api.get_exid(f"http://192.168.1.107:9696/v2.0/networks",name="pvm_ex")
print(id)
router_api.create_router(name="pvm_router",id=id)
router_id = router_api.router_id(name="pvm_router")
subnet_id = router_api.subnet_id(name="pvm_int",resUrl=f"http://192.168.1.107:9696/v2.0/subnets")
router_api.router_interface(router_id=router_id,subnet_id=subnet_id)
status_code = requests.get(f"http://192.168.1.107:9696/v2.0/routers",headers=headers).text
print(status_code)
