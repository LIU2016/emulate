package com.lqd.spring.microserviceproject.annotations.respository;

import com.lqd.spring.microserviceproject.annotations.BootConfigurationProperties;
import com.lqd.spring.microserviceproject.annotations.IBaseBean;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 * @ClassName MybatisBean
 * @Description TODO
 * @Author lqd
 * @Date 2019/3/24 18:11
 * @Version 1.0
 * @see BootConfigurationProperties
 **/
@Component
@Slf4j
@EnableConfigurationProperties(BootConfigurationProperties.class)
public class MybatisBean implements IBaseBean
{
    @Autowired
    private BootConfigurationProperties bootConfigurationProperties ;

    /**
     *
     * @throws Exception
     */
    @Override
    public void afterPropertiesSet() throws Exception {
        log.info("MybatisBean#afterPropertiesSet:" + String.format(print_jdbc_msg,"something",
                bootConfigurationProperties.getUrl(),bootConfigurationProperties.getPassword()));
    }

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {

        if (bean instanceof IBaseBean)
        {
            log.info("MybatisBean#postProcessAfterInitialization:" + String.format(print_jdbc_msg,bean.hashCode(),
                    bootConfigurationProperties.getUrl(),bootConfigurationProperties.getPassword()));
        }
        return bean ;
    }
}
