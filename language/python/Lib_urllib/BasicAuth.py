'''

'''
from server import request
import base64

url = 'http://127.0.0.1:5000'
headers = {
    'Authorization': 'Basic '+str(base64.b64encode(bytes('lqd:123456','utf-8')),'utf-8'),
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Host': '127.0.0.1:5000'
}
req = request.Request(url=url,headers=headers,method='GET')
resp = request.urlopen(req)
print(resp.read().decode('utf-8'))
