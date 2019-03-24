package com.lqd.spring.microserviceproject.annotations.respository;

import lombok.extern.slf4j.Slf4j;
import javax.annotation.PostConstruct;

/**
 * @ClassName ImportBean
 * @Description @Configuration
 * @see org.springframework.context.annotation.ConfigurationClassParser
 * @Author lqd
 * @Date 2019/3/24 16:55
 * @Version 1.0
 **/
@Slf4j
public class ImportBean
{
    private final JdbcBean jdbcBean ;

    public ImportBean(JdbcBean jdbcBean) {
        this.jdbcBean = jdbcBean;
    }

    @PostConstruct
    public void print()
    {
       String msg = String.format("ImportBean hashCode:%s" +
                                    ",jdbcBean.url:%s" +
                                    ",jdbcBean.password:%s",
                                    jdbcBean.hashCode(),
                                    jdbcBean.getUrl(),
                                    jdbcBean.getPassword());
       log.info(msg);
    }
}
