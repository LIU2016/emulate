package com.lqd.spring.microserviceproject.annotations;

import org.springframework.context.annotation.Condition;
import org.springframework.context.annotation.ConditionContext;
import org.springframework.core.type.AnnotatedTypeMetadata;

/**
 * @ClassName BootConditional
 * @Description Conditional
 * @Author lqd
 * @Date 2019/3/24 19:13
 * @Version 1.0
 **/
public class BootConditional implements Condition {

    @Override
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {

        try {
            context.getClassLoader().loadClass("com.lqd.spring.microserviceproject.annotations.BootImport");
        } catch (ClassNotFoundException e) {
            return false;
        }
        return true;
    }
}
