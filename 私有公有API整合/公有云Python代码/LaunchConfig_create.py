import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.autoscaling.v20180419 import autoscaling_client, models

try:
    cred = credential.Credential("AKIDVmY5LOJtFK7RWLzEixuEgZkVyankOm9G", "xc6NN7Yy80b1qQjlqvjGWUFivaFdlbLF")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "as.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = autoscaling_client.AutoscalingClient(cred, "ap-beijing", clientProfile)

    req = models.CreateLaunchConfigurationRequest()
    params = {
        "LaunchConfigurationName": "template-python",
        "ImageId": "img-25szkc8t",
        "InternetAccessible": {
            "InternetChargeType": "BANDWIDTH_POSTPAID_BY_HOUR",
            "PublicIpAssigned": True,
            "InternetMaxBandwidthOut": 5
        },
        "HostNameSettings": {
            "HostName": "VM-python"
        },
        "InstanceType": "SA2.MEDIUM4",
        "InstanceChargeType": "POSTPAID_BY_HOUR"
    }
    req.from_json_string(json.dumps(params))

    resp = client.CreateLaunchConfiguration(req)
    print(resp.to_json_string())
    req = models.DescribeLaunchConfigurationsRequest()
    resp = client.DescribeLaunchConfigurations(req)
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)