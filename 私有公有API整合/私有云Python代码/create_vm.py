import requests,json,time

controller_ip='192.168.1.107'

url=f"http://{controller_ip}:5000/v3/auth/tokens"

body = {"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name":"demo"},"name":"admin","password":"000000"}}},
        "scope":{"project":{"domain":{"name":"demo"},"name":"admin"}}}}

headers = {"Content-Type":"application/json"}

Token = requests.post(url,data=json.dumps(body),headers=headers).headers['X-Subject-Token']

headers={'X-Auth-Token':Token}
print(headers)
class server_api:
 def __init__(self,resUrl,headers):
  self.headers=headers
  self.resUrl=resUrl
 def create_server(self,image):
  body = {
    "server": {
        "name": "auto-allocate-network",
        "imageRef": image,
        "flavorRef": "12345",
        "networks": [{
          'uuid': "761c9d2b-da8b-4bbe-8339-a6a1b785794d"
      }],
        "security_group": "id"
    }
}
  status_code = requests.post(self.resUrl,data=json.dumps(body),headers=self.headers).text
  print(status_code)

server_api=server_api(f"http://192.168.1.107:8774/v2.1/servers",headers)
server_api.create_server(image="8b25e8d3-754e-4cd2-9cd0-448fa30e873e")
print("云主机创建成功")
