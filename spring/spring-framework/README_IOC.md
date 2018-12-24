[TOC]

### 什么是 IOC/DI

IOC(Inversion of Control)控制反转：所谓控制反转，就是**把原先我们代码里面需要实现的对象创建、依赖的代码，反转给容器来帮忙实现。**那么必然的我们需要创建一个容器，同时需要一种描述来让容器知道需要创建的对象与对象的关系。这个描述最具体表现就是我们可配置的文件。

DI(Dependency Injection)依赖注入：就是指对象是被动接受依赖类而不是自己主动去找，换句话说就是指对象不是从容器中查找它依赖的类，而是在容器实例化对象的时候主动将它依赖的类注入给它。

先从我们自己设计这样一个视角来考虑：

对象和对象关系怎么表示？可以用 xml，properties 文件等语义化配置文件表示。

描述对象关系的文件存放在哪里？可能是 classpath，filesystem，或者是 URL 网络资源，servletContext 等。

回到正题，有了配置文件，还需要对配置文件解析。

不同的配置文件对对象的描述不一样，如标准的，自定义声明式的，如何统一？在内部需要有一个统一的关于对象的定义，所有外部的描述都必须转化成统一的描述定义。

如何对不同的配置文件进行解析？需要对不同的配置文件语法，采用不同的解析器

### Spring核心容器体系结构

#### BeanFactory

Spring Bean 的创建是典型的工厂模式，这一系列的 Bean 工厂，也即 IOC 容器为开发者管理对象间的依赖关系提供了很多便利和基础服务，在 Spring 中有许多的 IOC 容器的实现供用户选择和使用，其相互关系如下

其中 BeanFactory 作为最顶层的一个接口类，它定义了 IOC 容器的基本功能规范，BeanFactory 有三个子类：ListableBeanFactory、HierarchicalBeanFactory 和 AutowireCapableBeanFactory。但是从上图中我们可以发现最终的默认实现类是 DefaultListableBeanFactory，他实现了所有的接口。

那为何要定义这么多层次的接口呢？查阅这些接口的源码和说明发现，每个接口都有他使用的场合，它主要是为了区分在 Spring 内部在操作过程中对象的传递和转化过程中，对对象的数据访问所做的限制。

例如 ListableBeanFactory 接口表示这些 Bean 是可列表的，而 HierarchicalBeanFactory 表示的是这些 Bean 是有继承关系的，也就是每个Bean 有可能有父Bean。AutowireCapableBeanFactory接口定义 Bean 的自动装配规则。这四个接口共同定义了 Bean 的集合、Bean 之间的关系、以及 Bean行为.

在 BeanFactory 里只对 IOC 容器的基本行为作了定义，根本不关心你的 Bean 是如何定义怎样加载的。正如我们只关心工厂里得到什么的产品对象，至于工厂是怎么生产这些对象的，这个基本的接口不关心。而要知道工厂是如何产生对象的，我们需要看具体的 IOC 容器实现，Spring 提供了许多 IOC 容器的实现。比如 XmlBeanFactory，ClasspathXmlApplicationContext 等。其中 XmlBeanFactory 就是针对最基本的 IOC 容器的实现，这个 IOC 容器可以读取 XML 文件定义的 BeanDefinition（XML 文件中对 bean 的描述）,如果说 XmlBeanFactory 是容器中的屌丝，ApplicationContext 应该算容器中的高帅富.

ApplicationContext 是 Spring 提供的一个高级的 IOC 容器，它除了能够提供 IOC 容器的基本功能外，还为用户提供了以下的附加服务。从 ApplicationContext 接口的实现，我们看出其特点：

1.支持信息源，可以实现国际化。（实现 MessageSource 接口）
2.访问资源。(实现 ResourcePatternResolver 接口，后面章节会讲到)
3.支持应用事件。(实现 ApplicationEventPublisher 接口)

#### BeanDefinition

SpringIOC 容器管理了我们定义的各种 Bean 对象及其相互的关系，Bean 对象在 Spring 实现中是以 BeanDefinition 来描述的，其继承体系如下：

Bean 的解析过程非常复杂，功能被分的很细，因为这里需要被扩展的地方很多，必须保证有足够的灵活性，以应对可能的变化。Bean 的解析主要就是对 Spring 配置文件的解析。这个解析过程主要通过下图中的类完成：

### IOC容器的初始化

IOC 容器的初始化包括 BeanDefinition 的 Resource **定位、载入和注册**这三个基本的过程。我们以 ApplicationContext 为例讲解，ApplicationContext 系列容器也许是我们最熟悉的，因为 Web项 目 中 使 用 的 XmlWebApplicationContext 就 属 于 这 个 继 承 体 系 ， 还 有ClasspathXmlApplicationContext 等，其继承体系如下图所示

ApplicationContext 允许上下文嵌套，通过保持父上下文可以维持一个上下文体系。对于 Bean 的查找可以在这个上下文体系中发生，首先检查当前上下文，其次是父上下文，逐级向上，这样为不同的Spring 应用提供了一个共享的 Bean 定义环境。

下面我们分别简单地演示一下两种 IOC 容器的创建过程：

#### XmlBeanFactory屌丝IOC

XmlBeanFactory(屌丝 IOC)的整个流程通过 XmlBeanFactory 的源码，我们可以发现:

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

package org.springframework.beans.factory.xml;

import org.springframework.beans.BeansException;
import org.springframework.beans.factory.BeanFactory;
import org.springframework.beans.factory.support.DefaultListableBeanFactory;
import org.springframework.core.io.Resource;

/**
 * Convenience extension of {@link DefaultListableBeanFactory} that reads bean definitions
 * from an XML document. Delegates to {@link XmlBeanDefinitionReader} underneath; effectively
 * equivalent to using an XmlBeanDefinitionReader with a DefaultListableBeanFactory.
 *
 * <p>The structure, element and attribute names of the required XML document
 * are hard-coded in this class. (Of course a transform could be run if necessary
 * to produce this format). "beans" doesn't need to be the root element of the XML
 * document: This class will parse all bean definition elements in the XML file.
 *
 * <p>This class registers each bean definition with the {@link DefaultListableBeanFactory}
 * superclass, and relies on the latter's implementation of the {@link BeanFactory} interface.
 * It supports singletons, prototypes, and references to either of these kinds of bean.
 * See {@code "spring-beans-3.x.xsd"} (or historically, {@code "spring-beans-2.0.dtd"}) for
 * details on options and configuration style.
 *
 * <p><b>For advanced needs, consider using a {@link DefaultListableBeanFactory} with
 * an {@link XmlBeanDefinitionReader}.</b> The latter allows for reading from multiple XML
 * resources and is highly configurable in its actual XML parsing behavior.
 *
 * @author Rod Johnson
 * @author Juergen Hoeller
 * @author Chris Beams
 * @since 15 April 2001
 * @see org.springframework.beans.factory.support.DefaultListableBeanFactory
 * @see XmlBeanDefinitionReader
 * @deprecated as of Spring 3.1 in favor of {@link DefaultListableBeanFactory} and
 * {@link XmlBeanDefinitionReader}
 */
@Deprecated
@SuppressWarnings({"serial", "all"})
public class XmlBeanFactory extends DefaultListableBeanFactory {

   private final XmlBeanDefinitionReader reader = new XmlBeanDefinitionReader(this);


   /**
    * Create a new XmlBeanFactory with the given resource,
    * which must be parsable using DOM.
    * @param resource the XML resource to load bean definitions from
    * @throws BeansException in case of loading or parsing errors
    */
   public XmlBeanFactory(Resource resource) throws BeansException {
      this(resource, null);
   }

   /**
    * Create a new XmlBeanFactory with the given input stream,
    * which must be parsable using DOM.
    * @param resource the XML resource to load bean definitions from
    * @param parentBeanFactory parent bean factory
    * @throws BeansException in case of loading or parsing errors
    */
   public XmlBeanFactory(Resource resource, BeanFactory parentBeanFactory) throws BeansException {
      super(parentBeanFactory);
      this.reader.loadBeanDefinitions(resource);
   }

}
```

参照源码，自己演示一遍，理解定位、载入、注册的全过程

```java
// 根据 Xml 配置文件创建 Resource 资源对象，该对象中包含了 BeanDefinition 的信息
ClassPathResource resource = new ClassPathResource("application-context.xml");
// 创建 DefaultListableBeanFactory
DefaultListableBeanFactory factory = new DefaultListableBeanFactory();
//创建 XmlBeanDefinitionReader 读取器，用于载入 BeanDefinition。
// 之所以需要 BeanFactory 作为参数，是因为会将读取的信息回调配置给 factory
XmlBeanDefinitionReader reader = new XmlBeanDefinitionReader(factory);
// XmlBeanDefinitionReader 执行载入 BeanDefinition 的方法，最后会完成 Bean 的载入和注册。
// 完成后 Bean 就成功的放置到 IOC 容器当中，以后我们就可以从中取得 Bean 来使用
reader.loadBeanDefinitions(resource);
```

通过前面的源码，XmlBeanDefinitionReader reader = new XmlBeanDefinitionReader(this);中其中 this 传的是 factory 对象。

#### FileSystemXmlApplicationContext高富帅版IOC解剖

ApplicationContext = new FileSystemXmlApplicationContext(xmlPath);先看其构造函数的调用：

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

package org.springframework.context.support;

import org.springframework.beans.BeansException;
import org.springframework.context.ApplicationContext;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.lang.Nullable;

/**
 * Standalone XML application context, taking the context definition files
 * from the file system or from URLs, interpreting plain paths as relative
 * file system locations (e.g. "mydir/myfile.txt"). Useful for test harnesses
 * as well as for standalone environments.
 *
 * <p><b>NOTE:</b> Plain paths will always be interpreted as relative
 * to the current VM working directory, even if they start with a slash.
 * (This is consistent with the semantics in a Servlet container.)
 * <b>Use an explicit "file:" prefix to enforce an absolute file path.</b>
 *
 * <p>The config location defaults can be overridden via {@link #getConfigLocations},
 * Config locations can either denote concrete files like "/myfiles/context.xml"
 * or Ant-style patterns like "/myfiles/*-context.xml" (see the
 * {@link org.springframework.util.AntPathMatcher} javadoc for pattern details).
 *
 * <p>Note: In case of multiple config locations, later bean definitions will
 * override ones defined in earlier loaded files. This can be leveraged to
 * deliberately override certain bean definitions via an extra XML file.
 *
 * <p><b>This is a simple, one-stop shop convenience ApplicationContext.
 * Consider using the {@link GenericApplicationContext} class in combination
 * with an {@link org.springframework.beans.factory.xml.XmlBeanDefinitionReader}
 * for more flexible context setup.</b>
 *
 * @author Rod Johnson
 * @author Juergen Hoeller
 * @see #getResource
 * @see #getResourceByPath
 * @see GenericApplicationContext
 */
public class FileSystemXmlApplicationContext extends AbstractXmlApplicationContext {

   /**
    * Create a new FileSystemXmlApplicationContext for bean-style configuration.
    * @see #setConfigLocation
    * @see #setConfigLocations
    * @see #afterPropertiesSet()
    */
   public FileSystemXmlApplicationContext() {
   }

   /**
    * Create a new FileSystemXmlApplicationContext for bean-style configuration.
    * @param parent the parent context
    * @see #setConfigLocation
    * @see #setConfigLocations
    * @see #afterPropertiesSet()
    */
   public FileSystemXmlApplicationContext(ApplicationContext parent) {
      super(parent);
   }

   /**
    * Create a new FileSystemXmlApplicationContext, loading the definitions
    * from the given XML file and automatically refreshing the context.
    * @param configLocation file path
    * @throws BeansException if context creation failed
    */
   public FileSystemXmlApplicationContext(String configLocation) throws BeansException {
      this(new String[] {configLocation}, true, null);
   }

   /**
    * Create a new FileSystemXmlApplicationContext, loading the definitions
    * from the given XML files and automatically refreshing the context.
    * @param configLocations array of file paths
    * @throws BeansException if context creation failed
    */
   public FileSystemXmlApplicationContext(String... configLocations) throws BeansException {
      this(configLocations, true, null);
   }

   /**
    * Create a new FileSystemXmlApplicationContext with the given parent,
    * loading the definitions from the given XML files and automatically
    * refreshing the context.
    * @param configLocations array of file paths
    * @param parent the parent context
    * @throws BeansException if context creation failed
    */
   public FileSystemXmlApplicationContext(String[] configLocations, ApplicationContext parent) throws BeansException {
      this(configLocations, true, parent);
   }

   /**
    * Create a new FileSystemXmlApplicationContext, loading the definitions
    * from the given XML files.
    * @param configLocations array of file paths
    * @param refresh whether to automatically refresh the context,
    * loading all bean definitions and creating all singletons.
    * Alternatively, call refresh manually after further configuring the context.
    * @throws BeansException if context creation failed
    * @see #refresh()
    */
   public FileSystemXmlApplicationContext(String[] configLocations, boolean refresh) throws BeansException {
      this(configLocations, refresh, null);
   }

   /**
    * Create a new FileSystemXmlApplicationContext with the given parent,
    * loading the definitions from the given XML files.
    * @param configLocations array of file paths
    * @param refresh whether to automatically refresh the context,
    * loading all bean definitions and creating all singletons.
    * Alternatively, call refresh manually after further configuring the context.
    * @param parent the parent context
    * @throws BeansException if context creation failed
    * @see #refresh()
    */
   public FileSystemXmlApplicationContext(
         String[] configLocations, boolean refresh, @Nullable ApplicationContext parent)
         throws BeansException {

      super(parent);
      setConfigLocations(configLocations);
      if (refresh) {
         refresh();
      }
   }


   /**
    * Resolve resource paths as file system paths.
    * <p>Note: Even if a given path starts with a slash, it will get
    * interpreted as relative to the current VM working directory.
    * This is consistent with the semantics in a Servlet container.
    * @param path path to the resource
    * @return the Resource handle
    * @see org.springframework.web.context.support.XmlWebApplicationContext#getResourceByPath
    */
   @Override
   protected Resource getResourceByPath(String path) {
      if (path.startsWith("/")) {
         path = path.substring(1);
      }
      return new FileSystemResource(path);
   }

}
```

##### 设置资源加载器和资源定位

通过分析FileSystemXmlApplicationContext 的源代码可以知道，在创建FileSystemXmlApplicationContext 容器时，构造方法做以下两项重要工作：

首先，调用父类容器的构造方法(super(parent)方法)为容器设置好 Bean 资源加载器。然 后 ， 再 调 用 父 类 AbstractRefreshableConfigApplicationContext 的setConfigLocations(configLocations)方法设置 Bean 定义资源文件的定位路径。通 过 追 踪 FileSystemXmlApplicationContext 的 继 承 体 系 ， 发 现 其 父 类 的 父 类
AbstractApplicationContext 中初始化 IOC 容器所做的主要源码如下：

```java
/**
 * Create a new AbstractApplicationContext with no parent.
 */
public AbstractApplicationContext() {
   this.resourcePatternResolver = getResourcePatternResolver();
}
```

```java
/**
	 * Set the config locations for this application context in init-param style,
	 * i.e. with distinct locations separated by commas, semicolons or whitespace.
	 * <p>If not set, the implementation may use a default as appropriate.
	 */
	public void setConfigLocation(String location) {
		setConfigLocations(StringUtils.tokenizeToStringArray(location, CONFIG_LOCATION_DELIMITERS));
	}

/**
 * Set the config locations for this application context.
 * <p>If not set, the implementation may use a default as appropriate.
 */
public void setConfigLocations(@Nullable String... locations) {
   if (locations != null) {
      Assert.noNullElements(locations, "Config locations must not be null");
      this.configLocations = new String[locations.length];
      for (int i = 0; i < locations.length; i++) {
         this.configLocations[i] = resolvePath(locations[i]).trim();
      }
   }
   else {
      this.configLocations = null;
   }
}
```

通过这两个方法的源码我们可以看出，我们既可以使用一个字符串来配置多个 Spring Bean 定义资源文件，也可以使用字符串数组，即下面两种方式都是可以的：ClasspathResource res = new ClasspathResource(“a.xml,b.xml,……”);多个资源文件路径之间可以是用” , ; \t\n”等分隔。

B. ClasspathResource res = new ClasspathResource(newString[]{“a.xml”,”b.xml”,……});至此，SpringIOC 容器在初始化时将配置的 Bean 定义资源文件定位为 Spring 封装的 Resource。

#### AbstractApplicationContext的refresh函数载入Bean 定义过程

SpringIOC 容器对 Bean 定义资源的载入是从 refresh()函数开始的，refresh()是一个模板方法，refresh()方法的作用是：**在创建 IOC 容器前，如果已经有容器存在，则需要把已有的容器销毁和关闭，以保证在 refresh 之后使用的是新建立起来的 IOC 容器**。refresh 的作用类似于对 IOC 容器的重启，在新建立好的容器中对容器进行初始化，对 Bean 定义资源进行载入。

FileSystemXmlApplicationContext通过调用其父类AbstractApplicationContext的refresh()函数启动整个 IOC 容器对 Bean 定义的载入过程：

```java
Override
public void refresh() throws BeansException, IllegalStateException {
synchronized (this.startupShutdownMonitor) {
//调用容器准备刷新的方法，获取容器的当时时间，同时给容器设置同步标识
prepareRefresh();
//告诉子类启动 refreshBeanFactory()方法，Bean 定义资源文件的载入从
//子类的 refreshBeanFactory()方法启动
ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();
//为 BeanFactory 配置容器特性，例如类加载器、事件处理器等
prepareBeanFactory(beanFactory);
try {
//为容器的某些子类指定特殊的 BeanPost 事件处理器
postProcessBeanFactory(beanFactory);
//调用所有注册的 BeanFactoryPostProcessor 的 Bean
invokeBeanFactoryPostProcessors(beanFactory);
//为 BeanFactory 注册 BeanPost 事件处理器.
//BeanPostProcessor 是 Bean 后置处理器，用于监听容器触发的事件
registerBeanPostProcessors(beanFactory);
//初始化信息源，和国际化相关.
initMessageSource();
//初始化容器事件传播器.
initApplicationEventMulticaster();
//调用子类的某些特殊 Bean 初始化方法
onRefresh();
//为事件传播器注册事件监听器.
registerListeners();
//初始化所有剩余的单例 Bean
finishBeanFactoryInitialization(beanFactory);
//初始化容器的生命周期事件处理器，并发布容器的生命周期事件
finishRefresh();
}
catch (BeansException ex) {
if (logger.isWarnEnabled()) {
logger.warn("Exception encountered during context initialization - " +
"cancelling refresh attempt: " + ex);
}
//销毁已创建的 Bean
destroyBeans();
//取消 refresh 操作，重置容器的同步标识.
cancelRefresh(ex);
throw ex;
}
finally {
resetCommonCaches();
}
}
}
```

