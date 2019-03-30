# Linux服务器开发

## 搭建开发环境

### 安装samba服务器

[参考文档](https://blog.csdn.net/learner198461/article/details/77651949)

``` properties
安装：
yum install -y samba samba-common

添加/etc/samba/smb.conf的配置且新建lqd账号：
[share]
       comment = this is samba dir
       path = /home/lqd/share
       writable = yes
       browseable = yes

添加用户[root账号下面执行]：
sudo smbpasswd -a lqd
sudo smbpasswd -a root
setsebool -P samba_enable_home_dirs 1

启动：
systemctl start smb.service

```

## 入门必备命令

## 开启linux编程之旅

```
只编译执行一个C程序
$ gcc hello.c                                                                     
$ ./a.out                                                                         
$Hello world!                                                                    

默认的a.out 并不友好，gcc 提供 -o 选项指定执行文件的文件名：
$gcc -o hello  hello.c       ##编译源代码，并把可执行文件命名为 hello                
$Hello world!                                                                     

编译C++程序，我们可以直接用GCC 编译其中的g++命令，用法同 gcc；当然g++ 和 gcc 都可以用来编译 c 和 c++程序。gcc 编译c++程序需要带上 -lstdc++  指定使用c++库。
```

### **编译常用选项**

| 选   项 | 功   能                                          |
| ------- | ------------------------------------------------ |
| -c      | 只激活预处理、编译和汇编,生成.o 目标代码文件     |
| -S      | 只激活预处理和编译，生成扩展名为.s的汇编代码文件 |
| -E      | 只激活预处理，并将结果输出至标准输出             |
| -g      | 为调试程序(如gdb)生成相关信息                    |
| -O      | 等同-O1,常用的编译优化选项                       |
| -Wall   | 打开一些很有用的警告选项，建议编译时加此选项。   |

注意：-c 选项在编写大型程序是必须的，多个文件的源代码首先需要编译成目标代码，再链接成执行文件。如果由多个源文件，工程做法建议采用 makefile 。

## 网络服务器开发



## 多线程并发服务器