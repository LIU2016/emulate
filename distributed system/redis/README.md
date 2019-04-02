[TOC]

# 1，背景

数据都是先缓存在内存中，再周期性的把更新的数据写入磁盘或者把修改操作写入追加的记录文件，并且在此基础上实现了master-slave(主从)同步。

# 2、什么

缓存大致可以分为两类，一种是应用内缓存，比如Map(简单的数据结构)，以及EH Cache(Java第三方库)，另一种
就是缓存组件，比如Memached，Redis；Redis（remote dictionary server）是一个基于KEY-VALUE的高性能的
存储系统，通过提供多种键值数据类型来适应不同场景下的缓存与存储需求.

> 1.可以为每个key设置超时时间；
>
> 2.可以通过列表类型来实现分布式队列的操作
>
> 3.支持发布订阅的消息模式

> 提供了很多命令与redis进行交互。单线程高的原因：采用了epoll模型

他的相关功能有：

> 1.数据缓存（商品数据、新闻、热点数据）
>
> 2.单点登录
>
> 3.秒杀、抢购
>
> 4.网站访问排名…
>
> 5.应用的模块开发

# 3、主要特性

## 支持多数据源

> 默认支持16个数据库；可以理解为一个命名空间跟关系型数据库不一样的点.
>
> 1.redis不支持自定义数据库名词
>
> 2.每个数据库不能单独设置授权
>
> 3.每个数据库之间并不是完全隔离的。 
>
> 可以通过flushall命令清空redis实例面的所有数据库中的数据.通过  select dbid 去选择不同的数据库命名空间 。 dbid的取值范围默认是0 -15 . 可以创建相同的key，因为有不同的命名空间.

## 各种数据结构

### 字符类型

> 字符串类型是redis中最基本的数据类型，它能存储任何形式的字符串，包括二进制数据。你可以用它存储用户的邮箱、json化的对象甚至是图片。一个字符类型的key默认存储的最大容量是512M.
>
> 赋值和取值
> SET key  value
> GET key
> 递增数字 (原子递增)  --要求设置的key的值是数字类型
> incr key
> 错误的演示
> int value= get key;
> value =value +1;
> set key value;
>
> **key的设计**
> 对象类型:对象id:对象属性:对象子属性
>
> 建议对key进行分类，同步在wiki统一管理
>
> 短信重发机制：sms:limit:mobile 138。。。。。 expire 
> 操作命令：
> incryby key increment  递增指定的整数
> decr key   原子递减
> append key value   向指定的key追加字符串
> strlen  key  获得key对应的value的长度
> mget  key key..  同时获得多个key的value
> mset key value  key value  key value …
> setnx 

#### 内部数据结构

> 在Redis内部，String类型通过 **int、SDS(simple dynamic string)** 作为结构存储，int用来存放整型数据，sds存放字节/字符串和浮点型数据。

> 在C的标准字符串结构下进行了封装，用来提升基本操作的性能，同时也充分利用已有的C的标准库，简化实现逻辑。我们可以在redis的源码中【sds.h】中看到sds的结构如下；
> typedef char *sds;
>
> redis3.2分支引入了五种sdshdr类型，目的是为了满足不同长度字符串可以使用不同大小的Header，从而节省内存，每次在创建一个sds时根据sds的实际长度判断应该选择什么类型的sdshdr，不同类型的sdshdr占用的内存空间不同。
>
> 这样细分一下可以省去很多不必要的内存开销，下面是3.2的sdshdr定义.

### 列表类型 L

> list, 可以存储一个有序的字符串列表
>
> LPUSH/RPUSH： 从左边或者右边push数据
> LPUSH/RPUSH key value value …
> ｛17 20 19 18 16｝
> llen num  获得列表的长度
> lrange key  start stop   取值;  索引可以是负数， -1表示最右边的第一个元素
> lrem key count value 删除
> lset key index value 设置
> LPOP/RPOP : 取数据
> 应用场景：可以用来做分布式消息队列

> 列表类型(list)可以存储一个有序的字符串列表，常用的操作是向列表两端添加元素或者获得列表的某一个片段。
>
> 列表类型内部使用双向链表实现，所以向列表两端添加元素的时间复杂度为O(1), 获取越接近两端的元素速度就越快。这意味着即使是一个有几千万个元素的列表，获取头部或尾部的10条记录也是很快的.

#### 内部数据结构

redis3.2之前，List类型的value对象内部以linkedlist或者ziplist来实现, 当list的元素个数和单个元素的长度比较小
的时候，Redis会采用ziplist（压缩列表）来实现来减少内存占用。否则就会采用linkedlist（双向链表）结构。redis3.2之后，采用的一种叫quicklist的数据结构来存储list，列表的底层都由quicklist实现。这两种存储方式都有优缺点，双向链表在链表两端进行push和pop操作，在插入节点上复杂度比较低，但是内存开销比较大； ziplist存储在一段连续的内存上，所以存储效率很高，但是插入和删除都需要频繁申请和释放内存；

quicklist仍然是一个双向链表，只是列表的每个节点都是一个ziplist，其实就是linkedlist和ziplist的结合。quicklist中每个节点ziplist都能够存储多个数据元素，在源码中的文件为【quicklist.c】，在源码第一行中有解释为：A，doubly linked list of ziplists意思为一个由ziplist组成的双向链表；

```c
// 快速列表
struct quicklist {
    quicklistNode* head;
    quicklistNode* tail;
    long count; // 元素总数
    int nodes; // ziplist 节点的个数
    int compressDepth; // LZF 算法压缩深度
    ...
}
// 快速列表节点
struct quicklistNode {
    quicklistNode* prev;
    quicklistNode* next;
    ziplist* zl; // 指向压缩列表
    int32 size; // ziplist 的字节总数
    int16 count; // ziplist 中的元素数量
    int2 encoding; // 存储形式 2bit，原生字节数组还是 LZF 压缩存储
    ...
}

struct ziplist_compressed {
    int32 size;
    byte[] compressed_data;
}

struct ziplist {
    ...
}
```

### 散列类型 H

> hash key value  不支持数据类型的嵌套，比较适合存储对象。优惠卷
> person
> age  18
> sex   男
> name mic
> ..
> hset key field value
> hget key filed 
> hmset key filed value [filed value …]  一次性设置多个值
> hmget key field field …  一次性获得多个值
> hgetall key  获得hash的所有信息，包括key和value
> hexists key field 判断字段是否存在。 存在返回1. 不存在返回0
> hincryby
> hsetnx
> hdel key field [field …] 删除一个或者多个字段

#### 内部数据结构

> map提供两种结构来存储，一种是hashtable、另一种是前面讲的ziplist，数据量小的时候用ziplist. 在redis中，哈希表分为三层，分别是，源码地址【dict.h】。

dictEntry

管理一个key-value，同时保留同一个桶中相邻元素的指针，用来维护哈希桶的内部链；

