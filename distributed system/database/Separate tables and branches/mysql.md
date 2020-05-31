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

# 主从复制

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

# sharding-jdbc

```
参考代码：

```



# 九、异常

```
Unable to lock ./ibdata1, error: 11
2020-04-19 11:27:19 45327 [Note] InnoDB: Check that you do not already have another mysqld process using the same InnoDB data or log files
----------------------
1、磁盘空间目录不足
2、ibdata1 文件被其他的进程占用

Cannot execute statement: impossible to write to binary log since statement is in row format and BINLOG_FORMAT = STATEMENT
————————————————
如果你采用默认隔离级别REPEATABLE-READ，那么建议binlog_format=ROW。如果你是READ-COMMITTED隔离级别，binlog_format=MIXED和binlog_format=ROW效果是一样的，binlog记录的格式都是ROW，对主从复制来说是很安全的参数。
set session binlog_format='MIXED';

```

# 十、MySQL 清除表空间碎片

```
碎片产生的原因
（1）表的存储会出现碎片化，每当删除了一行内容，该段空间就会变为空白、被留空，而在一段时间内的大量删除操作，会使这种留空的空间变得比存储列表内容所使用的空间更大；
（2）当执行插入操作时，MySQL会尝试使用空白空间，但如果某个空白空间一直没有被大小合适的数据占用，仍然无法将其彻底占用，就形成了碎片；
（3）当MySQL对数据进行扫描时，它扫描的对象实际是列表的容量需求上限，也就是数据被写入的区域中处于峰值位置的部分；
例如：
一个表有1万行，每行10字节，会占用10万字节存储空间，执行删除操作，只留一行，实际内容只剩下10字节，但MySQL在读取时，仍看做是10万字节的表进行处理，所以，碎片越多，就会越来越影响查询性能。

查看表碎片大小
（1）查看某个表的碎片大小
mysql> SHOW TABLE STATUS LIKE '表名';
结果中’Data_free’列的值就是碎片大小

（2）列出所有已经产生碎片的表
mysql> select table_schema db, table_name, data_free, engine     
from information_schema.tables 
where table_schema not in ('information_schema', 'mysql')  and data_free > 0;

清除表碎片
（1）MyISAM表
mysql> optimize table 表名

（2）InnoDB表
mysql> alter table 表名 engine=InnoDB
Engine不同,OPTIMIZE 的操作也不一样的,MyISAM 因为索引和数据是分开的,所以 OPTIMIZE 可以整理数据文件,并重排索引.
OPTIMIZE 操作会暂时锁住表,而且数据量越大,耗费的时间也越长,它毕竟不是简单查询操作.所以把 Optimize 命令放在程序中是不妥当的,不管设置的命中率多低,当访问量增大的时候,整体命中率也会上升,这样肯定会对程序的运行效率造成很大影响.比较好的方式就是做个shell,定期检查mysql中 information_schema.TABLES字段,查看 DATA_FREE 字段,大于0话,就表示有碎片

建议
清除碎片操作会暂时锁表，数据量越大，耗费的时间越长，可以做个脚本，定期在访问低谷时间执行，例如每周三凌晨，检查DATA_FREE字段，大于自己认为的警戒值的话，就清理一次。
```

# 十一、分片、分区、分表、分库

```
一、Sharding
Sharding 是把数据库横向扩展（Scale Out）到多个物理节点上的一种有效的方式，其主要目的是为突破单节点数据库服务器的 I/O 能力限制，解决数据库扩展性问题。Shard这个词的意思是“碎片”。如果将一个数据库当作一块大玻璃，将这块玻璃打碎，那么每一小块都称为数据库的碎片（DatabaseShard）。将整个数据库打碎的过程就叫做sharding，可以翻译为分片。

形式上，Sharding可以简单定义为将大数据库分布到多个物理节点上的一个分区方案。每一个分区包含数据库的某一部分，称为一个shard，分区方式可以是任意的，并不局限于传统的水平分区和垂直分区。一个shard可以包含多个表的内容甚至可以包含多个数据库实例中的内容。每个shard被放置在一个数据库服务器上。一个数据库服务器可以处理一个或多个shard的数据。系统中需要有服务器进行查询路由转发，负责将查询转发到包含该查询所访问数据的shard或shards节点上去执行。

二、Scale Out/Scale Up 和 垂直切分/水平拆分
Mysql的扩展方案包括Scale Out和Scale Up两种。

Scale Out（横向扩展）是指Application可以在水平方向上扩展。一般对数据中心的应用而言，Scale out指的是当添加更多的机器时，应用仍然可以很好的利用这些机器的资源来提升自己的效率从而达到很好的扩展性。


Scale Up（纵向扩展）是指Application可以在垂直方向上扩展。一般对单台机器而言，Scale Up值得是当某个计算节点（机器）添加更多的CPU Cores，存储设备，使用更大的内存时，应用可以很充分的利用这些资源来提升自己的效率从而达到很好的扩展性。

MySql的Sharding策略包括垂直切分和水平切分两种。

垂直(纵向)拆分：是指按功能模块拆分，以解决表与表之间的io竞争。比如分为订单库、商品库、用户库...这种方式多个数据库之间的表结构不同。

水平(横向)拆分：将同一个表的数据进行分块保存到不同的数据库中，来解决单表中数据量增长出现的压力。这些数据库中的表结构完全相同。

表结构设计垂直切分。常见的一些场景包括

a). 大字段的垂直切分。单独将大字段建在另外的表中，提高基础表的访问性能，原则上在性能关键的应用中应当避免数据库的大字段

b). 按照使用用途垂直切分。例如企业物料属性，可以按照基本属性、销售属性、采购属性、生产制造属性、财务会计属性等用途垂直切分

c). 按照访问频率垂直切分。例如电子商务、Web 2.0系统中，如果用户属性设置非常多，可以将基本、使用频繁的属性和不常用的属性垂直切分开

表结构设计水平切分。常见的一些场景包括
a). 比如在线电子商务网站，订单表数据量过大，按照年度、月度水平切分

b). Web 2.0网站注册用户、在线活跃用户过多，按照用户ID范围等方式，将相关用户以及该用户紧密关联的表做水平切分

c). 例如论坛的置顶帖子，因为涉及到分页问题，每页都需要显示置顶贴，这种情况可以把置顶贴水平切分开来，避免取置顶帖子时从所有帖子的表中读取

三、分表和分区
分表从表面意思说就是把一张表分成多个小表，分区则是把一张表的数据分成N多个区块，这些区块可以在同一个磁盘上，也可以在不同的磁盘上。

分表和分区的区别

1，实现方式上 

mysql的分表是真正的分表，一张表分成很多表后，每一个小表都是完正的一张表，都对应三个文件（MyISAM引擎：一个.MYD数据文件，.MYI索引文件，.frm表结构文件）。

2，数据处理上 

分表后数据都是存放在分表里，总表只是一个外壳，存取数据发生在一个一个的分表里面。分区则不存在分表的概念，分区只不过把存放数据的文件分成了许多小块，分区后的表还是一张表，数据处理还是由自己来完成。

3，提高性能上 

 分表后，单表的并发能力提高了，磁盘I/O性能也提高了。分区突破了磁盘I/O瓶颈，想提高磁盘的读写能力，来增加mysql性能。 

在这一点上，分区和分表的测重点不同，分表重点是存取数据时，如何提高mysql并发能力上；而分区呢，如何突破磁盘的读写能力，从而达到提高mysql性能的目的。 

4，实现的难易度上 

分表的方法有很多，用merge来分表，是最简单的一种方式。这种方式和分区难易度差不多，并且对程序代码来说可以做到透明的。如果是用其他分表方式就比分区麻烦了。 分区实现是比较简单的，建立分区表，跟建平常的表没什么区别，并且对代码端来说是透明的。 

分区的适用场景

1. 一张表的查询速度已经慢到影响使用的时候。

2. 表中的数据是分段的

3. 对数据的操作往往只涉及一部分数据，而不是所有的数据


CREATE TABLE sales (
    id INT AUTO_INCREMENT,
    amount DOUBLE NOT NULL,
    order_day DATETIME NOT NULL,
    PRIMARY KEY(id, order_day)
) ENGINE=Innodb 
PARTITION BY RANGE(YEAR(order_day)) (
    PARTITION p_2010 VALUES LESS THAN (2010),
    PARTITION p_2011 VALUES LESS THAN (2011),
    PARTITION p_2012 VALUES LESS THAN (2012),
PARTITION p_catchall VALUES LESS THAN MAXVALUE);
分表的适用场景

1. 一张表的查询速度已经慢到影响使用的时候。

2. 当频繁插入或者联合查询时，速度变慢。

分表的实现需要业务结合实现和迁移，较为复杂。

四、分表和分库
分表能够解决单表数据量过大带来的查询效率下降的问题，但是，却无法给数据库的并发处理能力带来质的提升。面对高并发的读写访问，当数据库master服务器无法承载写操作压力时，不管如何扩展slave服务器，此时都没有意义了。因此，我们必须换一种思路，对数据库进行拆分，从而提高数据库写入能力，这就是所谓的分库。

与分表策略相似，分库可以采用通过一个关键字取模的方式，来对数据访问进行路由，如下图所示

五、分库分表存在的问题
1 事务问题。

在执行分库分表之后，由于数据存储到了不同的库上，数据库事务管理出现了困难。如果依赖数据库本身的分布式事务管理功能去执行事务，将付出高昂的性能代价；如果由应用程序去协助控制，形成程序逻辑上的事务，又会造成编程方面的负担。

2 跨库跨表的join问题。

在执行了分库分表之后，难以避免会将原本逻辑关联性很强的数据划分到不同的表、不同的库上，这时，表的关联操作将受到限制，我们无法join位于不同分库的表，也无法join分表粒度不同的表，结果原本一次查询能够完成的业务，可能需要多次查询才能完成。

3 额外的数据管理负担和数据运算压力。

额外的数据管理负担，最显而易见的就是数据的定位问题和数据的增删改查的重复执行问题，这些都可以通过应用程序解决，但必然引起额外的逻辑运算，例如，对于一个记录用户成绩的用户数据表userTable，业务要求查出成绩最好的100位，在进行分表之前，只需一个order by语句就可以搞定，但是在进行分表之后，将需要n个order by语句，分别查出每一个分表的前100名用户数据，然后再对这些数据进行合并计算，才能得出结果。

解决方案

1. 使用类似JTA提供的分布式事物机制
```

