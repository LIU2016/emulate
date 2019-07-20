'''

HTTPBasicAuthHandler
build_opener

'''

from server import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener
from server import URLError

username = 'lqd'
password = '123456'
url = "http://127.0.0.1:5000/"
p = HTTPPasswordMgrWithDefaultRealm()
p.add_password("localhost", url, username, password)
auth_handler = HTTPBasicAuthHandler(p)

opener = build_opener(auth_handler)
try:
    result = opener.open(url)
    html = result.read().decode('utf-8')
    print(html)
except URLError as e:
    print(e.reason)

