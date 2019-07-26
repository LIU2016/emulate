'''

使用同一个会话（session）

'''

import requests

session=requests.Session()
session.get("http://httpbin.org/cookies/set/name1/lqd002")
resp=session.get("http://httpbin.org/cookies")
print(resp.text)