#### 操作eureka的实例

```
PeerAwareInstanceRegistry、SpringClientFactory
------------------------------------------------------
package com.twasp.eureka.serviceImpl;

import com.google.common.collect.Lists;
import com.netflix.appinfo.InstanceInfo;
import com.netflix.discovery.shared.Application;
import com.netflix.eureka.registry.PeerAwareInstanceRegistry;
import com.netflix.loadbalancer.Server;
import com.twasp.common.dto.InstanceInfoDTO;
import com.twasp.common.dto.ResponseDTO;
import com.twasp.common.utils.StringUtils;
import com.twasp.eureka.exception.ApiException;
import com.twasp.eureka.instance.GeneralInstance;
import com.twasp.eureka.instance.InstanceVO;
import com.twasp.eureka.service.EurekaService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.cloud.netflix.eureka.serviceregistry.EurekaRegistration;
import org.springframework.cloud.netflix.eureka.serviceregistry.EurekaServiceRegistry;
import org.springframework.cloud.netflix.ribbon.SpringClientFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;

/**
 * @author motorfu
 * @since 2017/8/6 19:02
 */
@Service
@RefreshScope
public class EurekaServiceImpl implements EurekaService {

  private final static Logger LOGGER = LoggerFactory.getLogger(EurekaServiceImpl.class);

  @Autowired
  private EurekaServiceRegistry eurekaServiceRegistry;

  @Autowired
  private EurekaRegistration registration;

  @Autowired
  private PeerAwareInstanceRegistry registry;

  @Autowired
  private RestTemplate restTemplate;

  @Autowired
  private SpringClientFactory springClientFactory;

  @Value("${server.port}")
  private Integer port;

  @Override
  public ResponseDTO registerService(InstanceVO instanceVO) {
    InstanceInfo instanceInfo = GeneralInstance.generateInstanceInfo(instanceVO);
    if (LOGGER.isDebugEnabled()) {
      LOGGER.debug("instanceVO id={}, appname={}", instanceInfo.getId(), instanceInfo.getAppName());
    }
    InstanceInfo info = registry.getInstanceByAppAndId(instanceInfo.getAppName(), instanceInfo.getId());
    if (LOGGER.isDebugEnabled()) {
      LOGGER.debug("instanceVO info={}", info);
    }
    if (info == null) {
      registry.register(instanceInfo, 30, false);
    } else {
      registry.renew(instanceInfo.getAppName(), instanceInfo.getId(), false);
    }
    return new ResponseDTO(true, "注册成功");
  }

  @Override
  public ResponseDTO getApplications() {
    return new ResponseDTO<>(registry.getSortedApplications());
  }

  @Override
  public ResponseDTO getApplicationCount() {
    return new ResponseDTO<>(registry.getSortedApplications().size());
  }


  @Override
  public ResponseDTO<List<String>> getApplicationsNames() {
    List<Application> applications = registry.getSortedApplications();
    List<String> names = Lists.newLinkedList();
    applications.forEach(application -> names.add(application.getName().toLowerCase()));

    return new ResponseDTO<>(names);
  }

  @Override
  public ResponseDTO<List<InstanceInfo>> findInstances(String appName) {
    if (StringUtils.isEmpty(appName)) {
      throw new ApiException(400, "服务名称参数不能为空");
    }
    Application application = registry.getApplication(appName.toUpperCase());
    return new ResponseDTO<>(application.getInstances());
  }

  @Override
  public ResponseDTO<List<InstanceInfoDTO>> findSimpleInstances(String appName) {
    if (StringUtils.isEmpty(appName)) {
      throw new ApiException(400, "服务名称参数不能为空");
    }
    Application application = registry.getApplication(appName.toUpperCase());
    List<InstanceInfoDTO> instanceDTOList = Lists.newLinkedList();
    final InstanceInfoDTO[] instanceDTO = {null};
    application.getInstances().forEach(instanceInfo -> {
      instanceDTO[0] = new InstanceInfoDTO();
      instanceDTO[0].setInstanceId(instanceInfo.getInstanceId());
      instanceDTO[0].setHostName(instanceInfo.getHostName());
      instanceDTO[0].setLastUpdatedTimestamp(instanceInfo.getLastUpdatedTimestamp());
      instanceDTO[0].setStatus(instanceInfo.getStatus().name());
      instanceDTOList.add(instanceDTO[0]);
    });

    return new ResponseDTO<>(instanceDTOList);
  }

  @Override
  public ResponseDTO getInstanceCount() {
    final int[] count = {0};
    List<Application> applications = registry.getSortedApplications();
    applications.forEach(application -> {
      count[0] += application.getInstances().size();
    });
    return new ResponseDTO<>(count[0]);
  }

  @Override
  public ResponseDTO<InstanceInfo> getInstance(String appName, String instanceId) {
    LOGGER.info("appName={}, instanceId={}", appName, instanceId);
    InstanceInfo instanceInfo = registry.getInstanceByAppAndId(appName.toUpperCase(), instanceId);
    return new ResponseDTO(instanceInfo);
  }


  @Override
  public ResponseDTO<Server> findServers(String serviceId) {
    return new ResponseDTO(springClientFactory.getLoadBalancer(serviceId).getAllServers());
  }
}

```

