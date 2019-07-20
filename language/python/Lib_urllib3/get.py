'''
urllib 处理URL
urllib3升级HTTP1.1的标准
1.线程安全
2.连接池
3.SSL验证
4.上传文件

'''

from urllib3 import *
disable_warnings()

httpPool = PoolManager()




