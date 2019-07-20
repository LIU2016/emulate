# 使用urlopen函数发送请求
'''https://docs.python.org/3/library/index.html'''

import server.request

response= server.request.urlopen("https://www.jd.com")
print('resp类型:',type(response))
print('resp响应状态码:',response.status)
print('resp的headers',response.headers)
print('resp的内容:',response.read().decode('utf-8'))

