[TOC]

# 一、为什么要分库分表

> 超大容量问题
> 性能问题

# 二、如何去做到

包含：垂直切分、 水平切分

> \1. 垂直分库（按业务分库）； 解决的是表过多的问题
> \2. 垂直分表； 解决单表列过多的问题
> \3. 水平切分（数据分表，按拆分策略拆分等等）； 大数据表拆成小表

常见的拆分策略

> 垂直拆分（ER分片）
>
> 水平拆分
>
> ​    一致性hash（根据字段的维度，例如拿字段%10.）
>
> ​    范围切分 可以按照ID（ID 0~10W）.
>
> 日期拆分.

# 三、拆分带来的问题

## 跨库join的问题（A表 join B表）

> \1. 设计的时候考虑到应用层的join问题。调用接口
>
> \2. 全局表
>
> ​	\1. 数据变更比较少的基于全局应用的表
>
> ​	\2. 公共服务
>
> \3. 做字段冗余（空间换时间的做法）

## 跨分片数据排序分页

## 唯一主键问题

> 1，用自增id做主键
>
> UUID 性能比较低
>
> snowflake （分布式系统中，有一些需要使用全局唯一ID的场景，这种时候为了防止ID冲突可以使用36位的UUID，但是UUID有一些缺点，首先他相对比较长，另外UUID一般是无序的。
> 有些时候我们希望能使用一种简单一些的ID，并且希望ID能够按照时间有序生成。
> 而twitter的snowflake解决了这种需求，最初Twitter把存储系统从MySQL迁移到Cassandra，因为Cassandra没有顺序ID生成机制，所以开发了这样一套全局唯一ID生成服务
> ）
>
> 2，mongoDB 
>
> 3，zookeeper 
>
> 4，数据库表（全局唯一表，主键id）

## 分布式事务问题

2PC\3PC 多个数据库表之间保证原子性  性能问题； 互联网公司用强一致性分布式事务比较少。

# 四、如何权衡当前公司的存储需要优化

> 1． 提前规划（主键问题解决、 join问题）
> 2． 当前数据单表超过1000W、每天的增长量持续上升

# 五、mysql安装

