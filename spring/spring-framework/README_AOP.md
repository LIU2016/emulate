[TOC]

# Spring事务原理详解

## 事务基本概念

事务(Transaction)是访问并可能更新数据库中各种数据项的一个程序执行单元(unit)。特点：事务是恢复和并发控制的基本单位。

> 事务应该具有 4 个属性：原子性、一致性、隔离性、持久性。这四个属性通常称为 ACID 特性。
>
> 原子性（atomicity）。一个事务是一个不可分割的工作单位，事务中包括的诸操作要么都做，要么都不做。
>
> 一致性（consistency）。事务必须是使数据库从一个一致性状态变到另一个一致性状态。一致性与原子性是密切相关的。
>
> 隔离性（isolation）。一个事务的执行不能被其他事务干扰。即一个事务内部的操作及使用的数据对并发的其他事务是隔离的，并发执行的各个事务之间不能互相干扰。
>
> 持久性（durability）。持久性也称永久性（permanence），指一个事务一旦提交，它对数据库中数据的改变就应该是永久性的。接下来的其他操作或故障不应该对其有任何影响。

## 事务的基本原理

Spring 事务的本质其实就是数据库对事务的支持，没有数据库的事务支持，spring 是无法提供事务功
能的。对于纯 JDBC 操作数据库，想要用到事务，可以按照以下步骤进行：

> 获取连接 Connection con = DriverManager.getConnection()
>
> 开启事务 con.setAutoCommit(true/false);
>
> 执行 CRUD
>
> 提交事务/回滚事务 con.commit() / con.rollback();
>
> 关闭连接 conn.close();

使用 Spring 的事务管理功能后，我们可以不再写步骤 2 和 4 的代码，而是由 Spirng 自动完成。那么 Spring 是如何在我们书写的 CRUD 之前和之后开启事务和关闭事务的呢？解决这个问题，也就可以从整体上理解 Spring 的事务管理实现原理了。下面简单地介绍下，注解方式为例子

> 配置文件开启注解驱动，在相关的类和方法上通过注解@Transactional 标识。
>
> spring 在启动的时候会去解析生成相关的 bean，这时候会查看拥有相关注解的类和方法，并且为这些类和方法生成代理，并根据@Transaction 的相关参数进行相关配置注入，这样就在代理中为我们把相关的事务处理掉了（开启正常提交事务，异常回滚事务）。
>
> 真正的数据库层的事务提交和回滚是通过 binlog 或者 redo log 实现的。

## Spring事务的传播属性

所谓 spring 事务的传播属性，就是定义在存在多个事务同时存在的时候，spring 应该如何处理这些事务的行为。这些属性在 TransactionDefinition 中定义，具体常量的解释见下表：

| 常量名称                  | 常量解释                                                     |
| :------------------------ | :----------------------------------------------------------- |
| PROPAGATION_REQUIRED      | 支持当前事务，如果当前没有事务，就新建一个事
务。这是最常见的选择，也是 Spring 默认的事务
的传播。 |
| PROPAGATION_REQUIRED_NEW  | 新建事务，如果当前存在事务，把当前事务挂起。
新建的事务将和被挂起的事务没有任何关系，是两
个独立的事务，外层事务失败回滚之后，不能回滚
内层事务执行的结果，内层事务失败抛出异常，外
层事务捕获，也可以不处理回滚操作 |
| PROPAGATION_SUPPORTS      | 支持当前事务，如果当前没有事务，就以非事务方
式执行。         |
| PROPAGATION_MANDATORY     | 支持当前事务，如果当前没有事务，就抛出异常。                 |
| PROPAGATION_NOT_SUPPORTED | 以非事务方式执行操作，如果当前存在事务，就把
当前事务挂起。   |
| PROPAGATION_NEVRE         | 以非事务方式执行，如果当前存在事务，则抛出异
常。             |
| PROPAGATION_NESTED        | 如果一个活动的事务存在，则运行在一个嵌套的事
务中。如果没有活动事务，则按 REQUIRED 属性执
行。它使用了一个单独的事务，这个事务拥有多个
可以回滚的保存点。内部事务的回滚不会对外部事
务 造 成 影 响 。 它 只 对
DataSourceTransactionManager 事务管理器起
效。 |

## 数据库隔离级别

| 隔离级别        | 隔离级别的值 | 导致的问题                                                   |
| :-------------- | :----------- | :----------------------------------------------------------- |
| Read-Uncommited | 0            | 导致脏读                                                     |
| Read-commited   | 1            | 避免脏读，允许不可重复读和幻读                               |
| Repeatable-read | 2            | 避免脏读，不可重复读，允许幻读                               |
| Serializable    | 3            | 串行化读，事务只能一个一个执行，避免了脏读、
不可重复读、幻读。执行效率慢，使用时慎重 |

脏读：一事务对数据进行了增删改，但未提交，另一事务可以读取到未提交的数据。如果第一个事务这时候回滚了，那么第二个事务就读到了脏数据。

不可重复读：一个事务中发生了两次读操作，第一次读操作和第二次操作之间，另外一个事务对数据进行了修改，这时候两次读取的数据是不一致的。

