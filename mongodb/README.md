[TOC]

# 一、基本概念及原理

> MongoDB 是一个基于分布式文件存储的数据库。由 C++语言编写。旨在为 WEB 应用提供可 扩展的高性能数据存储解决方案。 MongoDB 是一个介于关系数据库和非关系数据库之间的 产品，是非关系数据库当中功能最丰富，最像关系数据库的。

# 二、什么是NoSQL

> NoSQL，指的是非关系型的数据库。NoSQL 有时也称作 Not Only SQL 的缩写，是对不同于传 统的关系型数据库的数据库管理系统的统称。NoSQL 用于超大规模数据的存储。（例如谷歌 或 Facebook 每天为他们的用户收集万亿比特的数据）。这些类型的数据存储不需要固定的 模式，无需多余操作就可以横向扩展

# 三、关系型数据库 PK 非关系型数据库

![img](https://img.mubu.com/document_image/07ad06f7-4fba-48b7-babd-cfca3f7efe7f-862021.jpg)

# 四、NoSQL数据库分类

![img](https://img.mubu.com/document_image/9a681c6a-c17e-4bed-bb5d-5c74361d6828-862021.jpg)

![img](https://img.mubu.com/document_image/d18c34b8-7125-4c30-b5fb-c7ac6e5bac1a-862021.jpg)

# 五、CAP 原则

在计算机科学中, CAP 定理（CAP theorem）, 又被称作 布鲁尔定理（Brewer's theorem）, 它指出对于一个分布式计算系统来说，不可能同时满足以下三点:
一致性(Consistency) (所有节点在同一时间具有相同的数据)
可用性(Availability) (保证每个请求不管成功或者失败都有响应)
分区容错性(Partition tolerance) (系统中任意信息的丢失或失败不影响系统的继续运行)
CAP 理论的核心是：一个分布式系统不可能同时很好的满足一致性，可用性和分区容错性这三个需求，最多只能同时较好的满足两个。 因此，根据 CAP 原理将 NoSQL 数据库分成了满足 CA 原则、满足 CP 原则和满足 AP 原则三 大类：
CA - 单点集群，满足一致性，可用性的系统，通常在可扩展性上不太强大。
CP - 满足一致性，分区容错性的系统，通常性能不是特别高。
AP - 满足可用性，分区容错性的系统，通常可能对一致性要求低一些。 MongoDB默认就是满足Ap的，弱事务性。

# 六、MongoDB的数据结构与关系型数据库数据结构对比

![img](https://img.mubu.com/document_image/cf578ca7-9c1e-40d6-9b67-f54f89dfcdbf-862021.jpg)

# 七、MongoDB 中的数据类型

![img](https://img.mubu.com/document_image/cace966d-352f-4d1a-8588-0c10cac76fd3-862021.jpg)

![img](https://img.mubu.com/document_image/b095a3c4-cc5b-401c-9eec-bd13250c70ea-862021.jpg)

# 八、MongoDB 的集群部署

MongoDB 的集群部署方案中有三类角色：实际数据存储结点、配置文件存储结点和路由接入结点。连接的客户端直接与路由结点相连，从配置结点上查询数据，根据查询结果到实际的存储结
点上查询和存储数据。MongoDB 的部署方案有单机部署、复本集（主备）部署、分片部署、复本集与分片混合部署。
路由结点：路由角色的结点在分片的情况下起到负载均衡的作用。
配置结点：存储配置文件的服务器其实存储的是片键与 chunk 以及 chunk 与 server 的映射关系。

## 混合的部署方式

![img](https://img.mubu.com/document_image/30a95897-05bf-48c6-9260-710430f3d085-862021.jpg)

## 复本集

![img](https://img.mubu.com/document_image/87724c10-5926-435f-9ae0-4e5b1953ab3d-862021.jpg)

![img](https://img.mubu.com/document_image/1ffd44f2-59c4-4354-8641-4bfa1c54dab3-862021.jpg)

对于复本集，又有主和从两种角色，写数据和读数据也是不同，写数据的过程是只写到主结点中，由主结点以异步的方式同步到从结点中。而读数据则只要从任一结点中读取，具体到哪个结点读取是可以指定的。

# 九、MongoDB的应用场景和不适用场景

## 1、适用场景

对于 MongoDB 实际应用来讲，是否使用 MongoDB 需要根据项目的特定特点进行一一甄别，
这就要求我们对 MongoDB 适用和不适用的场景有一定的了解。
根据 MongoDB 官网的说明，MongoDB 的适用场景如下:
1）网站实时数据:MongoDB 非常适合实时的插入，更新与查询，并具备网站实时数据存储
所需的复制及高度伸缩性。
2）数据缓存:由于性能很高，MongoDB 也适合作为信息基础设施的缓存层。在系统重启之
后，由 MongoDB 搭建的持久化缓存层可以避免下层的数据源过载。
3）大尺寸、低价值数据存储:使用传统的关系型数据库存储一些数据时可能会比较昂贵，在
此之前，很多时候程序员往往会选择传统的文件进行存储。
4）高伸缩性场景:MongoDB 非常适合由数十或数百台服务器组成的数据库。MongoDB 的路
线图中已经包含对 MapReduce 引擎的内置支持。
5）对象或 JSON 数据存储:MongoDB 的 BSON 数据格式非常适合文档化格式的存储及查询。

## 2、不适用场景

了解了 MongoDB 适用场景之后，还需要了解哪些场景下不适合使用 MongoDB，具体如下:
1）高度事务性系统:例如银行或会计系统。传统的关系型数据库目前还是更适用于需要
大量原子性复杂事务的应用程序。
2）传统的商业智能应用:针对特定问题的 BI 数据库会对产生高度优化的查询方式。对
于此类应用，数据仓库可能是更合适的选择。
3）需要复杂 SQL 查询的问题。
相信通过上面的说明，你已经大致了解了 MongoDB 的使用规则，需要说明一点的是，
MongoDB 不仅仅是数据库，更多的使用是将 MongoDB 作为一个数据库中间件在实际应用中
合理划分使用细节，这一点对于 MongoDB 应用来讲至关重要！

# 十、安装配置、常用命令及客户端

## 安装配置

![img](https://img.mubu.com/document_image/f44ae1e6-d036-4615-b5d1-7ea22fb777aa-862021.jpg)

可以结合mongodb（一）来理解。
​1，在官网上找到社区版并下载社区版：wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.6.5.tgz 
2，​解压
3，进入解压目录​，观察bin下的执行文件。其中：mongo（改动配置）、mongod（启动数据库）、mongos（配置路由）。
​4，修改/etc/profile，设置环境变量export MONGO_HOME=/opt/mongodb-linux-x86_64-3.6.5 ，export PATH=$MONGO_HOME/bin:$PATH ，source /etc/profile
5，​mongo -version检测。
6，​创建mongodb的数据文件夹： mkdir -p /data/mongodb/data2
7，简易启动：​mongod --dbpath=/data/mongodb/data2(最后一行显示我们的 MongoDB 已经连接到 27017,它是默认的数据库的端口；它建立完数据
库之后，会在我们的 /data/mongodb/data2文件夹下，生成一些文件夹和文件：在 journal 文件夹中
会存储相应的数据文件，NoSQL 的 MongoDB，它以文件的形式，也就是说被二进制码转换
过的 json 形式来存储所有的数据模型。)​
8，启动mongo客户端连接：

mongo 
show dbs​ 查看​
9，通过配置启动：这里若是要远程连接，建议新建conf文件夹并且添加​mongodb.conf配置文件，编辑该文件:

``` xml

```

10，​再重启启动 ： nohup mongod -f mongodb.conf &
11，添加fork=true​ 保证后台启动​

## ​参考文档

https://www.mongodb.com/download-center?jmp=nav#community

# 十一、常用命令

![img](https://img.mubu.com/document_image/38cc6a7f-19ac-4977-8a5c-07ef3a050a88-862021.jpg)

通过mongodb客户端连接，输入如下命令操作：

```properties

```

# 十二、客户端

![img](https://img.mubu.com/document_image/12306097-bcf8-44fa-a39e-a1f799dab72c-862021.jpg)

可以使用mongovue、Studio 3T等工具连接。如上图，这里使用Studio 3T客户端连接。
可以通过如下链接下载客户端：<https://studio3t.com/download>​

# 十三、支持mongodb的ORM框架

1，<http://mongodb.github.io/morphia/>
2，<https://projects.spring.io/spring-data-mongodb/> 

注意要添加mongodb的驱动包:

``` xml
<dependency>
    <groupId>org.mongodb</groupId>
    <artifactId>mongo-java-driver</artifactId>
    <version>3.7.1</version>
</dependency>
```

## mongodb的ORM框架使用

### 简单版 直接使用java驱动

![img](https://img.mubu.com/document_image/4d9e8cae-d327-4e38-8fa2-fae22a9d6165-862021.jpg)

``` xml
<dependency>
<groupId>org.mongodb</groupId>
<artifactId>mongo-java-driver</artifactId>
<version>3.4.0</version>
</dependency>
```

### morphia（mongo官方推荐的一个ORM框架）

![img](https://img.mubu.com/document_image/5c718896-8bf5-4800-b462-550fe7397f97-862021.jpg)

``` xml
<dependency>
<groupId>org.mongodb.morphia</groupId>
<artifactId>morphia</artifactId>
<version>1.3.2</version>
</dependency>
```

### spring（常用） - 手写ORM框架

``` xml
<dependency>
<groupId>org.springframework.data</groupId>
<artifactId>spring-data-mongodb</artifactId>
<version>1.10.9.RELEASE</version>
</dependency>
```

# 十四、用户管理

## 1.1、添加用户

为 testdb 添加 tom 用户
use testdb
db.createUser({user:"tom",pwd:"123",roles:[{ role:"dbAdmin",db:"testdb"}]})
具体角色有
read：允许用户读取指定数据库
readWrite：允许用户读写指定数据库
dbAdmin：允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问
system.profile
userAdmin：允许用户向 system.users 集合写入，可以找指定数据库里创建、删除和管理用
户
clusterAdmin：只在 admin 数据库中可用，赋予用户所有分片和复制集相关函数的管理权限。
readAnyDatabase：只在 admin 数据库中可用，赋予用户所有数据库的读权限
readWriteAnyDatabase：只在 admin 数据库中可用，赋予用户所有数据库的读写权限
userAdminAnyDatabase：只在 admin 数据库中可用，赋予用户所有数据库的 userAdmin 权限
dbAdminAnyDatabase：只在 admin 数据库中可用，赋予用户所有数据库的 dbAdmin 权限。
root：只在 admin 数据库中可用。超级账号，超级权限

## 1.2 查看所有用户

db.system.users.find()

和用户管理相关的操作基本都要在 admin 数据库下运行，要先 use admin;
如果在某个单一的数据库下，那只能对当前数据库的权限进行操作;

## 1.3、用户删除操作

db.system.users.remove({user:"tom"});

## 1.4 查看当前用户权限

db.runCommand({usersInfo:"tom",showPrivileges:true})

## 1.5 修改密码

use testdb
db.changeUserPassword("tom", "123456")

## 1.6、启用用户

db.auth("tom","123")

## 1.7、安全检查 --auth

> 非 testdb 是不能操作数据库的,启用自己的用户才能访问
>
> 非 admin 数据库的用户不能使用数据库命令，admin 数据库中的数据经过认证为管理员



# 十五、Mongodb 的三种集群方式的搭建：Master-Slaver/Replica Set / Sharding

![img](https://img.mubu.com/document_image/377d4ccf-bb26-4abf-a0f3-dd84981e5d09-862021.jpg)

![img](https://img.mubu.com/document_image/86fc4ab0-c484-4406-9c7c-722fdf764e6c-862021.jpg)

三种集群搭建方式首选 Replica Set，只有真的是大数据，Sharding 才能显现威力，毕竟备节点同步数据是需要时间的。Sharding 可以将多片数据集中到路由节点上进行一些对比，然后将数据返回给客户端，但是效率还是比较低

## 主从 （单机-搭建伪分布式）

这个是最简答的集群搭建，不过准确说也不能算是集群，只能说是主备。并且官方已经不推荐这种方式，所以在这里只是简单的介绍下吧，搭建方式也相对简单。
注意：从机不能读也不能写。从机若要可以读数据，可以在连接从机上输入修改：r​s.slaveOk(); 

### 主从新建文件目录

![img](https://img.mubu.com/document_image/d7642d2c-7668-42a5-993e-1432ac0a8bf1-862021.jpg)

### 修改主从的mongodb.conf的配置文件，如：

主机修改或添加：
master=true
source=192.168.254.135:27008
从机修改或添加：
slave=true
source=192.168.254.135:27009

### 启动，如下图：

![img](https://img.mubu.com/document_image/f1e0c6f5-a99a-43aa-8bcb-7987a8fdd065-862021.jpg)

### 验证（主机造数据，从机查看）：

![img](https://img.mubu.com/document_image/1319b180-1ea3-451d-b52c-68603863c0ce-862021.jpg)

## 副本集

主、从、仲裁节点添加安装文件

master节点（192.168.254.135）
配置mongodb.conf文件，添加副本集： replSet=shard001

slave节点（192.168.254.134）
配置mongodb.conf文件，添加副本集： replSet=shard001

arbiter节点（192.168.254.132）
配置mongodb.conf文件，添加副本集： replSet=shard001

配置主、备、仲裁节点
\>mongo 192.168.254.135:27017 #ip 和 port 是某个节点的地址
\>use admin
>cfg={_id:"shard001",members:[{_id:0,host:'192.168.254.135:27017',priority:9},{_id:1,host:'192.168.254.134:27017',priority:1},{_id:2,host:'192.168.254.132:27017',arbiterOnly:true}]};
\>rs.initiate(cfg) #使配置生效

检测是否成功

![img](https://img.mubu.com/document_image/add997a2-0d54-477e-a605-e5c050fa4abd-862021.jpg)

![img](https://img.mubu.com/document_image/699a6842-3880-4eb1-a668-910783e14dd1-862021.jpg)

\>如上图，输入下面命令即可看到主从仲裁各节点。
\>​mongo 192.168.254.135:27017
\>rs.status();​
可以通过在主节点添加数据，在从机上查看，如图。

## Sharding

![img](https://img.mubu.com/document_image/9a9abc47-4ee7-45c6-99df-c4b1024e2aca-862021.jpg)

基本概念：RouteServer（路由服务器）、ConfigServer（配置服务器）、Replica Set（副本集）、Shard（切片）、Chunk（分块）

基于上面的副本集的环境，再搭建一个单机的伪分布式环境，从而构建两个如上图所示的两个副本集。

### 添加新的副本集

新建文件目录，并添加修改配置文件mongodb.cfg

![img](https://img.mubu.com/document_image/2767f8c3-eb14-4ab0-930c-29e369a7c179-862021.jpg)

\>mongodb.cfg配置文件大同，如下：
dbpath=/opt/mongodb/shard/replset/replica1/data
logpath=/opt/mongodb/shard/replset/replica1/logs/mongodb.log
logappend=true
fork=true
bind_ip=192.168.254.135（根据环境而定）
port=27001（修改端口）
replSet=shard002（不能和已有的副本集名称重复）
shardsvr=true​
\>mongo 192.168.254.135 :27001连接节点
\>cfg=cfg={_id:"shard002",members:[{_id:0,host:'192.168.254.135:27001'},{_id:1,host:'192.168.254.135:27002'},{_id:2,host:'192.168.254.135:27003'}]};
\>rs.initiate(cfg) ​

### 配置 configsvr

新建文件目录，并修改配置文件mongodb.cfg

![img](https://img.mubu.com/document_image/421e39b9-d177-4f6b-96b8-31d4fea1c946-862021.jpg)

\>mongodb.cfg配置文件大同，如下：
​dbpath=/opt/mongodb/shard/configsvr/config3/data
configsvr=true
port=28003
fork=true
logpath=/opt/mongodb/shard/configsvr/config3/logs/mongodb.log
replSet=configrs
logappend=true
bind_ip=192.168.254.135
\>mongo 192.168.254.135 :28001 连接节点.
\>cfg={_id:"configrs",members:[{_id:0,host:'192.168.254.135:28001'},{_id:1,host:'192.168.254.135:28002'},{_id:2,host:'192.168.254.135:28003'}]};
\>rs.initiate(cfg) ​
​​​

### 配置路由节点

![img](https://img.mubu.com/document_image/09cd26dc-9c02-4ebe-a7fe-a04b280a74d7-862021.jpg)

新建文件目录，如：mkdir -p /opt/mongodb/shard/routesvr/logs

修改配置文件mongodb.cfg
configdb=configrs/192.168.254.135:28001,192.168.254.135:28002,192.168.254.135:28003
port=30000
fork=true
logpath=/opt/mongodb/shard/routesvr/logs/mongodb.log
logappend=true
bind_ip=192.168.254.135

启动路由节点：mongos -f /opt/mongodb/shard/routesvr/mongodb.cfg 

### 配置Sharding

![img](https://img.mubu.com/document_image/6aabcd1b-cc0c-49c6-9acf-d59b56231972-862021.jpg)

![img](https://img.mubu.com/document_image/c782e373-eed8-4ca3-a06b-1d144bad15f2-862021.jpg)

ReplicaSet（副本集）、shard（切片）和chunk（分块）的区别

![img](https://img.mubu.com/document_image/f3cfc334-bffd-4df3-970b-7bdfcefac0ad-862021.jpg)

![img](https://img.mubu.com/document_image/d45b21c3-b9f5-4066-9b24-c2be43566f9c-862021.jpg)