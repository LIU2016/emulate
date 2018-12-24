[TOC]

参考文档：

http://projects.spring.io/spring-boot/

https://gitter.im

https://docs.spring.io/spring-boot/docs/2.1.1.RELEASE/api/

https://docs.spring.io/spring-boot

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