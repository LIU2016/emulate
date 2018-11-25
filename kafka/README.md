[TOC]

# 一、介绍和安装集群

# 场景

> 1，消息分发 - 触发
> 2，用户数据分析

## 主要用途

> 消息中间件
>
> 流式计算处理
>
> 日志

### 官网

> <http://kafka.apache.org/>
>
> 下载地址：<http://kafka.apache.org/downloads>

## windows下的kafka

> 启动 zookeeper : 第一次使用，需要复制 config/zoo_sampe.cfg ，并且重命名为"zoo.cfg"
>
> bin/zkServer.cmd
>
> 启动 kafka:bin/windows/kafka-server-start.bat

## linux下的Kafka安装部署以及集群

> 下载安装包
> <http://mirrors.hust.edu.cn/apache/kafka/0.11.0.1/kafka_2.12-0.11.0.1.tgz>
> 安装过程
> 0.前提安装zookeeper或者使用内嵌zk
> 1.tar -zxvf解压安装包
> 2.进入到config目录下修改server.properties
> [broker.id](http://broker.id) 保证唯一
> listeners=<PLAINTEXT://本机ip:9092>（不要指定localhost）
> zookeeper.connect
> 3.启动
> sh [kafka-server-start.sh](http://kafka-server-start.sh) -daemon ../config/server.properties
> sh [kafka-server-stop.sh](http://kafka-server-stop.sh)
> kafka目录介绍
> /bin 操作kafka的可执行脚本
> /config 配置文件
> Libs 依赖库目录
> /logs 日志数据目录，目前kafka把server端日志分为5种类型，：server，request，state，log-cleaner，controller
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

## 同类产品比较

> ActiveMQ：JMS（Java Message Service） 规范实现
>
> RabbitMQ：AMQP（Advanced Message Queue Protocol）规范实现
>
> Kafka：并非某种规范实现，它灵活和性能相对是优势

# 二、实现细节（消息、分区、日志保留策略、副本机制）

## 消息、主题、分区

> 1，消息
> 消息有key[可选，根据key做哈希，路由到指定的位置]、value ；
> 2，topic&partition
> Topic是用于存储消息的逻辑概念，可以看作一个消息集合。每个topic可以有多个生产者向其推送消息，也可以有任意多个消费者消费其中的消息。
> 每个topic可以划分多个分区（每个Topic至少有一个分区），同一topic下的不同分区包含的消息是不同的。
> 每个消息在被添加到分区时，都会被分配一个offset（称之为偏移量），它是消息在此分区中的唯一编号，kafka通过offset保证消息在分区内的顺序，offset的顺序不跨分区，即kafka只保证在同一个分区内的消息是有序的；
> Partition是以文件的形式存储在文件系统中，存储在kafka-log目录下，命名规则是：<topic_name>-<partition_id>。用partition对数据进行水平切分。若是多台节点情况，会将多partition分配到不同节点服务器。

## 日志策略

> 日志保留策略（什么时候可以被清除）
> 无论消费者是否已经消费了消息，kafka都会一直保存这些消息，但并不会像数据库那样长期保存。为了避免磁盘被占满，kafka会配置响应的保留策略（retention policy），以实现周期性地删除陈旧的消息
> kafka有两种“保留策略”：
> 1.根据消息保留的时间，当消息在kafka中保存的时间超过了指定时间，就可以被删除；
> 2.根据topic存储的数据大小，当topic所占的日志文件大小大于一个阀值，则可以开始删除最旧的消息

## 日志压缩策略

> 对相同的key的值进行合并，保证最新的value值就一个。在很多场景中，消息的key与value的值之间的对应关系是不断变化的，就像数据库中的数据会不断被修改一样，消费者只关心key对应的最新的value。我们可以开启日志压缩功能，kafka定期将相同key的消息进行合并，只保留最新的value值 

## kafka的高吞吐量的因素

> 1.顺序写的方式存储数据 ； 通过文件追加的方式。频繁的io（网络io和磁盘io）
> 2.批量发送（异步发送才有，先放在缓存中，当batch.size 、 linger.ms达到临界点时才发送）；
> 3.零拷贝：FileChannel.transferTo

## 零拷贝

> 消息从发送到落地保存，broker维护的消息日志本身就是文件目录，每个文件都是二进制保存，生产者和消费者使用相同的格式来处理。在消费者获取消息时，服务器先从硬盘读取数据到内存，然后把内存中的数据原封不动的通过socket发送给消费者。虽然这个操作描述起来很简单，但实际上经历了很多步骤：
> ▪ 操作系统将数据从磁盘读入到内核空间的页缓存
> ▪ 应用程序将数据从内核空间读入到用户空间缓存中
> ▪ 应用程序将数据写回到内核空间到socket缓存中
> ▪ 操作系统将数据从socket缓冲区复制到网卡缓冲区，以便将数据经网络发出
> 而通过“零拷贝”技术可以去掉这些没必要的数据复制操作，同时也会减少上下文切换次数

## kafka消息发送和存储可靠性机制

### 消息发送的可靠性

> 生产者发送消息到broker，有三种确认方式（request.required.acks）
> acks = 0: producer不会等待broker（leader）发送ack 。因为发送消息网络超时或broker crash(1.Partition的Leader还没有commit消息 2.Leader与Follower数据不同步)，既有可能丢失也可能会重发。
> acks = 1: 当leader接收到消息之后发送ack，丢会重发，丢的概率很小
> acks = -1: 当所有的follower都同步消息成功后发送ack.  丢失消息可能性比较低。

### 消息存储的可靠性

> 根据partition的规则进行路由，均衡存储可以水平扩展，数据分片。
> 每一条消息被发送到broker中，会根据partition规则选择被存储到哪一个partition（一般是根据key的哈希值%分区数量）。如果partition规则设置的合理，所有消息可以均匀分布到不同的partition里，这样就实现了水平扩展。
> 在创建topic时可以指定这个topic对应的partition的数量。在发送一条消息时，可以指定这条消息的key，producer根据这个key和partition机制来判断这个消息发送到哪个partition。
> kafka的高可靠性的保障来自于另一个叫副本（replication）策略，通过设置副本的相关参数，可以使kafka在性能和可靠性之间做不同的切换。

### 索引分段、日志分段

### 查看消息文件

> 查看消息存放目录，发现：
> 00000000000000000000.index  00000000000000000000.log  00000000000000000000.timeindex  leader-epoch-checkpoint
> 命令：sh [kafka-run-class.sh](http://kafka-run-class.sh)kafka.tools.DumpLogSegments --files /tmp/kafka-logs/second-1/00000000000000000000.log -print-data-log

### 一个group中的消息为什么只被消费一次

> 因为：offset（即__consumer_offsets-X(0~49)），就是消费指针。
>
> 求当前消费的offset存放的分区物理位置
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

## kafka的消费分区策略

> 在kafka中每个topic一般都会有很多个partitions。为了提高消息的消费速度，我们可能会启动多个consumer去消费； 同时，kafka存在consumer group的概念，也就是group.id一样的consumer，这些consumer属于一个consumer group，组内的所有消费者协调在一起来消费消费订阅主题的所有分区。同一个consumer group里面的consumer是怎么去分配该消费哪个分区里的数据，这个就设计到了kafka内部分区分配策略（Partition Assignment Strategy）
> 在 Kafka 内部存在两种默认的分区分配策略：Range（默认） 和 RoundRobin。通过：partition.assignment.strategy指定
> 分区策略：
> 1，Range策略（默认） - 范围
> 0、1，2，3，4，5 ，6
> partition num / consumer num ，余的放一个consumer
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
> ​        this.consumer.assign(Arrays.asList(p0));
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

### 副本机制

> 何为副本（不是broker，他是leader的拷贝）：保证交叉备份（两两之间相互备份，可以做到故障迁移），从而保证可靠性。
> --replication-factor  1（1表示没有副本），〉1（有）
>  bin/[kafka-topics.sh](http://kafka-topics.sh) --create --zookeeper 192.168.254.128:2181 --replication-factor 2 --partitions 3 --topic third
>
> - 选举leader
>   为什么要有leader选举？
>   减少复制的复杂度，都与leader交互就可以了。
>   什么时候有leader？
>   当有副本的时候就有了leader
>   zk的ISR（副本同步队列）：维护的是有资格的follower节点。
>   1.副本的所有节点都必须要和zookeeper保持连接状态
>   2.副本的最后一条消息的offset和leader副本的最后一条消息的offset之间的差值不能超过指定的阀值，这个阀值是可以设置的（replica.lag.max.messages）。
>   延迟就会踢出,恢复后要加入。
>   ​
>   HW&LEO（highwatermark&leo offset）
>   关于follower副本同步的过程中，还有两个关键的概念，HW(HighWatermark)和LEO(Log End Offset). 这两个参数跟ISR集合紧密关联。HW标记了一个特殊的offset，当消费者处理消息的时候，只能拉去到HW之前的消息，HW之后的消息对消费者来说是不可见的。也就是说，取partition对应ISR中最小的LEO作为HW，consumer最多只能消费到HW所在的位置。每个replica都有HW，leader和follower各自维护更新自己的HW的状态。对于leader新写入的消息，consumer不能立刻消费，leader会等待该消息被所有ISR中的replicas同步更新HW，此时消息才能被consumer消费。这样就保证了如果leader副本损坏，该消息仍然可以从新选举的leader中获取
>   LEO 是所有副本都会有的一个offset标记，它指向追加到当前副本的最后一个消息的offset。当生产者向leader副本追加消息的时候，leader副本的LEO标记就会递增；当follower副本成功从leader副本拉去消息并更新到本地的时候，follower副本的LEO就会增加

# 三、客户端操作

## linux下kafka的客户端基本命令操作

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

## windows下客户端操作

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

## kafka Java api使用

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



## Spring Kafka

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

## Spring Boot Kafka

### 自动装配器：KafkaAutoConfiguration

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

### 创建生产者

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