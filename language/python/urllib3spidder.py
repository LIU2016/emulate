#
# 爬虫
#
#

from re import *
from urllib3 import *

http = PoolManager()
disable_warnings()


def download(url):
    result = http.request('GET', url)
    htmlStr = result.data.decode('utf-8')
    return htmlStr


def parser(htmlStr):
    aList = findall('<a[^>]*>', htmlStr)
    result = []
    for a in aList:
        g = search('href[\s]*=[\s]*[\'"]([^>\'""]*)[\'"]',a)
        if g is not None:
            url = g.group(1)
            result.append(url)
            print(url)
    return result


def crawler(url):
    html = download(url)
    urls = parser(html)
    for url in urls:
        crawler(url)

print(crawler('http://www.baidu.com'))



