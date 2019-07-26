import requests

from requests.auth import HTTPBasicAuth

r = requests.get("http://127.0.0.1:5000/",auth=HTTPBasicAuth('lqd1','123456'))
print(r.text)