```c++
typedef struct dictEntry {
  void *key;
  union {  //因为value有多种类型，所以value用了union来存储
    void *val;
    uint64_t u64;
    int64_t s64;
    double d;
 } v;
  struct dictEntry *next;//下一个节点的地址，用来处理碰撞，所有分配到同一索引的元素通过next指针
链接起来形成链表key和v都可以保存多种类型的数据
} dictEntry;
```

dictht

实现一个hash表会使用一个buckets存放dictEntry的地址，一般情况下通过hash(key)%len得到的值就是buckets的索引，这个值决定了我们要将此dictEntry节点放入buckets的哪个索引里,这个buckets实际上就是我们说的hash
表。dict.h的dictht结构中table存放的就是buckets的地址.

```c++
typedef struct dictht {
  dictEntry **table;//buckets的地址
  unsigned long size;//buckets的大小,总保持为 2^n
  unsigned long sizemask;//掩码，用来计算hash值对应的buckets索引
  unsigned long used;//当前dictht有多少个dictEntry节点
} dictht;
```

dict

dictht实际上就是hash表的核心，但是只有一个dictht还不够，比如rehash、遍历hash等操作，所以redis定义了
一个叫dict的结构以支持字典的各种操作，当dictht需要扩容/缩容时，用来管理dictht的迁移，以下是它的数据结
构,源码在

```C++
typedef struct dict {
  dictType *type;//dictType里存放的是一堆工具函数的函数指针，
  void *privdata;//保存type中的某些函数需要作为参数的数据
  dictht ht[2];//两个dictht，ht[0]平时用，ht[1] rehash时用
  long rehashidx; //当前rehash到buckets的哪个索引，-1时表示非rehash状态
  int iterators; //安全迭代器的计数。
} dict;
```

比如我们要讲一个数据存储到hash表中，那么会先通过murmur计算key对应的hashcode，然后根据hashcode取模得到bucket的位置，再插入到链表中.

### 集合类型 S

> set 跟list 不一样的点。 集合类型不能存在重复的数据。而且是无序的
> sadd key member [member ...] 增加数据； 如果value已经存在，则会忽略存在的值，并且返回成功加入的元素的数量.
> srem key member  删除元素
> smembers key 获得所有数据
> sdiff key key …  对多个集合执行差集运算
> sunion 对多个集合执行并集操作, 同时存在在两个集合里的所有值

> 集合类型中，每个元素都是不同的，也就是不能有重复数据，同时集合类型中的数据是无序的。一个集合类型键可以存储至多232-1个 。集合类型和列表类型的最大的区别是有序性和唯一性
>
> 集合类型的常用操作是向集合中加入或删除元素、判断某个元素是否存在。由于集合类型在redis内部是使用的值为空的散列表(hash table)，所以这些操作的时间复杂度都是O(1).

#### 内部数据结构

> Set在的底层数据结构以intset或者hashtable来存储。当set中只包含整数型的元素时，采用intset来存储，否则，采用hashtable存储，但是对于set来说，该hashtable的value值用于为NULL。通过key来存储元素.

### 有序集合 Z

> zadd key score member
> zrange key start stop [withscores] 去获得元素。 withscores是可以获得元素的分数
> 如果两个元素的score是相同的话，那么根据(0<9<A<Z<a<z) 方式从小到大
> 网站访问的前10名。

> 有序集合类型，顾名思义，和前面讲的集合类型的区别就是多了有序的功能在集合类型的基础上，有序集合类型为集合中的每个元素都关联了一个分数，这使得我们不仅可以完成插入、删除和判断元素是否存在等集合类型支持的操作，还能获得分数最高(或最低)的前N个元素、获得指定分数范围内的元素等与分数有关的操作。虽然集合中每个元素都是不同的，但是他们的分数却可以相同

#### 内部数据结构

有序集合类型，顾名思义，和前面讲的集合类型的区别就是多了有序的功能

在集合类型的基础上，有序集合类型为集合中的每个元素都关联了一个分数，这使得我们不仅可以完成插入、删除
和判断元素是否存在等集合类型支持的操作，还能获得分数最高(或最低)的前N个元素、获得指定分数范围内的元
素等与分数有关的操作。虽然集合中每个元素都是不同的，但是他们的分数却可以相同.

zset类型的数据结构就比较复杂一点，内部是以ziplist或者skiplist+hashtable来实现，这里面最核心的一个结构就
是skiplist，也就是跳表.

# 4，使用

## redis的安装

> 1.下载redis安装包 
>
> wget <http://download.redis.io/releases/redis-4.0.9.tar.gz>
>
> 2.tar -zxvf 安装包
>
> 3.在redis目录下 执行 make  (编译操作)
>
> 4.可以通过make test测试编译状态
>
> 5.make install [prefix=/path]完成安装(版本3以上参考官网安装)
>
> 启动停止redis
> ./redis-server ../redis.conf
> ./redis-cli shutdown
> 以后台进程的方式启动，修改redis.conf   daemonize =yes
>
> 连接到redis的命令 ./redis-cli -h 127.0.0.1 -p 6379
>
> 若有密码，登录后请输入：**auth 密码** 
>
> **一般不能通过外围访问，可以修改redis.conf的配置文件的bind绑定 和 protected-mode no即可。**
>
> cd异常：
> You need tcl 8.5 or newer in order to run the Redis test
> 处理办法：
> wget <http://downloads.sourceforge.net/tcl/tcl8.6.1-src.tar.gz>  
> sudo tar xzvf tcl8.6.1-src.tar.gz  -C /usr/local/  
> cd  /usr/local/tcl8.6.1/unix/  
> sudo ./configure  
> sudo make  
> sudo make install   
> yum install gcc-c++
> yum install gcc

```properties
其他命令说明
Redis-server 启动服务
Redis-cli 访问到redis的控制台
redis-benchmark 性能测试的工具
redis-check-aof aof文件进行检测的工具
redis-check-dump  rdb文件检查工具
redis-sentinel  sentinel 服务器配置
```

## 集群（master-slave）

### 集群配置

先来简单了解下redis中提供的集群策略, 虽然redis有持久化功能能够保障redis服务器宕机也能恢复并且只有少量
的数据损失，但是由于所有数据在一台服务器上，如果这台服务器出现硬盘故障，那就算是有备份也仍然不可避免
数据丢失的问题。

在实际生产环境中，我们不可能只使用一台redis服务器作为我们的缓存服务器，必须要多台实现集群，避免出现单点故障；

> 配置过程
>
> 修改slave (11.140和11.141)的redis.conf文件，增加
>
> slaveof masterip masterport
> slaveof 192.168.11.138 6379
>
> 验证：
>
> 1,./redisp-cli
> 2,info replication
> 3,replconf listening-port 6379 监听master对slave的同步命令
> 4,sync
> 5,若是考虑脏数据或者主从失联，保证数据是最新的，则slave-serve-stale-data yes

