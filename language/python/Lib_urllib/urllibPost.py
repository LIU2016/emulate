import server.request

data = bytes(server.parse.urlencode({'name': 'Bill', 'age':30}), encoding='utf-8')
response = server.request.urlopen('http://httpbin.org/post', data=data)
print(response.read().decode('utf-8'))
