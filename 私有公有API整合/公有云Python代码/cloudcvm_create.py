import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import cvm_client, models
try:
    cred = credential.Credential("AKIDzfGQK0Qn57uQhisyDRLPCl0yYpwhwTBm", "NUNegV3f1B1by4xaJq9bjzzkIZKtDANJ")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "cvm.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = cvm_client.CvmClient(cred, "ap-beijing", clientProfile)

    req = models.RunInstancesRequest()
    params = {
        "Placement": {
            "Zone": "ap-beijing-3"
        },
        "SystemDisk": {
        "DiskType": "CLOUD_PREMIUM",
        "DiskSize": 60
        },
        "InstanceName": "chinacloudskill",
        "ImageId": "img-25szkc8t",
        "InstanceType": "S5.SMALL4",
        "InstanceChargeType": "POSTPAID_BY_HOUR"
    }
    req.from_json_string(json.dumps(params))

    resp = client.RunInstances(req)
    print(resp.to_json_string())
    print('create successful')

    req = models.DescribeInstancesRequest()
    resp = client.DescribeInstances(req)
    print(resp.to_json_string())
except TencentCloudSDKException as err:
    print(err)