### 实现原理

> 1.slave第一次或者重连到master上以后，会向master发送一个SYNC的命令
> 2.master收到SYNC的时候，会做两件事
> ​	a)执行bgsave（rdb的快照文件）
> ​	b)master会把新收到的修改命令存入到缓冲区

### 缺点

> 没有办法对master进行动态选举

### 主从复制的方式

> 复制的作用是把redis的数据库复制多个副本部署在不同的服务器上，如果其中一台服务器出现故障，也能快速迁移到其他服务器上提供服务。
>
> 复制功能可以实现当一台redis服务器的数据更新后，自动将新的数据同步到其他服务器上主从复制就是我们常见的master/slave模式， 主数据库可以进行读写操作，当写操作导致数据发生变化时会自动将数据同步给从数据库。而一般情况下，从数据库是只读的，并接收主数据库同步过来的数据。 一个主数据库可以有多个从数据库

> 1.基于rdb文件的复制（第一次连接或者重连的时候）
> 2.无硬盘复制
> 3.增量复制
> PSYNC master run id. offset
> 集群（redis3.0以后的功能）
> 根据key的hash值取模 服务器的数量 

### 主从数据不一致

> 直接拷贝rdb文件就可以了

### 市面上提供了集群方案

> 1.redis shardding   而且jedis客户端就支持shardding操作  SharddingJedis ； 增加和减少节点的问题； pre shardding
> 3台虚拟机 redis 。但是我部署了9个节点 。每一台部署3个redis增加cpu的利用率
> 9台虚拟机单独拆分到9台服务器
> ​
> 2.codis 基于redis2.8.13分支开发了一个codis-server
> ​
> 3.twemproxy  twitter提供的开源解决方案

## 使用入门

> 在redis-Cli使用：
>
> 1.获得一个符合匹配规则的键名列表
> keys pattern  [? / * /[]]
> keys mic:hobby
>
> 2.判断一个键是否存在 ， EXISTS key 
>
> 3.type key 去获得这个key的数据结构类型

## redis的事务处理

> MULTI 去开启事务
> EXEC 去执行事务

## 过期时间

> expire key seconds  设置key的过期时间 
> ttl  获得key的过期时间

在Redis中提供了Expire命令设置一个键的过期时间，到期以后Redis会自动删除它。这个在我们实际使用过程中用
得非常多。

EXPIRE命令的使用方法为

> EXPIRE key seconds，其中seconds 参数表示键的过期时间，单位为秒。
> EXPIRE 返回值为1表示设置成功，0表示设置失败或者键不存在

如果想知道一个键还有多久时间被删除，可以使用TTL命令

TTL key

> 当键不存在时，TTL命令会返回-2
>
> 而对于没有给指定键设置过期时间的，通过TTL命令会返回-1

如果向取消键的过期时间设置（使该键恢复成为永久的），可以使用PERSIST命令，如果该命令执行成功或者成功
清除了过期时间，则返回1 。 否则返回0（键不存在或者本身就是永久的）。

> EXPIRE命令的seconds命令必须是整数，所以最小单位是1秒，如果向要更精确的控制键的过期时间可以使用
> PEXPIRE命令，当然实际过程中用秒的单位就够了。 PEXPIRE命令的单位是毫秒。即PEXPIRE key 1000与EXPIRE key 1相等；对应的PTTL以毫秒单位获取键的剩余有效时间。

还有一个针对字符串独有的过期时间设置方式：setex(String key,int seconds,String value)

### 过期删除的原理

Redis 中的主键失效是如何实现的，即失效的主键是如何删除的？实际上，Redis 删除失效主键的方法主要有两
种：

#### 消极方法（passive way）

> 在主键被访问时如果发现它已经失效，那么就删除它

#### 积极方法（active way）

周期性地从设置了失效时间的主键中选择一部分失效的主键删除。对于那些从未被查询的key，即便它们已经过期，被动方式也无法清除。因此Redis会周期性地随机测试一些key，已过期的key将会被删掉。Redis每秒会进行10次操作，具体的流程：

> \1. 随机测试 20 个带有timeout信息的key；
> \2. 删除其中已经过期的key；
> \3. 如果超过25%的key被删除，则重复执行步骤1；

这是一个简单的概率算法（trivial probabilistic algorithm），基于假设我们随机抽取的key代表了全部的key空
间。

## 发布订阅

> publish channel message
> subscribe channel [ …]
> 一般用得少，不稳定，性能开销
> redis和业务层之间加代理层：codis . twmproxy

Redis提供了发布订阅功能，可以用于消息的传输，Redis提供了一组命令可以让开发者实现“**发布/订阅**”模式(publish/subscribe) . 该模式同样可以实现进程间的消息传递，它的实现原理是：发布/订阅模式包含两种角色，分别是发布者和订阅者。

订阅者可以订阅一个或多个频道，而发布者可以向指定的频道发送消息，所有订阅此频道的订阅者都会收到该消息。

发布者发布消息的命令是PUBLISH， 用法是

PUBLISH channel message

比如向channel.1发一条消息:hello

PUBLISH channel.1 “hello”

这样就实现了消息的发送，该命令的返回值表示接收到这条消息的订阅者数量。因为在执行这条命令的时候还没有
订阅者订阅该频道，所以返回为0. 另外值得注意的是消息发送出去不会持久化，如果发送之前没有订阅者，那么后续再有订阅者订阅该频道，之前的消息就收不到了。

订阅者订阅消息的命令是

SUBSCRIBE channel [channel …]

该命令同时可以订阅多个频道，比如订阅channel.1的频道。 

SUBSCRIBE channel.1

执行SUBSCRIBE命令后客户端会进入订阅状态。

### 结构图

channel分两类，一个是普通channel、另一个是pattern channel（规则匹配）， producer1发布了一条消息
【publish abc hello】,redis server发给abc这个普通channel上的所有订阅者，同时abc也匹配上了pattern
channel的名字，所以这条消息也会同时发送给pattern channel *bc上的所有订阅者。

## redis实现分布式锁

> 数据库可以做 activemq
> 缓存 -redis  setnx
> zookeeper 

## 密码设置

> requirepass foobared

## 缓存的更新（保证缓存和数据库一致性）

> 1，先删除缓存，再更新数据库 （2PC、3PC）。
> 2，先更新数据库，更新成功后，让缓存失效。
> 3，更新数据的时候，只更新缓存，不更新数据库，然后异步调度去批量更新数据库。

## 分布式锁的实现

### 怎么实现分布式锁

> 锁是用来解决什么问题的;
>
> 1.一个进程中的多个线程，多个线程并发访问同一个资源的时候，如何解决线程安全问题。
> 2.一个分布式架构系统中的两个模块同时去访问一个文件对文件进行读写操作
> 3.多个应用对同一条数据做修改的时候，如何保证数据的安全性
>
> 在进程中，我们可以用到synchronized、lock之类的同步操作去解决，但是对于分布式架构下多进程的情况下，如何做到跨进程的锁。就需要借助一些第三方手段来完成

