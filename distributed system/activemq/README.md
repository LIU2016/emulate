[TOC]

# 一、ActiveMQ简介及作用

ActiveMQ是Apache开源基金会研发的消息中间件。是完全支持JMS1.1和J2EE1.4规范的JMS provider实现。它主要应用在分布式系统架构中，帮助构建高可用、高性能、可伸缩的企业级面向消息服务的系统。

## 应用场景

异步消息，应用解耦，流量削峰

![1543122225523](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1543122225523.png)

# 二、安装使用

## 安装

> \1. 下载activeMq安装包
> \2. tar -zxvf **.tar.gz
> \3. sh bin/activemq start 启动activeMQ服务
> \4. 登录 默认账号密码 ：admin/admin​
> \5. 参考：<http://activemq.apache.org/getting-started.html>

## java客户端操作

0，简单演示用阻塞的方式，如下，非阻塞方式可以通过实现MessgeListener来处理。
1，引用jar：

``` xml
<dependency>
<groupId>org.apache.activemq</groupId>
<artifactId>activemq-all</artifactId>
<version>5.15.0</version>
</dependency>
```

### 2，P2P 模型

2.1，简单消息生产者：

```java
public static void main(String[] args) {
ConnectionFactory connectionFactory=new ActiveMQConnectionFactory("" +
"<tcp://192.168.254.128:61616>");
Connection connection=null;
try {
//创建连接
connection=connectionFactory.createConnection();
connection.start();
Session session=connection.createSession(Boolean.TRUE, Session.AUTO_ACKNOWLEDGE);
//创建队列（如果队列已经存在则不会创建，myQueue是队列名称）
//destination表示目的地
Destination destination=session.createQueue("myQueue");
//创建消息发送者
MessageProducer producer=session.createProducer(destination);
TextMessage textMessage=session.createTextMessage("hello,world");
producer.send(textMessage);
session.commit();
session.close();
} catch (JMSException e) {
e.printStackTrace();
}finally {
if(connection!=null){
try {
connection.close();
} catch (JMSException e) {
e.printStackTrace();
}
}
}
}
```

2.2，简单消息消费者 -- 这里是阻塞监听

``` java
public static void main(String[] args) {
ConnectionFactory connectionFactory = new ActiveMQConnectionFactory("" +
"<tcp://192.168.254.128:61616>");
Connection connection = null;
try {
//创建连接
connection = connectionFactory.createConnection();
connection.start();
Session session = connection.createSession(Boolean.TRUE, Session.AUTO_ACKNOWLEDGE);
//创建队列（如果队列已经存在则不会创建， first-queue是队列名称）
//destination表示目的地
Destination destination = session.createQueue("myQueue");
//创建消息接收者
MessageConsumer consumer = session.createConsumer(destination);
TextMessage textMessage = (TextMessage) consumer.receive();
System.out.println(textMessage.getText());
session.commit();
session.close();
} catch (JMSException e) {
e.printStackTrace();
} finally {
if (connection != null) {
try {
connection.close();
} catch (JMSException e) {
e.printStackTrace();
}
}
}
}
```

### 3，JMS （pub/sub）模型

3.1，生产端

``` java
public static void main(String[] args) {
ConnectionFactory connectionFactory=new ActiveMQConnectionFactory("" +
"<tcp://192.168.254.128:61616>");
Connection connection=null;
try {
//创建连接
connection=connectionFactory.createConnection();
connection.start();
Session session=connection.createSession(Boolean.TRUE, Session.AUTO_ACKNOWLEDGE);
//创建队列（如果队列已经存在则不会创建， first-queue是队列名称）
//destination表示目的地
Destination destination=session.createTopic("first-topic");
//创建消息发送者
MessageProducer producer=session.createProducer(destination);
TextMessage textMessage=session.createTextMessage("今天心情，晴转多云");
producer.send(textMessage);
session.commit();
session.close();
} catch (JMSException e) {
e.printStackTrace();
}finally {
if(connection!=null){
try {
connection.close();
} catch (JMSException e) {
e.printStackTrace();
}
}
}
}
```

