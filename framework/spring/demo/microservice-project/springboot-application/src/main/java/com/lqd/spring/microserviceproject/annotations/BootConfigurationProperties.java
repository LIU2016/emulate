package com.lqd.spring.microserviceproject.annotations;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

/**
 * @ClassName BootConfigurationProperties
 * @Description ConfigurationProperties 注解
 * @Author lqd
 * @Date 2019/3/24 17:58
 * @Version 1.0
 * @EnableConfigurationProperties (使用类) + @ConfigurationProperties = @Component(定义的类) + @ConfigurationProperties
 **/

@Data
//@Component
@ConfigurationProperties("spring.jdbc")
public class BootConfigurationProperties
{
    public String url;
    public String password;
}
