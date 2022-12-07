import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cdb.v20170320 import cdb_client, models
try:
    cred = credential.Credential("AKIDzfGQK0Qn57uQhisyDRLPCl0yYpwhwTBm", "NUNegV3f1B1by4xaJq9bjzzkIZKtDANJ")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "cdb.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = cdb_client.CdbClient(cred, "ap-beijing", clientProfile)

    req = models.CreateDBInstanceHourRequest()
    params = {
        "GoodsNum": 1,
        "Memory": 1000,
        "Volume": 50,
        "Zone": "ap-beijing-3",
        "InstanceName": "chinacloudmysql",
        "EngineVersion": "5.7"
    }
    req.from_json_string(json.dumps(params))

    resp = client.CreateDBInstanceHour(req)
    print(resp.to_json_string())
    print('create successful')
    req = models.DescribeDBInstancesRequest()
    resp = client.DescribeDBInstances(req)
    print(resp.to_json_string())
except TencentCloudSDKException as err:
    print(err)