package com.lqd.spring.microserviceproject.Annotations;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.Configuration;

/**
 * @ClassName AnnatationsTest
 * @Description TODO
 * @Author lqd
 * @Date 2019/3/17 12:36
 * @Version 1.0
 **/
@SpringBootApplication
public class AnnatationsTest
{
    public static void main(String[] args) {

        //"com.lqd.spring.*"
        //AnnatationsTest
        AnnotationConfigApplicationContext
                annotationConfigApplicationContext =
                new AnnotationConfigApplicationContext(AnnatationsTest.class);
      //  annotationConfigApplicationContext.register();
      //  annotationConfigApplicationContext.refresh();
        System.out.println(annotationConfigApplicationContext.getBean(AnnatationsTest.class));
    }
}
