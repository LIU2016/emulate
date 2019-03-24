package com.lqd.spring.microserviceproject.annotations;

import com.lqd.spring.microserviceproject.annotations.respository.JdbcBean;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * @ClassName BootConfiguration
 * @Description TODO
 * @Author lqd
 * @Date 2019/3/24 14:59
 * @Version 1.0
 * <beans>
 *     <bean class="xx.xx.BootConfiguraion"></bean>
 * </beans>
 **/
@Configuration
@Slf4j
@Data
public class BootConfiguration
{
    /**
     * 若是很多处要用到这些配置 怎么办？要是key修改了名称？
     */
    @Value("${spring.jdbc.url}")
    public String url;
    @Value("${spring.jdbc.password:123}")
    public String password;

    @Bean
    public JdbcBean jdbcBean()
    {
        JdbcBean jdbcBean = new JdbcBean(url,password) ;
        log.info(String.format("jdbcBean:%s",jdbcBean.hashCode()));
        return jdbcBean;
    }
}