refresh()方法主要为 IOC 容器 Bean 的生命周期管理提供条件，Spring IOC 容器载入 Bean 定义资源文 件 从 其 子 类 容 器 的 refreshBeanFactory() 方 法 启 动 ， 所 以 整 个 refresh() 中“ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();”这句以后代码的都是注册容器的信息源和生命周期事件，载入过程就是从这句代码启动。

refresh()方法的作用是：在创建 IOC 容器前，如果已经有容器存在，则需要把已有的容器销毁和关闭，以保证在 refresh 之后使用的是新建立起来的 IOC 容器。refresh 的作用类似于对 IOC 容器的重启，在新建立好的容器中对容器进行初始化，对 Bean 定义资源进行载入

##### AbstractApplicationContext的obtainFreshBeanFactory()方法

AbstractApplicationContext 的 obtainFreshBeanFactory() 方 法 调 用 子 类 容 器 的refreshBeanFactory()方法，启动容器载入 Bean 定义资源文件的过程，代码如下：

```java
/**
 * Tell the subclass to refresh the internal bean factory.
 * @return the fresh BeanFactory instance
 * @see #refreshBeanFactory()
 * @see #getBeanFactory()
 */
protected ConfigurableListableBeanFactory obtainFreshBeanFactory() {
   refreshBeanFactory();
   return getBeanFactory();
}
```

```java
/**
 * This implementation performs an actual refresh of this context's underlying
 * bean factory, shutting down the previous bean factory (if any) and
 * initializing a fresh bean factory for the next phase of the context's lifecycle.
 */
@Override
protected final void refreshBeanFactory() throws BeansException {
   if (hasBeanFactory()) {
      destroyBeans();
      closeBeanFactory();
   }
   try {
      DefaultListableBeanFactory beanFactory = createBeanFactory();
      beanFactory.setSerializationId(getId());
      customizeBeanFactory(beanFactory);
      loadBeanDefinitions(beanFactory);
      synchronized (this.beanFactoryMonitor) {
         this.beanFactory = beanFactory;
      }
   }
   catch (IOException ex) {
      throw new ApplicationContextException("I/O error parsing bean definition source for " + getDisplayName(), ex);
   }
}
```

AbstractApplicationContext 类中只抽象定义了 refreshBeanFactory()方法，容器真正调用的是其子类 AbstractRefreshableApplicationContext 实现的 refreshBeanFactory()方法

在这个方法中，先判断 BeanFactory 是否存在，如果存在则先销毁 beans 并关闭 beanFactory，接着，创建 DefaultListableBeanFactory，并调用loadBeanDefinitions(beanFactory)装载 bean 定义。

##### AbstractRefreshableApplicationContext 子类的 loadBeanDefinitions 方法

bstractRefreshableApplicationContext 中只定义了抽象的 loadBeanDefinitions 方法，容器真 正 调 用 的 是 其 子 类 AbstractXmlApplicationContext 对 该 方 法 的 实 现 ，Xml Bean 读取器(XmlBeanDefinitionReader)调用其父类 AbstractBeanDefinitionReader 的reader.loadBeanDefinitions 方法读取 Bean 定义资源。

由于我们使用 FileSystemXmlApplicationContext 作为例子分析，因此 getConfigResources 的返回值为 null，因此程序执行 reader.loadBeanDefinitions(configLocations)分支。

AbstractBeanDefinitionReader 读 取 Bean 定 义 资 源 , 在 其 抽 象 父 类AbstractBeanDefinitionReader 中定义了载入过程。

loadBeanDefinitions(Resource...resources)方法和上面分析的 3 个方法类似，同样也是调用XmlBeanDefinitionReader 的 loadBeanDefinitions 方法。

从对 AbstractBeanDefinitionReader 的loadBeanDefinitions 方法源码分析可以看出该方法做了以下两件事：

首先，调用资源加载器的获取资源方法 resourceLoader.getResource(location)，获取到要加载的资源。其次，真正执行加载功能是其子类 XmlBeanDefinitionReader 的 loadBeanDefinitions 方法。

看到上面的 ResourceLoader 与 ApplicationContext 的继承系图，可以知道其实际调用的是DefaultResourceLoader 中 的 getSource() 方 法 定 位 Resource ， 因 为FileSystemXmlApplicationContext 本身就是 DefaultResourceLoader 的实现类，所以此时又回到了 FileSystemXmlApplicationContext 中来。

**关键步骤：XmlBeanDefinitionReader.registerBeanDefinitions()**

```java
public int registerBeanDefinitions(Document doc, Resource resource) throws BeanDefinitionStoreException {
   BeanDefinitionDocumentReader documentReader = createBeanDefinitionDocumentReader();
   int countBefore = getRegistry().getBeanDefinitionCount();
   documentReader.registerBeanDefinitions(doc, createReaderContext(resource));
   return getRegistry().getBeanDefinitionCount() - countBefore;
}
```

资源加载的其他步骤（略）

经过对 Spring Bean 定义资源文件转换的 Document 对象中的元素层层解析，Spring IOC 现在已经将XML 形式定义的 Bean 定义资源文件转换为 Spring IOC 所识别的数据结构——BeanDefinition，它是Bean 定 义 资 源 文 件 中 配 置 的 POJO 对 象 在 Spring IOC 容 器 中 的 映 射 ， 我 们 可 以 通 过AbstractBeanDefinition 为入口，看到了 IOC 容器进行索引、查询和操作。

通过 Spring IOC 容器对 Bean 定义资源的解析后，IOC 容器大致完成了管理 Bean 对象的准备工作，即初始化过程，但是最为重要的依赖注入还没有发生，现在在 IOC 容器中 BeanDefinition 存储的只是一些静态信息，接下来需要向容器注册 Bean 定义信息才能全部完成 IOC 容器的初始化过程。

#### 解析过后的BeanDefinition在IOC容器中的注册

让我们继续跟踪程序的执行顺序，接下来我们来分析 DefaultBeanDefinitionDocumentReader 对Bean 定义转换的 Document 对象解析的流程中，在其 parseDefaultElement 方法中完成对 Document对 象 的 解 析 后 得 到 封 装 BeanDefinition 的 BeanDefinitionHold 对 象 ， 然 后 调 用BeanDefinitionReaderUtils 的 registerBeanDefinition 方法向 IOC 容器注册解析的 Bean，BeanDefinitionReaderUtils 的注册的源码如下：

```java
/**
 * Process the given bean element, parsing the bean definition
 * and registering it with the registry.
 */
protected void processBeanDefinition(Element ele, BeanDefinitionParserDelegate delegate) {
   BeanDefinitionHolder bdHolder = delegate.parseBeanDefinitionElement(ele);
   if (bdHolder != null) {
      bdHolder = delegate.decorateBeanDefinitionIfRequired(ele, bdHolder);
      try {
         // Register the final decorated instance.
         BeanDefinitionReaderUtils.registerBeanDefinition(bdHolder, getReaderContext().getRegistry());
      }
      catch (BeanDefinitionStoreException ex) {
         getReaderContext().error("Failed to register bean definition with name '" +
               bdHolder.getBeanName() + "'", ele, ex);
      }
      // Send registration event.
      getReaderContext().fireComponentRegistered(new BeanComponentDefinition(bdHolder));
   }
}
```

```java
/**
 * Register the given bean definition with the given bean factory.
 * @param definitionHolder the bean definition including name and aliases
 * @param registry the bean factory to register with
 * @throws BeanDefinitionStoreException if registration failed
 */
public static void registerBeanDefinition(
      BeanDefinitionHolder definitionHolder, BeanDefinitionRegistry registry)
      throws BeanDefinitionStoreException {

   // Register bean definition under primary name.
   String beanName = definitionHolder.getBeanName();
   registry.registerBeanDefinition(beanName, definitionHolder.getBeanDefinition());

   // Register aliases for bean name, if any.
   String[] aliases = definitionHolder.getAliases();
   if (aliases != null) {
      for (String alias : aliases) {
         registry.registerAlias(beanName, alias);
      }
   }
}
```

当调用 BeanDefinitionReaderUtils 向 IOC 容器注册解析的 BeanDefinition 时，真正完成注册功能的是 DefaultListableBeanFactory。

至此，Bean 定义资源文件中配置的 Bean 被解析过后，已经注册到 IOC 容器中，被容器管理起来，真正完成了 IOC 容器初始化所做的全部工作。

现在 IOC 容器中已经建立了整个 Bean 的配置信息，这些BeanDefinition 信息已经可以使用，并且可以被检索，IOC 容器的作用就是对这些注册的 Bean 定义信息进行处理和维护。这些的注册的 Bean 定义信息是 IOC 容器控制反转的基础，正是有了这些注册的数据，容器才可以进行依赖注入。

总结：现在通过上面的代码，总结一下 IOC 容器初始化的基本步骤：

(1).初始化的入口在容器实现中的 refresh()调用来完成。
(2).对 bean 定义载入 IOC 容器使用的方法是 loadBeanDefinition,

其中的大致过程如下：通过 ResourceLoader 来完成资源文件位置的定位，DefaultResourceLoader是默认的实现，同时上下文本身就给出了 ResourceLoader 的实现，可以从类路径，文件系统,URL 等方式来定为资源位置。

如果是 XmlBeanFactory 作为 IOC 容器，那么需要为它指定 bean 定义的资源，也 就 是 说 bean 定 义 文 件 时 通 过 抽 象 成 Resource 来 被 IOC 容 器 处 理 的 ， 容 器 通 过BeanDefinitionReader 来 完 成 定 义 信 息 的 解 析 和 Bean 信 息 的 注 册 , 往 往 使 用 的 是XmlBeanDefinitionReader 来 解 析 bean 的 xml 定 义 文 件 - 实 际 的 处 理 过 程 是 委 托 给BeanDefinitionParserDelegate 来完成的，从而得到 bean 的定义信息，这些信息在 Spring 中使用BeanDefinition 对 象 来 表 示 - 这 个 名 字 可 以 让 我 们 想 到loadBeanDefinition,RegisterBeanDefinition 这些相关方法-他们都是为处理 BeanDefinitin 服务的，容器解析得到 BeanDefinition 以后，需要把它在 IOC 容器中注册，这由 IOC 实现.

BeanDefinitionRegistry 接口来实现。注册过程就是在 IOC 容器内部维护的一个 HashMap 来保存得到的 BeanDefinition 的过程。这个 HashMap 是 IOC 容器持有 Bean 信息的场所，以后对 Bean 的操作都是围绕这个 HashMap 来实现的。(DefaultListableBeanFactory.beanDefinitionMap)

```java
/** Map of bean definition objects, keyed by bean name. */
private final Map<String, BeanDefinition> beanDefinitionMap = new ConcurrentHashMap<>(256);
```

然后我们就可以通过 BeanFactory 和 ApplicationContext 来享受到 SpringIOC 的服务了,在使用IOC 容器的时候，我们注意到除了少量粘合代码，绝大多数以正确 IOC 风格编写的应用程序代码完全不用关心如何到达工厂，因为容器将把这些对象与容器管理的其他对象钩在一起。

基本的策略是把工厂放到已知的地方，最好是放在对预期使用的上下文有意义的地方，以及代码将实际需要访问工厂的地方。
Spring本身提供了对声明式载入web应用程序用法的应用程序上下文,并将其存储在ServletContext中的框架实现。
以下是容器初始化全过程的时序图：

![1544080227569](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1544080227569.png)



在使用 SpringIOC 容器的时候我们还需要区别两个概念:

BeanFactory 和 FactoryBean ， 其 中 BeanFactory 指 的 是 IOC 容 器 的 编 程 抽 象 ， 比 如ApplicationContext，XmlBeanFactory 等，这些都是 IOC 容器的具体表现，需要使用什么样的容器由客户决定,但 Spring 为我们提供了丰富的选择。

#### FactoryBean 

FactoryBean 只是一个可以在 IOC容器中被管理的一个 Bean,是对各种处理过程和资源使用的抽象,FactoryBean 在需要时产生另一个对象，而不返回FactoryBean 本身,我们可以把它看成是一个抽象工厂，对它的调用返回的是工厂生产的产品。所有的FactoryBean 都实现特殊的 org.springframework.beans.factory.FactoryBean 接口，当使用容器中 FactoryBean 的时候，该容器不会返回 FactoryBean 本身,而是返回其生成的对象。

Spring 包括了**大部分的通用资源和服务访问抽象的 FactoryBean 的实现**，其中包括:对 JNDI 查询的处理，对代理对象的处理，对事务性代理的处理，对 RMI 代理的处理等，这些我们都可以看成是具体的工厂,看成是Spring 为我们建立好的工厂。也就是说 Spring 通过使用抽象工厂模式为我们准备了**一系列工厂来生产一些特定的对象**,免除我们手工重复的工作，我们要使用时只需要在 IOC 容器里配置好就能很方便的使用了。

### 基于XML 的依赖注入

#### 依赖注入发生的时间

当 Spring IOC 容器完成了 Bean 定义资源的定位、载入和解析注册以后，IOC 容器中已经管理类 Bean定义的相关数据，但是此时 IOC 容器还没有对所管理的 Bean 进行依赖注入，依赖注入在以下两种情况发生：

(1).用户第一次通过 getBean 方法向 IOC 容索要 Bean 时，IOC 容器触发依赖注入。

(2).当用户在 Bean 定义资源中为<bean>元素配置了 lazy-init 属性，即让容器在解析注册 Bean 定义时进行预实例化，触发依赖注入。

BeanFactory 接口定义了 Spring IOC 容器的基本功能规范，是 Spring IOC 容器所应遵守的最底层和最基本的编程规范。BeanFactory 接口中定义了几个 getBean 方法，就是用户向 IOC 容器索取管理的Bean 的方法，我们通过分析其子类的具体实现，理解 Spring IOC 容器在用户索取 Bean 时如何完成依赖注入。

在 BeanFactory 中我们看到 getBean（String...）函数，它的具体实现在 AbstractBeanFactory中。

#### AbstractBeanFactory通过getBean向IOC容器获取被管理的 Bean

对向 IOC 容器获取 Bean 方法的分析，我们可以看到在 Spring 中，

如果 Bean 定义的单例模式(Singleton)，则容器在创建之前先从缓存中查找，以确保整个容器中只存在一个实例对象。

如果 Bean定义的是原型模式(Prototype)，则容器每次都会创建一个新的实例对象。除此之外，Bean 定义还可以扩展为指定其生命周期范围。

```java
@SuppressWarnings("unchecked")
protected <T> T doGetBean(final String name, @Nullable final Class<T> requiredType,
      @Nullable final Object[] args, boolean typeCheckOnly) throws BeansException {

   final String beanName = transformedBeanName(name);
   Object bean;

   // Eagerly check singleton cache for manually registered singletons.
   Object sharedInstance = getSingleton(beanName);
   if (sharedInstance != null && args == null) {
      if (logger.isTraceEnabled()) {
         if (isSingletonCurrentlyInCreation(beanName)) {
            logger.trace("Returning eagerly cached instance of singleton bean '" + beanName +
                  "' that is not fully initialized yet - a consequence of a circular reference");
         }
         else {
            logger.trace("Returning cached instance of singleton bean '" + beanName + "'");
         }
      }
      bean = getObjectForBeanInstance(sharedInstance, name, beanName, null);
   }

   else {
      // Fail if we're already creating this bean instance:
      // We're assumably within a circular reference.
      if (isPrototypeCurrentlyInCreation(beanName)) {
         throw new BeanCurrentlyInCreationException(beanName);
      }

      // Check if bean definition exists in this factory.
      BeanFactory parentBeanFactory = getParentBeanFactory();
      if (parentBeanFactory != null && !containsBeanDefinition(beanName)) {
         // Not found -> check parent.
         String nameToLookup = originalBeanName(name);
         if (parentBeanFactory instanceof AbstractBeanFactory) {
            return ((AbstractBeanFactory) parentBeanFactory).doGetBean(
                  nameToLookup, requiredType, args, typeCheckOnly);
         }
         else if (args != null) {
            // Delegation to parent with explicit args.
            return (T) parentBeanFactory.getBean(nameToLookup, args);
         }
         else if (requiredType != null) {
            // No args -> delegate to standard getBean method.
            return parentBeanFactory.getBean(nameToLookup, requiredType);
         }
         else {
            return (T) parentBeanFactory.getBean(nameToLookup);
         }
      }

      if (!typeCheckOnly) {
         markBeanAsCreated(beanName);
      }

      try {
         final RootBeanDefinition mbd = getMergedLocalBeanDefinition(beanName);
         checkMergedBeanDefinition(mbd, beanName, args);

         // Guarantee initialization of beans that the current bean depends on.
         String[] dependsOn = mbd.getDependsOn();
         if (dependsOn != null) {
            for (String dep : dependsOn) {
               if (isDependent(beanName, dep)) {
                  throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                        "Circular depends-on relationship between '" + beanName + "' and '" + dep + "'");
               }
               registerDependentBean(dep, beanName);
               try {
                  getBean(dep);
               }
               catch (NoSuchBeanDefinitionException ex) {
                  throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                        "'" + beanName + "' depends on missing bean '" + dep + "'", ex);
               }
            }
         }

         // Create bean instance.
         if (mbd.isSingleton()) {
            sharedInstance = getSingleton(beanName, () -> {
               try {
                  return createBean(beanName, mbd, args);
               }
               catch (BeansException ex) {
                  // Explicitly remove instance from singleton cache: It might have been put there
                  // eagerly by the creation process, to allow for circular reference resolution.
                  // Also remove any beans that received a temporary reference to the bean.
                  destroySingleton(beanName);
                  throw ex;
               }
            });
            bean = getObjectForBeanInstance(sharedInstance, name, beanName, mbd);
         }

         else if (mbd.isPrototype()) {
            // It's a prototype -> create a new instance.
            Object prototypeInstance = null;
            try {
               beforePrototypeCreation(beanName);
               prototypeInstance = createBean(beanName, mbd, args);
            }
            finally {
               afterPrototypeCreation(beanName);
            }
            bean = getObjectForBeanInstance(prototypeInstance, name, beanName, mbd);
         }

         else {
            String scopeName = mbd.getScope();
            final Scope scope = this.scopes.get(scopeName);
            if (scope == null) {
               throw new IllegalStateException("No Scope registered for scope name '" + scopeName + "'");
            }
            try {
               Object scopedInstance = scope.get(beanName, () -> {
                  beforePrototypeCreation(beanName);
                  try {
                     return createBean(beanName, mbd, args);
                  }
                  finally {
                     afterPrototypeCreation(beanName);
                  }
               });
               bean = getObjectForBeanInstance(scopedInstance, name, beanName, mbd);
            }
            catch (IllegalStateException ex) {
               throw new BeanCreationException(beanName,
                     "Scope '" + scopeName + "' is not active for the current thread; consider " +
                     "defining a scoped proxy for this bean if you intend to refer to it from a singleton",
                     ex);
            }
         }
      }
      catch (BeansException ex) {
         cleanupAfterBeanCreationFailure(beanName);
         throw ex;
      }
   }

   // Check if required type matches the type of the actual bean instance.
   if (requiredType != null && !requiredType.isInstance(bean)) {
      try {
         T convertedBean = getTypeConverter().convertIfNecessary(bean, requiredType);
         if (convertedBean == null) {
            throw new BeanNotOfRequiredTypeException(name, requiredType, bean.getClass());
         }
         return convertedBean;
      }
      catch (TypeMismatchException ex) {
         if (logger.isTraceEnabled()) {
            logger.trace("Failed to convert bean '" + name + "' to required type '" +
                  ClassUtils.getQualifiedName(requiredType) + "'", ex);
         }
         throw new BeanNotOfRequiredTypeException(name, requiredType, bean.getClass());
      }
   }
   return (T) bean;
}
```

