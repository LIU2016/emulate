### @FeignClient解析

#### RibbonClientConfiguration

ribbon的核心启动，配置了ribbon相关的初始化类。其中ZoneAwareLoadBalancer就是获取注册中心eureka的服务器实例的bean。

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

package org.springframework.cloud.netflix.ribbon;

import java.net.URI;

import javax.annotation.PostConstruct;

import org.apache.http.client.params.ClientPNames;
import org.apache.http.client.params.CookiePolicy;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.cloud.client.loadbalancer.LoadBalancedRetryPolicyFactory;
import org.springframework.cloud.netflix.ribbon.apache.RetryableRibbonLoadBalancingHttpClient;
import org.springframework.cloud.netflix.ribbon.apache.RibbonLoadBalancingHttpClient;
import org.springframework.cloud.netflix.ribbon.okhttp.OkHttpLoadBalancingClient;
import org.springframework.cloud.netflix.ribbon.okhttp.RetryableOkHttpLoadBalancingClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Lazy;

import com.netflix.client.AbstractLoadBalancerAwareClient;
import com.netflix.client.DefaultLoadBalancerRetryHandler;
import com.netflix.client.RetryHandler;
import com.netflix.client.config.DefaultClientConfigImpl;
import com.netflix.client.config.IClientConfig;
import com.netflix.loadbalancer.ConfigurationBasedServerList;
import com.netflix.loadbalancer.DummyPing;
import com.netflix.loadbalancer.ILoadBalancer;
import com.netflix.loadbalancer.IPing;
import com.netflix.loadbalancer.IRule;
import com.netflix.loadbalancer.PollingServerListUpdater;
import com.netflix.loadbalancer.Server;
import com.netflix.loadbalancer.ServerList;
import com.netflix.loadbalancer.ServerListFilter;
import com.netflix.loadbalancer.ServerListUpdater;
import com.netflix.loadbalancer.ZoneAvoidanceRule;
import com.netflix.loadbalancer.ZoneAwareLoadBalancer;
import com.netflix.niws.client.http.RestClient;
import com.netflix.servo.monitor.Monitors;
import com.sun.jersey.api.client.Client;
import com.sun.jersey.client.apache4.ApacheHttpClient4;

import static com.netflix.client.config.CommonClientConfigKey.DeploymentContextBasedVipAddresses;
import static org.springframework.cloud.netflix.ribbon.RibbonUtils.setRibbonProperty;
import static org.springframework.cloud.netflix.ribbon.RibbonUtils.updateToHttpsIfNeeded;

/**
 * @author Dave Syer
 */
@SuppressWarnings("deprecation")
@Configuration
@EnableConfigurationProperties
public class RibbonClientConfiguration {

   @Value("${ribbon.client.name}")
   private String name = "client";

   // TODO: maybe re-instate autowired load balancers: identified by name they could be
   // associated with ribbon clients

   @Autowired
   private PropertiesFactory propertiesFactory;

   @Bean
   @ConditionalOnMissingBean
   public IClientConfig ribbonClientConfig() {
      DefaultClientConfigImpl config = new DefaultClientConfigImpl();
      config.loadProperties(this.name);
      return config;
   }

   @Bean
   @ConditionalOnMissingBean
   public IRule ribbonRule(IClientConfig config) {
      if (this.propertiesFactory.isSet(IRule.class, name)) {
         return this.propertiesFactory.get(IRule.class, config, name);
      }
      ZoneAvoidanceRule rule = new ZoneAvoidanceRule();
      rule.initWithNiwsConfig(config);
      return rule;
   }

   @Bean
   @ConditionalOnMissingBean
   public IPing ribbonPing(IClientConfig config) {
      if (this.propertiesFactory.isSet(IPing.class, name)) {
         return this.propertiesFactory.get(IPing.class, config, name);
      }
      return new DummyPing();
   }

