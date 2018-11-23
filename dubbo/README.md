# 一、快速启动

## 官网地址

<http://dubbo.io/books/dubbo-user-book/preface/architecture.html>

## 项目代码





























dubbo能解决什么问题
1.怎么去维护url
通过注册中心去维护url（zookeeper、redis、memcache…）
2.F5硬件负载均衡器的单点压力比较大
软负载均衡
3.怎么去整理出服务之间的依赖关系。
自动去整理各个服务之间的依赖
4.如果服务器的调用量越来越大，服务器的容量问题怎么去评估，扩容的指标
需要一个监控平台，可以监控调用量、响应时间

dubbo是什么
dubbo是一个分布式的服务框架，提供高性能的以及透明化的RPC远程服务调用解决方法，以及SOA服务治理方案。
Dubbo的核心部分：
远程通信
集群容错
服务的自动发现
负载均衡

dubbo的架构
Provider ： tomcat
Consumer ：tomcat
Registry ：zk（dubbo在zk节点上存放服务路径地址）、redis
Monitor ：
Container ：docker

main方法怎么实现
spi、扩展机制

日志集成

admin控制台的安装
1.下载dubbo的源码
2.找到dubbo-admin
3.修改webapp/WEB-INF/dubbo.properties
dubbo.registry.address=zookeeper的集群地址
控制中心是用来做服务治理的，比如控制服务的权重、服务的路由、。。。

