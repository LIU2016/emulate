from urllib3 import *

disable_warnings()
http = PoolManager()
url = "http://localhost:5000/upload"

while True:
    filename = input("请输入上传文件名:")
    if not filename:
        break
    with open(filename, 'rb') as fp:
        fileData = fp.read()
    response = http.request("POST", url, fields={'file': (filename, fileData)})
    print(response.data.decode())
