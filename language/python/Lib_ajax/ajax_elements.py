'''

    ELements : 未渲染的渲染完的结果
    REsponse ：异步的请求后的结果 (Ajax)

'''

import requests
import json

result = requests.get("")
text = result.text.encode("utf-8").decode("unicode-escape")
print(text)
json.load(text)

