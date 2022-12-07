
import requests,json

controller_ip = '192.168.1.107'

url = f"http://{controller_ip}:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}

headers = { "Content-Type" : "application/json" }

Token = requests.post(url,data=json.dumps(body),headers=headers).headers[ 'X-Subject-Token' ]

headers = { 'X-Auth-Token': Token }

class manila_api:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def create_manila(self,name):
  body = {
   "share_network": {
    "neutron_net_id": "07106af5-8fc2-4dcf-919a-c19dbd19a6bb",
    "neutron_subnet_id": "e5d7f575-837f-4d63-9250-804a4faf64f7",
    "name": name
}
 }
  status_code=requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).text
  print(status_code)
 def get_id(self,name):
  result = requests.get(self.resUrl,headers=self.headers).text
  print(result)
  for item in result['share_networks']:
   if (item['name']==name):
    return itm['id']

manila_api=manila_api(headers,f"http://192.168.1.107:8786/share-networks")
manila_api.create_manila(name="my")
#id=manila_api.get_id(name="my")
status_code=requests.get(f"http://192.168.1.107:8786/v2/share-networks/",headers=headers).text
print(status_code)
