# spring boot

## Spring Boot 介绍

http://projects.spring.io/spring-boot/

### 基本概念

```
应用分为两个方面：功能性、非功能性 功能性：
系统所设计的业务范畴 非功能性：安全、性能、监控、数据指标（CPU利用率、网卡使用率） 
```

### Spring Boot有四大神器

分别是auto-configuration、starters、cli、actuator

```
starters
SpringBoot的starter主要用来简化依赖用的。本文主要分两部分，一部分是列出一些starter的依赖，另一部分是教你自己写一个starter。

actuator
actuator是spring boot提供的对应用系统的自省和监控的集成功能，可以对应用系统进行配置查看、相关功能统计等。

cli
SpringBootCLI是一个命令行工具，可用于快速搭建基于spring的原型。它支持运行Groovy脚本，这也就意味着你可以使用类似Java的语法，但不用写很多的模板代码。

auto-configuration
查看(脱掉)Spring的代码(衣服),auto-configuration 就是一个实现了Configuration接口的类。使用@Conditional注解来限制何时让auto-configuration 生效，通常auto-configuration 使用ConditionalOnClass和ConditionalOnMissingBean注解，这两注解的确保只有当我们拥有相关类的时候使得@Configuration注解生效。
```

自动装配

```
Spring Boot 规约大于配置，大多数组件，不需要自行配置，而是自动组装！简化开发，大多数情况，使用默认即可！ production-ready 就是非功能性范畴！
```

独立Spring 应用

```
独立Spring 应用，不需要外部依赖，依赖容器（Tomcat），嵌入式 Tomcat Jetty 
```

外部配置：启动参数、配置文件、环境变量

```
外部应用：Servlet 应用、Spring Web MVC、Spring Web Flux、WebSocket、WebService
```

actuator

```
GET	/autoconfig	查看自动配置的使用情况	true
GET	/configprops	查看配置属性，包括默认配置	true
GET	/beans	查看bean及其关系列表	true
GET	/dump	打印线程栈	true
GET	/env	查看所有环境变量	true
GET	/env/{name}	查看具体变量值	true
GET	/health	查看应用健康指标	false
GET	/info	查看应用信息	false
GET	/mappings	查看所有url映射	true
GET	/metrics	查看应用基本指标	true
GET	/metrics/{name}	查看具体指标	true
POST	/shutdown	关闭应用	true
GET	/trace	查看基本追踪信息	true
```

SQL：JDBC、JPA、ORM

NoSQL（Not Only SQL）：Redis、ElasticSearch、Hbase

Mono : 0 - 1 元素，Optional

Flux：0 - N 个元素，类似于 Iterable 或者 Collection

Req -> WebFlux -> 1 - N 线程执行任务执行函数式任务

### 第一个Spring Boot项目

1，图形化方式（<http://start.spring.io/>）

2，命令行方式（Maven）

多模块项目，并构建可执行jar或者war

```
1，修改主工程类型jar -> pom

2，新建 web 工程，将遗留代码移动到 web java 目录下

3，再从 web 工程，独立出 model 工程

4，将 web 工程依赖 model 工程

5，重复步骤 3，独立出 persistence（持久层）

6，再从 persistence 添加 model 的依赖

7，最终依赖关系 web -> persistence -> model

8，web-1.0.0-SNAPSHOT.jar中没有主清单属性？
jar 规范里面，有一个 MANIFEST.MF，里面有一个 Main-Class 的属性。API：java.util.jar.Manifest#getAttributes需要一个 Spring Boot 的插件：
<build>
  <plugins>
    <plugin>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-maven-plugin</artifactId>
    </plugin>
  </plugins>
</build>

9，从 jar 切换成war打包方式
修改成 war,创建webapp/WEB-INF 目录（相对于src/main新建一个空的web.xml或者使用
<plugin>
     <artifactId>maven-war-plugin</artifactId>
     <configuration>
              <failOnMissingWebXml>false</failOnMissingWebXml>
     </configuration>
</plugin>
注意事项
BOOT-INF 是 Spring Boot 1.4开始才有
当使用依赖或者插件时，如果版本是 Milestone的时候，需要增加：
 <repositories>
      <repository>
          <id>spring-milestones</id>
          <name>Spring Milestones</name>
          <url>https://repo.spring.io/libs-milestone</url>
          <snapshots>
              <enabled>false</enabled>
          </snapshots>
      </repository>
  </repositories>
  <pluginRepositories>
      <pluginRepository>
          <id>spring-snapshots</id>
          <url>http://repo.spring.io/snapshot</url>
      </pluginRepository>
      <pluginRepository>
          <id>spring-milestones</id>
          <url>http://repo.spring.io/milestone</url>
      </pluginRepository>
  </pluginRepositories>
META-INF/MANIFEST.MF 里面有指定两个属性
Main-Class Start-Class 例子： Main-Class: org.springframework.boot.loader.JarLauncher Start-Class: com.gupao.App 

除了 jar （jar -jar jar包名）或者 war（jar -jar war包名） 启动的方式，
还有目录启动方式,目录启动方式可以帮助解决老旧的jar 不支持 Spring Boot 新方式，比如老版本的 MyBatis 
1，如果是jar 包，解压后，跳转解压目录，并且执行java命令启动，启动类是 org.springframework.boot.loader.JarLauncher （java org.springframework.boot.loader.JarLauncher） 
2，如果是 war包，解压后，跳转解压目录，并且执行java命令启动类是org.springframework.boot.loader.WarLauncher 

```

