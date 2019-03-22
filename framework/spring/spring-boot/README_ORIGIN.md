[TOC]

## 源码分析

1，SpringApplication的第一步就是初始化所有的spring.factories文件中的ApplicationContextInitializer和ApplicationListener对应的类。



### SpringApplication

```java
public static ConfigurableApplicationContext run(Object source, String... args) {
		return run(new Object[] { source }, args);
	}

public static ConfigurableApplicationContext run(Object[] sources, String[] args) {
		return new SpringApplication(sources).run(args);
	}

public SpringApplication(Object... sources) {
		initialize(sources);
	}

//重点方法,获取spring.factories的所有配置ApplicationContextInitializer和ApplicationListener
@SuppressWarnings({ "unchecked", "rawtypes" })
private void initialize(Object[] sources) {
   if (sources != null && sources.length > 0) {
      this.sources.addAll(Arrays.asList(sources));
   }
   this.webEnvironment = deduceWebEnvironment();
   setInitializers((Collection) getSpringFactoriesInstances(
         ApplicationContextInitializer.class));
   setListeners((Collection) getSpringFactoriesInstances(ApplicationListener.class));
   this.mainApplicationClass = deduceMainApplicationClass();//初始化启动类
}

private <T> Collection<? extends T> getSpringFactoriesInstances(Class<T> type,
			Class<?>[] parameterTypes, Object... args) {
		ClassLoader classLoader = Thread.currentThread().getContextClassLoader();
		// Use names and ensure unique to protect against duplicates
		Set<String> names = new LinkedHashSet<String>(
				SpringFactoriesLoader.loadFactoryNames(type, classLoader));//重点
		List<T> instances = createSpringFactoriesInstances(type, parameterTypes,
				classLoader, args, names);
		AnnotationAwareOrderComparator.sort(instances);
		return instances;
	}

//重点方法
/**
	 * Run the Spring application, creating and refreshing a new
	 * {@link ApplicationContext}.
	 * @param args the application arguments (usually passed from a Java main method)
	 * @return a running {@link ApplicationContext}
	 */
	public ConfigurableApplicationContext run(String... args) {
		StopWatch stopWatch = new StopWatch();
		stopWatch.start();
		ConfigurableApplicationContext context = null;
		FailureAnalyzers analyzers = null;
		configureHeadlessProperty();//自力更生 开启非终端处理
        //listeners - > EventPublishingRunListener 用于广播在spring容器启动之前周期上的事件
		SpringApplicationRunListeners listeners = getRunListeners(args);
		listeners.starting();
		try {
			ApplicationArguments applicationArguments = new DefaultApplicationArguments(
					args);
            //1，创建并配置当前SpringBoot应用将要使用的Environment（包括配置要使用的PropertySource以及Profile）,
            //2，并遍历调用所有的SpringApplicationRunListener的environmentPrepared()方法，广播Environment准备完毕。
            //3,在ApplicationEnvironmentPreparedEvent事件中解析注解@PropertySource、
			ConfigurableEnvironment environment = prepareEnvironment(listeners,
					applicationArguments);//广播事件 - 重点
			Banner printedBanner = printBanner(environment);//打印banner
            //根据webEnvironment的值来决定创建何种类型的ApplicationContext对象
            //如果是web环境，则创建org.springframework.boot.context.embedded.AnnotationConfigEmbeddedWebApplicationContext
            //否则创建org.springframework.context.annotation.AnnotationConfigApplicationContext
            context = this.createApplicationContext();
			context = createApplicationContext();//新建IOC容器 
            
             //注册异常分析器
            //查找spring.factories的所有配置的FailureAnalyzer
			analyzers = new FailureAnalyzers(context);
            
            //为ApplicationContext加载environment，之后逐个执行ApplicationContextInitializer的initialize()方法来进一步封装ApplicationContext，
            //并调用所有的SpringApplicationRunListener的contextPrepared()方法，【EventPublishingRunListener只提供了一个空的contextPrepared()方法】， 
            //这里就包括通过**@EnableAutoConfiguration**导入的各种自动配置类。
            //这里的source 取得是spring.factories指定的BootstrapConfiguration所有配置，这个操作在BootstrapApplicationListener事件触发时候完成
			prepareContext(context, environment, listeners, applicationArguments,
					printedBanner);
            
            ////初始化所有自动配置类，调用ApplicationContext的refresh()方法
            //ioc容器初始化
			refreshContext(context);
            
            //遍历所有注册的ApplicationRunner和CommandLineRunner，并执行其run()方法。
            //该过程可以理解为是SpringBoot完成ApplicationContext初始化前的最后一步工作，
            //我们可以实现自己的ApplicationRunner或者CommandLineRunner，来对SpringBoot的启动过程进行扩展。
			afterRefresh(context, applicationArguments);
            
             //调用所有的SpringApplicationRunListener的finished()方法，广播SpringBoot已经完成了ApplicationContext初始化的全部过程。
			listeners.finished(context, null);
			stopWatch.stop();
			if (this.logStartupInfo) {
				new StartupInfoLogger(this.mainApplicationClass)
						.logStarted(getApplicationLog(), stopWatch);
			}
			return context;
		}
		catch (Throwable ex) {
			handleRunFailure(context, listeners, analyzers, ex);
			throw new IllegalStateException(ex);
		}
	}
```