##### eureka实例注册、取消注册的事件

```java
EurekaInstanceRegisteredEvent、EurekaInstanceCanceledEvent
----------------------------------------------------------------


```

#### Eureka获取服务器列表的流程

EurekaClientAutoConfiguration(初始化)

->CloudEurekaClient(初始化)

->DiscoveryClient

​	->fetchRegistry()方法->getAndStoreFullRegistry()方法

->MetricsCollectingEurekaHttpClient

​	->execute()方法

->EurekaHttpClientDecorator

​	->

->AbstractJerseyEurekaHttpClient

​	->getApplications()方法->getApplicationsInternal()获取eureka服务器应用实例列表

->Applications

​	->addApplication()方法保存到appNameApplicationMap中。同时将应用实例维护到virtualHostNameAppMap（按名称来）、secureVirtualHostNameAppMap（按名称来）、applications

#### Eureka刷新远程服务器列表流程

DiscoveryClient初始化构造函数的时候

​	->initScheduledTasks() 初始化所有的定时器任务->eureka.shouldFetchRegistry 为true即可。registration.enabled

```properties
#不注册到eureka服务器
eureka.registration.enabled=true
```

#### Applications

```java
private AbstractQueue<Application> applications;

private Map<String, Application> appNameApplicationMap = new ConcurrentHashMap<String, Application>();
private Map<String, AbstractQueue<InstanceInfo>> virtualHostNameAppMap = new ConcurrentHashMap<String, AbstractQueue<InstanceInfo>>();
private Map<String, AbstractQueue<InstanceInfo>> secureVirtualHostNameAppMap = new ConcurrentHashMap<String, AbstractQueue<InstanceInfo>>();
```

#### EurekaHttpClient

这是Eureka的顶级接口，用于获取服务器信息。他的实现类是MetricsCollectingEurekaHttpClient。

```java
@Override
protected <R> EurekaHttpResponse<R> execute(RequestExecutor<R> requestExecutor) {
    EurekaHttpClientRequestMetrics requestMetrics = metricsByRequestType.get(requestExecutor.getRequestType());
    Stopwatch stopwatch = requestMetrics.latencyTimer.start();
    try {
        EurekaHttpResponse<R> httpResponse = requestExecutor.execute(delegate);
        requestMetrics.countersByStatus.get(mappedStatus(httpResponse)).increment();
        return httpResponse;
    } catch (Exception e) {
        requestMetrics.connectionErrors.increment();
        exceptionsMetric.count(e);
        throw e;
    } finally {
        stopwatch.stop();
    }
}
```

#### EurekaClientAutoConfiguration

CloudEurekaClient就是从这里实例化的，主要操作在他的父类DiscoveryClient。