上面的源码只是定义了根据 Bean 定义的模式，采取的不同创建 Bean 实例对象的策略，具体的 Bean 实例 对象 的 创 建过 程由实现了 ObejctFactory 接口的匿名内部类的 createBean 方法完 成 ，ObejctFactory 使 用 委 派 模 式 ， 具 体 的 Bean 实 例 创 建 过 程 交 由 其 实 现 类AbstractAutowireCapableBeanFactory 完 成 ， 我 们 继 续 分 析AbstractAutowireCapableBeanFactory 的 createBean 方法的源码，理解其创建 Bean 实例的具体实现过程。

#### AbstractAutowireCapableBeanFactory创建Bean实例对象

AbstractAutowireCapableBeanFactory 类实现了 ObejctFactory 接口，创建容器指定的 Bean 实例对象，同时还对创建的 Bean 实例对象进行初始化处理。其创建 Bean 实例对象的方法源码如下

```java
/**
 * Central method of this class: creates a bean instance,
 * populates the bean instance, applies post-processors, etc.
 * @see #doCreateBean
 */
@Override
protected Object createBean(String beanName, RootBeanDefinition mbd, @Nullable Object[] args)
      throws BeanCreationException {

   if (logger.isTraceEnabled()) {
      logger.trace("Creating instance of bean '" + beanName + "'");
   }
   RootBeanDefinition mbdToUse = mbd;

   // Make sure bean class is actually resolved at this point, and
   // clone the bean definition in case of a dynamically resolved Class
   // which cannot be stored in the shared merged bean definition.
   Class<?> resolvedClass = resolveBeanClass(mbd, beanName);
   if (resolvedClass != null && !mbd.hasBeanClass() && mbd.getBeanClassName() != null) {
      mbdToUse = new RootBeanDefinition(mbd);
      mbdToUse.setBeanClass(resolvedClass);
   }

   // Prepare method overrides.
   try {
      mbdToUse.prepareMethodOverrides();
   }
   catch (BeanDefinitionValidationException ex) {
      throw new BeanDefinitionStoreException(mbdToUse.getResourceDescription(),
            beanName, "Validation of method overrides failed", ex);
   }

   try {
      // Give BeanPostProcessors a chance to return a proxy instead of the target bean instance.
      Object bean = resolveBeforeInstantiation(beanName, mbdToUse);
      if (bean != null) {
         return bean;
      }
   }
   catch (Throwable ex) {
      throw new BeanCreationException(mbdToUse.getResourceDescription(), beanName,
            "BeanPostProcessor before instantiation of bean failed", ex);
   }

   try {
      Object beanInstance = doCreateBean(beanName, mbdToUse, args);
      if (logger.isTraceEnabled()) {
         logger.trace("Finished creating instance of bean '" + beanName + "'");
      }
      return beanInstance;
   }
   catch (BeanCreationException | ImplicitlyAppearedSingletonException ex) {
      // A previously detected exception with proper bean creation context already,
      // or illegal singleton state to be communicated up to DefaultSingletonBeanRegistry.
      throw ex;
   }
   catch (Throwable ex) {
      throw new BeanCreationException(
            mbdToUse.getResourceDescription(), beanName, "Unexpected exception during bean creation", ex);
   }
}
```

```java
/**
 * Actually create the specified bean. Pre-creation processing has already happened
 * at this point, e.g. checking {@code postProcessBeforeInstantiation} callbacks.
 * <p>Differentiates between default bean instantiation, use of a
 * factory method, and autowiring a constructor.
 * @param beanName the name of the bean
 * @param mbd the merged bean definition for the bean
 * @param args explicit arguments to use for constructor or factory method invocation
 * @return a new instance of the bean
 * @throws BeanCreationException if the bean could not be created
 * @see #instantiateBean
 * @see #instantiateUsingFactoryMethod
 * @see #autowireConstructor
 */
protected Object doCreateBean(final String beanName, final RootBeanDefinition mbd, final @Nullable Object[] args)
      throws BeanCreationException {

   // Instantiate the bean.
   BeanWrapper instanceWrapper = null;
   if (mbd.isSingleton()) {
      instanceWrapper = this.factoryBeanInstanceCache.remove(beanName);
   }
   if (instanceWrapper == null) {
      instanceWrapper = createBeanInstance(beanName, mbd, args);
   }
   final Object bean = instanceWrapper.getWrappedInstance();
   Class<?> beanType = instanceWrapper.getWrappedClass();
   if (beanType != NullBean.class) {
      mbd.resolvedTargetType = beanType;
   }

   // Allow post-processors to modify the merged bean definition.
   synchronized (mbd.postProcessingLock) {
      if (!mbd.postProcessed) {
         try {
            applyMergedBeanDefinitionPostProcessors(mbd, beanType, beanName);
         }
         catch (Throwable ex) {
            throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                  "Post-processing of merged bean definition failed", ex);
         }
         mbd.postProcessed = true;
      }
   }

   // Eagerly cache singletons to be able to resolve circular references
   // even when triggered by lifecycle interfaces like BeanFactoryAware.
   boolean earlySingletonExposure = (mbd.isSingleton() && this.allowCircularReferences &&
         isSingletonCurrentlyInCreation(beanName));
   if (earlySingletonExposure) {
      if (logger.isTraceEnabled()) {
         logger.trace("Eagerly caching bean '" + beanName +
               "' to allow for resolving potential circular references");
      }
      addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
   }

   // Initialize the bean instance.
   Object exposedObject = bean;
   try {
      populateBean(beanName, mbd, instanceWrapper);
      exposedObject = initializeBean(beanName, exposedObject, mbd);
   }
   catch (Throwable ex) {
      if (ex instanceof BeanCreationException && beanName.equals(((BeanCreationException) ex).getBeanName())) {
         throw (BeanCreationException) ex;
      }
      else {
         throw new BeanCreationException(
               mbd.getResourceDescription(), beanName, "Initialization of bean failed", ex);
      }
   }

   if (earlySingletonExposure) {
      Object earlySingletonReference = getSingleton(beanName, false);
      if (earlySingletonReference != null) {
         if (exposedObject == bean) {
            exposedObject = earlySingletonReference;
         }
         else if (!this.allowRawInjectionDespiteWrapping && hasDependentBean(beanName)) {
            String[] dependentBeans = getDependentBeans(beanName);
            Set<String> actualDependentBeans = new LinkedHashSet<>(dependentBeans.length);
            for (String dependentBean : dependentBeans) {
               if (!removeSingletonIfCreatedForTypeCheckOnly(dependentBean)) {
                  actualDependentBeans.add(dependentBean);
               }
            }
            if (!actualDependentBeans.isEmpty()) {
               throw new BeanCurrentlyInCreationException(beanName,
                     "Bean with name '" + beanName + "' has been injected into other beans [" +
                     StringUtils.collectionToCommaDelimitedString(actualDependentBeans) +
                     "] in its raw version as part of a circular reference, but has eventually been " +
                     "wrapped. This means that said other beans do not use the final version of the " +
                     "bean. This is often the result of over-eager type matching - consider using " +
                     "'getBeanNamesOfType' with the 'allowEagerInit' flag turned off, for example.");
            }
         }
      }
   }

   // Register bean as disposable.
   try {
      registerDisposableBeanIfNecessary(beanName, bean, mbd);
   }
   catch (BeanDefinitionValidationException ex) {
      throw new BeanCreationException(
            mbd.getResourceDescription(), beanName, "Invalid destruction signature", ex);
   }

   return exposedObject;
}
```

通过对方法源码的分析，我们看到具体的依赖注入实现在以下两个方法中：

(1).createBeanInstance：生成 Bean 所包含的 java 对象实例。
(2).populateBean ：对 Bean 属性的依赖注入进行处理。

下面继续分析这两个方法的代码实现。

##### createBeanInstance 方法创建Bean的java实例对象

在 createBeanInstance 方法中，根据指定的初始化策略，使用静态工厂、工厂方法或者容器的自动装配特性生成 java 实例对象，创建对象的源码如下：

经过对上面的代码分析，我们可以看出，对使用工厂方法和自动装配特性的 Bean 的实例化相当比较清楚，调用相应的工厂方法或者参数匹配的构造方法即可完成实例化对象的工作，

但是对于我们**最常使用的默认无参构造方法就需要使用相应的初始化策略(JDK 的反射机制或者 CGLIB)来进行初始化了**，在方法 getInstantiationStrategy().instantiate()中就具体实现类使用初始策略实例化对象。

```java
/**
 * Instantiate the given bean using its default constructor.
 * @param beanName the name of the bean
 * @param mbd the bean definition for the bean
 * @return a BeanWrapper for the new instance
 */
protected BeanWrapper instantiateBean(final String beanName, final RootBeanDefinition mbd) {
   try {
      Object beanInstance;
      final BeanFactory parent = this;
      if (System.getSecurityManager() != null) {
         beanInstance = AccessController.doPrivileged((PrivilegedAction<Object>) () ->
               getInstantiationStrategy().instantiate(mbd, beanName, parent),
               getAccessControlContext());
      }
      else {
         beanInstance = getInstantiationStrategy().instantiate(mbd, beanName, parent);
      }
      BeanWrapper bw = new BeanWrapperImpl(beanInstance);
      initBeanWrapper(bw);
      return bw;
   }
   catch (Throwable ex) {
      throw new BeanCreationException(
            mbd.getResourceDescription(), beanName, "Instantiation of bean failed", ex);
   }
}
```

##### SimpleInstantiationStrategy类使用默认的无参构造方法创建Bean实例化对象

在 使 用 默 认 的 无 参 构 造 方 法 创 建 Bean 的 实 例 化 对 象 时 ，方 法getInstantiationStrategy().instantiate()调用了 SimpleInstantiationStrategy 类中的实例化 Bean 的方法

通过上面的代码分析，我们看到了如果 Bean 有方法被覆盖了，则使用 JDK 的反射机制进行实例化，否则，使用 CGLIB 进行实例化。instantiateWithMethodInjection方法调用SimpleInstantiationStrategy的子类
CglibSubclassingInstantiationStrategy 使用 CGLIB 来进行初始化.

```java
/**
 * Create a new instance of a dynamically generated subclass implementing the
 * required lookups.
 * @param ctor constructor to use. If this is {@code null}, use the
 * no-arg constructor (no parameterization, or Setter Injection)
 * @param args arguments to use for the constructor.
 * Ignored if the {@code ctor} parameter is {@code null}.
 * @return new instance of the dynamically generated subclass
 */
public Object instantiate(@Nullable Constructor<?> ctor, Object... args) {
   Class<?> subclass = createEnhancedSubclass(this.beanDefinition);
   Object instance;
   if (ctor == null) {
      instance = BeanUtils.instantiateClass(subclass);
   }
   else {
      try {
         Constructor<?> enhancedSubclassConstructor = subclass.getConstructor(ctor.getParameterTypes());
         instance = enhancedSubclassConstructor.newInstance(args);
      }
      catch (Exception ex) {
         throw new BeanInstantiationException(this.beanDefinition.getBeanClass(),
               "Failed to invoke constructor for CGLIB enhanced subclass [" + subclass.getName() + "]", ex);
      }
   }
   // SPR-10785: set callbacks directly on the instance instead of in the
   // enhanced class (via the Enhancer) in order to avoid memory leaks.
   Factory factory = (Factory) instance;
   factory.setCallbacks(new Callback[] {NoOp.INSTANCE,
         new LookupOverrideMethodInterceptor(this.beanDefinition, this.owner),
         new ReplaceOverrideMethodInterceptor(this.beanDefinition, this.owner)});
   return instance;
}

/**
 * Create an enhanced subclass of the bean class for the provided bean
 * definition, using CGLIB.
 */
private Class<?> createEnhancedSubclass(RootBeanDefinition beanDefinition) {
   Enhancer enhancer = new Enhancer();
   enhancer.setSuperclass(beanDefinition.getBeanClass());
   enhancer.setNamingPolicy(SpringNamingPolicy.INSTANCE);
   if (this.owner instanceof ConfigurableBeanFactory) {
      ClassLoader cl = ((ConfigurableBeanFactory) this.owner).getBeanClassLoader();
      enhancer.setStrategy(new ClassLoaderAwareGeneratorStrategy(cl));
   }
   enhancer.setCallbackFilter(new MethodOverrideCallbackFilter(beanDefinition));
   enhancer.setCallbackTypes(CALLBACK_TYPES);
   return enhancer.createClass();
}
```

CGLIB 是一个常用的字节码生成器的类库，它提供了一系列 API 实现 java 字节码的生成和转换功能。我们在学习 JDK 的动态代理时都知道，JDK 的动态代理只能针对接口，如果一个类没有实现任何接口，要对其进行动态代理只能使用 CGLIB。

##### populateBean方法对Bean属性的依赖注入

在第 3 步的分析中我们已经了解到 Bean 的依赖注入分为以下两个过程：

(1).createBeanInstance：生成 Bean 所包含的 Java 对象实例。
(2).populateBean：对 Bean 属性的依赖注入进行处理。

上面我们已经分析了容器初始化生成 Bean 所包含的 Java 实例对象的过程，现在我们继续分析生成对象后，Spring IOC 容器是如何将 Bean 的属性依赖关系注入 Bean 实例对象中并设置好的，属性依赖注入的代码如下：

```java
//将 Bean 属性设置到生成的实例对象上
protected void populateBean(String beanName, RootBeanDefinition mbd, @Nullable BeanWrapper bw) {
if (bw == null) {
if (mbd.hasPropertyValues()) {
throw new BeanCreationException(
mbd.getResourceDescription(), beanName, "Cannot apply property values to null instance");
}
else {
// Skip property population phase for null instance.
return;
}
}
boolean continueWithPropertyPopulation = true;
if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
for (BeanPostProcessor bp : getBeanPostProcessors()) {
if (bp instanceof InstantiationAwareBeanPostProcessor) {
InstantiationAwareBeanPostProcessor ibp = (InstantiationAwareBeanPostProcessor) bp;
if (!ibp.postProcessAfterInstantiation(bw.getWrappedInstance(), beanName)) {
continueWithPropertyPopulation = false;
break;
}
}
}
}
if (!continueWithPropertyPopulation) {
return;
}
//获取容器在解析 Bean 定义资源时为 BeanDefiniton 中设置的属性值
PropertyValues pvs = (mbd.hasPropertyValues() ? mbd.getPropertyValues() : null);
//对依赖注入处理，首先处理 autowiring 自动装配的依赖注入
if (mbd.getResolvedAutowireMode() == RootBeanDefinition.AUTOWIRE_BY_NAME ||
mbd.getResolvedAutowireMode() == RootBeanDefinition.AUTOWIRE_BY_TYPE) {
MutablePropertyValues newPvs = new MutablePropertyValues(pvs);
//根据 Bean 名称进行 autowiring 自动装配处理
if (mbd.getResolvedAutowireMode() == RootBeanDefinition.AUTOWIRE_BY_NAME) {
autowireByName(beanName, mbd, bw, newPvs);
}
//根据 Bean 类型进行 autowiring 自动装配处理
if (mbd.getResolvedAutowireMode() == RootBeanDefinition.AUTOWIRE_BY_TYPE) {
autowireByType(beanName, mbd, bw, newPvs);
}
pvs = newPvs;
}
//对非 autowiring 的属性进行依赖注入处理
...
}
```

```java
//解析并注入依赖属性的过程
protected void applyPropertyValues(String beanName, BeanDefinition mbd, BeanWrapper bw, PropertyValues pvs) {
if (pvs.isEmpty()) {
return;
}
//封装属性值
MutablePropertyValues mpvs = null;
List<PropertyValue> original;
if (System.getSecurityManager() != null) {
if (bw instanceof BeanWrapperImpl) {
//设置安全上下文，JDK 安全机制
((BeanWrapperImpl) bw).setSecurityContext(getAccessControlContext());
}
}
if (pvs instanceof MutablePropertyValues) {
mpvs = (MutablePropertyValues) pvs;
//属性值已经转换
if (mpvs.isConverted()) {
try {
//为实例化对象设置属性值
bw.setPropertyValues(mpvs);
return;
}
catch (BeansException ex) {
throw new BeanCreationException(
mbd.getResourceDescription(), beanName, "Error setting property values", ex);
}
}
//获取属性值对象的原始类型值
original = mpvs.getPropertyValueList();
}
else {
original = Arrays.asList(pvs.getPropertyValues());
}
//获取用户自定义的类型转换
TypeConverter converter = getCustomTypeConverter();
if (converter == null) {
converter = bw;
}
//创建一个 Bean 定义属性值解析器，将 Bean 定义中的属性值解析为 Bean 实例对象的实际值
BeanDefinitionValueResolver valueResolver = new BeanDefinitionValueResolver(this, beanName, mbd, converter);
//为属性的解析值创建一个拷贝，将拷贝的数据注入到实例对象中
List<PropertyValue> deepCopy = new ArrayList<>(original.size());
boolean resolveNecessary = false;
for (PropertyValue pv : original) {
//属性值不需要转换
if (pv.isConverted()) {
deepCopy.add(pv);
}
//属性值需要转换
else {
String propertyName = pv.getName();
//原始的属性值，即转换之前的属性值
Object originalValue = pv.getValue();
//转换属性值，例如将引用转换为 IOC 容器中实例化对象引用
Object resolvedValue = valueResolver.resolveValueIfNecessary(pv, originalValue);
//转换之后的属性值
Object convertedValue = resolvedValue;
//属性值是否可以转换
boolean convertible = bw.isWritableProperty(propertyName) &&
!PropertyAccessorUtils.isNestedOrIndexedProperty(propertyName);
if (convertible) {
//使用用户自定义的类型转换器转换属性值
convertedValue = convertForProperty(resolvedValue, propertyName, bw, converter);
}
//存储转换后的属性值，避免每次属性注入时的转换工作
if (resolvedValue == originalValue) {
if (convertible) {
//设置属性转换之后的值
pv.setConvertedValue(convertedValue);
}
deepCopy.add(pv);
}
//属性是可转换的，且属性原始值是字符串类型，且属性的原始类型值不是
//动态生成的字符串，且属性的原始值不是集合或者数组类型
else if (convertible && originalValue instanceof TypedStringValue &&
!((TypedStringValue) originalValue).isDynamic() &&
!(convertedValue instanceof Collection || ObjectUtils.isArray(convertedValue))) {
pv.setConvertedValue(convertedValue);
//重新封装属性的值
deepCopy.add(pv);
}
else {
resolveNecessary = true;
deepCopy.add(new PropertyValue(pv, convertedValue));
}
}
}
if (mpvs != null && !resolveNecessary) {
//标记属性值已经转换过
mpvs.setConverted();
}
//进行属性依赖注入
try {
bw.setPropertyValues(new MutablePropertyValues(deepCopy));
}
catch (BeansException ex) {
throw new BeanCreationException(
mbd.getResourceDescription(), beanName, "Error setting property values", ex);
}
}
```