#### SpringFactoriesLoader

```java
/**
	 * Load the fully qualified class names of factory implementations of the
	 * given type from {@value #FACTORIES_RESOURCE_LOCATION}, using the given
	 * class loader.
	 * @param factoryClass the interface or abstract class representing the factory
	 * @param classLoader the ClassLoader to use for loading resources; can be
	 * {@code null} to use the default
	 * @see #loadFactories
	 * @throws IllegalArgumentException if an error occurs while loading factory names
	 */
	public static List<String> loadFactoryNames(Class<?> factoryClass, ClassLoader classLoader) {
		String factoryClassName = factoryClass.getName();
		try {
			Enumeration<URL> urls = (classLoader != null ? classLoader.getResources(FACTORIES_RESOURCE_LOCATION) :
					ClassLoader.getSystemResources(FACTORIES_RESOURCE_LOCATION));
			List<String> result = new ArrayList<String>();
			while (urls.hasMoreElements()) {
				URL url = urls.nextElement();
				Properties properties = PropertiesLoaderUtils.loadProperties(new UrlResource(url));
				String factoryClassNames = properties.getProperty(factoryClassName);
				result.addAll(Arrays.asList(StringUtils.commaDelimitedListToStringArray(factoryClassNames)));
			}
			return result;
		}
		catch (IOException ex) {
			throw new IllegalArgumentException("Unable to load [" + factoryClass.getName() +
					"] factories from location [" + FACTORIES_RESOURCE_LOCATION + "]", ex);
		}
	}
```

搜索所有的spring.factories文件，其中以spring-boot的jar中的为例：

```properties
# PropertySource Loaders
org.springframework.boot.env.PropertySourceLoader=\
org.springframework.boot.env.PropertiesPropertySourceLoader,\
org.springframework.boot.env.YamlPropertySourceLoader

# Run Listeners
org.springframework.boot.SpringApplicationRunListener=\
org.springframework.boot.context.event.EventPublishingRunListener

# Application Context Initializers
org.springframework.context.ApplicationContextInitializer=\
org.springframework.boot.context.ConfigurationWarningsApplicationContextInitializer,\
org.springframework.boot.context.ContextIdApplicationContextInitializer,\
org.springframework.boot.context.config.DelegatingApplicationContextInitializer,\
org.springframework.boot.context.embedded.ServerPortInfoApplicationContextInitializer

# Application Listeners
org.springframework.context.ApplicationListener=\
org.springframework.boot.ClearCachesApplicationListener,\
org.springframework.boot.builder.ParentContextCloserApplicationListener,\
org.springframework.boot.context.FileEncodingApplicationListener,\
org.springframework.boot.context.config.AnsiOutputApplicationListener,\
org.springframework.boot.context.config.ConfigFileApplicationListener,\
org.springframework.boot.context.config.DelegatingApplicationListener,\
org.springframework.boot.liquibase.LiquibaseServiceLocatorApplicationListener,\
org.springframework.boot.logging.ClasspathLoggingApplicationListener,\
org.springframework.boot.logging.LoggingApplicationListener

# Environment Post Processors
org.springframework.boot.env.EnvironmentPostProcessor=\
org.springframework.boot.cloud.CloudFoundryVcapEnvironmentPostProcessor,\
org.springframework.boot.env.SpringApplicationJsonEnvironmentPostProcessor

# Failure Analyzers
org.springframework.boot.diagnostics.FailureAnalyzer=\
org.springframework.boot.diagnostics.analyzer.BeanCurrentlyInCreationFailureAnalyzer,\
org.springframework.boot.diagnostics.analyzer.BeanNotOfRequiredTypeFailureAnalyzer,\
org.springframework.boot.diagnostics.analyzer.BindFailureAnalyzer,\
org.springframework.boot.diagnostics.analyzer.ConnectorStartFailureAnalyzer,\
org.springframework.boot.diagnostics.analyzer.NoUniqueBeanDefinitionFailureAnalyzer,\
org.springframework.boot.diagnostics.analyzer.PortInUseFailureAnalyzer,\
org.springframework.boot.diagnostics.analyzer.ValidationExceptionFailureAnalyzer

# FailureAnalysisReporters
org.springframework.boot.diagnostics.FailureAnalysisReporter=\
org.springframework.boot.diagnostics.LoggingFailureAnalysisReporter
```

