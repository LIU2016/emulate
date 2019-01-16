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



## CentOS修改IP地址

**# ifconfig eth0 192.168.1.80**

这样就把IP地址修改为**192.168.1.80**(如果发现上不了网了，那么你可能需要把网关和DNS也改一下，后面会提到)，但是当你重新启动系统或网卡之后，还是会变回原来的地址，这种修改方式只适用于需要临时做IP修改。要想永久性修改，就要修改**/etc/sysconfig/network-scripts/ifcfg-eth0**这个文件，这个文件的主要内容如下（你的文件中没有的项，你可以手动添加）：

**# vi  /etc/sysconfig/network-scripts/ifcfg-eth0**

**DEVICE=eth0 #描述网卡对应的设备别名**

**BOOTPROTO=static #设置网卡获得ip地址的方式，选项可以为为static，dhcp或bootp**

**BROADCAST=192.168.1.255 #对应的子网广播地址**

**HWADDR=00:07:E9:05:E8:B4 #对应的网卡物理地址**

**IPADDR=12.168.1.80 #只有网卡设置成static时，才需要此字段**

**NETMASK=255.255.255.0 #网卡对应的网络掩码**

**NETWORK=192.168.1.0 #网卡对应的网络地址，也就是所属的网段**

**ONBOOT=yes #系统启动时是否设置此网络接口，设置为yes时，系统启动时激活此设备**

## CentOS修改网关

**# route add default gw 192.168.1.1 dev eth0**

这样就把网关修改为**192.168.1.1了**，这种修改只是临时的，当你重新启动系统或网卡之后，还是会变回原来的网关。要想永久性修改，就要修改**/etc/sysconfig/network** 这个文件，这个文件的主要内容如下（你的文件中没有的项，你可以手动添加）：

**# vi  /etc/sysconfig/network**

**NETWORKING=yes #表示系统是否使用网络，一般设置为yes。如果设为no，则不能使用网络。**

**HOSTNAME=centos #设置本机的主机名，这里设置的主机名要和/etc/hosts中设置的主机名对应**

**GATEWAY=192.168.1.1 #设置本机连接的网关的IP地址。**

**********上面的文件修改完要重新启动一下网卡才会生效：**# service network restart** ***\*********

## CentOS修改DNS

上面的都修改完之后，当你ping一个域名是肯能不通，但ping对应的IP地址是同的，这时我们需要修改一下DNS。修改DNS要通过修改**/etc/resolv.conf**这个文件：

**# vi /etc/resolv.conf**

**nameserver 8.8.8.8 #google域名服务器 nameserver 8.8.4.4 #google域名服务器**

通过上面的所有设置，系统应该可以上网了。

如果centos系统建立在虚拟机之上，那么在设置虚拟机的网络时请选择‘网桥适配器’连接。

修改vi /etc/sysconfig/network-scripts/ifcfg-eth0，添加

```properties
DNS1=192.168.102.3
DNS2=8.8.8.8
```

## 更换yum源

进入以下目录，替换同目录的CentOS-Base.repo.

```shell
[root@root3-7 yum.repos.d]# ll
total 28
-rw-r--r--. 1 root root 1664 Aug 30  2017 CentOS-Base.repo
-rw-r--r--. 1 root root 1309 Aug 30  2017 CentOS-CR.repo
-rw-r--r--. 1 root root  649 Aug 30  2017 CentOS-Debuginfo.repo
-rw-r--r--. 1 root root  314 Aug 30  2017 CentOS-fasttrack.repo
-rw-r--r--. 1 root root  630 Aug 30  2017 CentOS-Media.repo
-rw-r--r--. 1 root root 1331 Aug 30  2017 CentOS-Sources.repo
-rw-r--r--. 1 root root 3830 Aug 30  2017 CentOS-Vault.repo
[root@root3-7 yum.repos.d]# pwd
/etc/yum.repos.d
```

## 根据端口定位到进程

netstat   -anp   |   grep  portno

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