分析上述代码，我们可以看出，对属性的注入过程分以下两种情况：

(1).属性值类型不需要转换时，不需要解析属性值，直接准备进行依赖注入。
(2).属性值需要进行类型转换时，如对其他对象的引用等，首先需要解析属性值，然后对解析后的属性值进行依赖注入。

对属性值的解析是在 BeanDefinitionValueResolver 类中的 resolveValueIfNecessary 方法中进行的，对属性值的依赖注入是通过 bw.setPropertyValues 方法实现的，在分析属性值的依赖注入之前，我们先分析一下对属性值的解析过程。

###### BeanDefinitionValueResolver解析属性值

当容器在对属性进行依赖注入时，如果发现属性值需要进行类型转换，如属性值是容器中另一个 Bean实例对象的引用，则容器首先需要根据属性值解析出所引用的对象，然后才能将该引用对象注入到目标实例对象的属性上去，对属性进行解析的由 resolveValueIfNecessary 方法实现，其源码如下

```java
//解析属性值，对注入类型进行转换
@Nullable
public Object resolveValueIfNecessary(Object argName, @Nullable Object value) {
//对引用类型的属性进行解析
if (value instanceof RuntimeBeanReference) {
RuntimeBeanReference ref = (RuntimeBeanReference) value;
//调用引用类型属性的解析方法
return resolveReference(argName, ref);
}
//对属性值是引用容器中另一个 Bean 名称的解析
else if (value instanceof RuntimeBeanNameReference) {
String refName = ((RuntimeBeanNameReference) value).getBeanName();
refName = String.valueOf(doEvaluate(refName));
//从容器中获取指定名称的 Bean
if (!this.beanFactory.containsBean(refName)) {
throw new BeanDefinitionStoreException(
"Invalid bean name '" + refName + "' in bean reference for " + argName);
}
return refName;
}
//对 Bean 类型属性的解析，主要是 Bean 中的内部类
else if (value instanceof BeanDefinitionHolder) {
BeanDefinitionHolder bdHolder = (BeanDefinitionHolder) value;
return resolveInnerBean(argName, bdHolder.getBeanName(), bdHolder.getBeanDefinition());
}
else if (value instanceof BeanDefinition) {
BeanDefinition bd = (BeanDefinition) value;
String innerBeanName = "(inner bean)" + BeanFactoryUtils.GENERATED_BEAN_NAME_SEPARATOR +
ObjectUtils.getIdentityHexString(bd);
return resolveInnerBean(argName, innerBeanName, bd);
}
//对集合数组类型的属性解析
else if (value instanceof ManagedArray) {
ManagedArray array = (ManagedArray) value;
//获取数组的类型
Class<?> elementType = array.resolvedElementType;
if (elementType == null) {
//获取数组元素的类型
String elementTypeName = array.getElementTypeName();
if (StringUtils.hasText(elementTypeName)) {
try {
//使用反射机制创建指定类型的对象
elementType = ClassUtils.forName(elementTypeName, this.beanFactory.getBeanClassLoader());
array.resolvedElementType = elementType;
}
catch (Throwable ex) {
throw new BeanCreationException(
this.beanDefinition.getResourceDescription(), this.beanName,
"Error resolving array type for " + argName, ex);
}
}
//没有获取到数组的类型，也没有获取到数组元素的类型
//则直接设置数组的类型为 Object
else {
elementType = Object.class;
}
}
//创建指定类型的数组
return resolveManagedArray(argName, (List<?>) value, elementType);
}
//解析 list 类型的属性值
else if (value instanceof ManagedList) {
return resolveManagedList(argName, (List<?>) value);
}
//解析 set 类型的属性值
else if (value instanceof ManagedSet) {
return resolveManagedSet(argName, (Set<?>) value);
}
//解析 map 类型的属性值
else if (value instanceof ManagedMap) {
return resolveManagedMap(argName, (Map<?, ?>) value);
}
//解析 props 类型的属性值，props 其实就是 key 和 value 均为字符串的 map
else if (value instanceof ManagedProperties) {
Properties original = (Properties) value;
//创建一个拷贝，用于作为解析后的返回值
Properties copy = new Properties();
original.forEach((propKey, propValue) -> {
if (propKey instanceof TypedStringValue) {
propKey = evaluate((TypedStringValue) propKey);
}
if (propValue instanceof TypedStringValue) {
propValue = evaluate((TypedStringValue) propValue);
}
if (propKey == null || propValue == null) {
throw new BeanCreationException(
this.beanDefinition.getResourceDescription(), this.beanName,
"Error converting Properties key/value pair for " + argName + ": resolved to null");
}
copy.put(propKey, propValue);
});
return copy;
}
//解析字符串类型的属性值
else if (value instanceof TypedStringValue) {
TypedStringValue typedStringValue = (TypedStringValue) value;
Object valueObject = evaluate(typedStringValue);
try {
//获取属性的目标类型
Class<?> resolvedTargetType = resolveTargetType(typedStringValue);
if (resolvedTargetType != null) {
//对目标类型的属性进行解析，递归调用
return this.typeConverter.convertIfNecessary(valueObject, resolvedTargetType);
}
//没有获取到属性的目标对象，则按 Object 类型返回
else {
return valueObject;
}
}
catch (Throwable ex) {
throw new BeanCreationException(
this.beanDefinition.getResourceDescription(), this.beanName,
"Error converting typed String value for " + argName, ex);
}
}
else if (value instanceof NullBean) {
return null;
}
else {
return evaluate(value);
}
}

//解析引用类型的属性值
@Nullable
private Object resolveReference(Object argName, RuntimeBeanReference ref) {
try {
Object bean;
//获取引用的 Bean 名称
String refName = ref.getBeanName();
refName = String.valueOf(doEvaluate(refName));
//如果引用的对象在父类容器中，则从父类容器中获取指定的引用对象
if (ref.isToParent()) {
if (this.beanFactory.getParentBeanFactory() == null) {
throw new BeanCreationException(
this.beanDefinition.getResourceDescription(), this.beanName,
"Can't resolve reference to bean '" + refName +
"' in parent factory: no parent factory available");
}
bean = this.beanFactory.getParentBeanFactory().getBean(refName);
}
//从当前的容器中获取指定的引用 Bean 对象，如果指定的 Bean 没有被实例化
//则会递归触发引用 Bean 的初始化和依赖注入
else {
bean = this.beanFactory.getBean(refName);
//将当前实例化对象的依赖引用对象
this.beanFactory.registerDependentBean(refName, this.beanName);
}
if (bean instanceof NullBean) {
bean = null;
}
return bean;
}
catch (BeansException ex) {
throw new BeanCreationException(
this.beanDefinition.getResourceDescription(), this.beanName,
"Cannot resolve reference to bean '" + ref.getBeanName() + "' while setting " + argName, ex);
}
}
//解析 array 类型的属性
private Object resolveManagedArray(Object argName, List<?> ml, Class<?> elementType) {
//创建一个指定类型的数组，用于存放和返回解析后的数组
Object resolved = Array.newInstance(elementType, ml.size());
for (int i = 0; i < ml.size(); i++) {
//递归解析 array 的每一个元素，并将解析后的值设置到 resolved 数组中，索引为 i
Array.set(resolved, i,
resolveValueIfNecessary(new KeyedArgName(argName, i), ml.get(i)));
}
return resolved;
}
```

通过上面的代码分析，我们明白了 Spring 是如何将引用类型，内部类以及集合类型等属性进行解析的，属性值解析完成后就可以进行依赖注入了，依赖注入的过程就是 Bean 对象实例设置到它所依赖的 Bean对象属性上去，在第 6 步中我们已经说过，依赖注入是通过 bw.setPropertyValues 方法实现的，该方法也使用了委托模式，在 BeanWrapper 接口中至少定义了方法声明，依赖注入的具体实现交由其实现类 BeanWrapperImpl 来完成，下面我们就分析依 BeanWrapperImpl 中赖注入相关的源码。

##### BeanWrapperImpl对Bean属性的依赖注入

BeanWrapperImpl 类主要是对容器中完成初始化的 Bean 实例对象进行属性的依赖注入，即把 Bean 对象设置到它所依赖的另一个 Bean 的属性中去。然而，BeanWrapperImpl 中的注入方法实际上由AbstractNestablePropertyAccessor 来实现的，其相关源码如下：

```java
//实现属性依赖注入功能
protected void setPropertyValue(PropertyTokenHolder tokens, PropertyValue pv) throws BeansException {
if (tokens.keys != null) {
processKeyedProperty(tokens, pv);
}
else {
processLocalProperty(tokens, pv);
}
}
//实现属性依赖注入功能
@SuppressWarnings("unchecked")
private void processKeyedProperty(PropertyTokenHolder tokens, PropertyValue pv) {
//调用属性的 getter(readerMethod)方法，获取属性的值
Object propValue = getPropertyHoldingValue(tokens);
PropertyHandler ph = getLocalPropertyHandler(tokens.actualName);
if (ph == null) {
throw new InvalidPropertyException(
getRootClass(), this.nestedPath + tokens.actualName, "No property handler found");
}
Assert.state(tokens.keys != null, "No token keys");
String lastKey = tokens.keys[tokens.keys.length - 1];
//注入 array 类型的属性值
if (propValue.getClass().isArray()) {
Class<?> requiredType = propValue.getClass().getComponentType();
int arrayIndex = Integer.parseInt(lastKey);
Object oldValue = null;
try {
if (isExtractOldValueForEditor() && arrayIndex < Array.getLength(propValue)) {
oldValue = Array.get(propValue, arrayIndex);
}
Object convertedValue = convertIfNecessary(tokens.canonicalName, oldValue, pv.getValue(),
requiredType, ph.nested(tokens.keys.length));
//获取集合类型属性的长度
int length = Array.getLength(propValue);
if (arrayIndex >= length && arrayIndex < this.autoGrowCollectionLimit) {
Class<?> componentType = propValue.getClass().getComponentType();
Object newArray = Array.newInstance(componentType, arrayIndex + 1);
System.arraycopy(propValue, 0, newArray, 0, length);
setPropertyValue(tokens.actualName, newArray);
//调用属性的 getter(readerMethod)方法，获取属性的值
propValue = getPropertyValue(tokens.actualName);
}
//将属性的值赋值给数组中的元素
Array.set(propValue, arrayIndex, convertedValue);
}
catch (IndexOutOfBoundsException ex) {
throw new InvalidPropertyException(getRootClass(), this.nestedPath + tokens.canonicalName,
"Invalid array index in property path '" + tokens.canonicalName + "'", ex);
}
}
//注入 list 类型的属性值
else if (propValue instanceof List) {
//获取 list 集合的类型
Class<?> requiredType = ph.getCollectionType(tokens.keys.length);
List<Object> list = (List<Object>) propValue;
//获取 list 集合的 size
int index = Integer.parseInt(lastKey);
Object oldValue = null;
if (isExtractOldValueForEditor() && index < list.size()) {
oldValue = list.get(index);
}
//获取 list 解析后的属性值
Object convertedValue = convertIfNecessary(tokens.canonicalName, oldValue, pv.getValue(),
requiredType, ph.nested(tokens.keys.length));
int size = list.size();
//如果 list 的长度大于属性值的长度，则多余的元素赋值为 null
if (index >= size && index < this.autoGrowCollectionLimit) {
for (int i = size; i < index; i++) {
try {
list.add(null);
}
catch (NullPointerException ex) {
throw new InvalidPropertyException(getRootClass(), this.nestedPath + tokens.canonicalName,
"Cannot set element with index " + index + " in List of size " +
size + ", accessed using property path '" + tokens.canonicalName +
"': List does not support filling up gaps with null elements");
}
}
list.add(convertedValue);
}
else {
try {
//将值添加到 list 中
list.set(index, convertedValue);
}
catch (IndexOutOfBoundsException ex) {
throw new InvalidPropertyException(getRootClass(), this.nestedPath + tokens.canonicalName,
"Invalid list index in property path '" + tokens.canonicalName + "'", ex);
}
}
}
//注入 map 类型的属性值
else if (propValue instanceof Map) {
//获取 map 集合 key 的类型
Class<?> mapKeyType = ph.getMapKeyType(tokens.keys.length);
//获取 map 集合 value 的类型
Class<?> mapValueType = ph.getMapValueType(tokens.keys.length);
Map<Object, Object> map = (Map<Object, Object>) propValue;
TypeDescriptor typeDescriptor = TypeDescriptor.valueOf(mapKeyType);
//解析 map 类型属性 key 值
Object convertedMapKey = convertIfNecessary(null, null, lastKey, mapKeyType, typeDescriptor);
Object oldValue = null;
if (isExtractOldValueForEditor()) {
oldValue = map.get(convertedMapKey);
}
//解析 map 类型属性 value 值
Object convertedMapValue = convertIfNecessary(tokens.canonicalName, oldValue, pv.getValue(),
mapValueType, ph.nested(tokens.keys.length));
//将解析后的 key 和 value 值赋值给 map 集合属性
map.put(convertedMapKey, convertedMapValue);
}
else {
throw new InvalidPropertyException(getRootClass(), this.nestedPath + tokens.canonicalName,
"Property referenced in indexed property path '" + tokens.canonicalName +
"' is neither an array nor a List nor a Map; returned value was [" + propValue + "]");
}
}
private Object getPropertyHoldingValue(PropertyTokenHolder tokens) {
Assert.state(tokens.keys != null, "No token keys");
PropertyTokenHolder getterTokens = new PropertyTokenHolder(tokens.actualName);
getterTokens.canonicalName = tokens.canonicalName;
getterTokens.keys = new String[tokens.keys.length - 1];
System.arraycopy(tokens.keys, 0, getterTokens.keys, 0, tokens.keys.length - 1);
Object propValue;
try {
//获取属性值
propValue = getPropertyValue(getterTokens);
}
catch (NotReadablePropertyException ex) {
throw new NotWritablePropertyException(getRootClass(), this.nestedPath + tokens.canonicalName,
"Cannot access indexed value in property referenced " +
"in indexed property path '" + tokens.canonicalName + "'", ex);
}
if (propValue == null) {
if (isAutoGrowNestedPaths()) {
int lastKeyIndex = tokens.canonicalName.lastIndexOf('[');
getterTokens.canonicalName = tokens.canonicalName.substring(0, lastKeyIndex);
propValue = setDefaultValue(getterTokens);
}
else {
throw new NullValueInNestedPathException(getRootClass(), this.nestedPath + tokens.canonicalName,
"Cannot access indexed value in property referenced " +
"in indexed property path '" + tokens.canonicalName + "': returned null");
}
}
return propValue;
}
```

通过对上面注入依赖代码的分析，我们已经明白了 Spring IOC 容器是如何将属性的值注入到 Bean 实例对象中去的：

(1).对于集合类型的属性，将其属性值解析为目标类型的集合后直接赋值给属性。

(2).对于非集合类型的属性，大量使用了 JDK 的反射和内省机制，通过属性的 getter 方法(readerMethod)获取指定属性注入以前的值，同时调用属性的 setter 方法(writer Method)为属性设置注入后的值。看到这里相信很多人都明白了 Spring 的 setter 注入原理。

至此 Spring IOC 容器对 Bean 定义资源文件的定位，载入、解析和依赖注入已经全部分析完毕，现在Spring IOC 容器中管理了一系列靠依赖关系联系起来的 Bean，程序不需要应用自己手动创建所需的对象，Spring IOC 容器会在我们使用的时候自动为我们创建，并且为我们注入好相关的依赖，这就是Spring 核心功能的控制反转和依赖注入的相关功能。

### 基于Annotation的依赖注入

从 Spring2.0 以后的版本中，Spring 也引入了基于注解(Annotation)方式的配置，注解(Annotation)是 JDK1.5 中引入的一个新特性，用于简化 Bean 的配置，某些场合可以取代 XML 配置文件。

开发人员对注解(Annotation)的态度也是萝卜青菜各有所爱，个人认为注解可以大大简化配置，提高开发速度，同时也不能完全取代 XML 配置方式，XML 方式更加灵活，并且发展的相对成熟，这种配置方式为大多数 Spring 开发者熟悉；注解方式使用起来非常简洁，但是尚处于发展阶段，XML 配置文件和注解(Annotation)可以相互配合使用。

Spring IOC 容器对于类级别的注解和类内部的注解分以下两种处理策略：

(1).类级别的注解：如@Component、@Repository、@Controller、@Service 以及 JavaEE6 的@ManagedBean 和@Named 注解，都是添加在类上面的类级别注解，Spring 容器根据注解的过滤规则扫描读取注解 Bean 定义类，并将其注册到 Spring IOC 容器中。

(2).类内部的注解：如@Autowire、@Value、@Resource 以及 EJB 和 WebService 相关的注解等，都是添加在类内部的字段或者方法上的类内部注解，SpringIOC 容器通过 Bean 后置注解处理器解析 Bean内部的注解。

下面将根据这两种处理策略，分别分析 Spring 处理注解相关的源码。

#### AnnotationConfigApplicationContext对注解Bean初始化

Spring 中 ， 管 理 注 解 Bean 定 义 的 容 器 有 两 个 ： AnnotationConfigApplicationContext 和
AnnotationConfigWebApplicationContex。这两个类是专门处理 Spring 注解方式配置的容器，直接依赖于注解作为容器配置信息来源的 IOC 容器。

AnnotationConfigWebApplicationContext 是AnnotationConfigApplicationContext 的 web 版本，两者的用法以及对注解的处理方式几乎没有什么差别。

现在来看看 AnnotationConfigApplicationContext 的源码

