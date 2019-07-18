### 环境搭建

```properties
1，安装python
https://www.python.org/
例如：https://www.python.org/ftp/python/3.7.2/python-3.7.2.exe
要使用python3及以上

2，安装pycharm 专业版
下载：
https://www.jetbrains.com/pycharm/
激活码：
https://blog.csdn.net/qq_32811489/article/details/78636049
https://blog.csdn.net/u014044812/article/details/78727496
https://blog.csdn.net/weixin_43641304/article/details/87071864

3，安装python库
pip install requests -i http://pypi.douban.com/simple --trusted-host=pypi.douban.com
python -m pip install -upgrade pip

```

#### 包依赖工具

```properties
pip:是 Python 包管理工具，该工具提供了对Python 包的查找、下载、安装、卸载的功能。
https://www.runoob.com/w3cnote/python-pip-install-usage.html

注意：若是使用pip，最好是在C:\Windows\System32执行命令。

C:\Windows\System32>python -m ensurepip
Looking in links: C:\Users\lqd\AppData\Local\Temp\tmp871mshf6
Requirement already satisfied: setuptools in d:\python\python37-32\lib\site-packages (40.6.2)
Collecting pip
Installing collected packages: pip
Successfully installed pip-18.1

C:\Windows\System32>python -m pip install --upgrade pip
Collecting pip
  Using cached https://files.pythonhosted.org/packages/5c/e0/be401c003291b56efc55aeba6a80ab790d3d4cece2778288d65323009420/pip-19.1.1-py2.py3-none-any.whl
Installing collected packages: pip
  Found existing installation: pip 18.1
    Uninstalling pip-18.1:
      Successfully uninstalled pip-18.1
Successfully installed pip-19.1.1

C:\Windows\System32>
C:\Windows\System32>pip install urllib3
Requirement already satisfied: urllib3 in d:\python\python37-32\lib\site-packages (1.25.3)

C:\Windows\System32>pip uninstall urllib3
Uninstalling urllib3-1.25.3:
  Would remove:
    d:\python\python37-32\lib\site-packages\urllib3-1.25.3.dist-info\*
    d:\python\python37-32\lib\site-packages\urllib3\*
Proceed (y/n)? y
  Successfully uninstalled urllib3-1.25.3
```

