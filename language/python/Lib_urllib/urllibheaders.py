''' 请求头 中英文值~~ '''

from urllib import request
from urllib.parse import unquote, urlencode
import base64
import json

url = "http://httpbin.org/post"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Host': 'httpbin.org',
    'who': 'python urllib',
    'Chinesel': urlencode({'name': '柴宝宝'}),  ##url编码
    'describe': base64.b64encode(bytes('这是中文请求头，完美！', encoding='utf-8'))  ##base64编码
}
dict = {
    'name': 'dingguo',
    'age': '32'
}

data = bytes(urlencode(dict), encoding="utf-8")
req = request.Request(url=url, headers=headers, data=data, method='POST')
req.add_header('Chinese2', urlencode({'国籍': '中国'}))
response = request.urlopen(req)
value = response.read().decode('utf-8')
print(value)

responseobj=json.loads(value)
print(unquote(responseobj['headers']['Chinesel']))
print(unquote(responseobj['headers']['Chinese2']))
print(str(base64.b64decode(responseobj['headers']['Describe']),'utf-8'))