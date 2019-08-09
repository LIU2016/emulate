'''

比xpath lxml 更方便的

节点选择器：
            若有同名节点，只输出第一个，不存在，输出None :soup.title

直接子节点：
            contents、children
孙子节点选择器：
            descendants

方法选择器：
           find find_all

css选择器：
          select

获取文本：
          get_text，string属性

获取属性值：
          ['key'],attrs['key']

通过浏览器直接拷贝选择器

'''

from bs4 import BeautifulSoup
from urllib3 import *

http=PoolManager()
disable_warnings()
response= http.request(url="https://www.cnhnb.com/supply/",method="GET").data
html=response.decode("utf-8")
#print(html)

soup=BeautifulSoup(html,'lxml')
#print(soup.title.string)

#print(soup.body.contents)
#print(soup.body.children)
for i,item in enumerate(soup.body.div.ul):
    print(i,item)


