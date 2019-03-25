package com.lqd.spring.microserviceproject.annotations.respository;

import com.lqd.spring.microserviceproject.annotations.BootConditional;
import com.lqd.spring.microserviceproject.annotations.IBaseBean;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.BeansException;
import org.springframework.context.annotation.Conditional;
import org.springframework.stereotype.Component;

/**
 * @ClassName ConditionalBean
 * @Description use Conditional
 * @Author lqd
 * @Date 2019/3/24 19:16
 * @Version 1.0
 * @see BootConditional
 **/
@Conditional(BootConditional.class)
@Component
@Slf4j
public class ConditionalBean implements IBaseBean {

    @Override
    public void afterPropertiesSet() throws Exception {
        log.info(String.format(print_bean_msg,"ConditionalBean#afterPropertiesSet",this.hashCode()));
    }

    @Override
    public Object postProcessBeforeInitialization(Object o, String s) throws BeansException {
        return null;
    }

    @Override
    public Object postProcessAfterInitialization(Object o, String s) throws BeansException {
        return null;
    }
}