### 数据库

> 1.怎么去获取锁
>
> 数据库，通过唯一约束
> lock(
>   id  int(11)
>   methodName  varchar(100),
>   memo varchar(1000) 
>   modifyTime timestamp
>  unique key mn (method)  --唯一约束
> )
> 获取锁的伪代码
> try{
> exec  insert into lock(methodName,memo) values(‘method’,’desc’);    method
> return true;
> }Catch(DuplicateException e){
> return false;
> }
> 释放锁
> delete from lock where methodName=’’;
>
> 存在的需要思考的问题
>
> 1.锁没有失效时间，一旦解锁操作失败，就会导致锁记录一直在数据库中，其他线程无法再获得到锁。
> 2.锁是非阻塞的，数据的insert操作，一旦插入失败就会直接报错。没有获得锁的线程并不会进入排队队列，要想再次获得锁就要再次触发获得锁操作。
> 3.锁是非重入的，同一个线程在没有释放锁之前无法再次获得该锁。

### zookeeper实现分布式锁

> 利用zookeeper的唯一节点特性或者有序临时节点特性获得最小节点作为锁. zookeeper 的实现相对简单，通过curator客户端，已经对锁的操作进行了封装，原理如下：
>
> zookeeper的优势
>
> 1.	可靠性高、实现简单
> 2.	zookeeper因为临时节点的特性，如果因为其他客户端因为异常和zookeeper连接中断了，那么节点会被删除，意味着锁会被自动释放
> 3.	zookeeper本身提供了一套很好的集群方案，比较稳定
> 4.	释放锁操作，会有watch通知机制，也就是服务器端会主动发送消息给客户端这个锁已经被释放了

### redis

> redis中有一个setNx命令，这个命令只有在key不存在的情况下为key设置值。所以可以利用这个特性来实现分布式锁的操作

## 使用lua脚本(类似数据库使用sql)

### redis中使用lua脚本(类似数据库使用sql)

> Lua是一个高效的轻量级脚本语言，用标准C语言编写并以源代码形式开放， 其设计目的是为了嵌入应用程序中，从而为应用程序提供灵活的扩展和定制功能。
>
> 使用脚本的好处:
>
> 1.减少网络开销，在Lua脚本中可以把多个命令放在同一个脚本中运行
>
> 2.原子操作，redis会将整个脚本作为一个整体执行，中间不会被其他命令插入。换句话说，编写脚本的过程中无需担心会出现竞态条件。
>
> 3.复用性，客户端发送的脚本会永远存储在redis中，这意味着其他客户端可以复用这一脚本来完成同样的逻辑 。

### 安装使用

> <http://www.lua.org/start.html>到官网下载lua的tar.gz的源码包
> tar -zxvf lua-5.3.0.tar.gz
> 进入解压的目录：
> cd lua-5.2.0
> make linux  (linux环境下编译)
> make install
> 如果报错，说找不到readline/readline.h, 可以通过yum命令安装
> yum -y install readline-devel ncurses-devel
> 安装完以后再make linux  / make install
> 最后，直接输入 lua命令即可进入lua的控制台
> 异常注意：
> lua.c:82:31: fatal error: readline/readline.h
>
> 解决方法：
>
> 缺少libreadline-dev依赖包
> centos: yum install readline-devel
> debian: apt-get install libreadline-dev.

### lua语法

> 变量：全局、局部变量
> 逻辑表达式：+ ，-  ，~=
> 逻辑运算符：

### 开发工具

> windows下安装lua：
>
> <https://jingyan.baidu.com/article/f7ff0bfc1cd72c2e26bb13aa.html>
> SciTe ：<https://scite.en.softonic.com/download>

### Redis与Lua

> 在Lua脚本中调用Redis命令
>
> 可以使用redis.call函数调用。比如我们调用string类型的命令redis.call(‘set’,’hello’,’world’).
> redis.call 函数的返回值就是redis命令的执行结果。
>
> 前面我们介绍过redis的5中类型的数据返回的值的类型也都不一样。
>
> redis.call函数会将这5种类型的返回值转化对应的Lua的数据类型从Lua脚本中获得返回值.
>
> 在很多情况下我们都需要脚本可以有返回值，在脚本中可以使用return 语句将值返回给redis客户端，通过return语句来执行，如果没有执行return，默认返回为nil。
>
> 如何在redis.cli中执行lua脚本
>
> Redis提供了EVAL命令可以使开发者像调用其他Redis内置命令一样调用脚本。[EVAL][脚本内容] [key参数的数量][key …] [arg …]
> 可以通过key和arg这两个参数向脚本中传递数据，他们的值可以在脚本中分别使用KEYS和ARGV 这两个类型的全局变量访问。
>
> 比如我们通过脚本实现一个set命令，通过在redis客户端中调用，那么执行的语句是：
>
> lua脚本的内容为： return redis.call(‘set’,KEYS[1],ARGV[1])         //KEYS和ARGV必须大写
> eval "return redis.call('set',KEYS[1],ARGV[1])" 1 hello world
> EVAL命令是根据 key参数的数量-也就是上面例子中的1来将后面所有参数分别存入脚本中KEYS和ARGV两个表类型的全局变量。当脚本不需要任何参数时也不能省略这个参数。如果没有参数则为0
> eval "return redis.call(‘get’,’hello’)" 0
> 如何在jredis中执行lua基本
> Jedis jedis = RedisManager.getJedis() ;
> jedis.eval(luaSql,keys,argss) ;
> 或者：（通过先加载得到摘要，再运行 -- 处理lua脚本太大的缘故）
> jedis.evalsha(jedis.scriptLoad(luaSql),keys,argss);
> EVALSHA命令
> 考虑到我们通过eval执行lua脚本，脚本比较长的情况下，每次调用脚本都需要把整个脚本传给redis，比较占用带宽。为了解决这个问题，redis提供了EVALSHA命令允许开发者通过脚本内容的SHA1摘要来执行脚本。该命令的用法和EVAL一样，只不过是将脚本内容替换成脚本内容的SHA1摘要
> 1.Redis在执行EVAL命令时会计算脚本的SHA1摘要并记录在脚本缓存中
> 2.执行EVALSHA命令时Redis会根据提供的摘要从脚本缓存中查找对应的脚本内容，如果找到了就执行脚本，否则返回“NOSCRIPT No matching script,Please use EVAL”
> 通过以下案例来演示EVALSHA命令的效果
> script load "return redis.call('get','hello')"          将脚本加入缓存并生成sha1命令
> evalsha "a5a402e90df3eaeca2ff03d56d99982e05cf6574" 0
> 我们在调用eval命令之前，先执行evalsha命令，如果提示脚本不存在，则再调用eval命令