3.2，消费端

``` java
public static void main(String[] args) {
ConnectionFactory connectionFactory = new ActiveMQConnectionFactory("" +
"<tcp://192.168.254.128:61616>");
Connection connection = null;
try {
//创建连接
connection = connectionFactory.createConnection();
connection.start();
Session session = connection.createSession(Boolean.TRUE, Session.AUTO_ACKNOWLEDGE);
//创建队列（如果队列已经存在则不会创建， first-queue是队列名称）
//destination表示目的地
Destination destination = session.createTopic("first-topic");
//创建消息接收者
MessageConsumer consumer = session.createConsumer(destination);
TextMessage textMessage = (TextMessage) consumer.receive();
System.out.println(textMessage.getText());
session.commit();
session.close();
} catch (JMSException e) {
e.printStackTrace();
} finally {
if (connection != null) {
try {
connection.close();
} catch (JMSException e) {
e.printStackTrace();
}
}
}
}
```

### api总结

``` properties
ConnectionFactory                  连接工厂
Connection  			        封装客户端与JMS provider之间的一个虚拟的连接
Session					生产和消费消息的一个单线程上下文； 用于创建producer、consumer、message、queue..\
Destination				消息发送或者消息接收的目的地
MessageProducer/consumer	消息生产者/消费者
```

### mq监控

![1543122294322](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1543122294322.png)

![1543122303019](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1543122303019.png)

# 三、JMS的基本概念

> java消息服务（java Message Service）是java平台中关于面向消息中间件的API，用于在两个应用程序之间，或者分布式系统中发送消息，进行异步通讯。
> Jms是一个与具体平台无关的api，绝大多数MOM提供商都对JMS提供了支持。

## 什么是MOM

![1543122330356](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1543122330356.png)

> 面向消息的中间件，使用消息传送提供者来协调消息传输操作。 MOM需要提供API和管理工具。 
>
> 客户端调用api， 把消息发送到消息传送提供者指定的目的地。
>
> 在消息发送之后，客户端会技术执行其他的工作。并且在接收方收到这个消息确认之前。提供者一直保留该消息。

## JMS的概念和规范

![1543122431668](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1543122431668.png)

# 四、ActiveMQ域模型

## 消息传递域

![1543122484564](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1543122484564.png)



### 点对点(p2p)

> \1. 每个消息只能有一个消费者。
> \2. 消息的生产者和消费者之间没有时间上的相关性。无论消费者在生产者发送消息的时候是否处于运行状态，都可以提取消息。
> \3. 如果session关闭时，有一些消息已经收到，但还没有被签收，那么当消费者下次连接到相同的队列时，消息还会被签收。
> \4. 如果用户在receive方法中设定了消息选择条件，那么不符合条件的消息会留在队列中不会被接收。
> \5. 队列可以长久保存消息直到消息被消费者签收。消费者不需要担心因为消息丢失而时刻与jms provider保持连接状态。

### 发布订阅(pub/sub)

> \1. 每个消息可以有多个消费者
> \2. 消息的生产者和消费者之间存在时间上的相关性，订阅一个主题的消费者只能消费自它订阅之后发布的消息(之前的历史消费莫有，当然JMS规范允许提供客户端创建持久订阅
> )。
> 3.订阅可以分为非持久订阅和持久订阅. 当所有的消息必须接收的时候，则需要用到持久订阅。反之，则用非持久订阅。
> 4.消费发送默认是持久化的，事务的，所以是异步模型。​
> 5.如果是非事务模型下，使用持久化发送策略，那么该发送方式为同步模型。 或者主动设置同步才是同步模型。

#### 持久订阅

消费端设置clientId：connection.setClientID("");以及先执行给中间件设置订阅。适合消费端服务器异常无法消费消息时候。

``` java

```

### 消息组成

消息头

> 包含消息的识别信息和路由信息

消息体

> TextMessage
> MapMessage
> BytesMessage
> StreamMessage   输入输出流
> ObjectMessage  可序列化对象

属性

# 五、JMS的可靠性机制

