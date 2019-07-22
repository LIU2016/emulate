from requests import *


playload={"username":"lqd","password":"123456"}
resp=post(url="http://httpbin.org/post",data=playload)

print(resp.json()['form']['password'])
