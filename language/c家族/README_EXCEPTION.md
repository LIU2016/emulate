```c
[root@localhost server]# gcc echo_server.c -o echo_server
echo_server.c: In function ‘errormsg’:
echo_server.c:15:5: warning: incompatible implicit declaration of built-in function ‘exit’ [enabled by default]
     exit(1);

解决方法：
-------------------
少了stdlib.h

直接通过man 命令查看就可以了
查看[root@localhost server]# man perror 命令依赖的头文件

```



```
visual studio 2017 编译报错：无法找到stdio.h的源文件：

解决方法：
---------------------
https://blog.csdn.net/liuerquan/article/details/79541421
https://blog.csdn.net/z_m_1/article/details/80833782
https://blog.csdn.net/xapxxf/article/details/78356612 重点
```



```
严重性	代码	说明	项目	文件	行	禁止显示状态
错误	MSB8020	无法找到 v120 的生成工具(平台工具集 =“v120”)。若要使用 v120 生成工具进行生成，请安装 v120 生成工具。或者，可以升级到当前 Visual Studio 工具，方式是通过选择“项目”菜单或右键单击该解决方案，然后选择“重定解决方案目标”。	secondhelloworld	D:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\IDE\VC\VCTargets\Microsoft.Cpp.Platform.targets	67	

解决方法：
------------------------

```



```
引用#include <Winsock2.h> ，wingdi.h报错

解决方法：
-------------------------
将#include <Winsock2.h>放在stdio.h前面
```



```
visual studio 调试时提示 已加载“C:\Windows\SysWOW64\ntdll.dll”。无法查找或打开 PDB 文件。

解决方法：
-------------------------
开启服务器支持、符号支持
https://blog.csdn.net/win_turn/article/details/50468115
```

