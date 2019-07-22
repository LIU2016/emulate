import urllib.request
import socket
import urllib.error

try:
    response = urllib.request.urlopen("http://www.baidu.com",timeout=0.001)
    print(response.status)
except urllib.error.URLError as e:
    if isinstance(e.reason,socket.timeout):
        print("超时了")
    else:
        print("其他原因")
print("other")

