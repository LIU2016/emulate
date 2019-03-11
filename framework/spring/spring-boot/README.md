[TOC]

参考文档：

http://projects.spring.io/spring-boot/

https://gitter.im

https://docs.spring.io/spring-boot/docs/2.1.1.RELEASE/api/

https://docs.spring.io/spring-boot

# SpringApplication

启动方式

SpringApplication

```
SpringApplication sp= new SpringApplication();
Map properties=new LinkedHashMap();
sp.setDefaultProperties(properties);
sp.,run(args);
```

配置Spring boot源

```
new SpringApplicationBuilder(this).properties("server.port=0").run(args);
```

SpringApplication类型推断

```
SpringApplication Spring Boot 驱动 Spring 应用上下文的引导类
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = {
        @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class),
        @Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })
public @interface SpringBootApplication {
    ...
}
@ComponentScan: 它是版本引入的？ Spring Framework 3.1
@EnableAutoConfiguration: 激活自动装配 @Enable -> @Enable 开头的
@EnableWebMvc
@EnableTransactionManagement
@EnableAspectJAutoProxy
@EnableAsync
@SpringBootConfiguration : 等价于 @Configuration -> Configuration Class 注解
@Component 的“派生性”
@Component -> @ComponentScan
处理类 -> ConfigurationClassParser
扫描类 -> 
ClassPathBeanDefinitionScanner
ClassPathScanningCandidateComponentProvider
    protected void registerDefaultFilters() {
        this.includeFilters.add(new AnnotationTypeFilter(Component.class));
        ...
    }
Dubbo @Service -> 2.5.7 -> new AnnotationTypeFilter(Service.class);
```

Spring boot事件

# spring boot特性



# spring boot异常处理

## SpringApplication引入不了，怎么办？

这是maven引入jar包失败导致，需要删除本地资源库的spring的boot目录，重新拉。



# spring boot新加入的常用注解

## Bean 单例注入

### @Bean方式

1、在SpringBootApplication中添加@Bean,返回实例对象即可

```java 
package cn.com.showclear.plan.impl.plan;

/**

- 测试
  *

- @author YF-XIACHAOYANG

- @date 2017/12/13 18:04
  */
  public class TestBean {

  private String name;

  /*可以自定义构造器*/
  public TestBean(String name) {
      this.name = name;
  }

  public String getName() {
      return name;
  }

  public TestBean setName(String name) {
     this.name = name;
      return this;
  }

  public void hello() {
     System.out.println(this.name);
  }
  }
```

2，@Bean注入

~~~java 
package cn.com.showclear.config;

@SpringBootApplication
@ComponentScan(basePackages = "cn.com.showclear")
@EnableScheduling
public class WebMvcConfig {

```
...
 
@Bean
public TestBean getTestBean() {
    return new TestBean("hello bean1!");
}

}
~~~

3、使用@Autowired引用TestBean

``` java
@RestController
@RequestMapping("/data/plan/config/")
public class PlanConfigController {
@Autowired
private TestBean testBean;

 /**
 * 加载预案应急事件标签组[含有组内标签信息]
 *
 * @return
 */
@RequestMapping(value = "loadTagGroupList", method = RequestMethod.POST)
public RespMapJson loadTagGroupList(String groupName) {
    testBean.hello();
    return planConfigService.load(planHandleDeliver.getTagConfigHandle().init(this, groupName));
}
```