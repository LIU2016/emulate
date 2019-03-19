[TOC]

# 设计模式是什么有什么作用

解决一些具有代表新的一些问题，就是经验。
设计模式提升代码的可读性、可扩展性、维护成本、复杂的业务问题。
设计模式 -- 生活案例

# 设计模式在应用中遵循的六大原则

- 开闭原则
  开闭原则就是说对扩展开放，对修改关闭。在程序需要进行拓展的时候，不能去修改原有的代码，实现一个热插拔的效果。所以一句话概括就是：为了使程序的扩展性好，易于维护和升级。想要达到这样的效果，我们需要使用接口和抽象类，后面的具体设计中我们会提到这点
- 里氏代换原则
  里氏代换原则(LiskovSubstitutionPrincipleLSP)
  面向对象设计的基本原则之一。里氏代换原则中说，任何基类可以出现的地方，子类一定可以出现。LSP是继承复用的基石，只有当衍生类可以替换掉基类，软件单位的功能不受到影响时，基类才能真正被复用，而衍生类也能够在基类的基础上增加新的行为。里氏代换原则是对“开-闭”原则的补充。
  实现“开-闭”原则的关键步骤就是抽象化。而基类与子类的继承关系就是抽象化的具体实现，所以里氏代换原则是对实现抽象化的具体步骤的规范。
- 依赖倒转原则
  这个是开闭原则的基础，具体内容：针对接口编程，依赖于抽象而不依赖于具体。
- 接口隔离原则
  这个原则的意思是：使用多个隔离的接口，比使用单个接口要好。还是一个降低类之间的耦合度的意思，从这儿我们看出，其实设计模式就是一个软件的设计思想，从大型软件架构出发，为了升级和维护方便。所以上文中多次出现：降低依赖，降低耦合。
- 迪米特法则
  为什么叫最少知道原则，就是说：一个实体应当尽量少的与其他实体之间发生相互作用，使得系统功能模块相对独立
- 合成复用原则
  原则是尽量使用合成/聚合的方式，而不是使用继承。

# 创建型

## 工厂模式

集体生活-没有标准-私有制-小作坊（提升产品质量，提高生产的效率）-工厂式（大规模的标准化的排量的生产）-流水线（一条流水线只生产一个产品）
解决了用户与产品之间的问题

- 小作坊-简单工厂模式
  产品统一标准
  1，创建产品的过程隐藏了，对于用户完全不清楚
  2，有统一的标准接口
  3，批量生产、标准化
  例如：spring中的BeanFactory
- 工厂式-工厂方法模式
  工厂统一标准（接口）
  将工厂实现统一标准
- 流水线-抽象工厂模式
  1，有抽象的工厂类
  获取工厂的方式在抽象工厂中定义
  2，定义实现抽象工厂的具体类。分别实现抽象中获取工厂的方法。
  3，可以将公共逻辑写在抽象过程中
  4，易于扩展

## 单例模式

- 懒汉
- 饿汉
- 静态内部类
- 注册/枚举
- 序列化与反序列保持一致：重写readResolve

## 原型模式

- Cloneable
  继承Cloneable
  浅拷贝：拷贝地址
  深拷贝：拷贝属性，产生不同对象 。用字节码流重写一个
- 反射

# 结构型

## 代理模式

应用场景：为其他对象提供一种代理以控制对这个对象的访问。从结构上来看和Decorator模式类似，但Proxy是控制，更像是一种对功能的限制，而Decorator是增加职责。Spring的Proxy模式在AOP中有体现，比如JdkDynamicAopProxy和Cglib2AopProxy。
租房中介、售票黄牛、婚介、经纪人、快递、事务代理、非侵入式日志监听
静态代理和动态代理的根本区别：静态代理在代理之前，所有的东西都是已知的。动态代理就不需要了，未知的，自动化，智能的。

