import json
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cbs.v20170312 import cbs_client, models
try:
    cred = credential.Credential("AKIDzfGQK0Qn57uQhisyDRLPCl0yYpwhwTBm", "NUNegV3f1B1by4xaJq9bjzzkIZKtDANJ")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "cbs.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = cbs_client.CbsClient(cred, "ap-beijing", clientProfile)

    req = models.CreateDisksRequest()
    params = {
        "Placement": {
            "Zone": "ap-beijing-3"
        },
        "DiskType": "CLOUD_PREMIUM",
        "DiskChargeType": "POSTPAID_BY_HOUR",
        "DiskName": "chinaclouddisk",
        "DiskSize": 10
    }
    req.from_json_string(json.dumps(params))

    resp = client.CreateDisks(req)
    print(resp.to_json_string())
    print('create successful')

    time.sleep(5)
    req = models.DescribeDisksRequest()
    resp = client.DescribeDisks(req)
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)