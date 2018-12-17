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

    //不建议添加这个
    @Around("aspect()")
    public Object around(JoinPoint joinPoint) throws Throwable
    {
         System.out.println("around aspect() start");
         //特别处理 -- 不然advice chain 在这里结束，同时不会执行目标对象的方法
         //重新执行
         ((ProceedingJoinPoint)joinPoint).proceed();
         System.out.println("around aspect() end");
         return object ;
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

#### 获取当前方法匹配的advisor

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

### ReflectiveMethodInvocation

无论JDKDynamicAopProxy还是CglibAopProxy都会执行下面的方法：

#### 执行advisor的chain

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

### CglibAopProxy

<aop:aspectj-autoproxy proxy-target-class="true"/>，选择GglibAopProxy进行代理。

CglibAopProxy有多个静态类 ，都实现了MethodInterceptor接口，

```java
/**
 * General purpose AOP callback. Used when the target is dynamic or when the
 * proxy is not frozen.
 */
private static class DynamicAdvisedInterceptor implements MethodInterceptor, Serializable {

   private final AdvisedSupport advised;

   public DynamicAdvisedInterceptor(AdvisedSupport advised) {
      this.advised = advised;
   }

   @Override
   @Nullable
   public Object intercept(Object proxy, Method method, Object[] args, MethodProxy methodProxy) throws Throwable {
      Object oldProxy = null;
      boolean setProxyContext = false;
      Object target = null;
      TargetSource targetSource = this.advised.getTargetSource();
      try {
         if (this.advised.exposeProxy) {
            // Make invocation available if necessary.
            oldProxy = AopContext.setCurrentProxy(proxy);
            setProxyContext = true;
         }
         // Get as late as possible to minimize the time we "own" the target, in case it comes from a pool...
         target = targetSource.getTarget();
         Class<?> targetClass = (target != null ? target.getClass() : null);
         List<Object> chain = this.advised.getInterceptorsAndDynamicInterceptionAdvice(method, targetClass);
         Object retVal;
         // Check whether we only have one InvokerInterceptor: that is,
         // no real advice, but just reflective invocation of the target.
         if (chain.isEmpty() && Modifier.isPublic(method.getModifiers())) {
            // We can skip creating a MethodInvocation: just invoke the target directly.
            // Note that the final invoker must be an InvokerInterceptor, so we know
            // it does nothing but a reflective operation on the target, and no hot
            // swapping or fancy proxying.
            Object[] argsToUse = AopProxyUtils.adaptArgumentsIfNecessary(method, args);
            retVal = methodProxy.invoke(target, argsToUse);
         }
         else {
            // We need to create a method invocation...
            retVal = new CglibMethodInvocation(proxy, target, method, args, targetClass, chain, methodProxy).proceed();
         }
         retVal = processReturnType(proxy, target, method, retVal);
         return retVal;
      }
      finally {
         if (target != null && !targetSource.isStatic()) {
            targetSource.releaseTarget(target);
         }
         if (setProxyContext) {
            // Restore old proxy.
            AopContext.setCurrentProxy(oldProxy);
         }
      }
   }

   @Override
   public boolean equals(Object other) {
      return (this == other ||
            (other instanceof DynamicAdvisedInterceptor &&
                  this.advised.equals(((DynamicAdvisedInterceptor) other).advised)));
   }

   /**
    * CGLIB uses this to drive proxy creation.
    */
   @Override
   public int hashCode() {
      return this.advised.hashCode();
   }
}
```

#### DefaultAdvisorChainFactory

通过不同的通知类型的advisor获取代理对象的增强的拦截器：

```java
@Override
public List<Object> getInterceptorsAndDynamicInterceptionAdvice(
      Advised config, Method method, @Nullable Class<?> targetClass) {

   // This is somewhat tricky... We have to process introductions first,
   // but we need to preserve order in the ultimate list.
   AdvisorAdapterRegistry registry = GlobalAdvisorAdapterRegistry.getInstance();
   Advisor[] advisors = config.getAdvisors();
   List<Object> interceptorList = new ArrayList<>(advisors.length);
   Class<?> actualClass = (targetClass != null ? targetClass : method.getDeclaringClass());
   Boolean hasIntroductions = null;

   for (Advisor advisor : advisors) {
      if (advisor instanceof PointcutAdvisor) {
         // Add it conditionally.
         PointcutAdvisor pointcutAdvisor = (PointcutAdvisor) advisor;
         if (config.isPreFiltered() || pointcutAdvisor.getPointcut().getClassFilter().matches(actualClass)) {
            MethodMatcher mm = pointcutAdvisor.getPointcut().getMethodMatcher();
            boolean match;
            if (mm instanceof IntroductionAwareMethodMatcher) {
               if (hasIntroductions == null) {
                  hasIntroductions = hasMatchingIntroductions(advisors, actualClass);
               }
               match = ((IntroductionAwareMethodMatcher) mm).matches(method, actualClass, hasIntroductions);
            }
            else {
               match = mm.matches(method, actualClass);
            }
            if (match) {
               MethodInterceptor[] interceptors = registry.getInterceptors(advisor);
               if (mm.isRuntime()) {
                  // Creating a new object instance in the getInterceptors() method
                  // isn't a problem as we normally cache created chains.
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

#### DefaultAdvisorAdpaterRegistery

具体的获取拦截器的方法：

```java
@Override
public MethodInterceptor[] getInterceptors(Advisor advisor) throws UnknownAdviceTypeException {
   List<MethodInterceptor> interceptors = new ArrayList<>(3);
   Advice advice = advisor.getAdvice();
   if (advice instanceof MethodInterceptor) {
      interceptors.add((MethodInterceptor) advice);
   }
   for (AdvisorAdapter adapter : this.adapters) {
      if (adapter.supportsAdvice(advice)) {
         interceptors.add(adapter.getInterceptor(advisor));
      }
   }
   if (interceptors.isEmpty()) {
      throw new UnknownAdviceTypeException(advisor.getAdvice());
   }
   return interceptors.toArray(new MethodInterceptor[0]);
}
```

这里的adapters只有3个：

```java
s DefaultAdvisorAdapterRegistry implements AdvisorAdapterRegistry, Serializable {

   private final List<AdvisorAdapter> adapters = new ArrayList<>(3);


   /**
    * Create a new DefaultAdvisorAdapterRegistry, registering well-known adapters.
    */
   public DefaultAdvisorAdapterRegistry() {
      registerAdvisorAdapter(new MethodBeforeAdviceAdapter());
      registerAdvisorAdapter(new AfterReturningAdviceAdapter());
      registerAdvisorAdapter(new ThrowsAdviceAdapter());
   }
```

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
    //若改类没有通知，则不生成代理类
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

#### 怎么获取容器中的所有切面

在BeanFactoryAdvisorRetrievalHelper.findAdvisorBeans方法获取所有的切面。

```java
public List<Advisor> findAdvisorBeans() {
   // Determine list of advisor bean names, if not cached already.
   String[] advisorNames = this.cachedAdvisorBeanNames;
   if (advisorNames == null) {
      // Do not initialize FactoryBeans here: We need to leave all regular beans
      // uninitialized to let the auto-proxy creator apply to them!
      advisorNames = BeanFactoryUtils.beanNamesForTypeIncludingAncestors(
            this.beanFactory, Advisor.class, true, false);
      this.cachedAdvisorBeanNames = advisorNames;
   }
   if (advisorNames.length == 0) {
      return new ArrayList<>();
   }

   List<Advisor> advisors = new ArrayList<>();
   for (String name : advisorNames) {
      if (isEligibleBean(name)) {
         if (this.beanFactory.isCurrentlyInCreation(name)) {
            if (logger.isTraceEnabled()) {
               logger.trace("Skipping currently created advisor '" + name + "'");
            }
         }
         else {
            try {
               advisors.add(this.beanFactory.getBean(name, Advisor.class));
            }
            catch (BeanCreationException ex) {
               Throwable rootCause = ex.getMostSpecificCause();
               if (rootCause instanceof BeanCurrentlyInCreationException) {
                  BeanCreationException bce = (BeanCreationException) rootCause;
                  String bceBeanName = bce.getBeanName();
                  if (bceBeanName != null && this.beanFactory.isCurrentlyInCreation(bceBeanName)) {
                     if (logger.isTraceEnabled()) {
                        logger.trace("Skipping advisor '" + name +
                              "' with dependency on currently created bean: " + ex.getMessage());
                     }
                     // Ignore: indicates a reference back to the bean we're trying to advise.
                     // We want to find advisors other than the currently created bean itself.
                     continue;
                  }
               }
               throw ex;
            }
         }
      }
   }
   return advisors;
}
```

#### 怎么将切面的通知收集

AbstractAdvisorAutoProxyCreator的getAdvicesAndAdvisorsForBean()方法：

```java
@Override
	@Nullable
	protected Object[] getAdvicesAndAdvisorsForBean(
			Class<?> beanClass, String beanName, @Nullable TargetSource targetSource) {

		List<Advisor> advisors = findEligibleAdvisors(beanClass, beanName);
		if (advisors.isEmpty()) {
			return DO_NOT_PROXY;
		}
		return advisors.toArray();
	}

protected List<Advisor> findEligibleAdvisors(Class<?> beanClass, String beanName) {
    //获取所有的切面的通知
   List<Advisor> candidateAdvisors = findCandidateAdvisors();
    //匹配目标类合适的通知
   List<Advisor> eligibleAdvisors = findAdvisorsThatCanApply(candidateAdvisors, beanClass, beanName);
    //添加暴露JointPoint的advisor
   extendAdvisors(eligibleAdvisors);
   if (!eligibleAdvisors.isEmpty()) {
       //按照自然排序
      eligibleAdvisors = sortAdvisors(eligibleAdvisors);
   }
   return eligibleAdvisors;
}
```

上面的findEligibleAdvisors方法查找的通过findCandidateAdvisors方法是找到是他的子类AnnotationAwareAspectJAutoProxyCreator.findCandidateAdvisors() ，该方法被子类覆盖(Override)：

```java
@Override
protected List<Advisor> findCandidateAdvisors() {
   // Add all the Spring advisors found according to superclass rules.
   List<Advisor> advisors = super.findCandidateAdvisors();
   // Build Advisors for all AspectJ aspects in the bean factory.
   if (this.aspectJAdvisorsBuilder != null) {
      advisors.addAll(this.aspectJAdvisorsBuilder.buildAspectJAdvisors());
   }
   return advisors;
}
```

通过上面的findCandidateAdvisors方法我们知道了BeanFactoryAspectJAdvisorsBuilder类的buildAspectJAdvisors方法。--- 获取所有的切面的通知：

```java
/**
 * Look for AspectJ-annotated aspect beans in the current bean factory,
 * and return to a list of Spring AOP Advisors representing them.
 * <p>Creates a Spring Advisor for each AspectJ advice method.
 * @return the list of {@link org.springframework.aop.Advisor} beans
 * @see #isEligibleBean
 */
public List<Advisor> buildAspectJAdvisors() {
   List<String> aspectNames = this.aspectBeanNames;

   if (aspectNames == null) {
      synchronized (this) {
         aspectNames = this.aspectBeanNames;
         if (aspectNames == null) {
            List<Advisor> advisors = new ArrayList<>();
            aspectNames = new ArrayList<>();
            String[] beanNames = BeanFactoryUtils.beanNamesForTypeIncludingAncestors(
                  this.beanFactory, Object.class, true, false);
            for (String beanName : beanNames) {
               if (!isEligibleBean(beanName)) {
                  continue;
               }
               // We must be careful not to instantiate beans eagerly as in this case they
               // would be cached by the Spring container but would not have been weaved.
               Class<?> beanType = this.beanFactory.getType(beanName);
               if (beanType == null) {
                  continue;
               }
               if (this.advisorFactory.isAspect(beanType)) {
                  aspectNames.add(beanName);
                  AspectMetadata amd = new AspectMetadata(beanType, beanName);
                  if (amd.getAjType().getPerClause().getKind() == PerClauseKind.SINGLETON) {
                     MetadataAwareAspectInstanceFactory factory =
                           new BeanFactoryAspectInstanceFactory(this.beanFactory, beanName);
                     List<Advisor> classAdvisors = this.advisorFactory.getAdvisors(factory);
                     if (this.beanFactory.isSingleton(beanName)) {
                        this.advisorsCache.put(beanName, classAdvisors);
                     }
                     else {
                        this.aspectFactoryCache.put(beanName, factory);
                     }
                     advisors.addAll(classAdvisors);
                  }
                  else {
                     // Per target or per this.
                     if (this.beanFactory.isSingleton(beanName)) {
                        throw new IllegalArgumentException("Bean with name '" + beanName +
                              "' is a singleton, but aspect instantiation model is not singleton");
                     }
                     MetadataAwareAspectInstanceFactory factory =
                           new PrototypeAspectInstanceFactory(this.beanFactory, beanName);
                     this.aspectFactoryCache.put(beanName, factory);
                     advisors.addAll(this.advisorFactory.getAdvisors(factory));
                  }
               }
            }
            this.aspectBeanNames = aspectNames;
            return advisors;
         }
      }
   }

   if (aspectNames.isEmpty()) {
      return Collections.emptyList();
   }
   List<Advisor> advisors = new ArrayList<>();
   for (String aspectName : aspectNames) {
      List<Advisor> cachedAdvisors = this.advisorsCache.get(aspectName);
      if (cachedAdvisors != null) {
         advisors.addAll(cachedAdvisors);
      }
      else {
         MetadataAwareAspectInstanceFactory factory = this.aspectFactoryCache.get(aspectName);
         advisors.addAll(this.advisorFactory.getAdvisors(factory));
      }
   }
   return advisors;
}
```

将通知应用到目标对象：

```java
/**
 * Search the given candidate Advisors to find all Advisors that
 * can apply to the specified bean.
 * @param candidateAdvisors the candidate Advisors
 * @param beanClass the target's bean class
 * @param beanName the target's bean name
 * @return the List of applicable Advisors
 * @see ProxyCreationContext#getCurrentProxiedBeanName()
 */
protected List<Advisor> findAdvisorsThatCanApply(
      List<Advisor> candidateAdvisors, Class<?> beanClass, String beanName) {

   ProxyCreationContext.setCurrentProxiedBeanName(beanName);
   try {
      return AopUtils.findAdvisorsThatCanApply(candidateAdvisors, beanClass);
   }
   finally {
      ProxyCreationContext.setCurrentProxiedBeanName(null);
   }
}
```

从上面的代码可以看出：AopUtils.findAdvisorsThatCanApply 是终极应用的地方。

```java
/**
 * Determine the sublist of the {@code candidateAdvisors} list
 * that is applicable to the given class.
 * @param candidateAdvisors the Advisors to evaluate
 * @param clazz the target class
 * @return sublist of Advisors that can apply to an object of the given class
 * (may be the incoming List as-is)
 */
public static List<Advisor> findAdvisorsThatCanApply(List<Advisor> candidateAdvisors, Class<?> clazz) {
   if (candidateAdvisors.isEmpty()) {
      return candidateAdvisors;
   }
   List<Advisor> eligibleAdvisors = new ArrayList<>();
  /**
  	candidateAdvisors 所有的切面的通知
  	clazz 目标类
  **/
   for (Advisor candidate : candidateAdvisors) {
      if (candidate instanceof IntroductionAdvisor && canApply(candidate, clazz)) {
         eligibleAdvisors.add(candidate);
      }
   }
   boolean hasIntroductions = !eligibleAdvisors.isEmpty();
   for (Advisor candidate : candidateAdvisors) {
      if (candidate instanceof IntroductionAdvisor) {
         // already processed
         continue;
      }
      if (canApply(candidate, clazz, hasIntroductions)) {
         eligibleAdvisors.add(candidate);
      }
   }
   return eligibleAdvisors;
}
```

```java
/**
 * Can the given pointcut apply at all on the given class?
 * <p>This is an important test as it can be used to optimize
 * out a pointcut for a class.
 * @param pc the static or dynamic pointcut to check
 * @param targetClass the class to test
 * @param hasIntroductions whether or not the advisor chain
 * for this bean includes any introductions
 * @return whether the pointcut can apply on any method
 pc：通知
 targetClass：目标类
 */
public static boolean canApply(Pointcut pc, Class<?> targetClass, boolean hasIntroductions) {
   Assert.notNull(pc, "Pointcut must not be null");
   if (!pc.getClassFilter().matches(targetClass)) {
      return false;
   }

   MethodMatcher methodMatcher = pc.getMethodMatcher();
   if (methodMatcher == MethodMatcher.TRUE) {
      // No need to iterate the methods if we're matching any method anyway...
      return true;
   }

   IntroductionAwareMethodMatcher introductionAwareMethodMatcher = null;
   if (methodMatcher instanceof IntroductionAwareMethodMatcher) {
      introductionAwareMethodMatcher = (IntroductionAwareMethodMatcher) methodMatcher;
   }

   Set<Class<?>> classes = new LinkedHashSet<>();
   if (!Proxy.isProxyClass(targetClass)) {
      classes.add(ClassUtils.getUserClass(targetClass));
   }
   classes.addAll(ClassUtils.getAllInterfacesForClassAsSet(targetClass));

   for (Class<?> clazz : classes) {
      Method[] methods = ReflectionUtils.getAllDeclaredMethods(clazz);
      for (Method method : methods) {
         if (introductionAwareMethodMatcher != null ?
               introductionAwareMethodMatcher.matches(method, targetClass, hasIntroductions) :
               methodMatcher.matches(method, targetClass)) {
            return true;
         }
      }
   }

   return false;
}
```

添加特殊的advisor，用来在chain里面暴露JoinPoint 。

```java
/**
 * Add special advisors if necessary to work with a proxy chain that contains AspectJ advisors.
 * This will expose the current Spring AOP invocation (necessary for some AspectJ pointcut matching)
 * and make available the current AspectJ JoinPoint. The call will have no effect if there are no
 * AspectJ advisors in the advisor chain.
 * @param advisors the advisors available
 * @return {@code true} if any special {@link Advisor Advisors} were added, otherwise {@code false}
 */
public static boolean makeAdvisorChainAspectJCapableIfNecessary(List<Advisor> advisors) {
   // Don't add advisors to an empty list; may indicate that proxying is just not required
   if (!advisors.isEmpty()) {
      boolean foundAspectJAdvice = false;
      for (Advisor advisor : advisors) {
         // Be careful not to get the Advice without a guard, as
         // this might eagerly instantiate a non-singleton AspectJ aspect
         if (isAspectJAdvice(advisor)) {
            foundAspectJAdvice = true;
         }
      }
      if (foundAspectJAdvice && !advisors.contains(ExposeInvocationInterceptor.ADVISOR)) {
         advisors.add(0, ExposeInvocationInterceptor.ADVISOR);
         return true;
      }
   }
   return false;
}
```

```java
/**
 * Wrap the given bean if necessary, i.e. if it is eligible for being proxied.
 * @param bean the raw bean instance
 * @param beanName the name of the bean
 * @param cacheKey the cache key for metadata access
 * @return a proxy wrapping the bean, or the raw bean instance as-is
 */
protected Object wrapIfNecessary(Object bean, String beanName, Object cacheKey) {
  ....

   // Create proxy if we have advice.
      //得到所有的合适目标类的通知
   Object[] specificInterceptors = getAdvicesAndAdvisorsForBean(bean.getClass(), beanName, null);
   if (specificInterceptors != DO_NOT_PROXY) {
      this.advisedBeans.put(cacheKey, Boolean.TRUE);
      //创建目标类代理对象
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

![spring-aop-initializebean-advisors](E:\workspace_train\spring\spring-framework\spring-aop-initializebean-advisors.png)*advisors的大概。*

### 总结

1，spring先从容器中获取所有的切面类（实现了 Advisor.class），然后当目标类实例化的时候，将目标类的规则与切面的规则匹配比较。

2，收集匹配目标类的通知

3，添加暴露jointPoint的通知

4，通知按自然排序

5，然后用这些通知到全局注册器中注册。

6，创建代理对象。

7，当请求发生在代理对象的时候，就会去匹配出这些advisor，从而在下一步的chain中这些通知可以做目标对象功能以外的操作。

## 基于Spring JDBC开发ORM 

#### Spring JDBC应用实例

第一步：添加依赖包（数据库驱动包、连接池（druid）、springjdbc包）以及添加spring-jdbc.xml配置文件(jdbc的工具类注入)：

```xml
<bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">
    <constructor-arg ref="dataSource"></constructor-arg>
</bean>

<!-- <bean id="simpleJdbcInsert" class="org.springframework.jdbc.core.simple.SimpleJdbcInsert">
    <constructor-arg ref="dataSource" />
</bean>
<bean id="simpleJdbcCall" class="org.springframework.jdbc.core.simple.SimpleJdbcCall">
    <constructor-arg ref="dataSource" />
</bean> -->
```

第二步：编写repository

```java
package com.lqd.service;

import com.lqd.repository.User;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.context.annotation.Scope;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Service;
import javax.annotation.PostConstruct;
import java.sql.ResultSet;
import java.sql.SQLException;
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

    @Autowired
    private JdbcTemplate jdbcTemplate ;

    public void saveUser(User user) throws Exception {
        jdbcTemplate.execute("insert into t_e_user(username,address,id) values" +
                " ('"+user.getUserName()+"','"+user.getAddress()+"',nextval('seq_t_e_user'))");
    }

    public List<User> getUserList()
    {
        return jdbcTemplate.query("select * from t_e_user",
                new BeanPropertyRowMapper<>(User.class));
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

其中，BeanPropertyRowMapper介绍下：

##### BeanPropertyRowMapper

在每次调用查询的时候都会初始化一次表与bean的映射，所以可以定义一个全局的BeanPropertyRowMapper对象，提高程序处理的效率。

```java
/**
 * Initialize the mapping meta-data for the given class.
 * @param mappedClass the mapped class
 */
protected void initialize(Class<T> mappedClass) {
   this.mappedClass = mappedClass;
   this.mappedFields = new HashMap<>();
   this.mappedProperties = new HashSet<>();
   PropertyDescriptor[] pds = BeanUtils.getPropertyDescriptors(mappedClass);
   for (PropertyDescriptor pd : pds) {
      if (pd.getWriteMethod() != null) {
         this.mappedFields.put(lowerCaseName(pd.getName()), pd);
         String underscoredName = underscoreName(pd.getName());
         if (!lowerCaseName(pd.getName()).equals(underscoredName)) {
            this.mappedFields.put(underscoredName, pd);
         }
         this.mappedProperties.add(pd.getName());
      }
   }
}

/**
 * Convert a name in camelCase to an underscored name in lower case.
 * Any upper case letters are converted to lower case with a preceding underscore.
 * @param name the original name
 * @return the converted name
 * @since 4.2
 * @see #lowerCaseName
 */
protected String underscoreName(String name) {
   if (!StringUtils.hasLength(name)) {
      return "";
   }
   StringBuilder result = new StringBuilder();
   result.append(lowerCaseName(name.substring(0, 1)));
   for (int i = 1; i < name.length(); i++) {
      String s = name.substring(i, i + 1);
      String slc = lowerCaseName(s);
      if (!s.equals(slc)) {
         result.append("_").append(slc);
      }
      else {
         result.append(s);
      }
   }
   return result.toString();
}

/**
	 * Extract the values for all columns in the current row.
	 * <p>Utilizes public setters and result set meta-data.
	 * @see java.sql.ResultSetMetaData
	 */
	@Override
	public T mapRow(ResultSet rs, int rowNumber) throws SQLException {
		Assert.state(this.mappedClass != null, "Mapped class was not specified");
		T mappedObject = BeanUtils.instantiateClass(this.mappedClass);
		BeanWrapper bw = PropertyAccessorFactory.forBeanPropertyAccess(mappedObject);
		initBeanWrapper(bw);

		ResultSetMetaData rsmd = rs.getMetaData();
		int columnCount = rsmd.getColumnCount();
		Set<String> populatedProperties = (isCheckFullyPopulated() ? new HashSet<>() : null);

		for (int index = 1; index <= columnCount; index++) {
			String column = JdbcUtils.lookupColumnName(rsmd, index);
			String field = lowerCaseName(StringUtils.delete(column, " "));
			PropertyDescriptor pd = (this.mappedFields != null ? this.mappedFields.get(field) : null);
			if (pd != null) {
				try {
					Object value = getColumnValue(rs, index, pd);
					if (rowNumber == 0 && logger.isDebugEnabled()) {
						logger.debug("Mapping column '" + column + "' to property '" + pd.getName() +
								"' of type '" + ClassUtils.getQualifiedName(pd.getPropertyType()) + "'");
					}
					try {
						bw.setPropertyValue(pd.getName(), value);
					}
					catch (TypeMismatchException ex) {
						if (value == null && this.primitivesDefaultedForNullValue) {
							if (logger.isDebugEnabled()) {
								logger.debug("Intercepted TypeMismatchException for row " + rowNumber +
										" and column '" + column + "' with null value when setting property '" +
										pd.getName() + "' of type '" +
										ClassUtils.getQualifiedName(pd.getPropertyType()) +
										"' on object: " + mappedObject, ex);
							}
						}
						else {
							throw ex;
						}
					}
					if (populatedProperties != null) {
						populatedProperties.add(pd.getName());
					}
				}
				catch (NotWritablePropertyException ex) {
					throw new DataRetrievalFailureException(
							"Unable to map column '" + column + "' to property '" + pd.getName() + "'", ex);
				}
			}
			else {
				// No PropertyDescriptor found
				if (rowNumber == 0 && logger.isDebugEnabled()) {
					logger.debug("No property found for column '" + column + "' mapped to field '" + field + "'");
				}
			}
		}

		if (populatedProperties != null && !populatedProperties.equals(this.mappedProperties)) {
			throw new InvalidDataAccessApiUsageException("Given ResultSet does not contain all fields " +
					"necessary to populate object of class [" + this.mappedClass.getName() + "]: " +
					this.mappedProperties);
		}

		return mappedObject;
	}

```

这个数据库表的列与java bean的转换映射关系 很坑爹。若属性有大写字母那么在相邻的字段之间就用_分隔。

#### JdbcTemplate

由于他继承了JdbcAccessor，所以他实现了InitializingBean接口。

```java
public class JdbcTemplate extends JdbcAccessor implements JdbcOperations {
    ................

        @Override
	public <T> List<T> query(String sql, RowMapper<T> rowMapper) throws DataAccessException {
		return result(query(sql, new RowMapperResultSetExtractor<>(rowMapper)));
	}
        
        
@Override
@Nullable
public <T> T query(final String sql, final ResultSetExtractor<T> rse) throws DataAccessException {
   Assert.notNull(sql, "SQL must not be null");
   Assert.notNull(rse, "ResultSetExtractor must not be null");
   if (logger.isDebugEnabled()) {
      logger.debug("Executing SQL query [" + sql + "]");
   }

   /**
    * Callback to execute the query.
    */
   class QueryStatementCallback implements StatementCallback<T>, SqlProvider {
      @Override
      @Nullable
      public T doInStatement(Statement stmt) throws SQLException {
         ResultSet rs = null;
         try {
            rs = stmt.executeQuery(sql);
             //执行将记录转成bean对象。
            return rse.extractData(rs);
         }
         finally {
            JdbcUtils.closeResultSet(rs);
         }
      }
      @Override
      public String getSql() {
         return sql;
      }
   }

   return execute(new QueryStatementCallback());
}
```

RowMapperResultSetExtractor

```java
@Override
public List<T> extractData(ResultSet rs) throws SQLException {
   List<T> results = (this.rowsExpected > 0 ? new ArrayList<>(this.rowsExpected) : new ArrayList<>());
   int rowNum = 0;
   while (rs.next()) {
       //根据这个应用实例，这里会调用BeanPropertyRowMapper的mapRow方法
      results.add(this.rowMapper.mapRow(rs, rowNum++));
   }
   return results;
}
```

RowMapper是表记录与java bean映射的核心接口，我们可以实现这个接口来定义自己的映射关系：

```java
/*
 * Copyright 2002-2018 the original author or authors.
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

package org.springframework.jdbc.core;

import java.sql.ResultSet;
import java.sql.SQLException;

import org.springframework.lang.Nullable;

/**
 * An interface used by {@link JdbcTemplate} for mapping rows of a
 * {@link java.sql.ResultSet} on a per-row basis. Implementations of this
 * interface perform the actual work of mapping each row to a result object,
 * but don't need to worry about exception handling.
 * {@link java.sql.SQLException SQLExceptions} will be caught and handled
 * by the calling JdbcTemplate.
 *
 * <p>Typically used either for {@link JdbcTemplate}'s query methods
 * or for out parameters of stored procedures. RowMapper objects are
 * typically stateless and thus reusable; they are an ideal choice for
 * implementing row-mapping logic in a single place.
 *
 * <p>Alternatively, consider subclassing
 * {@link org.springframework.jdbc.object.MappingSqlQuery} from the
 * {@code jdbc.object} package: Instead of working with separate
 * JdbcTemplate and RowMapper objects, you can build executable query
 * objects (containing row-mapping logic) in that style.
 *
 * @author Thomas Risberg
 * @author Juergen Hoeller
 * @param <T> the result type
 * @see JdbcTemplate
 * @see RowCallbackHandler
 * @see ResultSetExtractor
 * @see org.springframework.jdbc.object.MappingSqlQuery
 */
@FunctionalInterface
public interface RowMapper<T> {

   /**
    * Implementations must implement this method to map each row of data
    * in the ResultSet. This method should not call {@code next()} on
    * the ResultSet; it is only supposed to map values of the current row.
    * @param rs the ResultSet to map (pre-initialized for the current row)
    * @param rowNum the number of the current row
    * @return the result object for the current row (may be {@code null})
    * @throws SQLException if a SQLException is encountered getting
    * column values (that is, there's no need to catch SQLException)
    */
   @Nullable
   T mapRow(ResultSet rs, int rowNum) throws SQLException;

}
```

#### spring jdbc介绍

使用 Spring 进行基本的 JDBC 访问数据库有多种选择。Spring 至少提供了三种不同的工作模式：

JdbcTemplate, 一个在Spring2.5中新提供的SimpleJdbc 类能够更好的处理数据库元数据; 还有一种称之为 RDBMS Object 的风格的面向对象封装方式, 有点类似于 JDO 的查询设计。 我们在这里简要列举你采取某一种工作方式的主要理由. 不过请注意, 即使你选择了其中的一种工作模式, 你依然可以在你的代码中混用其他任何一种模式以获取其带来的好处和优势。 所有的工作模式都必须要求 JDBC2.0 以上的数据库驱动的支持, 其中一些高级的功能可能需要 JDBC 3.0 以上的数据库驱动支持。

> JdbcTemplate - 这是经典的也是最常用的 Spring 对于 JDBC 访问的方案。这也是最低级别的封装, 其他的工作模式事实上在底层使用了 JdbcTemplate 作为其底层的实现基础。JdbcTemplate 在 JDK 1.4以上的环境上工作得很好。

> NamedParameterJdbcTemplate - 对 JdbcTemplate 做了封装，提供了更加便捷的基于命名参数的使用方式而不是传统的 JDBC 所使用的“?”作为参数的占位符。这种方式在你需要为某个 SQL 指定许多个参数时，显得更加直观而易用。该特性必须工作在 JDK 1.4 以上。

> SimpleJdbcTemplate - 这个类结合了 JdbcTemplate 和 NamedParameterJdbcTemplate 的最常用的功能，同时它也利用了一些 Java 5 的特性所带来的优势，例如泛型、varargs 和 autoboxing 等，从而提供了更加简便的 API 访问方式。需要工作在 Java 5 以上的环境中。SimpleJdbcInsert 和 SimpleJdbcCall - 这两个类可以充分利用数据库元数据的特性来简化配置。通过使用这两个类进行编程，你可以仅仅提供数据库表名或者存储过程的名称以及一个 Map 作为参数。其中 Map 的 key 需要与数据库表中的字段保持一致。这两个类通常和 SimpleJdbcTemplate 配合使用。这两个类需要工作在 JDK 5 以上，同时数据库需要提供足够的元数据信息。RDBMS 对象包括 MappingSqlQuery, SqlUpdate and StoredProcedure - 这种方式允许你在初始化你的数据访问层时创建可重用并且线程安全的对象。该对象在你定义了你的查询语句，声明查询参数并编译相应的 Query 之后被模型化。一旦模型化完成，任何执行函数就可以传入不同的参数对之进行多次调用。这种方式需要工作在 JDK 1.4 以上。

##### 异常处理

SQLExceptionTranslator 是 一 个 接 口 ， 如 果 你 需 要 在 SQLException 和org.springframework.dao.DataAccessException 之间作转换，那么必须实现该接口。 转换器类的实现可以采用一般通用的做法(比如使用 JDBC 的 SQLState code)，如果为了使转换更准确，也可以进行定制（比如使用 Oracle 的 error code）。

SQLErrorCodeSQLExceptionTranslator 是 SQLExceptionTranslator 的默认实现。 该实现使用指定数据库厂商的 error code，比采用 SQLState 更精确。转换过程基于一个 JavaBean（类型为SQLErrorCodes）中的 error code。 这个 JavaBean 由 SQLErrorCodesFactory 工厂类创建，其中的内容来自于 “sql-error-codes.xml”配置文件。该文件中的数据库厂商代码基于 DatabaseMetaData 信息中的 DatabaseProductName，从而配合当前数据库的使用。

SQLErrorCodeSQLExceptionTranslator 使用以下的匹配规则：
首先检查是否存在完成定制转换的子类实现。通常 SQLErrorCodeSQLExceptionTranslator 这个类可以作为一个具体类使用，不需要进行定制，那么这个规则将不适用。接着将 SQLException 的 error code 与错误代码集中的 error code 进行匹配。 默认情况下错误代码集将从 SQLErrorCodesFactory 取得。 错误代码集来自 classpath 下的 sql-error-codes.xml文件，它们将与数据库 metadata 信息中的 database name 进行映射。使用 fallback 翻译器。SQLStateSQLExceptionTranslator 类是缺省的 fallback 翻译器。

##### config模块

NamespaceHandler 接口，DefaultBeanDefinitionDocumentReader 使用该接口来处理在 spring xml 配置文件中自定义的命名空间。在 jdbc 模块，我们使用 JdbcNamespaceHandler 来处理 jdbc 配置的命名空间，其代码如下

```java
public class JdbcNamespaceHandler extends NamespaceHandlerSupport {
@Override
public void init() {
registerBeanDefinitionParser("embedded-database", new EmbeddedDatabaseBeanDefinitionParser());
registerBeanDefinitionParser("initialize-database", new InitializeDatabaseBeanDefinitionParser());
}
}
```

其中，EmbeddedDatabaseBeanDefinitionParser 继承了 AbstractBeanDefinitionParser，解析
<embedded-database>元素，并使用 EmbeddedDatabaseFactoryBean 创建一个 BeanDefinition。顺便介绍一下用到的软件包 org.w3c.dom。

###### rg.w3c.dom

软件包 org.w3c.dom:为文档对象模型 (DOM) 提供接口，该模型是 Java API for XML Processing的组件 API。该 Document Object Model Level 2 Core API 允许程序动态访问和更新文档的内容和结构。

> Attr：Attr 接口表示 Element 对象中的属性。
> CDATASection： CDATA 节用于转义文本块，该文本块包含的字符如果不转义则会被视为标记。
> CharacterData： CharacterData 接口使用属性集合和用于访问 DOM 中字符数据的方法扩展节点。
> Comment： 此接口继承自 CharacterData 表示注释的内容，即起始 '<!--' 和结束 '-->' 之间的所有字符。
> Document： Document 接口表示整个 HTML 或 XML 文档。
> DocumentFragment： DocumentFragment 是“轻量级”或“最小”Document 对象。
> DocumentType： 每个 Document 都有 doctype 属性，该属性的值可以为 null，也可以为
> DocumentType 对象。
> DOMConfiguration： 该 DOMConfiguration 接口表示文档的配置，并维护一个可识别的参数表。
> DOMError： DOMError 是一个描述错误的接口。
> DOMErrorHandler： DOMErrorHandler 是在报告处理 XML 数据时发生的错误或在进行某些其他处理如验证文档）时 DOM 实现可以调用的回调接口。
> DOMImplementation： DOMImplementation 接口为执行独立于文档对象模型的任何特定实例的操作提供了许多方法。
> DOMImplementationList： DOMImplementationList 接口提供对 DOM 实现的有序集合的抽象，没有定义或约束如何实现此集合。
> DOMImplementationSource：此接口允许 DOM 实现程序根据请求的功能和版本提供一个或多个实现，如下所述。
> DOMLocator： DOMLocator 是一个描述位置（如发生错误的位置）的接口。
> DOMStringList： DOMStringList 接口提供对 DOMString 值的有序集合的抽象，没有定义或约束此集合是如何实现的。
> Element： Element 接口表示 HTML 或 XML 文档中的一个元素。
> Entity： 此接口表示在 XML 文档中解析和未解析的已知实体。
> EntityReference： EntityReference 节点可以用来在树中表示实体引用。
> NamedNodeMap： 实现 NamedNodeMap 接口的对象用于表示可以通过名称访问的节点的集合。
> NameList NameList 接口提供对并行的名称和名称空间值对（可以为 null 值）的有序集合的抽象，无需定义或约束如何实现此集合。
> Node： 该 Node 接口是整个文档对象模型的主要数据类型。
> NodeList： NodeList 接口提供对节点的有序集合的抽象，没有定义或约束如何实现此集合。
> Notation： 此接口表示在 DTD 中声明的表示法。
> ProcessingInstruction： ProcessingInstruction 接口表示“处理指令”，该指令作为一种在文档的文本中保持特定于处理器的信息的方法在 XML 中使用。
> Text： 该 Text 接口继承自 CharacterData，并且表示 Element 或 Attr 的文本内容（在 XML 中称为 字符数据）。
> TypeInfo： TypeInfo 接口表示从 Element 或 Attr 节点引用的类型，用与文档相关的模式指定。
> UserDataHandler： 当使用 Node.setUserData() 将一个对象与节点上的键相关联时，当克隆、导入或重命名该对象关联的节点时应用程序可以提供调用的处理程序。

#####  core模块

\JdbcTeamplate 对象

\RowMapper

\元数据 metaData 模块(CallMetaDataProviderFactory 创建 CallMetaDataProvider 的工厂类)

\使用 SqlParameterSource 提供参数值

> 使用 Map 来指定参数值有时候工作得非常好，但是这并不是最简单的使用方式。Spring 提供了一些其他 的 SqlParameterSource 实 现 类 来 指 定 参 数 值 。 我 们 首 先 可 以 看 看BeanPropertySqlParameterSource 类，这是一个非常简便的指定参数的实现类，只要你有一个符JavaBean 规范的类就行了。它将使用其中的 getter 方法来获取参数值。SqlParameter 封 装 了 定 义 sql 参 数 的 对 象 。 CallableStateMentCallback ，PrePareStateMentCallback ， StateMentCallback ，ConnectionCallback 回 调 类 分 别 对 应JdbcTemplate 中的不同处理方法。

\simple 实现

\DataSource

> spring 通过 DataSource 获取数据库的连接。Datasource 是 jdbc 规范的一部分，它通过ConnectionFactory 获取。一个容器和框架可以在应用代码层中隐藏连接池和事务管理。当使用 spring 的 jdbc 层，你可以通过 JNDI 来获取 DataSource，也可以通过你自己配置的第三方连接池实现来获取。流行的第三方实现由 apache Jakarta Commons dbcp 和 c3p0.

> TransactionAwareDataSourceProxy 作为目标 DataSource 的一个代理， 在对目标 DataSource 包装的同时，还增加了 Spring 的事务管理能力， 在这一点上，这个类的功能非常像 J2EE 服务器所提供的事务化的 JNDI DataSource。

\Note

该类几乎很少被用到，除非现有代码在被调用的时候需要一个标准的 JDBC DataSource 接口实现作为参数。 这种情况下，这个类可以使现有代码参与 Spring 的事务管理。通常最好的做法是使用更高层的抽象 来对数据源进行管理，比如 JdbcTemplate 和 DataSourceUtils 等等。注意：DriverManagerDataSource 仅限于测试使用，因为它没有提供池的功能，这会导致在多个请求获取连接时性能很差。

##### object模块

##### JdbcTemplate是core包的核心类

它替我们完成了资源的创建以及释放工作，从而简化了我们对 JDBC 的使用。 它还可以帮助我们避免一些常见的错误，比如忘记关闭数据库连接。 JdbcTemplate 将完成 JDBC 核心处理流程，比如 SQL 语句的创建、执行，而把 SQL 语句的生成以及查询结果的提取工作留给我们的应用代码。 它可以完成 SQL查询、更新以及调用存储过程，可以对 ResultSet 进行遍历并加以提取。 它还可以捕获 JDBC 异常并将其转换成 org.springframework.dao 包中定义的，通用的，信息更丰富的异常。使 用 JdbcTemplate 进 行 编 码 只 需 要 根 据 明 确 定 义 的 一 组 契 约 来 实 现 回 调 接 口 。

PreparedStatementCreator 回调接口通过给定的 Connection 创建一个PreparedStatement，包含SQL 和任何相关的参数。 

CallableStatementCreateor 实现同样的处理，只不过它创建的是CallableStatement。 RowCallbackHandler 接口则从数据集的每一行中提取值。

我们可以在 DAO 实现类中通过传递一个 DataSource 引用来完成 JdbcTemplate 的实例化，也可以在Spring 的 IOC 容器中配置一个 JdbcTemplate 的 bean 并赋予 DAO 实现类作为一个实例。 需要注意的是 DataSource 在 Spring 的 IOC 容器中总是配制成一个 bean，第一种情况下，DataSource bean 将传递给 service，第二种情况下 DataSource bean 传递给 JdbcTemplate bean。

##### NamedParameterJdbcTemplate 

类为 JDBC 操作增加了命名参数的特性支持，而不是传统的使用（'?'）作为参数的占位符。NamedParameterJdbcTemplate 类对 JdbcTemplate 类进行了封装， 在底层，JdbcTemplate 完成了多数的工作。

#### 数据一致性理解

强一致性：当更新操作完成之后，任何多个后续进程或者线程的访问都会返回最新的更新过的值。这种是对用户最友好的，就是用户上一次写什么，下一次就保证能读到什么。根据 CAP 理论，这种实现需要牺牲可用性。

弱一致性：系统并不保证后续进程或者线程的访问都会返回最新的更新过的值。系统在数据写入成功之后，不承诺立即可以读到最新写入的值，也不会具体的承诺多久之后可以读到。

最终一致性：弱一致性的特定形式。系统保证在没有后续更新的前提下，系统最终返回上一次更新操作的值。在没有故障发生的前提下，不一致窗口的时间主要受通信延迟，系统负载和复制副本的个数影响

## Spring 事务设计及源码解析

### spring事务应用实例

第一步，添加依赖包以及修改spring的配置文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:aop="http://www.springframework.org/schema/aop"
       xmlns:c="http://www.springframework.org/schema/c" xmlns:cache="http://www.springframework.org/schema/cache"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:jdbc="http://www.springframework.org/schema/jdbc" xmlns:jee="http://www.springframework.org/schema/jee"
       xmlns:lang="http://www.springframework.org/schema/lang" xmlns:mvc="http://www.springframework.org/schema/mvc"
       xmlns:p="http://www.springframework.org/schema/p" xmlns:task="http://www.springframework.org/schema/task"
       xmlns:tx="http://www.springframework.org/schema/tx" xmlns:util="http://www.springframework.org/schema/util"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop.xsd
        http://www.springframework.org/schema/cache http://www.springframework.org/schema/cache/spring-cache.xsd
        http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd
        http://www.springframework.org/schema/jdbc http://www.springframework.org/schema/jdbc/spring-jdbc.xsd
        http://www.springframework.org/schema/jee http://www.springframework.org/schema/jee/spring-jee.xsd
        http://www.springframework.org/schema/lang http://www.springframework.org/schema/lang/spring-lang.xsd
        http://www.springframework.org/schema/mvc http://www.springframework.org/schema/mvc/spring-mvc.xsd
        http://www.springframework.org/schema/task http://www.springframework.org/schema/task/spring-task.xsd
        http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx.xsd
        http://www.springframework.org/schema/util http://www.springframework.org/schema/util/spring-util.xsd">

    <bean id="dataSourceTransactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource"></property>
    </bean>

    <tx:annotation-driven transaction-manager="dataSourceTransactionManager" proxy-target-class="true"></tx:annotation-driven>

</beans>
```

第二步，在repository的操作上添加事务@Transactional(rollBackFor=Exception.class)

```java
@Transactional(rollbackFor = Exception.class)
public void saveUser(User user) throws Exception {
    jdbcTemplate.execute("insert into t_e_user(username,address,id) values" +
            " ('"+user.getUserName()+"','"+user.getAddress()+"',nextval('seq_t_e_user'))");
}
```

### BeanFactoryTransactionAttributeSourceAdvisor

他继承了advisor。在容器在获取切面的时候是根据这个接口去判断的。

```java
/*
 * Copyright 2002-2017 the original author or authors.
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

package org.springframework.transaction.interceptor;

import org.springframework.aop.ClassFilter;
import org.springframework.aop.Pointcut;
import org.springframework.aop.support.AbstractBeanFactoryPointcutAdvisor;
import org.springframework.lang.Nullable;

/**
 * Advisor driven by a {@link TransactionAttributeSource}, used to include
 * a transaction advice bean for methods that are transactional.
 *
 * @author Juergen Hoeller
 * @since 2.5.5
 * @see #setAdviceBeanName
 * @see TransactionInterceptor
 * @see TransactionAttributeSourceAdvisor
 */
@SuppressWarnings("serial")
public class BeanFactoryTransactionAttributeSourceAdvisor extends AbstractBeanFactoryPointcutAdvisor {

   @Nullable
   private TransactionAttributeSource transactionAttributeSource;

   private final TransactionAttributeSourcePointcut pointcut = new TransactionAttributeSourcePointcut() {
      @Override
      @Nullable
      protected TransactionAttributeSource getTransactionAttributeSource() {
         return transactionAttributeSource;
      }
   };


   /**
    * Set the transaction attribute source which is used to find transaction
    * attributes. This should usually be identical to the source reference
    * set on the transaction interceptor itself.
    * @see TransactionInterceptor#setTransactionAttributeSource
    */
   public void setTransactionAttributeSource(TransactionAttributeSource transactionAttributeSource) {
      this.transactionAttributeSource = transactionAttributeSource;
   }

   /**
    * Set the {@link ClassFilter} to use for this pointcut.
    * Default is {@link ClassFilter#TRUE}.
    */
   public void setClassFilter(ClassFilter classFilter) {
      this.pointcut.setClassFilter(classFilter);
   }

   @Override
   public Pointcut getPointcut() {
      return this.pointcut;
   }

}
```

这个类在哪里初始化的？

```xml
<tx:annotation-driven transaction-manager="dataSourceTransactionManager" proxy-target-class="true" mode="proxy"></tx:annotation-driven>
```

当解析tx:annotation-driven这个xml标签的时候，在AnnotationDrivenBeanDefinitionParser解析的时候，如下：分别注册了根对象RootBeanDefinition（AnnotationTransactionAttributeSource\TransactionIntecerptor\BeanFactoryTransactionAttributeSourceAdvisor\）

```java
/**
 * Inner class to just introduce an AOP framework dependency when actually in proxy mode.
 */
private static class AopAutoProxyConfigurer {

   public static void configureAutoProxyCreator(Element element, ParserContext parserContext) {
      AopNamespaceUtils.registerAutoProxyCreatorIfNecessary(parserContext, element);

      String txAdvisorBeanName = TransactionManagementConfigUtils.TRANSACTION_ADVISOR_BEAN_NAME;
      if (!parserContext.getRegistry().containsBeanDefinition(txAdvisorBeanName)) {
         Object eleSource = parserContext.extractSource(element);

         // Create the TransactionAttributeSource definition.
         RootBeanDefinition sourceDef = new RootBeanDefinition(
               "org.springframework.transaction.annotation.AnnotationTransactionAttributeSource");
         sourceDef.setSource(eleSource);
         sourceDef.setRole(BeanDefinition.ROLE_INFRASTRUCTURE);
         String sourceName = parserContext.getReaderContext().registerWithGeneratedName(sourceDef);

         // Create the TransactionInterceptor definition.
         RootBeanDefinition interceptorDef = new RootBeanDefinition(TransactionInterceptor.class);
         interceptorDef.setSource(eleSource);
         interceptorDef.setRole(BeanDefinition.ROLE_INFRASTRUCTURE);
         registerTransactionManager(element, interceptorDef);
         interceptorDef.getPropertyValues().add("transactionAttributeSource", new RuntimeBeanReference(sourceName));
         String interceptorName = parserContext.getReaderContext().registerWithGeneratedName(interceptorDef);

         // Create the TransactionAttributeSourceAdvisor definition.
         RootBeanDefinition advisorDef = new RootBeanDefinition(BeanFactoryTransactionAttributeSourceAdvisor.class);
         advisorDef.setSource(eleSource);
         advisorDef.setRole(BeanDefinition.ROLE_INFRASTRUCTURE);
         advisorDef.getPropertyValues().add("transactionAttributeSource", new RuntimeBeanReference(sourceName));
         advisorDef.getPropertyValues().add("adviceBeanName", interceptorName);
         if (element.hasAttribute("order")) {
            advisorDef.getPropertyValues().add("order", element.getAttribute("order"));
         }
         parserContext.getRegistry().registerBeanDefinition(txAdvisorBeanName, advisorDef);

         CompositeComponentDefinition compositeDef = new CompositeComponentDefinition(element.getTagName(), eleSource);
         compositeDef.addNestedComponent(new BeanComponentDefinition(sourceDef, sourceName));
         compositeDef.addNestedComponent(new BeanComponentDefinition(interceptorDef, interceptorName));
         compositeDef.addNestedComponent(new BeanComponentDefinition(advisorDef, txAdvisorBeanName));
         parserContext.registerComponent(compositeDef);
      }
   }
}
```

这个advisor的advice是TransactionInterceptor。这是事务的核心处理器。

### TransactionInterceptor

```java
@Override
@Nullable
public Object invoke(MethodInvocation invocation) throws Throwable {
   // Work out the target class: may be {@code null}.
   // The TransactionAttributeSource should be passed the target class
   // as well as the method, which may be from an interface.
   Class<?> targetClass = (invocation.getThis() != null ? AopUtils.getTargetClass(invocation.getThis()) : null);

   // Adapt to TransactionAspectSupport's invokeWithinTransaction...
   return invokeWithinTransaction(invocation.getMethod(), targetClass, invocation::proceed);
}
```

核心处理的类：TransactionAspectSupport

```java
/**
 * Base class for transactional aspects, such as the {@link TransactionInterceptor}
 * or an AspectJ aspect.
 *
 * <p>This enables the underlying Spring transaction infrastructure to be used easily
 * to implement an aspect for any aspect system.
 *
 * <p>Subclasses are responsible for calling methods in this class in the correct order.
 *
 * <p>If no transaction name has been specified in the {@code TransactionAttribute},
 * the exposed name will be the {@code fully-qualified class name + "." + method name}
 * (by default).
 *
 * <p>Uses the <b>Strategy</b> design pattern. A {@code PlatformTransactionManager}
 * implementation will perform the actual transaction management, and a
 * {@code TransactionAttributeSource} is used for determining transaction definitions.
 *
 * <p>A transaction aspect is serializable if its {@code PlatformTransactionManager}
 * and {@code TransactionAttributeSource} are serializable.
 *
 * @author Rod Johnson
 * @author Juergen Hoeller
 * @author Stéphane Nicoll
 * @author Sam Brannen
 * @since 1.1
 * @see #setTransactionManager
 * @see #setTransactionAttributes
 * @see #setTransactionAttributeSource
 */
public abstract class TransactionAspectSupport implements BeanFactoryAware, InitializingBean {

	// NOTE: This class must not implement Serializable because it serves as base
	// class for AspectJ aspects (which are not allowed to implement Serializable)!

.......................

/**
 * General delegate for around-advice-based subclasses, delegating to several other template
 * methods on this class. Able to handle {@link CallbackPreferringPlatformTransactionManager}
 * as well as regular {@link PlatformTransactionManager} implementations.
 * @param method the Method being invoked
 * @param targetClass the target class that we're invoking the method on
 * @param invocation the callback to use for proceeding with the target invocation
 * @return the return value of the method, if any
 * @throws Throwable propagated from the target invocation
 */
@Nullable
protected Object invokeWithinTransaction(Method method, @Nullable Class<?> targetClass,
      final InvocationCallback invocation) throws Throwable {

   // If the transaction attribute is null, the method is non-transactional.
   TransactionAttributeSource tas = getTransactionAttributeSource();
   final TransactionAttribute txAttr = (tas != null ? tas.getTransactionAttribute(method, targetClass) : null);
    //获取事务管理器 ，根据xml配置来获取（例如这里的spring-tx.xml配置的DatasourceTransactionManager）
   final PlatformTransactionManager tm = determineTransactionManager(txAttr);
   final String joinpointIdentification = methodIdentification(method, targetClass, txAttr);

   if (txAttr == null || !(tm instanceof CallbackPreferringPlatformTransactionManager)) {
      // Standard transaction demarcation with getTransaction and commit/rollback calls.
       //开启新的 或者 使用上下文的事务
      TransactionInfo txInfo = createTransactionIfNecessary(tm, txAttr, joinpointIdentification);
      Object retVal = null;
      try {
         // This is an around advice: Invoke the next interceptor in the chain.
         // This will normally result in a target object being invoked.
         retVal = invocation.proceedWithInvocation();
      }
      catch (Throwable ex) {
         // target invocation exception
          //事务回滚
         completeTransactionAfterThrowing(txInfo, ex);
         throw ex;
      }
      finally {
         cleanupTransactionInfo(txInfo);
      }
       //事务提交
      commitTransactionAfterReturning(txInfo);
      return retVal;
   }

   else {
      final ThrowableHolder throwableHolder = new ThrowableHolder();

      // It's a CallbackPreferringPlatformTransactionManager: pass a TransactionCallback in.
      try {
         Object result = ((CallbackPreferringPlatformTransactionManager) tm).execute(txAttr, status -> {
            TransactionInfo txInfo = prepareTransactionInfo(tm, txAttr, joinpointIdentification, status);
            try {
               return invocation.proceedWithInvocation();
            }
            catch (Throwable ex) {
               if (txAttr.rollbackOn(ex)) {
                  // A RuntimeException: will lead to a rollback.
                  if (ex instanceof RuntimeException) {
                     throw (RuntimeException) ex;
                  }
                  else {
                     throw new ThrowableHolderException(ex);
                  }
               }
               else {
                  // A normal return value: will lead to a commit.
                  throwableHolder.throwable = ex;
                  return null;
               }
            }
            finally {
               cleanupTransactionInfo(txInfo);
            }
         });

         // Check result state: It might indicate a Throwable to rethrow.
         if (throwableHolder.throwable != null) {
            throw throwableHolder.throwable;
         }
         return result;
      }
      catch (ThrowableHolderException ex) {
         throw ex.getCause();
      }
      catch (TransactionSystemException ex2) {
         if (throwableHolder.throwable != null) {
            logger.error("Application exception overridden by commit exception", throwableHolder.throwable);
            ex2.initApplicationException(throwableHolder.throwable);
         }
         throw ex2;
      }
      catch (Throwable ex2) {
         if (throwableHolder.throwable != null) {
            logger.error("Application exception overridden by commit exception", throwableHolder.throwable);
         }
         throw ex2;
      }
   }
}
```

##### 什么时候导致异常后不会回滚

1，当抛出的异常不在@Transactional(rollbackFor = IndexOutOfBoundsException.class)定义得范围时，事务不会回滚。

```java
/**
 * Handle a throwable, completing the transaction.
 * We may commit or roll back, depending on the configuration.
 * @param txInfo information about the current transaction
 * @param ex throwable encountered
 */
protected void completeTransactionAfterThrowing(@Nullable TransactionInfo txInfo, Throwable ex) {
   ...................
      if (txInfo.transactionAttribute != null && txInfo.transactionAttribute.rollbackOn(ex)) {
         try {
            txInfo.getTransactionManager().rollback(txInfo.getTransactionStatus());
         }
         catch (TransactionSystemException ex2) {
            logger.error("Application exception overridden by rollback exception", ex);
            ex2.initApplicationException(ex);
            throw ex2;
         }
         catch (RuntimeException | Error ex2) {
            logger.error("Application exception overridden by rollback exception", ex);
            throw ex2;
         }
      }
      else {
         // We don't roll back on this exception.
         // Will still roll back if TransactionStatus.isRollbackOnly() is true.
         try {
            txInfo.getTransactionManager().commit(txInfo.getTransactionStatus());
         }
         catch (TransactionSystemException ex2) {
            logger.error("Application exception overridden by commit exception", ex);
            ex2.initApplicationException(ex);
            throw ex2;
         }
         catch (RuntimeException | Error ex2) {
            logger.error("Application exception overridden by commit exception", ex);
            throw ex2;
         }
      }
   }
}
```

```java
@Transactional(rollbackFor = IndexOutOfBoundsException.class)
public void saveUser(User user) throws IOException {

   /* try {*/
        jdbcTemplate.execute("insert into t_e_user(username,address,id) values" +
                " ('"+user.getUserName()+"','"+user.getAddress()+"',nextval('seq_t_e_user'))");
        throw new IOException();
   /* } catch (Exception e) {
        e.printStackTrace();
    }*/

}
```

2，当方法体中的代码被try catch后，会导致异常不会被TransactionInterceptor的异常捕获到，导致事务不会回滚。

```java
@Transactional(rollbackFor = Exception.class)
public void saveUser(User user) throws Exception {

   try {
        jdbcTemplate.execute("insert into t_e_user(username,address,id) values" +
                " ('"+user.getUserName()+"','"+user.getAddress()+"',nextval('seq_t_e_user'))");
        throw new IOException();
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

##### 只读事务

```java
@Transactional(rollbackFor = IndexOutOfBoundsException.class,readOnly = true)
```

只读事务顾名思义方法体中不能执行增删改。不然会报如下错误：

```
StatementCallback; uncategorized SQLException for SQL [insert into t_e_user(username,address,id) values ('adminBB','adminAddress',nextval('seq_t_e_user'))]; SQL state [25006]; error code [0]; ERROR: cannot execute INSERT in a read-only transaction; nested exception is org.postgresql.util.PSQLException: ERROR: cannot execute INSERT in a read-only transaction
```

对于只读查询，可以指定事务类型为readonly，即只读事务。由于只读事务不存在数据的修改，因此数据库将为只读事务提供一些优化手段，例如Oracle对于只读事务，不启动回滚段，不记录回滚log。它只是一个“暗示”，提示数据库驱动程序和数据库系统，这个事务并不包含更改数据的操作，那么JDBC驱动程序和数据库就有可能根据这种情况对该事务进行一些特定的优化，比方说不安排相应的数据库锁，以减轻事务对数据库的压力，毕竟事务也是要消耗数据库的资源的。

##### AbstractPlatformTransactionManager

事务的传播源自下面代码：

```java
/**
 * This implementation handles propagation behavior. Delegates to
 * {@code doGetTransaction}, {@code isExistingTransaction}
 * and {@code doBegin}.
 * @see #doGetTransaction
 * @see #isExistingTransaction
 * @see #doBegin
 */
@Override
public final TransactionStatus getTransaction(@Nullable TransactionDefinition definition) throws TransactionException {
   Object transaction = doGetTransaction();

   // Cache debug flag to avoid repeated checks.
   boolean debugEnabled = logger.isDebugEnabled();

   if (definition == null) {
      // Use defaults if no transaction definition given.
      definition = new DefaultTransactionDefinition();
   }

   if (isExistingTransaction(transaction)) {
      // Existing transaction found -> check propagation behavior to find out how to behave.
      return handleExistingTransaction(definition, transaction, debugEnabled);
   }

   // Check definition settings for new transaction.
   if (definition.getTimeout() < TransactionDefinition.TIMEOUT_DEFAULT) {
      throw new InvalidTimeoutException("Invalid transaction timeout", definition.getTimeout());
   }

   // No existing transaction found -> check propagation behavior to find out how to proceed.
   if (definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_MANDATORY) {
      throw new IllegalTransactionStateException(
            "No existing transaction found for transaction marked with propagation 'mandatory'");
   }
   else if (definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_REQUIRED ||
         definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_REQUIRES_NEW ||
         definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_NESTED) {
      SuspendedResourcesHolder suspendedResources = suspend(null);
      if (debugEnabled) {
         logger.debug("Creating new transaction with name [" + definition.getName() + "]: " + definition);
      }
      try {
         boolean newSynchronization = (getTransactionSynchronization() != SYNCHRONIZATION_NEVER);
         DefaultTransactionStatus status = newTransactionStatus(
               definition, transaction, true, newSynchronization, debugEnabled, suspendedResources);
         doBegin(transaction, definition);
         prepareSynchronization(status, definition);
         return status;
      }
      catch (RuntimeException | Error ex) {
         resume(null, suspendedResources);
         throw ex;
      }
   }
   else {
      // Create "empty" transaction: no actual transaction, but potentially synchronization.
      if (definition.getIsolationLevel() != TransactionDefinition.ISOLATION_DEFAULT && logger.isWarnEnabled()) {
         logger.warn("Custom isolation level specified but no actual transaction initiated; " +
               "isolation level will effectively be ignored: " + definition);
      }
      boolean newSynchronization = (getTransactionSynchronization() == SYNCHRONIZATION_ALWAYS);
      return prepareTransactionStatus(definition, null, true, newSynchronization, debugEnabled, null);
   }
}
```