```java
public class AnnotationConfigApplicationContext extends GenericApplicationContext implements
AnnotationConfigRegistry {
//保存一个读取注解的 Bean 定义读取器，并将其设置到容器中
private final AnnotatedBeanDefinitionReader reader;
//保存一个扫描指定类路径中注解 Bean 定义的扫描器，并将其设置到容器中
private final ClassPathBeanDefinitionScanner scanner;
//默认构造函数，初始化一个空容器，容器不包含任何 Bean 信息，需要在稍后通过调用其 register()
//方法注册配置类，并调用 refresh()方法刷新容器，触发容器对注解 Bean 的载入、解析和注册过程
public AnnotationConfigApplicationContext() {
this.reader = new AnnotatedBeanDefinitionReader(this);
this.scanner = new ClassPathBeanDefinitionScanner(this);
}
public AnnotationConfigApplicationContext(DefaultListableBeanFactory beanFactory) {
super(beanFactory);
this.reader = new AnnotatedBeanDefinitionReader(this);
this.scanner = new ClassPathBeanDefinitionScanner(this);
}
//最常用的构造函数，通过将涉及到的配置类传递给该构造函数，以实现将相应配置类中的 Bean 自动注册到容器中
public AnnotationConfigApplicationContext(Class<?>... annotatedClasses) {
this();
register(annotatedClasses);
refresh();
}
//该构造函数会自动扫描以给定的包及其子包下的所有类，并自动识别所有的 Spring Bean，将其注册到容器中
public AnnotationConfigApplicationContext(String... basePackages) {
this();
scan(basePackages);
refresh();
}
@Override
public void setEnvironment(ConfigurableEnvironment environment) {
super.setEnvironment(environment);
this.reader.setEnvironment(environment);
this.scanner.setEnvironment(environment);
}
//为容器的注解 Bean 读取器和注解 Bean 扫描器设置 Bean 名称产生器
public void setBeanNameGenerator(BeanNameGenerator beanNameGenerator) {
this.reader.setBeanNameGenerator(beanNameGenerator);
this.scanner.setBeanNameGenerator(beanNameGenerator);
getBeanFactory().registerSingleton(
AnnotationConfigUtils.CONFIGURATION_BEAN_NAME_GENERATOR, beanNameGenerator);
}
//为容器的注解 Bean 读取器和注解 Bean 扫描器设置作用范围元信息解析器
public void setScopeMetadataResolver(ScopeMetadataResolver scopeMetadataResolver) {
this.reader.setScopeMetadataResolver(scopeMetadataResolver);
this.scanner.setScopeMetadataResolver(scopeMetadataResolver);
}
//为容器注册一个要被处理的注解 Bean，新注册的 Bean，必须手动调用容器的
//refresh()方法刷新容器，触发容器对新注册的 Bean 的处理
public void register(Class<?>... annotatedClasses) {
Assert.notEmpty(annotatedClasses, "At least one annotated class must be specified");
this.reader.register(annotatedClasses);
}
//扫描指定包路径及其子包下的注解类，为了使新添加的类被处理，必须手动调用
//refresh()方法刷新容器
public void scan(String... basePackages) {
Assert.notEmpty(basePackages, "At least one base package must be specified");
this.scanner.scan(basePackages);
}
...
}
```

通过对 AnnotationConfigApplicationContext 的源码分析，我们了解到 Spring 对注解的处理分为两种方式：

(1).直接将注解 Bean 注册到容器中：

可以在初始化容器时注册；也可以在容器创建之后手动调用注册方法向容器注册，然后通过手动刷新容器，使得容器对注册的注解 Bean 进行处理。

(2).通过扫描指定的包及其子包下的所有类：

在初始化注解容器时指定要自动扫描的路径，如果容器创建以后向给定路径动态添加了注解 Bean，则需要手动调用容器扫描的方法，然后手动刷新容器，使得容器对所注册的 Bean 进行处理。

接下来，将会对两种处理方式详细分析其实现过程。

#### AnnotationConfigApplicationContext注册注解Bean

当创建注解处理容器时，如果传入的初始参数是具体的注解 Bean 定义类时，注解容器读取并注册。

(1).AnnotationConfigApplicationContext 通 过 调 用 注 解 Bean 定 义 读 取 器

AnnotatedBeanDefinitionReader 的 register 方法向容器注册指定的注解 Bean，注解 Bean 定义读取器向容器注册注解 Bean 的源码如下：

```java
//注册多个注解 Bean 定义类
public void register(Class<?>... annotatedClasses) {
for (Class<?> annotatedClass : annotatedClasses) {
registerBean(annotatedClass);
}
}
//注册一个注解 Bean 定义类
public void registerBean(Class<?> annotatedClass) {
doRegisterBean(annotatedClass, null, null, null);
}
public <T> void registerBean(Class<T> annotatedClass, @Nullable Supplier<T> instanceSupplier) {
doRegisterBean(annotatedClass, instanceSupplier, null, null);
}
public <T> void registerBean(Class<T> annotatedClass, String name, @Nullable Supplier<T> instanceSupplier) {
doRegisterBean(annotatedClass, instanceSupplier, name, null);
}
//Bean 定义读取器注册注解 Bean 定义的入口方法
@SuppressWarnings("unchecked")
public void registerBean(Class<?> annotatedClass, Class<? extends Annotation>... qualifiers) {
doRegisterBean(annotatedClass, null, null, qualifiers);
}
//Bean 定义读取器向容器注册注解 Bean 定义类
@SuppressWarnings("unchecked")
public void registerBean(Class<?> annotatedClass, String name, Class<? extends Annotation>... qualifiers) {
doRegisterBean(annotatedClass, null, name, qualifiers);
}
//Bean 定义读取器向容器注册注解 Bean 定义类
<T> void doRegisterBean(Class<T> annotatedClass, @Nullable Supplier<T> instanceSupplier, @Nullable String name,

@Nullable Class<? extends Annotation>[] qualifiers, BeanDefinitionCustomizer... definitionCustomizers) {
//根据指定的注解 Bean 定义类，创建 Spring 容器中对注解 Bean 的封装的数据结构
AnnotatedGenericBeanDefinition abd = new AnnotatedGenericBeanDefinition(annotatedClass);
if (this.conditionEvaluator.shouldSkip(abd.getMetadata())) {
return;
}
abd.setInstanceSupplier(instanceSupplier);
//解析注解 Bean 定义的作用域，若@Scope("prototype")，则 Bean 为原型类型；
//若@Scope("singleton")，则 Bean 为单态类型
ScopeMetadata scopeMetadata = this.scopeMetadataResolver.resolveScopeMetadata(abd);
//为注解 Bean 定义设置作用域
abd.setScope(scopeMetadata.getScopeName());
//为注解 Bean 定义生成 Bean 名称
String beanName = (name != null ? name : this.beanNameGenerator.generateBeanName(abd, this.registry));
//处理注解 Bean 定义中的通用注解
AnnotationConfigUtils.processCommonDefinitionAnnotations(abd);
//如果在向容器注册注解 Bean 定义时，使用了额外的限定符注解，则解析限定符注解。
//主要是配置的关于 autowiring 自动依赖注入装配的限定条件，即@Qualifier 注解
//Spring 自动依赖注入装配默认是按类型装配，如果使用@Qualifier 则按名称
if (qualifiers != null) {
for (Class<? extends Annotation> qualifier : qualifiers) {
//如果配置了@Primary 注解，设置该 Bean 为 autowiring 自动依赖注入装//配时的首选
if (Primary.class == qualifier) {
abd.setPrimary(true);
}
//如果配置了@Lazy 注解，则设置该 Bean 为非延迟初始化，如果没有配置，
//则该 Bean 为预实例化
else if (Lazy.class == qualifier) {
abd.setLazyInit(true);
}
//如果使用了除@Primary 和@Lazy 以外的其他注解，则为该 Bean 添加一
//个 autowiring 自动依赖注入装配限定符，该 Bean 在进 autowiring
//自动依赖注入装配时，根据名称装配限定符指定的 Bean
else {
abd.addQualifier(new AutowireCandidateQualifier(qualifier));
}
}
}
for (BeanDefinitionCustomizer customizer : definitionCustomizers) {
customizer.customize(abd);
}

//创建一个指定 Bean 名称的 Bean 定义对象，封装注解 Bean 定义类数据
BeanDefinitionHolder definitionHolder = new BeanDefinitionHolder(abd, beanName);
//根据注解 Bean 定义类中配置的作用域，创建相应的代理对象
definitionHolder = AnnotationConfigUtils.applyScopedProxyMode(scopeMetadata, definitionHolder,
this.registry);
//向 IOC 容器注册注解 Bean 类定义对象
BeanDefinitionReaderUtils.registerBeanDefinition(definitionHolder, this.registry);
}
```

从上面的源码我们可以看出，注册注解 Bean 定义类的基本步骤：

a，需要使用注解元数据解析器解析注解 Bean 中关于作用域的配置。
b，使用 AnnotationConfigUtils 的 processCommonDefinitionAnnotations 方法处理注解 Bean定义类中通用的注解。
c，使用 AnnotationConfigUtils 的 applyScopedProxyMode 方法创建对于作用域的代理对象。
d，通过 BeanDefinitionReaderUtils 向容器注册 Bean。

##### AnnotationScopeMetadataResolver 解析作用域元数据

AnnotationScopeMetadataResolver 通过 resolveScopeMetadata方法解析注解Bean定义类的作用域元信息，即判断注册的Bean是原生类型(prototype)还是单态(singleton)类型，其源码如下：

```java
//解析注解 Bean 定义类中的作用域元信息
@Override
public ScopeMetadata resolveScopeMetadata(BeanDefinition definition) {
ScopeMetadata metadata = new ScopeMetadata();
if (definition instanceof AnnotatedBeanDefinition) {
AnnotatedBeanDefinition annDef = (AnnotatedBeanDefinition) definition;
//从注解 Bean 定义类的属性中查找属性为”Scope”的值，即@Scope 注解的值
//annDef.getMetadata().getAnnotationAttributes 方法将 Bean
//中所有的注解和注解的值存放在一个 map 集合中
AnnotationAttributes attributes = AnnotationConfigUtils.attributesFor(
annDef.getMetadata(), this.scopeAnnotationType);
//将获取到的@Scope 注解的值设置到要返回的对象中
if (attributes != null) {
metadata.setScopeName(attributes.getString("value"));
//获取@Scope 注解中的 proxyMode 属性值，在创建代理对象时会用到
ScopedProxyMode proxyMode = attributes.getEnum("proxyMode");
//如果@Scope 的 proxyMode 属性为 DEFAULT 或者 NO
if (proxyMode == ScopedProxyMode.DEFAULT) {
//设置 proxyMode 为 NO
proxyMode = this.defaultProxyMode;
}
//为返回的元数据设置 proxyMode
metadata.setScopedProxyMode(proxyMode);
}
}
//返回解析的作用域元信息对象
return metadata;
}
```

上述代码中的 annDef.getMetadata().getAnnotationAttributes 方法就是获取对象中指定类型的注解的值。

##### AnnotationConfigUtils处理注解Bean定义类中的通用注解

AnnotationConfigUtils 类的 processCommonDefinitionAnnotations 在向容器注册 Bean 之前，首先对注解 Bean 定义类中的通用 Spring 注解进行处理，源码如下：

```java
//处理 Bean 定义中通用注解
static void processCommonDefinitionAnnotations(AnnotatedBeanDefinition abd, AnnotatedTypeMetadata metadata) {
AnnotationAttributes lazy = attributesFor(metadata, Lazy.class);
//如果 Bean 定义中有@Lazy 注解，则将该 Bean 预实例化属性设置为@lazy 注解的值
if (lazy != null) {
abd.setLazyInit(lazy.getBoolean("value"));
}
else if (abd.getMetadata() != metadata) {
lazy = attributesFor(abd.getMetadata(), Lazy.class);
if (lazy != null) {
abd.setLazyInit(lazy.getBoolean("value"));
}
}
//如果 Bean 定义中有@Primary 注解，则为该 Bean 设置为 autowiring 自动依赖注入装配的首选对象
if (metadata.isAnnotated(Primary.class.getName())) {
abd.setPrimary(true);
}
//如果 Bean 定义中有@ DependsOn 注解，则为该 Bean 设置所依赖的 Bean 名称，
//容器将确保在实例化该 Bean 之前首先实例化所依赖的 Bean
AnnotationAttributes dependsOn = attributesFor(metadata, DependsOn.class);
if (dependsOn != null) {
abd.setDependsOn(dependsOn.getStringArray("value"));
}
if (abd instanceof AbstractBeanDefinition) {
AbstractBeanDefinition absBd = (AbstractBeanDefinition) abd;
AnnotationAttributes role = attributesFor(metadata, Role.class);
if (role != null) {
absBd.setRole(role.getNumber("value").intValue());
}
AnnotationAttributes description = attributesFor(metadata, Description.class);
if (description != null) {
absBd.setDescription(description.getString("value"));
}
}
}
```

AnnotationConfigUtils 根据注解 Bean 定义类中配置的作用域为其应用相应的代理策略：

AnnotationConfigUtils 类的 applyScopedProxyMode 方法根据注解 Bean 定义类中配置的作用域@Scope 注解的值，为 Bean 定义应用相应的代理模式，主要是在 Spring 面向切面编程(AOP)中使用。源码如下

```java
//根据作用域为 Bean 应用引用的代码模式
static BeanDefinitionHolder applyScopedProxyMode(
ScopeMetadata metadata, BeanDefinitionHolder definition, BeanDefinitionRegistry registry) {
//获取注解 Bean 定义类中@Scope 注解的 proxyMode 属性值
ScopedProxyMode scopedProxyMode = metadata.getScopedProxyMode();
//如果配置的@Scope 注解的 proxyMode 属性值为 NO，则不应用代理模式
if (scopedProxyMode.equals(ScopedProxyMode.NO)) {
return definition;
}
//获取配置的@Scope 注解的 proxyMode 属性值，如果为 TARGET_CLASS
//则返回 true，如果为 INTERFACES，则返回 false
boolean proxyTargetClass = scopedProxyMode.equals(ScopedProxyMode.TARGET_CLASS);
//为注册的 Bean 创建相应模式的代理对象
return ScopedProxyCreator.createScopedProxy(definition, registry, proxyTargetClass);
}
```

这段为 Bean 引用创建相应模式的代理，这里不做深入的分析。

#### AnnotationConfigApplicationContext扫描指定包及其子包下的注解Bean

当创建注解处理容器时，如果传入的初始参数是注解 Bean 定义类所在的包时，注解容器将扫描给定的包及其子包，将扫描到的注解 Bean 定义载入并注册。

(1).ClassPathBeanDefinitionScanner 扫描给定的包及其子包：AnnotationConfigApplicationContext 通 过 调 用 类 路 径 Bean 定 义 扫 描 器ClassPathBeanDefinitionScanner 扫描给定包及其子包下的所有类，主要源码如下：

```java
public class ClassPathBeanDefinitionScanner extends ClassPathScanningCandidateComponentProvider {
//创建一个类路径 Bean 定义扫描器
public ClassPathBeanDefinitionScanner(BeanDefinitionRegistry registry) {
this(registry, true);
}
//为容器创建一个类路径 Bean 定义扫描器，并指定是否使用默认的扫描过滤规则。
//即 Spring 默认扫描配置：@Component、@Repository、@Service、@Controller
//注解的 Bean，同时也支持 JavaEE6 的@ManagedBean 和 JSR-330 的@Named 注解
public ClassPathBeanDefinitionScanner(BeanDefinitionRegistry registry, boolean useDefaultFilters) {
this(registry, useDefaultFilters, getOrCreateEnvironment(registry));
}
public ClassPathBeanDefinitionScanner(BeanDefinitionRegistry registry, boolean useDefaultFilters,
Environment environment) {
this(registry, useDefaultFilters, environment,
(registry instanceof ResourceLoader ? (ResourceLoader) registry : null));
}
public ClassPathBeanDefinitionScanner(BeanDefinitionRegistry registry, boolean useDefaultFilters,
Environment environment, @Nullable ResourceLoader resourceLoader) {
Assert.notNull(registry, "BeanDefinitionRegistry must not be null");
//为容器设置加载 Bean 定义的注册器
this.registry = registry;
if (useDefaultFilters) {
registerDefaultFilters();
}
setEnvironment(environment);
//为容器设置资源加载器
setResourceLoader(resourceLoader);
}
//调用类路径 Bean 定义扫描器入口方法
public int scan(String... basePackages) {
//获取容器中已经注册的 Bean 个数
int beanCountAtScanStart = this.registry.getBeanDefinitionCount();
//启动扫描器扫描给定包
doScan(basePackages);
// Register annotation config processors, if necessary.
//注册注解配置(Annotation config)处理器
if (this.includeAnnotationConfig) {
AnnotationConfigUtils.registerAnnotationConfigProcessors(this.registry);
}
//返回注册的 Bean 个数
return (this.registry.getBeanDefinitionCount() - beanCountAtScanStart);
}
//类路径 Bean 定义扫描器扫描给定包及其子包
protected Set<BeanDefinitionHolder> doScan(String... basePackages) {
Assert.notEmpty(basePackages, "At least one base package must be specified");
//创建一个集合，存放扫描到 Bean 定义的封装类
Set<BeanDefinitionHolder> beanDefinitions = new LinkedHashSet<>();
//遍历扫描所有给定的包
for (String basePackage : basePackages) {
//调用父类 ClassPathScanningCandidateComponentProvider 的方法
//扫描给定类路径，获取符合条件的 Bean 定义
Set<BeanDefinition> candidates = findCandidateComponents(basePackage);
//遍历扫描到的 Bean
for (BeanDefinition candidate : candidates) {
//获取 Bean 定义类中@Scope 注解的值，即获取 Bean 的作用域
ScopeMetadata scopeMetadata = this.scopeMetadataResolver.resolveScopeMetadata(candidate);
//为 Bean 设置注解配置的作用域
candidate.setScope(scopeMetadata.getScopeName());
//为 Bean 生成名称
String beanName = this.beanNameGenerator.generateBeanName(candidate, this.registry);
//如果扫描到的 Bean 不是 Spring 的注解 Bean，则为 Bean 设置默认值，
//设置 Bean 的自动依赖注入装配属性等
if (candidate instanceof AbstractBeanDefinition) {
postProcessBeanDefinition((AbstractBeanDefinition) candidate, beanName);
}
//如果扫描到的 Bean 是 Spring 的注解 Bean，则处理其通用的 Spring 注解
if (candidate instanceof AnnotatedBeanDefinition) {
//处理注解 Bean 中通用的注解，在分析注解 Bean 定义类读取器时已经分析过
AnnotationConfigUtils.processCommonDefinitionAnnotations((AnnotatedBeanDefinition) candidate);
}
//根据 Bean 名称检查指定的 Bean 是否需要在容器中注册，或者在容器中冲突
if (checkCandidate(beanName, candidate)) {
BeanDefinitionHolder definitionHolder = new BeanDefinitionHolder(candidate, beanName);
//根据注解中配置的作用域，为 Bean 应用相应的代理模式
definitionHolder =
AnnotationConfigUtils.applyScopedProxyMode(scopeMetadata, definitionHolder,
this.registry);
beanDefinitions.add(definitionHolder);
//向容器注册扫描到的 Bean
registerBeanDefinition(definitionHolder, this.registry);
}
}
}
return beanDefinitions;
}
...
}
```