### lua脚本实战

> 实现一个针对某个手机号的访问频次，
>  以下是lua脚本，保存为phone_limit.lua
> local num=redis.call('incr',KEYS[1])
> if tonumber(num)==1 then
>    redis.call('expire',KEYS[1],ARGV[1])
>    return 1
> elseif tonumber(num)>tonumber(ARGV[2]) then
>    return 0
> else
>    return 1
> end
> 通过如下命令调用
> ./redis-cli --eval phone_limit.lua rate.limiting:13700000000 , 10 3
> 语法为 ./redis-cli --eval [lua脚本][key…]空格,空格[args…]

### 原子性

> redis的脚本执行是原子的，即脚本执行期间Redis不会执行其他命令。所有的命令必须等待脚本执行完以后才能执行。
> 为了防止某个脚本执行时间过程导致Redis无法提供服务。Redis提供了lua-time-limit参数限制脚本的最长运行时间。默认是5秒钟。
> 当脚本运行时间超过这个限制后，Redis将开始接受其他命令但不会执行（以确保脚本的原子性），而是返回BUSY的错误。

### 实践操作

> 打开两个客户端窗口
> 在第一个窗口中执行lua脚本的死循环
> eval “while true do end” 0
> 在第二个窗口中运行get hello
> 最后第二个窗口的运行结果是Busy, 可以通过script kill命令终止正在执行的脚本。如果当前执行的lua脚本对redis的数据进行了修改，比如（set）操作，那么script kill命令没办法终止脚本的运行，因为要保证lua脚本的原子性。如果执行一部分终止了，就违背了这一个原则
> 在这种情况下，只能通过 shutdown nosave命令强行终止

# 5，原理

## redis多路复用机制

linux的内核会把所有外部设备都看作一个文件来操作，对一个文件的读写操作会调用内核提供的系统命令，返回一个 file descriptor（文件描述符）。

对于一个socket的读写也会有响应的描述符，称为socketfd(socket 描述符)。而IO多路复用是指内核一旦发现进程指定的一个或者多个文件描述符IO条件准备好以后就通知该进程。

IO多路复用又称为事件驱动，操作系统提供了一个功能，当某个socket可读或者可写的时候，它会给一个通知。
当配合非阻塞socket使用时，只有当系统通知我哪个描述符可读了，我才去执行read操作，可以保证每次read都能读到有效数据。

操作系统的功能通过select/pool/epoll/kqueue之类的系统调用函数来使用，这些函数可以同时监视多个描述符的读写就绪情况，这样多个描述符的I/O操作都能在一个线程内并发交替完成，这就叫I/O多路复用，这里的复用指的是同一个线程。

多路复用的优势在于用户可以在一个线程内同时处理多个socket的 io请求，达到同一个线程同时处理多个IO请求的目的。而在同步阻塞模型中，必须通过多线程的方式才能达到目的。

Redis采用了一种非常简单的做法，单线程来处理来自所有客户端的并发请求，Redis把任务封闭在一个线程中从而避免了线程安全问题；

redis为什么是单线程？
官方的解释是，CPU并不是Redis的瓶颈所在，Redis的瓶颈主要在机器的内存和网络的带宽。那么Redis能不能处
理高并发请求呢？当然是可以的，至于怎么实现的，我们来具体了解一下。 【注意并发不等于并行，并发性I/O
流，意味着能够让一个计算单元来处理来自多个客户端的流请求。并行性，意味着服务器能够同时执行几个事情，
具有多个计算单元】

Redis 是跑在单线程中的，所有的操作都是按照顺序线性执行的，但是由于读写操作等待用户输入或输出都是阻塞
的，所以 I/O 操作在一般情况下往往不能直接返回，这会导致某一文件的 I/O 阻塞导致整个进程无法对其它客户提
供服务，而 I/O 多路复用就是为了解决这个问题而出现的。

### 几种I/O模型

了解多路复用之前，先简单了解下几种I/O模型

（1）同步阻塞IO（Blocking IO）：即传统的IO模型。
（2）同步非阻塞IO（Non-blocking IO）：默认创建的socket都是阻塞的，非阻塞IO要求socket被设置为
NONBLOCK。
（3）IO多路复用（IO Multiplexing）：即经典的Reactor设计模式，也称为异步阻塞IO，Java中的Selector和
Linux中的epoll都是这种模型。
（4）异步IO（Asynchronous IO）：即经典的Proactor设计模式，也称为异步非阻塞IO。

同步和异步、阻塞和非阻塞，到底是什么意思，感觉原理都差不多，我来简单解释一下
同步和异步，指的是用户线程和内核的交互方式
阻塞和非阻塞，指用户线程调用内核IO操作的方式是阻塞还是非阻塞

就像在Java中使用多线程做异步处理的概念，通过多线程去执行一个流程，主线程可以不用等待。而阻塞和非阻塞
我们可以理解为假如在同步流程或者异步流程中做IO操作，如果缓冲区数据还没准备好，IO的这个过程会阻塞。

## redis持久化策略

Redis支持两种方式的持久化，一种是RDB方式、另一种是AOF（append-only-file）方式。前者会根据指定的规
则“定时”将内存中的数据存储在硬盘上，而后者在每次执行命令后将命令本身记录下来。两种持久化方式可以单独
使用其中一种，也可以将这两种方式结合使用。

### RDB(快照)

RDB的持久化策略： 按照规则定时讲内从的数据同步到磁盘snapshot。

RDB的优缺点

1.使用RDB方式实现持久化，一旦Redis异常退出，就***会丢失最后一次快照以后更改的所有数据***。这个时候我们就需要根据具体的应用场景，通过组合设置自动快照条件的方式来将可能发生的数据损失控制在能够接受范围。如果数据相对来说比较重要，希望将损失降到最小，则可以使用AOF方式进行持久化

2.RDB可以最大化Redis的性能：父进程在保存RDB文件时唯一要做的就是fork出一个子进程，然后这个子进程就会处理接下来的所有保存工作，父进程无序执行任何磁盘I/O操作。同时这个也是一个缺点，如果数据集比较大的时候，fork**可以能比较耗时**，造成服务器在一段时间内停止处理客户端的请求；

快照的实现原理

> 1：redis使用fork函数复制一份当前进程的副本(子进程)
> 2：父进程继续接收并处理客户端发来的命令，而子进程开始将内存中的数据写入硬盘中的临时文件
> 3：当子进程写入完所有数据后会用该临时文件替换旧的RDB文件，至此，一次快照操作完成。 
>
> ​     注意：redis在进行快照的过程中不会修改RDB文件，只有快照结束后才会将旧的文件替换成新的，也就是说任何时候RDB文件都是完整的。 这就使得我们可以通过定时备份RDB文件来实现redis数据库的备份， RDB文件是经过压缩的二进制文件，占用的空间会小于内存中的数据，更加利于传输。整个过程中，主进程是不进行任何IO操作的，这就确保了极高的性能。如果需要进行大规模数据的恢复，且对于数据恢复的完整性不是非常敏感，那RDB方式要比AOF方式更加的高效。

