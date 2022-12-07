import requests,json

controller_ip = '192.168.1.107'

url = f"http://{controller_ip}:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}

headers = { "Content-Type" : "application/json" }

Token = requests.post(url,data=json.dumps(body),headers=headers).headers[ 'X-Subject-Token' ]

headers= { 'X-Auth-Token':Token }
print(headers)
class security_group:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def create_security(self,name):
  body = {
   "security_group": {
    "name": name,
    
   }
}
  status_code = requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).text
  print(status_code)
 def create_rules(self,id,resUrl):
  body = {
   "security_group_rule": {
    "direction": "ingress",
    "port_range_min": 20,
    "port_range_max": 3306,
    "ethertype": "IPv4",
    "protocol": "tcp",
    "security_group_id": id
}
}
  status_code= requests.post(resUrl,data=json.dumps(body),headers=self.headers).text
  print(status_code)
 def get_id(self,name):
  result = json.loads(requests.get(self.resUrl,headers=self.headers).text)
  for item in result['security_groups']:
   if (item['name']==name):
    return item['id']
    


security_group = security_group(headers,f"http://192.168.1.107:9696/v2.0/security-groups")
security_group.create_security(name="pvm_sec")
print("安全组创建成功id为:"+security_group.get_id(name="pvm_sec"))
id = security_group.get_id(name="pvm_sec")
security_group.create_rules(id,f"http://192.168.1.107:9696/v2.0/security-group-rules")