```java
/*
 * Copyright 2013-2014 the original author or authors.
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

package org.springframework.cloud.netflix.eureka;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.AutoConfigureAfter;
import org.springframework.boot.autoconfigure.AutoConfigureBefore;
import org.springframework.boot.autoconfigure.condition.AnyNestedCondition;
import org.springframework.boot.autoconfigure.condition.ConditionalOnBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.autoconfigure.condition.SearchStrategy;
import org.springframework.boot.bind.RelaxedPropertyResolver;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.cloud.autoconfigure.RefreshAutoConfiguration;
import org.springframework.cloud.client.CommonsClientAutoConfiguration;
import org.springframework.cloud.client.actuator.HasFeatures;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.cloud.client.discovery.noop.NoopDiscoveryClientAutoConfiguration;
import org.springframework.cloud.client.serviceregistry.AutoServiceRegistrationProperties;
import org.springframework.cloud.client.serviceregistry.ServiceRegistryAutoConfiguration;
import org.springframework.cloud.commons.util.InetUtils;
import org.springframework.cloud.context.scope.refresh.RefreshScope;
import org.springframework.cloud.netflix.eureka.serviceregistry.EurekaAutoServiceRegistration;
import org.springframework.cloud.netflix.eureka.serviceregistry.EurekaRegistration;
import org.springframework.cloud.netflix.eureka.serviceregistry.EurekaServiceRegistry;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Conditional;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Lazy;
import org.springframework.core.env.ConfigurableEnvironment;
import org.springframework.util.StringUtils;

import com.netflix.appinfo.ApplicationInfoManager;
import com.netflix.appinfo.EurekaInstanceConfig;
import com.netflix.appinfo.HealthCheckHandler;
import com.netflix.appinfo.InstanceInfo;
import com.netflix.discovery.DiscoveryClient.DiscoveryClientOptionalArgs;
import com.netflix.discovery.EurekaClient;
import com.netflix.discovery.EurekaClientConfig;

import static org.springframework.cloud.commons.util.IdUtils.getDefaultInstanceId;

/**
 * @author Dave Syer
 * @author Spencer Gibb
 * @author Jon Schneider
 * @author Matt Jenkins
 * @author Ryan Baxter
 */
@Configuration
@EnableConfigurationProperties
@ConditionalOnClass(EurekaClientConfig.class)
@ConditionalOnBean(EurekaDiscoveryClientConfiguration.Marker.class)
@ConditionalOnProperty(value = "eureka.client.enabled", matchIfMissing = true)
@AutoConfigureBefore({ NoopDiscoveryClientAutoConfiguration.class,
      CommonsClientAutoConfiguration.class, ServiceRegistryAutoConfiguration.class })
@AutoConfigureAfter(name = "org.springframework.cloud.autoconfigure.RefreshAutoConfiguration")
public class EurekaClientAutoConfiguration {

   @Value("${server.port:${SERVER_PORT:${PORT:8080}}}")
   private int nonSecurePort;

   @Value("${management.port:${MANAGEMENT_PORT:${server.port:${SERVER_PORT:${PORT:8080}}}}}")
   private int managementPort;

   @Autowired
   private ConfigurableEnvironment env;

   @Autowired(required = false)
   private HealthCheckHandler healthCheckHandler;

   @Bean
   public HasFeatures eurekaFeature() {
      return HasFeatures.namedFeature("Eureka Client", EurekaClient.class);
   }

   @Bean
   @ConditionalOnMissingBean(value = EurekaClientConfig.class, search = SearchStrategy.CURRENT)
   public EurekaClientConfigBean eurekaClientConfigBean() {
      EurekaClientConfigBean client = new EurekaClientConfigBean();
      if ("bootstrap".equals(this.env.getProperty("spring.config.name"))) {
         // We don't register during bootstrap by default, but there will be another
         // chance later.
         client.setRegisterWithEureka(false);
      }
      return client;
   }

   @Bean
   @ConditionalOnMissingBean(value = EurekaInstanceConfig.class, search = SearchStrategy.CURRENT)
   public EurekaInstanceConfigBean eurekaInstanceConfigBean(InetUtils inetUtils) {
      RelaxedPropertyResolver relaxedPropertyResolver = new RelaxedPropertyResolver(env, "eureka.instance.");
      String hostname = relaxedPropertyResolver.getProperty("hostname");
      boolean preferIpAddress = Boolean.parseBoolean(relaxedPropertyResolver.getProperty("preferIpAddress"));
      EurekaInstanceConfigBean instance = new EurekaInstanceConfigBean(inetUtils);
      instance.setNonSecurePort(this.nonSecurePort);
      instance.setInstanceId(getDefaultInstanceId(this.env));
      instance.setPreferIpAddress(preferIpAddress);

      if (this.managementPort != this.nonSecurePort && this.managementPort != 0) {
         if (StringUtils.hasText(hostname)) {
            instance.setHostname(hostname);
         }
         String statusPageUrlPath = relaxedPropertyResolver.getProperty("statusPageUrlPath");
         String healthCheckUrlPath = relaxedPropertyResolver.getProperty("healthCheckUrlPath");
         if (StringUtils.hasText(statusPageUrlPath)) {
            instance.setStatusPageUrlPath(statusPageUrlPath);
         }
         if (StringUtils.hasText(healthCheckUrlPath)) {
            instance.setHealthCheckUrlPath(healthCheckUrlPath);
         }
         String scheme = instance.getSecurePortEnabled() ? "https" : "http";
         instance.setStatusPageUrl(scheme + "://" + instance.getHostname() + ":"
               + this.managementPort + instance.getStatusPageUrlPath());
         instance.setHealthCheckUrl(scheme + "://" + instance.getHostname() + ":"
               + this.managementPort + instance.getHealthCheckUrlPath());
      }
      return instance;
   }

   @Bean
   public DiscoveryClient discoveryClient(EurekaInstanceConfig config,
         EurekaClient client) {
      return new EurekaDiscoveryClient(config, client);
   }

   @Bean
   public EurekaServiceRegistry eurekaServiceRegistry() {
      return new EurekaServiceRegistry();
   }

   @Bean
   @ConditionalOnBean(AutoServiceRegistrationProperties.class)
   @ConditionalOnProperty(value = "spring.cloud.service-registry.auto-registration.enabled", matchIfMissing = true)
   public EurekaRegistration eurekaRegistration(EurekaClient eurekaClient, CloudEurekaInstanceConfig instanceConfig, ApplicationInfoManager applicationInfoManager) {
      return EurekaRegistration.builder(instanceConfig)
            .with(applicationInfoManager)
            .with(eurekaClient)
            .with(healthCheckHandler)
            .build();
   }

   @Bean
   @ConditionalOnBean(AutoServiceRegistrationProperties.class)
   @ConditionalOnProperty(value = "spring.cloud.service-registry.auto-registration.enabled", matchIfMissing = true)
   public EurekaAutoServiceRegistration eurekaAutoServiceRegistration(ApplicationContext context, EurekaServiceRegistry registry, EurekaRegistration registration) {
      return new EurekaAutoServiceRegistration(context, registry, registration);
   }

   @Bean
   @ConditionalOnMissingBean(value = DiscoveryClientOptionalArgs.class, search = SearchStrategy.CURRENT)
   public MutableDiscoveryClientOptionalArgs discoveryClientOptionalArgs() {
      return new MutableDiscoveryClientOptionalArgs();
   }

   @Configuration
   @ConditionalOnMissingRefreshScope
   protected static class EurekaClientConfiguration {

      @Autowired
      private ApplicationContext context;

      @Autowired(required = false)
      private DiscoveryClientOptionalArgs optionalArgs;

      @Bean(destroyMethod = "shutdown")
      @ConditionalOnMissingBean(value = EurekaClient.class, search = SearchStrategy.CURRENT)
      public EurekaClient eurekaClient(ApplicationInfoManager manager,
            EurekaClientConfig config) {
         return new CloudEurekaClient(manager, config, this.optionalArgs,
               this.context);
      }

      @Bean
      @ConditionalOnMissingBean(value = ApplicationInfoManager.class, search = SearchStrategy.CURRENT)
      public ApplicationInfoManager eurekaApplicationInfoManager(
            EurekaInstanceConfig config) {
         InstanceInfo instanceInfo = new InstanceInfoFactory().create(config);
         return new ApplicationInfoManager(config, instanceInfo);
      }
   }

   @Configuration
   @ConditionalOnRefreshScope
   protected static class RefreshableEurekaClientConfiguration {

      @Autowired
      private ApplicationContext context;

      @Autowired(required = false)
      private DiscoveryClientOptionalArgs optionalArgs;

      @Bean(destroyMethod = "shutdown")
      @ConditionalOnMissingBean(value = EurekaClient.class, search = SearchStrategy.CURRENT)
      @org.springframework.cloud.context.config.annotation.RefreshScope
      @Lazy
      public EurekaClient eurekaClient(ApplicationInfoManager manager,
            EurekaClientConfig config, EurekaInstanceConfig instance) {
         manager.getInfo(); // force initialization
          //这里是eureka client获取服务器list的地方
         return new CloudEurekaClient(manager, config, this.optionalArgs,
               this.context);
      }

      @Bean
      @ConditionalOnMissingBean(value = ApplicationInfoManager.class, search = SearchStrategy.CURRENT)
      @org.springframework.cloud.context.config.annotation.RefreshScope
      @Lazy
      public ApplicationInfoManager eurekaApplicationInfoManager(
            EurekaInstanceConfig config) {
         InstanceInfo instanceInfo = new InstanceInfoFactory().create(config);
         return new ApplicationInfoManager(config, instanceInfo);
      }

   }

   @Target({ ElementType.TYPE, ElementType.METHOD })
   @Retention(RetentionPolicy.RUNTIME)
   @Documented
   @Conditional(OnMissingRefreshScopeCondition.class)
   @interface ConditionalOnMissingRefreshScope {

   }

   @Target({ ElementType.TYPE, ElementType.METHOD })
   @Retention(RetentionPolicy.RUNTIME)
   @Documented
   @ConditionalOnClass(RefreshScope.class)
   @ConditionalOnBean(RefreshAutoConfiguration.class)
   @interface ConditionalOnRefreshScope {

   }

   private static class OnMissingRefreshScopeCondition extends AnyNestedCondition {

      public OnMissingRefreshScopeCondition() {
         super(ConfigurationPhase.REGISTER_BEAN);
      }

      @ConditionalOnMissingClass("org.springframework.cloud.context.scope.refresh.RefreshScope")
      static class MissingClass {
      }

      @ConditionalOnMissingBean(RefreshAutoConfiguration.class)
      static class MissingScope {
      }

   }

}
```

