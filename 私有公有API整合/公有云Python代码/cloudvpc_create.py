import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.vpc.v20170312 import vpc_client, models

try:
    cred = credential.Credential("AKIDVmY5LOJtFK7RWLzEixuEgZkVyankOm9G", "xc6NN7Yy80b1qQjlqvjGWUFivaFdlbLF")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "vpc.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = vpc_client.VpcClient(cred, "ap-beijing", clientProfile)

    req = models.CreateVpcRequest()
    params = {
        "VpcName": "intnetPython",
        "CidrBlock": "192.168.2.0/24"
    }
    req.from_json_string(json.dumps(params))

    resp = client.CreateVpc(req)
    print(resp.to_json_string())

    req = models.DescribeVpcsRequest()
    resp = client.DescribeVpcs(req)
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)