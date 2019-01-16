# Spring 事件

## spring event 应用实例

第一步，新建事件

```java
package com.lqd.event;

import org.springframework.context.ApplicationEvent;

/**
 * @author lqd
 * @DATE 2018/12/24
 * @Description xxxxx
 */
public class MyEvent extends ApplicationEvent
{
    private String name ;
    /**
     * Create a new ApplicationEvent.
     *
     * @param source the object on which the event initially occurred (never {@code null})
     */
    public MyEvent(Object source,String name) {
        super(source);
        this.name = name ;
    }

    public void say()
    {
        System.out.println(name);
    }
}
```

第二步，新建监听

```java
package com.lqd.event;

import org.springframework.context.ApplicationListener;
import org.springframework.stereotype.Service;

/**
 * @author lqd
 * @DATE 2018/12/24
 * @Description xxxxx
 */
@Service
public class MyEventListener implements ApplicationListener<MyEvent>
{
    @Override
    public void onApplicationEvent(MyEvent event) {

        event.say();
    }
}
```

第三步，调用的时候向容器中推事件

```java
package com.lqd.event;

import org.springframework.context.ApplicationEvent;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.ApplicationEventPublisherAware;
import org.springframework.stereotype.Service;

/**
 * @author lqd
 * @DATE 2018/12/24
 * @Description xxxxx
 */
@Service
public class MyEventService implements ApplicationEventPublisherAware
{
    ApplicationEventPublisher applicationEventPublisher ;

    public void sendEventToListener()
    {
        applicationEventPublisher.publishEvent(new MyEvent(this,"spring event"));
    }

    @Override
    public void setApplicationEventPublisher(ApplicationEventPublisher applicationEventPublisher)
    {
        this.applicationEventPublisher = applicationEventPublisher ;
    }
}
```

## 源码分析

### 监听器注入

#### SimpleApplicationEventMulticaster

其父类AbstractApplicationEventMulticaster添加监听器，以便后面处理事件。

```java
@Override
public void addApplicationListener(ApplicationListener<?> listener) {
   synchronized (this.retrievalMutex) {
      // Explicitly remove target for a proxy, if registered already,
      // in order to avoid double invocations of the same listener.
      Object singletonTarget = AopProxyUtils.getSingletonTarget(listener);
      if (singletonTarget instanceof ApplicationListener) {
         this.defaultRetriever.applicationListeners.remove(singletonTarget);
      }
      this.defaultRetriever.applicationListeners.add(listener);
      this.retrieverCache.clear();
   }
}
```

从哪里调用这个方法的？

还是我们的监听器在初始化的时候，依赖注入之前（注册到容器的时候），在ApplicationListenerDetector中处理。这个类实现了BeanPostProcessor方法。

```java
@Override
public Object postProcessAfterInitialization(Object bean, String beanName) {
   if (bean instanceof ApplicationListener) {
      // potentially not detected as a listener by getBeanNamesForType retrieval
      Boolean flag = this.singletonNames.get(beanName);
      if (Boolean.TRUE.equals(flag)) {
         // singleton bean (top-level or inner): register on the fly
         this.applicationContext.addApplicationListener((ApplicationListener<?>) bean);
      }
      else if (Boolean.FALSE.equals(flag)) {
         if (logger.isWarnEnabled() && !this.applicationContext.containsBean(beanName)) {
            // inner bean with other scope - can't reliably process events
            logger.warn("Inner bean '" + beanName + "' implements ApplicationListener interface " +
                  "but is not reachable for event multicasting by its containing ApplicationContext " +
                  "because it does not have singleton scope. Only top-level listener beans are allowed " +
                  "to be of non-singleton scope.");
         }
         this.singletonNames.remove(beanName);
      }
   }
   return bean;
}
```

### 事件触发后执行监听器的方法

