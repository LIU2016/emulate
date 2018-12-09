package com.lqd.demo;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

/**
 * @ClassName Application
 * @Description TODO
 * @Author lqd
 * @Date 2018/12/9 9:18
 * @Version 1.0
 **/
public class Application
{
    public static void main(String[] args) {
       /* ClassPathXmlApplicationContext classPathXmlApplicationContext =
                new ClassPathXmlApplicationContext("classpath:spring-base.xml");
        classPathXmlApplicationContext.start();*/
        AnnotationConfigApplicationContext annotationConfigApplicationContext =
                new AnnotationConfigApplicationContext();
        annotationConfigApplicationContext.refresh();
    }
}
