### SpringApplication启动过程分析

*通过现象找本质（源码）*

#### 启动的方式

``` java

@SpringBootApplication
public class MicroserviceProjectApplication {
    
public static void main(String[] args) {
		
    	//第一种：
		//SpringApplication.run(MicroserviceProjectApplication.class, args);
    
    	//第三种：
    	//fluent api模式 - 编程的模式
    	//jquery、jdk8等
		/*new SpringApplicationBuilder(MicroserviceProjectApplication.class)
				//单元测试，PORT随机
				.properties("server.port=0")
				.run(args);*/
    
		//第二种：
		SpringApplication springApplication =
				new SpringApplication(MicroserviceProjectApplication.class);
		final Map<String,Object> map = new LinkedHashMap<>(1);
		map.put("server.port",0);
		springApplication.setDefaultProperties(map);
		ConfigurableApplicationContext configurableApplicationContext =springApplication.run(args);	
   System.out.println(configurableApplicationContext);   //System.out.println(configurableApplicationContext.getBean(MicroserviceProjectApplication.class));
	}}
```

[Fluent Builder API](https://docs.spring.io/spring-boot/docs/2.1.3.RELEASE/reference/htmlsingle/#boot-features-fluent-builder-api)

##### AnnotationConfigApplicationContext

###### 模拟

```java
public static void main(String[] args) {
    
AnnotationConfigApplicationContext
                annotationConfigApplicationContext = new AnnotationConfigApplicationContext();
        annotationConfigApplicationContext.register(AnnatationsTest.class);
        annotationConfigApplicationContext.refresh();
        AnnatationsTest annatationsTest = annotationConfigApplicationContext.getBean(AnnatationsTest.class);
        System.out.println(annatationsTest);
}    
```

```java
public static void main(String[] args) {

    AnnotationConfigApplicationContext
            annotationConfigApplicationContext = new AnnotationConfigApplicationContext(AnnatationsTest.class);
    AnnatationsTest annatationsTest =
            annotationConfigApplicationContext.getBean(AnnatationsTest.class);
    System.out.println(annatationsTest);
}
```

###### 启动的核心注解

```java
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = {
      @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class),
      @Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })
public @interface SpringBootApplication {
```

###### @EnableAutoConfiguration

流程：自动装配的流程（spring boot四大神器之一）

```java
refresh()

->invokeBeanFactoryPostProcessors()

//PostProcessorRegistrationDelegate相当重要的类
->PostProcessorRegistrationDelegate.invokeBeanFactoryPostProcessors()->PostProcessorRegistrationDelegate.invokeBeanDefinitionRegistryPostProcessors()

->ConfigurationClassPostProcessor.postProcessBeanDefinitionRegistry()

    //解析@Import
->ConfigurationClassParser.parse()
    //相当重要的解析方法（解析注解import，ImportResource，ComponentScan，PropertySource，Bean）
   -> ConfigurationClassParser.doProcessConfigurationClass()
   -> DeferredImportSelectorHandler.handle()
    ->保存在
    private List<DeferredImportSelectorHolder> deferredImportSelectors = new ArrayList<>();

->DeferredImportSelectorHandler.process()
	->将DeferredImportSelectorHandler对象注入到DeferredImportSelectorGrouping.deferredImports属性中
    
->AutoConfigurationImportSelector$AutoConfigurationGroup.process()

->AutoConfigurationImportSelector.getAutoConfigurationEntry()

->结合@Contitional注解进行自动装配    

```

ConfigurationClassParser获取@Import

```java
/**
 * Returns {@code @Import} class, considering all meta-annotations.
 */
private Set<SourceClass> getImports(SourceClass sourceClass) throws IOException {
   Set<SourceClass> imports = new LinkedHashSet<>();
   Set<SourceClass> visited = new LinkedHashSet<>();
   collectImports(sourceClass, imports, visited);
   return imports;
}
```

ConfigurationClassParser解析@Import：

```java
public void parse(Set<BeanDefinitionHolder> configCandidates) {
   for (BeanDefinitionHolder holder : configCandidates) {
      BeanDefinition bd = holder.getBeanDefinition();
      try {
         if (bd instanceof AnnotatedBeanDefinition) {
             //解析@Import：
            parse(((AnnotatedBeanDefinition) bd).getMetadata(), holder.getBeanName());
         }
         else if (bd instanceof AbstractBeanDefinition && ((AbstractBeanDefinition) bd).hasBeanClass()) {
            parse(((AbstractBeanDefinition) bd).getBeanClass(), holder.getBeanName());
         }
         else {
            parse(bd.getBeanClassName(), holder.getBeanName());
         }
      }
      catch (BeanDefinitionStoreException ex) {
         throw ex;
      }
      catch (Throwable ex) {
         throw new BeanDefinitionStoreException(
               "Failed to parse configuration class [" + bd.getBeanClassName() + "]", ex);
      }
   }
	
   //将
   this.deferredImportSelectorHandler.process();
}


public void process() {
			List<DeferredImportSelectorHolder> deferredImports = this.deferredImportSelectors;
			this.deferredImportSelectors = null;
			try {
				if (deferredImports != null) {
					DeferredImportSelectorGroupingHandler handler = new DeferredImportSelectorGroupingHandler();
                    //继承了order的接口，排优先级顺序
					deferredImports.sort(DEFERRED_IMPORT_COMPARATOR);
                    //注册到groups中
					deferredImports.forEach(handler::register);
                    //执行select中的process
					handler.processGroupImports();
				}
			}
			finally {
				this.deferredImportSelectors = new ArrayList<>();
			}
		}


private void processImports(ConfigurationClass configClass, SourceClass currentSourceClass,
			Collection<SourceClass> importCandidates, boolean checkForCircularImports) {

		if (importCandidates.isEmpty()) {
			return;
		}

		if (checkForCircularImports && isChainedImportOnStack(configClass)) {
			this.problemReporter.error(new CircularImportProblem(configClass, this.importStack));
		}
		else {
			this.importStack.push(configClass);
			try {
				for (SourceClass candidate : importCandidates) {
                    //解析@Import - AutoConfigurationImportSelector注解
					if (candidate.isAssignable(ImportSelector.class)) {
						// Candidate class is an ImportSelector -> delegate to it to determine imports
						Class<?> candidateClass = candidate.loadClass();
						ImportSelector selector = BeanUtils.instantiateClass(candidateClass, ImportSelector.class);
						ParserStrategyUtils.invokeAwareMethods(
								selector, this.environment, this.resourceLoader, this.registry);
						if (selector instanceof DeferredImportSelector) {
							this.deferredImportSelectorHandler.handle(
									configClass, (DeferredImportSelector) selector);
						}
						else {
							String[] importClassNames = selector.selectImports(currentSourceClass.getMetadata());
							Collection<SourceClass> importSourceClasses = asSourceClasses(importClassNames);
							processImports(configClass, currentSourceClass, importSourceClasses, false);
						}
					}
					else if 
                        //解析@AutoConfigurationPackage注解
                       (candidate.isAssignable(ImportBeanDefinitionRegistrar.class)) {
						// Candidate class is an ImportBeanDefinitionRegistrar ->
						// delegate to it to register additional bean definitions
						Class<?> candidateClass = candidate.loadClass();
						ImportBeanDefinitionRegistrar registrar =
								BeanUtils.instantiateClass(candidateClass, ImportBeanDefinitionRegistrar.class);
						ParserStrategyUtils.invokeAwareMethods(
								registrar, this.environment, this.resourceLoader, this.registry);
						configClass.addImportBeanDefinitionRegistrar(registrar, currentSourceClass.getMetadata());
					}
					else {
						// Candidate class not an ImportSelector or ImportBeanDefinitionRegistrar ->
						// process it as an @Configuration class
						this.importStack.registerImport(
								currentSourceClass.getMetadata(), candidate.getMetadata().getClassName());
						processConfigurationClass(candidate.asConfigClass(configClass));
					}
				}
			}
		.....
	}

```

获取自动装配的内容：

```java
protected AutoConfigurationEntry getAutoConfigurationEntry(
      AutoConfigurationMetadata autoConfigurationMetadata,
      AnnotationMetadata annotationMetadata) {
   if (!isEnabled(annotationMetadata)) {
      return EMPTY_ENTRY;
   }
   AnnotationAttributes attributes = getAttributes(annotationMetadata);
    /**核心处理**/
   List<String> configurations = getCandidateConfigurations(annotationMetadata,
         attributes);
   configurations = removeDuplicates(configurations);
   Set<String> exclusions = getExclusions(annotationMetadata, attributes);
   checkExcludedClasses(configurations, exclusions);
   configurations.removeAll(exclusions);
   configurations = filter(configurations, autoConfigurationMetadata);
   fireAutoConfigurationImportEvents(configurations, exclusions);
   return new AutoConfigurationEntry(configurations, exclusions);
}
```

```
@EnableAutoConfiguration 作用
从classpath中搜索所有META-INF/spring.factories配置文件然后，将其中org.springframework.boot.autoconfigure.EnableAutoConfiguration key对应的配置项加载到spring容器

其内部实现的关键点有
1）ImportSelector 该接口的方法的返回值都会被纳入到spring容器管理中
2）SpringFactoriesLoader 该类可以从classpath中搜索所有META-INF/spring.factories配置文件，并读取配置
```

你会发现spring boot到处都是spring.factories文件，包含初始化、监听、自动装配、分析等等。他的核心思想源于：JDK中的SPI机制

###### SPI

（Service Provider Interface）介绍

```
JDK通过SPI定义的方式，将要暴露对外使用的具体实现在META-INF/services/文件下声明，使用的工具类是ServiceLoader.

spring配置放在 META-INF/spring.factories中，Spring中使用的类是SpringFactoriesLoader，在org.springframework.core.io.support包中.
```

#### 注解的派生性

##### 派生性以@Component为例

###### 例子

```
 //"com.lqd.spring.*"
  //AnnatationsTest
  AnnotationConfigApplicationContext
          annotationConfigApplicationContext =
          new AnnotationConfigApplicationContext(AnnatationsTest.class);
//  annotationConfigApplicationContext.register();
//  annotationConfigApplicationContext.refresh();
  System.out.println(annotationConfigApplicationContext.getBean(AnnatationsTest.class));
```

###### @Component源码讲解

```java 
1,@Component --> @ComponentScan
    @Service \ @Controller \ @configuration \ @Respository   
    
2,ComponentScanAnnotationParser.parse
	ClassPathBeanDefinitionScanner --> ClassPathScanningCandidateComponentProvider	
(
AnnotationConfigApplicationContext
#refresh()#invokeBeanFactoryPostProcessors(beanFactory);
)
```

###### ClassPathScanningCandidateComponentProvider

核心处理的方法

```java
/**
 * Determine whether the given class does not match any exclude filter
 * and does match at least one include filter.
 * @param metadataReader the ASM ClassReader for the class
 * @return whether the class qualifies as a candidate component
 */
protected boolean isCandidateComponent(MetadataReader metadataReader) throws IOException {
   for (TypeFilter tf : this.excludeFilters) {
      if (tf.match(metadataReader, getMetadataReaderFactory())) {
         return false;
      }
   }
   for (TypeFilter tf : this.includeFilters) {
      if (tf.match(metadataReader, getMetadataReaderFactory())) {
         return isConditionMatch(metadataReader);
      }
   }
   return false;
}

private Set<BeanDefinition> scanCandidateComponents(String basePackage) {
		Set<BeanDefinition> candidates = new LinkedHashSet<>();
		try {
			String packageSearchPath = ResourcePatternResolver.CLASSPATH_ALL_URL_PREFIX +
					resolveBasePackage(basePackage) + '/' + this.resourcePattern;
			Resource[] resources = getResourcePatternResolver().getResources(packageSearchPath);
			boolean traceEnabled = logger.isTraceEnabled();
			boolean debugEnabled = logger.isDebugEnabled();
			for (Resource resource : resources) {
				if (traceEnabled) {
					logger.trace("Scanning " + resource);
				}
				if (resource.isReadable()) {
					try {
                        //获取类的元注解
						MetadataReader metadataReader = getMetadataReaderFactory().getMetadataReader(resource);
                        //判断是否是Component注解
						if (isCandidateComponent(metadataReader)) {
							ScannedGenericBeanDefinition sbd = new ScannedGenericBeanDefinition(metadataReader);
							sbd.setResource(resource);
							sbd.setSource(resource);
							.....
```

###### AnnotationAttributesReadingVisitor

```java

/**
*ClassPathScanningCandidateComponentProvider获取元注解的方法
*/
@Override
public void visitEnd() {
   super.visitEnd();

   Class<? extends Annotation> annotationClass = this.attributes.annotationType();
   if (annotationClass != null) {
      List<AnnotationAttributes> attributeList = this.attributesMap.get(this.annotationType);
      if (attributeList == null) {
         this.attributesMap.add(this.annotationType, this.attributes);
      }
      else {
         attributeList.add(0, this.attributes);
      }
      if (!AnnotationUtils.isInJavaLangAnnotationPackage(annotationClass.getName())) {
         try {
            Annotation[] metaAnnotations = annotationClass.getAnnotations();
            if (!ObjectUtils.isEmpty(metaAnnotations)) {
               Set<Annotation> visited = new LinkedHashSet<>();
               for (Annotation metaAnnotation : metaAnnotations) {
                  recursivelyCollectMetaAnnotations(visited, metaAnnotation);
               }
               if (!visited.isEmpty()) {
                  Set<String> metaAnnotationTypeNames = new LinkedHashSet<>(visited.size());
                  for (Annotation ann : visited) {
                     metaAnnotationTypeNames.add(ann.annotationType().getName());
                  }
                  this.metaAnnotationMap.put(annotationClass.getName(), metaAnnotationTypeNames);
               }
            }
         }
         catch (Throwable ex) {
            if (logger.isDebugEnabled()) {
               logger.debug("Failed to introspect meta-annotations on " + annotationClass + ": " + ex);
            }
         }
      }
   }
}
```

###### AnnotationTypeFilter

``` java
@Override
	protected boolean matchSelf(MetadataReader metadataReader) {
        //这里得到的就是AnnotationAttributesReadingVisitor类
        //用到的就是AnnotationAttributesReadingVisitor解析得到类的的所有非java的元注解
		AnnotationMetadata metadata = metadataReader.getAnnotationMetadata();
		return metadata.hasAnnotation(this.annotationType.getName()) ||
				(this.considerMetaAnnotations && metadata.hasMetaAnnotation(this.annotationType.getName()));
	}
```

###### 总结

```properties
@Component的”派生性“流程：
1，扫描文件夹下所有的资源
2，解析每个资源的注解，获取元注解集合
3，判断是否有@Component的注解，若有就向IOC容器注册bean

这样某些其他功能的注解就可以用到@Component的特性，同时又可以起到自己独特的作用，是不是提高了代码的重复利用率，可读性！
```

以此来推：

1，spring framework 4.0中的@Conditional的派生性：

``` java
ConditionalOnBean / ConditionalOnClass / ConditionalOnCloudPlatform /
ConditionalOnEnabledResourceChain / ConditionalOnExpression /
ConditionalOnJava / ConditionalOnJndi / ConditionalOnMissingBean 

对上述注解解析都在：OnXXXXXcondition类
```

2，spring framework 3.0中的@Import的派生性：

```java 
EnableAsync / EnableWebMvc / EnableAspectJAutoProxy /EnableAsync
```

##### [注解编程模型](https://github.com/spring-projects/spring-framework/wiki/Spring-Annotation-Programming-Model)

``` java
meta  annotations (元注解)    
stereotype annotations (spring的模式注解)
```

#### 类型推断

```java
SpringApplication springApplication =
				new SpringApplication(MicroserviceProjectApplication.class);
		final Map<String,Object> map = new LinkedHashMap<>(1);
		map.put("server.port",0);
		springApplication.setDefaultProperties(map);
		/**
		 * 类型推断
		 */
		springApplication.setWebApplicationType(WebApplicationType.NONE);
		ConfigurableApplicationContext configurableApplicationContext =springApplication.run(args);
		System.out.println(configurableApplicationContext);
```

``` java
static WebApplicationType deduceFromClasspath() {
		if (ClassUtils.isPresent(WEBFLUX_INDICATOR_CLASS, null)
				&& !ClassUtils.isPresent(WEBMVC_INDICATOR_CLASS, null)
				&& !ClassUtils.isPresent(JERSEY_INDICATOR_CLASS, null)) {
			return WebApplicationType.REACTIVE;
		}
		for (String className : SERVLET_INDICATOR_CLASSES) {
			if (!ClassUtils.isPresent(className, null)) {
				return WebApplicationType.NONE;
			}
		}
		return WebApplicationType.SERVLET;
	}
```

#### 事件/监听	

目的

``` java
1，ApplicationEventMulticaster 加载或者初始化组件
2，spring上下文生命周期控制 注解驱动Bean
```

要理解下面的内容，首先要有了解到一个事件周期：1，定义事件；2，注册监听；3，发布事件 。

```properties
Spring 事件理解为消息：

ApplicationEvent 相当于消息内容
ApplicationListener 相当于消息消费者、订阅者
ApplicationEventMulticaster 相当于消息生产者、发布者
```

##### 自定义spring 事件

```java
SpringApplication springApplication
        = new SpringApplication(MicroserviceProjectApplication.class);
springApplication.setWebApplicationType(WebApplicationType.NONE);
final Map map = new HashMap(1);
map.put("server.port","0");
springApplication.setDefaultProperties(map);
ConfigurableApplicationContext configurableApplicationContext
        = springApplication.run(args);
configurableApplicationContext.addApplicationListener(new SpringEventListener());
configurableApplicationContext.publishEvent
        (new SpringEvent(MicroserviceProjectApplication.class,
         "spring event!"));

// SimpleApplicationEventMulticaster simpleApplicationEventMulticaster =configurableApplicationContext.getBean(SimpleApplicationEventMulticaster.class);
//simpleApplicationEventMulticaster.multicastEvent(new SpringEvent(MicroserviceProjectApplication.class,
                        "spring event!"));
```

##### spring boot的事件类型

```java
new SpringApplicationBuilder(MicroserviceProjectApplication.class)
        .listeners(event -> {
            System.err.println(event.getClass().getSimpleName());
        }).run(args)
            .close();
```

[解释](https://docs.spring.io/spring-boot/docs/2.1.3.RELEASE/reference/htmlsingle/#boot-features-application-events-and-listeners)

##### application.properties的读取

ConfigFileApplicationListener. onApplicationEvent()

->ConfigFileApplicationListener.postProcessEnvironment()

->ConfigFileApplicationListener$Loader.load()

```java
@Override
public void onApplicationEvent(ApplicationEvent event) {
   if (event instanceof ApplicationEnvironmentPreparedEvent) {
      onApplicationEnvironmentPreparedEvent(
            (ApplicationEnvironmentPreparedEvent) event);
   }
   if (event instanceof ApplicationPreparedEvent) {
      onApplicationPreparedEvent(event);
   }
}

private void onApplicationEnvironmentPreparedEvent(
			ApplicationEnvironmentPreparedEvent event) {
		List<EnvironmentPostProcessor> postProcessors = loadPostProcessors();
		postProcessors.add(this);
		AnnotationAwareOrderComparator.sort(postProcessors);
		for (EnvironmentPostProcessor postProcessor : postProcessors) {
            //加载配置
            //遍历所有的EnvironmentPostProcessor接口的实现类，并处理逻辑
			postProcessor.postProcessEnvironment(event.getEnvironment(),
					event.getSpringApplication());
		}
	}



```

```java
public void load() {
			this.profiles = new LinkedList<>();
			this.processedProfiles = new LinkedList<>();
			this.activatedProfiles = false;
			this.loaded = new LinkedHashMap<>();
			initializeProfiles();
			while (!this.profiles.isEmpty()) {
				Profile profile = this.profiles.poll();
				if (profile != null && !profile.isDefaultProfile()) {
					addProfileToEnvironment(profile.getName());
				}
				load(profile, this::getPositiveProfileFilter,
						addToLoaded(MutablePropertySources::addLast, false));
				this.processedProfiles.add(profile);
			}
			resetEnvironmentProfiles(this.processedProfiles);
			load(null, this::getNegativeProfileFilter,
					addToLoaded(MutablePropertySources::addFirst, true));
   			 //资源配置文件的顺序控制MutablePropertySources
			addLoadedPropertySources();
		}

private void load(PropertySourceLoader loader, String location, Profile profile,
      DocumentFilter filter, DocumentConsumer consumer) {
   try {
      Resource resource = this.resourceLoader.getResource(location);
      if (resource == null || !resource.exists()) {
         if (this.logger.isTraceEnabled()) {
            StringBuilder description = getDescription(
                  "Skipped missing config ", location, resource, profile);
            this.logger.trace(description);
         }
         return;
      }
      if (!StringUtils.hasText(
            StringUtils.getFilenameExtension(resource.getFilename()))) {
         if (this.logger.isTraceEnabled()) {
            StringBuilder description = getDescription(
                  "Skipped empty config extension ", location, resource,
                  profile);
            this.logger.trace(description);
         }
         return;
      }
      String name = "applicationConfig: [" + location + "]";
      List<Document> documents = loadDocuments(loader, name, resource);
      if (CollectionUtils.isEmpty(documents)) {
         if (this.logger.isTraceEnabled()) {
            StringBuilder description = getDescription(
                  "Skipped unloaded config ", location, resource, profile);
            this.logger.trace(description);
         }
         return;
      }
      List<Document> loaded = new ArrayList<>();
      for (Document document : documents) {
         if (filter.match(document)) {
            addActiveProfiles(document.getActiveProfiles());
            addIncludedProfiles(document.getIncludeProfiles());
            loaded.add(document);
         }
      }
      Collections.reverse(loaded);
       //将配置文件内容的propertysources添加到MutablePropertySources中
       //MutablePropertySources是一个容纳各种PropertySource的对象，然后通过getProperty去取
      if (!loaded.isEmpty()) {
         loaded.forEach((document) -> consumer.accept(profile, document));
         if (this.logger.isDebugEnabled()) {
            StringBuilder description = getDescription("Loaded config file ",
                  location, resource, profile);
            this.logger.debug(description);
         }
      }
   }
   catch (Exception ex) {
      throw new IllegalStateException("Failed to load property "
            + "source from location '" + location + "'", ex);
   }
}
```

#### context上下文

```java
Environment 有三种实现方式：

普通类型：StandardEnvironment
Reactive类型：StandardReactiveWebEnvironment
Web类型：StandardServletEnvironment

Environment
AbstractEnvironment
 - StandardEnvironment
Enviroment 关联着一个PropertySources 实例
PropertySources 关联着多个PropertySource，并且有优先级

其中比较常用的PropertySource 实现：
Java System#getProperties 实现：  名称"systemProperties"，对应的内容 System.getProperties()
Java System#getenv 实现(环境变量）：  名称"systemEnvironment"，对应的内容 System.getProperties()
Environment 允许出现同名的配置，不过优先级高的胜出，

关于 Spring Boot 优先级顺序，可以参考：
https://docs.spring.io/spring-boot/docs/2.0.0.BUILD-SNAPSHOT/reference/htmlsingle/#boot-features-external-config
```

PropertySourceBootstrapConfiguration.initialize()

```java
@Override
public void initialize(ConfigurableApplicationContext applicationContext) {
   CompositePropertySource composite = new CompositePropertySource(
         BOOTSTRAP_PROPERTY_SOURCE_NAME);
    //优先级 源码 ~~ 取决于Order 这个接口 @Order
   AnnotationAwareOrderComparator.sort(this.propertySourceLocators);
   boolean empty = true;
   ConfigurableEnvironment environment = applicationContext.getEnvironment();
   for (PropertySourceLocator locator : this.propertySourceLocators) {
      PropertySource<?> source = null;
      source = locator.locate(environment);
      if (source == null) {
         continue;
      }
      logger.info("Located property source: " + source);
      composite.addPropertySource(source);
      empty = false;
   }
   if (!empty) {
      MutablePropertySources propertySources = environment.getPropertySources();
      String logConfig = environment.resolvePlaceholders("${logging.config:}");
      LogFile logFile = LogFile.get(environment);
      if (propertySources.contains(BOOTSTRAP_PROPERTY_SOURCE_NAME)) {
         propertySources.remove(BOOTSTRAP_PROPERTY_SOURCE_NAME);
      }
      insertPropertySources(propertySources, composite);
      reinitializeLoggingSystem(environment, logConfig, logFile);
      setLogLevels(environment);
      handleIncludedProfiles(environment);
   }
}
```

##### environment

SpringApplication.run()

```java
ConfigurableEnvironment environment = prepareEnvironment(listeners,
      applicationArguments);
```

-> SpringApplication.prepareEnvironment()

```java
private ConfigurableEnvironment prepareEnvironment(
      SpringApplicationRunListeners listeners,
      ApplicationArguments applicationArguments) {
   // Create and configure the environment
    //创建的environment有三种：StandardServletEnvironment \StandardReactiveWebEnvironment \StandardEnvironment
   ConfigurableEnvironment environment = getOrCreateEnvironment();
    //添加配置信息，defaultproperty 和 runline命令操作的配置信息（cli）
    // SpringApplicationBuilder().profiles("test")指定激活的profiles
   configureEnvironment(environment, applicationArguments.getSourceArgs());
    //触发ApplicationEnvironmentPreparedEvent事件的监听器
   listeners.environmentPrepared(environment);
    //将environment绑定到启动类springapplication
   bindToSpringApplication(environment);
   if (!this.isCustomEnvironment) {
      environment = new EnvironmentConverter(getClassLoader())
            .convertEnvironmentIfNecessary(environment, deduceEnvironmentClass());
   }
    //environment的MutablePropertySources中添加名为configurationProperties的ConfigurationPropertySourcesPropertySource
   ConfigurationPropertySources.attach(environment);
   return environment;
}
```

->在上面的步骤中触发了ApplicationEnvironmentPreparedEvent的监听器，其中就有application.properties的ConfigFileApplicationListener监听器。

##### 以redis为例 

按自己的配置来重写微服务的（ECO）远程配置

```java
1，redis的配置信息怎么解析到redisConnectionFactory(JedisConnectionFactory实现类)中？
RedisAutoConfiguration 获取配置
->其实就是解析@ConfigurationProperties注解
->ConfigurationPropertiesBindingPostProcessor.postProcessBeforeInitialization()解析
  ->PropertiesConfigurationFactory.bindPropertiesToTarget()
    ->PropertiesConfigurationFactory.doBindPropertiesToTarget()解析prefix以及绑定evironment中的propertySource。propertySource是有顺序的，key一旦绑定就不会在取获取其他的propertySource的key的value。   
->redisConnectionFactory 生成redis客户端

2，配置信息从哪儿取来的？
->SpringApplication.run()
    ->SpringApplication.prepareContext()
    ->SpringApplication.applyInitializers() 遍历ApplicationContextInitializer接口的实现类
    ->PropertySourceBootstrapConfiguration.initialize()方法，这里要遍历了PropertySourceLocator的所有实现类 ，其中ConfigServicePropertySourceLocator就是自定义的配置添加器 （这个类的初始化源自BootstrapConfiguration的SPI实现）

3，怎么调整本地的信息，屏蔽掉远程的信息？
3.1，添加配置文件处理插件
/**
 * @author lqd
 * @DATE 2019/3/28
 * @Description 取本地配置 - 用于自定义的配置项
 */
@ConditionalOnProperty(name="aihomework.localproperty.enabled",havingValue = "true")
@Configuration
@Order(-1)
public class MyPropertySourceLocator implements PropertySourceLocator,InitializingBean
{
    @Override
    public PropertySource<?> locate(Environment environment) {
        CompositePropertySource compositepropertySource = new CompositePropertySource("mysource");
        Map<String, Object> source = new HashMap<>();
        source.put("spring.redis.cluster.nodes","192.168.102.241:6379");
        source.put("spring.redis.password","");
        MapPropertySource mapPropertySource = new MapPropertySource("source",source);
        compositepropertySource.addFirstPropertySource(mapPropertySource);
        return compositepropertySource;
    }

    @Override
    public void afterPropertiesSet() throws Exception {
        System.out.println("MyPropertySourceLocator#init()after");
    }
}

3.2，添加配置spring.factories
org.springframework.cloud.bootstrap.BootstrapConfiguration=\
  com.tianwen.springcloud.microservice.aihomework.config.MyPropertySourceLocator
 
3.3，使用Command line方式注入参数 
--aihomework.localproperty.enabled=true

参数为什么不加到配置文件中？    

PropertySourceLocator怎么加入到PropertySourceBootstrapConfiguration的数组对象？
---
请注意：PropertySourceBootstrapConfiguration#propertySourceLocators的定义的注入标签。只不过这里是PropertySourceLocator的list数组，根据类型依赖注入。
@Autowired(required = false)
private List<PropertySourceLocator> propertySourceLocators = new ArrayList<>();


    
```

PropertiesConfigurationFactory.doBindPropertiesToTarget()

```java
private void doBindPropertiesToTarget() throws BindException {
   RelaxedDataBinder dataBinder = (this.targetName != null
         ? new RelaxedDataBinder(this.target, this.targetName)
         : new RelaxedDataBinder(this.target));
   if (this.validator != null
         && this.validator.supports(dataBinder.getTarget().getClass())) {
      dataBinder.setValidator(this.validator);
   }
   if (this.conversionService != null) {
      dataBinder.setConversionService(this.conversionService);
   }
   dataBinder.setAutoGrowCollectionLimit(Integer.MAX_VALUE);
   dataBinder.setIgnoreNestedProperties(this.ignoreNestedProperties);
   dataBinder.setIgnoreInvalidFields(this.ignoreInvalidFields);
   dataBinder.setIgnoreUnknownFields(this.ignoreUnknownFields);
   customizeBinder(dataBinder);
   Iterable<String> relaxedTargetNames = getRelaxedTargetNames();
   Set<String> names = getNames(relaxedTargetNames);
    //获取propertySource集合
   PropertyValues propertyValues = getPropertySourcesPropertyValues(names,
         relaxedTargetNames);
    //绑定key的value值
   dataBinder.bind(propertyValues);
   if (this.validator != null) {
      dataBinder.validate();
   }
   checkForBindingErrors(dataBinder);
}
```

AbstractAutowireCapableBeanFactory.doCreateBean()

```java
protected Object doCreateBean(final String beanName, final RootBeanDefinition mbd, final Object[] args)
      throws BeanCreationException {

   // Instantiate the bean.
   BeanWrapper instanceWrapper = null;
   if (mbd.isSingleton()) {
      instanceWrapper = this.factoryBeanInstanceCache.remove(beanName);
   }
   if (instanceWrapper == null) {
      instanceWrapper = createBeanInstance(beanName, mbd, args);
   }
   final Object bean = (instanceWrapper != null ? instanceWrapper.getWrappedInstance() : null);
   Class<?> beanType = (instanceWrapper != null ? instanceWrapper.getWrappedClass() : null);
   mbd.resolvedTargetType = beanType;

   // Allow post-processors to modify the merged bean definition.
   synchronized (mbd.postProcessingLock) {
      if (!mbd.postProcessed) {
         try {
             //找到@autowire标签
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
      if (logger.isDebugEnabled()) {
         logger.debug("Eagerly caching bean '" + beanName +
               "' to allow for resolving potential circular references");
      }
      addSingletonFactory(beanName, new ObjectFactory<Object>() {
         @Override
         public Object getObject() throws BeansException {
            return getEarlyBeanReference(beanName, mbd, bean);
         }
      });
   }

   // Initialize the bean instance.
   Object exposedObject = bean;
   try {
       //注入对象
      populateBean(beanName, mbd, instanceWrapper);
      if (exposedObject != null) {
         exposedObject = initializeBean(beanName, exposedObject, mbd);
      }
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
            Set<String> actualDependentBeans = new LinkedHashSet<String>(dependentBeans.length);
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

@Autowired依赖注入核心代码：InjectionMetadata.inject()

```java
public void inject(Object target, String beanName, PropertyValues pvs) throws Throwable {
   Collection<InjectedElement> elementsToIterate =
         (this.checkedElements != null ? this.checkedElements : this.injectedElements);
   if (!elementsToIterate.isEmpty()) {
      boolean debug = logger.isDebugEnabled();
      for (InjectedElement element : elementsToIterate) {
         if (debug) {
            logger.debug("Processing injected element of bean '" + beanName + "': " + element);
         }
         element.inject(target, beanName, pvs);
      }
   }
}
```

DefaultListableBeanFactory.doResolveDependency()

```java
public Object doResolveDependency(DependencyDescriptor descriptor, String beanName,
      Set<String> autowiredBeanNames, TypeConverter typeConverter) throws BeansException {

   InjectionPoint previousInjectionPoint = ConstructorResolver.setCurrentInjectionPoint(descriptor);
   try {
      Object shortcut = descriptor.resolveShortcut(this);
      if (shortcut != null) {
         return shortcut;
      }

      Class<?> type = descriptor.getDependencyType();
      Object value = getAutowireCandidateResolver().getSuggestedValue(descriptor);
      if (value != null) {
         if (value instanceof String) {
            String strVal = resolveEmbeddedValue((String) value);
            BeanDefinition bd = (beanName != null && containsBean(beanName) ? getMergedBeanDefinition(beanName) : null);
            value = evaluateBeanDefinitionString(strVal, bd);
         }
         TypeConverter converter = (typeConverter != null ? typeConverter : getTypeConverter());
         return (descriptor.getField() != null ?
               converter.convertIfNecessary(value, type, descriptor.getField()) :
               converter.convertIfNecessary(value, type, descriptor.getMethodParameter()));
      }

      Object multipleBeans = resolveMultipleBeans(descriptor, beanName, autowiredBeanNames, typeConverter);
      if (multipleBeans != null) {
         return multipleBeans;
      }

      Map<String, Object> matchingBeans = findAutowireCandidates(beanName, type, descriptor);
      if (matchingBeans.isEmpty()) {
         if (descriptor.isRequired()) {
            raiseNoMatchingBeanFound(type, descriptor.getResolvableType(), descriptor);
         }
         return null;
      }

      String autowiredBeanName;
      Object instanceCandidate;

      if (matchingBeans.size() > 1) {
         autowiredBeanName = determineAutowireCandidate(matchingBeans, descriptor);
         if (autowiredBeanName == null) {
            if (descriptor.isRequired() || !indicatesMultipleBeans(type)) {
               return descriptor.resolveNotUnique(type, matchingBeans);
            }
            else {
               // In case of an optional Collection/Map, silently ignore a non-unique case:
               // possibly it was meant to be an empty collection of multiple regular beans
               // (before 4.3 in particular when we didn't even look for collection beans).
               return null;
            }
         }
         instanceCandidate = matchingBeans.get(autowiredBeanName);
      }
      else {
         // We have exactly one match.
         Map.Entry<String, Object> entry = matchingBeans.entrySet().iterator().next();
         autowiredBeanName = entry.getKey();
         instanceCandidate = entry.getValue();
      }

      if (autowiredBeanNames != null) {
         autowiredBeanNames.add(autowiredBeanName);
      }
      return (instanceCandidate instanceof Class ?
            descriptor.resolveCandidate(autowiredBeanName, type, this) : instanceCandidate);
   }
   finally {
      ConstructorResolver.setCurrentInjectionPoint(previousInjectionPoint);
   }
}
```