```java
package com.lqd.event;

import org.springframework.context.ApplicationEvent;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.ApplicationEventPublisherAware;
import org.springframework.stereotype.Service;

/**
 * @author lqd
 * @DATE 2018/12/24
 * @Description xxxxx
 */
@Service
public class MyEventService implements ApplicationEventPublisherAware
{
    ApplicationEventPublisher applicationEventPublisher ;

    public void sendEventToListener()
    {
        applicationEventPublisher.publishEvent(new MyEvent(this,"spring event"));
    }

    @Override
    public void setApplicationEventPublisher(ApplicationEventPublisher applicationEventPublisher)
    {
        this.applicationEventPublisher = applicationEventPublisher ;
    }
}
```

入口ApplicationEventPublisher的publishEvent方法。通过遍历监听器的集合。

```java
/**
 * Publish the given event to all listeners.
 * @param event the event to publish (may be an {@link ApplicationEvent}
 * or a payload object to be turned into a {@link PayloadApplicationEvent})
 * @param eventType the resolved event type, if known
 * @since 4.2
 */
protected void publishEvent(Object event, @Nullable ResolvableType eventType) {
   Assert.notNull(event, "Event must not be null");

   // Decorate event as an ApplicationEvent if necessary
   ApplicationEvent applicationEvent;
   if (event instanceof ApplicationEvent) {
      applicationEvent = (ApplicationEvent) event;
   }
   else {
      applicationEvent = new PayloadApplicationEvent<>(this, event);
      if (eventType == null) {
         eventType = ((PayloadApplicationEvent) applicationEvent).getResolvableType();
      }
   }

   // Multicast right now if possible - or lazily once the multicaster is initialized
   if (this.earlyApplicationEvents != null) {
      this.earlyApplicationEvents.add(applicationEvent);
   }
   else {
      getApplicationEventMulticaster().multicastEvent(applicationEvent, eventType);
   }

   // Publish event via parent context as well...
   if (this.parent != null) {
      if (this.parent instanceof AbstractApplicationContext) {
         ((AbstractApplicationContext) this.parent).publishEvent(event, eventType);
      }
      else {
         this.parent.publishEvent(event);
      }
   }
}
```

这时要回到了SimpleApplicationEventMulticaster查找监听器的集合去匹配事件，并执行监听器的事件执行方法。

```java
@Override
public void multicastEvent(final ApplicationEvent event, @Nullable ResolvableType eventType) {
   ResolvableType type = (eventType != null ? eventType : resolveDefaultEventType(event));
   for (final ApplicationListener<?> listener : getApplicationListeners(event, type)) {
      Executor executor = getTaskExecutor();
      if (executor != null) {
         executor.execute(() -> invokeListener(listener, event));
      }
      else {
         invokeListener(listener, event);
      }
   }
}

/**
	 * Invoke the given listener with the given event.
	 * @param listener the ApplicationListener to invoke
	 * @param event the current event to propagate
	 * @since 4.1
	 */
	protected void invokeListener(ApplicationListener<?> listener, ApplicationEvent event) {
		ErrorHandler errorHandler = getErrorHandler();
		if (errorHandler != null) {
			try {
				doInvokeListener(listener, event);
			}
			catch (Throwable err) {
				errorHandler.handleError(err);
			}
		}
		else {
			doInvokeListener(listener, event);
		}
	}

@SuppressWarnings({"unchecked", "rawtypes"})
	private void doInvokeListener(ApplicationListener listener, ApplicationEvent event) {
		try {
			listener.onApplicationEvent(event);
		}
		catch (ClassCastException ex) {
			String msg = ex.getMessage();
			if (msg == null || matchesClassCastMessage(msg, event.getClass())) {
				// Possibly a lambda-defined listener which we could not resolve the generic event type for
				// -> let's suppress the exception and just log a debug message.
				Log logger = LogFactory.getLog(getClass());
				if (logger.isDebugEnabled()) {
					logger.debug("Non-matching event type for listener: " + listener, ex);
				}
			}
			else {
				throw ex;
			}
		}
	}

```

