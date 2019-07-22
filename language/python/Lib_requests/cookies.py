import requests

resp=requests.get("http://www.baidu.com")
print(resp.cookies)
cookies=resp.cookies
for key,value in cookies.items():
    print(key,'=',value)

#headers cookie


#
