##### 参考文档

https://blog.csdn.net/qq_34288630/article/details/79097913

<https://blog.51cto.com/snowtiger/2059691>

<https://github.com/Netflix/Hystrix/wiki/How-To-Use>

<https://www.javazhiyin.com/25952.html>

##### HystrixCommandProperties

关键属性，

```
HystrixCommandProperties
```

##### HystrixCommandAspect

切面，hystrix的注解。

```

```

##### HystrixConcurrencyStrategy

将指定的传参传递到hystrix的线程隔离策略的线程中

```
package com.tianwen.springcloud.microservice.hystrix;

import com.netflix.hystrix.HystrixThreadPoolKey;
import com.netflix.hystrix.strategy.HystrixPlugins;
import com.netflix.hystrix.strategy.concurrency.HystrixConcurrencyStrategy;
import com.netflix.hystrix.strategy.concurrency.HystrixRequestVariable;
import com.netflix.hystrix.strategy.concurrency.HystrixRequestVariableLifecycle;
import com.netflix.hystrix.strategy.eventnotifier.HystrixEventNotifier;
import com.netflix.hystrix.strategy.executionhook.HystrixCommandExecutionHook;
import com.netflix.hystrix.strategy.metrics.HystrixMetricsPublisher;
import com.netflix.hystrix.strategy.properties.HystrixPropertiesStrategy;
import com.netflix.hystrix.strategy.properties.HystrixProperty;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.context.request.RequestAttributes;
import org.springframework.web.context.request.RequestContextHolder;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.Callable;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/**
 * @program: FeignHystrixConcurrencyStrategy
 * @description: 更改Hystrix并发处理策略（将现有的并发策略作为新并发策略的成员变量，在新并发策略中，返回现有并发策略的线程池、Queue。）
 * @author: luqihang
 * @date: 2019/10/24 20:07
 */
@Component
public class FeignHystrixConcurrencyStrategy extends HystrixConcurrencyStrategy {
    private static final Logger log = LoggerFactory.getLogger(FeignHystrixConcurrencyStrategy.class);

    private HystrixConcurrencyStrategy delegate;

    public FeignHystrixConcurrencyStrategy() {
        try {
            this.delegate = HystrixPlugins.getInstance().getConcurrencyStrategy();
            if (this.delegate instanceof FeignHystrixConcurrencyStrategy) {
                // Welcome to singleton hell...
                return;
            }
            HystrixCommandExecutionHook commandExecutionHook = HystrixPlugins.getInstance().getCommandExecutionHook();
            HystrixEventNotifier eventNotifier = HystrixPlugins.getInstance().getEventNotifier();
            HystrixMetricsPublisher metricsPublisher = HystrixPlugins.getInstance().getMetricsPublisher();
            HystrixPropertiesStrategy propertiesStrategy = HystrixPlugins.getInstance().getPropertiesStrategy();
            this.logCurrentStateOfHystrixPlugins(eventNotifier, metricsPublisher, propertiesStrategy);
            HystrixPlugins.reset();
            HystrixPlugins.getInstance().registerConcurrencyStrategy(this);
            HystrixPlugins.getInstance().registerCommandExecutionHook(commandExecutionHook);
            HystrixPlugins.getInstance().registerEventNotifier(eventNotifier);
            HystrixPlugins.getInstance().registerMetricsPublisher(metricsPublisher);
            HystrixPlugins.getInstance().registerPropertiesStrategy(propertiesStrategy);
        } catch (Exception e) {
            log.error("Failed to register Sleuth Hystrix Concurrency Strategy", e);
        }
    }

    private void logCurrentStateOfHystrixPlugins(HystrixEventNotifier eventNotifier,
                                                 HystrixMetricsPublisher metricsPublisher, HystrixPropertiesStrategy propertiesStrategy) {
        if (log.isDebugEnabled()) {
            log.debug("Current Hystrix plugins configuration is [" + "concurrencyStrategy [" + this.delegate + "],"
                    + "eventNotifier [" + eventNotifier + "]," + "metricPublisher [" + metricsPublisher + "],"
                    + "propertiesStrategy [" + propertiesStrategy + "]," + "]");
            log.debug("Registering Sleuth Hystrix Concurrency Strategy.");
        }
    }

    @Override
    public <T> Callable<T> wrapCallable(Callable<T> callable) {
        RequestAttributes requestAttributes = RequestContextHolder.getRequestAttributes();
        return new WrappedCallable<>(callable, requestAttributes);
    }

    @Override
    public ThreadPoolExecutor getThreadPool(HystrixThreadPoolKey threadPoolKey, HystrixProperty<Integer> corePoolSize,
                                            HystrixProperty<Integer> maximumPoolSize, HystrixProperty<Integer> keepAliveTime, TimeUnit unit,
                                            BlockingQueue<Runnable> workQueue) {
        return this.delegate
                .getThreadPool(threadPoolKey, corePoolSize, maximumPoolSize, keepAliveTime, unit, workQueue);
    }

    // @Override
    // public ThreadPoolExecutor getThreadPool(HystrixThreadPoolKey threadPoolKey,
    // HystrixThreadPoolProperties threadPoolProperties)
    // {
    // return this.delegate.getThreadPool(threadPoolKey, threadPoolProperties);
    // }

    @Override
    public BlockingQueue<Runnable> getBlockingQueue(int maxQueueSize) {
        return this.delegate.getBlockingQueue(maxQueueSize);
    }

    @Override
    public <T> HystrixRequestVariable<T> getRequestVariable(HystrixRequestVariableLifecycle<T> rv) {
        return this.delegate.getRequestVariable(rv);
    }

    static class WrappedCallable<T> implements Callable<T> {

        private final Callable<T> target;

        private final RequestAttributes requestAttributes;

        public WrappedCallable(Callable<T> target, RequestAttributes requestAttributes) {
            this.target = target;
            this.requestAttributes = requestAttributes;
        }

        @Override
        public T call()
                throws Exception {
            try {
                RequestContextHolder.setRequestAttributes(requestAttributes);
                return target.call();
            } finally {
                RequestContextHolder.resetRequestAttributes();
            }
        }
    }
}
```

