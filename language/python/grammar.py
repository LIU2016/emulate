import keyword

## 解释性语言
## 输出对应的python的保留字
print(keyword.kwlist)

## if 与 缩进部分 是个完整整体。
age = 18
if age > 18:
    print("18岁了")
else:
    print("还未18")
print("没有缩进")
