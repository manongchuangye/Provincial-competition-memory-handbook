创建pod

```python
import requests,json,yaml
def get_api_server_token(api_server_token, node_url):
    #for request header
    bearer_token = "bearer " + api_server_token
    return bearer_token

class pod_manager():
    def __init__(self, node_url: str, bearer_token: str):
        self.node_url = node_url
        self.bearer_token = bearer_token
    # 创建pod
    def create_pod(self, yamlFile:str,namespace:str):
        headers = {
            "Authorization": self.bearer_token,
            "Content-Type": "application/json"
        }
        # 读取yaml文件，并转化为JSON数据
        with open(yamlFile, encoding="utf8") as f:
            body = json.dumps(yaml.safe_load(f))
        request_url = self.node_url + "/api/v1/namespaces/" + namespace +"/pods"
        result = json.loads(requests.post(request_url, data=body, headers=headers, verify=False).text)
        return result
if __name__ == "__main__":
    # 将获取到的token值放到api_server_token中去
    api_server_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1icXhrdm1xZjJ3ajlzM0tiRnVOVGZ3QkdsSGc4Yk9PdXFKVHhrZUdFLU0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbjEtdG9rZW4tZnY2bnAiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiYWRtaW4xIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiODAzYmNjYmItM2VkMi00ZDM3LWEzNTEtNDExM2I5NDkxY2Q1Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmFkbWluMSJ9.1K3xUaC9KeK1_x8ZGyOPmxWaM1zEgrxtcCiJ3U3wqa0z1rdwMo-UoCir37XKkdPa56BahbxNzj5XMcJgo94ItNWy4UgrrlRoN-lcY7ReYVm3qakUlKoXNrJHpMoFiXLbTxstF1W-zHvYAF-rfA7mcI_JVSOVaLuU3uyIolHwS8LAdejpithBfv98wCkQ9bvqqmWZ282Cz1G3daDnystn-pNPAtvhKe29-K3v3CDvn4ahuSMMpUKLCuPThR80aMhmJEDvreDBH9AX25RVADGcZos44V2MH53DbXdPQAacoGDLF1ckF6wDLZbQedrIJDYJ8frhS4iSCnt6ClofYF2ZOw"
    # 节点URL地址 10.10.16.10
    cluster_server_url = "https://10.10.16.10:6443"
    bearer_token = get_api_server_token(api_server_token, cluster_server_url)
    pod_m = pod_manager(cluster_server_url, bearer_token)
    # #创建Pod
    print("--------create pod with a yaml file ------------")
    result = pod_m.create_pod(yamlFile="nginx-pod.yaml",namespace="kube-system")
    print(result)
```

查询pod（不可用）

```python
import requests,json,yaml
import logging
logger = logging.getLogger(__name__)

def get_api_server_token(api_server_token, node_url):
    #for request header
    bearer_token = "bearer " + api_server_token
    return bearer_token

class pod_manager():
    def __init__(self, node_url: str, bearer_token: str):
        self.node_url = node_url
        self.bearer_token = bearer_token
    # 查询创建的pod
    def get_pod(self, pod_name: str):
        headers = {
            "Authorization": self.bearer_token
        }
        request_url = self.node_url + "/api/v1/namespaces/default/pods/" + pod_name
        result = json.loads(requests.get(request_url, headers=headers, verify=False).text)
        logger.debug(f"返回信息:{str(result)}")
        return result


if __name__ == "__main__":
    # 将获取到的token值放到api_server_token中去
    api_server_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1icXhrdm1xZjJ3ajlzM0tiRnVOVGZ3QkdsSGc4Yk9PdXFKVHhrZUdFLU0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbjEtdG9rZW4tZnY2bnAiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiYWRtaW4xIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiODAzYmNjYmItM2VkMi00ZDM3LWEzNTEtNDExM2I5NDkxY2Q1Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmFkbWluMSJ9.1K3xUaC9KeK1_x8ZGyOPmxWaM1zEgrxtcCiJ3U3wqa0z1rdwMo-UoCir37XKkdPa56BahbxNzj5XMcJgo94ItNWy4UgrrlRoN-lcY7ReYVm3qakUlKoXNrJHpMoFiXLbTxstF1W-zHvYAF-rfA7mcI_JVSOVaLuU3uyIolHwS8LAdejpithBfv98wCkQ9bvqqmWZ282Cz1G3daDnystn-pNPAtvhKe29-K3v3CDvn4ahuSMMpUKLCuPThR80aMhmJEDvreDBH9AX25RVADGcZos44V2MH53DbXdPQAacoGDLF1ckF6wDLZbQedrIJDYJ8frhS4iSCnt6ClofYF2ZOw"
    # 节点URL地址 192.168.138.201
    cluster_server_url = "https://10.10.16.10:6443"
    bearer_token = get_api_server_token(api_server_token, cluster_server_url)
    pod_m = pod_manager(cluster_server_url, bearer_token)
    #查找Pod
    print("--------get pod with name ------------")
    result = pod_m.get_pod(pod_name="nginx")
    print(result)
```

