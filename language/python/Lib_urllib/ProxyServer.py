'''

175.14.141.6:42970
https://proxy.horocn.com/login.html
https://proxy.horocn.com/api/free-proxy?format=json&loc_name=%E4%B8%AD%E5%9B%BD&app_id=163957843537099843348

'''

from server import URLError
from server import ProxyHandler, build_opener

proxy_handler = ProxyHandler({
    'http': 'http://14.116.153.16:3128',
    'https': 'https://14.116.153.16:3128'
})

opener = build_opener(proxy_handler)
try:
    resp = opener.open('http://www.baidu.com')
    print(resp.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