- 动态代理

  1.代理对象,不需要实现接口
  2.代理对象的生成,是利用JDK的API,动态的在内存中构建代理对象(需要我们指定创建代理对象/目标对象实现的接口的类型)
  3.动态代理也叫做:JDK代理,接口代理

  - JDK中生成代理对象的API

    代理类所在包:java.lang.reflect.Proxy
    JDK实现代理只需要使用newProxyInstance方法,但是该方法需要接收三个参数,完整的写法是:
    static Object newProxyInstance(ClassLoader loader, Class<?>[] interfaces,InvocationHandler h )注意该方法是在Proxy类中是静态方法,且接收的三个参数依次为:
    ClassLoader loader,:指定当前目标对象使用类加载器,获取加载器的方法是固定的
    Class<?>[] interfaces,:目标对象实现的接口的类型,使用泛型方式确认类型
    InvocationHandler h:事件处理,执行目标对象的方法时,会触发事件处理器的方法,会把当前执行目标对象的方法作为参数传入。
    代理对象不需要实现接口,但是目标对象一定要实现接口,否则不能用动态代理​

    ```java
    /**
    * 接口
    */
    public interface IUserDao {
    void save();
    }
    
    目标对象:UserDao.java
    /**
    * 接口实现
    * 目标对象
    */
    public class UserDao implements IUserDao {
    public void save() {
    System.out.println("----已经保存数据!----");
    }
    }
    
    /**
    * 创建动态代理对象
    * 动态代理不需要实现接口,但是需要指定接口类型
    */
    public class ProxyFactory{
    //维护一个目标对象
    private Object target;
    public ProxyFactory(Object target){
    this.target=target;
    }
    //给目标对象生成代理对象
    public Object getProxyInstance(){
    return Proxy.newProxyInstance(
    target.getClass().getClassLoader(),
    target.getClass().getInterfaces(),
    new InvocationHandler() {
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
    System.out.println("开始事务2");
    //执行目标对象方法
    Object returnValue = method.invoke(target, args);
    System.out.println("提交事务2");
    return returnValue;
    }
    }
    );
    }
    }
    
    /**
    * 测试类
    */
    public class App {
    public static void main(String[] args) {
    // 目标对象
    IUserDao target = new UserDao();
    // 【原始的类型 class cn.itcast.b_dynamic.UserDao】
    System.out.println(target.getClass());
    // 给目标对象，创建代理对象
    IUserDao proxy = (IUserDao) new ProxyFactory(target).getProxyInstance();
    // class $Proxy0 内存中动态生成的代理对象
    System.out.println(proxy.getClass());
    // 执行方法 【代理对象】
    proxy.save();
    }
    }
    ```

  - Cglib代理
    上面的静态代理和动态代理模式都是要求目标对象是实现一个接口的目标对象,但是有时候目标对象只是一个单独的对象,并没有实现任何的接口,这个时候就可以使用以目标对象子类的方式类实现代理,这种方法就叫做:Cglib代理 。
    ​
    Cglib代理,也叫作子类代理,它是在内存中构建一个子类对象从而实现对目标对象功能的扩展.JDK的动态代理有一个限制,就是使用动态代理的对象必须实现一个或多个接口,如果想代理没有实现接口的类,就可以使用Cglib实现.Cglib是一个强大的高性能的代码生成包,它可以在运行期扩展java类与实现java接口.它广泛的被许多AOP的框架使用,例如Spring AOP和synaop,为他们提供方法的interception(拦截).
    Cglib包的底层是通过使用一个小而块的字节码处理框架ASM来转换字节码并生成新的类.不鼓励直接使用ASM,因为它要求你必须对JVM内部结构包括class文件的格式和指令集都很熟悉.

    1.需要引入cglib的jar文件,但是Spring的核心包中已经包括了Cglib功能,所以直接引入pring-core-3.2.5.jar即可.
    2.引入功能包后,就可以在内存中动态构建子类
    3.代理的类不能为final,否则报错
    4.目标对象的方法如果为final/static,那么就不会被拦截,即不会执行目标对象额外的业务方法.​

    ```java
    目标对象类:UserDao.java
    /**
    * 目标对象,没有实现任何接口
    */
    public class UserDao {
    public void save() {
    System.out.println("----已经保存数据!----");
    }
    }
    Cglib代理工厂:ProxyFactory.java
    /**
    * Cglib子类代理工厂
    * 对UserDao在内存中动态构建一个子类对象
    */
    public class ProxyFactory implements MethodInterceptor{
    //维护目标对象
    private Object target;
    public ProxyFactory(Object target) {
    this.target = target;
    }
    //给目标对象创建一个代理对象
    public Object getProxyInstance(){
    //1.工具类
    Enhancer en = new Enhancer();
    //2.设置父类
    en.setSuperclass(target.getClass());
    //3.设置回调函数
    en.setCallback(this);
    //4.创建子类(代理对象)
    return en.create();
    }
    @Override
    public Object intercept(Object obj, Method method, Object[] args, MethodProxy proxy) throws Throwable {
    System.out.println("开始事务...");
    //执行目标对象的方法
    Object returnValue = method.invoke(target, args);
    System.out.println("提交事务...");
    return returnValue;
    }
    }
    测试类:
    /**
    * 测试类
    */
    public class App {
    @Test
    public void test(){
    //目标对象
    UserDao target = new UserDao();
    //代理对象
    UserDao proxy = (UserDao)new ProxyFactory(target).getProxyInstance();
    //执行代理对象的方法
    proxy.save();
    }
    }
    ```