查看端口

```
注意控制台：Netty started on port(s): 8080 --server.port=0 随机可用端口 自动装配的模式 XXX-AutoConfiguration 
```

spring的老项目迁移到springboot，怎么弄

```
老的XML 方式采用 @ImportResource 导入！
```

#### 嵌入式tomcat如何调优

```
第一种通过 application.properties文件调整配置参数 
第二种通过接口回调： TomcatConnectorCustomizer TomcatContextCustomizer 
```

# Spring REST \ MVC

# Spring jdbc

## 数据源（DataSource）

```
数据源
数据源是数据库连接的来源，通过DataSource接口获取。
类型
通用型数据源
javax.sql.DataSource
分布式数据源
javax.sql.XADataSource
嵌入式数据源
org.springframework.jdbc.datasource.embedded.EmbeddedDatabase
```

### 演示

单数据源场景

```
spring.datasource.driverClassName=com.mysql.jdbc.Driver 
spring.datasource.url=jdbc:<mysql://192.168.254.136:3306/test> spring.datasource.username=root 
spring.datasource.password=root123
```

多数据源场景

```JAVA
@Configuration
public class MultipleDataSourceConfiguration {
    @Bean
    @Primary
    public DataSource masterDataSource(){
        DataSourceBuilder dataSourceBuilder = DataSourceBuilder.create();
        return dataSourceBuilder.driverClassName("com.mysql.jdbc.Driver").url("jdbc:mysql://192.168.254.136:3306/test")
                .password("root123").username("root").build();
    }
    @Bean
    public DataSource slaveDataSource(){
        DataSourceBuilder dataSourceBuilder = DataSourceBuilder.create();
        return dataSourceBuilder.driverClassName("com.mysql.jdbc.Driver").url("jdbc:mysql://192.168.254.136:3306/test")
                .password("root123").username("root").build();
    }
}

private final DataSource dataSource;
private final DataSource masterDataSource;
private final DataSource slaveDataSource;
public UserRepository(DataSource dataSource,
                      @Qualifier("masterDataSource") DataSource masterDataSource,
                      @Qualifier("slaveDataSource") DataSource slaveDataSource){
    this.dataSource = dataSource;
    this.masterDataSource = masterDataSource;
    this.slaveDataSource = slaveDataSource;
}
```

操作

```JAVA
public boolean save(User user) {
    try {
        Connection connection = dataSource.getConnection();
        connection.setAutoCommit(false);//不自动提交 -- 事务
        PreparedStatement preparedStatement = connection.prepareStatement("Insert into t_test(id,name) values(?,?)") ;
        preparedStatement.setInt(1,user.getId());
        preparedStatement.setString(2,user.getName());
        preparedStatement.executeUpdate();
        preparedStatement.close();
        connection.commit();
        connection.close();
    } catch (SQLException e) {
        e.printStackTrace();
    } finally {
    }
    System.out.println("user:" + user);
    return true;
}
```

## 事务（Transaction） 

-- 就是非自动提交时，控制保护点和commit，rollback

事务

```
事务用于提供数据完整性，并在并发访问下确保数据视图的一致性。
```

重要概念

```
自动提交模式（Auto-commit mode）
事务隔离级别（Transaction isolation levels）
保护点（Savepoints） -- 事务设置的还原点
Annotation 驱动
API 驱动
JDBC 4.0（JSR-221）
```

核心接口

```
驱动接口：java.sql.Drvier
驱动管理：java.sql.DriverManager
数据源：javax.sql.DataSource
数据连接：java.sql.Connection
执行语句：java.sql.Statement
查询结果集：java.sql.ResultSet
元数据接口：java.sql.DatabaseMetaData、java.sql.ResultSetMetaData
```

# 验证

