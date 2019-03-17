package com.lqd.spring.microserviceproject.Annotations;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.InitializingBean;

/**
 * @ClassName MyRespository
 * @Description TODO
 * @Author lqd
 * @Date 2019/3/17 14:53
 * @Version 1.0
 **/
@MyService
@Slf4j
public class MyRespository implements InitializingBean
{
    @Override
    public void afterPropertiesSet() throws Exception {
        log.info("Annatations:hello spring!","");
    }
}