![img](https://img.mubu.com/document_image/467479b3-9ccd-421f-b109-3f10f8dc117c-862021.jpg)

## mysql安装

### 安装以后文件对应的目录

mysql的数据文件和二进制文件： /var/lib/mysql/
mysql的配置文件： /etc/my.cnf
mysql的日志文件： /var/log/mysql.log

### 登录mysql

![img](https://img.mubu.com/document_image/f79a9105-fce7-4baf-b8eb-f78549f9d7d2-862021.jpg)

> 1，5.7版本默认对于root帐号有一个随机密码，可以通过 grep "password" /var/log/mysqld.log获得，root@localhost: 此处为随机密码
> 2，运行mysql -uroot -p 回车
> 3，粘贴随机密码，如上图所示。

### 操作

默认的随机密码是没办法直接对数据库做操作的，需要修改密码，然后，5.7版本用了validate_password密码加强插件，因此在修改密码的时候绝对不是 123456 能糊弄过去的。需要严格按照规范去设置密码
但是，如果想让密码简单点也可以，降低安全策略， 登录到mysql客户端执行如下两条命令
\>set global validate_password_length=1;
\>set global validate_password_policy=0; 
这样就能设置简单的密码了，但是密码长度必须是大于等于4位
\>set password=password("root");

### 赋权操作

默认情况下其他服务器的客户端不能直接访问mysql服务端，需要对ip授权
\>GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION;

### 卸载mysql

```
//rpm包安装方式卸载
查包名：rpm -qa|grep -i mysql
删除命令：rpm -e –nodeps 包名

//yum安装方式下载
1.查看已安装的mysql
命令：rpm -qa | grep -i mysql
2.卸载mysql
命令：yum remove mysql-community-server-5.6.36-2.el7.x86_64
查看mysql的其它依赖：rpm -qa | grep -i mysql

//卸载依赖
yum remove mysql-libs
yum remove mysql-server
yum remove perl-DBD-MySQL
yum remove mysql
```



# 六、主从实操

按前面的安装步骤分别部署2台mysql服务器。（132作为master节点，128作为slave节点）。

## master（132服务器）上操作：

在132服务器上创建数据同步账号。

![img](https://img.mubu.com/document_image/c4455b7c-ebf5-497d-81e8-6d4fad7c777f-862021.jpg)

创建一个用户’repl’,并且允许其他服务器可以通过该用户远程访问master，通过该用户去读取二进制数据，实现数据同步
Create user repl identified by ‘repl； repl用户必须具有REPLICATION SLAVE权限，除此之外其他权限都不需要
GRANT REPLICATION SLAVE ON *.* TO ‘repl’@’%’ IDENTIFIED BY ‘repl’ ; 

在132服务器修改my.cnf配置文件，在[mysqld] 下添加如下配置
log-bin=mysql-bin //启用二进制日志文件
server-id=132 服务器唯一ID

重启数据库 systemctl restart mysqld 

登录到数据库，通过show master status  查看master的状态信息：注意这个File字段，slave上需要用到。

![img](https://img.mubu.com/document_image/49cac387-aff1-42ab-a940-dd4ef2b1ccd2-862021.jpg)

## slave（128服务器）上操作

在128服务器修改my.cnf配置文件，在[mysqld] 下添加如下配置

server-id=132  服务器id，唯一
relay-log=slave-relay-bin //启动中继日志
relay-log-index=slave-relay-bin.index
read_only=1

重启数据库： systemctl restart mysqld

登录到数据库，通过如下命令建立同步连接

change master to master_host='192.168.254.132', master_port=3306,master_user='repl',master_password='repl',master_log_file='mysql-bin.000001',master_log_pos=154;
master_log_file和master_log_pos 从master的show master status可以找到对应的值，不能随便写。

start slave

show slave status\G;查看slave服务器状态，当如下标红的两个线程（对应slave的io线程和sql线程）状态为yes，表示主从复制配置成功. 其中，延迟可以查看Seconds_Behid_Master.

![img](https://img.mubu.com/document_image/892ae179-11d2-4b29-a90c-cb3500a6aeb9-862021.jpg)

检验在master创建数据库和表，添加数据等操作。在slave上刷新即可看到数据同步过来了。

![img](https://img.mubu.com/document_image/1d16398e-b6f5-4f89-a465-4f806620fb0f-862021.jpg)

## 主从同步原理

![img](https://img.mubu.com/document_image/f82c5fb3-0826-40d2-af7f-aab817b47d08-862021.jpg)

> \1.  master记录二进制日志。在每个事务更新数据完成之前，master在二日志记录这些改变。MySQL将事务串行的写入二进制日志，即使事务中的语句都是交叉执行的。在事件写入二进制日志完成后，master通知存储引擎提交事务
> \2.  slave将master的binary log拷贝到它自己的中继日志。首先，slave开始一个工作线程——I/O线程。I/O线程在master上打开一个普通的连接，然后开始binlog dump process。Binlog dump process从master的二进制日志中读取事件，如果已经跟上master，它会睡眠并等待master产生新的事件。I/O线程将这些事件写入中继日志
> \3. SQL线程从中继日志读取事件，并重放其中的事件而更新slave的数据，使其与master中的数据一致

### binlog

用来记录mysql的数据更新或者潜在更新（update xxx where id=x effect row 0）;

文件内容存储：/var/lib/mysql

查看binlog的内容：mysqlbinlog --base64-output=decode-rows -v mysql-bin.000001

![img](https://img.mubu.com/document_image/9bd5070e-6871-48ef-8a40-43a6613ae51b-862021.jpg)

#### binlog的格式

修改binlog_formater,通过在mysql客户端输入如下命令可以修改
set global binlog_format='row/mixed/statement';
或者在vim /etc/my.cnf  的[mysqld]下增加binlog_format='mixed'

statement ： 基于sql语句的模式。

row： 基于行模式; 存在1000条数据变更；记录修改以后每一条记录变化的值.

mixed: 混合模式，由mysql自动判断处理是使用statement还是row。

主从同步的延时问题

> 主从同步延迟是怎么产生
>
> \1. 当master库tps比较高的时候，产生的DDL数量超过slave一个sql线程所能承受的范围，或者slave的大型query语句产生锁等待
> \2. 网络传输： bin文件的传输延迟
> \3. 磁盘的读写耗时：文件通知更新、磁盘读取延迟、磁盘写入延迟
>
> 解决方案
>
> \1. 在数据库和应用层增加缓存处理，优先从缓存中读取数据
> \2. 减少slave同步延迟，可以修改slave库sync_binlog属性； 
> sync_binlog=0  执行事务不会马上刷新，文件系统来调度把binlog_cache刷新到磁盘。
> sync_binlog=n  （n>0） =1 每执行一次事务就刷新一次。
> \3. 增加延时监控
> Nagios做网络监控
> mk-heartbeat心跳做监控

# 七、mysql+keepalived（实现双主）（略）

![img](https://img.mubu.com/document_image/282a982d-5dc4-4f9e-a4ec-d555ba3888c1-862021.jpg)

主主服务器可以按上面的配置，拷贝。然后通过keepalived访问。

# 八、Mycat

![img](https://img.mubu.com/document_image/a3377d9c-29f5-4e94-bee9-c2e94b9278fe-862021.jpg)

> 开源的分布式数据库系统，是一个实现了 MySQL 协议的的 Server，前端用户可以把它看作是一个数据库代理，用 MySQL 客户端工具和命令行访问，而其后端可以用 MySQL 原生（Native）协议与多个 MySQL 服务器通信，也可以用 JDBC 协议与大多数主流数据库服务器通信， 其核心功能是分表分库，即将一个大表水平分割为 N 个小表，存储在后端 MySQL 服务器里或者其他数据库里。
>
> 类似的中间件还有：TDDL\Sharding-JDBC\COBAR。
>
> MyCAT 支持多种数据库接入，如：MySQL、SQLServer、Oracle、MongoDB 等，推荐使用 MySQL 做群。
>
> 分库分表后不影响应用层。

## 应用场景

 单纯的读写分离，此时配置最为简单，支持读写分离，主从切换 
 分表分库，对于超过 1000 万的表进行分片，最大支持 1000 亿的单表分片 
 多租户应用，每个应用一个库，但应用程序只连接 Mycat，从而不改造程序本身，实现多租户化 
 报表系统，借助于 Mycat 的分表能力，处理大规模报表的统计 
 替代 Hbase，分析大数据 
 作为海量数据实时查询的一种简单有效方案，比如 100 亿条频繁查询的记录需要在 3 秒内查询出来结果， 除了基于主键的查询，还可能存在范围查询或其他属性查询，此时 Mycat 可能是最简单有效的选择 

## mycat入门

> 下载源码启动
>
> 下载源码 <https://github.com/MyCATApache/>
>
> 源码调试与配置
> MyCAT 目前主要通过配置文件的方式来定义逻辑库和相关配置：
> • MYCAT_HOME/conf/schema.xml 中定义逻辑库，表、分片节点等内容.
> • MYCAT_HOME/conf/rule.xml 中定义分片规则.
> • MYCAT_HOME/conf/server.xml 中定义用户以及系统相关变量，如端口等.
> 注：以上几个文件的具体配置请参考前面章节中的具体说明.
>
> 源码运行
> MyCAT 入口程序是 org.opencloudb.MycatStartup.java，右键 run as .
> 需要设置MYCAT_HOME 目录，为你工程当前所在目录(src/main)：设置完 MYCAT 主目录后即可正常运行 MyCAT 服务。
> 注：
> 若启动报错，DirectBuffer 内存不够，则可以再加 JVM 系统参数：XX:MaxDirectMemorySize=128M。
> 若报错java.lang.illegalArgumentException:Invalid Datasource:0，则是schema.xml配置错误。你可能没有定义数据库dn1,dn2,dn3等dataNode节点。
>
> navicat连接mycat（localhost,8066,root/123456）
>
> ![img](https://img.mubu.com/document_image/ee513cc0-c9aa-4e76-a976-b882ef3432d0-862021.jpg)

## linux/windows下安装（略）

参考<http://dl.mycat.io/>

## 实战-单库大表拆分 - 水平分片

![img](https://img.mubu.com/document_image/99f465cb-0337-4d98-859d-4e5d1c04e72a-862021.jpg)

![img](https://img.mubu.com/document_image/02dfee1f-76e7-47d6-9cf1-e1f34c9eb0ac-862021.jpg)

> 1，135的数据库中添加数据库DB。
> 2，在DB上添加表order1，order2，order3
> 3，配置mycat的 ​schema.xml配置文件
> 4，启动mycat
> 5，验证：客户端登录mycat数据库 ，对表order插入数据，并查询。

## 实战-跨库分表

![img](https://img.mubu.com/document_image/4c6a2060-f623-47d1-aab5-d632baa1d99d-862021.jpg)

> 1，新建db2，db3数据库
> 2，如上配置
> 3，同样登录mycat数据库，往company​添加数据，验证数据。

## 实战-读写分离

![img](https://img.mubu.com/document_image/000e6aa9-9c2d-472e-9df1-20d97697e91f-862021.jpg)

> 这里的数据库主从是单向的，可以关注公众号“丁锅笔记”参考：分表分库（一）mysql的master-slave。
>
> 配置后验证：登录mycat的数据库，向company表插入多条数据。因为是单向的，所以这里的2个库的数据应该是一样的。



## RPM安装

```
---------安装
#mysql随机密码文件
/root/.mysql_secret
##安装
rpm -ivh /usr/twsm/install/mysql/MySQL-server-5.6.21-1.rhel5.x86_64.rpm --force
rpm -ivh /usr/twsm/install/mysql/MySQL-client-5.6.21-1.rhel5.x86_64.rpm --force
rpm -ivh /usr/twsm/install/mysql/MySQL-devel-5.6.21-1.rhel5.x86_64.rpm --force
yum install perl-Data-Dumper.x86_64
/usr/bin/mysql_install_db

---------启动
/usr/sbin/mysqld --defaults-file=/usr/my.cnf --user=root &

---------登录
 /usr/bin/mysql -uroot -p
 
---------修改密码
方法1： 用SET PASSWORD命令 
首先登录MySQL。 
格式：mysql> set password for 用户名@localhost = password('新密码'); 
例子：mysql> set password for root@localhost = password('123'); 

方法2：用mysqladmin 
格式：mysqladmin -u用户名 -p旧密码 password 新密码 
例子：mysqladmin -uroot -p123456 password 123 

方法3：用UPDATE直接编辑user表 
首先登录MySQL。 
mysql> use mysql; 
mysql> update user set password=password('123') where user='root' and host='localhost'; 
mysql> flush privileges; 

----------远程连接
update user set host='%' where user='root' and host='localhost';

----------mysql\user数据库不见了，用户密码修改后重启不生效。
/bin/sh /usr/bin/mysqld_safe --defaults-file=/usr/my.cnf --user=root --skip-grant-tables
启动后，执行：
use mysql
select * from user where user='' //如果有数据，那么你的问题基本就可以确定了
delete from user where user='';
flush privileges;  //重载权限表

```

主从复制：

https://www.jianshu.com/p/b0cf461451fb

```
innodb_flush_log_at_trx_commit
0: 由mysql的main_thread每秒将存储引擎log buffer中的redo日志写入到log file，并调用文件系统的sync操作，将日志刷新到磁盘。
1：每次事务提交时，将存储引擎log buffer中的redo日志写入到log file，并调用文件系统的sync操作，将日志刷新到磁盘。
2：每次事务提交时，将存储引擎log buffer中的redo日志写入到log file，并由存储引擎的main_thread 每秒将日志刷新到磁盘。

sync_binlog
默认，sync_binlog=0，表示MySQL不控制binlog的刷新，由文件系统自己控制它的缓存的刷新。这时候的性能是最好的，但是风险也是最大的。因为一旦系统Crash，在binlog_cache中的所有binlog信息都会被丢失。
如果sync_binlog>0，表示每sync_binlog次事务提交，MySQL调用文件系统的刷新操作将缓存刷下去。最安全的就是sync_binlog=1了，表示每次事务提交，MySQL都会把binlog刷下去，是最安全但是性能损耗最大的设置。这样的话，在数据库所在的主机操作系统损坏或者突然掉电的情况下，系统才有可能丢失1个事务的数据。但是binlog虽然是顺序IO，但是设置sync_binlog=1，多个事务同时提交，同样很大的影响MySQL和IO性能。虽然可以通过group commit的补丁缓解，但是刷新的频率过高对IO的影响也非常大。对于高并发事务的系统来说，“sync_binlog”设置为0和设置为1的系统写入性能差距可能高达5倍甚至更多。
所以很多MySQL DBA设置的sync_binlog并不是最安全的1，而是100或者是0。这样牺牲一定的一致性，可以获得更高的并发和性能。
```

```
1,修改配置
2，主：
#创建slave账号account，密码123456
mysql>grant replication slave on *.* to 'account'@'10.10.20.116' identified by '123456';
#更新数据库权限
mysql>flush privileges;
3，从：
#执行同步命令，设置主服务器ip，同步账号密码，同步位置
mysql>change master to master_host='10.10.20.111',master_user='account',master_password='123456',master_log_file='mysql-bin.000033',master_log_pos=337523;
#开启同步功能
mysql>start slave;

```