- 静态代理
  做决定的方法 - 就是A对象中引用B对象的方法。

- 字节码重组
  1，拿到所有的被代理类的接口和方法
  2，根据上述条件生成新的类
  3，

## 装饰者模式

通过构造方法包装上一级类，注重覆盖和扩展，IS-A的关系，有层级关系。装饰者与被装饰者实现同一个接口，同宗同源IO流。

动态的将责任附加到对象上(因为利用组合而不是继承来实现，而组合是可以在运行时进行随机组合的)。若要扩展功能，装饰者提供了比继承更富有弹性的替代方案(同样地，通过组合可以很好的避免类暴涨，也规避了继承中的子类必须无条件继承父类所有属性的弊端)。

## 适配器模式

老系统运行很久比较稳定，为了保持稳定，要向下兼容，采用该模式。
1，继承。2，使用老类的对象。
基本都是以Adapter结尾的类

将一个类的接口，转换成客户期望的另外一个接口。适配器让原本接口不兼容的类可以很好的合作。

## 区别

适配器模式：包装另一个对象，并提供**不同的接口**。

外观模式：包装**许多**对象，以简化他们的接口。

装饰者模式：包装另一个对象，并提供**额外的行为**。

代理模式：包装另一个对象，并**控制对它的访问**。

从它们的定义中可以总结出以下几点区别：

1）适配器模式强调的是转换接口。举例：JDBC是java定义的数据库操作规范，其已经定义好了操作数据库的接口，假设一个数据库厂商提供了一套操作数据库的接口，但是该接口并不符合JDBC的规范，也就是说JDBC规范规定的接口和数据库厂商提供的接口不一致。这个时候就可以使用适配器模式将数据库厂商的接口转换成JDBC规范要求的接口。其他三种模式均不提供接口转换的功能。

```
InputStreamReader继承了Reader抽象类并实现，且持有了InputStream的引用，这里是通过StreamDecoder类间接持有的，因为从byte到char要经过编码。 
很显然，适配器就是InputStreamReader，源角色就是InputStream代表的实例对象，目标接口就是Reader类。OutputStreamWriter 也类似。 
在I.O类库中还有很多类似的用法，如StringReader将一个string类适配到Reader接口，ByteArrayInputStream适配器将byte数组适配到InputStream流接口处理。
```

```
将Connection接口适配成DataSource
```

2）外观模式强调的是包装多个对象，以简化他们的接口。想象这样一种场景：你家的电器都是智能控制的，当你回家的时候你要打开空调、打开电视、打开热水器等等，这些都需要你自己一个个的去操作，这个时候你就会有这样一种需求，就是当你到家的时候只要进行一个操作，就能依次打开空调、电视、热水器等。这个时候就可以使用外观模式将空调、电视、热水器等的接口进行包装，只对外提供一个按钮。其他三种模式均强调的是对一个对象的包装。

3）装饰者模式强调的是为被装饰对象增加额外的行为。举例：java.io包。

```
InputeStream 类就是以抽象组件存在的：而FileInputStream就是具体组件，它实现了抽象组件的所有接口；FilterInputStream类无疑就是装饰角色，它实现了InputStream类的所有接口，并且持有InputStream的对象实例的引用； 
BufferedInputStream是具体的装饰器实现者，它给InputStream类附加了功能，这个装饰器类的作用就是使得InputStream读取的数据保存在内存中，而提高读取的性能。

与这个装饰器类有类似功能的还有LineNumberInputStream（java 1.8 已经过期）类，它的作用就是提高行按行读取数据的功能，它们都是InputStream类增强了功能，或者提升了性能。

装饰器与适配器都有一个别名叫做 包装模式(Wrapper)，它们看似都是起到包装一个类或对象的作用，但是使用它们的目的很不一一样。适配器模式的意义是要将一个接口转变成另一个接口，它的目的是通过改变接口来达到重复使用的目的。 

而装饰器模式不是要改变被装饰对象的接口，而是恰恰要保持原有的接口，但是增强原有对象的功能，或者改变原有对象的处理方式而提升性能。所以这两个模式设计的目的是不同的。
```