simple监控中心
Monitor也是一个dubbo服务，所以也会有端口和url
1，下载dubbo-monitor-simple
2，修改/conf目录下dubbo.properties ：
dubbo.registry.address=<zookeeper://192.168.11.129:2181?backup=192.168.11.137:2181,192.168.11.138:2181,192.168.11.139:2181>
3，项目的服务提供方的/order-provider.xml中
添加：<dubbo:monitor ;protocol="registry">
4，/bin/[start.sh](http://start.sh)
监控服务的调用次数、调用关系、响应事件

telnet 连接dubbo
port:20880
telnet  ip port 
ls、cd、pwd、clear、invoker

dubbo多协议

大并发使用长链接：dubbo，默认采用netty （TCP）
大数据使用短链接：hessian
可以同时提供多个协议，多个接口服务

dubbo
服务端： 
1，导包
<dependency>
​        <groupId>com.alibaba</groupId>
​        <artifactId>dubbo</artifactId>
​        <version>2.5.3</version>
​      </dependency>
​      <dependency>
​        <groupId>com.github.sgroschupf</groupId>
​        <artifactId>zkclient</artifactId>
​        <version>0.1</version>
​      </dependency>
2，<dubbo:protocol name="dubbo" port="20880"/>

hessian
服务端： 
1，配置
<dubbo:protocol name="hessian" port="8090" server="jetty" />
<!--服务发布的配置，需要暴露的服务接口-->
<dubbo:service
​           interface="com.lqd.study.IOrderServices"
​            ref="orderService"  protocol="hessian" />
2，导包：
<dependency>
​        <groupId>com.caucho</groupId>
​        <artifactId>hessian</artifactId>
​        <version>4.0.38</version>
​      </dependency>
​      <dependency>
​        <groupId>javax.servlet</groupId>
​        <artifactId>servlet-api</artifactId>
​        <version>2.5</version>
​      </dependency>
​      <dependency>
​        <groupId>org.mortbay.jetty</groupId>
​        <artifactId>jetty</artifactId>
​        <version>6.1.26</version>
​      </dependency>
客户端：不用端口指定
1，<dubbo:reference id="orderServices" interface="com.lqd.study.IOrderServices" check="true" protocol="hessian"/>
2，导包
<dependency>
​        <groupId>com.caucho</groupId>
​        <artifactId>hessian</artifactId>
​        <version>4.0.38</version>
​      </dependency>
请求地址：
<hessian://192.168.254.1:8090/com.lqd.study.IOrderServices?anyhost=true&application=order-provider&dubbo=2.5.3&interface=com.lqd.study.IOrderServices&methods=doOrder&owner=lqd&pid=6064&server=jetty&side=provider×tamp=1522564991904>

dubbo多注册中心
<dubbo:registry id="one" protocol="zookeeper" address="B:2181"/>
<dubbo:registry id="zk1" protocol="zookeeper" address="A:2181"/>
<dubbo:service
​           interface="com.lqd.study.IOrderServices"
​            ref="orderService"  protocol="hessian" registry="zk1"/>
使用情况：
1，语言环境不一样
2，负载

dubbo多版本控制
1，服务器
<dubbo:service
​           interface="com.lqd.study.IOrderServices"
​            ref="orderService"  protocol="hessian" registry="zk1" version="2.0"/>
<hessian://192.168.254.1:8090/com.lqd.study.IOrderServices?anyhost=true&application=order-provider&dubbo=2.5.3&interface=com.lqd.study.IOrderServices&methods=doOrder&owner=lqd&pid=9384&revision=2.0&server=jetty&side=provider×tamp=1522566926302&version=2.0>
2，客户端
需要客户端传递version

dubbo异步调用
服务端不用处理，客户端：
 <dubbo:reference id="orderServices" interface="com.lqd.study.IOrderServices" check="true" protocol="dubbo" version="1.0" async="true"/>
异步：只支持dubbo协议
代码处理：
 Future<DoOrderResponse> response = RpcContext.getContext().getFuture();
​        System.out.println(response);

dubbo主机绑定
  <dubbo:protocol name="dubbo" port="20880" host="ip"/>
地址只能绑定一个

dubbo服务只订阅
在调试或者开发过程中，服务提供者不提供服务但又依赖其他服务时，只订阅
<dubbo:registry protocol="zookeeper" address="192.168.254.128:2181,192.168.254.129:2181,192.168.254.130:2181" register="false"/>

dubbo服务只注册
只提供服务(多注册中心)
不使用某个的注册中心
 <dubbo:registry subscribe="false"></dubbo:registry>

dubbo负载均衡

场景：
dubbo 启动多个 ，因为他自带负载
策略
Random(默认)。
roundRonbin（轮询）：按照公约的权重设置轮询比率。
LeastActivvve LoadBalance ： 最少活跃调用数，对于响应比较短的服务会优先
Consistent LoadBalance：一致性hash，相同参数的请求都回落到同一个服务
 <dubbo:service
​            interface="com.lqd.study.IOrderServices"
​            ref="orderService"  protocol="dubbo"  version="2.0" loadbalance="random" />

集群容错
Failover（默认） : 失败了自动切换尝试其他服务器，通过retries=number。来设置尝试次数。
failfast 快速失败，只发起一次调用；写操作。比如新增记录的时候，非幂等请求。
failsafe 失败了也忽略异常。例如写日志
failback 失败自动恢复，定时重发 。例如：定时处理
forking 并行调用服务器，只要有一个成功就返回。 例如：读请求
broadcast 广播调用所有的提供者，其中一台失败就返回异常。
<dubbo:service
​            interface="com.lqd.study.IOrderServices"
​            ref="orderService"  protocol="dubbo"  version="2.0" 
​            loadbalance="random" timeout="2000"
​    cluster="failfast"/>
只配置在客户端

连接超时
<dubbo:service
​            interface="com.lqd.study.IOrderServices"
​            ref="orderService"  protocol="dubbo"  version="2.0" loadbalance="random" timeout="2000"/> 
单位：ms
一定要设置服务处理的超时时间

配置优先级
消费端的优先级最高。（timeout）
reference >

怎么处理dubbo服务架构

集成spring包改造
1，导包 
<!--Spring-->
​      <dependency>
​        <groupId>org.springframework</groupId>
​        <artifactId>spring-core</artifactId>
​        <version>4.3.10.RELEASE</version>
​      </dependency>
​      <dependency>
​        <groupId>org.springframework</groupId>
​        <artifactId>spring-beans</artifactId>
​        <version>4.3.10.RELEASE</version>
​      </dependency>
​      <dependency>
​        <groupId>org.springframework</groupId>
​        <artifactId>spring-context</artifactId>
​        <version>4.3.10.RELEASE</version>
​      </dependency>
​      <dependency>
​        <groupId>org.springframework</groupId>
​        <artifactId>spring-context-support</artifactId>
​        <version>4.3.10.RELEASE</version>
​      </dependency>
​      <dependency>
​        <groupId>org.springframework</groupId>
​        <artifactId>spring-orm</artifactId>
​        <version>4.3.10.RELEASE</version>
​      </dependency>
​      <dependency>
​        <groupId>com.alibaba</groupId>
​        <artifactId>dubbo</artifactId>
​        <version>2.5.3</version>
​        <exclusions>
​          <exclusion>
​            <groupId>org.springframework</groupId>
​            <artifactId>spring</artifactId>
​          </exclusion>
​        </exclusions>
​      </dependency>

将客户端的dubbo配置可以放置到服务端的api的resources/META-INF/client中

客户端只需要在spring配置文件中使用xml方式引用进来和引进api jar包即可
<import resource="classpath*:META-INF/">

配置dubbo缓存文件
使用：
<dubbo:registry protocol="zookeeper" file="d:/dubbo.cache" 
缓存内容：
注册中心的列表
服务提供者列表