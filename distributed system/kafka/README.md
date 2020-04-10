[TOC]

# 1，背景

```
活动流数据是几乎所有站点在对其网站使用情况做报表时都要用到的数据中最常规的部分。活动数据包括页面访问量（Page View）、被查看内容方面的信息以及搜索情况等内容。这种数据通常的处理方式是先把各种活动以日志的形式写入某种文件，然后周期性地对这些文件进行统计分析。运营数据指的是服务器的性能数据（CPU、IO使用率、请求时间、服务日志等等数据)。运营数据的统计方法种类繁多。

为何使用消息系统，消息系统在日常的工程开发中得到大量的应用，主要是其具有如下多的优点
解耦 在项目启动之初来预测将来项目会碰到什么需求，是极其困难的。消息系统在处理过程中间插入了一个隐含的、基于数据的接口层，两边的处理过程都要实现这一接口。这允许你独立的扩展或修改两边的处理过程，只要确保它们遵守同样的接口约束。
冗余 
有些情况下，处理数据的过程会失败。除非数据被持久化，否则将造成丢失。消息队列把数据进行持久化直到它们已经被完全处理，通过这一方式规避了数据丢失风险。许多消息队列所采用的"插入-获取-删除"范式中，在把一个消息从队列中删除之前，需要你的处理系统明确的指出该消息已经被处理完毕，从而确保你的数据被安全的保存直到你使用完毕。
扩展性 因为消息队列解耦了你的处理过程，所以增大消息入队和处理的频率是很容易的，只要另外增加处理过程即可。不需要改变代码、不需要调节参数。扩展就像调大电力按钮一样简单。
灵活性 & 峰值处理能力 在访问量剧增的情况下，应用仍然需要继续发挥作用，但是这样的突发流量并不常见；如果为以能处理这类峰值访问为标准来投入资源随时待命无疑是巨大的浪费。使用消息队列能够使关键组件顶住突发的访问压力，而不会因为突发的超负荷的请求而完全崩溃。
可恢复性 系统的一部分组件失效时，不会影响到整个系统。消息队列降低了进程间的耦合度，所以即使一个处理消息的进程挂掉，加入队列中的消息仍然可以在系统恢复后被处理。
顺序保证 在大多使用场景下，数据处理的顺序都很重要。大部分消息队列本来就是排序的，并且能保证数据会按照特定的顺序来处理。Kafka保证一个Partition内的消息的有序性。
缓冲 在任何重要的系统中，都会有需要不同的处理时间的元素。例如，加载一张图片比应用过滤器花费更少的时间。消息队列通过一个缓冲层来帮助任务最高效率的执行———写入队列的处理会尽可能的快速。该缓冲有助于控制和优化数据流经过系统的速度。
异步通信 很多时候，用户不想也不需要立即处理消息。消息队列提供了异步处理机制，允许用户把一个消息放入队列，但并不立即处理它。想向队列中放入多少消息就放多少，然后在需要的时候再去处理它们。

```

# 2，什么

```
ActiveMQ：JMS（Java Message Service） 规范实现
RabbitMQ：AMQP（Advanced Message Queue Protocol）规范实现
Kafka：并非某种规范实现，它灵活和性能相对是优势
```

## 场景

> 1，消息分发 - 触发
> 2，用户数据分析

## 主要用途

> 消息中间件、流式计算处理、日志

### 官网

> <http://kafka.apache.org/>
>
> 下载地址：<http://kafka.apache.org/downloads>

# 3，主要特性

## 消息、主题、分区

> 1，消息
>
> 消息有key[可选，根据key做哈希，路由到指定的位置]、value ；
>
> 2，topic&partition
>
> Topic是用于存储消息的逻辑概念，可以看作一个消息集合。每个topic可以有多个生产者向其推送消息，也可以有任意多个消费者消费其中的消息。
>
> 每个topic可以划分多个分区（每个Topic至少有一个分区），同一topic下的不同分区包含的消息是不同的。
> 每个消息在被添加到分区时，都会被分配一个offset（称之为偏移量），它是消息在此分区中的唯一编号，kafka通过offset保证消息在分区内的顺序，offset的顺序不跨分区，即kafka只保证在同一个分区内的消息是有序的；
>
> Partition是以文件的形式存储在文件系统中，存储在kafka-log目录下，命名规则是：<topic_name>-<partition_id>。用partition对数据进行水平切分。若是多台节点情况，会将多partition分配到不同节点服务器。

# 4，使用

参考文档：

https://www.cnblogs.com/luotianshuai/p/5206662.html

## 介绍和安装集群

### kafka配置文件(conf/server.properties)