   @Bean
   @ConditionalOnMissingBean
   @SuppressWarnings("unchecked")
   public ServerList<Server> ribbonServerList(IClientConfig config) {
      if (this.propertiesFactory.isSet(ServerList.class, name)) {
         return this.propertiesFactory.get(ServerList.class, config, name);
      }
      ConfigurationBasedServerList serverList = new ConfigurationBasedServerList();
      serverList.initWithNiwsConfig(config);
      return serverList;
   }

   @Configuration
   @ConditionalOnProperty(name = "ribbon.httpclient.enabled", matchIfMissing = true)
   protected static class HttpClientRibbonConfiguration {
      @Value("${ribbon.client.name}")
      private String name = "client";

      @Bean
      @ConditionalOnMissingBean(AbstractLoadBalancerAwareClient.class)
      @ConditionalOnMissingClass(value = "org.springframework.retry.support.RetryTemplate")
      public RibbonLoadBalancingHttpClient ribbonLoadBalancingHttpClient(
            IClientConfig config, ServerIntrospector serverIntrospector,
            ILoadBalancer loadBalancer, RetryHandler retryHandler) {
         RibbonLoadBalancingHttpClient client = new RibbonLoadBalancingHttpClient(
               config, serverIntrospector);
         client.setLoadBalancer(loadBalancer);
         client.setRetryHandler(retryHandler);
         Monitors.registerObject("Client_" + this.name, client);
         return client;
      }

      @Bean
      @ConditionalOnMissingBean(AbstractLoadBalancerAwareClient.class)
      @ConditionalOnClass(name = "org.springframework.retry.support.RetryTemplate")
      public RetryableRibbonLoadBalancingHttpClient retryableRibbonLoadBalancingHttpClient(
            IClientConfig config, ServerIntrospector serverIntrospector,
            ILoadBalancer loadBalancer, RetryHandler retryHandler,
            LoadBalancedRetryPolicyFactory loadBalancedRetryPolicyFactory) {
         RetryableRibbonLoadBalancingHttpClient client = new RetryableRibbonLoadBalancingHttpClient(
               config, serverIntrospector, loadBalancedRetryPolicyFactory);
         client.setLoadBalancer(loadBalancer);
         client.setRetryHandler(retryHandler);
         Monitors.registerObject("Client_" + this.name, client);
         return client;
      }
   }

   @Configuration
   @ConditionalOnProperty("ribbon.okhttp.enabled")
   @ConditionalOnClass(name = "okhttp3.OkHttpClient")
   protected static class OkHttpRibbonConfiguration {
      @Value("${ribbon.client.name}")
      private String name = "client";



      @Bean
      @ConditionalOnMissingBean(AbstractLoadBalancerAwareClient.class)
      @ConditionalOnClass(name = "org.springframework.retry.support.RetryTemplate")
      public RetryableOkHttpLoadBalancingClient okHttpLoadBalancingClient(IClientConfig config,
                                                         ServerIntrospector serverIntrospector,
                                                         ILoadBalancer loadBalancer,
                                                         RetryHandler retryHandler,
                                                         LoadBalancedRetryPolicyFactory loadBalancedRetryPolicyFactory) {
         RetryableOkHttpLoadBalancingClient client = new RetryableOkHttpLoadBalancingClient(config,
               serverIntrospector, loadBalancedRetryPolicyFactory);
         client.setLoadBalancer(loadBalancer);
         client.setRetryHandler(retryHandler);
         Monitors.registerObject("Client_" + this.name, client);
         return client;
      }

      @Bean
      @ConditionalOnMissingBean(AbstractLoadBalancerAwareClient.class)
      @ConditionalOnMissingClass(value = "org.springframework.retry.support.RetryTemplate")
      public OkHttpLoadBalancingClient retryableOkHttpLoadBalancingClient(IClientConfig config,
                                                   ServerIntrospector serverIntrospector, ILoadBalancer loadBalancer,
                                                   RetryHandler retryHandler) {
         OkHttpLoadBalancingClient client = new OkHttpLoadBalancingClient(config,
               serverIntrospector);
         client.setLoadBalancer(loadBalancer);
         client.setRetryHandler(retryHandler);
         Monitors.registerObject("Client_" + this.name, client);
         return client;
      }
   }

