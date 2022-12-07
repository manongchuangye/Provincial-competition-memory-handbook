SecretId = "AKIDzfGQK0Qn57uQhisyDRLPCl0yYpwhwTBm"
SecretKey = "NUNegV3f1B1by4xaJq9bjzzkIZKtDANJ"

import time
uri = "cvm.tencentcloudapi.com"
paramDict = {
    "Action":"DescribeImages",
    "Version":"2017-03-12",
    "SecretId":SecretId,
    "Nonce":123456,
    "Timestamp":int(time.time()),
    "Region":"ap-beijing",
    "ImageIds.0":"img-25szkc8t"
}
tempList = []
tempDict = {}
for eveKey, eveValue in paramDict.items():
    tempLowerData = eveKey.lower()
    tempList.append(tempLowerData)
    tempDict[tempLowerData] = eveKey
tempList.sort()

resultList = []
for eveData in tempList:
    tempStr = str(tempDict[eveData]) + "=" + str(paramDict[tempDict[eveData]])
    resultList.append(tempStr)

sourceStr = "&".join(resultList)

requestStr = "%s%s%s%s%s"%("GET", uri, "/", "?", sourceStr)

import sys
if sys.version_info[0] > 2:
    signStr = requestStr.encode("utf-8")
    SecretKey = SecretKey.encode("utf-8")

import hashlib
digestmod = hashlib.sha1

import hmac
hashed = hmac.new(SecretKey, signStr, digestmod)

import binascii
base64Data = binascii.b2a_base64(hashed.digest())[:-1]

if sys.version_info[0] > 2:
    base64Data = base64Data.decode()

import urllib.parse
base64Data = urllib.parse.quote(base64Data)

url = "https://" + uri + "/" + "?" + sourceStr + "&Signature=" + base64Data
print(url)

import urllib.request
import json
print(json.loads(urllib.request.urlopen(url).read().decode("utf-8")))