# 十二、Mysql优化

参考文献：

http://blog.sae.sina.com.cn/archives/3352

https://cloud.tencent.com/developer/article/1056283

https://blog.csdn.net/yang1982_0907/article/details/20123055

https://zhuanlan.zhihu.com/p/55947158

```
表状态 - 表碎片
-----------
SHOW TABLE STATUS LIKE '表名'; 

连接数
-----------
show variables like 'max_connections' #数据库的最大连接数
show global status like 'Max_used_connections'; #已发生的连接情况
Max_used_connections / max_connections * 100% ≈ 85% #最好的情况

慢查询
-----------
show variables like '%slow%' ; #是否开启慢查询
show global status like '%slow%'; # 目前的状态

MyISAM --- Key_buffer_size(指定用于索引的缓冲区大小，增加它可得到更好处理的索引(对所有读和多重写))
-----------
show variables like 'key_buffer_size';
show global status like 'key_read%';
show global status like 'key_blocks_u%';

Key_read_requests：从缓存读取索引的请求次数。
Key_reads：从磁盘读取索引的请求次数。

key_cache_miss_rate ＝ Key_reads / Key_read_requests * 100%
比如上面的数据，key_cache_miss_rate为0.0244%，4000个索引读取请求才有一个直接读硬盘，已经很BT了，key_cache_miss_rate在0.1%以下都很好（每1000个请求有一个直接读硬盘），如果key_cache_miss_rate在0.01%以下的话，key_buffer_size分配的过多，可以适当减少

Key_blocks_used / (Key_blocks_unused + Key_blocks_used) * 100% ≈ 80%
Key_blocks_unused表示未使用的缓存簇(blocks)数，Key_blocks_used表示曾经用到的最大的blocks数，比如这台服务器，所有的缓存都用到了，要么增加key_buffer_size，要么就是过渡索引了，把缓存占满了.

Innodb  --- Innodb_buffer_pool_size (指定用于索引的缓冲区大小，增加它可得到更好处理的索引(对所有读和多重写))
------------
show variables like '%innodb_buffer_pool_size';
show status like  'Innodb_buffer_pool_%';
| Innodb_buffer_pool_dump_status        | not started |
| Innodb_buffer_pool_load_status        | not started |
| Innodb_buffer_pool_pages_data         | 574         |
| Innodb_buffer_pool_bytes_data         | 9404416     |
| Innodb_buffer_pool_pages_dirty        | 0           |
| Innodb_buffer_pool_bytes_dirty        | 0           |
| Innodb_buffer_pool_pages_flushed      | 230         |
| Innodb_buffer_pool_pages_free         | 7616        |
| Innodb_buffer_pool_pages_misc         | 1           |
| Innodb_buffer_pool_pages_total        | 8191        |
| Innodb_buffer_pool_read_ahead_rnd     | 0           |
| Innodb_buffer_pool_read_ahead         | 0           |
| Innodb_buffer_pool_read_ahead_evicted | 0           |
| Innodb_buffer_pool_read_requests      | 263613      | #总读取
| Innodb_buffer_pool_reads              | 448         | #磁盘命中
| Innodb_buffer_pool_wait_free          | 0           |
| Innodb_buffer_pool_write_requests     | 42026       

Innodb --- innodb_log_buffer_size 参数的使用,这个参数就是用来设置 Innodb 的 Log Buffer 大小的，系统默认值为 1MB。Log  Buffer 的主要作用就是缓冲 Log 数据，提高写 Log 的 IO 性能。一般来说，如果你的系统不是写负载非常高且以 大事务居多的话，8MB 以内的大小就完全足够了。
-------------
show status like 'innodb_log%';
+---------------------------+-------+
| Variable_name             | Value |
+---------------------------+-------+
| Innodb_log_waits          | 0     |
| Innodb_log_write_requests | 5183  |
| Innodb_log_writes         | 30    |
+---------------------------+-------+

临时表tmp_table_size/max_heap_table_size
-------------
show global status like 'created_tmp%';

每次创建临时表，Created_tmp_tables增加，如果是在磁盘上创建临时表，Created_tmp_disk_tables也增加,Created_tmp_files表示MySQL服务创建的临时文件文件数，比较理想的配置是：
Created_tmp_disk_tables / Created_tmp_tables * 100% <= 25%
比如上面的服务器Created_tmp_disk_tables / Created_tmp_tables * 100% ＝ 1.20%，应该相当好了。我们再看一下MySQL服务器对临时表的配置。
show variables where Variable_name in ('tmp_table_size', 'max_heap_table_size');
只有256MB以下的临时表才能全部放内存，超过的就会用到硬盘临时表。

打开表table_cache
-------------
show global status like 'open%table%'
show variables like 'table_cache';

Open_tables:当前用缓存打开表的数量。
Opened_tables:曾经打开表的缓存数，会一直累加。
Open_tables表示打开表的数量，Opened_tables表示打开过的表数量，如果Opened_tables数量过大，说明配置中table_cache(5.1.3之后这个值叫做table_open_cache)值可能太小，我们查询一下服务器table_cache值。

验证：
执行flush tables后，open_tables会清0，opened_tables则不会。因为flush_tables后，mysql会关闭打开的缓存表。

thread_cache_size(当客户端断开连接后 将当前线程缓存起来 当在接到新的连接请求时快速响应 无需创建新的线程 )
----------------
show global status like 'Thread%';
show variables like 'thread_cache_size';

在MySQL服务器配置文件中设置了thread_cache_size，当客户端断开之后，服务器处理此客户的线程将会缓存起来以响应下一个客户而不是销毁（前提是缓存数未达上限）。Threads_created表示创建过的线程数，如果发现Threads_created值过大的话，表明MySQL服务器一直在创建线程，这也是比较耗资源，可以适当增加配置文件中thread_cache_size值，查询服务器thread_cache_size配置

Threads_cached :代表当前此时此刻线程缓存中有多少空闲线程。
Threads_connected :代表当前已建立连接的数量，因为一个连接就需要一个线程，所以也可以看成当前被使用的线程数。
Threads_created :代表从最近一次服务启动，已创建线程的数量。
Threads_running :代表当前激活的（非睡眠状态）线程数。并不是代表正在使用的线程数，有时候连接已建立，但是连接处于sleep状态，这里相对应的线程也是sleep状态。

查询缓存(query cache)
----------------
mysql> SHOW STATUS LIKE 'Qcache%';
+-------------------------+--------+
| Variable_name           | Value  |
+-------------------------+--------+
| Qcache_free_blocks      | 1      | ----在查询缓存中的闲置块，如果该值比较大，则说明Query Cache中的内存碎片可能比较多。FLUSH QUERY CACHE会对缓存中的碎片进行整理，从而得到一个较大的空闲内存块。
| Qcache_free_memory      | 382704 | ----剩余缓存的大小
| Qcache_hits             | 198    | ----缓存命中次数
| Qcache_inserts          | 131    | ----缓存被插入的次数，也就是查询没有命中的次数。
| Qcache_lowmem_prunes    | 0      | ----由于内存低而被删除掉的缓存条数，如果这个数值在不断增长，那么一般是Query Cache的空闲内存不足（通过Qcache_free_memory判断），或者内存碎片较严重（通过Qcache_free_blocks判断）。
| Qcache_not_cached       | 169    | ----没有被缓存的条数，有三种情况会导致查询结果不会被缓存：其一，由于query_cache_type的设置；其二，查询不是SELECT语句；其三，使用了now()之类的函数，导致查询语句一直在变化。
| Qcache_queries_in_cache | 128    | ----缓存中有多少条查询语句
| Qcache_total_blocks     | 281    | ----总块数
+-------------------------+--------+
mysql> show variables like ‘query_cache%‘;
+------------------------------+---------+
| Variable_name                | Value   |
+------------------------------+---------+
| have_query_cache             | YES     |      --查询缓存是否可用
| query_cache_limit            | 1048576 |      --可缓存具体查询结果的最大值
| query_cache_min_res_unit     | 4096    |      --查询缓存分配的最小块的大小(字节)
| query_cache_size             | 599040  |      --查询缓存的大小
| query_cache_type             | ON      |      --是否支持查询缓存
| query_cache_wlock_invalidate | OFF     |      --控制当有写锁加在表上的时候，是否先让该表相关的 Query Cache失效

排序使用情况
-----------------
mysql> show global status like 'sort%';
+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| Sort_merge_passes | 0     |
| Sort_range        | 0     |
| Sort_rows         | 1573  |
| Sort_scan         | 25    |
+-------------------+-------+
Sort_merge_passes 包括两步。MySQL 首先会尝试在内存中做排序，使用的内存大小由系统变量 Sort_buffer_size 决定，如果它的大小不够把所有的记录都读到内存中，MySQL 就会把每次在内存中排序的结果存到临时文件中，等 MySQL 找到所有记录之后，再把临时文件中的记录做一次排序。这再次排序就会增加 Sort_merge_passes。实际上，MySQL 会用另一个临时文件来存再次排序的结果，所以通常会看到 Sort_merge_passes 增加的数值是建临时文件数的两倍。因为用到了临时文件，所以速度可能会比较慢，增加 Sort_buffer_size 会减少 Sort_merge_passes 和 创建临时文件的次数。但盲目的增加 Sort_buffer_size 并不一定能提高速度

文件打开数(open_files)
-----------------
show global status like 'open_files';

表锁情况
-----------------
show global status like 'table_locks%';
+-----------------------+-------+
| Variable_name         | Value |
+-----------------------+-------+
| Table_locks_immediate | 235   |
| Table_locks_waited    | 0     |
+-----------------------+-------+
Table_locks_immediate / Table_locks_waited > 5000，最好

表扫描情况
-----------------
mysql> show global status like 'handler_read%';
+-----------------------+--------+
| Variable_name         | Value  |
+-----------------------+--------+
| Handler_read_first    | 55     |
| Handler_read_key      | 36     |
| Handler_read_last     | 0      |
| Handler_read_next     | 4      |
| Handler_read_prev     | 0      |
| Handler_read_rnd      | 1583   |
| Handler_read_rnd_next | 266580 |
+-----------------------+--------+
7 rows in set (0.00 sec)
mysql>  show global status like 'com_select';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| Com_select    | 209   |
+---------------+-------+
1 row in set (0.00 sec)
表扫描率 ＝ Handler_read_rnd_next / Com_select
如果表扫描率超过4000，说明进行了太多表扫描，很有可能索引没有建好，增加read_buffer_size值会有一些好处，但最好不要超过8MB.(read_buffer_size：是MySQL读入缓冲区大小。对表进行顺序扫描的请求将分配一个读入缓冲区，MySQL会为它分配一段内存缓冲区。read_buffer_size变量控制这一缓冲区的大小。如果对表的顺序扫描请求非常频繁，并且你认为频繁扫描进行得太慢，可以通过增加该变量值以及内存缓冲区大小提高其性能)

```