```java
/**
	 * Perform a scan within the specified base packages,
	 * returning the registered bean definitions.
	 * <p>This method does <i>not</i> register an annotation config processor
	 * but rather leaves this up to the caller.
	 * @param basePackages the packages to check for annotated classes
	 * @return set of beans registered if any for tooling registration purposes (never {@code null})
	 */
	protected Set<BeanDefinitionHolder> doScan(String... basePackages) {
		Assert.notEmpty(basePackages, "At least one base package must be specified");
		Set<BeanDefinitionHolder> beanDefinitions = new LinkedHashSet<>();
		for (String basePackage : basePackages) {
			Set<BeanDefinition> candidates = findCandidateComponents(basePackage);
			for (BeanDefinition candidate : candidates) {
				ScopeMetadata scopeMetadata = this.scopeMetadataResolver.resolveScopeMetadata(candidate);
				candidate.setScope(scopeMetadata.getScopeName());
				String beanName = this.beanNameGenerator.generateBeanName(candidate, this.registry);
				if (candidate instanceof AbstractBeanDefinition) {
					postProcessBeanDefinition((AbstractBeanDefinition) candidate, beanName);
				}
				if (candidate instanceof AnnotatedBeanDefinition) {
					AnnotationConfigUtils.processCommonDefinitionAnnotations((AnnotatedBeanDefinition) candidate);
				}
				if (checkCandidate(beanName, candidate)) {
					BeanDefinitionHolder definitionHolder = new BeanDefinitionHolder(candidate, beanName);
					definitionHolder =
							AnnotationConfigUtils.applyScopedProxyMode(scopeMetadata, definitionHolder, this.registry);
					beanDefinitions.add(definitionHolder);
					registerBeanDefinition(definitionHolder, this.registry);
				}
			}
		}
		return beanDefinitions;
	}
```

类路径 Bean 定义扫描器 ClassPathBeanDefinitionScanner 主要通过 findCandidateComponents方法调用其父类 ClassPathScanningCandidateComponentProvider 类来扫描获取给定包及其子包下的类。

(2).ClassPathScanningCandidateComponentProvider 扫描给定包及其子包的类：ClassPathScanningCandidateComponentProvider 类的 findCandidateComponents 方法具体实现扫描给定类路径包的功能，主要源码如下：

```java
public class ClassPathScanningCandidateComponentProvider implements EnvironmentCapable, ResourceLoaderAware {
//保存过滤规则要包含的注解，即 Spring 默认的@Component、@Repository、@Service、
//@Controller 注解的 Bean，以及 JavaEE6 的@ManagedBean 和 JSR-330 的@Named 注解
private final List<TypeFilter> includeFilters = new LinkedList<>();
//保存过滤规则要排除的注解
private final List<TypeFilter> excludeFilters = new LinkedList<>();
//构造方法，该方法在子类 ClassPathBeanDefinitionScanner 的构造方法中被调用
public ClassPathScanningCandidateComponentProvider(boolean useDefaultFilters) {
this(useDefaultFilters, new StandardEnvironment());
}
public ClassPathScanningCandidateComponentProvider(boolean useDefaultFilters, Environment environment) {
//如果使用 Spring 默认的过滤规则，则向容器注册过滤规则
if (useDefaultFilters) {
registerDefaultFilters();
}
setEnvironment(environment);
setResourceLoader(null);
}
//向容器注册过滤规则
@SuppressWarnings("unchecked")
protected void registerDefaultFilters() {
//向要包含的过滤规则中添加@Component 注解类，注意 Spring 中@Repository
//@Service 和@Controller 都是 Component，因为这些注解都添加了@Component 注解
this.includeFilters.add(new AnnotationTypeFilter(Component.class));
//获取当前类的类加载器
ClassLoader cl = ClassPathScanningCandidateComponentProvider.class.getClassLoader();
try {
//向要包含的过滤规则添加 JavaEE6 的@ManagedBean 注解
this.includeFilters.add(new AnnotationTypeFilter(
((Class<? extends Annotation>) ClassUtils.forName("javax.annotation.ManagedBean", cl)), false));
logger.debug("JSR-250 'javax.annotation.ManagedBean' found and supported for component scanning");
}
catch (ClassNotFoundException ex) {
// JSR-250 1.1 API (as included in Java EE 6) not available - simply skip.
}
try {
//向要包含的过滤规则添加@Named 注解
this.includeFilters.add(new AnnotationTypeFilter(
((Class<? extends Annotation>) ClassUtils.forName("javax.inject.Named", cl)), false));
logger.debug("JSR-330 'javax.inject.Named' annotation found and supported for component scanning");
}
catch (ClassNotFoundException ex) {
// JSR-330 API not available - simply skip.
}
}
//扫描给定类路径的包
public Set<BeanDefinition> findCandidateComponents(String basePackage) {
if (this.componentsIndex != null && indexSupportsIncludeFilters()) {
return addCandidateComponentsFromIndex(this.componentsIndex, basePackage);
}
else {
return scanCandidateComponents(basePackage);
}
}
private Set<BeanDefinition> addCandidateComponentsFromIndex(CandidateComponentsIndex index, String
basePackage) {
//创建存储扫描到的类的集合
Set<BeanDefinition> candidates = new LinkedHashSet<>();
try {
Set<String> types = new HashSet<>();
for (TypeFilter filter : this.includeFilters) {
String stereotype = extractStereotype(filter);
if (stereotype == null) {
throw new IllegalArgumentException("Failed to extract stereotype from "+ filter);
}
types.addAll(index.getCandidateTypes(basePackage, stereotype));
}
boolean traceEnabled = logger.isTraceEnabled();
boolean debugEnabled = logger.isDebugEnabled();
for (String type : types) {
//为指定资源获取元数据读取器，元信息读取器通过汇编(ASM)读//取资源元信息
MetadataReader metadataReader = getMetadataReaderFactory().getMetadataReader(type);
//如果扫描到的类符合容器配置的过滤规则
if (isCandidateComponent(metadataReader)) {
//通过汇编(ASM)读取资源字节码中的 Bean 定义元信息
AnnotatedGenericBeanDefinition sbd = new AnnotatedGenericBeanDefinition(
metadataReader.getAnnotationMetadata());
if (isCandidateComponent(sbd)) {
if (debugEnabled) {
logger.debug("Using candidate component class from index: " + type);
}
candidates.add(sbd);
}
else {
if (debugEnabled) {
logger.debug("Ignored because not a concrete top-level class: " + type);
}
}
}
else {
if (traceEnabled) {
logger.trace("Ignored because matching an exclude filter: " + type);
}
}
}
}
catch (IOException ex) {
throw new BeanDefinitionStoreException("I/O failure during classpath scanning", ex);
}
return candidates;
}
//判断元信息读取器读取的类是否符合容器定义的注解过滤规则
protected boolean isCandidateComponent(MetadataReader metadataReader) throws IOException {
//如果读取的类的注解在排除注解过滤规则中，返回 false
for (TypeFilter tf : this.excludeFilters) {
if (tf.match(metadataReader, getMetadataReaderFactory())) {
return false;
}
}
//如果读取的类的注解在包含的注解的过滤规则中，则返回 ture
for (TypeFilter tf : this.includeFilters) {
if (tf.match(metadataReader, getMetadataReaderFactory())) {
return isConditionMatch(metadataReader);
}
}
//如果读取的类的注解既不在排除规则，也不在包含规则中，则返回 false
return false;
}
}
```

#### AnnotationConfigWebApplicationContext载入注解Bean定义

AnnotationConfigWebApplicationContext是AnnotationConfigApplicationContext的Web版，它们对于注解 Bean 的注册和扫描是基本相同的，但是 AnnotationConfigWebApplicationContext对注解Bean定义的载入稍有不同，AnnotationConfigWebApplicationContext 注入注解 Bean 定义源码如下：

```java
//载入注解 Bean 定义资源
@Override
protected void loadBeanDefinitions(DefaultListableBeanFactory beanFactory) {
//为容器设置注解 Bean 定义读取器
AnnotatedBeanDefinitionReader reader = getAnnotatedBeanDefinitionReader(beanFactory);
//为容器设置类路径 Bean 定义扫描器
ClassPathBeanDefinitionScanner scanner = getClassPathBeanDefinitionScanner(beanFactory);
//获取容器的 Bean 名称生成器
BeanNameGenerator beanNameGenerator = getBeanNameGenerator();
//为注解 Bean 定义读取器和类路径扫描器设置 Bean 名称生成器
if (beanNameGenerator != null) {
reader.setBeanNameGenerator(beanNameGenerator);
scanner.setBeanNameGenerator(beanNameGenerator);
beanFactory.registerSingleton(AnnotationConfigUtils.CONFIGURATION_BEAN_NAME_GENERATOR,
beanNameGenerator);
}
//获取容器的作用域元信息解析器
ScopeMetadataResolver scopeMetadataResolver = getScopeMetadataResolver();
//为注解 Bean 定义读取器和类路径扫描器设置作用域元信息解析器
if (scopeMetadataResolver != null) {
reader.setScopeMetadataResolver(scopeMetadataResolver);
scanner.setScopeMetadataResolver(scopeMetadataResolver);
}
if (!this.annotatedClasses.isEmpty()) {
if (logger.isInfoEnabled()) {
logger.info("Registering annotated classes: [" +
StringUtils.collectionToCommaDelimitedString(this.annotatedClasses) + "]");
}
reader.register(this.annotatedClasses.toArray(new Class<?>[this.annotatedClasses.size()]));
}
if (!this.basePackages.isEmpty()) {
if (logger.isInfoEnabled()) {
logger.info("Scanning base packages: [" +
StringUtils.collectionToCommaDelimitedString(this.basePackages) + "]");
}
scanner.scan(this.basePackages.toArray(new String[this.basePackages.size()]));
}
//获取容器定义的 Bean 定义资源路径
String[] configLocations = getConfigLocations();
//如果定位的 Bean 定义资源路径不为空
if (configLocations != null) {
for (String configLocation : configLocations) {
try {
//使用当前容器的类加载器加载定位路径的字节码类文件
Class<?> clazz = ClassUtils.forName(configLocation, getClassLoader());
if (logger.isInfoEnabled()) {
logger.info("Successfully resolved class for [" + configLocation + "]");
}
reader.register(clazz);
}
catch (ClassNotFoundException ex) {
if (logger.isDebugEnabled()) {
logger.debug("Could not load class for config location [" + configLocation +
"] - trying package scan. " + ex);
}
//如果容器类加载器加载定义路径的 Bean 定义资源失败
//则启用容器类路径扫描器扫描给定路径包及其子包中的类
int count = scanner.scan(configLocation);
if (logger.isInfoEnabled()) {
if (count == 0) {
logger.info("No annotated classes found for specified class/package [" + configLocation + "]");
}
else {
logger.info("Found " + count + " annotated classes in package [" + configLocation + "]");
}
}
}
}
}
}
```

### IOC容器中那些鲜为人知的事儿

#### 介绍

通过前面章节中对 Spring IOC 容器的源码分析，我们已经基本上了解了 Spring IOC 容器对 Bean定义资源的定位、读入和解析过程，同时也清楚了当用户通过 getBean 方法向 IOC 容器获取被管理的Bean 时，IOC 容器对 Bean 进行的初始化和依赖注入过程，这些是 Spring IOC 容器的基本功能特性。

Spring IOC 容器还有一些高级特性，如使用 lazy-init 属性对 Bean 预初始化、FactoryBean 产生或者修饰 Bean 对象的生成、IOC 容器初始化 Bean 过程中使用 BeanPostProcessor 后置处理器对 Bean声明周期事件管理和 IOC 容器的 autowiring 自动装配功能等。

#### Spring IOC 容器的 lazy-init 属性实现预实例化

通过前面我们对 IOC 容器的实现和工作原理分析，我们知道 IOC 容器的初始化过程就是对 Bean 定义资源的定位、载入和注册，此时容器对 Bean 的依赖注入并没有发生，依赖注入主要是在应用程序第一次向容器索取 Bean 时，通过 getBean 方法的调用完成。

当Bean定义资源的<Bean>元素中配置了lazy-init属性时，容器将会在初始化的时候对所配置的Bean进行预实例化，Bean 的依赖注入在容器初始化的时候就已经完成。这样，当应用程序第一次向容器索取被管理的 Bean 时，就不用再初始化和对 Bean 进行依赖注入了，直接从容器中获取已经完成依赖注入的现成 Bean，可以提高应用第一次向容器获取 Bean 的性能。

下面我们通过代码分析容器预实例化的实现过程：

(1).refresh()

先从 IOC 容器的初始会过程开始，通过前面文章分析，我们知道 IOC 容器读入已经定位的 Bean 定义资源是从 refresh 方法开始的，我们首先从 AbstractApplicationContext 类的 refresh 方法入手分析.

在 refresh()方法中ConfigurableListableBeanFactorybeanFactory = obtainFreshBeanFactory();启动了 Bean定义资源的载入、注册过程，而 finishBeanFactoryInitialization 方法是对注册后的 Bean 定义中的预实例化(lazy-init=false,Spring 默认就是预实例化,即为 true)的 Bean 进行处理的地方。

当 Bean 定义资源被载入 IOC 容器之后，容器将 Bean 定义资源解析为容器内部的数据结构BeanDefinition 注 册 到 容 器 中 ， AbstractApplicationContext 类 中 的finishBeanFactoryInitialization 方法对配置了预实例化属性的 Bean 进行预初始化过程，源码如下

```java
//对配置了 lazy-init 属性的 Bean 进行预实例化处理
protected void finishBeanFactoryInitialization(ConfigurableListableBeanFactory beanFactory) {
//这是 Spring3 以后新加的代码，为容器指定一个转换服务(ConversionService)
//在对某些 Bean 属性进行转换时使用
if (beanFactory.containsBean(CONVERSION_SERVICE_BEAN_NAME) &&
beanFactory.isTypeMatch(CONVERSION_SERVICE_BEAN_NAME, ConversionService.class)) {
beanFactory.setConversionService(
beanFactory.getBean(CONVERSION_SERVICE_BEAN_NAME, ConversionService.class));
}
if (!beanFactory.hasEmbeddedValueResolver()) {
beanFactory.addEmbeddedValueResolver(strVal -> getEnvironment().resolvePlaceholders(strVal));
}
String[] weaverAwareNames = beanFactory.getBeanNamesForType(LoadTimeWeaverAware.class, false, false);
for (String weaverAwareName : weaverAwareNames) {
getBean(weaverAwareName);
}
//为了类型匹配，停止使用临时的类加载器
beanFactory.setTempClassLoader(null);
//缓存容器中所有注册的 BeanDefinition 元数据，以防被修改
beanFactory.freezeConfiguration();
//对配置了 lazy-init 属性的单态模式 Bean 进行预实例化处理
beanFactory.preInstantiateSingletons();
}
```

ConfigurableListableBeanFactory 是一个接口，其 preInstantiateSingletons 方法由其子类DefaultListableBeanFactory 提供。

DefaultListableBeanFactory 对配置 lazy-init 属性单态 Bean 的预实例化

```java
public void preInstantiateSingletons() throws BeansException {
if (this.logger.isDebugEnabled()) {
this.logger.debug("Pre-instantiating singletons in " + this);
}
List<String> beanNames = new ArrayList<>(this.beanDefinitionNames);
for (String beanName : beanNames) {
//获取指定名称的 Bean 定义
RootBeanDefinition bd = getMergedLocalBeanDefinition(beanName);
//Bean 不是抽象的，是单态模式的，且 lazy-init 属性配置为 false
if (!bd.isAbstract() && bd.isSingleton() && !bd.isLazyInit()) {
//如果指定名称的 bean 是创建容器的 Bean
if (isFactoryBean(beanName)) {
//FACTORY_BEAN_PREFIX=”&”，当 Bean 名称前面加”&”符号
//时，获取的是产生容器对象本身，而不是容器产生的 Bean.
//调用 getBean 方法，触发容器对 Bean 实例化和依赖注入过程
final FactoryBean<?> factory = (FactoryBean<?>) getBean(FACTORY_BEAN_PREFIX + beanName);
//标识是否需要预实例化
boolean isEagerInit;
if (System.getSecurityManager() != null && factory instanceof SmartFactoryBean) {
//一个匿名内部类
isEagerInit = AccessController.doPrivileged((PrivilegedAction<Boolean>) () ->
((SmartFactoryBean<?>) factory).isEagerInit(),
getAccessControlContext());
}
else {
isEagerInit = (factory instanceof SmartFactoryBean &&
((SmartFactoryBean<?>) factory).isEagerInit());
}
if (isEagerInit) {
//调用 getBean 方法，触发容器对 Bean 实例化和依赖注入过程
getBean(beanName);
}
}
else {
getBean(beanName);
}
}
}
```

通过对 lazy-init 处理源码的分析，我们可以看出，如果设置了 lazy-init 属性，则容器在完成 Bean定义的注册之后，会通过 getBean 方法，触发对指定 Bean 的初始化和依赖注入过程，这样当应用第一次向容器索取所需的 Bean 时，容器不再需要对 Bean 进行初始化和依赖注入，直接从已经完成实例化和依赖注入的 Bean 中取一个现成的 Bean，这样就提高了第一次获取 Bean 的性能。

#### FactoryBean的实现

在 Spring 中，有两个很容易混淆的类：BeanFactory 和 FactoryBean。

BeanFactory：Bean 工厂，是一个工厂(Factory)，我们 Spring IOC 容器的最顶层接口就是这个BeanFactory，它的作用是管理 Bean，即实例化、定位、配置应用程序中的对象及建立这些对象间的依赖。

FactoryBean：工厂 Bean，是一个 Bean，作用是产生其他 bean 实例。通常情况下，这种 bean 没有什么特别的要求，仅需要提供一个工厂方法，该方法用来返回其他 bean 实例。通常情况下，bean 无须自己实现工厂模式，Spring 容器担任工厂角色；但少数情况下，容器中的 bean 本身就是工厂，其作用是产生其它 bean 实例。

当用户使用容器本身时，可以使用转义字符”&”来得到 FactoryBean 本身，以区别通过 FactoryBean产生的实例对象和 FactoryBean 对象本身。在 BeanFactory 中通过如下代码定义了该转义字符：

String FACTORY_BEAN_PREFIX = "&";
如果 myJndiObject 是一个 FactoryBean，则使用&myJndiObject 得到的是 myJndiObject 对象，而不是 myJndiObject 产生出来的对象。

#### BeanPostProcessor后置处理器的实现

BeanPostProcessor 后置处理器是 Spring IOC 容器经常使用到的一个特性，这个 Bean 后置处理器是一个监听器，可以监听容器触发的 Bean 声明周期事件。后置处理器向容器注册以后，容器中管理的 Bean就具备了接收 IOC 容器事件回调的能力。

BeanPostProcessor 的使用非常简单，只需要提供一个实现接口 BeanPostProcessor 的实现类，然后在 Bean 的配置文件中设置即可

BeanPostProcessor 的源码如下：

```JAVA
public interface BeanPostProcessor {
//为在 Bean 的初始化前提供回调入口
@Nullable
default Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
return bean;
}
//为在 Bean 的初始化之后提供回调入口
@Nullable
default Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
return bean;
}
}
```

这两个回调的入口都是和容器管理的 Bean 的生命周期事件紧密相关，可以为用户提供在 Spring IOC容器初始化 Bean 过程中自定义的处理操作。

AbstractAutowireCapableBeanFactory 类对容器生成的 Bean 添加后置处理器,BeanPostProcessor后置处理器的调用发生在Spring IOC容器完成对Bean实例对象的创建和属性的依赖注入完成之后.

