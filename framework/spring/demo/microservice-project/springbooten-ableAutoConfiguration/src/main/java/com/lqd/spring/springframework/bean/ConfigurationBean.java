package com.lqd.spring.springframework.bean;

import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.InitializingBean;

/**
 * @ClassName ConfigurationBean
 * @Description TODO
 * @Author lqd
 * @Date 2019/3/25 19:41
 * @Version 1.0
 **/
@Slf4j
@Data
public class ConfigurationBean implements InitializingBean
{
    public void afterPropertiesSet() throws Exception {
       log.info("@EnableAutoConfiguration#ConfigurationBean#afterPropertiesSet");
    }
}