   @Configuration
   @RibbonAutoConfiguration.ConditionalOnRibbonRestClient
   protected static class RestClientRibbonConfiguration {
      @Value("${ribbon.client.name}")
      private String name = "client";

      /**
       * Create a Netflix {@link RestClient} integrated with Ribbon if none already exists
       * in the application context. It is not required for Ribbon to work properly and is
       * therefore created lazily if ever another component requires it.
       *
       * @param config             the configuration to use by the underlying Ribbon instance
       * @param loadBalancer       the load balancer to use by the underlying Ribbon instance
       * @param serverIntrospector server introspector to use by the underlying Ribbon instance
       * @param retryHandler       retry handler to use by the underlying Ribbon instance
       * @return a {@link RestClient} instances backed by Ribbon
       */
      @Bean
      @Lazy
      @ConditionalOnMissingBean(AbstractLoadBalancerAwareClient.class)
      public RestClient ribbonRestClient(IClientConfig config, ILoadBalancer loadBalancer,
                                 ServerIntrospector serverIntrospector, RetryHandler retryHandler) {
         RestClient client = new OverrideRestClient(config, serverIntrospector);
         client.setLoadBalancer(loadBalancer);
         client.setRetryHandler(retryHandler);
         Monitors.registerObject("Client_" + this.name, client);
         return client;
      }
   }

   @Bean
   @ConditionalOnMissingBean
   public ServerListUpdater ribbonServerListUpdater(IClientConfig config) {
      return new PollingServerListUpdater(config);
   }

   @Bean
   @ConditionalOnMissingBean
   public ILoadBalancer ribbonLoadBalancer(IClientConfig config,
         ServerList<Server> serverList, ServerListFilter<Server> serverListFilter,
         IRule rule, IPing ping, ServerListUpdater serverListUpdater) {
      if (this.propertiesFactory.isSet(ILoadBalancer.class, name)) {
         return this.propertiesFactory.get(ILoadBalancer.class, config, name);
      }
      return new ZoneAwareLoadBalancer<>(config, rule, ping, serverList,
            serverListFilter, serverListUpdater);
   }

   @Bean
   @ConditionalOnMissingBean
   @SuppressWarnings("unchecked")
   public ServerListFilter<Server> ribbonServerListFilter(IClientConfig config) {
      if (this.propertiesFactory.isSet(ServerListFilter.class, name)) {
         return this.propertiesFactory.get(ServerListFilter.class, config, name);
      }
      ZonePreferenceServerListFilter filter = new ZonePreferenceServerListFilter();
      filter.initWithNiwsConfig(config);
      return filter;
   }

   @Bean
   @ConditionalOnMissingBean
   public RibbonLoadBalancerContext ribbonLoadBalancerContext(
         ILoadBalancer loadBalancer, IClientConfig config, RetryHandler retryHandler) {
      return new RibbonLoadBalancerContext(loadBalancer, config, retryHandler);
   }

   @Bean
   @ConditionalOnMissingBean
   public RetryHandler retryHandler(IClientConfig config) {
      return new DefaultLoadBalancerRetryHandler(config);
   }
   
   @Bean
   @ConditionalOnMissingBean
   public ServerIntrospector serverIntrospector() {
      return new DefaultServerIntrospector();
   }

   @PostConstruct
   public void preprocess() {
      setRibbonProperty(name, DeploymentContextBasedVipAddresses.key(), name);
   }

   static class OverrideRestClient extends RestClient {

      private IClientConfig config;
      private ServerIntrospector serverIntrospector;

      protected OverrideRestClient(IClientConfig config,
            ServerIntrospector serverIntrospector) {
         super();
         this.config = config;
         this.serverIntrospector = serverIntrospector;
         initWithNiwsConfig(this.config);
      }

      @Override
      public URI reconstructURIWithServer(Server server, URI original) {
         URI uri = updateToHttpsIfNeeded(original, this.config, this.serverIntrospector, server);
         return super.reconstructURIWithServer(server, uri);
      }

