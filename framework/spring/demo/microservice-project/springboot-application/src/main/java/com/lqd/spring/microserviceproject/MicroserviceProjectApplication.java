package com.lqd.spring.microserviceproject;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.LinkedHashMap;
import java.util.Map;

@SpringBootApplication
public class MicroserviceProjectApplication {

	public static void main(String[] args) {

		//SpringApplication.run(MicroserviceProjectApplication.class, args);

		//fluent api模式
		/*new SpringApplicationBuilder(MicroserviceProjectApplication.class)
				//单元测试，PORT随机
				.properties("server.port=0")
				.run(args);*/

		//
		SpringApplication springApplication =
				new SpringApplication(MicroserviceProjectApplication.class);
		final Map<String,Object> map = new LinkedHashMap<>(1);
		map.put("server.port",0);
		springApplication.setDefaultProperties(map);
		//springApplication.setWebApplicationType(WebApplicationType.NONE);
		ConfigurableApplicationContext configurableApplicationContext =springApplication.run(args);
		//System.out.println(configurableApplicationContext.getBean(MicroserviceProjectApplication.class));
		//configurableApplicationContext.close();
	}

}
