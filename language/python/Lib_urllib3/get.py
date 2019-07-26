'''
urllib 处理URL
urllib3升级HTTP1.1的标准
1.线程安全
2.连接池
3.SSL验证
4.上传文件

'''

from urllib3 import *
from urllib.parse import urlencode
disable_warnings()

httpPool = PoolManager()

url="http://www.baidu.com/s?"
url="http://www.cnhnb.com/p/sgzw/"
response = httpPool.request(url=url, method="GET")

print(response.data.decode('utf-8'))


