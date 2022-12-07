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
    print(f"获取Token值失败，请检查访问云主机控制节点P是否正确？输出错误信息如下：{str(e)}")
    exit(0)

class glance_api:
    def __init__(self, headers: dict, resUrl: str):
        self.headers = headers
        self.resUrl = resUrl
    #创建glance镜像
    def create_glance(self, image_name: str, container_format="bare", disk_format="qcow2"):
        body = {
            "container_format": container_format,
            "disk_format": disk_format,
            "name": image_name,
        }
        status_code = requests.post(self.resUrl, data=json.dumps(body), headers=self.headers).status_code
    #获取glance镜像id
    def get_glance_id(self,image_name:str):
        result = json.loads(requests.get(self.resUrl,headers=self.headers).text)
        for item in result['images']:
            if(item['name']==image_name):
                return item['id']
    #上传glance镜像
    def update_glance(self,image_name:str,file_path=""):
        self.resUrl=self.resUrl+"/"+self.get_glance_id(image_name)+"/file"
        self.headers['Content-Type'] = "application/octet-stream"
        status_code = requests.put(self.resUrl,data=open(file_path,'rb').read(),headers=self.headers).status_code
glance_api = glance_api(headers,f"http://{controller_ip}:9292/v2/images")
glance_api.create_glance(image_name="cirros001")  #调用glance-api中创建镜像方法
print("镜像创建成功，id为: ",glance_api.get_glance_id(image_name="cirros001"))
glance_api.update_glance(image_name="cirros001",file_path="./cirros-0.3.4-x86_64-disk.img")