##### eureka-client配置文件

eureka-client.properties是eureka-client的配置文件。

```java
Manifest-Version=1.0
Implementation-Title=com.netflix.eureka#eureka-client;1.6.2
Implementation-Version=1.6.2
Built-Status=integration
Built-By=travis
Built-OS=Linux
Build-Date=2017-03-16_18:47:01
Gradle-Version=2.10
Module-Owner=netflixoss@netflix.com
Module-Email=netflixoss@netflix.com
Module-Source=/eureka-client
Module-Origin=https://github.com/Netflix/eureka.git
Change=64e5e2e
Branch=64e5e2ee97c6036d9a2f447bada79d643c985fb6
Build-Host=testing-docker-cc8792b2-d1fe-415d-91bf-67b9d0b91b14
Build-Job=LOCAL
Build-Number=LOCAL
Build-Id=LOCAL
Created-By=1.8.0_111-b14 (Oracle Corporation)
Build-Java-Version=1.8.0_111
X-Compile-Target-JDK=1.7
X-Compile-Source-JDK=1.7
```

##### DefaultEurekaClientConfig

控制eureka client相关配置的配置类，shouldFetchRegistry获取eureka server的远程服务信息。

##### EurekaClientConfigBean

控制eureka client相关配置的配置类，和DefaultEurekaClientConfig一样