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

    req = models.CreateSubnetRequest()
    params = {
        "VpcId": "vpc-64oyzyzo",
        "SubnetName": "intnetPython-subnet",
        "CidrBlock": "192.168.2.0/25",
        "Zone": "ap-beijing-3"
    }
    req.from_json_string(json.dumps(params))

    resp = client.CreateSubnet(req)
    print(resp.to_json_string())


    req = models.DescribeSubnetsRequest()
    resp = client.DescribeSubnets(req)
    print(resp.to_json_string())
except TencentCloudSDKException as err:
    print(err)