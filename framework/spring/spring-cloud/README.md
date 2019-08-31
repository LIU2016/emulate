##### eureka

操作eureka的实例：

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