缓存查询的流程：

```
1) 读查询开始之前必须检查是否命中缓存。
2) 如果读查询可以缓存，那么执行完查询操作后，会查询结果和查询语句写入缓存。
3) 当向某个表写入数据的时候，必须将这个表所有的缓存设置为失效，如果缓存空间很大，则消耗也会很大，可能使系统僵死一段时间，因为这个操作是靠全局锁操作来保护的。
4) 对InnoDB表，当修改一个表时，设置了缓存失效，但是多版本特性会暂时将这修改对其他事务屏蔽，在这个事务提交之前，所有查询都无法使用缓存，直到这个事务被提交，所以长时间的事务，会大大降低查询缓存的命中
```

![img](https://pic3.zhimg.com/80/v2-0319cbb300dd86154f26bcce8b64a496_720w.jpg)

# 十三、MySQL Query Cache碎片优化

```
没有什么办法能够完全避免碎片，但是选择合适的query_cache_min_res_unit可以帮你减少由碎片导致的内存空间浪费。这个值太小，则浪费的空间更少，但是会导致频繁的内存块申请操作；如果设置得太大，那么碎片会很多。调整合适的值其实是在平衡内存浪费和CPU消耗。可以通过内存实际消耗（query_cache_size - Qcache_free_memory）除以Qcache_queries_in_cahce计算单个查询的平均缓存大小。可以通过Qcahce_free_blocks来观察碎片。

通过FLUSH_QUERY_CAHCE完成碎片整理，这个命令将所有的查询缓存重新排序，并将所有的空闲空间都聚焦到查询缓存的一块区域上。
```



# 十四、explain\show profiles

```
1，id：from表 越大越先加载。相同顺序加载
2，select_type：from表类型
3，table
4，type：system>const>eq_ref>ref>range>index>all
5，possible_keys:
6，key
7，key_len
8，ref
9，rows
10，extra：using filesort\using temporary\using index等

set profiling=on;  #profile默认关闭，生产环境中也建议关闭。
mysql> show profiles;
+----------+------------+-------------------------------------------------------------------------+
| Query_ID | Duration   | Query                                                                   |
+----------+------------+-------------------------------------------------------------------------+
|        1 | 0.00045250 | select * from user_log where user_id like '2186%'                       |
|        2 | 0.00747275 | select * from user_log where user_id like '%2186%' order by cat_id desc |
+----------+------------+-------------------------------------------------------------------------+
2 rows in set, 1 warning (0.00 sec)
mysql> show profile cpu,block io for query 1;
+----------------------+----------+----------+------------+--------------+---------------+
| Status               | Duration | CPU_user | CPU_system | Block_ops_in | Block_ops_out |
+----------------------+----------+----------+------------+--------------+---------------+
| starting             | 0.000108 | 0.000020 |   0.000079 |            0 |             0 |
| checking permissions | 0.000011 | 0.000002 |   0.000007 |            0 |             0 |
| Opening tables       | 0.000019 | 0.000004 |   0.000015 |            0 |             0 |
| init                 | 0.000025 | 0.000005 |   0.000020 |            0 |             0 |
| System lock          | 0.000010 | 0.000002 |   0.000007 |            0 |             0 |
| optimizing           | 0.000008 | 0.000002 |   0.000006 |            0 |             0 |
| statistics           | 0.000045 | 0.000009 |   0.000037 |            0 |             0 |
| preparing            | 0.000013 | 0.000003 |   0.000009 |            0 |             0 |
| executing            | 0.000003 | 0.000000 |   0.000003 |            0 |             0 |
| Sending data         | 0.000131 | 0.000028 |   0.000104 |            0 |             0 |
| end                  | 0.000006 | 0.000001 |   0.000005 |            0 |             0 |
| query end            | 0.000007 | 0.000001 |   0.000005 |            0 |             0 |
| closing tables       | 0.000008 | 0.000002 |   0.000006 |            0 |             0 |
| freeing items        | 0.000046 | 0.000009 |   0.000037 |            0 |             0 |
| cleaning up          | 0.000015 | 0.000003 |   0.000011 |            0 |             0 |
+----------------------+----------+----------+------------+--------------+---------------+
15 rows in set, 1 warning (0.00 sec)

慢日志记录
----------------
slow_query_log=1;											//开启慢查询日志
slow_query_log_file="/usr/local/mysql/data/"    			//慢查询如日存放的路径
long_query_time=3;											//慢查询SQL记录的时间
log_output=FILE												//以文件方式记录
```

# 十五、索引

```
1，最佳左前缀法则
2，!=\is null\like\or\不加单引号的字符串\索引列上计算 等索引失效
3，尽量使用覆盖索引
```

# 十六、查询优化

```
1，小表驱动大表
2，order by 用索引 调整max_length_for_sort_data\sort_buffer_size
3，group by 用索引 调整max_length_for_sort_data\sort_buffer_size
```

# 十七、进阶-原理分析

## 读写的流程、锁、事务

![img](https://static001.geekbang.org/resource/image/0d/d9/0d2070e8f84c4801adbfa03bda1f98d9.png)

![img](http://www.ywnds.com/wp-content/uploads/2017/02/2017022105591128.jpg)

![img](http://www.ywnds.com/wp-content/uploads/2017/02/2017022105594116.jpg)

![img](http://www.ywnds.com/wp-content/uploads/2017/02/2017022106001249.png)

![img](https://static001.geekbang.org/resource/image/9e/3e/9ed86644d5f39efb0efec595abb92e3e.png)



```
------------mysql查执行顺序如下-------
1，连接器
mysql> show processlist; 查看连接的进程
2，查询缓存
一个系统配置表，那这张表上的查询才适合使用查询缓存.
MySQL 8.0 版本直接将查询缓存的整块功能删掉了，也就是说 8.0 开始彻底没有这个功能了
mysql> select SQL_CACHE * from T where ID=10；
3，分析器
4，优化器
5，执行器

-------------mysql写操作-------------
1、先写undo log。
2、在内存更新数据，这步操作就在内存中形成了脏页，如果脏页过多，checkpoint机制进行刷新，innodb_max_dirty_pages_pct决定了刷新脏页比例。innodb_io_capacity参数可以动态调整刷新脏页的数量，innodb_lru_scan_depth这个参数决定了刷新每个innodb_buffer_pool的脏页数量。
3、记录变更到redo log，prepare这里会写事务id。innodb_flush_log_at_trx_commit决定了事务的刷盘方式。
为0时，log buffer将每秒一次地写入log file中，并且log file的flush(刷到磁盘)操作同时进行。该模式下，在事务提交的时候，不会主动触发写入磁盘的操作。
为1，每次事务提交时MySQL都会把log buffer的数据写入log file，并且flush(刷到磁盘)中去.
为2，每次事务提交时MySQL都会把log buffer的数据写入log file.但是flush(刷到磁盘)操作并不会同时进行。该模式下，MySQL会每秒执行一次 flush(刷到磁盘)操作。
4、写入binlog这里会写入一个事务id这里有个sync_binlog参数决定多个事务进行一次性提交。
5、redo log第二阶段，这里会进行判断前2步是否成功，成功则默认commit，否则rollback。刷入磁盘操作。这里是先从脏页数据刷入到内存2M大小的doublewrite buffer，然后是一次性从内存的doublewrite buffer刷新到共享表空间的doublewrite buffer，这里产生了一次IO。然后从内存的内存的doublewrite buffer刷新2m数据到磁盘的ibd文件中，这里需要发生128次io。然后校验，如果不一致，就由共享表空间的副本进行修复。这里有个参数innodb_flush_method决定了数据刷新直接刷新到磁盘，绕过os cache。
6、返回给client。
如果有slave，第4步之后经过slave服务线程io_thread写到从库的relay log ，再由sql thread应用relay log到从库中。

---------------binlog写入机制-----------
事务执行过程中，先把日志写到 binlog cache，事务提交的时候，再把 binlog cache 写到 binlog 文件中。一个事务的 binlog 是不能被拆开的，因此不论这个事务多大，也要确保一次性写入。这就涉及到了 binlog cache 的保存问题。系统给 binlog cache 分配了一片内存，每个线程一个，参数 binlog_cache_size 用于控制单个线程内 binlog cache 所占内存的大小。如果超过了这个参数规定的大小，就要暂存到磁盘。事务提交的时候，执行器把 binlog cache 里的完整事务写入到page cache（write），然后fsync到 binlog磁盘中，并清空 binlog cache。
write 和 fsync 的时机，是由参数 sync_binlog 控制的：sync_binlog=0 的时候，表示每次提交事务都只 write，不 fsync；sync_binlog=1 的时候，表示每次提交事务都会执行 fsync；sync_binlog=N(N>1) 的时候，表示每次提交事务都 write，但累积 N 个事务后才 fsync。因此，在出现 IO 瓶颈的场景里，将 sync_binlog 设置成一个比较大的值，可以提升性能。在实际的业务场景中，考虑到丢失日志量的可控性，一般不建议将这个参数设成 0，比较常见的是将其设置为 100~1000 中的某个数值。但是，将 sync_binlog 设置为 N，对应的风险是：如果主机发生异常重启，会丢失最近 N 个事务的 binlog 日志。

----------------redo.log的写入机制----------------
事务在执行过程中，生成的 redo log 是要先写到 redo log buffer 的，再写入到page cache（write），然后fsync到 redolog磁盘中.

为了控制 redo log 的写入策略，InnoDB 提供了 innodb_flush_log_at_trx_commit 参数，它有三种可能取值：设置为 0 的时候，表示每次事务提交时都只是把 redo log 留在 redo log buffer 中 ;设置为 1 的时候，表示每次事务提交时都将 redo log 直接持久化到磁盘；设置为 2 的时候，表示每次事务提交时都只是把 redo log 写到 page cache。InnoDB 有一个后台线程，每隔 1 秒，就会把 redo log buffer 中的日志，调用 write 写到文件系统的 page cache，然后调用 fsync 持久化到磁盘。

提升 binlog 组提交的效果，可以通过设置 binlog_group_commit_sync_delay 和 binlog_group_commit_sync_no_delay_count 来实现。binlog_group_commit_sync_delay 参数，表示延迟多少微秒后才调用 fsync;binlog_group_commit_sync_no_delay_count 参数，表示累积多少次以后才调用 fsync。这两个条件是或的关系，也就是说只要有一个满足条件就会调用 fsync。所以，当 binlog_group_commit_sync_delay 设置为 0 的时候，binlog_group_commit_sync_no_delay_count 也无效了。

如果你的 MySQL 现在出现了性能瓶颈，而且瓶颈在 IO 上，可以通过哪些方法来提升性能呢？针对这个问题，可以考虑以下三种方法：
设置 binlog_group_commit_sync_delay 和 binlog_group_commit_sync_no_delay_count 参数，减少 binlog 的写盘次数。这个方法是基于“额外的故意等待”来实现的，因此可能会增加语句的响应时间，但没有丢失数据的风险。
将 sync_binlog 设置为大于 1 的值（比较常见是 100~1000）。这样做的风险是，主机掉电时会丢 binlog 日志。
将 innodb_flush_log_at_trx_commit 设置为 2。这样做的风险是，主机掉电的时候会丢数据。

-----------抖一下mysql---------------
当内存数据页跟磁盘数据页内容不一致的时候，我们称这个内存页为“脏页”。内存数据写入到磁盘后，内存和磁盘上的数据页的内容就一致了，称为“干净页”。
平时执行很快的更新操作，其实就是在写内存和日志，而 MySQL 偶尔“抖”一下的那个瞬间，可能就是在刷脏页（flush）。
对应的就是 InnoDB 的 redo log 写满了。这时候系统会停止所有更新操作，把 checkpoint 往前推进，redo log 留出空间可以继续写。
对应的就是系统内存不足。当需要新的内存页，而内存不够用的时候，就要淘汰一些数据页，空出内存给别的数据页使用。如果淘汰的是“脏页”，就要先将脏页写到磁盘。
要合理地安排时间，即使是“生意好”的时候，也要见缝插针地找时间，只要有机会就刷一点“脏页”。
对应的就是 MySQL 正常关闭的情况。这时候，MySQL 会把内存的脏页都 flush 到磁盘上，这样下次 MySQL 启动的时候，就可以直接从磁盘上读数据，启动速度会很快。
```

![img](https://static001.geekbang.org/resource/image/2e/be/2e5bff4910ec189fe1ee6e2ecc7b4bbe.png)

![img](https://static001.geekbang.org/resource/image/16/a7/16a7950217b3f0f4ed02db5db59562a7.png)

```
mysql的日志：binlog、redo
将 redo log 的写入拆成了两个步骤：prepare 和 commit，这就是"两阶段提交"。

redo log 是 InnoDB 引擎特有的日志，而 Server 层也有自己的日志，称为 binlog（归档日志）。

redo log 是 InnoDB 引擎特有的；binlog 是 MySQL 的 Server 层实现的，所有引擎都可以使用。

redo log 是物理日志，记录的是“在某个数据页上做了什么修改”；binlog 是逻辑日志，记录的是这个语句的原始逻辑，比如“给 ID=2 这一行的 c 字段加 1 ”。

redo log 是循环写的，空间固定会用完；binlog 是可以追加写入的。“追加写”是指 binlog 文件写到一定大小后会切换到下一个，并不会覆盖以前的日志。

Redo log不是记录数据页“更新之后的状态”，而是记录这个页 “做了什么改动”。

Binlog有两种模式，statement 格式的话是记sql语句， row格式会记录行的内容，记两条，更新前和更新后都有。
```

![img](https://static001.geekbang.org/resource/image/d9/ee/d9c313809e5ac148fc39feff532f0fee.png)

```
事务实现逻辑：
------------------
在实现上，数据库里面会创建一个视图，访问的时候以视图的逻辑结果为准。在“可重复读”隔离级别下，这个视图是在事务启动时创建的，整个事务存在期间都用这个视图。在“读提交”隔离级别下，这个视图是在每个 SQL 语句开始执行的时候创建的。这里需要注意的是，“读未提交”隔离级别下直接返回记录上的最新值，没有视图概念；而“串行化”隔离级别下直接用加锁的方式来避免并行访问。

长事务
------------------
实际上每条记录在更新的时候都会同时记录一条回滚操作。记录上的最新值，通过回滚操作，都可以得到前一个状态的值。
长事务意味着系统里面会存在很老的事务视图。由于这些事务随时可能访问数据库里面的任何数据，所以这个事务提交之前，数据库里面它可能用到的回滚记录都必须保留，这就会导致大量占用存储空间。对回滚段的影响，长事务还占用锁资源，也可能拖垮整个库。
你可以在 information_schema 库的 innodb_trx 这个表中查询长事务，比如下面这个语句，用于查找持续时间超过 60s 的事务：
select * from information_schema.innodb_trx where TIME_TO_SEC(timediff(now(),trx_started))>60

如何避免长事务对业务的影响？这个问题，我们可以从应用开发端和数据库端来看。
首先，从应用开发端来看：确认是否使用了 set autocommit=0。这个确认工作可以在测试环境中开展，把 MySQL 的 general_log 开起来，然后随便跑一个业务逻辑，通过 general_log 的日志来确认。
一般框架如果会设置这个值，也就会提供参数来控制行为，你的目标就是把它改成 1。确认是否有不必要的只读事务。有些框架会习惯不管什么语句先用 begin/commit 框起来。我见过有些是业务并没有这个需要，但是也把好几个 select 语句放到了事务中。这种只读事务可以去掉。
业务连接数据库的时候，根据业务本身的预估，通过 SET MAX_EXECUTION_TIME 命令，来控制每个语句执行的最长时间，避免单个语句意外执行太长时间。（为什么会意外？在后续的文章中会提到这类案例）.
其次，从数据库端来看：
监控 information_schema.Innodb_trx 表，设置长事务阈值，超过就报警 / 或者 kill；Percona 的 pt-kill 这个工具不错，推荐使用；
在业务功能测试阶段要求输出所有的 general_log，分析日志行为提前发现问题；
如果使用的是 MySQL  5.6 或者更新版本，把 innodb_undo_tablespaces 设置成 2（或更大的值）。如果真的出现大事务导致回滚段过大，这样设置后清理起来更方便.
mysql> select * from information_schema.innodb_trx;
+--------+-----------+---------------------+-----------------------+------------------+------------+---------------------+-----------+---------------------+-------------------+-------------------+------------------+-----------------------+-----------------+-------------------+-------------------------+---------------------+-------------------+------------------------+----------------------------+---------------------------+---------------------------+------------------+----------------------------+
| trx_id | trx_state | trx_started         | trx_requested_lock_id | trx_wait_started | trx_weight | trx_mysql_thread_id | trx_query | trx_operation_state | trx_tables_in_use | trx_tables_locked | trx_lock_structs | trx_lock_memory_bytes | trx_rows_locked | trx_rows_modified | trx_concurrency_tickets | trx_isolation_level | trx_unique_checks | trx_foreign_key_checks | trx_last_foreign_key_error | trx_adaptive_hash_latched | trx_adaptive_hash_timeout | trx_is_read_only | trx_autocommit_non_locking |
+--------+-----------+---------------------+-----------------------+------------------+------------+---------------------+-----------+---------------------+-------------------+-------------------+------------------+-----------------------+-----------------+-------------------+-------------------------+---------------------+-------------------+------------------------+----------------------------+---------------------------+---------------------------+------------------+----------------------------+
| 11137  | RUNNING   | 2020-04-27 11:18:13 | NULL                  | NULL             |          0 |                   3 | NULL      | NULL                |                 0 |                 0 |                0 |                   360 |               0 |                 0 |                       0 | READ COMMITTED      |                 1 |                      1 | NULL                       |                         0 |                     10000 |                0 |                          0 |
+--------+-----------+---------------------+-----------------------+------------------+------------+---------------------+-----------+---------------------+-------------------+-------------------+------------------+-----------------------+-----------------+-------------------+-------------------------+---------------------+-------------------+------------------------+----------------------------+---------------------------+---------------------------+------------------+----------------------------+
1 row in set (0.00 sec)
mysql> kill 3;
Query OK, 0 rows affected (0.00 sec)


事务隔离级别	脏读	不可重复读	幻读
读未提交（read-uncommitted）	是	是	是
不可重复读（read-committed）	否	是	是
可重复读（repeatable-read）	否	否	是
串行化（serializable）	否	否	否

使用命令：SET session TRANSACTION ISOLATION LEVEL Serializable;（参数可以为：Read uncommitted，Read committed，Repeatable，Serializable）

幻读的验证：
不能两个客户端都在事务里头；
插入的客户端要先查一遍，处在事务中的客户端才能出现幻读。
设置为serializable后，插入数据的客户端会阻塞。

Read uncommitted，Read committed的隔离级别要修改：
set session binlog_format='MIXED';否则报错。


事务默认隔离级别：
-------------------
mysql> show variables like 'tx_%';
+---------------+-----------------+
| Variable_name | Value           |
+---------------+-----------------+
| tx_isolation  | REPEATABLE-READ |
| tx_read_only  | OFF             |
+---------------+-----------------+
2 rows in set (0.00 sec)

在 MySQL 里，有两个“视图”的概念：
一个是 view。它是一个用查询语句定义的虚拟表，在调用的时候执行查询语句并生成结果。创建视图的语法是 create view … ，而它的查询方法与表一样。
另一个是 InnoDB 在实现 MVCC 时用到的一致性读视图，即 consistent read view，用于支持 RC（Read Committed，读提交）和 RR（Repeatable Read，可重复读）隔离级别的实现。

InnoDB 里面每个事务有一个唯一的事务 ID，叫作 transaction id。它是在事务开始的时候向 InnoDB 的事务系统申请的，是按申请顺序严格递增的。而每行数据也都是有多个版本的。每次事务更新数据的时候，都会生成一个新的数据版本，并且把 transaction id 赋值给这个数据版本的事务 ID，记为 row trx_id。同时，旧的数据版本要保留，并且在新的数据版本中，能够有信息可以直接拿到它。
实际上，图 2 中的三个虚线箭头，就是 undo log；而 V1、V2、V3 并不是物理上真实存在的，而是每次需要的时候根据当前版本和 undo log 计算出来的。比如，需要 V2 的时候，就是通过 V4 依次执行 U3、U2 算出来。

在实现上， InnoDB 为每个事务构造了一个数组，用来保存这个事务启动瞬间，当前正在“活跃”的所有事务 ID。“活跃”指的就是，启动了但还没提交。数组里面事务 ID 的最小值记为低水位，当前系统里面已经创建过的事务 ID 的最大值加 1 记为高水位。这个视图数组和高水位，就组成了当前事务的一致性视图（read-view）。

数据版本的可见性规则，就是基于数据的 row trx_id 和这个一致性视图的对比结果得到的。

InnoDB 利用了“所有数据都有多个版本”的这个特性，实现了“秒级创建快照”的能力。

这里就用到了这样一条规则：更新数据都是先读后写的，而这个读，只能读当前的值，称为“当前读”（current read），其实，除了 update 语句外，select 语句如果加锁，也是当前读。所以，如果把事务 A 的查询语句 select * from t where id=1 修改一下，加上 lock in share mode 或 for update，也都可以读到版本号是 101 的数据，返回的 k 的值是 3。

InnoDB 的行数据有多个版本，每个数据版本有自己的 row trx_id，每个事务或者语句有自己的一致性视图。普通查询语句是一致性读，一致性读会根据 row trx_id 和一致性视图确定数据版本的可见性：
对于可重复读，查询只承认在事务启动前就已经提交完成的数据；
对于读提交，查询只承认在语句启动前就已经提交完成的数据；
而当前读，总是读取已经提交完成的最新版本。




```

![img](https://static001.geekbang.org/resource/image/04/68/04fb9d24065635a6a637c25ba9ddde68.png)

```
索引的常见三种模型:哈希表、有序数组和N茶树-搜索树。

哈希表：增加新的 User 时速度会很快，只需要往后追加，缺点是，因为不是有序的，所以哈希索引做区间查询的速度是很慢的。你可以设想下，如果你现在要找身份证号在[ID_card_X, ID_card_Y]这个区间的所有用户，就必须全部扫描一遍了。哈希表这种结构适用于只有等值查询的场景，比如 Memcached 及其他一些 NoSQL 引擎。

有序数组：仅仅看查询效率，有序数组就是最好的数据结构了。但是，在需要更新数据的时候就麻烦了，你往中间插入一个记录就必须得挪动后面所有的记录，成本太高。有序数组索引只适用于静态存储引擎，比如你要保存的是 2017 年某个城市的所有人口信息。

数据库底层存储的核心就是基于这些数据模型的。每碰到一个新数据库，我们需要先关注它的数据模型。

-------------主键索引和普通索引----------------
我们有一个主键列为 ID 的表，表中有字段 k，并且在 k 上有索引。
根据上面的索引结构说明，我们来讨论一个问题：基于主键索引和普通索引的查询有什么区别？
如果语句是 select * from T where ID=500，即主键查询方式，则只需要搜索 ID 这棵 B+ 树；
如果语句是 select * from T where k=5，即普通索引查询方式，则需要先搜索 k 索引树，得到 ID 的值为 500，再到 ID 索引树搜索一次。这个过程称为回表.
也就是说，基于非主键索引的查询需要多扫描一棵索引树。因此，我们在应用中应该尽量使用主键查询.

而更糟的情况是，如果 R5 所在的数据页已经满了，根据 B+ 树的算法，这时候需要申请一个新的数据页，然后挪动部分数据过去。这个过程称为页分裂。在这种情况下，性能自然会受影响.除了性能外，页分裂操作还影响数据页的利用率。原本放在一个页的数据，现在分到两个页中，整体空间利用率降低大约 50%.

显然，主键长度越小，普通索引的叶子节点就越小，普通索引占用的空间也就越小。所以，从性能和存储空间方面考量，自增主键往往是更合理的选择。

为什么要重建索引。我们文章里面有提到，索引可能因为删除，或者页分裂等原因，导致数据页有空洞，重建索引的过程会创建一个新的索引，把数据按顺序插入，这样页面的利用率最高，也就是索引更紧凑、更省空间。
重建索引 k 的做法是合理的，可以达到省空间的目的。但是，重建主键的过程不合理。不论是删除主键还是创建主键，都会将整个表重建。所以连着执行这两个语句的话，第一个语句就白做了。这两个语句，你可以用这个语句代替 ： alter table T engine=InnoDB

mysql> show table status like 'T';
如果执行的语句是 select ID from T where k between 3 and 5，这时只需要查 ID 的值，而 ID 的值已经在 k 索引树上了，因此可以直接提供查询结果，不需要回表。也就是说，在这个查询里面，索引 k 已经“覆盖了”我们的查询需求，我们称为覆盖索引。
由于覆盖索引可以减少树的搜索次数，显著提升查询性能，所以使用覆盖索引是一个常用的性能优化手段。

在一个市民信息表上，是否有必要将身份证号和名字建立联合索引：
如果现在有一个高频请求，要根据市民的身份证号查询他的姓名，这个联合索引就有意义了。它可以在这个高频请求上用到覆盖索引，不再需要回表查整行记录，减少语句的执行时间。

创建索引的原则（最左匹配原则）：
第一原则是，如果通过调整顺序，可以少维护一个索引，那么这个顺序往往就是需要优先考虑采用的。
第二原则就是空间了。比如上面这个市民表的情况，name 字段是比 age 字段大的 ，那我就建议你创建一个（name,age) 的联合索引和一个 (age) 的单字段索引。

MySQL 5.6 引入的索引下推优化（index condition pushdown)， 可以在索引遍历过程中，对索引中包含的字段先做判断，直接过滤掉不满足条件的记录，减少回表次数。

-----------------普通索引与唯一索引----------------
查询过程：你知道的，InnoDB 的数据是按数据页为单位来读写的。也就是说，当需要读一条记录的时候，并不是将这个记录本身从磁盘读出来，而是以页为单位，将其整体读入内存。在 InnoDB 中，每个数据页的大小默认是 16KB。

更新过程：当需要更新一个数据页时，如果数据页在内存中就直接更新，而如果这个数据页还没有在内存中的话，在不影响数据一致性的前提下，InnoDB 会将这些更新操作缓存在 change buffer 中，这样就不需要从磁盘中读入这个数据页了。在下次查询需要访问这个数据页的时候，将数据页读入内存，然后执行 change buffer 中与这个页有关的操作。通过这种方式就能保证这个数据逻辑的正确性。需要说明的是，虽然名字叫作 change buffer，实际上它是可以持久化的数据。也就是说，change buffer 在内存中有拷贝，也会被写入到磁盘上。

将 change buffer 中的操作应用到原数据页，得到最新结果的过程称为 merge。除了访问这个数据页会触发 merge 外，系统有后台线程会定期 merge。在数据库正常关闭（shutdown）的过程中，也会执行 merge 操作。显然，如果能够将更新操作先记录在 change buffer，减少读磁盘，语句的执行速度会得到明显的提升。而且，数据读入内存是需要占用 buffer pool 的，所以这种方式还能够避免占用内存，提高内存利用率。

当这个记录要更新的目标页不在内存中。这时，InnoDB 的处理流程如下：对于唯一索引来说，需要将数据页读入内存，判断到没有冲突，插入这个值，语句执行结束；对于普通索引来说，则是将更新记录在 change buffer，语句执行就结束了。将数据从磁盘读入内存涉及随机 IO 的访问，是数据库里面成本最高的操作之一。change buffer 因为减少了随机磁盘访问，所以对更新性能的提升是会很明显的。

因此，对于写多读少的业务来说，页面在写完以后马上被访问到的概率比较小，此时 change buffer 的使用效果最好。这种业务模型常见的就是账单类、日志类的系统。反过来，假设一个业务的更新模式是写入之后马上会做查询，那么即使满足了条件，将更新先记录在 change buffer，但之后由于马上要访问这个数据页，会立即触发 merge 过程。这样随机访问 IO 的次数不会减少，反而增加了 change buffer 的维护代价。所以，对于这种业务模式来说，change buffer 反而起到了副作用。

普通索引和唯一索引应该怎么选择？
如果所有的更新后面，都马上伴随着对这个记录的查询，那么你应该关闭 change buffer。而在其他情况下，change buffer 都能提升更新性能。在实际使用中，你会发现，普通索引和 change buffer 的配合使用，对于数据量大的表的更新优化还是很明显的。在实际使用中，你会发现，普通索引和 change buffer 的配合使用，对于数据量大的表的更新优化还是很明显的。特别地，在使用机械硬盘时，change buffer 这个机制的收效是非常显著的。所以，当你有一个类似“历史数据”的库，并且出于成本考虑用的是机械硬盘时，那你应该特别关注这些表里的索引，尽量使用普通索引，然后把 change buffer 尽量开大，以确保这个“历史数据”表的数据写入速度。

redo log 主要节省的是随机写磁盘的 IO 消耗（转成顺序写），而 change buffer 主要节省的则是随机读磁盘的 IO 消耗。

更新语句，你会发现它涉及了四个部分：内存、redo log（ib_log_fileX）、 数据表空间（t.ibd）、系统表空间（ibdata1）。这条更新语句做了如下的操作（按照图中的数字顺序）：Page 1 在内存中，直接更新内存；Page 2 没有在内存中，就在内存的 change buffer 区域，记录下“我要往 Page 2 插入一行”这个信息将上述两个动作记入 redo log 中。

系统表空间就是用来放系统信息的，比如数据字典什么的，对应的磁盘文件是ibdata1,
数据表空间就是一个个的表数据文件，对应的磁盘文件就是 表名.ibd。

--------------mysql选错索引--------
mysql> CREATE TABLE `t` (  `id` int(11) NOT NULL,  `c` int(11) DEFAULT NULL,  PRIMARY KEY (`id`)) ENGINE=InnoDB;insert into t(id, c) values(1,1),(2,2),(3,3),(4,4);
Query OK, 0 rows affected (0.03 sec)
mysql> delimiter ;;
mysql> create procedure idata()begin  declare i int;  set i=1;  while(i<=100000)do    insert into t values(i, i, i);    set i=i+1;  end while;end;;
Query OK, 0 rows affected (0.02 sec)
mysql> delimiter ;
mysql> call idata();
分析：
mysql> show index from t;
mysql> explain select * from t where (a between 1 and 1000)  and (b between 50000 and 100000) order by b limit 1;

解决办法：
对于由于索引统计信息不准确导致的问题，你可以用 analyze table 来解决
一种方法是，像我们第一个例子一样，采用 force index 强行选择一个索引。
第二种方法就是，我们可以考虑修改语句，引导 MySQL 使用我们期望的索引。
第三种方法是，在有些场景下，我们可以新建一个更合适的索引，来提供给优化器做选择，或删掉误用的索引。

----------------mysql怎么给字符串加索引----------
使用前缀索引，定义好长度，就可以做到既节省空间，又不用额外增加太多的查询成本。否则，可能会增加扫描行数，这会影响到性能。使用前缀索引就用不上覆盖索引对查询性能的优化了，这也是你在选择是否使用前缀索引时需要考虑的一个因素。
怎么选取不同长度的前缀来看这个值？

mysql> select 
  count(distinct left(email,4)）as L4,
  count(distinct left(email,5)）as L5,
  count(distinct left(email,6)）as L6,
  count(distinct left(email,7)）as L7,
from SUser;

既可以占用更小的空间，也能达到相同的查询效率？
第一种方式是使用倒序存储。如果你存储身份证号的时候把它倒过来存。
mysql> select field_list from t where id_card = reverse('input_id_card_string');
第二种方式是使用 hash 字段。你可以在表上再创建一个整数字段，来保存身份证的校验码，同时在这个字段上创建索引。
mysql> alter table t add id_card_crc int unsigned, add index(id_card_crc);
由于校验码可能存在冲突，也就是说两个不同的身份证号通过 crc32() 函数得到的结果可能是相同的，所以你的查询语句 where 部分要判断 id_card 的值是否精确相同。
mysql> select field_list from t where id_card_crc=crc32('input_id_card_string') and id_card='input_id_card_string'


```

![img](https://static001.geekbang.org/resource/image/7c/ce/7cf6a3bf90d72d1f0fc156ececdfb0ce.jpg)

```
行锁、表锁（表锁和MDL锁）、全局锁（锁库）
-------------------------------------------
在 InnoDB 事务中，行锁是在需要的时候才加上的，但并不是不需要了就立刻释放，而是要等到事务结束时才释放。这个就是两阶段锁协议.

事务 A 在等待事务 B 释放 id=2 的行锁，而事务 B 在等待事务 A 释放 id=1 的行锁。 
事务 A 和事务 B 在互相等待对方的资源释放，就是进入了死锁状态。
当出现死锁以后，有两种策略：
一种策略是，直接进入等待，直到超时。这个超时时间可以通过参数 innodb_lock_wait_timeout 来设置。
另一种策略是，发起死锁检测，发现死锁后，主动回滚死锁链条中的某一个事务，让其他事务得以继续执行。将参数 innodb_deadlock_detect 设置为 on，表示开启这个逻辑。

可以低价预售一年内所有的电影票，而且这个活动只做一天。于是在活动时间开始的时候，你的 MySQL 就挂了。你登上服务器一看，CPU 消耗接近 100%，但整个数据库每秒就执行不到 100 个事务。这是什么原因呢？
每个新来的被堵住的线程，都要判断会不会由于自己的加入导致了死锁，这是一个时间复杂度是 O(n) 的操作。假设有 1000 个并发线程要同时更新同一行，那么死锁检测操作就是 100 万这个量级的。
虽然最终检测的结果是没有死锁，但是这期间要消耗大量的 CPU 资源。因此，你就会看到 CPU 利用率很高，但是每秒却执行不了几个事务。我们引入了死锁和死锁检测的概念，以及提供了三个方案，来减少死锁对数据库的影响。减少死锁的主要方向，就是控制访问相同资源的并发事务量.

事务开启语句：
1.begin或者start transaction：显式开启一个事务
2.commit：提交一个事务，使修改是永久的
3.rollback：回滚事务，撤销未提交的修改
4.savepoint identifier：创建一个保存点，一个事务中可以有多个保存点
5.release savepoint identifier：删除一个事务的保存点，若没有这个保存点，抛出异常
6.rollback to identifier：事务回滚到保存点
7.set transaction：设置事务的隔离级别，InnoDB提供的级别有read uncommitted，read committed，repeatable read，serializable

间隙锁、Next-Key Lock的算法
-----------------------------------------
例子一：
session A:
mysql> create table t(a int ,key idx_a(a))engine=innodb;
Query OK, 0 rows affected (0.04 sec)
mysql> insert into t values(1),(3),(5),(8),(11);
Query OK, 5 rows affected (0.00 sec)
Records: 5  Duplicates: 0  Warnings: 0
session B:
mysql> begin;
Query OK, 0 rows affected (0.00 sec)
mysql> select * from t where a=8 for update;
session A:
mysql> begin;
Query OK, 0 rows affected (0.00 sec)
mysql> select * from t;
+------+
| a    |
+------+
|    1 |
|    3 |
|    5 |
|    8 |
|   11 |
+------+
5 rows in set (0.00 sec)
mysql> insert into t values(2);
Query OK, 1 row affected (0.00 sec)
mysql> select * from t;
+------+
| a    |
+------+
|    1 |
|    2 |
|    3 |
|    5 |
|    8 |
|   11 |
+------+
6 rows in set (0.00 sec)
mysql> insert into t values(4);
Query OK, 1 row affected (0.00 sec)
mysql> insert into t values(6);//阻塞
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
mysql> insert into t values(9);//阻塞
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
mysql> insert into t values(12);
Query OK, 1 row affected (0.00 sec)
InnoDB对于行的查询都是采用了Next-Key Lock的算法，锁定的不是单个值，而是一个范围（GAP）。上面索引值有1，3，5，8，11，其记录的GAP的区间如下：是一个左开右闭的空间（原因是默认主键的有序自增的特性，结合后面的例子说明）（-∞,1]，(1,3]，(3,5]，(5,8]，(8,11]，(11,+∞）

例子二：
root@localhost : test 04:58:49>create table t(a int primary key)engine =innodb;
Query OK, 0 rows affected (0.19 sec)
root@localhost : test 04:59:02>insert into t values(1),(3),(5),(8),(11);
Query OK, 5 rows affected (0.00 sec)
Records: 5  Duplicates: 0  Warnings: 0
root@localhost : test 04:59:10>select * from t;
+----+
| a  |
+----+
|  1 |
|  3 |
|  5 |
|  8 |
| 11 |
+----+
rows in set (0.00 sec)

section A:
root@localhost : test 04:59:30>start transaction;
Query OK, 0 rows affected (0.00 sec)
root@localhost : test 04:59:33>select * from t where a = 8 for update;
+---+
| a |
+---+
| 8 |
+---+
row in set (0.00 sec)

section B:
root@localhost : test 04:58:41>start transaction;
Query OK, 0 rows affected (0.00 sec)
root@localhost : test 04:59:45>insert into t values(6);
Query OK, 1 row affected (0.00 sec)
root@localhost : test 05:00:05>insert into t values(7);
Query OK, 1 row affected (0.00 sec)
root@localhost : test 05:00:08>insert into t values(9);
Query OK, 1 row affected (0.00 sec)
root@localhost : test 05:00:10>insert into t values(10);
Query OK, 1 row affected (0.00 sec)

InnoDB对于行的查询都是采用了Next-Key Lock的算法，锁定的不是单个值，而是一个范围，按照这个方法是会和第一次测试结果一样。但是，当查询的索引含有唯一属性的时候，Next-Key Lock 会进行优化，将其降级为Record Lock，即仅锁住索引本身，不是范围。

```

## 主从

![img](https://static001.geekbang.org/resource/image/a6/a3/a66c154c1bc51e071dd2cc8c1d6ca6a3.png)

```
依然建议你把节点 B（也就是备库）设置成只读（readonly）模式。因为 readonly 设置对超级 (super) 权限用户是无效的，而用于同步更新的线程，就拥有超级权限。

一个事务日志同步的完整过程是这样的：
在备库 B 上通过 change master 命令，设置主库 A 的 IP、端口、用户名、密码，以及要从哪个位置开始请求 binlog，这个位置包含文件名和日志偏移量。
在备库 B 上执行 start slave 命令，这时候备库会启动两个线程，就是图中的 io_thread 和 sql_thread。其中 io_thread 负责与主库建立连接。
主库 A 校验完用户名、密码后，开始按照备库 B 传过来的位置，从本地读取 binlog，发给 B。备库 B 拿到 binlog 后，写到本地文件，称为中转日志（relay log）。
sql_thread 读取中转日志，解析出日志里的命令，并执行。

-------------查看binlog内容、binlog格式
mysql> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql-bin.000017 |       120 |
| mysql-bin.000018 |       167 |
| mysql-bin.000019 |      5769 |
| mysql-bin.000020 |       167 |
| mysql-bin.000021 |      1477 |
| mysql-bin.000022 |  26785862 |
+------------------+-----------+
6 rows in set (0.00 sec)
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000022 | 26785862 | db           |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
mysql> show binlog events in 'mysql-bin.000022';
mysqlbinlog  -vv data/master.000001 --start-position=8900;//查看binlog为row格式的文件。
row格式记录的是真实发生的操作（更可靠），statement格式记录的是执行语句。但 row 格式的缺点是，很占空间。MySQL 就取了个折中方案，也就是有了 mixed 格式的 binlog。mixed 格式的意思是，MySQL 自己会判断这条 SQL 语句是否可能引起主备不一致，如果有可能，就用 row 格式，否则就用 statement 格式。

现在越来越多的场景要求把 MySQL 的 binlog 格式设置成 row。这么做的理由有很多，我来给你举一个可以直接看出来的好处：恢复数据。由 delete、insert 或者 update 语句导致的数据操作错误，需要恢复到操作之前状态的情况，也时有发生，还有now()等时间节点数据恢复。MariaDB 的Flashback工具就是基于上面介绍的原理来回滚数据的。

-------------双主机制解决循环复制
来解决两个节点间的循环复制的问题：规定两个库的 server id 必须不同，如果相同，则它们之间不能设定为主备关系；一个备库接到 binlog 并在重放的过程中，生成与原 binlog 的 server id 相同的新的 binlog；每个库在收到从自己的主库发过来的日志后，先判断 server id，如果跟自己的相同，表示这个日志是自己生成的，就直接丢弃这个日志。按照这个逻辑，如果我们设置了双 M 结构，日志的执行流就会变成这样：从节点 A 更新的事务，binlog 里面记的都是 A 的 server id；传到节点 B 执行一次以后，节点 B 生成的 binlog 的 server id 也是 A 的 server id；再传回给节点 A，A 判断到这个 server id 与自己的相同，就不会再处理这个日志。所以，死循环在这里就断掉了。

-------------主备、主从延迟原因
首先，有些部署条件下，备库所在机器的性能要比主库所在的机器性能差。
第二种常见的可能了，即备库的压力大。
这就是第三种可能了，即大事务。（不要一次性地用 delete 语句删除太多数据，另一种典型的大事务场景，就是大表 DDL。这个场景，我在前面的文章中介绍过。处理方案就是，计划内的 DDL，建议使用 gh-ost 方案）

-------------主备切换
可靠性优先策略：
判断备库 B 现在的 seconds_behind_master，如果小于某个值（比如 5 秒）继续下一步，否则持续重试这一步；把主库 A 改成只读状态，即把 readonly 设置为 true；判断备库 B 的 seconds_behind_master 的值，直到这个值变成 0 为止；把备库 B 改成可读写状态，也就是把 readonly 设置为 false；把业务请求切到备库 B。
可用性优先策略：
。。。。。。。。。。。
因延迟可能导致数据不一致，最好采   性优先策略，但设置 binlog_format=row。在实际的应用中，我更建议使用可靠性优先的策略。毕竟保证数据准确，应该是数据库服务的底线。在这个基础上，通过减少主备延迟，提升系统的可用性。
在满足数据可靠性的前提下，MySQL 高可用系统的可用性，是依赖于主备延迟的。延迟的时间越小，在主库故障的时候，服务恢复需要的时间就越短，可用性就越高，

基于 GTID 的主备切换
GTID 模式的启动也很简单，我们只需要在启动一个 MySQL 实例的时候，加上参数 gtid_mode=on 和 enforce_gtid_consistency=on 就可以了。
主从延迟还是不能 100% 避免的。
强制走主库方案；sleep 方案；判断主备无延迟方案；配合 semi-sync 方案；等主库位点方案；等 GTID 方案。



```



## 实战

### order by是怎么工作的

```
------------order by流程------------
初始化 sort_buffer，确定放入 name、city、age 这三个字段；
从索引 city 找到第一个满足 city='杭州’条件的主键 id，也就是图中的 ID_X；
到主键 id 索引取出整行，取 name、city、age 三个字段的值，存入 sort_buffer 中；
从索引 city 取下一个记录的主键 id；
重复步骤 3、4 直到 city 的值不满足查询条件为止，对应的主键 id 也就是图中的 ID_Y；
对 sort_buffer 中的数据按照字段 name 做快速排序；
按照排序结果取前 1000 行返回给客户端。

MySQL 将需要排序的数据分成 12 份，每一份单独排序后存在这些临时文件中。然后把这 12 个有序文件再合并成一个有序的大文件。
如果 sort_buffer_size 超过了需要排序的数据量的大小，number_of_tmp_files 就是 0，表示排序可以直接在内存中完成。否则就需要放在临时文件中排序。sort_buffer_size 越小，需要分成的份数越多，number_of_tmp_files 的值就越大。

如果查询要返回的字段很多的话，那么 sort_buffer 里面要放的字段数太多，这样内存里能够同时放下的行数很少，要分成很多个临时文件，排序的性能会很差。所以如果单行很大，这个方法效率不够好。

SET max_length_for_sort_data = 16;后执行逻辑变化如下：
初始化 sort_buffer，确定放入两个字段，即 name 和 id；
从索引 city 找到第一个满足 city='杭州’条件的主键 id，也就是图中的 ID_X；
到主键 id 索引取出整行，取 name、id 这两个字段，存入 sort_buffer 中；
从索引 city 取下一个记录的主键 id；
重复步骤 3、4 直到不满足 city='杭州’条件为止，也就是图中的 ID_Y；
对 sort_buffer 中的数据按照字段 name 进行排序；
遍历排序结果，取前 1000 行，并按照 id 的值回到原表中取出 city、name 和 age 三个字段返回给客户端。

MySQL 实在是担心排序内存太小，会影响排序效率，才会采用 rowid 排序算法，这样排序过程中一次可以排序更多行，但是需要再回到原表去取数据。如果 MySQL 认为内存足够大，会优先选择全字段排序，把需要的字段都放到 sort_buffer 中，这样排序后就会直接从内存里面返回查询结果了，不用再回到原表去取数据。

并不是所有的order by语句，都需要排序操作的。从上面分析的执行过程，我们可以看到，MySQL 之所以需要生成临时表，并且在临时表上做排序操作，其原因是原来的数据都是无序的。你可以设想下，如果能够保证从 city 这个索引上取出来的行，天然就是按照 name 递增排序的话，就可以不用再排序了。

mysql> CREATE TABLE `t1` (   `id` int(11) NOT NULL,   `city` varchar(16) NOT NULL,   `name` varchar(16) NOT NULL,   `age` int(11) NOT NULL,   `addr` varchar(128) DEFAULT NULL,   PRIMARY KEY (`id`),   KEY `city`` (`city`) ) ENGINE=InnoDB;
Query OK, 0 rows affected (0.28 sec) 
mysql> explain select city,name,age from t1 where city='12' order by name limit 1000;
+----+-------------+-------+------+---------------+------+---------+-------+------+----------------------------------------------------+
| id | select_type | table | type | possible_keys | key  | key_len | ref   | rows | Extra                                              |
+----+-------------+-------+------+---------------+------+---------+-------+------+----------------------------------------------------+
|  1 | SIMPLE      | t1    | ref  | city          | city | 18      | const |    1 | Using index condition; Using where; Using filesort |
+----+-------------+-------+------+---------------+------+---------+-------+------+----------------------------------------------------+
1 row in set (0.00 sec)

mysql> alter table t1 add index city_user(city, name);
Query OK, 0 rows affected (0.11 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> explain select city,name,age from t1 where city='12' order by name limit 1000;
+----+-------------+-------+------+----------------+-----------+---------+-------+------+-------------+
| id | select_type | table | type | possible_keys  | key       | key_len | ref   | rows | Extra       |
+----+-------------+-------+------+----------------+-----------+---------+-------+------+-------------+
|  1 | SIMPLE      | t1    | ref  | city,city_user | city_user | 18      | const |    1 | Using where |
+----+-------------+-------+------+----------------+-----------+---------+-------+------+-------------+
1 row in set (0.00 sec)

select word from words order by rand() limit 3;
---------------------------
order by rand() 使用了内存临时表，内存临时表排序的时候使用了 rowid 排序方法。
是不是所有的临时表都是内存表呢？其实不是的。tmp_table_size 这个配置限制了内存临时表的大小，默认值是 16M。如果临时表大小超过了 tmp_table_size，那么内存临时表就会转成磁盘临时表。

在实际应用的过程中，比较规范的用法就是：尽量将业务逻辑写在业务代码中，让数据库只做“读写数据”的事情。因此，这类方法的应用还是比较广泛的. 
```

### 为什么逻辑相同，性能差别这么大

```
条件字段函数操作，对索引字段做函数操作，可能会破坏索引值的有序性，因此优化器就决定放弃走树搜索功能。因此调整：
------------------------------------------------------
select count(*) from tradelog where    -> (t_modified >= '2016-7-1' and t_modified<'2016-8-1') or    -> (t_modified >= '2017-7-1' and t_modified<'2017-8-1') or     -> (t_modified >= '2018-7-1' and t_modified<'2018-8-1');

隐式类型转换\隐式字符编码转换
-----------------------

```

### 只查一行也执行慢

```
等待锁。
flush 磁盘。
等待MDL锁。
```



### 有损提升性能的方法

```
第一种方法：先处理掉那些占着连接但是不工作的线程。
在 T 时刻之后的 30 秒执行 show processlist，而要看事务具体状态的话，你可以查 information_schema 库的 innodb_trx 表。
从服务端断开连接使用的是 kill connection + id 的命令。

第二种方法：减少连接过程的消耗

导致慢查询
----------------------------
导致慢查询的第一种可能是，索引没有设计好
在备库 B 上执行 set sql_log_bin=off，也就是不写 binlog，然后执行 alter table 语句加上索引；执行主备切换；这时候主库是 B，备库是 A。在 A 上执行 set sql_log_bin=off，然后执行 alter table 语句加上索引。这是一个“古老”的 DDL 方案。平时在做变更的时候，你应该考虑类似 gh-ost 这样的方案，更加稳妥。但是在需要紧急处理时，上面这个方案的效率是最高的。

导致慢查询的第二种可能是，语句没写好。
MySQL 5.7 提供了 query_rewrite 功能:
mysql> insert into query_rewrite.rewrite_rules(pattern, replacement, pattern_database) values ("select * from t where a + 1 = ?", "select * from t where a = ? - 2", "db1");call query_rewrite.flush_rewrite_rules();

qps突增
---------------------
一种是由全新业务的 bug 导致的。假设你的 DB 运维是比较规范的，也就是说白名单是一个个加的。这种情况下，如果你能够确定业务方会下掉这个功能，只是时间上没那么快，那么就可以从数据库端直接把白名单去掉。如果这个新功能使用的是单独的数据库用户，可以用管理员账号把这个用户删掉，然后断开现有连接。这样，这个新功能的连接不成功，由它引发的 QPS 就会变成 0。如果这个新增的功能跟主体功能是部署在一起的，那么我们只能通过处理语句来限制。这时，我们可以使用上面提到的查询重写功能，把压力最大的 SQL 语句直接重写成"select 1"返回。


```

### 误删行、表

```
------------误删行
我们提到如果是使用 delete 语句误删了数据行，可以用 Flashback 工具通过闪回把数据恢复回来。Flashback 恢复数据的原理，是修改 binlog 的内容，拿回原库重放。而能够使用这个方案的前提是，需要确保 binlog_format=row 和 binlog_row_image=FULL。

需要说明的是，我不建议你直接在主库上执行这些操作。恢复数据比较安全的做法，是恢复出一个备份，或者找一个从库作为临时库，在这个临时库上执行这些操作，然后再将确认过的临时库的数据，恢复回主库。

我们不止要说误删数据的事后处理办法，更重要是要做到事前预防。我有以下两个建议：
把 sql_safe_updates 参数设置为 on。这样一来，如果我们忘记在 delete 或者 update 语句中写 where 条件，或者 where 条件里面没有包含索引字段的话，这条语句的执行就会报错。
代码上线前，必须经过 SQL 审计。

而使用 truncate /drop table 和 drop database 命令删除的数据，就没办法通过 Flashback 来恢复了。为什么呢？这是因为，即使我们配置了 binlog_format=row，执行这三个命令时，记录的 binlog 还是 statement 格式。binlog 里面就只有一个 truncate/drop 语句，这些信息是恢复不出数据的。

-------------误删表、库
这两个方案都要求备份系统定期备份全量日志，而且需要确保 binlog 在被从本地删除之前已经做了备份。

延迟复制的备库是一种特殊的备库，通过 CHANGE MASTER TO MASTER_DELAY = N 命令，可以指定这个备库持续保持跟主库有 N 秒的延迟。比如你把 N 设置为 3600，这就代表了如果主库上有数据被误删了，并且在 1 小时内发现了这个误操作命令，这个命令就还没有在这个延迟复制的备库执行。这时候到这个备库上执行 stop slave，再通过之前介绍的方法，跳过误操作命令，就可以恢复出需要的数据。

-------------预防策略
第一条建议是，账号分离。这样做的目的是，避免写错命令。比如：我们只给业务开发同学 DML 权限，而不给 truncate/drop 权限。而如果业务开发人员有 DDL 需求的话，也可以通过开发管理系统得到支持。即使是 DBA 团队成员，日常也都规定只使用只读账号，必要的时候才使用有更新权限的账号。
第二条建议是，制定操作规范。这样做的目的，是避免写错要删除的表名。比如：在删除数据表之前，必须先对表做改名操作。然后，观察一段时间，确保对业务无影响以后再删除这张表。改表名的时候，要求给表名加固定的后缀（比如加 _to_be_deleted)，然后删除表的动作必须通过管理系统执行。并且，管理系删除表的时候，只能删除固定后缀的表。

```

### 为什么还有kill不掉的语句

```
如果库里面的表特别多，连接就会很慢。
----------------------
为了实现这个功能，客户端在连接成功后，需要多做一些操作：执行 show databases；切到 db1 库，执行 show tables；把这两个命令的结果用于构建一个本地的哈希表。在这些操作中，最花时间的就是第三步在本地构建哈希表的操作。所以，当一个库中的表个数非常多的时候，这一步就会花比较长的时间。
你自动补全功能用得并不多，我建议你每次使用的时候都默认加 -A。


```

### 查很多数据会不会把数据库内存打爆

```
MySQL 是“边读边发的”，这个概念很重要。这就意味着，如果客户端接收得慢，会导致 MySQL 服务端由于结果发不出去，这个事务的执行时间变长。

MySQL 客户端发送请求后，接收服务端返回结果的方式有两种：
一种是本地缓存，也就是在本地开一片内存，先把结果存起来。如果你用 API 开发，对应的就是 mysql_store_result 方法。
另一种是不缓存，读一个处理一个。如果你用 API 开发，对应的就是 mysql_use_result 方法。MySQL 客户端默认采用第一种方式，而如果加上–quick 参数，就会使用第二种不缓存的方式。

-----------------
取数据和发数据的流程是这样的：
获取一行，写到 net_buffer 中。这块内存的大小是由参数 net_buffer_length 定义的，默认是 16k。
重复获取行，直到 net_buffer 写满，调用网络接口发出去。
如果发送成功，就清空 net_buffer，然后继续取下一行，并写入 net_buffer。
如果发送函数返回 EAGAIN 或 WSAEWOULDBLOCK，就表示本地网络栈（socket send buffer）写满了，进入等待。直到网络栈重新可写，再继续发送。

如果你在自己负责维护的 MySQL 里看到很多个线程都处于“Sending to client”这个状态，就意味着你要让业务开发同学优化查询结果，并评估这么多的返回结果是否合理。

仅当一个线程处于“等待客户端接收结果”的状态，才会显示"Sending to client"；而如果显示成“Sending data”，它的意思只是“正在执行”。

show engine innodb status 结果中，查看一个系统当前的 BP 命中率。一般情况下，一个稳定服务的线上系统，要保证响应时间符合要求的话，内存命中率要在 99% 以上。执行 show engine innodb status ，可以看到“Buffer pool hit rate”字样，显示的就是当前的命中率。
InnoDB Buffer Pool 的大小是由参数 innodb_buffer_pool_size 确定的，一般建议设置成可用物理内存的 60%~80%。




```

### 关于join

```

```

### 临时表

```
临时表在使用上有以下几个特点：
建表语法是 create temporary table …。
一个临时表只能被创建它的 session 访问，对其他线程不可见。所以，图中 session A 创建的临时表 t，对于 session B 就是不可见的。
临时表可以与普通表同名。
session A 内有同名的临时表和普通表的时候，show create 语句，以及增删改查语句访问的是临时表。
show tables 命令不显示临时表。

---------应用分库分表
各个分库拿到的数据，汇总到一个 MySQL 实例的一个表中，然后在这个汇总实例上做逻辑操作。

---------重名实现、主从复制
MySQL 维护数据表，除了物理上要有文件外，内存里面也有一套机制区别不同的表，每个表都对应一个 table_def_key。
一个普通表的 table_def_key 的值是由“库名 + 表名”得到的，所以如果你要在同一个库下创建两个同名的普通表，创建第二个表的过程中就会发现 table_def_key 已经存在了。
而对于临时表，table_def_key 在“库名 + 表名”基础上，又加入了“server_id+thread_id”。

MySQL 在记录 binlog 的时候，会把主库执行这个语句的线程 id 写到 binlog 中。
这样，在备库的应用线程就能够知道执行每个语句的主库线程 id，并利用这个线程 id 来构造临时表的 table_def_key：
session A 的临时表 t1，在备库的 table_def_key 就是：库名 +t1+“M 的 serverid”+“session A 的 thread_id”;
session B 的临时表 t1，在备库的 table_def_key 就是 ：库名 +t1+“M 的 serverid”+“session B 的 thread_id”。
在 binlog_format='row’的时候，临时表的操作不记录到 binlog 中，也省去了不少麻烦，这也可以成为你选择 binlog_format 时的一个考虑因素。

```

