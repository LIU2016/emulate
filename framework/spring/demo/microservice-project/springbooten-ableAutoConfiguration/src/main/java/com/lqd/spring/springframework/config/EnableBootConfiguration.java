package com.lqd.spring.springframework.config;

import com.lqd.spring.springframework.bean.ConfigurationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * @ClassName EnableBootConfiguration
 * @Description TODO
 * @Author lqd
 * @Date 2019/3/25 19:41
 * @Version 1.0
 **/
@Configuration
public class EnableBootConfiguration
{
    @Bean
    public ConfigurationBean configurationBean()
    {
        return new ConfigurationBean();
    }
}