> JMS的可靠性机制
>
> JMS消息之后被确认后，才会认为是被成功消费。消息的消费包含三个阶段： 客户端接收消息、客户端处理消息、消息被确认

## 事务性会话

![img](https://img.mubu.com/document_image/bfc62654-13ae-47ea-b8be-7081b128f84d-862021.jpg)

> 如上图，消费端设置为true的时候，消息会在消费端session.commit以后自动签收。例如：格格铺。

## 非事务性会话

![img](https://img.mubu.com/document_image/077f5d84-8e0a-4a8c-a858-5eb15283974f-862021.jpg)

![img](https://img.mubu.com/document_image/18aa4ac4-2d1c-4a84-9eeb-4d6f35a00f05-862021.jpg)

> 在该模式下，消费端设置为false的时候，消息何时被确认取决于创建会话时的应答模式，如下：
> AUTO_ACKNOWLEDGE当客户端成功从recive方法返回以后，或者[MessageListener.onMessage] 方法成功返回以后，会话会自动确认该消息。
> CLIENT_ACKNOWLEDGE客户端通过调用消息的textMessage.acknowledge();确认消息。
> 在这种模式中，如果一个消息消费者消费一共是10个消息，那么消费了5个消息，然后在第5个消息通过textMessage.acknowledge()，那么之前的所有消息都会被消确认。
> DUPS_OK_ACKNOWLEDGE延迟确认。

## 本地事务

> 在一个JMS客户端，可以使用本地事务来组合消息的发送和接收。JMS Session 接口提供了commit和rollback方法。
> JMS Provider会缓存每个生产者当前生产的所有消息，直到commit或者rollback，commit操作将会导致事务中所有的消息被持久存储；rollback意味着JMS Provider将会清除此事务下所有的消息记录。在事务未提交之前，消息是不会被持久化存储的，也不会被消费者消费；
> 事务提交意味着生产的所有消息都被发送。消费的所有消息都被确认； 
> 事务回滚意味着生产的所有消息被销毁，消费的所有消息被恢复，也就是下次仍然能够接收到发送端的消息，除非消息已经过期了

# 六、本地Broker

![img](https://img.mubu.com/document_image/35c46a8c-afc2-4da7-a651-0d0b6b51ed5a-862021.jpg)

上图：数据存储地址。

``` java
public static void main(String[] args) {
BrokerService brokerService=new BrokerService();
try {
brokerService.setUseJmx(true);
brokerService.addConnector("<tcp://localhost:61616>");
brokerService.start();
} catch (Exception e) {
e.printStackTrace();
}
}
```

# 七、日志查看

默认情况下，日志查看地址：data/activemq.log

# 八、ActiveMQ支持的传输协议

![img](https://img.mubu.com/document_image/57b7528b-12cc-4db9-a630-01da0812b6d3-862021.jpg)

client端和broker端的通讯协议
TCP(默认)、UDP 、NIO、SSL、Http（s）、vm
可以在 ​conf/activemq.xml查看或者添加协议。

# 九、ActiveMQ持久化存储

![img](https://img.mubu.com/document_image/e335b03f-36f0-488a-ab30-2f9e0d87249e-862021.jpg)

- \1. kahaDB  默认的存储方式

  ![img](https://img.mubu.com/document_image/a5099084-e87c-45cf-bd6a-731d50877bb6-862021.jpg)

  ![img](https://img.mubu.com/document_image/4051714b-fed7-4650-863e-47c4248ce73c-862021.jpg)

  优势：消息存储容量高，恢复数据快。
  ​默认的配置在activemq的conf/activemq.xml文件下。如图​
  ​<persistenceAdapter>
  ​    <kahaDB directory="${activemq.data}/kahadb"/>
  </persistenceAdapter>

- \2. AMQ 基于文件的存储方式
  优势：写入速度很快，容易恢复。
  文件默认大小是32M.
  默认的配置在activemq的conf/activemq.xml文件下。​
  <persistenceAdapter>
  ​      <amqPersistenceAdapter directory="" maxFileLength=""/>
  </persistenceAdapter>​​

- \3. JDBC 基于数据库的存储

  ![img](https://img.mubu.com/document_image/b2261771-1c22-4b41-8b01-001065e29fba-862021.jpg)

  ![img](https://img.mubu.com/document_image/2358af93-d3ad-4cd7-8e35-163d7a22368a-862021.jpg)

  ![img](https://img.mubu.com/document_image/01e748b6-e876-437d-9d0a-70cbacaff74f-862021.jpg)

  3.1，实现你要配置JDBC，要在conf/activemq.xml中配置数据库源和修改存储方式：
  ​ <bean id="mysqlDataSource" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
             <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
             <property name="url" value="jdbc:mysql://localhost:3306/activemq"/>
             <property name="username" value="root"/>
             <property name="password" value="root123"/>
  </bean>
  ​<persistenceAdapter>
             <!-- <kahaDB directory="${activemq.data}/kahadb"/>-->
             <jdbcPersistenceAdapter dataSource="#mysqlDataSource" createTablesOnStartup="true"/>
   </persistenceAdapter>
  3.2，在lib下添加jar包：commons-dbcp，commons-pool，mysql-connector-java等3个jar包。
  3.3，​​sh bin/activemq start
  3.4，此时在数据库中会有如下表自动生成：​
  ​ ​ACTIVEMQ_ACKS ： 存储持久订阅的信息
  ACTIVEMQ_LOCK ： 锁表（用来做集群的时候，实现master选举的表）
  ACTIVEMQ_MSGS ： 消息表
  ​3.5，当我们使用生产者生产消息时，会在ACTIVEMQ_MSGS产生数据
  3.6，当我们使用消费者消费该消息时，​ACTIVEMQ_MSGS表会去掉该消息。
  ​3.7，当然这里的JDBC store方式对性能不太好，可能导致最后的瓶颈都在数据库这块。
  3.8，​因此还提供了JDBC message store with ActiveMQ journal方式（就是提供缓存的方式不实时从数据库中操作数据，而是通过缓存的方式）
  JDBC Message store with activeMQ journal
  1. 引入了快速缓存机制，缓存到Log文件中。
  2. 性能会比jdbc store要好。
  3. JDBC Message store with activeMQ journal 不能应用于master/slave模式。

- 4.Memory基于内存的存储方式

- 5.LevelDB（activeMQ5.8 以后引入的持久化策略。通常用于集群配置）下节处理

# 十、ActiveMQ的网络连接（高性能策略）

activeMQ如果要实现扩展性和高可用性的要求的话，就需要用用到网络连接模式

使用NetworkConnector做网络连接

![img](https://img.mubu.com/document_image/5a92b18e-d42a-4d42-9322-657e9c3d40b6-862021.jpg)

主要用来配置broker与broker之间的通信连接，服务器S1和S2通过NewworkConnector相连。

## 包含静态连接和动态连接

### 静态网络连接

![img](https://img.mubu.com/document_image/381496cc-20a2-4d09-8527-b2ab2e4a5f17-862021.jpg)

![img](https://img.mubu.com/document_image/9653ef36-d097-4888-8cfa-8cb43f9a747d-862021.jpg)

![img](https://img.mubu.com/document_image/fdecba82-9511-432b-bef2-22f97067836c-862021.jpg)

修改activemq.xml，增加如下内容:
​ <networkConnectors>
​        <networkConnector uri="<static://(tcp://192.168.254.128:61616,192.168.254.133:61616)>"></networkConnector>
 </networkConnectors>
注意：
先检查防火墙，不然会有图1报错。
其次，配置完重启后查看管理平台network会看到另外一台服务器的数据。
（实现双机热备，同时提供服务。即生产者的消息数据发送给broker1后，连接broker2的消费者A也能消费这些数据，这时这些消息会从broker1转移到broker2，若此时A只是消费了其中一部分消息，那么就会剩余部分消息到broker2。这时，broker2当机了，由于采用容错链接，A会连接到broker1上，但这台服务器上没有消息，所以无法消费，消息就丢失了。当broker2重启后，我们采用消息回流，这时消息就要可以回到broker1上，供A消费。）

丢失的消息的处理办法

![img](https://img.mubu.com/document_image/85818490-9409-44b8-8a89-62925ec93c95-862021.jpg)

从5.6版本开始，在destinationPolicy上新增了一个选项replayWhenNoConsumers属性，
​这个属性可以用来解决当broker1上有需要转发的消息但是没有消费时，把消息回流到它原始的broker。
​同时把enableAudit设置为false，为了防止消息回流后被当作重复消息而不被分发。
分别在两台服务器通过如上在activeMQ.xml中配置即可完成消息回流处理。

容错连接
brokerUrl写成：failover:(<tcp://IP1:61616,tcp://IP2:61616)?randomize:false即可>。
作用是负载均衡。

### 动态网络连接

当broker太多的时候，网络配置太麻烦。所以需要动态网络连接。mutilcast组播的方式，发送给组内的所有broker。

# 十一、高可用的方案

> 上一节中说的networkConnector是一个高性能的方案，但并不是一个高可用的方案。
> 原因是在networkConnector这种方案下，broker节点有消费者，消息才会转移到该broker，否则只会停留在生产者对应的某个broker。若这个broker挂掉了，就不能保证消息即时消费。

高可用的方案（zookeeper+activemq）2n+1

## 主备

1，前置条件：

> 准备3台服务器（254.128，254.132，254.134）
>
> 取消之前配置的静态网络连接
>
> 搭建zk分布式，这里不详细展开。leader(128) ，follower(132)，observer(134)

![img](https://img.mubu.com/document_image/3c4f0914-dc2f-4aff-b879-e4baa048f447-862021.jpg)

![img](https://img.mubu.com/document_image/dc1ae6f9-ba0b-4567-be61-95c420191c83-862021.jpg)

![img](https://img.mubu.com/document_image/af5a83bf-ac94-49e6-b867-a74d67822fe9-862021.jpg)

2，搭建activemq集成到zk。

将activemq的安装包上传到各个服务器。

修改activemq的配置conf/activemq.xml文件

``` xml
 <persistenceAdapter>
            <!--<kahaDB directory="${activemq.data}/kahadb"/>-->
             <replicatedLevelDB 
directory="${activemq.data}/levelDB" <!--数据存储-->
replicas="2" <!--必须成活的总的节点数：计算公式（replicas/2）+1  ， 当replicas的值为2的时候， 最终的结果是2. 表示集群中至少有2台是启动的-->
bind="<tcp://0.0.0.0:61615>" <!--用来负责slave和master的数据同步的端口和ip-->
                             zkAddress="192.168.254.128,192.168.254.134,192.168.254.132" <!--表示zk的服务端地址-->
                             hostname="192.168.254.132" <!--本机ip-->
                             zkPath="/activemq/leveldb"/>
</persistenceAdapter>
```

顺序启动各个服务器上activemq，然后打开zk的客户端查看是否存在节点（都是临时节点，ephemeralOwner有sessionId值）。

![img](https://img.mubu.com/document_image/e502dd08-8c62-4a4b-87d6-fb07b4e71d44-862021.jpg)

此时查看activemq的master节点，根据zk的节点可以判断000000000节点对应的是mq的master节点，访问：<http://192.168.254.128:8161>（其他节点是访问不到的。只要master挂掉后，才会选取新的节点对外提供服务。）

![img](https://img.mubu.com/document_image/0300f479-e8f8-47b1-a398-8622c7bdb13e-862021.jpg)

![img](https://img.mubu.com/document_image/e36c8932-2dcc-4569-a672-bef19e22bb6c-862021.jpg)

停止128服务器后，选举132为master

![img](https://img.mubu.com/document_image/a6d69c78-5d05-45e8-8c29-b202ad0e4f2f-862021.jpg)

## 其他的主从方案

1，jdbc存储（基于LOCK锁表的操作来实现master/slave）
2，基于共享文件系统的主从方案（挂载网络磁盘，将数据文件保存到指定磁盘上即可完成master/slave模式）

# 十二、监控 - hawtio 略