[TOC]

# linux下的常用操作

## 查看linux进程占用的内存

```properties
可以直接使用top命令后，查看%MEM的内容。可以选择按进程查看或者按用户查看，如想查看oracle用户的进程内存使用情况的话可以使用如下的命令：
　 (1)top
　　top命令是Linux下常用的性能分析工具，能够实时显示系统中各个进程的资源占用状况，类似于Windows的任务管理器
　　可以直接使用top命令后，查看%MEM的内容。可以选择按进程查看或者按用户查看，如想查看oracle用户的进程内存使用情况的话可以使用如下的命令：
　　$ top -u oracle
内容解释：
　　PID：进程的ID
　　USER：进程所有者
　　PR：进程的优先级别，越小越优先被执行
　　NInice：值
　　VIRT：进程占用的虚拟内存
　　RES：进程占用的物理内存
　　SHR：进程使用的共享内存
　　S：进程的状态。S表示休眠，R表示正在运行，Z表示僵死状态，N表示该进程优先值为负数
　　%CPU：进程占用CPU的使用率
　　%MEM：进程使用的物理内存和总内存的百分比
　　TIME+：该进程启动后占用的总的CPU时间，即占用CPU使用时间的累加值。
　　COMMAND：进程启动命令名称
　　常用的命令：
　　P：按%CPU使用率排行
　　T：按MITE+排行
　　M：按%MEM排行
(2)pmap
　　可以根据进程查看进程相关信息占用的内存情况，(进程号可以通过ps查看)如下所示：
　　$ pmap -d 14596
(3)ps
　　如下例所示：
　　$ ps -e -o 'pid,comm,args,pcpu,rsz,vsz,stime,user,uid'  其中rsz是是实际内存
　　$ ps -e -o 'pid,comm,args,pcpu,rsz,vsz,stime,user,uid' | grep oracle |  sort -nrk5
　　其中rsz为实际内存，上例实现按内存排序，由大到小
```

## 磁盘挂载和取消挂载

```properties
mkfs.ext4 /dev/vdb //新建数据盘，要格式化
mkdir /data
mount /dev/vdb /data
vi /etc/fstab
/dev/vda2               /usr/twsm               ext4    defaults        0 0
/dev/vda3               /opt                    ext4    defaults        0 0
/dev/vdb                /data                   ext4    defaults        0 0
umount /dev/vdb   ，其他反过来

更换磁盘：
将老数据拷贝到临时目录B，将新磁盘S1挂载上B。
将旧磁盘S2取消挂载A。
创建同名目录A。
取消新磁盘挂载B，然后挂载到这个同名目录A即可。
```

## 磁盘分区

```properties
fdisk -l
fdisk /dev/vda
n
p
2
p5
w
fdisk -l
fdisk /dev/vda
n
p
3
p
w
fdisk -l
reboot
mkfs.ext4 /dev/vda2
mkfs.ext4 /dev/vda3
mkdir /usr/twsm
mount /dev/vda2 /usr/twsm
mount /dev/vda3 /opt
```

## Linux如何查看端口

> lsof -i:端口号 用于查看某一端口的占用情况，比如查看8000端口使用情况，lsof -i:8000
>
> netstat -tunlp |grep 端口号，用于查看指定的端口号的进程情况，如查看8000端口的情况，netstat -tunlp |grep 8000



# shell 脚本编写

## 语法

### if

```shell
1.只适用于数值的比较
该类型操作会把两边变量当成整型进行加减运算，字符串abcd按整型运算无法进行，所以此类型不能用于字符串比较

参数	说明
-eq	等于则为真
-ne	不等于则为真
-gt	大于则为真
-ge	大于等于则为真
-lt	小于则为真
-le	小于等于则为真
 

 

 

 

 

 

 

 

2.适用于字符串的比较（也可用于数值比较）
参数	说明
==	相等则为真
!=	不相等则为真
 

 

 

 

3.字符串测试运算
参数	说明
-z 字符串	字符串的长度为零则为真
-n 字符串	字符串的长度不为零则为真
 
 
 
 

4.文件测试运算
参数	说明
-e 文件名	如果文件存在则为真
-r 文件名	如果文件存在且可读则为真
-w 文件名	如果文件存在且可写则为真
-x 文件名	如果文件存在且可执行则为真
-s 文件名	如果文件存在且至少有一个字符则为真
-d 文件名	如果文件存在且为目录则为真
-f 文件名	如果文件存在且为普通文件则为真
-c 文件名	如果文件存在且为字符型特殊文件则为真
-b 文件名	如果文件存在且为块特殊文件则为真

```

解决执行脚本报syntax error: unexpected end of file或syntax error near unexpected token `fi'错误的问题：

vim --- > set ff=unix