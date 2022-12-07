import json,requests
url = f"http://192.168.1.214:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}


header={"Content-Type":"application/json"}
token = requests.post(url,data=json.dumps(body),headers=header).headers['X-Subject-Token']
headers={
 'X-Auth-Token': token,
 'Content-Type':'application/json'
}

class domain_api:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def create_domain(self,name):
  body = {
   "domain": {
    "name": "mydomain"
}
}
  status_code=requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).text
  print(status_code)

domain_api=domain_api(headers,f"http://192.168.1.214:5000/v3/domains")
domain_api.create_domain(name="123")
print("创建成功")