#### redis在指定的情况下会触发快照

> 1.自己配置的快照规则
>
> Redis允许用户自定义快照条件，当符合快照条件时，Redis会自动执行快照操作。快照的条件可以由用户在配置文件中配置。配置格式如下
> save
> 第一个参数是时间窗口，第二个是键的个数，也就是说，在第一个时间参数配置范围内被更改的键的个数大于后面的changes时，即符合快照条件。redis默认配置了三个规则：
>
> save <seconds> <changes> 
> save 900 1  OR //当在900秒内被更改的key的数量大于1的时候，就执行快照 。
> save 300 10 OR
> save 60 10000
>
> 2.save或者bgsave
>
> save: 执行内存的数据同步到磁盘的操作，这个操作会阻塞客户端的请求。
> bgsave: 在后台异步执行快照操作，这个操作不会阻塞客户端的请求。
>
> 除了让Redis自动进行快照以外，当我们对服务进行重启或者服务器迁移我们需要人工去干预备份。redis提供了两条命令来完成这个任务。
>
> \1. save命令
> 当执行save命令时，Redis同步做快照操作，在快照执行过程中会阻塞所有来自客户端的请求。当redis内存中的数据较多时，通过该命令将导致Redis较长时间的不响应。所以不建议在生产环境上使用这个命令，而是推荐使用
> bgsave命令
>
> \2. bgsave命令
> bgsave命令可以在后台异步地进行快照操作，快照的同时服务器还可以继续响应来自客户端的请求。执行BGSAVE后，Redis会立即返回ok表示开始执行快照操作。
> 通过LASTSAVE命令可以获取最近一次成功执行快照的时间； （自动快照采用的是异步快照操作）。
>
> 3.执行flushall的时候
>
> 该命令在前面讲过，会清除redis在内存中的所有数据。执行该命令后，只要redis中配置的快照规则不为空，也就是save 的规则存在。redis就会执行一次快照操作。不管规则是什么样的都会执行。如果没有定义快照规则，就不会执行快照操作。
>
> 4.执行复制的时候
>
> 这里只需要了解当执行复制操作时，及时没有定义自动快照规则，并且没有手动执行过快照操作，它仍然会生成RDB快照文件。

#### 实践

> 修改redis.conf中的appendonly yes ; 重启后执行对数据的变更命令， 会在bin目录下生成对应的.aof文件， aof文件中会记录所有的操作命令
> 如下两个参数可以去对aof文件做优化
> auto-aof-rewrite-percentage 100  表示当前aof文件大小超过上一次aof文件大小的百分之多少的时候会进行重写。如果之前没有重写过，以启动时aof文件大小为准
> auto-aof-rewrite-min-size 64mb   限制允许重写最小aof文件大小，也就是文件大小小于64mb的时候，不需要进行优化

#### 快照文件

> 存放在bin/dump.rdb

### AOF(操作日志)

> AOF可以将Redis执行的每一条写命令追加到硬盘文件中，这一过程显然会降低Redis的性能，但大部分情况下这个影响是能够接受的，另外使用较快的硬盘可以提高AOF的性能

> ### 实践
>
> 默认情况下Redis没有开启AOF（append only file）方式的持久化，可以通过appendonly参数启用，在redis.conf中找到 appendonly yes
> 开启AOF持久化后每执行一条会更改Redis中的数据的命令后，Redis就会将该命令写入硬盘中的AOF文件。
> AOF文件的保存位置和RDB文件的位置相同，都是通过dir参数设置的，默认的文件名是apendonly.aof. 可以
>
> 在redis.conf中的属性 appendfilename appendonlyh.aof修改
> \------------------------------------------------------
>
> ```
> 修改redis.conf中的appendonly yes ; 
> 重启后执行对数据的变更命令， 会在bin目录下生成对应的.aof文件， aof文件中会记录所有的操作命令
> 如下两个参数可以去对aof文件做优化。
> auto-aof-rewrite-percentage 100  表示当前aof文件大小超过上一次aof文件大小的百分之多少的时候会进行重写。如果之前没有重写过，以启动时aof文件大小为准。
> auto-aof-rewrite-min-size 64mb   限制允许重写最小aof文件大小，也就是文件大小小于64mb的时候，不需要进行优化。
> ```
>
> ### aof重写的原理
>
> Redis 可以在 AOF 文件体积变得过大时，自动地在后台对 AOF 进行重写： 
> 重写后的新 AOF 文件包含了恢复当前数据集所需的最小命令集合。 整个重写操作是绝对安全的，因为 Redis 在创建新 AOF 文件的过程中，会继续将命令追加到现有的 AOF 文件里面，即使重写过程中发生停机，现有的 AOF 文件也不会丢失。 而一旦新 AOF 文件创建完毕，Redis 就会从旧 AOF 文件切换到新 AOF 文件，并开始对新 AOF 文件进行追加操作。AOF 文件有序地保存了对数据库执行的所有写入操作， 这些写入操作以 Redis 协议的格式保存， 因此 AOF 文件的内容非常容易被人读懂， 对文件进行分析（parse）也很轻松
> ​
>
> ### 同步磁盘数据
>
> redis每次更改数据的时候， aof机制都会将命令记录到aof文件，但是实际上由于操作系统的缓存机制，数据并没有实时写入到硬盘，而是进入硬盘缓存。再通过硬盘缓存机制去刷新到保存到文件。
> \# appendfsync always  每次执行写入都会进行同步  ， 这个是最安全但是是效率比较低的方式
> appendfsync everysec   每一秒执行
> \# appendfsync no  不主动进行同步操作，由操作系统去执行，这个是最快但是最不安全的方式
>
> ### aof文件损坏以后如何修复  
>
> 服务器可能在程序正在对 AOF 文件进行写入时停机， 如果停机造成了 AOF 文件出错（corrupt）， 那么 Redis 在重启时会拒绝载入这个 AOF 文件， 从而确保数据的一致性不会被破坏。当发生这种情况时， 可以用以下方法来修复出错的 AOF 文件：
>
> 1.为现有的 AOF 文件创建一个备份。
> 2.使用 Redis 附带的 redis-check-aof 程序，对原来的 AOF 文件进行修复。
> redis-check-aof --fix
> 3.重启 Redis 服务器，等待服务器载入修复后的 AOF 文件，并进行数据恢复。

### RDB 和 AOF ,如何选择