更新（不可用）

```python
import requests,json,yaml

def get_api_server_token(api_server_token, node_url):
    #for request header
    bearer_token = "bearer " + api_server_token
    return bearer_token

class pod_manager():
    def __init__(self, node_url: str, bearer_token: str):
        self.node_url = node_url
        self.bearer_token = bearer_token
    def update_pod(self, yamlFile:str, pod_name:str,namespace:str):
        headers = {
            "Authorization": self.bearer_token,
            "Content-Type": "application/strategic-merge-patch+json"
        }
        # 读取yaml文件，并转化为JSON数据
        with open(yamlFile, encoding="utf8") as f:
            body = json.dumps(yaml.safe_load(f))

        request_url = self.node_url + "/api/v1/namespaces/" + namespace + "/pods"+ pod_name
        result = json.loads(requests.patch(request_url, data=json.dumps(body), headers=headers, verify=False).text)
        logger.debug(f"返回信息:{str(result)}")
        return result


if __name__ == "__main__":
    # 将获取到的token值放到api_server_token中去
    api_server_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1icXhrdm1xZjJ3ajlzM0tiRnVOVGZ3QkdsSGc4Yk9PdXFKVHhrZUdFLU0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbjEtdG9rZW4tZnY2bnAiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiYWRtaW4xIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiODAzYmNjYmItM2VkMi00ZDM3LWEzNTEtNDExM2I5NDkxY2Q1Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmFkbWluMSJ9.1K3xUaC9KeK1_x8ZGyOPmxWaM1zEgrxtcCiJ3U3wqa0z1rdwMo-UoCir37XKkdPa56BahbxNzj5XMcJgo94ItNWy4UgrrlRoN-lcY7ReYVm3qakUlKoXNrJHpMoFiXLbTxstF1W-zHvYAF-rfA7mcI_JVSOVaLuU3uyIolHwS8LAdejpithBfv98wCkQ9bvqqmWZ282Cz1G3daDnystn-pNPAtvhKe29-K3v3CDvn4ahuSMMpUKLCuPThR80aMhmJEDvreDBH9AX25RVADGcZos44V2MH53DbXdPQAacoGDLF1ckF6wDLZbQedrIJDYJ8frhS4iSCnt6ClofYF2ZOw"
    # 节点URL地址 192.168.138.201
    cluster_server_url = "https://10.10.16.10:6443"
    bearer_token = get_api_server_token(api_server_token, cluster_server_url)
    pod_m = pod_manager(cluster_server_url, bearer_token)
    #查找Pod
    print("--------get pod with name ------------")
    pod_m.get_pod(pod_name="nginx")
```

删除pod

