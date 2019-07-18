import urllib.request

data = bytes(urllib.parse.urlencode({'name':'Bill','age':30}),encoding='utf-8')
response = urllib.request.urlopen('http://httpbin.org/post',data=data)
print(response.read().decode('utf-8'))
