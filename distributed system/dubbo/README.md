# 一、快速启动

## 官网地址

<http://dubbo.io/books/dubbo-user-book/preface/architecture.html>

## 项目代码（基于spring框架的dubbo应用）

### 1，导入maven依赖

```xml
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.lqd.demo</groupId>
            <artifactId>api</artifactId>
        </dependency>
        <dependency>
            <groupId>org.apache.zookeeper</groupId>
            <artifactId>zookeeper</artifactId>
        </dependency>
        <dependency>
            <groupId>com.101tec</groupId>
            <artifactId>zkclient</artifactId>
        </dependency>
        <dependency>
            <groupId>com.caucho</groupId>
            <artifactId>hessian</artifactId>
        </dependency>
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>servlet-api</artifactId>
        </dependency>
        <dependency>
            <groupId>org.mortbay.jetty</groupId>
            <artifactId>jetty</artifactId>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <scope>test</scope>
        </dependency>
        <!--Spring-->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-beans</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context-support</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-orm</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>dubbo</artifactId>
            <exclusions>
                <exclusion>
                    <groupId>org.springframework</groupId>
                    <artifactId>spring</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
```

### 2，API端：创建api、实体、consumer.xml（消费者dubbo配置文件）

```java
package com.lqd.demo.entity;

import java.io.Serializable;

/**
 * @author lqd
 * @DATE 2018/11/23
 * @Description 用户
 */
public class Person implements Serializable
{
    private String name;
    private int id;
    private int status;

    public Person(String name, int id, int status) {
        this.name = name;
        this.id = id;
        this.status = status;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getStatus() {
        return status;
    }

    public void setStatus(int status) {
        this.status = status;
    }
}

```

```java
package com.lqd.demo.api;

import com.lqd.demo.entity.Person;
import java.util.List;

/**
 * @author lqd
 * @DATE 2018/11/23
 * @Description 用户中心api
 */
public interface IPerson
{
    /**
     * 获取用户列表
     * @return
     */
    List<Person> getPerson();

    /**
     * 保存用户
     * @return
     */
    boolean savePerson(Person person);
}

```

```XML
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dubbo="http://code.alibabatech.com/schema/dubbo"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans-4.3.xsd
       http://code.alibabatech.com/schema/dubbo
       http://code.alibabatech.com/schema/dubbo/dubbo.xsd">

    <!-- 消费方应用名，用于计算依赖关系，不是匹配条件，不要与提供方一样 -->
    <dubbo:application name="consumer-of-helloworld-app"  owner="lqd"/>

    <dubbo:registry id="zk" protocol="zookeeper" address="192.168.102.112:2189,
    192.168.102.241:2189,192.168.102.114:2189,192.168.130.32:2189" />

    <!-- 生成远程服务代理，可以和本地bean一样使用demoService -->
    <dubbo:reference id="demoService" interface="com.lqd.demo.api.IPerson" />

</beans>
```

### 3，服务提供者

```JAVA
package com.lqd.demo.controller;

import com.lqd.demo.impl.PersonService;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import java.io.IOException;

/**
 * @author lqd
 * @DATE 2018/11/23
 * @Description xxxxx
 */
public class PersonProvider
{
    public static void main(String[] args) throws IOException {

        ClassPathXmlApplicationContext classPathXmlApplicationContext
                = new ClassPathXmlApplicationContext
                (new String[]{"classpath:provider.xml"});
        classPathXmlApplicationContext.start();
        System.in.read();
    }
}

```

```JAVA
package com.lqd.demo.impl;

import com.lqd.demo.api.IPerson;
import com.lqd.demo.entity.Person;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * @author lqd
 * @DATE 2018/11/23
 * @Description xxxxx
 */
public class PersonService implements IPerson
{
    private ArrayList<Person> personArrayList = new ArrayList<>();

    @Override
    public List<Person> getPerson() {
        return personArrayList;
    }

    @Override
    public boolean savePerson(Person person)
    {
        personArrayList.add(person);
        return false;
    }
}

```

```XML
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dubbo="http://code.alibabatech.com/schema/dubbo"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans-4.3.xsd
       http://code.alibabatech.com/schema/dubbo
       http://code.alibabatech.com/schema/dubbo/dubbo.xsd">

    <!-- 提供方应用信息，用于计算依赖关系 -->
    <dubbo:application name="hello-world-app"  owner="lqd" />

    <!-- 使用zookeeper注册中心暴露服务地址 -->
    <dubbo:registry id="demoZk" protocol="zookeeper" address="192.168.102.112:2189,
    192.168.102.241:2189,192.168.102.114:2189,192.168.130.32:2189" />

    <!-- 用dubbo协议在20880端口暴露服务 -->
    <dubbo:protocol name="dubbo" port="20880" />

    <dubbo:protocol name="hessian" port="8888" />

    <!-- 声明需要暴露的服务接口 -->
    <dubbo:service interface="com.lqd.demo.api.IPerson" ref="demoService" />

    <!-- 和本地bean一样实现服务 -->
    <bean id="demoService" class="com.lqd.demo.impl.PersonService" />

</beans>
```

4，服务消费者

