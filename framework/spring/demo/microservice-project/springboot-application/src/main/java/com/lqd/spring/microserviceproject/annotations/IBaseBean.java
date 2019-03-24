package com.lqd.spring.microserviceproject.annotations;

import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.config.BeanPostProcessor;

/**
 * @ClassName IBaseBean
 * @Description TODO
 * @Author lqd
 * @Date 2019/3/24 18:13
 * @Version 1.0
 **/
public interface IBaseBean extends InitializingBean ,BeanPostProcessor {

    String print_jdbc_msg = "Bean hashCode:%s" +
            ",jdbcBean.url:%s" +
            ",jdbcBean.password:%s";
    String print_bean_msg = "Bean %s hashCode:%s" ;
}