      @Override
      protected Client apacheHttpClientSpecificInitialization() {
         ApacheHttpClient4 apache = (ApacheHttpClient4) super
               .apacheHttpClientSpecificInitialization();
         apache.getClientHandler()
               .getHttpClient()
               .getParams()
               .setParameter(ClientPNames.COOKIE_POLICY, CookiePolicy.IGNORE_COOKIES);
         return apache;
      }

   }

}
```

#### DynamicServerListLoadBalancer

他是ZoneAwareLoadBalancer的父类，在ZoneAwareLoadBalancer初始化的时候，启动了一个线程用于获取其他的实例的服务器配置。在该类的 enableAndInitLearnNewServersFeature()方法中实现，单线程池加载了这个线程。

```java
/*
 *
 * Copyright 2013 Netflix, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */
package com.netflix.loadbalancer;

import com.google.common.annotations.VisibleForTesting;
import com.netflix.client.ClientFactory;
import com.netflix.client.config.CommonClientConfigKey;
import com.netflix.client.config.DefaultClientConfigImpl;
import com.netflix.client.config.IClientConfig;
import com.netflix.servo.annotations.DataSourceType;
import com.netflix.servo.annotations.Monitor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * A LoadBalancer that has the capabilities to obtain the candidate list of
 * servers using a dynamic source. i.e. The list of servers can potentially be
 * changed at Runtime. It also contains facilities wherein the list of servers
 * can be passed through a Filter criteria to filter out servers that do not
 * meet the desired criteria.
 * 
 * @author stonse
 * 
 */
public class DynamicServerListLoadBalancer<T extends Server> extends BaseLoadBalancer {
    private static final Logger LOGGER = LoggerFactory.getLogger(DynamicServerListLoadBalancer.class);

    boolean isSecure = false;
    boolean useTunnel = false;

    // to keep track of modification of server lists
    protected AtomicBoolean serverListUpdateInProgress = new AtomicBoolean(false);

    volatile ServerList<T> serverListImpl;

    volatile ServerListFilter<T> filter;

    protected final ServerListUpdater.UpdateAction updateAction = new ServerListUpdater.UpdateAction() {
        @Override
        public void doUpdate() {
            updateListOfServers();
        }
    };

    protected volatile ServerListUpdater serverListUpdater;

    public DynamicServerListLoadBalancer() {
        super();
    }

    @Deprecated
    public DynamicServerListLoadBalancer(IClientConfig clientConfig, IRule rule, IPing ping, 
            ServerList<T> serverList, ServerListFilter<T> filter) {
        this(
                clientConfig,
                rule,
                ping,
                serverList,
                filter,
                new PollingServerListUpdater()
        );
    }

    public DynamicServerListLoadBalancer(IClientConfig clientConfig, IRule rule, IPing ping,
                                         ServerList<T> serverList, ServerListFilter<T> filter,
                                         ServerListUpdater serverListUpdater) {
        super(clientConfig, rule, ping);
        this.serverListImpl = serverList;
        this.filter = filter;
        this.serverListUpdater = serverListUpdater;
        if (filter instanceof AbstractServerListFilter) {
            ((AbstractServerListFilter) filter).setLoadBalancerStats(getLoadBalancerStats());
        }
        restOfInit(clientConfig);
    }

    public DynamicServerListLoadBalancer(IClientConfig clientConfig) {
        initWithNiwsConfig(clientConfig);
    }
    
