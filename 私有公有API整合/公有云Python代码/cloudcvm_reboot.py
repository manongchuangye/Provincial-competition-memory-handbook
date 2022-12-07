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

    req = models.RebootInstancesRequest()
    params = {
        "InstanceIds": ["ins-79zd86i5"]
    }
    req.from_json_string(json.dumps(params))

    resp = client.RebootInstances(req)
    print(resp.to_json_string())
    print('reboot successful')

    req = models.DescribeInstancesStatusRequest()
    resp = client.DescribeInstancesStatus(req)
    print(resp.to_json_string())
except TencentCloudSDKException as err:
    print(err)