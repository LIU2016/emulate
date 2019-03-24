package com.lqd.spring.microserviceproject.annotations.respository;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.ToString;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.InitializingBean;

/**
 * @ClassName JdbcBean
 * @Description TODO
 * @Author lqd
 * @Date 2019/3/24 16:51
 * @Version 1.0
 **/
@Slf4j
@Data
@ToString
@AllArgsConstructor
public class JdbcBean implements InitializingBean {

    private String url;
    private String password;

    @Override
    public void afterPropertiesSet() throws Exception {
        String toString = "@Configuration:%s ok!" ;
        log.info(String.format(toString,"jdbc configuration "));
    }
}
