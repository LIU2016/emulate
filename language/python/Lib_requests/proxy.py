'''

代理

'''

import requests

proxy_handler = {
    'http': 'http://112.252.192.158:32629',
    'https': 'https://112.252.192.158:32629'
}

resp=requests.get("https://www.baidu.com",proxies=proxy_handler)

print(resp.text)