在对 Spring 依赖注入的源码分析过程中我们知道，当应用程序第一次调用 getBean方法(lazy-init预实例化除外)向Spring IOC容器索取指定Bean时触发Spring IOC容器创建Bean实例对象并进行依赖注入的过程，其中真正实现创建 Bean 对象并进行依赖注入的方法是AbstractAutowireCapableBeanFactory 类的 doCreateBean 方法，主要源码如下

```java
//真正创建 Bean 的方法
protected Object doCreateBean(final String beanName, final RootBeanDefinition mbd, final @Nullable Object[] args)
throws BeanCreationException {
//创建 Bean 实例对象
...
Object exposedObject = bean;
try {
//对 Bean 属性进行依赖注入
populateBean(beanName, mbd, instanceWrapper);
//在对 Bean 实例对象生成和依赖注入完成以后，开始对 Bean 实例对象
//进行初始化 ，为 Bean 实例对象应用 BeanPostProcessor 后置处理器
exposedObject = initializeBean(beanName, exposedObject, mbd);
}
catch (Throwable ex) {
if (ex instanceof BeanCreationException && beanName.equals(((BeanCreationException) ex).getBeanName())) {
throw (BeanCreationException) ex;
}
else {
throw new BeanCreationException(
mbd.getResourceDescription(), beanName, "Initialization of bean failed", ex);
}
}
...
//为应用返回所需要的实例对象
return exposedObject;
}
```

从上面的代码中我们知道，为 Bean 实例对象添加 BeanPostProcessor 后置处理器的入口的是initializeBean 方法。initializeBean 方法为容器产生的 Bean 实例对象添加 BeanPostProcessor 后置处理器：同样在 AbstractAutowireCapableBeanFactory 类中，initializeBean 方法实现为容器创建的 Bean实例对象添加 BeanPostProcessor 后置处理器，源码如下

```java
//初始容器创建的 Bean 实例对象，为其添加 BeanPostProcessor 后置处理器
protected Object initializeBean(final String beanName, final Object bean, @Nullable RootBeanDefinition mbd) {
//JDK 的安全机制验证权限
if (System.getSecurityManager() != null) {
//实现 PrivilegedAction 接口的匿名内部类
AccessController.doPrivileged((PrivilegedAction<Object>) () -> {
invokeAwareMethods(beanName, bean);
return null;
}, getAccessControlContext());
}
else {
//为 Bean 实例对象包装相关属性，如名称，类加载器，所属容器等信息
invokeAwareMethods(beanName, bean);
}
Object wrappedBean = bean;
//对 BeanPostProcessor 后置处理器的 postProcessBeforeInitialization
//回调方法的调用，为 Bean 实例初始化前做一些处理
if (mbd == null || !mbd.isSynthetic()) {
wrappedBean = applyBeanPostProcessorsBeforeInitialization(wrappedBean, beanName);
}
//调用 Bean 实例对象初始化的方法，这个初始化方法是在 Spring Bean 定义配置
//文件中通过 init-Method 属性指定的
try {
invokeInitMethods(beanName, wrappedBean, mbd);
}
catch (Throwable ex) {
throw new BeanCreationException(
(mbd != null ? mbd.getResourceDescription() : null),
beanName, "Invocation of init Method failed", ex);
}
//对 BeanPostProcessor 后置处理器的 postProcessAfterInitialization
//回调方法的调用，为 Bean 实例初始化之后做一些处理
if (mbd == null || !mbd.isSynthetic()) {
wrappedBean = applyBeanPostProcessorsAfterInitialization(wrappedBean, beanName);
}
return wrappedBean;
}

@Override
//调用 BeanPostProcessor 后置处理器实例对象初始化之前的处理方法
public Object applyBeanPostProcessorsBeforeInitialization(Object existingBean, String beanName)
throws BeansException {
Object result = existingBean;
//遍历容器为所创建的 Bean 添加的所有 BeanPostProcessor 后置处理器
for (BeanPostProcessor beanProcessor : getBeanPostProcessors()) {
//调用 Bean 实例所有的后置处理中的初始化前处理方法，为 Bean 实例对象在
//初始化之前做一些自定义的处理操作
Object current = beanProcessor.postProcessBeforeInitialization(result, beanName);
if (current == null) {
return result;
}
result = current;
}
return result;
}

@Override
//调用 BeanPostProcessor 后置处理器实例对象初始化之后的处理方法
public Object applyBeanPostProcessorsAfterInitialization(Object existingBean, String beanName)
throws BeansException {
Object result = existingBean;
//遍历容器为所创建的 Bean 添加的所有 BeanPostProcessor 后置处理器
for (BeanPostProcessor beanProcessor : getBeanPostProcessors()) {
//调用 Bean 实例所有的后置处理中的初始化后处理方法，为 Bean 实例对象在
//初始化之后做一些自定义的处理操作
Object current = beanProcessor.postProcessAfterInitialization(result, beanName);
if (current == null) {
return result;
}
result = current;
}
return result;
}
```

BeanPostProcessor 是一个接口，其初始化前的操作方法和初始化后的操作方法均委托其实现子类来实现，在 Spring 中，BeanPostProcessor 的实现子类非常的多，分别完成不同的操作，如：AOP 面向切面编程的注册通知适配器、Bean 对象的数据校验、Bean 继承属性/方法的合并等等，我们以最简单的 AOP 切面织入来简单了解其主要的功能。

AdvisorAdapterRegistrationManager 在 Bean 对象初始化后注册通知适配器：AdvisorAdapterRegistrationManager 是 BeanPostProcessor 的一个实现类，其主要的作用为容器中管理的 Bean 注册一个面向切面编程的通知适配器，以便在 Spring 容器为所管理的 Bean 进行面向切面编程时提供方便，其源码如下：

```java
//为容器中管理的 Bean 注册一个面向切面编程的通知适配器
public class AdvisorAdapterRegistrationManager implements BeanPostProcessor {
//容器中负责管理切面通知适配器注册的对象
private AdvisorAdapterRegistry advisorAdapterRegistry = GlobalAdvisorAdapterRegistry.getInstance();
public void setAdvisorAdapterRegistry(AdvisorAdapterRegistry advisorAdapterRegistry) {
//如果容器创建的 Bean 实例对象是一个切面通知适配器，则向容器的注册
this.advisorAdapterRegistry = advisorAdapterRegistry;
}
//BeanPostProcessor 在 Bean 对象初始化后的操作
@Override
public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
return bean;
}
//BeanPostProcessor 在 Bean 对象初始化前的操作
@Override
public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
if (bean instanceof AdvisorAdapter){
this.advisorAdapterRegistry.registerAdvisorAdapter((AdvisorAdapter) bean);
}
//没有做任何操作，直接返回容器创建的 Bean 对象
return bean;
}
}
```

其他的 BeanPostProcessor 接口实现类的也类似，都是对 Bean 对象使用到的一些特性进行处理，或者向 IOC 容器中注册，为创建的 Bean 实例对象做一些自定义的功能增加，这些操作是容器初始化 Bean时自动触发的，不需要认为的干预。

#### Spring IOC容器autowiring实现原理

Spring IOC 容器提供了两种管理 Bean 依赖关系的方式：

a.显式管理：通过BeanDefinition的属性值和构造方法实现Bean依赖关系管理。

b.autowiring：Spring IOC 容器的依赖自动装配功能，不需要对 Bean 属性的依赖关系做显式的声明，只需要在配置好 autowiring 属性，IOC 容器会自动使用反射查找属性的类型和名称，然后基于属性的类型或者名称来自动匹配容器中管理的 Bean，从而自动地完成依赖注入。

通过对 autowiring 自动装配特性的理解，我们知道容器对 Bean 的自动装配发生在容器对 Bean 依赖注入的过程中。在前面对 Spring IOC 容器的依赖注入过程源码分析中，我们已经知道了容器对 Bean实例对象的属性注入的处理发生在 AbstractAutoWireCapableBeanFactory 类中的 populateBean方法中，我们通过程序流程分析 autowiring 的实现原理：

(1). AbstractAutoWireCapableBeanFactory 对 Bean 实例进行属性依赖注入：

应用第一次通过 getBean 方法(配置了 lazy-init 预实例化属性的除外)向 IOC 容器索取 Bean 时，容器 创 建 Bean 实 例 对 象 ， 并 且 对 Bean 实 例 对 象 进 行 属 性 依 赖 注 入 ，AbstractAutoWireCapableBeanFactory的populateBean方法就是实现Bean属性依赖注入的功能，其主要源码如下：

```java
//将 Bean 属性设置到生成的实例对象上
protected void populateBean(String beanName, RootBeanDefinition mbd, @Nullable BeanWrapper bw) {
if (bw == null) {
if (mbd.hasPropertyValues()) {
throw new BeanCreationException(
mbd.getResourceDescription(), beanName, "Cannot apply property values to null instance");
}
else {
// Skip property population phase for null instance.
return;
}
}
boolean continueWithPropertyPopulation = true;
if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
for (BeanPostProcessor bp : getBeanPostProcessors()) {
if (bp instanceof InstantiationAwareBeanPostProcessor) {
InstantiationAwareBeanPostProcessor ibp = (InstantiationAwareBeanPostProcessor) bp;
if (!ibp.postProcessAfterInstantiation(bw.getWrappedInstance(), beanName)) {
continueWithPropertyPopulation = false;
break;
}
}
}
}
if (!continueWithPropertyPopulation) {
return;
}
//获取容器在解析 Bean 定义资源时为 BeanDefiniton 中设置的属性值
PropertyValues pvs = (mbd.hasPropertyValues() ? mbd.getPropertyValues() : null);
//对依赖注入处理，首先处理 autowiring 自动装配的依赖注入
if (mbd.getResolvedAutowireMode() == RootBeanDefinition.AUTOWIRE_BY_NAME ||
mbd.getResolvedAutowireMode() == RootBeanDefinition.AUTOWIRE_BY_TYPE) {
MutablePropertyValues newPvs = new MutablePropertyValues(pvs);
//根据 Bean 名称进行 autowiring 自动装配处理
if (mbd.getResolvedAutowireMode() == RootBeanDefinition.AUTOWIRE_BY_NAME) {
autowireByName(beanName, mbd, bw, newPvs);
}
//根据 Bean 类型进行 autowiring 自动装配处理
if (mbd.getResolvedAutowireMode() == RootBeanDefinition.AUTOWIRE_BY_TYPE) {
autowireByType(beanName, mbd, bw, newPvs);
}
pvs = newPvs;
}
//对非 autowiring 的属性进行依赖注入处理
...
}
```

```java
//根据类型对属性进行自动依赖注入
protected void autowireByType(
String beanName, AbstractBeanDefinition mbd, BeanWrapper bw, MutablePropertyValues pvs) {
//获取用户定义的类型转换器
TypeConverter converter = getCustomTypeConverter();
if (converter == null) {
converter = bw;
}
//存放解析的要注入的属性
Set<String> autowiredBeanNames = new LinkedHashSet<>(4);
//对 Bean 对象中非简单属性(不是简单继承的对象，如 8 中原始类型，字符
//URL 等都是简单属性)进行处理
String[] propertyNames = unsatisfiedNonSimpleProperties(mbd, bw);
for (String propertyName : propertyNames) {
try {
//获取指定属性名称的属性描述器
PropertyDescriptor pd = bw.getPropertyDescriptor(propertyName);
// Don't try autowiring by type for type Object: never makes sense,
// even if it technically is a unsatisfied, non-simple property.
//不对 Object 类型的属性进行 autowiring 自动依赖注入
if (Object.class != pd.getPropertyType()) {
//获取属性的 setter 方法
MethodParameter MethodParam = BeanUtils.getWriteMethodParameter(pd);
// Do not allow eager init for type matching in case of a prioritized post-processor.
//检查指定类型是否可以被转换为目标对象的类型
boolean eager = !PriorityOrdered.class.isInstance(bw.getWrappedInstance());
//创建一个要被注入的依赖描述
DependencyDescriptor desc = new AutowireByTypeDependencyDescriptor(MethodParam, eager);
//根据容器的 Bean 定义解析依赖关系，返回所有要被注入的 Bean 对象
Object autowiredArgument = resolveDependency(desc, beanName, autowiredBeanNames, converter);
if (autowiredArgument != null) {
//为属性赋值所引用的对象
pvs.add(propertyName, autowiredArgument);
}
for (String autowiredBeanName : autowiredBeanNames) {
//指定名称属性注册依赖 Bean 名称，进行属性依赖注入
registerDependentBean(autowiredBeanName, beanName);
if (logger.isDebugEnabled()) {
logger.debug("Autowiring by type from bean name '" + beanName + "' via property '" +
propertyName + "' to bean named '" + autowiredBeanName + "'");
}
}
//释放已自动注入的属性
autowiredBeanNames.clear();
}
}
catch (BeansException ex) {
throw new UnsatisfiedDependencyException(mbd.getResourceDescription(), beanName, propertyName, ex);
}
}
}
```

通过上面的源码分析，我们可以看出来通过属性名进行自动依赖注入的相对比通过属性类型进行自动依赖注入要稍微简单一些，但是真正实现属性注入的是 DefaultSingletonBeanRegistry 类的registerDependentBean 方法。

```java
/为指定的 Bean 注入依赖的 Bean
public void registerDependentBean(String beanName, String dependentBeanName) {
//处理 Bean 名称，将别名转换为规范的 Bean 名称
String canonicalName = canonicalName(beanName);
Set<String> dependentBeans = this.dependentBeanMap.get(canonicalName);
if (dependentBeans != null && dependentBeans.contains(dependentBeanName)) {
return;
}
// No entry yet -> fully synchronized manipulation of the dependentBeans Set
//多线程同步，保证容器内数据的一致性
//先从容器中：bean 名称-->全部依赖 Bean 名称集合找查找给定名称 Bean 的依赖 Bean
synchronized (this.dependentBeanMap) {
//获取给定名称 Bean 的所有依赖 Bean 名称
dependentBeans = this.dependentBeanMap.get(canonicalName);
if (dependentBeans == null) {
//为 Bean 设置依赖 Bean 信息
dependentBeans = new LinkedHashSet<>(8);
this.dependentBeanMap.put(canonicalName, dependentBeans);
}
//向容器中：bean 名称-->全部依赖 Bean 名称集合添加 Bean 的依赖信息
//即，将 Bean 所依赖的 Bean 添加到容器的集合中
dependentBeans.add(dependentBeanName);
}
//从容器中：bean 名称-->指定名称 Bean 的依赖 Bean 集合找查找给定名称 Bean 的依赖 Bean
synchronized (this.dependenciesForBeanMap) {
Set<String> dependenciesForBean = this.dependenciesForBeanMap.get(dependentBeanName);
if (dependenciesForBean == null) {
dependenciesForBean = new LinkedHashSet<>(8);
this.dependenciesForBeanMap.put(dependentBeanName, dependenciesForBean);
}
//向容器中：bean 名称-->指定 Bean 的依赖 Bean 名称集合添加 Bean 的依赖信息
//即，将 Bean 所依赖的 Bean 添加到容器的集合中
dependenciesForBean.add(canonicalName);
}
}
```

通过对 autowiring 的源码分析，我们可以看出，autowiring 的实现过程：

a.对 Bean 的属性代调用 getBean 方法，完成依赖 Bean 的初始化和依赖注入。
b.将依赖 Bean 的属性引用设置到被依赖的 Bean 属性上。
c.将依赖 Bean 的名称和被依赖 Bean 的名称存储在 IOC 容器的集合中。

Spring IOC 容器的 autowiring 属性自动依赖注入是一个很方便的特性，可以简化开发时的配置，但是凡是都有两面性，自动属性依赖注入也有不足，首先，Bean 的依赖关系在配置文件中无法很清楚地看出来，对于维护造成一定困难。其次，由于自动依赖注入是 Spring 容器自动执行的，容器是不会智能判断的，如果配置不当，将会带来无法预料的后果，所以自动依赖注入特性在使用时还是综合考虑 。

#### InitializingBean

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

package org.springframework.beans.factory;

/**
 * Interface to be implemented by beans that need to react once all their properties
 * have been set by a {@link BeanFactory}: e.g. to perform custom initialization,
 * or merely to check that all mandatory properties have been set.
 *
 * <p>An alternative to implementing {@code InitializingBean} is specifying a custom
 * init method, for example in an XML bean definition. For a list of all bean
 * lifecycle methods, see the {@link BeanFactory BeanFactory javadocs}.
 *
 * @author Rod Johnson
 * @author Juergen Hoeller
 * @see DisposableBean
 * @see org.springframework.beans.factory.config.BeanDefinition#getPropertyValues()
 * @see org.springframework.beans.factory.support.AbstractBeanDefinition#getInitMethodName()
 */
public interface InitializingBean {

   /**
    * Invoked by the containing {@code BeanFactory} after it has set all bean properties
    * and satisfied {@link BeanFactoryAware}, {@code ApplicationContextAware} etc.
    * <p>This method allows the bean instance to perform validation of its overall
    * configuration and final initialization when all bean properties have been set.
    * @throws Exception in the event of misconfiguration (such as failure to set an
    * essential property) or if initialization fails for any other reason
    */
   void afterPropertiesSet() throws Exception;

}
```

在AbstractAutowireCapableBeanFactory的initializeBean()方法中执行。

```java
protected Object initializeBean(final String beanName, final Object bean, @Nullable RootBeanDefinition mbd) {
   if (System.getSecurityManager() != null) {
      AccessController.doPrivileged((PrivilegedAction<Object>) () -> {
         invokeAwareMethods(beanName, bean);
         return null;
      }, getAccessControlContext());
   }
   else {
      invokeAwareMethods(beanName, bean);
   }

   Object wrappedBean = bean;
   if (mbd == null || !mbd.isSynthetic()) {
      wrappedBean = applyBeanPostProcessorsBeforeInitialization(wrappedBean, beanName);
   }

   try {
      invokeInitMethods(beanName, wrappedBean, mbd);
   }
   catch (Throwable ex) {
      throw new BeanCreationException(
            (mbd != null ? mbd.getResourceDescription() : null),
            beanName, "Invocation of init method failed", ex);
   }
   if (mbd == null || !mbd.isSynthetic()) {
      wrappedBean = applyBeanPostProcessorsAfterInitialization(wrappedBean, beanName);
   }

   return wrappedBean;
}
```

```java
/**
 * Give a bean a chance to react now all its properties are set,
 * and a chance to know about its owning bean factory (this object).
 * This means checking whether the bean implements InitializingBean or defines
 * a custom init method, and invoking the necessary callback(s) if it does.
 * @param beanName the bean name in the factory (for debugging purposes)
 * @param bean the new bean instance we may need to initialize
 * @param mbd the merged bean definition that the bean was created with
 * (can also be {@code null}, if given an existing bean instance)
 * @throws Throwable if thrown by init methods or by the invocation process
 * @see #invokeCustomInitMethod
 */