> 一般来说,如果对数据的安全性要求非常高的话，应该同时使用两种持久化功能。如果可以承受数分钟以内的数据丢失，那么可以只使用 RDB 持久化。有很多用户都只使用 AOF 持久化， 但并不推荐这种方式： 因为定时生成 RDB 快照（snapshot）非常便于进行数据库备份， 并且 RDB 恢复数据集的速度也要比 AOF 恢复的速度要快 。两种持久化策略可以同时使用，也可以使用其中一种。如果同时使用的话， 那么Redis重启时，会优先使用AOF文件来还原数据

## Redis内存回收策略

Redis中提供了多种内存回收策略，当内存容量不足时，为了保证程序的运行，这时就不得不淘汰内存中的一些对
象，释放这些对象占用的空间，那么选择淘汰哪些对象呢？

> 其中，默认的策略为noeviction策略，当内存使用达到阈值的时候，所有引起申请内存的命令会报错。
>
> allkeys-lru：从数据集（server.db[i].dict）中挑选最近最少使用的数据淘汰
> 适合的场景： 如果我们的应用对缓存的访问都是相对热点数据，那么可以选择这个策略
>
> allkeys-random：随机移除某个key。
> 适合的场景：如果我们的应用对于缓存key的访问概率相等，则可以使用这个策略
>
> volatile-random：从已设置过期时间的数据集（server.db[i].expires）中任意选择数据淘汰。
>
> volatile-lru：从已设置过期时间的数据集（server.db[i].expires）中挑选最近最少使用的数据淘汰。
>
> volatile-ttl：从已设置过期时间的数据集（server.db[i].expires）中挑选将要过期的数据淘汰
> 适合场景：这种策略使得我们可以向Redis提示哪些key更适合被淘汰，我们可以自己控制

> 实际上Redis实现的LRU并不是可靠的LRU，也就是名义上我们使用LRU算法淘汰内存数据，但是实际上被淘汰的键并不一定是真正的最少使用的数据，这里涉及到一个权衡的问题，如果需要在所有的数据中搜索最符合条件的数据，那么一定会增加系统的开销，Redis是单线程的，所以耗时的操作会谨慎一些。
>
> 为了在一定成本内实现相对的LRU，早期的Redis版本是基于采样的LRU，也就是放弃了从所有数据中搜索解改为采样空间搜索最优解。Redis3.0版本之后，Redis作者对于基于采样的LRU进行了一些优化，目的是在一定的成本内让结果更靠近真实的LRU。

## 哨兵机制

> sentinel
>
> 1.监控master和salve是否正常运行
>
> 2.如果master出现故障，那么会把其中一台salve数据升级为master
> ./src/redis-sentinel 
>
> sentinel.conf可以开启多个哨兵，相互监控

### 原理和作用

```
Redis哨兵(以下称哨兵)是为Redis提供一个高可靠解决方案，对一定程序上的错误，可以不需要人工干预自行解决。
哨兵功能还有监视、事件通知、配置功能。以下是哨兵的功能列表：
监控：不间断的检查主从服务是否如预期一样正常工作
事件通知：对被监视的redis实例的异常，能通知系统管理员，或者以API接口通知其他应用程序。
智能援救：当被监视的主服务异常时，哨兵会智能的把某个从服务提升为主服务，同时其他从服务与新的主服务之间的关系将得到重新的配置。应用程序将通过redis服务端重新得到新的主服务的地址并重新建立连接。
配置服务：客户端可连接哨兵的接口，获得主从服务的相关信息，如果发生改变，哨兵新通知客户端。

哨兵的分布式
哨兵是个分布式系统，通过配置文件可以多个哨兵合作，以实现它的健壮性：
1.某个主服务是否正常，需要通过多个哨兵确认，这样可保证误判的低概率。
2.当哨兵工作的时候，总会有个别哨兵不能正常运行，如个别系统出现故障，所以多个哨兵合作运行，保证了系统的健壮性。
所有的哨兵、redis实例(包括主与从)和客户端相互之间会有交互，这是一个大的分布式系统，在此文档中将由浅入深地介绍哨兵的基础概念，以便更好的理解其基本属性，然后是更复杂的特性，让你理解它是如果精确的工作。
```

## 集群的原理

> Redis Cluster中，Sharding采用slot(槽)的概念，一共分成16384个槽，这有点儿类似前面讲的pre sharding思路。
>
> 对于每个进入Redis的键值对，根据key进行散列，分配到这16384个slot中的某一个中。使用的hash算法也比较简单，就是CRC16后16384取模。Redis集群中的每个node(节点)负责分摊这16384个slot中的一部分，也就是说，每个slot都对应一个node负责处理。当动态添加或减少node节点时，需要将16384个槽做个再分配，槽中的键值也要迁移。当然，这一过程，在目前实现中，还处于半自动状态，需要人工介入。
>
> Redis集群，要保证16384个槽对应的node都正常工作，如果某个node发生故障，那它负责的slots也就失效，整个集群将不能工作。为了增加集群的可访问性，官方推荐的方案是将node配置成主从结构，即一个master主节点，挂n个slave从节点。这时，如果主节点失效，Redis Cluster会根据选举算法从slave节点中选择一个上升为主节点，整个集群继续对外提供服务。这非常类似服务器节点通过Sentinel监控架构成主从结构，只是Redis Cluster本身提供了故障转移容错的能力。

> slot（槽）的概念，在redis集群中一共会有16384个槽，根据key 的CRC16算法，得到的结果再对16384进行取模。 
> 假如有3个节点
> node1  0 5460
> node2  5461 10922
> node3  10923 16383
> ​
> 节点新增
> node4  0-1364,5461-6826,10923-12287
> ​
> 删除节点
> 先将节点的数据移动到其他节点上，然后才能执行删除

# 6，劣势

(一)缓存和数据库双写一致性问题

```
（1）更新数据库数据
（2）数据库会将操作信息写入binlog日志当中
（3）订阅程序提取出所需要的数据以及key
（4）另起一段非业务代码，获得该信息
（5）尝试删除缓存操作，发现删除失败
（6）将这些信息发送至消息队列
（7）重新从消息队列中获得该数据，重试操作。

备注说明：上述的订阅binlog程序在mysql中有现成的中间件叫canal，可以完成订阅binlog日志的功能。至于oracle中，博主目前不知道有没有现成中间件可以使用。另外，重试机制，博主是采用的是消息队列的方式。如果对一致性要求不是很高，直接在程序中另起一个线程，每隔一段时间去重试即可，这些大家可以灵活自由发挥，只是提供一个思路。
```

(二)缓存雪崩问题

```
缓存雪崩，即缓存同一时间大面积的失效，这个时候又来了一波请求，结果请求都怼到数据库上，从而导致数据库连接异常。
解决方案:
(一)给缓存的失效时间，加上一个随机值，避免集体失效。
(二)使用互斥锁，但是该方案吞吐量明显下降了。
(三)双缓存。我们有两个缓存，缓存A和缓存B。缓存A的失效时间为20分钟，缓存B不设失效时间。自己做缓存预热操作。然后细分以下几个小点
- I 从缓存A读数据库，有则直接返回
- II A没有数据，直接从B读数据，直接返回，并且异步启动一个更新线程。
- III 更新线程同时更新缓存A和缓存B。
```