幻读：第一个事务对一定范围的数据进行批量修改，第二个事务在这个范围增加一条数据，这时候第一个事务就会丢失对新增数据的修改。

总结：

> 隔离级别越高，越能保证数据的完整性和一致性，但是对并发性能的影响也越大。
>
> 大多数的数据库默认隔离级别为 Read Commited，比如 SqlServer、Oracle
>
> 少数数据库默认隔离级别为：Repeatable Read 比如： MySQL InnoDB

## Spring中的隔离级别

| 常量                      | 解释                                                         |
| ------------------------- | ------------------------------------------------------------ |
| ISOLATION_DEFAULT         | 这是个 PlatfromTransactionManager 默认的
隔离级别，使用数据库默认的事务隔离级别。另外
四个与 JDBC 的隔离级别相对应。 |
| ISOLATION_READ_UNCOMMITED |                                                              |
| ISOLATION_READ_COMMITED   |                                                              |
| ISOLATION_REPEATABLE_READ |                                                              |
| ISOLATION_SERIALIZABLE    |                                                              |

## 事务的嵌套

通过上面的理论知识的铺垫，我们大致知道了数据库事务和 spring 事务的一些属性和特点，接下来我们通过分析一些嵌套事务的场景，来深入理解 spring 事务传播的机制。假设外层事务 Service A 的 Method A() 调用内层 Service B 的 Method B().

PROPAGATION_REQUIRED(spring 默认) 

> 如果ServiceB.MethodB() 的 事 务 级 别 定 义 为PROPAGATION_REQUIRED ， 那 么 执 行ServiceA.MethodA() 的 时 候 spring 已 经 起 了 事 务 ， 这 时 调 用 ServiceB.MethodB() ，ServiceB.MethodB() 看到自己已经运行在 ServiceA.MethodA() 的事务内部，就不再起新的事务。假如 ServiceB.MethodB() 运行的时候发现自己没有在事务中，他就会为自己分配一个事务。这样，在 ServiceA.MethodA() 或者在 ServiceB.MethodB() 内的任何地方出现异常，事务都会被回滚。

PROPAGATION_REQUIRES_NEW

> 比如我们设计 ServiceA.MethodA() 的事务级别为 PROPAGATION_REQUIRED，ServiceB.MethodB()的事务级别为 PROPAGATION_REQUIRES_NEW。那么当执行到 ServiceB.MethodB() 的时候，ServiceA.MethodA() 所在的事务就会挂起，ServiceB.MethodB() 会起一个新的事务，等待 ServiceB.MethodB() 的事务完成以后，它才继续执行。他与 PROPAGATION_REQUIRED 的事务区别在于事务的回滚程度了。因为 ServiceB.MethodB() 是新起一个事务，那么就是存在两个不同的事务。如果 ServiceB.MethodB() 已经提交，那么ServiceA.MethodA() 失败回滚，ServiceB.MethodB() 是不会回滚的。如果 ServiceB.MethodB()失败回滚，如果他抛出的异常被 ServiceA.MethodA() 捕获，ServiceA.MethodA() 事务仍然可能提交(主要看B抛出的异常是不是A会回滚的异常)。

PROPAGATION_SUPPORTS

> 假 设 ServiceB.MethodB() 的 事 务 级 别 为 PROPAGATION_SUPPORTS ， 那 么 当 执 行 到ServiceB.MethodB()时，如果发现 ServiceA.MethodA()已经开启了一个事务，则加入当前的事务，如果发现 ServiceA.MethodA()没有开启事务，则自己也不开启事务。这种时候，内部方法的事务性完全依赖于最外层的事务。

PROPAGATION_NESTED