protected void invokeInitMethods(String beanName, final Object bean, @Nullable RootBeanDefinition mbd)
      throws Throwable {

   boolean isInitializingBean = (bean instanceof InitializingBean);
   if (isInitializingBean && (mbd == null || !mbd.isExternallyManagedInitMethod("afterPropertiesSet"))) {
      if (logger.isTraceEnabled()) {
         logger.trace("Invoking afterPropertiesSet() on bean with name '" + beanName + "'");
      }
      if (System.getSecurityManager() != null) {
         try {
            AccessController.doPrivileged((PrivilegedExceptionAction<Object>) () -> {
               ((InitializingBean) bean).afterPropertiesSet();
               return null;
            }, getAccessControlContext());
         }
         catch (PrivilegedActionException pae) {
            throw pae.getException();
         }
      }
      else {
         ((InitializingBean) bean).afterPropertiesSet();
      }
   }

   if (mbd != null && bean.getClass() != NullBean.class) {
      String initMethodName = mbd.getInitMethodName();
      if (StringUtils.hasLength(initMethodName) &&
            !(isInitializingBean && "afterPropertiesSet".equals(initMethodName)) &&
            !mbd.isExternallyManagedInitMethod(initMethodName)) {
         invokeCustomInitMethod(beanName, bean, mbd);
      }
   }
}
```

#### spring ioc中单例初始化

AbstractApplicationContext的refresh函数载入Bean 定义过程，有finishBeanFactoryInitialization(beanFactory);方法，将对所有的单例模式的bean进行初始化。只有是non-lazy-init的都会。

```java
/**
 * Finish the initialization of this context's bean factory,
 * initializing all remaining singleton beans.
 */
protected void finishBeanFactoryInitialization(ConfigurableListableBeanFactory beanFactory) {
   // Initialize conversion service for this context.
   if (beanFactory.containsBean(CONVERSION_SERVICE_BEAN_NAME) &&
         beanFactory.isTypeMatch(CONVERSION_SERVICE_BEAN_NAME, ConversionService.class)) {
      beanFactory.setConversionService(
            beanFactory.getBean(CONVERSION_SERVICE_BEAN_NAME, ConversionService.class));
   }

   // Register a default embedded value resolver if no bean post-processor
   // (such as a PropertyPlaceholderConfigurer bean) registered any before:
   // at this point, primarily for resolution in annotation attribute values.
   if (!beanFactory.hasEmbeddedValueResolver()) {
      beanFactory.addEmbeddedValueResolver(strVal -> getEnvironment().resolvePlaceholders(strVal));
   }

   // Initialize LoadTimeWeaverAware beans early to allow for registering their transformers early.
   String[] weaverAwareNames = beanFactory.getBeanNamesForType(LoadTimeWeaverAware.class, false, false);
   for (String weaverAwareName : weaverAwareNames) {
      getBean(weaverAwareName);
   }

   // Stop using the temporary ClassLoader for type matching.
   beanFactory.setTempClassLoader(null);

   // Allow for caching all bean definition metadata, not expecting further changes.
   beanFactory.freezeConfiguration();

   // Instantiate all remaining (non-lazy-init) singletons.
   beanFactory.preInstantiateSingletons();
}
```

```java
@Override
public void preInstantiateSingletons() throws BeansException {
   if (logger.isTraceEnabled()) {
      logger.trace("Pre-instantiating singletons in " + this);
   }

   // Iterate over a copy to allow for init methods which in turn register new bean definitions.
   // While this may not be part of the regular factory bootstrap, it does otherwise work fine.
   List<String> beanNames = new ArrayList<>(this.beanDefinitionNames);

   // Trigger initialization of all non-lazy singleton beans...
   for (String beanName : beanNames) {
      RootBeanDefinition bd = getMergedLocalBeanDefinition(beanName);
      if (!bd.isAbstract() && bd.isSingleton() && !bd.isLazyInit()) {
         if (isFactoryBean(beanName)) {
            Object bean = getBean(FACTORY_BEAN_PREFIX + beanName);
            if (bean instanceof FactoryBean) {
               final FactoryBean<?> factory = (FactoryBean<?>) bean;
               boolean isEagerInit;
               if (System.getSecurityManager() != null && factory instanceof SmartFactoryBean) {
                  isEagerInit = AccessController.doPrivileged((PrivilegedAction<Boolean>)
                              ((SmartFactoryBean<?>) factory)::isEagerInit,
                        getAccessControlContext());
               }
               else {
                  isEagerInit = (factory instanceof SmartFactoryBean &&
                        ((SmartFactoryBean<?>) factory).isEagerInit());
               }
               if (isEagerInit) {
                  getBean(beanName);
               }
            }
         }
         else {
            getBean(beanName);
         }
      }
   }

   // Trigger post-initialization callback for all applicable beans...
   for (String beanName : beanNames) {
      Object singletonInstance = getSingleton(beanName);
      if (singletonInstance instanceof SmartInitializingSingleton) {
         final SmartInitializingSingleton smartSingleton = (SmartInitializingSingleton) singletonInstance;
         if (System.getSecurityManager() != null) {
            AccessController.doPrivileged((PrivilegedAction<Object>) () -> {
               smartSingleton.afterSingletonsInstantiated();
               return null;
            }, getAccessControlContext());
         }
         else {
            smartSingleton.afterSingletonsInstantiated();
         }
      }
   }
}
```

```xml
<bean id="gobalService" class="com.lqd.service.GobalService" scope="singleton" lazy-init="true"></bean>
```

当lazy-init为true的时候，不会进行初始化。默认这个值是false。

#### init-method

```xml
<bean id="gobalService" class="com.lqd.service.GobalService" scope="singleton"
      lazy-init="false"
      init-method="say"></bean>
```

实现这块的源码在：（AbstractAutowireCapableBeanFactory.invokeInitMethods）

```java
protected void invokeInitMethods(String beanName, final Object bean, @Nullable RootBeanDefinition mbd)
      throws Throwable {

   boolean isInitializingBean = (bean instanceof InitializingBean);
   if (isInitializingBean && (mbd == null || !mbd.isExternallyManagedInitMethod("afterPropertiesSet"))) {
      if (logger.isTraceEnabled()) {
         logger.trace("Invoking afterPropertiesSet() on bean with name '" + beanName + "'");
      }
      if (System.getSecurityManager() != null) {
         try {
            AccessController.doPrivileged((PrivilegedExceptionAction<Object>) () -> {
               ((InitializingBean) bean).afterPropertiesSet();
               return null;
            }, getAccessControlContext());
         }
         catch (PrivilegedActionException pae) {
            throw pae.getException();
         }
      }
      else {
         ((InitializingBean) bean).afterPropertiesSet();
      }
   }

   if (mbd != null && bean.getClass() != NullBean.class) {
      String initMethodName = mbd.getInitMethodName();
      if (StringUtils.hasLength(initMethodName) &&
            !(isInitializingBean && "afterPropertiesSet".equals(initMethodName)) &&
            !mbd.isExternallyManagedInitMethod(initMethodName)) {
         invokeCustomInitMethod(beanName, bean, mbd);
      }
   }
}
```

#### @PostConstruct

1，当容器启动，AbstractApplicationContext.refresh()的时候，在执行registerBeanPostProcessors()方法时初始化的。先在BeanPostProcessor中注册有PostConstruct注解和PreDestroy注解的类。

```java
public static void registerBeanPostProcessors(
      ConfigurableListableBeanFactory beanFactory, AbstractApplicationContext applicationContext) {

   String[] postProcessorNames = beanFactory.getBeanNamesForType(BeanPostProcessor.class, true, false);

   // Register BeanPostProcessorChecker that logs an info message when
   // a bean is created during BeanPostProcessor instantiation, i.e. when
   // a bean is not eligible for getting processed by all BeanPostProcessors.
   int beanProcessorTargetCount = beanFactory.getBeanPostProcessorCount() + 1 + postProcessorNames.length;
   beanFactory.addBeanPostProcessor(new BeanPostProcessorChecker(beanFactory, beanProcessorTargetCount));

   // Separate between BeanPostProcessors that implement PriorityOrdered,
   // Ordered, and the rest.
   List<BeanPostProcessor> priorityOrderedPostProcessors = new ArrayList<>();
   List<BeanPostProcessor> internalPostProcessors = new ArrayList<>();
   List<String> orderedPostProcessorNames = new ArrayList<>();
   List<String> nonOrderedPostProcessorNames = new ArrayList<>();
   for (String ppName : postProcessorNames) {
      if (beanFactory.isTypeMatch(ppName, PriorityOrdered.class)) {
         BeanPostProcessor pp = beanFactory.getBean(ppName, BeanPostProcessor.class);
         priorityOrderedPostProcessors.add(pp);
         if (pp instanceof MergedBeanDefinitionPostProcessor) {
            internalPostProcessors.add(pp);
         }
      }
      else if (beanFactory.isTypeMatch(ppName, Ordered.class)) {
         orderedPostProcessorNames.add(ppName);
      }
      else {
         nonOrderedPostProcessorNames.add(ppName);
      }
   }

   // First, register the BeanPostProcessors that implement PriorityOrdered.
   sortPostProcessors(priorityOrderedPostProcessors, beanFactory);
   registerBeanPostProcessors(beanFactory, priorityOrderedPostProcessors);

   // Next, register the BeanPostProcessors that implement Ordered.
   List<BeanPostProcessor> orderedPostProcessors = new ArrayList<>();
   for (String ppName : orderedPostProcessorNames) {
      BeanPostProcessor pp = beanFactory.getBean(ppName, BeanPostProcessor.class);
      orderedPostProcessors.add(pp);
      if (pp instanceof MergedBeanDefinitionPostProcessor) {
         internalPostProcessors.add(pp);
      }
   }
   sortPostProcessors(orderedPostProcessors, beanFactory);
   registerBeanPostProcessors(beanFactory, orderedPostProcessors);

   // Now, register all regular BeanPostProcessors.
   List<BeanPostProcessor> nonOrderedPostProcessors = new ArrayList<>();
   for (String ppName : nonOrderedPostProcessorNames) {
      BeanPostProcessor pp = beanFactory.getBean(ppName, BeanPostProcessor.class);
      nonOrderedPostProcessors.add(pp);
      if (pp instanceof MergedBeanDefinitionPostProcessor) {
         internalPostProcessors.add(pp);
      }
   }
   registerBeanPostProcessors(beanFactory, nonOrderedPostProcessors);

   // Finally, re-register all internal BeanPostProcessors.
   sortPostProcessors(internalPostProcessors, beanFactory);
   registerBeanPostProcessors(beanFactory, internalPostProcessors);

   // Re-register post-processor for detecting inner beans as ApplicationListeners,
   // moving it to the end of the processor chain (for picking up proxies etc).
   beanFactory.addBeanPostProcessor(new ApplicationListenerDetector(applicationContext));
}
```

凡是继承了BeanPostProcessor.class接口的类都会在这步初始化。

```java
/**
 * Create a new CommonAnnotationBeanPostProcessor,
 * with the init and destroy annotation types set to
 * {@link javax.annotation.PostConstruct} and {@link javax.annotation.PreDestroy},
 * respectively.
 */
public CommonAnnotationBeanPostProcessor() {
   setOrder(Ordered.LOWEST_PRECEDENCE - 3);
   setInitAnnotationType(PostConstruct.class);
   setDestroyAnnotationType(PreDestroy.class);
   ignoreResourceType("javax.xml.ws.WebServiceContext");
}
```

2，在这个类CommonAnnotationBeanPostProcessor初始化的时候，将会在AbstractAutowireCapableBeanFactory执行注册到上面的那个注册器的方法。

```java
public CommonAnnotationBeanPostProcessor() {
   setOrder(Ordered.LOWEST_PRECEDENCE - 3);
   setInitAnnotationType(PostConstruct.class);
   setDestroyAnnotationType(PreDestroy.class);
   ignoreResourceType("javax.xml.ws.WebServiceContext");
}
```

```java
protected Object initializeBean(final String beanName, final Object bean, @Nullable RootBeanDefinition mbd) {
   if (System.getSecurityManager() != null) {
      AccessController.doPrivileged((PrivilegedAction<Object>) () -> {
         invokeAwareMethods(beanName, bean);
         return null;
      }, getAccessControlContext());
   }
   else {
      invokeAwareMethods(beanName, bean);
   }

   Object wrappedBean = bean;
   if (mbd == null || !mbd.isSynthetic()) {
      wrappedBean = applyBeanPostProcessorsBeforeInitialization(wrappedBean, beanName);
   }

   try {
      invokeInitMethods(beanName, wrappedBean, mbd);
   }
   catch (Throwable ex) {
      throw new BeanCreationException(
            (mbd != null ? mbd.getResourceDescription() : null),
            beanName, "Invocation of init method failed", ex);
   }
   if (mbd == null || !mbd.isSynthetic()) {
      wrappedBean = applyBeanPostProcessorsAfterInitialization(wrappedBean, beanName);
   }

   return wrappedBean;
}
```

```java
@Override
public Object applyBeanPostProcessorsBeforeInitialization(Object existingBean, String beanName)
      throws BeansException {

   Object result = existingBean;
   for (BeanPostProcessor processor : getBeanPostProcessors()) {
      Object current = processor.postProcessBeforeInitialization(result, beanName);
      if (current == null) {
         return result;
      }
      result = current;
   }
   return result;
}
```

在CommonAnnotationBeanPostProcessor的父类InitDestroyAnnotationBeanPostProcessor中执行方法调用：

```java
public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
   LifecycleMetadata metadata = findLifecycleMetadata(bean.getClass());
   try {
      metadata.invokeInitMethods(bean, beanName);
   }
   catch (InvocationTargetException ex) {
      throw new BeanCreationException(beanName, "Invocation of init method failed", ex.getTargetException());
   }
   catch (Throwable ex) {
      throw new BeanCreationException(beanName, "Failed to invoke init method", ex);
   }
   return bean;
}
```

相比较，init-method，这个注解将先执行。这个注解和这个init-method执行都发生在依赖注入之后的类初始化。

而initializingBean的实现后的afterPropertiesSet方法执行在init-method之前，这个注解之后。

#### bean的默认scope

默认的类注解和xml配置的bean都是单例的。要修改可以添加注解和修改xml的bean ：

```xml
<bean id="gobalService" class="com.lqd.service.GobalService" scope="singleton"
      lazy-init="false"></bean>
```

```java
/**
 * @author lqd
 * @DATE 2018/12/7
 * @Description xxxxx
 */
@Component
@Scope("singleton")
public class GobalService implements InitializingBean
{
    private int gobal ;
```

#### InstantiationAwareBeanPostProcessor

在依赖注入属性对象的 时候，在调用前后会执行这个接口的实现类。、

```java
protected void populateBean(String beanName, RootBeanDefinition mbd, @Nullable BeanWrapper bw) {
   if (bw == null) {
      if (mbd.hasPropertyValues()) {
         throw new BeanCreationException(
               mbd.getResourceDescription(), beanName, "Cannot apply property values to null instance");
      }
      else {
         // Skip property population phase for null instance.
         return;
      }
   }

   // Give any InstantiationAwareBeanPostProcessors the opportunity to modify the
   // state of the bean before properties are set. This can be used, for example,
   // to support styles of field injection.
   boolean continueWithPropertyPopulation = true;

   if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
      for (BeanPostProcessor bp : getBeanPostProcessors()) {
         if (bp instanceof InstantiationAwareBeanPostProcessor) {
            InstantiationAwareBeanPostProcessor ibp = (InstantiationAwareBeanPostProcessor) bp;
            if (!ibp.postProcessAfterInstantiation(bw.getWrappedInstance(), beanName)) {
               continueWithPropertyPopulation = false;
               break;
            }
         }
      }
   }

   if (!continueWithPropertyPopulation) {
      return;
   }

   PropertyValues pvs = (mbd.hasPropertyValues() ? mbd.getPropertyValues() : null);

   if (mbd.getResolvedAutowireMode() == AUTOWIRE_BY_NAME || mbd.getResolvedAutowireMode() == AUTOWIRE_BY_TYPE) {
      MutablePropertyValues newPvs = new MutablePropertyValues(pvs);
      // Add property values based on autowire by name if applicable.
      if (mbd.getResolvedAutowireMode() == AUTOWIRE_BY_NAME) {
         autowireByName(beanName, mbd, bw, newPvs);
      }
      // Add property values based on autowire by type if applicable.
      if (mbd.getResolvedAutowireMode() == AUTOWIRE_BY_TYPE) {
         autowireByType(beanName, mbd, bw, newPvs);
      }
      pvs = newPvs;
   }

   boolean hasInstAwareBpps = hasInstantiationAwareBeanPostProcessors();
   boolean needsDepCheck = (mbd.getDependencyCheck() != AbstractBeanDefinition.DEPENDENCY_CHECK_NONE);

   PropertyDescriptor[] filteredPds = null;
   if (hasInstAwareBpps) {
      if (pvs == null) {
         pvs = mbd.getPropertyValues();
      }
      for (BeanPostProcessor bp : getBeanPostProcessors()) {
         if (bp instanceof InstantiationAwareBeanPostProcessor) {
            InstantiationAwareBeanPostProcessor ibp = (InstantiationAwareBeanPostProcessor) bp;
            PropertyValues pvsToUse = ibp.postProcessProperties(pvs, bw.getWrappedInstance(), beanName);
            if (pvsToUse == null) {
               if (filteredPds == null) {
                  filteredPds = filterPropertyDescriptorsForDependencyCheck(bw, mbd.allowCaching);
               }
               pvsToUse = ibp.postProcessPropertyValues(pvs, filteredPds, bw.getWrappedInstance(), beanName);
               if (pvsToUse == null) {
                  return;
               }
            }
            pvs = pvsToUse;
         }
      }
   }
   if (needsDepCheck) {
      if (filteredPds == null) {
         filteredPds = filterPropertyDescriptorsForDependencyCheck(bw, mbd.allowCaching);
      }
      checkDependencies(beanName, mbd, filteredPds, pvs);
   }

   if (pvs != null) {
      applyPropertyValues(beanName, mbd, bw, pvs);
   }
}
```

#### BeanNameAware

在依赖注入之后，initializingBean之前执行。

```java
protected Object initializeBean(final String beanName, final Object bean, @Nullable RootBeanDefinition mbd) {
   if (System.getSecurityManager() != null) {
      AccessController.doPrivileged((PrivilegedAction<Object>) () -> {
         invokeAwareMethods(beanName, bean);
         return null;
      }, getAccessControlContext());
   }
   else {
      invokeAwareMethods(beanName, bean);
   }
 ......
   return wrappedBean;
}
```

```java
private void invokeAwareMethods(final String beanName, final Object bean) {
   if (bean instanceof Aware) {
      if (bean instanceof BeanNameAware) {
         ((BeanNameAware) bean).setBeanName(beanName);
      }
      if (bean instanceof BeanClassLoaderAware) {
         ClassLoader bcl = getBeanClassLoader();
         if (bcl != null) {
            ((BeanClassLoaderAware) bean).setBeanClassLoader(bcl);
         }
      }
      if (bean instanceof BeanFactoryAware) {
         ((BeanFactoryAware) bean).setBeanFactory(AbstractAutowireCapableBeanFactory.this);
      }
   }
}
```