```properties 
############################ System #############################

#唯一标识在集群中的ID，要求是正数。
broker.id=0
#服务端口，默认9092
port=9092
#监听地址，不设为所有地址
host.name=debugo01
 
# 处理网络请求的最大线程数
num.network.threads=2
# 处理磁盘I/O的线程数
num.io.threads=8
# 一些后台线程数
background.threads = 4
# 等待IO线程处理的请求队列最大数
queued.max.requests = 500
 
#  socket的发送缓冲区（SO_SNDBUF）
socket.send.buffer.bytes=1048576
# socket的接收缓冲区 (SO_RCVBUF)
socket.receive.buffer.bytes=1048576
# socket请求的最大字节数。为了防止内存溢出，message.max.bytes必然要小于
socket.request.max.bytes = 104857600
 
############################# Topic #############################
# 每个topic的分区个数，更多的partition会产生更多的segment file
num.partitions=2
# 是否允许自动创建topic ，若是false，就需要通过命令创建topic
auto.create.topics.enable =true
# 一个topic ，默认分区的replication个数 ，不能大于集群中broker的个数。
default.replication.factor =1
# 消息体的最大大小，单位是字节
message.max.bytes = 1000000
 
############################# ZooKeeper #############################
# Zookeeper quorum设置。如果有多个使用逗号分割
zookeeper.connect=debugo01:2181,debugo02,debugo03
# 连接zk的超时时间
zookeeper.connection.timeout.ms=1000000
# ZooKeeper集群中leader和follower之间的同步实际
zookeeper.sync.time.ms = 2000
 
############################# Log #############################
#日志存放目录，多个目录使用逗号分割
log.dirs=/var/log/kafka
 
# 当达到下面的消息数量时，会将数据flush到日志文件中。默认10000
#log.flush.interval.messages=10000
# 当达到下面的时间(ms)时，执行一次强制的flush操作。interval.ms和interval.messages无论哪个达到，都会flush。默认3000ms
#log.flush.interval.ms=1000
# 检查是否需要将日志flush的时间间隔
log.flush.scheduler.interval.ms = 3000
 
# 日志清理策略（delete|compact）
log.cleanup.policy = delete
# 日志保存时间 (hours|minutes)，默认为7天（168小时）。超过这个时间会根据policy处理数据。bytes和minutes无论哪个先达到都会触发。
log.retention.hours=168
# 日志数据存储的最大字节数。超过这个时间会根据policy处理数据。
#log.retention.bytes=1073741824
 
# 控制日志segment文件的大小，超出该大小则追加到一个新的日志segment文件中（-1表示没有限制）
log.segment.bytes=536870912
# 当达到下面时间，会强制新建一个segment
log.roll.hours = 24*7
# 日志片段文件的检查周期，查看它们是否达到了删除策略的设置（log.retention.hours或log.retention.bytes）
log.retention.check.interval.ms=60000
 
# 是否开启压缩
log.cleaner.enable=false
# 对于压缩的日志保留的最长时间
log.cleaner.delete.retention.ms = 1 day
 
# 对于segment日志的索引文件大小限制
log.index.size.max.bytes = 10 * 1024 * 1024
#y索引计算的一个缓冲区，一般不需要设置。
log.index.interval.bytes = 4096
 
############################# replica #############################
# partition management controller 与replicas之间通讯的超时时间
controller.socket.timeout.ms = 30000
# controller-to-broker-channels消息队列的尺寸大小
controller.message.queue.size=10
# replicas响应leader的最长等待时间，若是超过这个时间，就将replicas排除在管理之外
replica.lag.time.max.ms = 10000
# 是否允许控制器关闭broker ,若是设置为true,会关闭所有在这个broker上的leader，并转移到其他broker
controlled.shutdown.enable = false
# 控制器关闭的尝试次数
controlled.shutdown.max.retries = 3
# 每次关闭尝试的时间间隔
controlled.shutdown.retry.backoff.ms = 5000
 
# 如果relicas落后太多,将会认为此partition relicas已经失效。而一般情况下,因为网络延迟等原因,总会导致replicas中消息同步滞后。如果消息严重滞后,leader将认为此relicas网络延迟较大或者消息吞吐能力有限。在broker数量较少,或者网络不足的环境中,建议提高此值.
replica.lag.max.messages = 4000
#leader与relicas的socket超时时间
replica.socket.timeout.ms= 30 * 1000
# leader复制的socket缓存大小
replica.socket.receive.buffer.bytes=64 * 1024
# replicas每次获取数据的最大字节数
replica.fetch.max.bytes = 1024 * 1024
# replicas同leader之间通信的最大等待时间，失败了会重试
replica.fetch.wait.max.ms = 500
# 每一个fetch操作的最小数据尺寸,如果leader中尚未同步的数据不足此值,将会等待直到数据达到这个大小
replica.fetch.min.bytes =1
# leader中进行复制的线程数，增大这个数值会增加relipca的IO
num.replica.fetchers = 1
# 每个replica将最高水位进行flush的时间间隔
replica.high.watermark.checkpoint.interval.ms = 5000
 
# 是否自动平衡broker之间的分配策略
auto.leader.rebalance.enable = false
# leader的不平衡比例，若是超过这个数值，会对分区进行重新的平衡
leader.imbalance.per.broker.percentage = 10
# 检查leader是否不平衡的时间间隔
leader.imbalance.check.interval.seconds = 300
# 客户端保留offset信息的最大空间大小
offset.metadata.max.bytes = 1024
 
#############################Consumer #############################
# Consumer端核心的配置是group.id、zookeeper.connect
# 决定该Consumer归属的唯一组ID，By setting the same group id multiple processes indicate that they are all part of the same consumer group.
group.id
# 消费者的ID，若是没有设置的话，会自增
consumer.id
# 一个用于跟踪调查的ID ，最好同group.id相同
client.id = <group_id>
 
# 对于zookeeper集群的指定，必须和broker使用同样的zk配置
zookeeper.connect=debugo01:2182,debugo02:2182,debugo03:2182
# zookeeper的心跳超时时间，超过这个时间就认为是无效的消费者
zookeeper.session.timeout.ms = 6000
# zookeeper的等待连接时间
zookeeper.connection.timeout.ms = 6000
# zookeeper的follower同leader的同步时间
zookeeper.sync.time.ms = 2000
# 当zookeeper中没有初始的offset时，或者超出offset上限时的处理方式 。
# smallest ：重置为最小值
# largest:重置为最大值
# anything else：抛出异常给consumer
auto.offset.reset = largest
/*
kafka + zookeeper,当消息被消费时,会向zk提交当前groupId的consumer消费的offset信息,当consumer再次启动将会从此offset开始继续消费.

在consumter端配置文件中(或者是ConsumerConfig类参数)有个"autooffset.reset"(在kafka 0.8版本中为auto.offset.reset),有2个合法的值"largest"/"smallest",默认为"largest",此配置参数表示当此groupId下的消费者,在ZK中没有offset值时(比如新的groupId,或者是zk数据被清空),consumer应该从哪个offset开始消费.
1、largest表示接受接收最大的offset(即最新消息),
2、smallest表示最小offset,即从topic的开始位置消费所有消息.
*/
 
# socket的超时时间，实际的超时时间为max.fetch.wait + socket.timeout.ms.
socket.timeout.ms= 30 * 1000
# socket的接收缓存空间大小
socket.receive.buffer.bytes=64 * 1024
#从每个分区fetch的消息大小限制
fetch.message.max.bytes = 1024 * 1024
 
# true时，Consumer会在消费消息后将offset同步到zookeeper，这样当Consumer失败后，新的consumer就能从zookeeper获取最新的offset
auto.commit.enable = true   ，项目里用false 不知道是什么原因
# 自动提交的时间间隔
auto.commit.interval.ms = 60 * 1000
 
# 用于消费的最大数量的消息块缓冲大小，每个块可以等同于fetch.message.max.bytes中数值
queued.max.message.chunks = 10
 
# 当有新的consumer加入到group时,将尝试reblance,将partitions的消费端迁移到新的consumer中, 该设置是尝试的次数
rebalance.max.retries = 4
# 每次reblance的时间间隔
rebalance.backoff.ms = 2000
# 每次重新选举leader的时间
refresh.leader.backoff.ms
 
# server发送到消费端的最小数据，若是不满足这个数值则会等待直到满足指定大小。默认为1表示立即接收。
fetch.min.bytes = 1
# 若是不满足fetch.min.bytes时，等待消费端请求的最长等待时间
fetch.wait.max.ms = 100
# 如果指定时间内没有新消息可用于消费，就抛出异常，默认-1表示不受限
consumer.timeout.ms = -1
 
#############################Producer#############################
# 核心的配置包括：
# metadata.broker.list
# request.required.acks
# producer.type
# serializer.class
 
# 消费者获取消息元信息(topics, partitions and replicas)的地址,配置格式是：host1:port1,host2:port2，也可以在外面设置一个vip
metadata.broker.list
 
#消息的确认模式
# 0：不保证消息的到达确认，只管发送，低延迟但是会出现消息的丢失，在某个server失败的情况下，有点像TCP
# 1：发送消息，并会等待leader 收到确认后，一定的可靠性
# -1：发送消息，等待leader收到确认，并进行复制操作后，才返回，最高的可靠性
request.required.acks = 0
 
# 消息发送的最长等待时间
request.timeout.ms = 10000
# socket的缓存大小
send.buffer.bytes=100*1024
# key的序列化方式，若是没有设置，同serializer.class
key.serializer.class
# 分区的策略，默认是取模
partitioner.class=kafka.producer.DefaultPartitioner
# 消息的压缩模式，默认是none，可以有gzip和snappy
compression.codec = none
# 可以针对默写特定的topic进行压缩
compressed.topics=null
# 消息发送失败后的重试次数
message.send.max.retries = 3
# 每次失败后的间隔时间
retry.backoff.ms = 100
# 生产者定时更新topic元信息的时间间隔 ，若是设置为0，那么会在每个消息发送后都去更新数据
topic.metadata.refresh.interval.ms = 600 * 1000
# 用户随意指定，但是不能重复，主要用于跟踪记录消息
client.id=""
 
# 异步模式下缓冲数据的最大时间。例如设置为100则会集合100ms内的消息后发送，这样会提高吞吐量，但是会增加消息发送的延时
queue.buffering.max.ms = 5000
# 异步模式下缓冲的最大消息数，同上
queue.buffering.max.messages = 10000
# 异步模式下，消息进入队列的等待时间。若是设置为0，则消息不等待，如果进入不了队列，则直接被抛弃
queue.enqueue.timeout.ms = -1
# 异步模式下，每次发送的消息数，当queue.buffering.max.messages或queue.buffering.max.ms满足条件之一时producer会触发发送。
batch.num.messages=200
```