```java
package com.lqd.demo.Controller;

import com.lqd.demo.api.IPerson;
import com.lqd.demo.entity.Person;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import java.io.IOException;
import java.util.List;

/**
 * @author lqd
 * @DATE 2018/11/23
 * @Description xxxxx
 */
public class PersonConsumer
{
    public static void main(String[] args) throws IOException {

        ClassPathXmlApplicationContext classPathXmlApplicationContext
                = new ClassPathXmlApplicationContext(new String[]{"classpath*:consumer.xml"});
        classPathXmlApplicationContext.start();
        IPerson iPerson = (IPerson) classPathXmlApplicationContext.getBean("demoService");
        iPerson.savePerson(new Person("demo working!",1,1)) ;
        List<Person> personList = iPerson.getPerson();
        System.out.printf("获取用户列表：\n");
        personList.stream().forEach(v->{
             System.out.printf("用户姓名：%s" ,v.getName());
             System.out.printf("用户ID：%s" ,v.getId());
             System.out.printf("用户状态：%s" ,v.getStatus());
             System.out.println("\n");
        });
    }
}
```

# 二、dubbo能解决什么问题

> 1.怎么去维护url-->通过注册中心去维护url（zookeeper、redis、memcache…）
> 2.F5硬件负载均衡器的单点压力比较大-->软负载均衡
> 3.怎么去整理出服务之间的依赖关系-->自动去整理各个服务之间的依赖
> 4.如果服务器的调用量越来越大，服务器的容量问题怎么去评估，扩容的指标-->需要一个监控平台，可以监控调用量、响应时间

# 三、dubbo是什么

> dubbo是一个分布式的服务框架，提供高性能的以及透明化的RPC远程服务调用解决方法，以及SOA服务治理方案。

# 四、Dubbo的核心部分

> 远程通信
> 集群容错
> 服务的自动发现
> 负载均衡

# 五、dubbo的架构

Provider ： tomcat
Consumer ：tomcat
Registry ：zk（dubbo在zk节点上存放服务路径地址）、redis
Monitor ：
Container ：docker

# 六、admin控制台的安装

1.下载dubbo的源码
2.找到dubbo-admin
3.修改webapp/WEB-INF/dubbo.properties
dubbo.registry.address=zookeeper的集群地址
控制中心是用来做服务治理的，比如控制服务的权重、服务的路由、。。。

> simple监控中心，Monitor也是一个dubbo服务，所以也会有端口和url
> 1，下载dubbo-monitor-simple
> 2，修改/conf目录下dubbo.properties ：
> dubbo.registry.address=<zookeeper://192.168.11.129:2181?backup=192.168.11.137:2181,192.168.11.138:2181,192.168.11.139:2181>
> 3，项目的服务提供方的/order-provider.xml中
> 添加：<dubbo:monitor ;protocol="registry">
> 4，/bin/[start.sh](http://start.sh)
> 监控服务的调用次数、调用关系、响应事件

# 七、dubbo多协议

> 大并发使用长链接：dubbo，默认采用netty （TCP）
> 大数据使用短链接：hessian
> 可以同时提供多个协议，多个接口服务

# 八、dubbo多注册中心

> <dubbo:registry id="one" protocol="zookeeper" address="B:2181"/>
> <dubbo:registry id="zk1" protocol="zookeeper" address="A:2181"/>
> <dubbo:service  interface="com.lqd.study.IOrderServices"  ref="orderService"  protocol="hessian" registry="zk1"/>
> 使用情况：
> 1，语言环境不一样
> 2，负载

# 九、dubbo多版本控制

1，服务器
<dubbo:service
​           interface="com.lqd.study.IOrderServices"
​            ref="orderService"  protocol="hessian" registry="zk1" version="2.0"/>
<hessian://192.168.254.1:8090/com.lqd.study.IOrderServices?anyhost=true&application=order-provider&dubbo=2.5.3&interface=com.lqd.study.IOrderServices&methods=doOrder&owner=lqd&pid=9384&revision=2.0&server=jetty&side=provider×tamp=1522566926302&version=2.0>
2，客户端
需要客户端传递version

# 十、dubbo异步调用

服务端不用处理，客户端：
 <dubbo:reference id="orderServices" interface="com.lqd.study.IOrderServices" check="true" protocol="dubbo" version="1.0" async="true"/>
异步：只支持dubbo协议
代码处理：
 Future<DoOrderResponse> response = RpcContext.getContext().getFuture();
​        System.out.println(response);

# 十一、dubbo主机绑定

  <dubbo:protocol name="dubbo" port="20880" host="ip"/>
地址只能绑定一个

# 十二、dubbo服务只订阅

在调试或者开发过程中，服务提供者不提供服务但又依赖其他服务时，只订阅
<dubbo:registry protocol="zookeeper" address="192.168.254.128:2181,192.168.254.129:2181,192.168.254.130:2181" register="false"/>

# 十三、dubbo服务只注册

只提供服务(多注册中心)
不使用某个的注册中心
 <dubbo:registry subscribe="false"></dubbo:registry>

# 十四、dubbo负载均衡

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

# 十五、集群容错

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

# 十六、连接超时

<dubbo:service
​            interface="com.lqd.study.IOrderServices"
​            ref="orderService"  protocol="dubbo"  version="2.0" loadbalance="random" timeout="2000"/> 
单位：ms
一定要设置服务处理的超时时间

# 十七、配置优先级

消费端的优先级最高。（timeout）

reference >

# 十八、配置dubbo缓存文件

使用：<dubbo:registry protocol="zookeeper" file="d:/dubbo.cache" 
缓存内容：
注册中心的列表
服务提供者列表