(三)缓存击穿问题

```
缓存穿透，即黑客故意去请求缓存中不存在的数据，导致所有的请求都怼到数据库上，从而数据库连接异常。
解决方案:
(一)利用互斥锁，缓存失效的时候，先去获得锁，得到锁了，再去请求数据库。没得到锁，则休眠一段时间重试
(二)采用异步更新策略，无论key是否取到值，都直接返回。value值中维护一个缓存失效时间，缓存如果过期，异步起一个线程去读数据库，更新缓存。需要做缓存预热(项目启动前，先加载缓存)操作。
(三)提供一个能迅速判断请求是否有效的拦截机制，比如，利用布隆过滤器，内部维护一系列合法有效的key。迅速判断出，请求所携带的Key是否合法有效。如果不合法，则直接返回。
```

(四)缓存的并发竞争问题

```
(1)如果对这个key操作，不要求顺序
这种情况下，准备一个分布式锁，大家去抢锁，抢到锁就做set操作即可，比较简单。
(2)如果对这个key操作，要求顺序
假设有一个key1,系统A需要将key1设置为valueA,系统B需要将key1设置为valueB,系统C需要将key1设置为valueC.
期望按照key1的value值按照 valueA-->valueB-->valueC的顺序变化。这种时候我们在数据写入数据库的时候，需要保存一个时间戳。假设时间戳如下
系统A key 1 {valueA  3:00}
系统B key 1 {valueB  3:05}
系统C key 1 {valueC  3:10}
那么，假设这会系统B先抢到锁，将key1设置为{valueB 3:05}。接下来系统A抢到锁，发现自己的valueA的时间戳早于缓存中的时间戳，那就不做set操作了。以此类推。
其他方法，比如利用队列，将set方法变成串行访问也可以。总之，灵活变通。
```

# 7，异常

``` properties
1，redis (error) MOVED
 ./redis-cli -c -h 192.168.210.54 -p 7002 （连接时加-c）

2，(error) NOAUTH Authentication required.
auth 密码（连接后输入密码）

3，Redirected to slot [1074] located at 192.168.210.54:7001
(error) NOAUTH Authentication required.

4,.redis01/redis-cli -h "xxx.xxx.xxx.xxx" -p 8001 -c
登陆进去测试
xxx.xxx.xxx.xxx>set test aaa
报错(error) CLUSTERDOWN Hash slot not served
没有分配槽，因为redis集群要分配16384个槽来储存数据，那么没有分配槽则报如上错误,处理方式：
./redis-trib.rb create --replicas 1 192.168.102.241:7006 192.168.102.241:7005 192.168.102.241:7004 192.168.102.241:7003 192.168.102.241:7002 192.168.102.241:7001


```

# 8，开发注意事项

```
1，目前AI作业基本上都是单表查询，在数据量变大和请求变大的情况下，必须在数据库和应用层中间添加一级缓存，减少数据库的调用次数，合并网络调用开销。
2，排名放到redis中去计算。

使用Redis开发规范要注意如下内容：

a,合理使用集合类
使用sortedset、set、list、hash等集合类的O(N)操作时要评估当前元素个数的规模以及将来的增长规模，对于短期就可能变为大集合的key，要预估O(N)操作的元素数量，避免全量操作，可以使用HSCAN、SSCAN、ZSCAN进行渐进操作。集合元素数量过大在使用过程中会影响redis的实际性能，元素个数建议尽量不要超过5000，元素数量过大可考虑拆分成多个key进行处理。

b,合理设置过期时间
如果key没有设置超时时间，会导致一直占用内存。对于可以预估使用生命周期的key应当设置合理的过期时间或在最后一次操作时进行清理，避免垃圾数据残留redis。

c,合理利用批操作命令
在redis使用过程中，要正视网络往返时间，合理利用批量操作命令，减少通讯时延和redis访问频次。redis为了减少大量小数据CMD操作的网络通讯时间开销 RTT (Round Trip Time)，支持多种批操作技术：
MSET/HMSET等都支持一次输入多个key，LPUSH/RPUSH/SADD等命令都支持一次输入多个value,也要注意每次操作数量不要过多,建议控制在500个以内；
PipeLining 模式 可以一次输入多个指令。redis提供一个 pipeline 的管道操作模式，将多个指令汇总到队列中批量执行，可以减少tcp交互产生的时间，一般情况下能够有10%~30%不等的性能提升；
更快的是Lua Script模式，还可以包含逻辑。redis内嵌了 lua 解析器，可以执行lua 脚本，脚本可以通过eval等命令直接执行，也可以使用script load等方式上传到服务器端的script cache中重复使用。

d,减少不必要的请求
ttl命令对于key不存在的情况会返回-2，若key不存在则不需要再调用del命令，可减少无效请求。
redis的所有请求对于不存在的key都会有输出返回，合理利用返回值处理，避免不必要的请求，提升业务吞吐量。

e,避免value设置过大
集合信息序列化后用redis的字符串类型存储，使用的时候再反序列化成对象列表使用，大小超过1MB，在网络传输的时候由于数据比较大会触发拆包，会降低redis的吞吐量。数量比较多时可以考虑改用hash结构存储，每一个field是商品id,value是该商品对象，如果数量较大可使用hscan获取。String类型尽量控制在10KB以内。虽然redis对单个key可以缓存的对象长度能够支持的很大，但是实际使用场合一定要合理拆分过大的缓存项，1k 基本是redis性能的一个拐点。当缓存项超过10k、100k、1m性能下降会特别明显。关于吞吐量与数据大小的关系可见下面官方网站提供的示意图。

f,设计规范的key名
1,可读性
以业务名为前缀，用冒号分隔，可使用业务名：子业务名：id的结构命名，子业务下多单词可再用下划线分隔
举例：ai作业-试题-id，可命名为 AIHOMEWORK:QUESTION:ID:CNBJTW0200000978968
2,简洁性
保证语义的前提下，控制key的长度，当key较多时，内存占用也不容忽视
3,不包含转义字符
不包含空格、换行、单双引号以及其他转义字符

g,留心禁用命令
keys、monitor、flushall、flushdb应当通过redis的rename机制禁掉命令，若没有禁用，开发人员要谨慎使用。其中flushall、flushdb会清空redis数据；keys命令可能会引起慢日志；monitor命令在开启的情况下会降低redis的吞吐量，根据压测结果大概会降低redis50%的吞吐量，越多客户端开启该命令，吞吐量下降会越多。
keys和monitor在一些必要的情况下还是有助于排查线上问题的，建议可在重命名后在必要情况下由redis相关负责人员在redis备机使用，monitor命令可借助redis-faina等脚本工具进行辅助分析，能更快排查线上ops飙升等问题。
```