    @Override
    public void initWithNiwsConfig(IClientConfig clientConfig) {
        try {
            super.initWithNiwsConfig(clientConfig);
            String niwsServerListClassName = clientConfig.getPropertyAsString(
                    CommonClientConfigKey.NIWSServerListClassName,
                    DefaultClientConfigImpl.DEFAULT_SEVER_LIST_CLASS);

            ServerList<T> niwsServerListImpl = (ServerList<T>) ClientFactory
                    .instantiateInstanceWithClientConfig(niwsServerListClassName, clientConfig);
            this.serverListImpl = niwsServerListImpl;

            if (niwsServerListImpl instanceof AbstractServerList) {
                AbstractServerListFilter<T> niwsFilter = ((AbstractServerList) niwsServerListImpl)
                        .getFilterImpl(clientConfig);
                niwsFilter.setLoadBalancerStats(getLoadBalancerStats());
                this.filter = niwsFilter;
            }

            String serverListUpdaterClassName = clientConfig.getPropertyAsString(
                    CommonClientConfigKey.ServerListUpdaterClassName,
                    DefaultClientConfigImpl.DEFAULT_SERVER_LIST_UPDATER_CLASS
            );

            this.serverListUpdater = (ServerListUpdater) ClientFactory
                    .instantiateInstanceWithClientConfig(serverListUpdaterClassName, clientConfig);

            restOfInit(clientConfig);
        } catch (Exception e) {
            throw new RuntimeException(
                    "Exception while initializing NIWSDiscoveryLoadBalancer:"
                            + clientConfig.getClientName()
                            + ", niwsClientConfig:" + clientConfig, e);
        }
    }

    void restOfInit(IClientConfig clientConfig) {
        boolean primeConnection = this.isEnablePrimingConnections();
        // turn this off to avoid duplicated asynchronous priming done in BaseLoadBalancer.setServerList()
        this.setEnablePrimingConnections(false);
        enableAndInitLearnNewServersFeature();

        updateListOfServers();
        if (primeConnection && this.getPrimeConnections() != null) {
            this.getPrimeConnections()
                    .primeConnections(getReachableServers());
        }
        this.setEnablePrimingConnections(primeConnection);
        LOGGER.info("DynamicServerListLoadBalancer for client {} initialized: {}", clientConfig.getClientName(), this.toString());
    }
    
    
    @Override
    public void setServersList(List lsrv) {
        super.setServersList(lsrv);
        List<T> serverList = (List<T>) lsrv;
        Map<String, List<Server>> serversInZones = new HashMap<String, List<Server>>();
        for (Server server : serverList) {
            // make sure ServerStats is created to avoid creating them on hot
            // path
            getLoadBalancerStats().getSingleServerStat(server);
            String zone = server.getZone();
            if (zone != null) {
                zone = zone.toLowerCase();
                List<Server> servers = serversInZones.get(zone);
                if (servers == null) {
                    servers = new ArrayList<Server>();
                    serversInZones.put(zone, servers);
                }
                servers.add(server);
            }
        }
        setServerListForZones(serversInZones);
    }

    protected void setServerListForZones(
            Map<String, List<Server>> zoneServersMap) {
        LOGGER.debug("Setting server list for zones: {}", zoneServersMap);
        getLoadBalancerStats().updateZoneServerMapping(zoneServersMap);
    }

    public ServerList<T> getServerListImpl() {
        return serverListImpl;
    }

    public void setServerListImpl(ServerList<T> niwsServerList) {
        this.serverListImpl = niwsServerList;
    }

    public ServerListFilter<T> getFilter() {
        return filter;
    }

    public void setFilter(ServerListFilter<T> filter) {
        this.filter = filter;
    }

    @Override
    /**
     * Makes no sense to ping an inmemory disc client
     * 
     */
    public void forceQuickPing() {
        // no-op
    }

    /**
     * Feature that lets us add new instances (from AMIs) to the list of
     * existing servers that the LB will use Call this method if you want this
     * feature enabled
     */
    public void enableAndInitLearnNewServersFeature() {
        LOGGER.info("Using serverListUpdater {}", serverListUpdater.getClass().getSimpleName());
        serverListUpdater.start(updateAction);
    }

    private String getIdentifier() {
        return this.getClientConfig().getClientName();
    }

    public void stopServerListRefreshing() {
        if (serverListUpdater != null) {
            serverListUpdater.stop();
        }
    }

    @VisibleForTesting
    public void updateListOfServers() {
        List<T> servers = new ArrayList<T>();
        if (serverListImpl != null) {
            servers = serverListImpl.getUpdatedListOfServers();
            LOGGER.debug("List of Servers for {} obtained from Discovery client: {}",
                    getIdentifier(), servers);

            if (filter != null) {
                servers = filter.getFilteredListOfServers(servers);
                LOGGER.debug("Filtered List of Servers for {} obtained from Discovery client: {}",
                        getIdentifier(), servers);
            }
        }
        updateAllServerList(servers);
    }

