package com.lqd.spring.microserviceproject.annotations;

import com.lqd.spring.microserviceproject.annotations.respository.ImportBean;
import com.lqd.spring.microserviceproject.annotations.respository.JdbcBean;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

/**
 * @ClassName BootImport
 * @Description @Import
 * @Author lqd
 * @Date 2019/3/24 16:48
 * @Version 1.0
 * <beans>
 *     <bean class=">
 *          <properties>
 *              <property>JdbcBean</property>
 *          </properties>
 *     </bean>
 * </beans>
 * @see com.lqd.spring.microserviceproject.annotations.respository.ImportBean
 * @see com.lqd.spring.microserviceproject.annotations.respository.JdbcBean
 **/
@Configuration
@Import(BootConfiguration.class)
@Slf4j
public class BootImport {

    @Bean
    public ImportBean invokeJdbcBeanImport(JdbcBean jdbcBean)
    {
        log.info(String.format("imported bean:%s",jdbcBean.hashCode()));
        return new ImportBean(jdbcBean) ;
    }
}