```
应用场景：在我们的项目中遇到这样一个问题：我们的项目需要连接多个数据库，而且不同的客户在每次访问中根据需要会去访问不同的数据库。我们以往在Spring和Hibernate框架中总是配置一个数据源，因而SessionFactory的DataSource属性总是指向这个数据源并且恒定不变，所有DAO在使用SessionFactory的时候都是通过这个数据源访问数据库。

但是现在，由于项目的需要，我们的DAO在访问SessionFactory的时候都不得不在多个数据源中不断切换，

问题就出现了：如何让SessionFactory在执行数据持久化的时候，根据客户的需求能够动态切换不同的数据源？我们能不能在Spring的框架下通过少量修改得到解决？是否有什么设计模式可以利用呢？首先想到在Spring的ApplicationContext中配置所有的DataSource。这些DataSource可能是各种不同类型的，比如不同的数据库：Oracle、SQLServer、MySQL等，也可能是不同的数据源：比如Apache提供的org.apache.commons.dbcp.BasicDataSource、Spring提供的org.springframework.jndi.JndiObjectFactoryBean等。然后SessionFactory根据客户的每次请求，将dataSource属性设置成不同的数据源，以到达切换数据源的目的。

Spring中用到的包装器模式在类名上有两种表现：一种是类名中含有Wrapper，另一种是类名中含有Decorator。基本上都是动态地给一个对象添加一些额外的职责。
```

4）代理模式强调的是对被代理对象进行控制。这些控制体现在很多方面，比如安全、权限控制等。

# 行为型

## 策略模式

1、最终执行结果是固定的。
2、执行过程和执行逻辑不一样。
--- 应该目标一致，通过不同的行为方式去做到
以Strategy结尾的​
支付、旅行

## 模板方法模式

1、执行流程固定，但中间有些步骤有细微差别（运
行时才确定）。
2、可实现批量生产
Spring ORM 数据模型

## 委派模式

干活是你的（普通员工），功劳是我的（项目经理）
以Dispatcher结尾的类大多都是委派模式。
\--
org.springframework.web.servlet.DispatcherServlet
经理派发工作任务

- 委派模式（Delegate）是面向对象设计模式中常用的一种模式。这种模式的原理为类B和类A是两个互相没有任何关系的类，B具有和A一模一样的方法和属性；并且调用B中的方法，属性就是调用A中同名的方法和属性。B好像就是一个受A授权委托的中介。第三方的代码不需要知道A的存在，也不需要和A发生直接的联系，通过B就可以直接使用A的功能，这样既能够使用到A的各种公能，又能够很好的将A保护起来了。
- 框架中的例子
  - mybatis
    - CachingExecutor

## 观察者模式

应用场景：定义对象间的一种一对多的依赖关系，当一个对象的状态发生改变时，所有依赖于它的对象都得到通知并被自动更新。Spring中Observer模式常用的地方是Listener的实现。如ApplicationListener。
监听器

- java实现 - 推的模式 广播。 拉模式就是自动去取

  ![img](https://img.mubu.com/document_image/d72dc0aa-651a-45c5-9917-5a7f3643dd87-862021.jpg)

- 事件/监听模式

  - java.util.EventObject : 事件对象
  - java.util.EventListener：事件监听接口
  - Java中的事件监听机制主要由事件源、事件对象、事件监听器三个部分组成。
    1）事件源（event source）：
    具体的事件源，比如说，你点击一个button，那么button就是event source，要想使button对某些事件进行响应，你就需要注册特定的listener。
    2）事件对象（event object）：
    一般继承自java.util.EventObject类，封装了事件源对象以及与事件相关的信息。它是在事件源和事件监听器之间传递信息的。
    3）事件监听器（event listener）：
    实现java.util.EventListener接口,需要注册在事件源上才能被调用。它监听事件，并进行事件处理或者转发。

- 区别

  ![img](https://img.mubu.com/document_image/tos_6b2a0f64-acbb-426a-bc22-da4b68056900-862021.jpg)



  # 参考文档

  - <https://www.cnblogs.com/jackson-zhangjiang/p/7784694.html> 事件模式和观察者模式区别
  - <https://blog.csdn.net/qq_22873427/article/details/77169781>

