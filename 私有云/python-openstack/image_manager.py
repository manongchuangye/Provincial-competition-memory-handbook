#encoding:utf-8
import requests,json,time

def get_auth_token(controller_ip,domain_name,username,password):
    try:
        url = f"http://{controller_ip}:5000/v3/auth/tokens"
        body = {
            "auth": {
                "identity": {
                    "methods": ['password'],
                    "password": {
                        "user": {
                            "domain": {"name": domain_name},
                            "name": username,
                            "password": password
                        }
                    }
                },
                "scope": {
                    "project": {
                        "domain": {"name": domain_name},
                        "name": username,
                    }
                }
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        tokens = requests.post(url,headers=headers,data=json.dumps(body)).headers['X-Subject-Token']
        headers = {
            "X-Auth-Token": tokens
        }
        print(f"get token:{tokens}")
        return headers
    except Exception as e:
        print(f"token err:{e}")

class ImageManager:
    def __init__(self,headers,url):
        self.headers = headers
        self.url = url

    def CreateImage(self,name,disk_format,container_format):
        body = {
            "name": name,
            "disk_format": disk_format,
            "container_format": container_format
        }
        req = json.loads(requests.post(self.url,headers=self.headers,data=json.dumps(body)).text)
        return req

    def GetImageId(self,name):
        images = json.loads(requests.get(self.url,headers=self.headers).text)
        for img in images['images']:
            if img['name'] == name:
                return img['id']
            return "NONE"

    def UploadImage(self,id,image_file):
        url = self.url + "/" + id + "/file"
        self.headers["Content-Type"] = "application/octet-stream"
        req = requests.put(url, headers=self.headers, data=open(image_file, 'rb').read())
        return req

    def GetImage(self,id):
        url = self.url + "/" + id
        req = json.loads(requests.get(url,headers=self.headers).text)
        return req

    def DeleteImage(self,id):
        url = self.url + "/" + id
        req = requests.delete(url,headers=self.headers)
        if req.status_code == 204:
            return {"Delte Image Successful:",req.status_code}

if __name__ == "__main__":
    controller_ip = "controller"
    domain_name = "demo"
    username = "admin"
    password = "000000"
    headers = get_auth_token(controller_ip,domain_name,username,password)
    image_m = ImageManager(headers,f"http://{controller_ip}:9292/v2/images")

    create_im = image_m.CreateImage("cirros0001","qcow2","bare")
    print(f"Create Image Successful:{create_im}")

    id = image_m.GetImageId("cirros0001")
    print(f"ImageId is:{id}")

    upload_im = image_m.UploadImage(id,"./cirros-0.3.4-x86_64-disk.img")
    print(f"Upload Status:{upload_im}")

    get_im = image_m.GetImage(id)
    print(f"Images is:{get_im}")