> 现在的情况就变得比较复杂了, ServiceB.MethodB() 的事务属性被配置为 PROPAGATION_NESTED,此时两者之间又将如何协作呢?   ServiceB#MethodB 如果 rollback, 那么内部事务 (即ServiceB#MethodB) 将回滚到它执行前的 SavePoint 而外部事务(即 ServiceA#MethodA) 可以有以下两种处理方式:
>
> 1，捕获异常，执行异常分支逻辑
>
> ```java
> void MethodA() {
> try {
> 		ServiceB.MethodB();
> 		} catch (SomeException) {
> 		// 执行其他业务, 如 ServiceC.MethodC();
> 	}
> }
> ```
>
> 这种方式也是嵌套事务最有价值的地方, 它起到了分支执行的效果, 如果 ServiceB.MethodB 失败,那么执行 ServiceC.MethodC(), 而 ServiceB.MethodB 已经回滚到它执行之前的 SavePoint, 所以不会产生脏数据(相当于此方法从未执行过), 这种特性可以用在某些特殊的业务中, 而PROPAGATION_REQUIRED 和 PROPAGATION_REQUIRES_NEW 都没有办法做到这一点。
>
> 2， 外部事务回滚/提交代码不做任何修改, 那么如果内部事务(ServiceB#MethodB) rollback, 那么首先 ServiceB.MethodB 回滚到它执行之前的 SavePoint(在任何情况下都会如此), 外部事务(即ServiceA#MethodA) 将根据具体的配置决定自己是 commit 还是 rollback

另外三种事务传播属性基本用不到，在此不做分析。

## Spring事务API架构图

![1544528764345](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1544528764345.png)

## Spring AOP设计原理及应用场景

### SpringAOP应用示例

AOP 是 OOP 的延续，是 Aspect Oriented Programming 的缩写，意思是面向切面编程。可以通过预编译方式和运行期动态代理实现在不修改源代码的情况下给程序动态统一添加功能的一种技术。

AOP 设计模式孜孜不倦追求的是调用者和被调用者之间的解耦，AOP 可以说也是这种目标的一种实现。我们现在做的一些非业务，如：日志、事务、安全等都会写在业务代码中(也即是说，这些非业务类横切于业务类)，但这些代码往往是重复，复制——粘贴式的代码会给程序的维护带来不便，AOP 就实现了把这些业务需求与系统需求分开来做。**这种解决的方式也称代理机制**。

先来了解一下 AOP 的相关概念

切面（Aspect）：官方的抽象定义为“一个关注点的模块化，这个关注点可能会横切多个对象”。“切面”在 ApplicationContext 中<aop:aspect>来配置。

连接点（Joinpoint）：程序执行过程中的某一行为，例如，MemberService .get 的调用或者MemberService .delete 抛出异常等行为。

通知（Advice） ：“切面”对于某个“连接点”所产生的动作。其中，一个“切面”可以包含多个“Advice”。切入点（Pointcut） ：匹配连接点的断言，在 AOP 中通知和一个切入点表达式关联。切面中的所有通知所关注的连接点，都由切入点表达式来决定。

目标对象（Target Object） ：被一个或者多个切面所通知的对象。例如，AServcieImpl 和BServiceImpl，当然在实际运行时，Spring AOP 采用代理实现，实际 AOP 操作的是 TargetObject的代理对象。

AOP 代理（AOP Proxy） ：在 Spring AOP 中有两种代理方式，JDK 动态代理和 CGLIB 代理。默认情况下，TargetObject 实现了接口时，则采用 JDK 动态代理，例如，AServiceImpl；反之，采用 CGLIB代理，例如，BServiceImpl。强制使用 CGLIB 代理需要将 <aop:config>的 proxy-target-class属性设为 true。

通知（Advice）类型：

> 前置通知（Before advice）：在某连接点（JoinPoint）之前执行的通知，但这个通知不能阻止连接点前的执行。ApplicationContext 中在<aop:aspect>里面使用<aop:before>元素进行声明。例如，TestAspect 中的 doBefore 方法。
>
> 后置通知（After advice）：当某连接点退出的时候执行的通知（不论是正常返回还是异常退出）。ApplicationContext 中在<aop:aspect>里面使用<aop:after>元素进行声明。例如，ServiceAspect中的 returnAfter 方法，所以 Teser 中调用 UserService.delete 抛出异常时，returnAfter 方法仍然执行。
>
> 返回后通知（After return advice）：在某连接点正常完成后执行的通知，不包括抛出异常的情况。ApplicationContext 中在<aop:aspect>里面使用<after-returning>元素进行声明。
>
> 环绕通知（Around advice）：包围一个连接点的通知，类似 Web 中 Servlet 规范中的 Filter 的doFilter 方法。可以在方法的调用前后完成自定义的行为，也可以选择不执行。ApplicationContext中在<aop:aspect>里面使用<aop:around>元素进行声明。例如，ServiceAspect 中的 around 方法。
>
> 抛出异常后通知（After throwing advice）：在方法抛出异常退出时执行的通知。ApplicationContext
> 中在<aop:aspect>里面使用<aop:after-throwing>元素进行声明。例如，ServiceAspect 中的returnThrow 方法。
> 注：可以将多个通知应用到一个目标对象上，即可以将多个切面织入到同一目标对象。

使用 Spring AOP 可以基于两种方式，一种是比较方便和强大的注解方式，另一种则是中规中矩的 xml配置方式。

先说注解，使用注解配置 Spring AOP 总体分为两步，

第一步是在 xml 文件中声明激活自动扫描组件功能，同时激活自动代理功能（来测试 AOP 的注解功能）：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xmlns:util="http://www.springframework.org/schema/util"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd
       http://www.springframework.org/schema/util
       http://www.springframework.org/schema/util/spring-util-2.0.xsd
       http://www.springframework.org/schema/context
       http://www.springframework.org/schema/context/spring-context-3.0.xsd
       http://www.springframework.org/schema/aop
       http://www.springframework.org/schema/aop/spring-aop-3.0.xsd">

    <context:annotation-config></context:annotation-config>
    <context:component-scan base-package="com.lqd"></context:component-scan>
    <aop:aspectj-autoproxy proxy-target-class="false"></aop:aspectj-autoproxy>

</beans>
```

第二步是为 Aspect 切面类添加注解：

```java
package com.lqd.aop;

import org.aopalliance.intercept.Joinpoint;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;
import org.springframework.stereotype.Component;

/**
 * @author lqd
 * @DATE 2018/12/11
 * @Description xxxxx
 */
@Component
@Aspect
public class AnnotationAspect
{
    @Pointcut("execution(* com.lqd.service..*(..))")
    public void aspect(){}

    @Before("aspect()")
    public void before(JoinPoint joinPoint){
        System.out.println("before aspect()");
    }

    @After("aspect()")
    public void after(JoinPoint joinPoint)
    {
        System.out.println("after aspect()");
    }

    @Around("aspect()")
    public void around(JoinPoint joinPoint) throws Throwable
    {
        System.out.println("around aspect() start");
        //特别处理 -- 不然advice chain 在这里结束，同时不会执行目标对象的方法
        ((ProceedingJoinPoint)joinPoint).proceed();
        System.out.println("around aspect() end");
    }

    @AfterReturning("aspect()")
    public void afterreturning(JoinPoint joinPoint)
    {
        System.out.println("afterreturning aspect()");
    }

    @AfterThrowing(pointcut="aspect()" ,throwing = "ex")
    public void afterThrow(JoinPoint joinPoint ,Exception ex)
    {
        System.out.println("afterThrow aspect()" + ex.getMessage());
    }
}

```

第三步，设置目标对象

```java
package com.lqd.service;

import com.lqd.repository.User;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.context.annotation.Lazy;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;
import javax.annotation.PostConstruct;
import java.util.ArrayList;
import java.util.List;

/**
 * @ClassName UserService
 * @Description TODO
 * @Author lqd
 * @Date 2018/12/9 9:23
 * @Version 1.0
 **/
@Service
@Scope(value="singleton")
@Lazy
public class UserService implements InitializingBean
{
    public UserService()
    {
        System.out.println("UserService cinit");
    }

    private List<User> userList = new ArrayList<>() ;

    public void saveUser(User user) throws Exception {
        System.out.println("hi save user!");
        userList.add(user);
        throw new Exception();
    }

    public List<User> getUserList()
    {
        System.out.println("hi get userList!");
        return userList ;
    }

    @PostConstruct
    public void postConstruct(){
        System.out.println("postConstruct");
    }

    @Override
    public void afterPropertiesSet() throws Exception {
        System.out.println("afterPropertiesSet");
    }
}
```

### 测试代码（spring Test使用以及junit）

```java
package com.lqd;

import com.lqd.aop.AnnotationAspect;
import com.lqd.repository.User;
import com.lqd.service.UserService;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.util.concurrent.TimeUnit;

/**
 * @author lqd
 * @DATE 2018/12/11
 * @Description xxxxx
 */
@ContextConfiguration(locations = {"classpath*:spring-aop.xml"})
@RunWith(SpringJUnit4ClassRunner.class)
public class TestAop
{
    @Autowired
    private UserService userService;

    @Autowired
    ApplicationContext applicationContext;

    @Test
    public void testAop() throws Throwable {
        AnnotationAspect annotationAspect = applicationContext.getBean(AnnotationAspect.class) ;
        System.out.println(annotationAspect);
        userService.getUserList();
        System.out.println("----------------------throw-------------");
        userService.saveUser(new User());
    }
}

```

*注意：spring5.1.2.RELEASE要和JUnit 4.12以及更高版本。*

执行结果展示

```
UserService cinit
postConstruct
afterPropertiesSet
com.lqd.aop.AnnotationAspect@165b8a71
around aspect() start
before aspect()
hi get userList!
around aspect() end
after aspect()
afterreturning aspect()
----------------------throw-------------
around aspect() start
before aspect()
hi save user!
after aspect()
afterThrow aspect()null
```

可以看到，正如我们预期的那样，虽然我们并没有对 MemberService 类包括其调用方式做任何改变，但是 Spring 仍然拦截到了其中方法的调用，或许这正是 AOP 的魔力所在。

再简单说一下 xml 配置方式，其实也一样简单：

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
xmlns:tx="http://www.springframework.org/schema/tx"
xmlns:aop="http://www.springframework.org/schema/aop"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.springframework.org/schema/beans
http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
http://www.springframework.org/schema/tx
http://www.springframework.org/schema/tx/spring-tx-3.0.xsd
http://www.springframework.org/schema/aop
http://www.springframework.org/schema/aop/spring-aop-3.0.xsd">
<aop:aspectj-autoproxy proxy-target-class="true"/>
<bean id="xmlAspect" class="com.lqd.aop.aspect.XmlAspect"></bean>
<!-- AOP 配置 -->
<aop:config>
<!-- 声明一个切面,并注入切面 Bean,相当于@Aspect -->
<aop:aspect ref="xmlAspect">
<!-- 配置一个切入点,相当于@Pointcut -->
<aop:pointcut expression="execution(* com.gupaoedu.aop.service..*(..))" id="simplePointcut"/>
<!-- 配置通知,相当于@Before、@After、@AfterReturn、@Around、@AfterThrowing -->
<aop:before pointcut-ref="simplePointcut" Method="before"/>
<aop:after pointcut-ref="simplePointcut" Method="after"/>
<aop:after-returning pointcut-ref="simplePointcut" Method="afterReturn"/>
<aop:after-throwing pointcut-ref="simplePointcut" Method="afterThrow" throwing="ex"/>
</aop:aspect>
</aop:config>
</beans>
```

下面我们简单地介绍一下切入点表达式的配置规则吧。通常情况下，表达式中使用”execution“就可以满足大部分的要求。表达式格式如下：

```java
execution(modifiers-pattern? ret-type-pattern declaring-type-pattern? name-pattern(param-pattern)
throws-pattern?
```

> modifiers-pattern：方法的操作权限
> ret-type-pattern：返回值
> declaring-type-pattern：方法所在的包
> name-pattern：方法名
> parm-pattern：参数名
> throws-pattern：异常

其中，除 ret-type-pattern 和 name-pattern 之外，其他都是可选的。上例中，execution(*com.spring.service.*.*(..))表示 com.spring.service 包下，返回值为任意类型；方法名任意；参数不作限制的所有方法。

最后说一下通知参数可以通过 args 来绑定参数，这样就可以在通知（Advice）中访问具体参数了。例如，<aop:aspect>配置如下：

```xml
<aop:config>
<aop:aspect ref="xmlAspect">
<aop:pointcut id="simplePointcut"
expression="execution(* com.lqd.aop.service..*(..)) and args(msg,..)" />
<aop:after pointcut-ref="simplePointcut" Method="after"/>
</aop:aspect>
</aop:config>
```

上面的代码 args(msg,..)是指将切入点方法上的第一个 String 类型参数添加到参数名为 msg 的通知的入参上，这样就可以直接使用该参数啦。

访问当前的连接点在上面的 Aspect 切面 Bean 中已经看到了，每个通知方法第一个参数都是 JoinPoint。其实，在 Spring中，任何通知（Advice）方法都可以将第一个参数定义为 org.aspectj.lang.JoinPoint 类型用以接受当前连接点对象。JoinPoint 接口提供了一系列有用的方法， 比如 getArgs() （返回方法参数）、getThis() （返回代理对象）、getTarget() （返回目标）、getSignature() （返回正在被通知的方法相关信息）和 toString() （打印出正在被通知的方法的有用信息）。

## SpringAOP设计原理及源码分析

![1544580081275](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1544580081275.png)

Spring 提供了两种方式来生成代理对象: JDKProxy 和 Cglib，具体使用哪种方式生成由AopProxyFactory 根据 AdvisedSupport 对象的配置来决定。默认的策略是如果目标类是接口，则使用 JDK 动态代理技术，否则使用 Cglib 来生成代理。下面我们来研究一下 Spring 如何使用 JDK 来生成代理对象，具体的生成代码放在JdkDynamicAopProxy 这个类中，直接上相关代码

### JdkDynamicAopProxy 

```java
/**
* 获取代理类要实现的接口 , 除了 Advised 对象中配置的 , 还会加上 SpringProxy, Advised(opaque=false)
* 检查上面得到的接口中有没有定义 equals 或者 hashcode 的接口
* 调用 Proxy.newProxyInstance 创建代理对象
*/
@Override
public Object getProxy(@Nullable ClassLoader classLoader) {
if (logger.isDebugEnabled()) {
logger.debug("Creating JDK dynamic proxy: target source is " + this.advised.getTargetSource());
}
Class<?>[] proxiedInterfaces = AopProxyUtils.completeProxiedInterfaces(this.advised, true);
findDefinedEqualsAndHashCodeMethods(proxiedInterfaces);
return Proxy.newProxyInstance(classLoader, proxiedInterfaces, this);}
```

那这个其实很明了，注释上我也已经写清楚了，不再赘述。下面的问题是，代理对象生成了，那切面是如何织入的？

我们知道 InvocationHandler 是 JDK 动态代理的核心，生成的代理对象的方法调用都会委托到InvocationHandler.invoke()方法。而通过 JdkDynamicAopProxy 的签名我们可以看到这个类其实也实现了 InvocationHandler，下面我们就通过分析这个类中实现的 invoke()方法来具体看下Spring AOP 是如何织入切面的。

```java
public Object invoke(Object proxy, Method Method, Object[] args) throws Throwable {
MethodInvocation invocation;
Object oldProxy = null;
boolean setProxyContext = false;
TargetSource targetSource = this.advised.targetSource;
Object target = null;
try {
//eqauls()方法，具目标对象未实现此方法
if (!this.equalsDefined && AopUtils.isEqualsMethod(Method)) {
return equals(args[0]);
}
//hashCode()方法，具目标对象未实现此方法
else if (!this.hashCodeDefined && AopUtils.isHashCodeMethod(Method)) {
return hashCode();
}
else if (Method.getDeclaringClass() == DecoratingProxy.class) {
return AopProxyUtils.ultimateTargetClass(this.advised);
}
//Advised 接口或者其父接口中定义的方法,直接反射调用,不应用通知
else if (!this.advised.opaque && Method.getDeclaringClass().isInterface() &&
Method.getDeclaringClass().isAssignableFrom(Advised.class)) {
return AopUtils.invokeJoinpointUsingReflection(this.advised, Method, args);
}
Object retVal;
if (this.advised.exposeProxy) {
    // Make invocation available if necessary.
oldProxy = AopContext.setCurrentProxy(proxy);
setProxyContext = true;
}
//获得目标对象的类
target = targetSource.getTarget();
Class<?> targetClass = (target != null ? target.getClass() : null);
//获取可以应用到此方法上的 Interceptor 列表
List<Object> chain = this.advised.getInterceptorsAndDynamicInterceptionAdvice(Method, targetClass);
//如果没有可以应用到此方法的通知(Interceptor)，此直接反射调用 Method.invoke(target, args)
if (chain.isEmpty()) {
Object[] argsToUse = AopProxyUtils.adaptArgumentsIfNecessary(Method, args);
retVal = AopUtils.invokeJoinpointUsingReflection(target, Method, argsToUse);
}
else {
//创建 MethodInvocation
invocation = new ReflectiveMethodInvocation(proxy, target, Method, args, targetClass, chain);
retVal = invocation.proceed();
}
Class<?> returnType = Method.getReturnType();
if (retVal != null && retVal == target &&
returnType != Object.class && returnType.isInstance(proxy) &&
!RawTargetAccess.class.isAssignableFrom(Method.getDeclaringClass())) {
retVal = proxy;
}
else if (retVal == null && returnType != Void.TYPE && returnType.isPrimitive()) {
throw new AopInvocationException(
"Null return value from advice does not match primitive return type for: " + Method);
}
return retVal;
}
finally {
if (target != null && !targetSource.isStatic()) {
targetSource.releaseTarget(target);
}
if (setProxyContext) {
AopContext.setCurrentProxy(oldProxy);
}
}
}
```

主流程可以简述为：获取可以应用到此方法上的通知链（Interceptor Chain）,如果有,则应用通知,并执行 joinpoint; 如果没有,则直接反射执行 joinpoint。而这里的关键是通知链是如何获取的以及它又是如何执行的，下面逐一分析下。

首 先 ， 从上面的代码可 以 看 到 ， 通 知 链 是 通 过Advised.getInterceptorsAndDynamicInterceptionAdvice()这个方法来获取的,我们来看下这个方法的实现:

```java
public List<Object> getInterceptorsAndDynamicInterceptionAdvice(Method Method, @Nullable Class<?> targetClass)
{
MethodCacheKey cacheKey = new MethodCacheKey(Method);
List<Object> cached = this.MethodCache.get(cacheKey);
if (cached == null) {
cached = this.advisorChainFactory.getInterceptorsAndDynamicInterceptionAdvice(
this, Method, targetClass);
this.MethodCache.put(cacheKey, cached);
}
return cached;
}
```

可以看到实际的获取工作其实是由AdvisorChainFactory.getInterceptorsAndDynamicInterceptionAdvice()这个方法来完成的，获取到的结果会被缓存。下面来分析下这个方法的实现：

```java
/**
* 从提供的配置实例 config 中获取 advisor 列表 , 遍历处理这些 advisor. 如果是 IntroductionAdvisor,
* 则判断此 Advisor 能否应用到目标类 targetClass 上 . 如果是 PointcutAdvisor, 则判断
* 此 Advisor 能否应用到目标方法 Method 上 . 将满足条件的 Advisor 通过 AdvisorAdaptor 转化成 Interceptor 列表返回 .
*/
@Override
public List<Object> getInterceptorsAndDynamicInterceptionAdvice(
Advised config, Method Method, @Nullable Class<?> targetClass) {
List<Object> interceptorList = new ArrayList<>(config.getAdvisors().length);
Class<?> actualClass = (targetClass != null ? targetClass : Method.getDeclaringClass());
//查看是否包含 IntroductionAdvisor
boolean hasIntroductions = hasMatchingIntroductions(config, actualClass);
//这里实际上注册一系列 AdvisorAdapter,用于将 Advisor 转化成 MethodInterceptor
AdvisorAdapterRegistry registry = GlobalAdvisorAdapterRegistry.getInstance();
for (Advisor advisor : config.getAdvisors()) {
if (advisor instanceof PointcutAdvisor) {
PointcutAdvisor pointcutAdvisor = (PointcutAdvisor) advisor;
if (config.isPreFiltered() || pointcutAdvisor.getPointcut().getClassFilter().matches(actualClass)) {
//这个地方这两个方法的位置可以互换下
//将 Advisor 转化成 Interceptor
MethodInterceptor[] interceptors = registry.getInterceptors(advisor);
//检查当前 advisor 的 pointcut 是否可以匹配当前方法
MethodMatcher mm = pointcutAdvisor.getPointcut().getMethodMatcher();
if (MethodMatchers.matches(mm, Method, actualClass, hasIntroductions)) {
if (mm.isRuntime()) {
for (MethodInterceptor interceptor : interceptors) {
interceptorList.add(new InterceptorAndDynamicMethodMatcher(interceptor, mm));
}
}
else {
interceptorList.addAll(Arrays.asList(interceptors));
}
}
}
}
else if (advisor instanceof IntroductionAdvisor) {
IntroductionAdvisor ia = (IntroductionAdvisor) advisor;
if (config.isPreFiltered() || ia.getClassFilter().matches(actualClass)) {
Interceptor[] interceptors = registry.getInterceptors(advisor);
interceptorList.addAll(Arrays.asList(interceptors));
}
}
else {
Interceptor[] interceptors = registry.getInterceptors(advisor);
interceptorList.addAll(Arrays.asList(interceptors));
}
}
return interceptorList;
}
```

这个方法执行完成后，Advised中配置能够应用到连接点或者目标类的Advisor全部被转化成了MethodInterceptor.接下来我们再看下得到的拦截器链是怎么起作用的。

```java
if (chain.isEmpty()) {
Object[] argsToUse = AopProxyUtils.adaptArgumentsIfNecessary(Method, args);
retVal = AopUtils.invokeJoinpointUsingReflection(target, Method, argsToUse);
}
else {
//创建 MethodInvocation
invocation = new ReflectiveMethodInvocation(proxy, target, Method, args, targetClass, chain);
retVal = invocation.proceed();
}
```

从这段代码可以看出，如果得到的拦截器链为空，则直接反射调用目标方法，否则创建MethodInvocation，调用其 proceed 方法，触发拦截器链的执行，来看下具体代码：其实就是将增强的类放到List，然后循环处理即可。这个list中存放的就是一系列的增强类（前置、后置等等，例如AspectJAfterAdvice、AspectJAfterThrowingAdvice）。

### MethodInvocation

无论JDKDynamicAopProxy还是CglibAopProxy都会执行下面的方法：

```java
public Object proceed() throws Throwable {
//如果 Interceptor 执行完了，则执行 joinPoint
if (this.currentInterceptorIndex == this.interceptorsAndDynamicMethodMatchers.size() - 1) {
return invokeJoinpoint();
}
Object interceptorOrInterceptionAdvice =
this.interceptorsAndDynamicMethodMatchers.get(++this.currentInterceptorIndex);
//如果要动态匹配 joinPoint
InterceptorAndDynamicMethodMatcher dm =
(InterceptorAndDynamicMethodMatcher) interceptorOrInterceptionAdvice;
//动态匹配：运行时参数是否满足匹配条件
if (dm.MethodMatcher.matches(this.Method, this.targetClass, this.arguments)) {
return dm.interceptor.invoke(this);
}
else {
//动态匹配失败时,略过当前 Intercetpor,调用下一个 Interceptor
return proceed();
}
}
else {
//执行当前 Intercetpor
return ((MethodInterceptor) interceptorOrInterceptionAdvice).invoke(this);
}
}
```

从下面的方法可以看出为什么Joinpoint能够携带参数返回给切面。

```java
/**
 * Invoke the joinpoint using reflection.
 * Subclasses can override this to use custom invocation.
 * @return the return value of the joinpoint
 * @throws Throwable if invoking the joinpoint resulted in an exception
 */
@Nullable
protected Object invokeJoinpoint() throws Throwable {
   return AopUtils.invokeJoinpointUsingReflection(this.target, this.method, this.arguments);
}
```

```java
/**
 * Invoke the given target via reflection, as part of an AOP method invocation.
 * @param target the target object
 * @param method the method to invoke
 * @param args the arguments for the method
 * @return the invocation result, if any
 * @throws Throwable if thrown by the target method
 * @throws org.springframework.aop.AopInvocationException in case of a reflection error
 */
@Nullable
public static Object invokeJoinpointUsingReflection(@Nullable Object target, Method method, Object[] args)
      throws Throwable {

   // Use reflection to invoke the method.
   try {
      ReflectionUtils.makeAccessible(method);
      return method.invoke(target, args);
   }
   catch (InvocationTargetException ex) {
      // Invoked method threw a checked exception.
      // We must rethrow it. The client won't see the interceptor.
      throw ex.getTargetException();
   }
   catch (IllegalArgumentException ex) {
      throw new AopInvocationException("AOP configuration seems to be invalid: tried calling method [" +
            method + "] on target [" + target + "]", ex);
   }
   catch (IllegalAccessException ex) {
      throw new AopInvocationException("Could not access method [" + method + "]", ex);
   }
}
```

### GglibAopProxy

<aop:aspectj-autoproxy proxy-target-class="true"/>，选择GglibAopProxy进行代理。

### 注解的aop怎么生成目标对象的代理类

![{ACBB0E35-D267-4E77-9E87-754D2693773F}](C:\Users\lqd\Desktop\{ACBB0E35-D267-4E77-9E87-754D2693773F}.bmp)

可以看出，aop的代理对象是通过AnnotationAwareAspectJAutoProxyCreator来生成的。

目标对象实例化的时候，进入AbstractAutowireCapableBeanFactory的initializeBean方法后，在进入applyBeanPostProcessorsAfterInitialization方法。

```java
/**
 * Initialize the given bean instance, applying factory callbacks
 * as well as init methods and bean post processors.
 * <p>Called from {@link #createBean} for traditionally defined beans,
 * and from {@link #initializeBean} for existing bean instances.
 * @param beanName the bean name in the factory (for debugging purposes)
 * @param bean the new bean instance we may need to initialize
 * @param mbd the bean definition that the bean was created with
 * (can also be {@code null}, if given an existing bean instance)
 * @return the initialized bean instance (potentially wrapped)
 * @see BeanNameAware
 * @see BeanClassLoaderAware
 * @see BeanFactoryAware
 * @see #applyBeanPostProcessorsBeforeInitialization
 * @see #invokeInitMethods
 * @see #applyBeanPostProcessorsAfterInitialization
 */
protected Object initializeBean(final String beanName, final Object bean, @Nullable RootBeanDefinition mbd) {
   ......
   if (mbd == null || !mbd.isSynthetic()) {
      wrappedBean = applyBeanPostProcessorsAfterInitialization(wrappedBean, beanName);
   }

   return wrappedBean;
}
```

```java
@Override
public Object applyBeanPostProcessorsAfterInitialization(Object existingBean, String beanName)
      throws BeansException {

   Object result = existingBean;
   for (BeanPostProcessor processor : getBeanPostProcessors()) {
      Object current = processor.postProcessAfterInitialization(result, beanName);
      if (current == null) {
         return result;
      }
      result = current;
   }
   return result;
}
```

因为开启了Aop，所以有AnnotationAwareAspectJAutoProxyCreator对象。在他执行postProcessAfterInitialization方法的时候根据切面的规则生成目标对象的代理对象。

```xml
<context:annotation-config></context:annotation-config>
<context:component-scan base-package="com.lqd"></context:component-scan>
<aop:aspectj-autoproxy proxy-target-class="false"></aop:aspectj-autoproxy>
```

```xml
<xsd:element name="aspectj-autoproxy">
   <xsd:annotation>
      <xsd:documentation source="java:org.springframework.aop.aspectj.annotation.AnnotationAwareAspectJAutoProxyCreator"><![CDATA[
Enables the use of the @AspectJ style of Spring AOP.
```

找到它的父类AbstractAutoProxyCreator的wrapIfNecessary方法，具体执行代理操作。

```java
protected Object wrapIfNecessary(Object bean, String beanName, Object cacheKey) {
   if (StringUtils.hasLength(beanName) && this.targetSourcedBeans.contains(beanName)) {
      return bean;
   }
   if (Boolean.FALSE.equals(this.advisedBeans.get(cacheKey))) {
      return bean;
   }
   if (isInfrastructureClass(bean.getClass()) || shouldSkip(bean.getClass(), beanName)) {
      this.advisedBeans.put(cacheKey, Boolean.FALSE);
      return bean;
   }

   // Create proxy if we have advice.
   Object[] specificInterceptors = getAdvicesAndAdvisorsForBean(bean.getClass(), beanName, null);
   if (specificInterceptors != DO_NOT_PROXY) {
      this.advisedBeans.put(cacheKey, Boolean.TRUE);
      Object proxy = createProxy(
            bean.getClass(), beanName, specificInterceptors, new SingletonTargetSource(bean));
      this.proxyTypes.put(cacheKey, proxy.getClass());
      return proxy;
   }

   this.advisedBeans.put(cacheKey, Boolean.FALSE);
   return bean;
}

/**
	 * Create an AOP proxy for the given bean.
	 * @param beanClass the class of the bean
	 * @param beanName the name of the bean
	 * @param specificInterceptors the set of interceptors that is
	 * specific to this bean (may be empty, but not null)
	 * @param targetSource the TargetSource for the proxy,
	 * already pre-configured to access the bean
	 * @return the AOP proxy for the bean
	 * @see #buildAdvisors
	 */
	protected Object createProxy(Class<?> beanClass, @Nullable String beanName,
			@Nullable Object[] specificInterceptors, TargetSource targetSource) {

		if (this.beanFactory instanceof ConfigurableListableBeanFactory) {
			AutoProxyUtils.exposeTargetClass((ConfigurableListableBeanFactory) this.beanFactory, beanName, beanClass);
		}

		ProxyFactory proxyFactory = new ProxyFactory();
		proxyFactory.copyFrom(this);

		if (!proxyFactory.isProxyTargetClass()) {
			if (shouldProxyTargetClass(beanClass, beanName)) {
				proxyFactory.setProxyTargetClass(true);
			}
			else {
				evaluateProxyInterfaces(beanClass, proxyFactory);
			}
		}

		Advisor[] advisors = buildAdvisors(beanName, specificInterceptors);
		proxyFactory.addAdvisors(advisors);
		proxyFactory.setTargetSource(targetSource);
		customizeProxyFactory(proxyFactory);

		proxyFactory.setFrozen(this.freezeProxy);
		if (advisorsPreFiltered()) {
			proxyFactory.setPreFiltered(true);
		}

		return proxyFactory.getProxy(getProxyClassLoader());
	}
```