```python
import requests,json,yaml

def get_api_server_token(api_server_token, node_url):
    #for request header
    bearer_token = "bearer " + api_server_token
    return bearer_token

class pod_manager():
    def __init__(self, node_url: str, bearer_token: str):
        self.node_url = node_url
        self.bearer_token = bearer_token
    #删除pod
    def delete_pod(self,pod_name: str):
        headers = {
            "Authorization": self.bearer_token
        }
        request_url = self.node_url + "/api/v1/namespaces/default/pods/" + pod_name
        result = json.loads(requests.delete(request_url, headers=headers, verify=False).text)
        return result

if __name__ == "__main__":
    # 将获取到的token值放到api_server_token中去
    api_server_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1icXhrdm1xZjJ3ajlzM0tiRnVOVGZ3QkdsSGc4Yk9PdXFKVHhrZUdFLU0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbjEtdG9rZW4tZnY2bnAiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiYWRtaW4xIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiODAzYmNjYmItM2VkMi00ZDM3LWEzNTEtNDExM2I5NDkxY2Q1Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmFkbWluMSJ9.1K3xUaC9KeK1_x8ZGyOPmxWaM1zEgrxtcCiJ3U3wqa0z1rdwMo-UoCir37XKkdPa56BahbxNzj5XMcJgo94ItNWy4UgrrlRoN-lcY7ReYVm3qakUlKoXNrJHpMoFiXLbTxstF1W-zHvYAF-rfA7mcI_JVSOVaLuU3uyIolHwS8LAdejpithBfv98wCkQ9bvqqmWZ282Cz1G3daDnystn-pNPAtvhKe29-K3v3CDvn4ahuSMMpUKLCuPThR80aMhmJEDvreDBH9AX25RVADGcZos44V2MH53DbXdPQAacoGDLF1ckF6wDLZbQedrIJDYJ8frhS4iSCnt6ClofYF2ZOw"
    # 节点URL地址 192.168.138.201
    cluster_server_url = "https://10.10.16.10:6443"
    bearer_token = get_api_server_token(api_server_token, cluster_server_url)
    pod_m = pod_manager(cluster_server_url, bearer_token)
    # 删除Pod
    print("--------delete pod with name ------------")
    pod_m.delete_pod(pod_name="nginx")
```

### SDK

```
将/root/.kube/config文件复制过来到脚本文件同级目录
```

创建

```python
import os
import yaml
from kubernetes import client, config
class pod_manager():
    def __init__(self,config_file):
        #传入配置文件
        config.load_kube_config(config_file)
        #获取API,管理Pod
        self.api = client.CoreV1Api()
    def create_pod(self,yamlFile):
        # 获取当前文件的绝对路径
        fileNamePath = os.path.split(os.path.realpath(__file__))[0]
        # 获取yaml配置文件的路径
        yamlPath = os.path.join(fileNamePath,yamlFile)
        #读取yaml文件，并转化为JSON数据
        with open(yamlPath,encoding="utf8") as f:
            result = yaml.safe_load(f) #转化成JSON格式
            resp = self.api.create_namespaced_pod(namespace="default",body=result)
            print(resp)
            #打印出创建时的具体信息
            print("\n[INFO] Pod `httpd` created.\n")
if __name__ == '__main__':
    pod_manager(config_file="config").create_pod(yamlFile="httpd-pod.yaml")
    
#只改文件名即可
```

查看

```python
import os
import yaml
from kubernetes import client, config
class pod_manager():
    def __init__(self,config_file):
        #传入配置文件
        config.load_kube_config(config_file)
        #获取API,管理Pod
        self.api = client.CoreV1Api()
    #查看Pod
    def get_pod(self):
        v1 = self.api
        resp = v1.read_namespaced_pod(name="httpd",namespace="default")
        #print(resp)
        print("\n[INFO] Pod `httpd` is read.\n")
if __name__ == '__main__':
    pod_manager(config_file="config").get_pod()
    
只改pod名即可
```

更新

```python
import os
import yaml
from kubernetes import client, config
class pod_manager():
    def __init__(self,config_file):
        #传入配置文件
        config.load_kube_config(config_file)
        #获取API,管理Pod
        self.api = client.CoreV1Api()
    #修改Pod的镜像（改）
    def update_pod(self):
        v1 = self.api
        old_resp = v1.read_namespaced_pod(name="httpd",namespace="default")
        #修改镜像
        old_resp.spec.containers[0].image = "httpd:latest"
        new_resp = v1.patch_namespaced_pod(name="nginx",namespace="default",body=old_resp)
        #print(new_resp)
        #打印信息
        print("\n[INFO] Update the image to httpd: latest \n")
if __name__ == '__main__':
    pod_manager(config_file="config").update_pod()
```

删除

```python
import os
import yaml
from kubernetes import client, config
class pod_manager():
    def __init__(self,config_file):
        #传入配置文件
        config.load_kube_config(config_file)
        #获取API,管理Pod
        self.api = client.CoreV1Api()
    #删除Pod（删）
    def delete_pod(self):
        v1 = self.api
        resp = v1.delete_namespaced_pod(name="httpd", namespace="default")
        #print(resp)
        print("\n[INFO] The Pod `httpd` is Deleted \n")
if __name__ == '__main__':
    pod_manager(config_file="config").delete_pod()
```

