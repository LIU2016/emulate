spring全家桶的顶级接口

```java
1,BeanPostProcessor：可以在前置和后置处理方法中修饰所有的Bean 。

2,BeanFactoryPostProcessor:可以用来修改所有bean的beandefinition 。
->AbstractApplicationContext.refresh()
	->AbstractApplicationContext.invokeBeanFactoryPostProcessors(beanFactory)
	->PostProcessorRegistrationDelegate.invokeBeanFactoryPostProcessors()
    
3,Ordered、PriorityOrdered:list中的排序优先级

4,BeanDefinition,BeanFactory,Aware,applicationLister,applicationEvent,ApplicationContext 
    
```

```java
/**
 * Invoke the given BeanFactoryPostProcessor beans.
 */
private static void invokeBeanFactoryPostProcessors(
      Collection<? extends BeanFactoryPostProcessor> postProcessors, ConfigurableListableBeanFactory beanFactory) {

   for (BeanFactoryPostProcessor postProcessor : postProcessors) {
      postProcessor.postProcessBeanFactory(beanFactory);
   }
}
```