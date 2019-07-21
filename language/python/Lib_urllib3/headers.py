from urllib3 import *
import re

disable_warnings()

url = "http://httpbin.org/get"

http = PoolManager()


# 分析文件 ，读取请求头
def str2Headers(file):
    headerDict = {}
    f = open(file, 'r')
    headerText = f.read()
    headersTmp = re.split('\n', headerText)
    for header in headersTmp:
        result = re.split(":", header, maxsplit=1)
        headerDict[result[0]] = result[1]
    f.close()
    return headerDict


headers = str2Headers('headers.txt')
print(headers)
response = http.request(url=url, headers=headers, method="GET")
for key in response.info().keys():
    print(key, ":", response.info()[key])
