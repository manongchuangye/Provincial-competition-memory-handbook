import json,requests,time
url = f"http://192.168.1.214:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}


header={"Content-Type":"application/json"}
token = requests.post(url,data=json.dumps(body),headers=header).headers['X-Subject-Token']
headers={
 'X-Auth-Token': token,
 "Content-Type":"application/json"
}

class zun_api:
 def __init__(self,headers,resUrl):
  self.headers=headers
  self.resUrl=resUrl
 def create_zun(self,name):
  body = {
   "name": name,
   "image": "centos7:1804",
   "image_driver": "docker",
   "image_pull_policy": "ifnotpresent"
}
  status_code = requests.post(self.resUrl,data=json.dumps(body),headers=headers).text
  print(status_code)
 def get_id(self,name):
  result=json.loads(requests.get(self.resUrl,headers=self.headers).text)
  for item in result['containers']:
   if (item['name']==name):
    return item ['uuid']
 def start_zun(self,id):
  status_code = requests.post(f"http://192.168.1.214:9517/v1/containers/"+id+"/start",headers=self.headers).text
  print(status_code)
zun_api=zun_api(headers=headers,resUrl=f"http://192.168.1.214:9517/v1/containers")
zun_api.create_zun(name="zun-container")
time.sleep(6)
id=zun_api.get_id(name="zun-container")
zun_api.start_zun(id=id)
print("创建成功")