import requests,json,time

# *******************全局变量IP*****************************
#执行代码前，请修改controller_ip的IP地址，与指定router
print("\n==============================基础环境配置==============================\n")
controller_ip=input("请输入访问openstack平台控制节点IP地址：（xx.xx.xx.xx)\n")

try:
    url  = f"http://{controller_ip}:5000/v3/auth/tokens"
    body = {"auth": {"identity": {"methods": ["password"], "password": {
                "user": {"domain": {"name": "default"}, "name": "admin", "password": "000000"}}},
                   "scope": {"project": {"domain": {"name": "default"}, "name": "admin"}}}}
    headers = {
                    "Content-Type": "application/json",
                }
    Token = requests.post(url, data=json.dumps(body), headers=headers).headers['X-Subject-Token']
    headers = {
                    "X-Auth-Token": Token
                }
except Exception as e:
    print(f"获取Token值失败，请检查访问云主机控制节点IP是否正确？输出错误信息如下：{str(e)}")
    exit(0)



class flavor_api:
    def __init__(self,handers:dict,resUrl:str):
        self.headers=handers
        self.resUrl=resUrl

    #创建flavor类型
    def create_flavor(self,flavor_name:str,ram,vcpus,disk,id):
        self.headers['Content-Type']="application/json"
        body={
            "flavor":{
                "name":flavor_name,
                "ram":ram,
                 "vcpus":vcpus,
                "disk":disk,
                "id":id,
            }
        }
        status_code = requests.post(self.resUrl, data=json.dumps(body), headers=self.headers).text
    #获取flavor_id
    def get_flavor_id(self,flavor_name:str):
        result = json.loads(requests.get(self.resUrl,headers=self.headers).text)
        for item in result['flavors']:
            if(item['name']==flavor_name):
                return item['id']
flavor_api=flavor_api(headers,f"http://{controller_ip}:8774/v2.1/flavors")

flavor_api.create_flavor(flavor_name="test",ram=1024,vcpus=1,disk=20,id=199999)
flavor_id = flavor_api.get_flavor_id(flavor_name="test")
print("云主机类型创建成功，flavor_id为:",flavor_id)

'''
#注意调用方法应该放在最前面！！！
'''