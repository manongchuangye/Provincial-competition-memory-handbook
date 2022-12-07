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

    req = models.CreateBackupRequest()
    params = {
        "BackupMethod": "logical",
        "InstanceId": "cdb-pefbbx28"
    }
    req.from_json_string(json.dumps(params))

    resp = client.CreateBackup(req)
    print(resp.to_json_string())
    req = models.DescribeBackupsRequest()
    params = {
        "InstanceId": "cdb-pefbbx28"
    }
    req.from_json_string(json.dumps(params))
    resp = client.DescribeBackups(req)
    print(resp.to_json_string())
except TencentCloudSDKException as err:
    print(err)