    /**
     * Update the AllServer list in the LoadBalancer if necessary and enabled
     * 
     * @param ls
     */
    protected void updateAllServerList(List<T> ls) {
        // other threads might be doing this - in which case, we pass
        if (serverListUpdateInProgress.compareAndSet(false, true)) {
            try {
                for (T s : ls) {
                    s.setAlive(true); // set so that clients can start using these
                                      // servers right away instead
                                      // of having to wait out the ping cycle.
                }
                setServersList(ls);
                super.forceQuickPing();
            } finally {
                serverListUpdateInProgress.set(false);
            }
        }
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("DynamicServerListLoadBalancer:");
        sb.append(super.toString());
        sb.append("ServerList:" + String.valueOf(serverListImpl));
        return sb.toString();
    }
    
    @Override 
    public void shutdown() {
        super.shutdown();
        stopServerListRefreshing();
    }


    @Monitor(name="LastUpdated", type=DataSourceType.INFORMATIONAL)
    public String getLastUpdate() {
        return serverListUpdater.getLastUpdate();
    }

    @Monitor(name="DurationSinceLastUpdateMs", type= DataSourceType.GAUGE)
    public long getDurationSinceLastUpdateMs() {
        return serverListUpdater.getDurationSinceLastUpdateMs();
    }

    @Monitor(name="NumUpdateCyclesMissed", type=DataSourceType.GAUGE)
    public int getNumberMissedCycles() {
        return serverListUpdater.getNumberMissedCycles();
    }

    @Monitor(name="NumThreads", type=DataSourceType.GAUGE)
    public int getCoreThreads() {
        return serverListUpdater.getCoreThreads();
    }
}
```

#### ILoadBalancer接口

加载服务器、实例之间的均衡负载的核心接口，

主要实现类：BaseLoadBalancer、DynamicServerListLoadBalancer

```java
/*
*
* Copyright 2013 Netflix, Inc.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
*/
package com.netflix.loadbalancer;

import java.util.List;

/**
 * Interface that defines the operations for a software loadbalancer. A typical
 * loadbalancer minimally need a set of servers to loadbalance for, a method to
 * mark a particular server to be out of rotation and a call that will choose a
 * server from the existing list of server.
 * 
 * @author stonse
 * 
 */
public interface ILoadBalancer {

	/**
	 * Initial list of servers.
	 * This API also serves to add additional ones at a later time
	 * The same logical server (host:port) could essentially be added multiple times
	 * (helpful in cases where you want to give more "weightage" perhaps ..)
	 * 
	 * @param newServers new servers to add
	 */
	public void addServers(List<Server> newServers);
	
	/**
	 * Choose a server from load balancer.
	 * 
	 * @param key An object that the load balancer may use to determine which server to return. null if 
	 *         the load balancer does not use this parameter.
	 * @return server chosen
	 */
	public Server chooseServer(Object key);
	
	/**
	 * To be called by the clients of the load balancer to notify that a Server is down
	 * else, the LB will think its still Alive until the next Ping cycle - potentially
	 * (assuming that the LB Impl does a ping)
	 * 
	 * @param server Server to mark as down
	 */
	public void markServerDown(Server server);
	
	/**
	 * @deprecated 2016-01-20 This method is deprecated in favor of the
	 * cleaner {@link #getReachableServers} (equivalent to availableOnly=true)
	 * and {@link #getAllServers} API (equivalent to availableOnly=false).
	 *
	 * Get the current list of servers.
	 *
	 * @param availableOnly if true, only live and available servers should be returned
	 */
	@Deprecated
	public List<Server> getServerList(boolean availableOnly);

	/**
	 * @return Only the servers that are up and reachable.
     */
    public List<Server> getReachableServers();

    /**
     * @return All known servers, both reachable and unreachable.
     */
	public List<Server> getAllServers();
}

```

