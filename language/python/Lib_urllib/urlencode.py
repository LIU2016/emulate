'''

url encode decode

'''

from urllib.parse import urljoin,unquote,quote,parse_qs,parse_qsl

query="key=1000&value=00000"

result=parse_qs(query)
result1=parse_qsl(query)

print(result)
print(result1)


