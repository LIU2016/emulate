#
# 爬虫实战 -
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
    aList = findall('<a[^>]*titlelnk[^>]*>[^<]*</a>', htmlStr)
    result = []
    for a in aList:
        g = search('href[\s]*=[\s]*[\'"]([^>\'""]*)[\'"]',a)
        if g is not None:
            url = g.group(1)
        index1 = a.find(">")
        index2 = a.rfind("<")
        title = a[index1+1:index2]
        d={}
        d['url'] = url
        d['title'] = title
        result.append(d)

    return result


def crawler(url):
    html = download(url)
    urls = parser(html)
    for url in urls:
        print('title',url['title'])
        print('url',url['url'])

print(crawler('https://www.cnblogs.com/'))



