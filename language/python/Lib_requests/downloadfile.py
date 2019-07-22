import requests

r = requests.request(url="http://t.cn/EfgN7gz",method="GET")

print(r.content)

with open('Python.png','wb') as f:
    f.write(r.content)