通过key：org.springframework.boot.SpringApplicationRunListener 从上面得到：org.springframework.boot.context.event.EventPublishingRunListener。

### SPI

（Service Provider Interface）介绍

```
JDK通过SPI定义的方式，将要暴露对外使用的具体实现在META-INF/services/文件下声明，使用的工具类是ServiceLoader.

spring配置放在 META-INF/spring.factories中，Spring中使用的类是SpringFactoriesLoader，在org.springframework.core.io.support包中.
```

### 事件机制

要理解下面的内容，首先要有了解到一个事件周期：1，定义事件；2，注册监听；3，发布事件 。

```
ApplicationEvent：应用事件
ApplicationListener：应用监听器
具体参考springframework的event
```

#### spring boot 的事件

参考：https://blog.csdn.net/sinat_25518349/article/details/85545848

#### ApplicationContextInitializer

### PropertySource

参考：https://jinnianshilongnian.iteye.com/blog/2000183

CompositePropertySource、Environment、Profile

```
PropertyPlaceholderHelper、PropertyResolver
```

#### SpringBoot 自动配置

主要通过 `@EnableAutoConfiguration`, `@Conditional`, `@EnableConfigurationProperties` 或者 `@ConfigurationProperties` 等几个注解来进行自动配置完成的。

`@EnableAutoConfiguration` 开启自动配置，主要作用就是调用 `Spring-Core` 包里的 `loadFactoryNames()`，将 `autoconfig` 包里的已经写好的自动配置加载进来。

```
# Auto Configure
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
org.springframework.boot.autoconfigure.admin.SpringApplicationAdminJmxAutoConfiguration,\
org.springframework.boot.autoconfigure.aop.AopAutoConfiguration,\
org.springframework.boot.autoconfigure.amqp.RabbitAutoConfiguration,\
org.springframework.boot.autoconfigure.batch.BatchAutoConfiguration,\
org.springframework.boot.autoconfigure.cache.CacheAutoConfiguration,\
org.springframework.boot.autoconfigure.cassandra.CassandraAutoConfiguration,\
org.springframework.boot.autoconfigure.cloud.CloudAutoConfiguration,\
org.springframework.boot.autoconfigure.context.ConfigurationPropertiesAutoConfiguration
```

`@Conditional` 条件注解，通过判断类路径下有没有相应配置的 `jar` 包来确定是否加载和自动配置这个类。

`@EnableConfigurationProperties` 的作用就是，给自动配置提供具体的配置参数，只需要写在 `application.properties` 中，就可以通过映射写入配置类的 `POJO` 属性中。  

### 上下文理解

参考：https://www.cnblogs.com/niechen/p/8968204.html

### 常用的注解

#### @Configuration

```java
@Configuation等价于<Beans></Beans>
@Bean等价于<Bean></Bean>
@ComponentScan等价于<context:component-scan base-package="com.dxz.demo"/>
```

### TypeFilter

### ZuulFilter