### windows下的kafka

> 启动 zookeeper : 第一次使用，需要复制 config/zoo_sampe.cfg ，并且重命名为"zoo.cfg"
>
> bin/zkServer.cmd
>
> 启动 kafka:bin/windows/kafka-server-start.bat

### linux下的Kafka安装部署以及集群

> 下载安装包
> <http://mirrors.hust.edu.cn/apache/kafka/0.11.0.1/kafka_2.12-0.11.0.1.tgz>
>
> 安装过程
>
> 0.前提安装zookeeper或者使用内嵌zk
>
> 1.tar -zxvf解压安装包
>
> 2.进入到config目录下修改server.properties
> [broker.id](http://broker.id) 保证唯一
> listeners=<PLAINTEXT://本机ip:9092>（不要指定localhost）
> zookeeper.connect
>
> 3.启动
> sh [kafka-server-start.sh](http://kafka-server-start.sh) -daemon ../config/server.properties
> sh [kafka-server-stop.sh](http://kafka-server-stop.sh)
>
> kafka目录介绍
> /bin 操作kafka的可执行脚本
> /config 配置文件
> Libs 依赖库目录
> /logs 日志数据目录，目前kafka把server端日志分为5种类型，：server，request，state，log-cleaner，controller
>
> 4.查看zookeeper节点变化：
> [zkCli.sh](http://zkCli.sh) -server zookeeper的IP:2181,
> 发现：
> 输入命令 ls /
> [cluster, controller_epoch, 
> controller(查看首领节点：get /controller),
> brokers(所有的节点信息), 
> zookeeper, 
> admin, 
> isr_change_notification, consumers, log_dir_event_notification, latest_producer_id_block, config]
> controller – 控制节点
> brokers  – kafka集群的broker信息 。 topic也在这里
> consumer  ids/owners/offsets

### 查看消息文件

> 查看消息存放目录，发现：
> 00000000000000000000.index  00000000000000000000.log  00000000000000000000.timeindex  leader-epoch-checkpoint
> 命令：sh [kafka-run-class.sh](http://kafka-run-class.sh)kafka.tools.DumpLogSegments --files /tmp/kafka-logs/second-1/00000000000000000000.log -print-data-log

### 一个group中的消息为什么只被消费一次

> 因为：offset（即__consumer_offsets-X(0~49)），就是消费指针。
>
> 求当前消费的offset存放的分区物理位置
>
> 1， 取模X：
> System.out.println(Math.abs("groupid".hashCode())%50);
> 2，/tmp/kakfa日志目录中的如下文件夹即为存放地址：
> __consumer_offsets-X
> 3，查看可用之前的命令：
> sh [kafka-run-class.sh](http://kafka-run-class.sh) kafka.tools.DumpLogSegments --files /tmp/kafka-logs/second-1/00000000000000000000.log -print-data-log
>
> 或者
> 通过以下操作来看看__consumer_offsets_topic是怎么存储消费进度的，__consumer_offsets_topic默认有50个分区
> 1.计算consumer group对应的hash值
> 2.获得consumer group的位移信息
>  bin/[kafka-simple-consumer-shell.sh](http://kafka-simple-consumer-shell.sh) --topic __consumer_offsets --partition 15 -broker-list 192.168.11.140:9092,192.168.11.141:9092,192.168.11.138:9092 --formatter kafka.coordinator.group.GroupMetadataManager\$OffsetsMessageFormatter
>
> offset的维护变更
> 旧版本的都是维护在zk上的，存在性能问题（0.8之前）。新版本维护在kafka的topic内部。
> ​
> 之前Kafka存在的一个非常大的性能隐患就是利用ZK来记录各个Consumer Group的消费进度（offset）。当然JVM Client帮我们自动做了这些事情，但是Consumer需要和ZK频繁交互，而利用ZK Client API对ZK频繁写入是一个低效的操作，并且从水平扩展性上来讲也存在问题。所以ZK抖一抖，集群吞吐量就跟着一起抖，严重的时候简直抖的停不下来。
> ​
> 新版Kafka已推荐将consumer的位移信息保存在Kafka内部的topic中，即__consumer_offsets 。

## 客户端操作

### linux下kafka的客户端基本命令操作

> 参考官方文档（kafka），
> 1，创建topic
> bin/[kafka-topics.sh](http://kafka-topics.sh) --create --zookeeper 192.168.254.128:2181 --replication-factor 1 --partitions 1 --topic Mytopic
> --replication-factor：副本数
> 2，查看topic
> bin/[kafka-topics.sh](http://kafka-topics.sh) --list --zookeeper 192.168.254.128:2181
> 3，消息发送
>  bin/[kafka-console-producer.sh](http://kafka-console-producer.sh) --broker-list 192.168.254.128:9092 --topic Mytopic (首领节点)
> 4，消息消费
> bin/[kafka-console-consumer.sh](http://kafka-console-consumer.sh) --bootstrap-server 192.168.254.128:9092 --topic Mytopic --from-beginning(从头到位开始接收消息)

### windows下客户端操作

> 创建主题
>
> - bin/windows/kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic gupao\
> - Created topic "gupao".
>
> 生产者发送消息
>
> - bin/windows/kafka-console-producer.bat --broker-list localhost:9092 --topic gupao
> - \>xiaomage
>
> 消费者：接受消息
>
> - bin/windows/kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic gupao --from-beginning
> - xiaomage

### kafka Java api使用

producer

```JAVA
public class KafkaProducer{
    private final org.apache.kafka.clients.producer.KafkaProducer<Integer,String> producer;
    public KafkaProducer() {
        Properties props=new Properties();
        props.put("bootstrap.servers", KafkaProperties.KAFKAF_BROKER_LIST);
        props.put("key.serializer","org.apache.kafka.common.serialization.IntegerSerializer");
        props.put("value.serializer","org.apache.kafka.common.serialization.StringSerializer");
       // props.put("partitioner.class","com.gupaoedu.kafka.chapter2.MyPartition");
        props.put("[client.id](http://client.id)",KafkaProperties.GROUP_ID);
        this.producer = new org.apache.kafka.clients.producer.KafkaProducer<Integer, String>(props);
    }
    public void sendMsg(){
        producer.send(new ProducerRecord<Integer, String>(KafkaProperties.TOPIC, 1, "message"), new Callback() {
            public void onCompletion(RecordMetadata recordMetadata, Exception e) {
                System.out.println("message send to:["+recordMetadata.partition()+"],offset:["+recordMetadata.offset()+"]");
            }
        });
    }
    public static void main(String[] args) throws IOException {
        KafkaProducer producer=new KafkaProducer();
        producer.sendMsg();
        System.in.read();
    }
}
```

consumer

```JAVA
继承 ShutdownableThread
类如下：
package com.gupaoedu.kafka.chapter2;
import kafka.utils.ShutdownableThread;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.TopicPartition;
import java.util.Arrays;
import java.util.Collections;
import java.util.Properties;
/**
 * 腾讯课堂搜索 咕泡学院
 * 加群获取视频：608583947
 * 风骚的Michael 老师
 */
public class Consumer extends ShutdownableThread{
    // High level consumer
    // Low level consumer
    private final KafkaConsumer<Integer,String> consumer;
    public Consumer() {
        super("KafkaConsumerTest",false);
        Properties properties=new Properties();
        properties.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,KafkaProperties.KAFKAF_BROKER_LIST);
        //GroupId 消息所属的分组
        properties.put(ConsumerConfig.GROUP_ID_CONFIG,"test");
        //是否自动提交消息:offset
        properties.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG,"true");
        //自动提交的间隔时间
        properties.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG,"1000");
        //设置使用最开始的offset偏移量为当前group.id的最早消息
        properties.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG,"earliest");
        //设置心跳时间
        properties.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG,"30000");
        //对key和value设置反序列化对象
        properties.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.IntegerDeserializer");
        properties.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringDeserializer");
        this.consumer=new KafkaConsumer<Integer, String>(properties);
      /*  TopicPartition p0=new TopicPartition(KafkaProperties.TOPIC,0);
        this.consumer.assign(Arrays.asList(p0));*/
    }
    public void doWork() {
       consumer.subscribe(Collections.singletonList(KafkaProperties.TOPIC));
        ConsumerRecords<Integer,String> records=consumer.poll(1000);
        for(ConsumerRecord record:records){
            System.out.println("["+record.partition()+"]receiver message:" +
                    "["+record.key()+"->"+record.value()+"],offset:"+record.offset()+"");
        }
    }
    public static void main(String[] args) {
        /*Consumer consumer=new Consumer();
        consumer.start();*/
        System.out.println(Math.abs("DemoGroup1".hashCode())%50);
    }
}
```

> 自动提交
>
> //是否自动提交消息:offset   properties.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG,"true");
> //自动提交的间隔时间
> properties.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG,"1000");
>
> 手动提交
>
> 1，手动异步
> consumer. commitASync() //手动异步ack
> 2，手动同步
> consumer. commitSync() //手动异步ack
>
> 事务一致性
>
> 将提交offset保存到数据库与其他业务数据提交放在同一个事务中处理即可。



### Spring Kafka

> 官方文档 ： <https://docs.spring.io/spring-kafka/reference/htmlsingle/>
>
> 设计模式
>
> Spring 社区对 data(spring-data) 操作，有一个基本的模式， Template 模式：
>
> - JDBC : JdbcTemplate
> - Redis : RedisTemplate
> - Kafka : KafkaTemplate
> - JMS : JmsTemplate
> - Rest: RestTemplate
> - XXXTemplate 一定实现 XXXOpeations
> - KafkaTemplate 实现了 KafkaOperations
>
> Maven 依赖
> <dependency>
>   <groupId>org.springframework.kafka</groupId>
>   <artifactId>spring-kafka</artifactId>
> </dependency>

### Spring Boot Kafka

#### 自动装配器：KafkaAutoConfiguration

其中KafkaTemplate 会被自动装配：

```JAVA 
  @Bean
    @ConditionalOnMissingBean(KafkaTemplate.class)
    public KafkaTemplate<?, ?> kafkaTemplate(
            ProducerFactory<Object, Object> kafkaProducerFactory,
            ProducerListener<Object, Object> kafkaProducerListener) {
        KafkaTemplate<Object, Object> kafkaTemplate = new KafkaTemplate<Object, Object>(
                kafkaProducerFactory);
        kafkaTemplate.setProducerListener(kafkaProducerListener);
        kafkaTemplate.setDefaultTopic(this.properties.getTemplate().getDefaultTopic());
        return kafkaTemplate;
    }
```

#### 创建生产者

增加生产者配置，修改：application.properties

```properties
全局配置：
\## Spring Kafka 配置信息
spring.kafka.bootstrapServers = localhost:9092
\### Kafka 生产者配置
\# spring.kafka.producer.bootstrapServers = localhost:9092
spring.kafka.producer.keySerializer =org.apache.kafka.common.serialization.StringSerializer
spring.kafka.producer.valueSerializer =org.apache.kafka.common.serialization.StringSerializer
```

编写发送端实现

```java
package com.gupao.springcloudstreamkafka.web.controller;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
/**
 \* Kafka 生产者 Controller
 *
 \* @author 小马哥 QQ 1191971402
 \* @copyright 咕泡学院出品
 \* @since 2017/11/12
 */
@RestController
public class KafkaProducerController {
    private final KafkaTemplate<String, String> kafkaTemplate;
    private final String topic;
    @Autowired
    public KafkaProducerController(KafkaTemplate<String, String> kafkaTemplate,
                                   @Value("${kafka.topic}") String topic) {
        this.kafkaTemplate = kafkaTemplate;
        this.topic = topic;
    }
    @PostMapping("/message/send")
    public Boolean sendMessage(@RequestParam String message) {
        kafkaTemplate.send(topic, message);
        return true;
    }
}
```

创建消费者

增加消费者配置

```properties
### Kafka 消费者配置
spring.kafka.consumer.groupId = gupao-1
spring.kafka.consumer.keyDeserializer =org.apache.kafka.common.serialization.StringDeserializer
spring.kafka.consumer.valueDeserializer =org.apache.kafka.common.serialization.StringDeserializer
```

编写消费端实现

```java
package com.gupao.springcloudstreamkafka.consumer;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
/**
 \* Kafka 消费者监听器
 *
 \* @author 小马哥 QQ 1191971402
 \* @copyright 咕泡学院出品
 \* @since 2017/11/12
 */
@Component
public class KafkaConsumerListener {
    @KafkaListener(topics ="${kafka.topic}")
    public void onMessage(String message) {
        System.out.println("Kafka 消费者监听器，接受到消息：" + message);
    }
}
```

异常问题:

> WARN [Controller id=0, targetBrokerId=1] Connection to node 1 could not be established. Broker may not be available. (org.apache.kafka.clients.NetworkClient)
> ：未关闭防火墙



#### 关键源码

KafkaBootstrapConfiguration 有 EnableKafka注解引入。spring - kafka核心入口

```java
/*
 * Copyright 2002-2016 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.springframework.kafka.annotation;

import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Role;
import org.springframework.kafka.config.KafkaListenerConfigUtils;
import org.springframework.kafka.config.KafkaListenerEndpointRegistry;

/**
 * {@code @Configuration} class that registers a {@link KafkaListenerAnnotationBeanPostProcessor}
 * bean capable of processing Spring's @{@link KafkaListener} annotation. Also register
 * a default {@link KafkaListenerEndpointRegistry}.
 *
 * <p>This configuration class is automatically imported when using the @{@link EnableKafka}
 * annotation.  See {@link EnableKafka} Javadoc for complete usage.
 *
 * @author Stephane Nicoll
 * @author Gary Russell
 *
 * @see KafkaListenerAnnotationBeanPostProcessor
 * @see KafkaListenerEndpointRegistry
 * @see EnableKafka
 */
@Configuration
public class KafkaBootstrapConfiguration {

	@SuppressWarnings("rawtypes")
	@Bean(name = KafkaListenerConfigUtils.KAFKA_LISTENER_ANNOTATION_PROCESSOR_BEAN_NAME)
	@Role(BeanDefinition.ROLE_INFRASTRUCTURE)
	public KafkaListenerAnnotationBeanPostProcessor kafkaListenerAnnotationProcessor() {
		return new KafkaListenerAnnotationBeanPostProcessor();
	}

	@Bean(name = KafkaListenerConfigUtils.KAFKA_LISTENER_ENDPOINT_REGISTRY_BEAN_NAME)
	public KafkaListenerEndpointRegistry defaultKafkaListenerEndpointRegistry() {
		return new KafkaListenerEndpointRegistry();
	}

}
```

KafkaAnnotationDrivenConfiguration / KafkaAutoConfiguration 主要的bean初始化的configuration

```java
/*
 * Copyright 2012-2016 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.springframework.boot.autoconfigure.kafka;

import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.config.KafkaListenerConfigUtils;
import org.springframework.kafka.core.ConsumerFactory;

/**
 * Configuration for Kafka annotation-driven support.
 *
 * @author Gary Russell
 * @since 1.5.0
 */
@Configuration
@ConditionalOnClass(EnableKafka.class)
class KafkaAnnotationDrivenConfiguration {

	private final KafkaProperties properties;

	KafkaAnnotationDrivenConfiguration(KafkaProperties properties) {
		this.properties = properties;
	}

	@Bean
	@ConditionalOnMissingBean
	public ConcurrentKafkaListenerContainerFactoryConfigurer kafkaListenerContainerFactoryConfigurer() {
		ConcurrentKafkaListenerContainerFactoryConfigurer configurer = new ConcurrentKafkaListenerContainerFactoryConfigurer();
		configurer.setKafkaProperties(this.properties);
		return configurer;
	}

	@Bean
	@ConditionalOnMissingBean(name = "kafkaListenerContainerFactory")
	public ConcurrentKafkaListenerContainerFactory<?, ?> kafkaListenerContainerFactory(
			ConcurrentKafkaListenerContainerFactoryConfigurer configurer,
			ConsumerFactory<Object, Object> kafkaConsumerFactory) {
		ConcurrentKafkaListenerContainerFactory<Object, Object> factory = new ConcurrentKafkaListenerContainerFactory<Object, Object>();
		configurer.configure(factory, kafkaConsumerFactory);
		return factory;
	}

	@EnableKafka
	@ConditionalOnMissingBean(name = KafkaListenerConfigUtils.KAFKA_LISTENER_ANNOTATION_PROCESSOR_BEAN_NAME)
	protected static class EnableKafkaConfiguration {

	}

}

```

ConcurrentMessageListenerContainer 消息接收的类

```
ConcurrentMessageListenerContainer
```

# 5，原理

## 日志策略

> 日志保留策略（什么时候可以被清除）
> 无论消费者是否已经消费了消息，kafka都会一直保存这些消息，但并不会像数据库那样长期保存。为了避免磁盘被占满，kafka会配置响应的保留策略（retention policy），以实现周期性地删除陈旧的消息
>
> kafka有两种“保留策略”：
> 1.根据消息保留的时间，当消息在kafka中保存的时间超过了指定时间，就可以被删除；
> 2.根据topic存储的数据大小，当topic所占的日志文件大小大于一个阀值，则可以开始删除最旧的消息

```properties
############################# Log Retention Policy #############################

# The following configurations control the disposal of log segments. The policy can
# be set to delete segments after a period of time, or after a given size has accumulated.
# A segment will be deleted whenever *either* of these criteria are met. Deletion always happens
# from the end of the log.

# The minimum age of a log file to be eligible for deletion
log.retention.hours=168

# A size-based retention policy for logs. Segments are pruned from the log as long as the remaining
# segments don't drop below log.retention.bytes.
log.retention.bytes=1073741824

# The maximum size of a log segment file. When this size is reached a new log segment will be created.
log.segment.bytes=536870912

# The interval at which log segments are checked to see if they can be deleted according
# to the retention policies
log.retention.check.interval.ms=300000


```

### 日志压缩策略

> 对相同的key的值进行合并，保证最新的value值就一个。在很多场景中，消息的key与value的值之间的对应关系是不断变化的，就像数据库中的数据会不断被修改一样，消费者只关心key对应的最新的value。
>
> 我们可以开启日志压缩功能，kafka定期将相同key的消息进行合并，只保留最新的value值 

## kafka的高吞吐量的因素

> 1.顺序写的方式存储数据 ； 通过文件追加的方式。频繁的io（网络io和磁盘io）
> 2.批量发送（异步发送才有，先放在缓存中，当batch.size 、 linger.ms达到临界点时才发送）；
> 3.零拷贝：FileChannel.transferTo

### 零拷贝

> 消息从发送到落地保存，broker维护的消息日志本身就是文件目录，每个文件都是二进制保存，生产者和消费者使用相同的格式来处理。在消费者获取消息时，服务器先从硬盘读取数据到内存，然后把内存中的数据原封不动的通过socket发送给消费者。虽然这个操作描述起来很简单，但实际上经历了很多步骤：
> ▪ 操作系统将数据从磁盘读入到内核空间的页缓存
> ▪ 应用程序将数据从内核空间读入到用户空间缓存中
> ▪ 应用程序将数据写回到内核空间到socket缓存中
> ▪ 操作系统将数据从socket缓冲区复制到网卡缓冲区，以便将数据经网络发出
> 而通过“零拷贝”技术可以去掉这些没必要的数据复制操作，同时也会减少上下文切换次数

- 减少甚至完全避免不必要的CPU拷贝，从而让CPU解脱出来去执行其他的任务
- 减少内存带宽的占用
- 通常零拷贝技术还能够减少用户空间和操作系统内核空间之间的

## kafka消息发送和存储可靠性机制 - 数据不丢失的保障

### 生产者消息发送的可靠性

> 生产者发送消息到broker，有三种确认方式（request.required.acks）
>
> acks = 0: producer不会等待broker（leader）发送ack 。因为发送消息网络超时或broker crash(1.Partition的Leader还没有commit消息 2.Leader与Follower数据不同步)，既有可能丢失也可能会重发。
>
> acks = 1: 当leader接收到消息之后发送ack，丢会重发，丢的概率很小
>
> acks = -1: 当所有的follower都同步消息成功后发送ack.  丢失消息可能性比较低。

### broker消息存储的可靠性

> 根据partition的规则进行路由，均衡存储可以水平扩展，数据分片。
>
> 每一条消息被发送到broker中，会根据partition规则选择被存储到哪一个partition（一般是根据key的哈希值%分区数量）。如果partition规则设置的合理，所有消息可以均匀分布到不同的partition里，这样就实现了水平扩展。
>
> 在创建topic时可以指定这个topic对应的partition的数量。在发送一条消息时，可以指定这条消息的key，producer根据这个key和partition机制来判断这个消息发送到哪个partition。
>
> kafka的高可靠性的保障来自于另一个叫副本（replication）策略，通过设置副本的相关参数，可以使kafka在性能和可靠性之间做不同的切换。

### 消费者消费数据的可靠性

通过offset commit 来保证数据的不丢失，kafka自己记录了每次消费的offset数值，下次继续消费的时候，会接着上次的offset进行消费。

## kafka的消费分区策略

> 在kafka中每个topic一般都会有很多个partitions。为了提高消息的消费速度，我们可能会启动多个consumer去消费； 同时，kafka存在consumer group的概念，也就是group.id一样的consumer，这些consumer属于一个consumer group，组内的所有消费者协调在一起来消费消费订阅主题的所有分区。
>
> 同一个consumer group里面的consumer是怎么去分配该消费哪个分区里的数据，这个就设计到了kafka内部分区分配策略（Partition Assignment Strategy）
>
> 在 Kafka 内部存在两种默认的分区分配策略：Range（默认） 和 RoundRobin。通过：partition.assignment.strategy指定分区策略：
>
> 1，Range策略（默认） - 范围
> 0、1，2，3，4，5 ，6
> partition num / consumer num ，余的放一个consumer
>
> 2，roundrobin策略 - 轮询
> 根据哈希值轮询分区

### Group组

> properties.put(ConsumerConfig.GROUP_ID_CONFIG,"test");
> 每一个group都能消费一次topic消息。即消息订阅（pub/sub）。这样就可以多个consumer消费同一个消息，否则同一个group中消息不能重复消费。

### 根据key设置指定分区

> 1，实现接口
> public class MyPartition implements Partitioner
>  public int partition(String topic, Object key, byte[] bytes, Object o1, byte[] bytes1, Cluster cluster) {
> ​        List<PartitionInfo> partitionerList=cluster.partitionsForTopic(topic);
> ​        int numPart=partitionerList.size(); //获得所有的分区
> ​        int hashCode=key.hashCode(); //获得key的 hashcode
> ​        return Math.abs(hashCode%numPart);
> ​    }
> ​    public void close() {
> ​    }
> ​    public void configure(Map<String, ?> map) {
> ​    }
> 2，producer和consumer参数使用
> props.put("partitioner.class","com.gupaoedu.kafka.chapter2.MyPartition");

### 指定分区消费

> TopicPartition p0=new TopicPartition(KafkaProperties.TOPIC,0);
> this.consumer.assign(Arrays.asList(p0));
>
> 这时就不用订阅了

### kafka的key为null

> 是随机的。[前提：一个Metadata的同步周期内，默认是10分钟]

### consumer rebalance(重新分区) 当以下事件发生时，Kafka 将会进行一次分区分配：

> 这个是kafka consumer 的rebalance机制。如何rebalance就涉及到前面说的分区分配策略。
>
> - 1.同一个consumer group内新增了消费者
> - 2.消费者离开当前所属的consumer group，包括shuts down 或crashes
> - 3.订阅的主题新增分区（分区数量发生变化）
> - 4.消费者主动取消对某个topic的订阅
> - 5.也就是说，把分区的所有权从一个消费者移到另外一个消费者上，
> - 异常注意
>   - <https://blog.csdn.net/changtianshuiyue/article/details/77725576>（重新分区，可能会导致消费不到新的信息），当信息处理的时间大于心跳设置的超时时间时，kafka服务端会认为消费者掉了，就会rebalance。

## 副本机制

> 何为副本（不是broker，他是leader的拷贝）：保证交叉备份（两两之间相互备份，可以做到故障迁移），从而保证可靠性。
>
> --replication-factor  1（1表示没有副本），〉1（有）
>  bin/[kafka-topics.sh](http://kafka-topics.sh) --create --zookeeper 192.168.254.128:2181 --replication-factor 2 --partitions 3 --topic third
>
> 选举leader，为什么要有leader选举？减少复制的复杂度，都与leader交互就可以了。
>
> 什么时候有leader？当有副本的时候就有了leader
>
> zk的ISR（副本同步队列）：维护的是有资格的follower节点。
> 1.副本的所有节点都必须要和zookeeper保持连接状态
> 2.副本的最后一条消息的offset和leader副本的最后一条消息的offset之间的差值不能超过指定的阀值，这个阀值是可以设置的（replica.lag.max.messages）。
>
> 延迟就会踢出,恢复后要加入。
> ​
> HW&LEO（highwatermark & leo offset）
>
> 关于follower副本同步的过程中，还有两个关键的概念，HW(HighWater mark)和LEO(Log End Offset). 这两个参数跟ISR集合紧密关联。
>
> HW标记了一个特殊的offset，当消费者处理消息的时候，只能拉去到HW之前的消息，HW之后的消息对消费者来说是不可见的。也就是说，取partition对应ISR中最小的LEO作为HW，consumer最多只能消费到HW所在的位置。
>
> 每个replica都有HW，leader和follower各自维护更新自己的HW的状态。
>
> 对于leader新写入的消息，consumer不能立刻消费，leader会等待该消息被所有ISR中的replicas同步更新HW，此时消息才能被consumer消费。这样就保证了如果leader副本损坏，该消息仍然可以从新选举的leader中获取。
>
> LEO 是所有副本都会有的一个offset标记，它指向追加到当前副本的最后一个消息的offset。当生产者向leader副本追加消息的时候，leader副本的LEO标记就会递增；当follower副本成功从leader副本拉去消息并更新到本地的时候，follower副本的LEO就会增加。

## 幂等性和事务

https://blog.csdn.net/mlljava1111/article/details/81180351

```
为了实现Producer的幂等性，Kafka引入了Producer ID（即PID）和Sequence Number。

PID。每个新的Producer在初始化的时候会被分配一个唯一的PID，这个PID对用户是不可见的。
Sequence Numbler。（对于每个PID，该Producer发送数据的每个<Topic, Partition>都对应一个从0开始单调递增的Sequence Number。
Broker端在缓存中保存了这seq number，对于接收的每条消息，如果其序号比Broker缓存中序号大于1则接受它，否则将其丢弃。这样就可以实现了消息重复提交了。但是，只能保证单个Producer对于同一个<Topic, Partition>的Exactly Once语义。不能保证同一个Producer一个topic不同的partion幂等。
```

```
所谓幂等性：对生产者而言是产生的信息发送给kafka后信息内容都是有顺序，用req number 和 pid来保证。
```



## 信息投递



# 6，劣势

https://www.cnblogs.com/qiaoyihang/p/9229854.html

https://blog.csdn.net/yjh314/article/details/77506512

```
数据重复消费：数据已经被消费但是offset没有提交。
原因1：强行kill线程，导致消费后的数据，offset没有提交。
原因2：设置offset为自动提交，关闭kafka时，如果在close之前，调用 consumer.unsubscribe() 则有可能部分offset没提交，下次重启会重复消费。
原因3（重复消费最常见的原因）：消费后的数据，当offset还没有提交时，partition就断开连接。比如，通常会遇到消费的数据，处理很耗时，导致超过了Kafka的session timeout时间（0.10.x版本默认是30秒），那么就会re-blance重平衡，此时有一定几率offset没提交，会导致重平衡后重复消费。

记录offset和恢复offset的方案
offset记录方案：
每次消费时更新每个topic+partition位置的offset在内存中，
Map<key, value>，key=topic+’-‘+partition，value=offset
当调用关闭consumer线程时，把上面Map的offset数据记录到 文件中*（分布式集群可能要记录到redis中）。
下一次启动consumer，需要读取上一次的offset信息，方法是 以当前的topic+partition为key，从上次的Map中去寻找offset。
然后使用consumer.seek()方法指定到上次的offset位置

```

# 7，异常

```properties
1，Got error produce response with correlation id 37 on topic-partition myKafkatopic2-1, retrying (1 attempts left). Error: UNKNOWN_TOPIC_OR_PARTITION 

2，WARN [Controller id=0, targetBrokerId=1] Connection to node 1 could not be established. Broker may not be available. (org.apache.kafka.clients.NetworkClient)
：未关闭防火墙
```

# 8，运维

可视化工具：

​        kafkatool

配置：

```properties
	advertised.host.name = null
	advertised.listeners = PLAINTEXT://192.168.254.138:9092
	advertised.port = null
	##
	alter.config.policy.class.name = null
	alter.log.dirs.replication.quota.window.num = 11
	alter.log.dirs.replication.quota.window.size.seconds = 1
	##
	authorizer.class.name = 
	auto.create.topics.enable = true
	auto.leader.rebalance.enable = true
	##
	background.threads = 10
	broker.id = 0
	broker.id.generation.enable = true
	broker.rack = null
	
	client.quota.callback.class = null
	
	compression.type = producer
	
	connection.failed.authentication.delay.ms = 100
	connections.max.idle.ms = 600000
	connections.max.reauth.ms = 0
	
	control.plane.listener.name = null
	
	controlled.shutdown.enable = true
	controlled.shutdown.max.retries = 3
	controlled.shutdown.retry.backoff.ms = 5000
	controller.socket.timeout.ms = 30000
	
	create.topic.policy.class.name = null
	
	default.replication.factor = 1
	
	delegation.token.expiry.check.interval.ms = 3600000
	delegation.token.expiry.time.ms = 86400000
	delegation.token.master.key = null
	delegation.token.max.lifetime.ms = 604800000
	delete.records.purgatory.purge.interval.requests = 1
	delete.topic.enable = true
	
	fetch.purgatory.purge.interval.requests = 1000
	
	group.initial.rebalance.delay.ms = 0
	group.max.session.timeout.ms = 1800000
	group.max.size = 2147483647
	group.min.session.timeout.ms = 6000
	
	host.name = 
	inter.broker.listener.name = null
	inter.broker.protocol.version = 2.3-IV1
	##
	kafka.metrics.polling.interval.secs = 10
	kafka.metrics.reporters = []
	##
	leader.imbalance.check.interval.seconds = 300
	leader.imbalance.per.broker.percentage = 10
	##
	listener.security.protocol.map = PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
	listeners = PLAINTEXT://192.168.254.138:9092
	##日志清理- 进行日志是否清理检查的时间间隔
	log.cleaner.backoff.ms = 15000
	log.cleaner.dedupe.buffer.size = 134217728
	log.cleaner.delete.retention.ms = 86400000
	log.cleaner.enable = true
	log.cleaner.io.buffer.load.factor = 0.9
	log.cleaner.io.buffer.size = 524288
	log.cleaner.io.max.bytes.per.second = 1.7976931348623157E308
	log.cleaner.max.compaction.lag.ms = 9223372036854775807
	log.cleaner.min.cleanable.ratio = 0.5
	log.cleaner.min.compaction.lag.ms = 0
	log.cleaner.threads = 1
	log.cleanup.policy = [delete]
	#
	log.dir = /tmp/kafka-logs
	log.dirs = /tmp/kafka-logs
	### 当达到下面的消息数量时，会将数据flush到日志文件中。默认10000
	log.flush.interval.messages = 9223372036854775807
	log.flush.interval.ms = null
	log.flush.offset.checkpoint.interval.ms = 60000
	log.flush.scheduler.interval.ms = 9223372036854775807
	log.flush.start.offset.checkpoint.interval.ms = 60000
	### 对于segment日志的索引文件大小限制
	log.index.interval.bytes = 4096
	## 索引计算的一个缓冲区，一般不需要设置。
	log.index.size.max.bytes = 10485760
	##
	log.message.downconversion.enable = true
	log.message.format.version = 2.3-IV1
	log.message.timestamp.difference.max.ms = 9223372036854775807
	##log.message.timestamp.type来统一指定集群中的所有topic使用哪种时间戳类型。用户也可以为单个topic设置不同的时间戳类型
	log.message.timestamp.type = CreateTime
	##
	log.preallocate = false
	##retention 消息存留时间
	log.retention.bytes = -1
	log.retention.check.interval.ms = 300000
	log.retention.hours = 168
	log.retention.minutes = null
	log.retention.ms = 100
	##达到了log.roll.ms或者log.roll.hours设置的值也会进行切割创建新的日志文件。
	log.roll.hours = 168
	log.roll.jitter.hours = 0
	log.roll.jitter.ms = null
	log.roll.ms = null
	##
	log.segment.bytes = 1073741824
	log.segment.delete.delay.ms = 60000
	
	max.connections = 2147483647
	max.connections.per.ip = 2147483647
	max.connections.per.ip.overrides = 
	max.incremental.fetch.session.cache.slots = 1000
	
	message.max.bytes = 1000012
	
	metric.reporters = []
	metrics.num.samples = 2
	metrics.recording.level = INFO
	metrics.sample.window.ms = 30000
	
	min.insync.replicas = 1
	
	num.io.threads = 8
	num.network.threads = 3
	num.partitions = 2
	num.recovery.threads.per.data.dir = 1
	num.replica.alter.log.dirs.threads = null
	num.replica.fetchers = 1
	
	offset.metadata.max.bytes = 4096
	offsets.commit.required.acks = -1
	offsets.commit.timeout.ms = 5000
	offsets.load.buffer.size = 5242880
	offsets.retention.check.interval.ms = 600000
	offsets.retention.minutes = 10080
	offsets.topic.compression.codec = 0
	offsets.topic.num.partitions = 50
	offsets.topic.replication.factor = 1
	offsets.topic.segment.bytes = 104857600
	
	password.encoder.cipher.algorithm = AES/CBC/PKCS5Padding
	password.encoder.iterations = 4096
	password.encoder.key.length = 128
	password.encoder.keyfactory.algorithm = null
	password.encoder.old.secret = null
	password.encoder.secret = null
	
	port = 9092
	principal.builder.class = null
	producer.purgatory.purge.interval.requests = 1000
	
	queued.max.request.bytes = -1
	queued.max.requests = 500
	
	quota.consumer.default = 9223372036854775807
	quota.producer.default = 9223372036854775807
	quota.window.num = 11
	quota.window.size.seconds = 1
	
	replica.fetch.backoff.ms = 1000
	replica.fetch.max.bytes = 1048576
	replica.fetch.min.bytes = 1
	replica.fetch.response.max.bytes = 10485760
	replica.fetch.wait.max.ms = 500
	replica.high.watermark.checkpoint.interval.ms = 5000
	replica.lag.time.max.ms = 10000
	replica.socket.receive.buffer.bytes = 65536
	replica.socket.timeout.ms = 30000
	replication.quota.window.num = 11
	replication.quota.window.size.seconds = 1
	
	request.timeout.ms = 30000
	reserved.broker.max.id = 1000
	
	sasl.client.callback.handler.class = null
	sasl.enabled.mechanisms = [GSSAPI]
	sasl.jaas.config = null
	sasl.kerberos.kinit.cmd = /usr/bin/kinit
	sasl.kerberos.min.time.before.relogin = 60000
	sasl.kerberos.principal.to.local.rules = [DEFAULT]
	sasl.kerberos.service.name = null
	sasl.kerberos.ticket.renew.jitter = 0.05
	sasl.kerberos.ticket.renew.window.factor = 0.8
	sasl.login.callback.handler.class = null
	sasl.login.class = null
	sasl.login.refresh.buffer.seconds = 300
	sasl.login.refresh.min.period.seconds = 60
	sasl.login.refresh.window.factor = 0.8
	sasl.login.refresh.window.jitter = 0.05
	sasl.mechanism.inter.broker.protocol = GSSAPI
	sasl.server.callback.handler.class = null
	
	security.inter.broker.protocol = PLAINTEXT
	
	socket.receive.buffer.bytes = 102400
	socket.request.max.bytes = 104857600
	socket.send.buffer.bytes = 102400
	
	ssl.cipher.suites = []
	ssl.client.auth = none
	ssl.enabled.protocols = [TLSv1.2, TLSv1.1, TLSv1]
	ssl.endpoint.identification.algorithm = https
	ssl.key.password = null
	ssl.keymanager.algorithm = SunX509
	ssl.keystore.location = null
	ssl.keystore.password = null
	ssl.keystore.type = JKS
	ssl.principal.mapping.rules = [DEFAULT]
	ssl.protocol = TLS
	ssl.provider = null
	ssl.secure.random.implementation = null
	ssl.trustmanager.algorithm = PKIX
	ssl.truststore.location = null
	ssl.truststore.password = null
	ssl.truststore.type = JKS
	
	transaction.abort.timed.out.transaction.cleanup.interval.ms = 60000
	transaction.max.timeout.ms = 900000
	transaction.remove.expired.transaction.cleanup.interval.ms = 3600000
	transaction.state.log.load.buffer.size = 5242880
	transaction.state.log.min.isr = 1
	transaction.state.log.num.partitions = 50
	transaction.state.log.replication.factor = 1
	transaction.state.log.segment.bytes = 104857600
	transactional.id.expiration.ms = 604800000
	
	unclean.leader.election.enable = false
	
	zookeeper.connect = localhost:2181
	zookeeper.connection.timeout.ms = 6000
	zookeeper.max.in.flight.requests = 10
	zookeeper.session.timeout.ms = 6000
	zookeeper.set.acl = false
	zookeeper.sync.time.ms = 2000
```

命令：

```properties
查看topic详情(leader是该partitons所在的所有broker中担任leader的broker id，每个broker都有可能成为leader)：
sh bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic test2

动态给已经修改topic的副本数replication-factor:
sh bin/kafka-reassign-partitions.sh -zookeeper localhost:2181 --reassignment-json-file increase-replication-factor.json --execute

消费的情况：
sh bin/kafka-consumer-groups.sh --describe --bootstrap-server 192.168.254.138:9092,192.168.254.139:9092 --group ctest-earliest

创建kafka主题：
sh bin/kafka-topics.sh --bootstrap-server 192.168.254.139:9092 --create --topic test_kafka_client --partitions 2 --replication-factor 2

查看位移主题的内容：
bin/kafka-console-consumer.sh --bootstrap-server 192.168.254.138:9092 --topic __consumer_offsets --formatter "kafka.coordinator.group.GroupMetadataManager\$GroupMetadataMessageFormatter" --from-beginning

查看位移主题的位移：
bin/kafka-console-consumer.sh --bootstrap-server 192.168.254.138:9092 --topic __consumer_offsets --formatter "kafka.coordinator.group.GroupMetadataManager\$OffsetsMessageFormatter" --from-beginning 

删除主题：
bin/kafka-topics.sh --bootstrap-server 192.168.254.138:9092 --delete  --topic test2

动态调整：
per-broker 参数 > cluster-wide 参数 > static 参数 > Kafka 默认值
全局动态修改属性：
bin/kafka-configs.sh --bootstrap-server 192.168.254.138:9092 --entity-type brokers --entity-default --alter --add-config unclean.leader.election.enable=true
bin/kafka-configs.sh --bootstrap-server 192.168.254.138:9092 --entity-type brokers --entity-default --describe
单个节点动态修改：
bin/kafka-configs.sh --bootstrap-server 192.168.254.138:9092 --entity-type brokers --entity-name 1 --alter --add-config unclean.leader.election.enable=false

重新分区：
bin/kafka-reassign-partitions.sh --bootstrap-server 192.168.254.138:9092 --reassignment-json-file expand-cluster-reassignment.json –execute

生产者压测：
bin/kafka-producer-perf-test.sh --num-records 1000000 --record-size 1000 --topic becket_test_3_replicas_4_partition --throughput 100000 --producer-props bootstrap.servers=192.168.254.138:9092,192.168.254.139:9092 compression.type=gzip max.in.flight.requests.per.connection=1 batch.size=80000 linger.ms=10 acks=0
kafka-producer-perf-test.sh 脚本命令的参数为：
--topic topic名称，本例为test_perf
--num-records 总共需要发送的消息数，本例为1000000
--record-size 每个记录的字节数，本例为1000
--throughput 每秒钟发送的记录数，本例为20000
--producer-props bootstrap.servers=localhost:9092
压测结果：
1000000 records sent, 41825.254088 records/sec (39.89 MB/sec), 8151.79 ms avg latency, 12599.00 ms max latency, 7856 ms 50th, 10152 ms 95th, 10639 ms 99th, 10808 ms 99.9th
调整了message.max.bytes=1000012000后的结果：
1000000 records sent, 80372.930397 records/sec (76.65 MB/sec), 141.19 ms avg latency, 686.00 ms max latency, 110 ms 50th, 371 ms 95th, 520 ms 99th, 564 ms 99.9th.

消费者压测：
bin/kafka-consumer-perf-test.sh --broker-list 192.168.254.138:9092 --zookeeper 192.168.254.138:2181 --topic s1 --messages 1000000 --fetch-size  10000  --threads 1

start.time, end.time, data.consumed.in.MB, MB.sec, data.consumed.in.nMsg, nMsg.sec, rebalance.time.ms, fetch.time.ms, fetch.MB.sec, fetch.nMsg.sec
2020-03-15 18:38:20:535, 2020-03-15 18:38:30:665, 0.0000, 0.0000, 0, 0.0000, 58, 10072, 0.0000, 0.0000

kafka-consumer-perf-test.sh 脚本命令的参数为：
--zookeeper 指定zookeeper的链接信息，本例为localhost:2181 ，如果使用新的纯java客户端则使用另外的配置
--topic 指定topic的名称，本例为test_perf
--fetch-size 指定每次fetch的数据的大小，本例为1048576，也就是1M
--messages 总共要消费的消息个数，本例为1000000，100w
```

 increase-replication-factor.json

```properties
{
        "version:": 1,
        "partitions": [{
                "topic": "test2",
                "partition": 0,
                "replicas": [0, 1]
        },{
                "topic": "test2",
                "partition": 1,
                "replicas": [0, 1]
        }]
}
```

expand-cluster-reassignment.json

```
{"version":1,
  "partitions":[{"topic":"test2","partition":0,"replicas":[5,6]},
 		{"topic":"test2","partition":1,"replicas":[5,6]}]
}
```



# 9，文档

https://kafka.apache.org/documentation/#brokerconfigs