##### hystrix执行方式的同步、异步、观察

```
package com.tianwen.springcloud.openapi.service;

import com.netflix.hystrix.contrib.javanica.annotation.HystrixCommand;
import com.netflix.hystrix.contrib.javanica.command.AsyncResult;
import com.tianwen.springcloud.microservice.entity.WorkPublish;
import org.springframework.stereotype.Service;
import rx.Subscriber;

import java.util.concurrent.Future;

/**
 * @program: aihomework
 * @description: Demo
 * @author: Mr.LQDing
 * @create: 2019-11-07 15:03
 **/
@Service
public class DemoService {

    @HystrixCommand(fallbackMethod = "getWorkPublishFallBack")
    public Future<WorkPublish> getWorkPublish()
    {
        return new AsyncResult<WorkPublish>() {
            @Override
            public WorkPublish invoke() {
                System.out.println("111111111");
                return new WorkPublish();
            }
        };
    }

    @HystrixCommand(fallbackMethod = "getWorkPublishFallBack")
    public rx.Observable<WorkPublish> getWorkPublishByObserve()
    {
        return rx.Observable.create(new rx.Observable.OnSubscribe<WorkPublish>() {
            @Override
            public void call(Subscriber<? super WorkPublish> subscriber) {
                System.out.println("2222222");
                if (!subscriber.isUnsubscribed())
                {
                    subscriber.onNext(new WorkPublish());
                    subscriber.onCompleted();
                }
            }
        });
    }

    public WorkPublish getWorkPublishFallBack()
    {
        return new WorkPublish();
    }
}
```

源码：

```
public static Object execute(HystrixInvokable invokable, ExecutionType executionType, MetaHolder metaHolder) throws RuntimeException {
    Validate.notNull(invokable);
    Validate.notNull(metaHolder);

    switch (executionType) {
        case SYNCHRONOUS: {
            return castToExecutable(invokable, executionType).execute();
        }
        case ASYNCHRONOUS: {
            HystrixExecutable executable = castToExecutable(invokable, executionType);
            if (metaHolder.hasFallbackMethodCommand()
                    && ExecutionType.ASYNCHRONOUS == metaHolder.getFallbackExecutionType()) {
                return new FutureDecorator(executable.queue());
            }
            return executable.queue();
        }
        case OBSERVABLE: {
            HystrixObservable observable = castToObservable(invokable);
            return ObservableExecutionMode.EAGER == metaHolder.getObservableExecutionMode() ? observable.observe() : observable.toObservable();
        }
        default:
            throw new RuntimeException("unsupported execution type: " + executionType);
    }
}
```

##### HystrixContextScheduler 、ScheduledAction、HystrixContexSchedulerAction、SleuthHystrixConcurrencyStrategy

执行调度的具体方法。

```
 private static class ThreadPoolWorker extends Worker {

        private final HystrixThreadPool threadPool;
        private final CompositeSubscription subscription = new CompositeSubscription();
        private final Func0<Boolean> shouldInterruptThread;

        public ThreadPoolWorker(HystrixThreadPool threadPool, Func0<Boolean> shouldInterruptThread) {
            this.threadPool = threadPool;
            this.shouldInterruptThread = shouldInterruptThread;
        }

        @Override
        public void unsubscribe() {
            subscription.unsubscribe();
        }

        @Override
        public boolean isUnsubscribed() {
            return subscription.isUnsubscribed();
        }

        @Override
        public Subscription schedule(final Action0 action) {
            if (subscription.isUnsubscribed()) {
                // don't schedule, we are unsubscribed
                return Subscriptions.unsubscribed();
            }

            // This is internal RxJava API but it is too useful.
            ScheduledAction sa = new ScheduledAction(action);
            
            subscription.add(sa);
            sa.addParent(subscription);

//重点
            Future<?> f = threadPool.getExecutor().submit(sa);
            sa.add(new FutureCompleterWithConfigurableInterrupt(f, shouldInterruptThread));

            return sa;
        }

        @Override
        public Subscription schedule(Action0 action, long delayTime, TimeUnit unit) {
            throw new IllegalStateException("Hystrix does not support delayed scheduling");
        }

    }
```