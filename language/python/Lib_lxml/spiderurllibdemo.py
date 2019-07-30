'''

https://m.zongheng.com/h5/chapter/list?bookid=89605&fpage=36&fmodule=24&_st=36_24-0_89605
https://www.cnhnb.com/p/sgzw/
xpath lxml

//* 所有节点
//li/a , //ul//a  子节点
[@class=""] 选取特定属性
contains 函数 包含 a[contains(@href,'www')]
.. 父节点
.  当前节点

and or

选择器

节点轴  - 祖先节点 ancestor[@class="www"]
        - 子节点   child::a
        - 子孙节点 descendant::li
        - 列出除本身外的后面所有节点 following
        - 列出除本身外的后面所有的兄弟节点 following-sibling

yield - 产生器函数
for item in yield函数： item就是产生器函数生成的对象

'''

from urllib3 import *
from lxml import etree
http= PoolManager()
disable_warnings()
response=http.request(url="https://www.cnhnb.com/supply/",method="GET").data
html=response.decode("utf-8", errors="replace")
#print(html)
parser=etree.HTMLParser();
#tree=etree.parse(html,parser)
#root=etree.fromstring(html,parser)

tree=etree.HTML(html,parser)
litags=tree.xpath('//li[@class="first-cate-item" and contains(@href,"/p")]')
mainType=[]
if len(litags) :
    for li in litags :
        print(li[0].get("href"))
        print(li[0].text)
        mainType.append({"href":li[0].get("href"),"title":li[0].text})

with open("mainType.txt","w") as f:
    f.write(str(mainType))

first = tree.xpath("//li//a[1]/text()");
#print(first)

first = tree.xpath("//li//a[position()>3]/text()");
#print(first)

first = tree.xpath("//li//a[position()>3 or position()=last()-1]/text()");
#print(first)

ancestors = tree.xpath("//a[1]/ancestor::*")
#for ancestor in ancestors:
   # print(ancestor.tag)

# pattern = '<a.*?href="(.+)".*?>(.*?)</a>'
#result = re.search(pattern,html)
#print(result)



