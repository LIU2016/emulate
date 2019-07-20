'''



'''

from urllib.parse import urlparse, urlunparse ,urljoin

result = urlparse('http://www.baidu.com/url.do?key=1')
print("scheme", result.scheme)
print(urljoin('http://www.baid/?key=000','?name=00'))

