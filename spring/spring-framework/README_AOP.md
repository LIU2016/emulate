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
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:context="http://www.springframework.org/schema/context"
xmlns:util="http://www.springframework.org/schema/util"
xsi:schemaLocation="http://www.springframework.org/schema/beans
http://www.springframework.org/schema/beans/spring-beans.xsd
http://www.springframework.org/schema/util
http://www.springframework.org/schema/util/spring-util-2.0.xsd
http://www.springframework.org/schema/context
http://www.springframework.org/schema/context/spring-context-3.0.xsd">
<context:component-scan base-package="com.gupaoedu"/>
<context:annotation-config />
</beans>
```

第二步是为 Aspect 切面类添加注解：

```java
//声明这是一个组件
@Component
//声明这是一个切面 Bean
@Aspect
public class AnnotaionAspect {
private final static Logger log = Logger.getLogger(String.valueOf(AnnotaionAspect.class));
//配置切入点,该方法无方法体,主要为方便同类中其他方法使用此处配置的切入点
@Pointcut("execution(* com.gupaoedu.aop.service..*(..))")
public void aspect(){ }
/*
* 配置前置通知,使用在方法 aspect()上注册的切入点
* 同时接受 JoinPoint 切入点对象,可以没有该参数
*/
@Before("aspect()")
public void before(JoinPoint joinPoint){
log.info("before " + joinPoint);
}
//配置后置通知,使用在方法 aspect()上注册的切入点
@After("aspect()")
public void after(JoinPoint joinPoint){
log.info("after " + joinPoint);
}
//配置环绕通知,使用在方法 aspect()上注册的切入点
@Around("aspect()")
public void around(JoinPoint joinPoint){
long start = System.currentTimeMillis();
try {
((ProceedingJoinPoint) joinPoint).proceed();
long end = System.currentTimeMillis();
log.info("around " + joinPoint + "\tUse time : " + (end - start) + " ms!");
} catch (Throwable e) {
long end = System.currentTimeMillis();
log.info("around " + joinPoint + "\tUse time : " + (end - start) + " ms with exception : " + e.getMessage());
}
}
//配置后置返回通知,使用在方法 aspect()上注册的切入点
@AfterReturning("aspect()")
public void afterReturn(JoinPoint joinPoint){
log.info("afterReturn " + joinPoint);
}
//配置抛出异常后通知,使用在方法 aspect()上注册的切入点
@AfterThrowing(pointcut="aspect()", throwing="ex")
public void afterThrow(JoinPoint joinPoint, Exception ex){
log.info("afterThrow " + joinPoint + "\t" + ex.getMessage());
}
}
```

### 测试代码（spring Test使用以及junit）

```java
@ContextConfiguration(locations = {"classpath*:application-context.xml"})
@RunWith(SpringJUnit4ClassRunner.class)
public class AnnotationTester {
@Autowired
MemberService annotationService;
@Autowired
ApplicationContext app;
@Test
// @Ignore
public void test(){
System.out.println("=====这是一条华丽的分割线======");
AnnotaionAspect aspect = app.getBean(AnnotaionAspect.class);
System.out.println(aspect);
annotationService.save(new Member());
System.out.println("=====这是一条华丽的分割线======");
try {
annotationService.delete(1L);
} catch (Exception e) {
//e.printStackTrace();
}
}
}
```

*注意：spring5.1.2.RELEASE要和JUnit 4.12以及更高版本。*

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
<bean id="xmlAspect" class="com.gupaoedu.aop.aspect.XmlAspect"></bean>
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
expression="execution(* com.gupaoedu.aop.service..*(..)) and args(msg,..)" />
<aop:after pointcut-ref="simplePointcut" Method="after"/>
</aop:aspect>
</aop:config>
```

上面的代码 args(msg,..)是指将切入点方法上的第一个 String 类型参数添加到参数名为 msg 的通知的入参上，这样就可以直接使用该参数啦。

访问当前的连接点在上面的 Aspect 切面 Bean 中已经看到了，每个通知方法第一个参数都是 JoinPoint。其实，在 Spring中，任何通知（Advice）方法都可以将第一个参数定义为 org.aspectj.lang.JoinPoint 类型用以接受当前连接点对象。JoinPoint 接口提供了一系列有用的方法， 比如 getArgs() （返回方法参数）、getThis() （返回代理对象）、getTarget() （返回目标）、getSignature() （返回正在被通知的方法相关信息）和 toString() （打印出正在被通知的方法的有用信息）。

## SpringAOP设计原理及源码分析

