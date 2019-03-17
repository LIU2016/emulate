### 第一节 SpringApplication

通过现象找本质（源码）

#### 启动的方式

``` java
public static void main(String[] args) {

		//SpringApplication.run(MicroserviceProjectApplication.class, args);

		//fluent api模式 - 编程的模式
		/*new SpringApplicationBuilder(MicroserviceProjectApplication.class)
				//单元测试，PORT随机
				.properties("server.port=0")
				.run(args);*/

		//
		SpringApplication springApplication =
				new SpringApplication(MicroserviceProjectApplication.class);
		final Map<String,Object> map = new LinkedHashMap<>(1);
		map.put("server.port",0);
		springApplication.setDefaultProperties(map);
		//springApplication.setWebApplicationType(WebApplicationType.NONE);
		ConfigurableApplicationContext configurableApplicationContext =springApplication.run(args);
		//System.out.println(configurableApplicationContext.getBean(MicroserviceProjectApplication.class));

	}
```

#### 注解的派生性

##### 以@Component为例

```java 
1,@Component --> @ComponentScan
    @Service \ @Controller \ @configuration \ @Respository   
    
2,ComponentScanAnnotationParser.parse
	ClassPathBeanDefinitionScanner --> ClassPathScanningCandidateComponentProvider	
(
AnnotationConfigApplicationContext
#refresh()#invokeBeanFactoryPostProcessors(beanFactory);
)

3,自定义@MyService 
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

了解观察者模式	

目的

``` java
1，ApplicationEventMulticaster 加载或者初始化组件
2，spring上下文生命周期控制 注解驱动Bean
```

要理解下面的内容，首先要有了解到一个事件周期：1，定义事件；2，注册监听；3，发布事件 。

```
ApplicationEvent：应用事件
ApplicationListener：应用监听器
具体参考springframework的event
```

##### application.properties的读取

（ConfigFileApplicationListener -> onApplicationEvent）

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
```