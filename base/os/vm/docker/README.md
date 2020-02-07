# 微服务docker插件

## pom配置如下插件（docker）

```xml
<?xml version="1.0" encoding="UTF-8"?>

<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.tianwen.springcloud</groupId>
  <artifactId>aihomework-parent</artifactId>
  <version>1.3.2.0508_alpha</version>

  <modules>
    <module>aihomework-api</module>
    <module>aihomework-common</module>
    <module>aihomework-platform</module>
    <module>microservice-onlinehomework</module>
    <module>microservice-offlinehomework</module>
    <module>microservice-knowledge</module>
    <module>microservice-mistakescollection</module>
    <module>microservice-question</module>
    <module>microservice-file</module>
    <module>microservice-scheduled</module>
    <module>openapi-selfstudy</module>
    <module>openapi-errorquestion</module>
    <module>openapi-analysis</module>
    <module>openapi-onlinehomework</module>
    <module>openapi-offlinehomework</module>
  </modules>

  <packaging>pom</packaging>

  <name>aihomework-parent</name>
  <url>http://www.example.com</url>
  <description>AI作业总工程</description>

  <parent>
    <groupId>com.tianwen.springcloud</groupId>
    <artifactId>tw-cloud-parent</artifactId>
    <version>2.1.1</version>
    <relativePath/>
  </parent>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
    <java.version>1.8</java.version>
    <docker.maven.version>1.0.0</docker.maven.version>
    <docker.registry.name.prefix>aihomework</docker.registry.name.prefix>
    <docker.server.ip>192.168.133.27</docker.server.ip>
    <docker.server.registry.port>8089</docker.server.registry.port>
    <docker.repository>http://${docker.server.ip}:${docker.server.registry.port}</docker.repository>
    <docker.host>http://${docker.server.ip}:2375</docker.host>
    <docker.skip>true</docker.skip>
    <maven.build.timestamp.format>yyyyMMddHHmmss</maven.build.timestamp.format>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.projectlombok</groupId>
      <artifactId>lombok</artifactId>
      <version>1.18.6</version>
    </dependency>
    <dependency>
      <groupId>com.github.xiaoymin</groupId>
      <artifactId>swagger-bootstrap-ui</artifactId>
      <version>1.9.3</version>
    </dependency>
    <dependency>
      <groupId>io.github.openfeign</groupId>
      <artifactId>feign-okhttp</artifactId>
      <version>9.4.0</version>
    </dependency>
    <dependency>
      <groupId>org.springframework.cloud</groupId>
      <artifactId>spring-cloud-starter-hystrix</artifactId>
      <version>${spring-cloud-commons.version}</version>
    </dependency>
    <dependency>
      <groupId>org.springframework.cloud</groupId>
      <artifactId>spring-cloud-starter-hystrix-dashboard</artifactId>
      <version>${spring-cloud-commons.version}</version>
    </dependency>
    <!--<dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-devtools</artifactId>
      <version>${springboot.version}</version>
    </dependency>-->
  </dependencies>

  <distributionManagement>
    <repository>
      <id>nexus-releases</id>
      <name>tianwenadmin</name>
      <url>http://192.168.102.222:8081/nexus/content/repositories/releases</url>
    </repository>
    <snapshotRepository>
      <id>nexus-snapshots</id>
      <name>tianwenadmin</name>
      <url>http://192.168.102.222:8081/nexus/content/repositories/snapshots</url>
    </snapshotRepository>
  </distributionManagement>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>io.springfox</groupId>
        <artifactId>springfox-swagger2</artifactId>
        <version>2.9.2</version>
        <exclusions>
          <exclusion>
            <groupId>io.swagger</groupId>
            <artifactId>swagger-annotations</artifactId>
          </exclusion>
        </exclusions>
      </dependency>
      <dependency>
        <groupId>io.springfox</groupId>
        <artifactId>springfox-swagger-ui</artifactId>
        <version>2.6.1</version>
      </dependency>
      <dependency>
        <groupId>io.springfox</groupId>
        <artifactId>springfox-staticdocs</artifactId>
        <version>2.6.1</version>
      </dependency>
      <dependency>
        <groupId>com.tianwen.springcloud</groupId>
        <artifactId>tw-cloud-datasource</artifactId>
        <version>${tianwen.springcloud.version}</version>
        <exclusions>
          <exclusion>
            <artifactId>log4j</artifactId>
            <groupId>log4j</groupId>
          </exclusion>
        </exclusions>
      </dependency>
      <dependency>
        <groupId>com.twasp.config.client</groupId>
        <artifactId>config-client</artifactId>
        <version>1.2.1</version>
      </dependency>
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-stream-binder-kafka</artifactId>
        <version>1.2.1.RELEASE</version>
      </dependency>
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-sleuth-stream</artifactId>
        <version>1.2.2.RELEASE</version>
      </dependency>
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-sleuth</artifactId>
        <version>1.2.2.RELEASE</version>
      </dependency>
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-eureka</artifactId>
        <version>${springcloudstarter.version}</version>
        <exclusions>
          <exclusion>
            <groupId>com.google.guava</groupId>
            <artifactId>guava</artifactId>
          </exclusion>
        </exclusions>
      </dependency>
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-feign</artifactId>
        <version>${springcloudstarter.version}</version>
      </dependency>
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-webmvc</artifactId>
        <version>4.3.17.RELEASE</version>
      </dependency>
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-web</artifactId>
        <version>4.3.17.RELEASE</version>
      </dependency>
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-context</artifactId>
        <version>1.2.0.RELEASE</version>
      </dependency>
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-netflix-core</artifactId>
        <version>1.3.0.RELEASE</version>
      </dependency>
      <dependency>
        <groupId>com.tianwen.springcloud</groupId>
        <artifactId>tw-cloud-common-api</artifactId>
        <version>${tianwen.springcloud.version}</version>
      </dependency>
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-stream-kafka</artifactId>
        <version>1.2.1.RELEASE</version>
      </dependency>

      <dependency>
        <groupId>com.tianwen.springcloud</groupId>
        <artifactId>tw-cloud-microservice-base</artifactId>
        <version>${tianwen.springcloud.version}</version>
        <classifier>api</classifier>
        <exclusions>
          <exclusion>
            <groupId>com.tianwen.springcloud</groupId>
            <artifactId>tw-cloud-datasource</artifactId>
          </exclusion>
          <exclusion>
            <artifactId>config-client</artifactId>
            <groupId>com.twasp.config.client</groupId>
          </exclusion>
          <exclusion>
            <artifactId>idcrt-spring-boot-starter</artifactId>
            <groupId>com.tianwen.springcloud</groupId>
          </exclusion>
        </exclusions>
      </dependency>

      <dependency>
        <groupId>com.tianwen.springcloud</groupId>
        <artifactId>tw-cloud-openapi-base</artifactId>
        <version>${tianwen.springcloud.version}</version>
        <classifier>api</classifier>
        <exclusions>
          <exclusion>
            <groupId>com.tianwen.springcloud</groupId>
            <artifactId>tw-cloud-datasource</artifactId>
          </exclusion>
          <exclusion>
            <groupId>com.tianwen.springcloud</groupId>
            <artifactId>redis</artifactId>
          </exclusion>
          <exclusion>
            <artifactId>config-client</artifactId>
            <groupId>com.twasp.config.client</groupId>
          </exclusion>
          <exclusion>
            <artifactId>idcrt-spring-boot-starter</artifactId>
            <groupId>com.tianwen.springcloud</groupId>
          </exclusion>
        </exclusions>
      </dependency>

      <dependency>
        <groupId>com.tianwen.springcloud</groupId>
        <artifactId>tw-cloud-microservice-user</artifactId>
        <version>${tianwen.springcloud.version}</version>
        <classifier>api</classifier>
        <exclusions>
          <exclusion>
            <groupId>com.tianwen.springcloud</groupId>
            <artifactId>tw-cloud-datasource</artifactId>
          </exclusion>
          <exclusion>
            <groupId>com.tianwen.springcloud</groupId>
            <artifactId>redis</artifactId>
          </exclusion>
          <exclusion>
            <artifactId>config-client</artifactId>
            <groupId>com.twasp.config.client</groupId>
          </exclusion>
          <exclusion>
            <artifactId>idcrt-spring-boot-starter</artifactId>
            <groupId>com.tianwen.springcloud</groupId>
          </exclusion>
        </exclusions>
      </dependency>

      <dependency>
        <groupId>com.tianwen.springcloud</groupId>
        <artifactId>tw-cloud-common-api</artifactId>
        <version>${tianwen.springcloud.version}</version>
        <exclusions>
          <exclusion>
            <artifactId>log4j</artifactId>
            <groupId>log4j</groupId>
          </exclusion>
        </exclusions>
      </dependency>

      <dependency>
        <groupId>org.jsoup</groupId>
        <artifactId>jsoup</artifactId>
        <version>1.8.3</version>
      </dependency>

      <dependency>
        <groupId>com.tianwen.springcloud</groupId>
        <artifactId>tw-cloud-taskscheduled</artifactId>
        <version>1.1.2</version>
        <exclusions>
          <exclusion>
            <artifactId>springfox-swagger2</artifactId>
            <groupId>io.springfox</groupId>
          </exclusion>
          <exclusion>
            <artifactId>springfox-swagger-ui</artifactId>
            <groupId>io.springfox</groupId>
          </exclusion>
          <exclusion>
            <artifactId>log4j</artifactId>
            <groupId>log4j</groupId>
          </exclusion>
          <exclusion>
              <groupId>com.tianwen.springcloud</groupId>
              <artifactId>tw-cloud-taskscheduled</artifactId>
          </exclusion>
        </exclusions>
      </dependency>
      <!--itext pdfTool start-->
      <dependency>
        <groupId>com.itextpdf</groupId>
        <artifactId>itextpdf</artifactId><!--主工具-->
        <version>5.5.13</version>
      </dependency>
      <dependency>
        <groupId>com.itextpdf</groupId>
        <artifactId>itext-asian</artifactId><!--中文支持-->
        <version>5.2.0</version>
      </dependency>
      <!--itext pdfTool start-->
      <!--poi tool start-->
      <dependency>
        <groupId>com.tianwen</groupId>
        <artifactId>aiexcel</artifactId>
        <version>1.5</version>
      </dependency>

      <dependency>
        <groupId>org.apache.poi</groupId>
        <artifactId>poi</artifactId>
        <version>3.16</version>
      </dependency>
      <dependency>
        <groupId>org.apache.poi</groupId>
        <artifactId>poi-ooxml</artifactId>
        <version>3.9</version>
      </dependency>

      <dependency>
        <groupId>net.sf.jxls</groupId>
        <artifactId>jxls-core</artifactId>
        <version>1.0.5</version>
      </dependency>
      <!--poi tool end-->

      <dependency>
        <groupId>io.github.openfeign</groupId>
        <artifactId>feign-core</artifactId>
        <version>9.4.0</version>
      </dependency>

      <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-cache</artifactId>
        <version>1.5.2.RELEASE</version>
      </dependency>

    </dependencies>
  </dependencyManagement>

  <profiles>
    <profile>
      <id>dev</id>
      <properties>
        <package.environment>dev</package.environment>
      </properties>
      <activation>
        <activeByDefault>true</activeByDefault>
      </activation>
    </profile>
    <profile>
      <id>prov</id>
      <properties>
        <package.environment>prov</package.environment>
      </properties>
    </profile>
    <profile>
      <id>test</id>
      <properties>
        <package.environment>test</package.environment>
      </properties>
    </profile>
  </profiles>

  <build>
    <resources>
      <resource>
        <directory>${project.basedir}/src/main/resources</directory>
        <filtering>true</filtering>
      </resource>
    </resources>
    <pluginManagement>
      <plugins>
        <plugin>
          <groupId>com.spotify</groupId>
          <artifactId>docker-maven-plugin</artifactId>
          <version>${docker.maven.version}</version>
          <executions>
            <execution>
              <id>build-image</id>
              <phase>deploy</phase>
              <goals>
                <goal>removeImage</goal>
                <goal>build</goal>
                <goal>push</goal>
              </goals>
            </execution>
          </executions>
          <configuration>
            <serverId>docker-hub</serverId>
            <registryUrl>${docker.repository}</registryUrl>
            <dockerHost>${docker.host}</dockerHost>
            <imageName>${docker.server.ip}:${docker.server.registry.port}/${docker.registry.name.prefix}/${project.artifactId}</imageName>
            <imageTags>
              <imageTag>${project.version}</imageTag>
            </imageTags>
            <baseImage>openjdk:8-jre</baseImage>
            <entryPoint>["java", "-jar", "/${project.build.finalName}-exc.jar"]</entryPoint>
            <resources>
              <resource>
                <targetPath>/</targetPath>
                <directory>${project.build.directory}</directory>
                <include>${project.build.finalName}-exc.jar</include>
              </resource>
            </resources>
          </configuration>
        </plugin>
      </plugins>
    </pluginManagement>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-deploy-plugin</artifactId>
        <configuration>
          <skip>true</skip>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>versions-maven-plugin</artifactId>
        <version>2.3</version>
      </plugin>
      <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>findbugs-maven-plugin</artifactId>
        <version>3.0.0</version>
        <configuration>
          <!-- <configLocation>${basedir}/springside-findbugs.xml</configLocation> -->
          <threshold>High</threshold>
          <effort>Default</effort>
          <findbugsXmlOutput>true</findbugsXmlOutput>
          <!-- findbugs xml输出路径-->
          <findbugsXmlOutputDirectory>target/site</findbugsXmlOutputDirectory>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>

</project>

```

2，子module配置

```xml
<plugin>
                <groupId>com.spotify</groupId>
                <artifactId>docker-maven-plugin</artifactId>
            </plugin>
```

## jenkins的maven配置

```xml
<server>
      <id>docker-hub</id>
      <username>dingguo</username>
      <password>Ding123456</password>
    </server>
```

4，在jenkins上配置任务，设置clean install deploy

5，推送到harbor

# 镜像仓库

## 镜像仓库执行脚本代理

#### 封面

```html
<!DOCTYPE html>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<html>

<head>
    <title>Welcome to Ai作业!</title>
    <style>
        html { height:100%; }
        body { position:relative; color:#333; font-family:"Microsoft YaHei",Tahoma, Geneva, sans-serif; padding: 2% 10%}
        ol, ul, li {margin:0; padding:0; }
        li{list-style:decimal;line-height: 1.7rem;padding: 10px 0; }
        h1{text-align: center;font-weight: 500;}
        a{color: dodgerblue;}
        code{display: block;font-family: Consolas;background: #282a36; color: #33b8ff;padding: .5em 1em;border-radius: 2px;}
        code>p{margin-bottom: 0;color: #fff;}
    </style>
</head>

<body>
    <h1>Ai作业应用安装使用说明</h1>
    <ul>
        <li>安装 <a>curl</a></li>
        <li>
            在centos服务器上执行以下命令就会安装完ai作业的应用
            <code>
                curl -sSL http://192.168.133.27:8666/aihomework-docker-install.sh |sh -xs [s [版本 服务名称]|a [版本]]
            <p>例如安装单个应用：</p>
                curl -sSL http://192.168.133.27:8666/aihomework-docker-install.sh |sh -xs s 1.3.2.0508_alpha openapi-onlinehomework
            <p>例如安装所有应用：</p>
                curl -sSL http://192.168.133.27:8666/aihomework-docker-install.sh |sh -xs a 1.3.2.0508_alpha</code>

        </li>
        <li>在浏览器中输入以下命令查看已启动的服务
            <code>http://IP:9000/</code>
        </li>
        <li>通过以下命令可以查看所有的服务名称和对应的端口
            <code>http://192.168.133.27:8666/aihomework.cfg</code>
        </li>
        <li>注意：~~</li>
    </ul>

</body>

</html>
```

#### 执行脚本镜像脚本

```shell
#!/bin/bash
docker pull nginx
docker rm -f nginxproxy
docker run --restart=always --name nginxproxy -d -p 8666:80 nginx
docker cp /usr/twsm/server-install/aihomework-docker-install.sh nginxproxy:/usr/share/nginx/html/
docker cp /usr/twsm/server-install/aihomework.cfg nginxproxy:/usr/share/nginx/html/
docker cp /usr/twsm/server-install/registry/index.html nginxproxy:/usr/share/nginx/html/
echo "ok!to install aihomework docker only one application: curl -sSL http://192.168.133.27:8666/aihomework-docker-install.sh |sh -xs s 1.3.2.0508_alpha openapi-onlinehomework"
echo "ok!to install aihomework docker all application: curl -sSL http://192.168.133.27:8666/aihomework-docker-install.sh |sh -xs a 1.3.2.0508_alpha"
```



## Harbor安装部署

#### 安装

```shell
1，下载
wget https://storage.googleapis.com/harbor-releases/harbor-offline-installer-v1.6.1.tgz

2，安装docker-compose
curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

3，其他操作
##启动容器
systemctl restart docker
##启动容器
##启动Harbor
# docker-compose start
##停止Harbor
# docker-comose stop
##重启Harbor
# docker-compose restart
docker-compose restart
## 安装harbor镜像仓库
## sh /usr/twsm/harbor/prepare
## nohup sh /usr/twsm/harbor/install.sh > process.txt &2>1 &
## systemctl daemon-reload
## systemctl restart docker
```

#### 重启

```
修改配置后启动

先停止harbor，在修改配置文件harbor.cfg，然后运行prepare脚本应用配置，最后重新创建harbor并运行它。

# docker-compose down -v
# vim harbor.cfg
# prepare
# docker-compose up -d
```

#### 配置

##### docker-compose.yml

```yaml
version: '2'
services:
  log:
    image: goharbor/harbor-log:v1.6.1
    container_name: harbor-log 
    restart: always
    volumes:
      - /var/log/harbor/:/var/log/docker/:z
      - ./common/config/log/:/etc/logrotate.d/:z
    ports:
      - 127.0.0.1:1514:10514
    networks:
      - harbor
  registry:
    image: goharbor/registry-photon:v2.6.2-v1.6.1
    container_name: registry
    restart: always
    volumes:
      - /data/registry:/storage:z
      - ./common/config/registry/:/etc/registry/:z
    networks:
      - harbor
    environment:
      - GODEBUG=netdns=cgo
    depends_on:
      - log
    ports:
      - 5000:5000
    logging:
      driver: "syslog"
      options:  
        syslog-address: "tcp://127.0.0.1:1514"
        tag: "registry"
  postgresql:
    image: goharbor/harbor-db:v1.6.1
    container_name: harbor-db
    restart: always
    volumes:
      - /data/database:/var/lib/postgresql/data:z
    networks:
      - harbor
    env_file:
      - ./common/config/db/env
    depends_on:
      - log
    logging:
      driver: "syslog"
      options:  
        syslog-address: "tcp://127.0.0.1:1514"
        tag: "postgresql"
  adminserver:
    image: goharbor/harbor-adminserver:v1.6.1
    container_name: harbor-adminserver
    env_file:
      - ./common/config/adminserver/env
    restart: always
    volumes:
      - /data/config/:/etc/adminserver/config/:z
      - /data/secretkey:/etc/adminserver/key:z
      - /data/:/data/:z
    networks:
      - harbor
    depends_on:
      - log
    logging:
      driver: "syslog"
      options:  
        syslog-address: "tcp://127.0.0.1:1514"
        tag: "adminserver"
  ui:
    image: goharbor/harbor-ui:v1.6.1
    container_name: harbor-ui
    env_file:
      - ./common/config/ui/env
    restart: always
    volumes:
      - ./common/config/ui/app.conf:/etc/ui/app.conf:z
      - ./common/config/ui/private_key.pem:/etc/ui/private_key.pem:z
      - ./common/config/ui/certificates/:/etc/ui/certificates/:z
      - /data/secretkey:/etc/ui/key:z
      - /data/ca_download/:/etc/ui/ca/:z
      - /data/psc/:/etc/ui/token/:z
    networks:
      - harbor
    depends_on:
      - log
      - adminserver
      - registry
    logging:
      driver: "syslog"
      options:  
        syslog-address: "tcp://127.0.0.1:1514"
        tag: "ui"
  jobservice:
    image: goharbor/harbor-jobservice:v1.6.1
    container_name: harbor-jobservice
    env_file:
      - ./common/config/jobservice/env
    restart: always
    volumes:
      - /data/job_logs:/var/log/jobs:z
      - ./common/config/jobservice/config.yml:/etc/jobservice/config.yml:z
    networks:
      - harbor
    depends_on:
      - redis
      - ui
      - adminserver
    logging:
      driver: "syslog"
      options:  
        syslog-address: "tcp://127.0.0.1:1514"
        tag: "jobservice"
  redis:
    image: goharbor/redis-photon:v1.6.1
    container_name: redis
    restart: always
    volumes:
      - /data/redis:/var/lib/redis
    networks:
      - harbor
    depends_on:
      - log
    logging:
      driver: "syslog"
      options:  
        syslog-address: "tcp://127.0.0.1:1514"
        tag: "redis"
  proxy:
    image: goharbor/nginx-photon:v1.6.1
    container_name: nginx
    restart: always
    volumes:
      - ./common/config/nginx:/etc/nginx:z
    networks:
      - harbor
    ports:
      - 8089:80
      - 443:443
      - 4443:4443
    depends_on:
      - postgresql
      - registry
      - ui
      - log
    logging:
      driver: "syslog"
      options:  
        syslog-address: "tcp://127.0.0.1:1514"
        tag: "proxy"
networks:
  harbor:
    external: false
```

##### habar.cfg

```properties
## Configuration file of Harbor

#This attribute is for migrator to detect the version of the .cfg file, DO NOT MODIFY!
_version = 1.6.0
#The IP address or hostname to access admin UI and registry service.
#DO NOT use localhost or 127.0.0.1, because Harbor needs to be accessed by external clients.
hostname = 192.168.133.27:8089

#The protocol for accessing the UI and token/notification service, by default it is http.
#It can be set to https if ssl is enabled on nginx.
ui_url_protocol = http

#Maximum number of job workers in job service  
max_job_workers = 10 

#Determine whether or not to generate certificate for the registry's token.
#If the value is on, the prepare script creates new root cert and private key 
#for generating token to access the registry. If the value is off the default key/cert will be used.
#This flag also controls the creation of the notary signer's cert.
customize_crt = on

#The path of cert and key files for nginx, they are applied only the protocol is set to https
ssl_cert = /data/cert/server.crt
ssl_cert_key = /data/cert/server.key

#The path of secretkey storage
secretkey_path = /data

#Admiral's url, comment this attribute, or set its value to NA when Harbor is standalone
admiral_url = NA

#Log files are rotated log_rotate_count times before being removed. If count is 0, old versions are removed rather than rotated.
log_rotate_count = 50
#Log files are rotated only if they grow bigger than log_rotate_size bytes. If size is followed by k, the size is assumed to be in kilobytes. 
#If the M is used, the size is in megabytes, and if G is used, the size is in gigabytes. So size 100, size 100k, size 100M and size 100G 
#are all valid.
log_rotate_size = 200M

#Config http proxy for Clair, e.g. http://my.proxy.com:3128
#Clair doesn't need to connect to harbor ui container via http proxy.
http_proxy =
https_proxy =
no_proxy = 127.0.0.1,localhost,ui,registry

#NOTES: The properties between BEGIN INITIAL PROPERTIES and END INITIAL PROPERTIES
#only take effect in the first boot, the subsequent changes of these properties 
#should be performed on web ui

#************************BEGIN INITIAL PROPERTIES************************

#Email account settings for sending out password resetting emails.

#Email server uses the given username and password to authenticate on TLS connections to host and act as identity.
#Identity left blank to act as username.
email_identity = 

email_server = smtp.mydomain.com
email_server_port = 25
email_username = sample_admin@mydomain.com
email_password = abc
email_from = admin <sample_admin@mydomain.com>
email_ssl = false
email_insecure = false

##The initial password of Harbor admin, only works for the first time when Harbor starts. 
#It has no effect after the first launch of Harbor.
#Change the admin password from UI after launching Harbor.
harbor_admin_password = Harbor12345

##By default the auth mode is db_auth, i.e. the credentials are stored in a local database.
#Set it to ldap_auth if you want to verify a user's credentials against an LDAP server.
auth_mode = db_auth

#The url for an ldap endpoint.
ldap_url = ldaps://ldap.mydomain.com

#A user's DN who has the permission to search the LDAP/AD server. 
#If your LDAP/AD server does not support anonymous search, you should configure this DN and ldap_search_pwd.
#ldap_searchdn = uid=searchuser,ou=people,dc=mydomain,dc=com

#the password of the ldap_searchdn
#ldap_search_pwd = password

#The base DN from which to look up a user in LDAP/AD
ldap_basedn = ou=people,dc=mydomain,dc=com

#Search filter for LDAP/AD, make sure the syntax of the filter is correct.
#ldap_filter = (objectClass=person)

# The attribute used in a search to match a user, it could be uid, cn, email, sAMAccountName or other attributes depending on your LDAP/AD  
ldap_uid = uid 

#the scope to search for users, 0-LDAP_SCOPE_BASE, 1-LDAP_SCOPE_ONELEVEL, 2-LDAP_SCOPE_SUBTREE
ldap_scope = 2 

#Timeout (in seconds)  when connecting to an LDAP Server. The default value (and most reasonable) is 5 seconds.
ldap_timeout = 5

#Verify certificate from LDAP server
ldap_verify_cert = true

#The base dn from which to lookup a group in LDAP/AD
ldap_group_basedn = ou=group,dc=mydomain,dc=com

#filter to search LDAP/AD group
ldap_group_filter = objectclass=group

#The attribute used to name a LDAP/AD group, it could be cn, name
ldap_group_gid = cn

#The scope to search for ldap groups. 0-LDAP_SCOPE_BASE, 1-LDAP_SCOPE_ONELEVEL, 2-LDAP_SCOPE_SUBTREE
ldap_group_scope = 2

#Turn on or off the self-registration feature
self_registration = on

#The expiration time (in minute) of token created by token service, default is 30 minutes
token_expiration = 30

#The flag to control what users have permission to create projects
#The default value "everyone" allows everyone to creates a project. 
#Set to "adminonly" so that only admin user can create project.
project_creation_restriction = everyone

#************************END INITIAL PROPERTIES************************

#######Harbor DB configuration section#######

#The address of the Harbor database. Only need to change when using external db.
db_host = postgresql

#The password for the root user of Harbor DB. Change this before any production use.
db_password = root123

#The port of Harbor database host
db_port = 5432

#The user name of Harbor database
db_user = postgres

##### End of Harbor DB configuration#######

##########Redis server configuration.############

#Redis connection address
redis_host = redis

#Redis connection port
redis_port = 6379

#Redis connection password
redis_password = 

#Redis connection db index
#db_index 1,2,3 is for registry, jobservice and chartmuseum. 
#db_index 0 is for UI, it's unchangeable
redis_db_index = 1,2,3

##########Redis server configuration.############

##########Clair DB configuration############

#Clair DB host address. Only change it when using an exteral DB.
clair_db_host = postgresql
#The password of the Clair's postgres database. Only effective when Harbor is deployed with Clair.
#Please update it before deployment. Subsequent update will cause Clair's API server and Harbor unable to access Clair's database.
clair_db_password = root123
#Clair DB connect port
clair_db_port = 5432
#Clair DB username
clair_db_username = postgres
#Clair default database
clair_db = postgres

#The interval of clair updaters, the unit is hour, set to 0 to disable the updaters.
clair_updaters_interval = 12

##########End of Clair DB configuration############

#The following attributes only need to be set when auth mode is uaa_auth
uaa_endpoint = uaa.mydomain.org
uaa_clientid = id
uaa_clientsecret = secret
uaa_verify_cert = true
uaa_ca_cert = /path/to/ca.pem


### Harbor Storage settings ###
#Please be aware that the following storage settings will be applied to both docker registry and helm chart repository.
#registry_storage_provider can be: filesystem, s3, gcs, azure, etc.
registry_storage_provider_name = filesystem
#registry_storage_provider_config is a comma separated "key: value" pairs, e.g. "key1: value, key2: value2".
#To avoid duplicated configurations, both docker registry and chart repository follow the same storage configuration specifications of docker registry.
#Refer to https://docs.docker.com/registry/configuration/#storage for all available configuration.
registry_storage_provider_config =
#registry_custom_ca_bundle is the path to the custom root ca certificate, which will be injected into the truststore
#of registry's and chart repository's containers.  This is usually needed when the user hosts a internal storage with self signed certificate.
registry_custom_ca_bundle = 

#If reload_config=true, all settings which present in harbor.cfg take effect after prepare and restart harbor, it overwrites exsiting settings.
#reload_config=true
#Regular expression to match skipped environment variables
#skip_reload_env_pattern=(^EMAIL.*)|(^LDAP.*)

```



#### 常见问题

###### 2375 [/192.168.133.27] failed

```shell
2375 [/192.168.133.27] failed: Connection refused: connect

-------解决
[root@ai harbor]# vi /usr/lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix://var/run/docker.sock \
          --insecure-registry 192.168.133.27:8089 \
          --add-runtime docker-runc=/usr/libexec/docker/docker-runc-current \
          --default-runtime=docker-runc \
[root@ai harbor]# systemctl daemon-reload
[root@ai harbor]# systemctl restart docker

记得关防火墙
```

###### resource is denied

```shell
6250e4399f29: Preparing 
d38f3d5a39fb: Preparing 
fe60061c6c4e: Preparing 
7d63f8777ebf: Preparing 
1b958b53b256: Preparing 
2c719774c1e1: Waiting 
ec62f19bb3aa: Waiting 
f94641f1fe1f: Waiting 
denied: requested access to the resource is denied

-------解决
1，push的格式不对，按如下操作：
docker tag dingguo/openapi-onlinehomework:latest 192.168.133.27:8089/aihomework【项目名】/openapi-onlinehomework:1.3.2.0508_alpha
docker push 192.168.133.27:8089/aihomework/openapi-onlinehomework:1.3.2.0508_alpha

2，maven的setting.xml配置（账号可以通过harbor创建）
<server>
      <id>docker-hub</id>
      <username>dingguo</username>
      <password>Ding123456</password>
    </server>
```

###### incorrect username or password

```shell
docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: dingguo
Password: 
Error response from daemon: Get https://registry-1.docker.io/v2/: unauthorized: incorrect username or password

-----------解决
[root@ai harbor]# docker login 192.168.133.27:8089
Username: dingguo
Password: 
Login Succeeded

```

###### login 443: connect

```shell
[root@ai harbor]# docker login 192.168.133.27:8089
Username: Dingguo
Password: 
Error response from daemon: Get https://192.168.133.27/v1/users/: dial tcp 192.168.133.27:443: connect: connection refused

-------解决
[root@ai harbor]# vi /usr/lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd-current \
          --insecure-registry 192.168.133.27:8089 \ ##添加此行
          --add-runtime docker-runc=/usr/libexec/docker/docker-runc-current \
[root@ai harbor]# systemctl daemon-reload
[root@ai harbor]# service docker restart

[root@node1 proxy]# vi /etc/sysconfig/docker
OPTIONS='--selinux-enabled --log-driver=journald --signature-verification=false --insecure-registry=192.168.133.31:8089'

```

###### docker build 报错

```shell
kernel:unregister_netdevice: waiting for lo to become free. Usage count = 1

--------解决
更新操作系统
yum -y update

```

###### docker unable to configure the Docker daemon with file /etc/docker/daemon

```shell
unable to configure the Docker daemon with file /etc/docker/daemon.json: the following directives are specified both as a

--------解决
/usr/lib/systemd/system/docker.service和/etc/docker/daemon.json重复配置同一个属性，删除一个就可以了

/usr/lib/systemd/system/docker.service \
```

###### tls: oversized record received with length 20527 。

```
centos6：
vi /etc/sysconfig/docker
--------------------------
other_args="--insecure-registry 192.168.133.27:8089 --insecure-registry 192.168.133.31:8089" ##配置多个镜像仓库

```

###### 外网IP

```
将harbor.cfg上的hostname修改成外网
然后./prepare即可
```

#### 清理磁盘

```
https://www.cnblogs.com/xzkzzz/p/10151482.html
1、编辑 common/config/registry/config.yml文件
注释掉token
4、 清理已删除未使用的清单
执行下面的命令
docker run --network="host" -it -v /data/registry:/registry -e REGISTRY_URL=http://127.0.0.1:5000 mortensrasmussen/docker-registry-manifest-cleanup
5、清理以删除现在不再与清单关联的blob
执行下面的命令
docker run -it --name gc --rm --volumes-from registry vmware/registry-photon:v2.6.2-v1.4.0 garbage-collect /etc/registry/config.yml

6、清理完后，必须删掉/data目录的内容，否则客户端拉不下镜像
```

#### 参考

[镜像仓库开源组件](https://blog.csdn.net/Andriy_dangli/article/details/84381383#2VMware_Harbor_17)

#### 配置多个非ssl的镜像仓库

<https://juejin.im/entry/57bce3821532bc0065825bff>

<https://www.imooc.com/article/270050>

```
Docker 如果需要从非SSL镜像源中拉取镜像是需要配置–insecure-registry 参数的，在Docker 安装与Registry V2私有仓库搭建 已经使用过。

解决这个问题的最简单方式是修改docker的启动脚本，添加-H tcp://127.0.0.1:2375 -H unix:///var/run/docker.sock --insecure-registry 172.18.2.40:5000 内容。

[root@M-CentOS72-36 ~]# vim /usr/lib/systemd/system/docker.service

[Service]
Type=notify
# the default is not to use systemd for cgroups because the delegate issues still
# exists and systemd currently does not support the cgroup feature set required
# for containers run by docker
ExecStart=/usr/bin/dockerd -H tcp://127.0.0.1:2375 -H unix:///var/run/docker.sock --insecure-registry 172.18.2.40:5000
那么如果要从多个非SSL镜像源中拉取镜像又需要怎么配置呢？其实很简单只需要再加一个–insecure-registry参数即可。
--insecure-registry 172.18.2.40:5000 --insecure-registry xx.xxx.com:5000

[root@M-CentOS72-36 ~]# vim /usr/lib/systemd/system/docker.service

[Service]
Type=notify
# the default is not to use systemd for cgroups because the delegate issues still
# exists and systemd currently does not support the cgroup feature set required
# for containers run by docker
ExecStart=/usr/bin/dockerd -H tcp://127.0.0.1:2375 -H unix:///var/run/docker.sock --insecure-registry 172.18.2.40:5000 --insecure-registry xx.xxx.com:5000


[root@M-CentOS72-36 ~]# systemctl daemon-reload
[root@M-CentOS72-36 ~]# systemctl start docker
重启完Docker 就可以从xx.xxx.com:5000中拉取镜像。拉取完镜像之后最好为这些镜像重新打上新的标签并推送到自建的Registry 私服。这样只需要在一台机器上添加一次其他镜像源，而不需要所有机器都添加多个镜像源，其他机器统一从Registry 私服中拉取。添加–insecure-registry 是要重启Docker 服务，若是所有机器的Docker 服务都要重启，影响非常大。

为什么这么多非SSL的镜像源呢？因为这种镜像基本都是为公司内部服务，都是内网服务没有打算对外公开，所以没有必要上https。另一个原因就是沃通不再签发免费的SSL证书🐶。
```

#### 容器安全扫描

<https://blog.51cto.com/dangzhiqiang/2097103>

# 镜像使用

#### 使用服务器安装docker

<https://www.yuque.com/wjwcloud/note/uwuqd2>

#### 使用服务器配置

```shell
1，vim /etc/sysconfig/docker

# /etc/sysconfig/docker
#
# Other arguments to pass to the docker daemon process
# These will be parsed by the sysv initscript and appended
# to the arguments list passed to docker -d

other_args=" --insecure-registry 192.168.102.116:5000 --insecure-registry 192.168.133.27:8089"
~                                                                                         
2，[root@NBACBA0 ~]# service restart docker

3，[root@NBACBA0 ~]# docker pull 192.168.133.27:8089/aihomework/microservice-offlinehomework:1.3.2.0508_alpha

```

#### 脚本

服务器网络配置

编辑：vi /etc/sysconfig/iptables ，添加:DOCKER - [0:0]

```properties
# Generated by iptables-save v1.4.7 on Tue May 14 13:39:25 2019
*nat
:PREROUTING ACCEPT [57926:8896724]
:POSTROUTING ACCEPT [756988:45430231]
:OUTPUT ACCEPT [756988:45430231]
:DOCKER - [0:0]
-A PREROUTING -m addrtype --dst-type LOCAL -j DOCKER
-A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE
-A OUTPUT ! -d 127.0.0.0/8 -m addrtype --dst-type LOCAL -j DOCKER
COMMIT
# Completed on Tue May 14 13:39:25 2019
# Generated by iptables-save v1.4.7 on Tue May 14 13:39:25 2019
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [2462:162052]
:DOCKER - [0:0]
-A INPUT -p tcp -m tcp --dport 8016 -j ACCEPT
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 8822 -j ACCEPT
-A INPUT -j REJECT --reject-with icmp-host-prohibited
-A FORWARD -o docker0 -j DOCKER
-A FORWARD -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i docker0 ! -o docker0 -j ACCEPT
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
-A FORWARD -i docker0 -o docker0 -j ACCEPT
COMMIT
# Completed on Tue May 14 13:39:25 2019
~                                                                                                                                                                                                        
~                                                                                                                                                                                                        
~                                                                                                                                                                                                        
~                                         
```

##### 下载镜像并安装容器脚本

```shell
#!/bin/bash
#####################################
#@author liuqianding
#@version 1.0
#@description application docker shell
######################################
##1.3.2.0508_alpha
aihomework_version=$2
aihomework_images_registry=192.168.133.27:8089
aihomework_project=aihomework
aihomework_proxy_server=http://192.168.133.27:8666
path=`pwd`
mkdir -p $path/logs/containerid
logspath=$path/logs/catalina.out
containerid=$path/logs/containerid
##镜像名称
IMAGENAMES=`curl -sSL $aihomework_proxy_server/aihomework.cfg | grep "appname" | awk -F "=" '{print $2}'`

function installallapplication()
{
        IMAGEARRAY=(${IMAGENAMES//,/})
	for IMAGENAME in ${IMAGEARRAY[@]}
	do
		installdockerimage $IMAGENAME
	done
}

function installdockerimage()
{
	port=`curl -sSL $aihomework_proxy_server/aihomework.cfg | grep $1".port" | awk -F "=" '{print $2}'`
	docker rm -f $1
	docker rmi -f $aihomework_images_registry/$aihomework_project/$1:$aihomework_version
	##下载镜像
	docker pull $aihomework_images_registry/$aihomework_project/$1:$aihomework_version
	rm -rf $containerid/$1
	docker create --name=$1 -p $port:$port -v /data/twcloud/logs:/data/twcloud/logs --net=host --restart=always --privileged=true $aihomework_images_registry/$aihomework_project/$1:$aihomework_version>$containerid/$1
	docker start `cat $containerid/$1 `
}

function installdocker()
{
	if [ -z "`whereis docker | awk -F ':' '{print $2}'`" ]; then
	   if [ `rpm -q centos-release|cut -d- -f3` != 7 ]; then
	      curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh -
	      echo 'docker install success'
	   else
	      yum install -y docker
	   fi
	fi
	
#镜像仓库配置
if [ -z "`cat /etc/sysconfig/docker | grep 'other_args'`" ]; then
   cat > /etc/docker/daemon.json <<EOF
        {
           "registry-mirrors":[
            "https://tqdx01q5.mirror.aliyuncs.com"
        ],
	 "insecure-registries":[
        	  "$aihomework_images_registry"
 	   ]
	}
EOF
else
   cat >> /etc/sysconfig/docker <<EOF
       other_args="$other_args --insecure-registry $aihomework_images_registry"
EOF
fi
	if [ `rpm -q centos-release|cut -d- -f3` = 7 ];then
	   systemctl restart docker
	   systemctl enable docker
	else
	   service docker start
	   echo "service docker start" >> /etc/rc.local
	fi
}

##监控
function monitor()
{
	echo "monitor"
	docker rm -f monitordocker
	docker run -d -p 9000:9000 --name=monitordocker --restart=always --privileged -v /var/run/docker.sock:/var/run/docker.sock uifd/ui-for-docker
}

#下载镜像
function downloaddockerimage()
{
	docker pull $aihomework_images_registry/aihomework/microservice-onlinehomework:$aihomework_version
	docker pull $aihomework_images_registry/aihomework/openapi-offlinehomework:$aihomework_version
	docker pull $aihomework_images_registry/aihomework/openapi-selfstudy:$aihomework_version
	docker pull $aihomework_images_registry/aihomework/openapi-errorquestion:$aihomework_version
	docker pull $aihomework_images_registry/aihomework/microservice-file:$aihomework_version
	docker pull $aihomework_images_registry/aihomework/microservice-offlinehomework:$aihomework_version
	docker pull $aihomework_images_registry/aihomework/openapi-analysis:$aihomework_version
	docker pull $aihomework_images_registry/aihomework/microservice-question:$aihomework_version
	docker pull $aihomework_images_registry/aihomework/openapi-onlinehomework:$aihomework_version
	docker pull $aihomework_images_registry/aihomework/microservice-onlinehomework:$aihomework_version
	docker pull $aihomework_images_registry/aihomework/microservice-scheduled:$aihomework_version
	docker pull $aihomework_images_registry/aihomework/microservice-knowledge:$aihomework_version
	docker pull $aihomework_images_registry/aihomework/microservice-mistakescollection:$aihomework_version
}

start=`date +%s`
while [ $# -ne 0 ]
do
   case $1 in 
   a)
        ## sh aihomework-docker-install.sh -all 1.3.2.0508_alpha
	installdocker
	installallapplication
	monitor
	exit 0;
   ;;
   s)
        ## sh aihomework-docker-install.sh -s 1.3.2.0508_alpha openapi-onlinehomework
	installdocker
	installdockerimage $3
	exit 0;
   ;;
   esac
   shift
done   
end=`date +%s` 
dif=$[end - start]
echo "cce安装耗时:$dif 秒"
```

配置文件

```properties
appname=microservice-onlinehomework
appname=openapi-offlinehomework
appname=openapi-selfstudy
appname=openapi-errorquestion
appname=microservice-file
appname=microservice-offlinehomework
appname=openapi-analysis
appname=microservice-question
appname=openapi-onlinehomework
appname=microservice-scheduled
appname=microservice-knowledge
appname=microservice-mistakescollection

microservice-onlinehomework.port=9520
microservice-question.port=9521
microservice-offlinehomework.port=9522
microservice-scheduled.port=9526
microservice-knowledge.port=9524
microservice-mistakescollection.port=9523
microservice-file.port=9525
openapi-offlinehomework.port=9527
openapi-selfstudy.port=9530
openapi-errorquestion.port=9531
openapi-analysis.port=9529
openapi-onlinehomework.port=9528
```

# docker和jenkins

#### 后端服务打包

（略）

#### 前端打包

1，注意nodejs和gcc的版本，若版本不对，修改gcc的版本：

```shell
cd  /usr/local/src
wget  http://ftp.gnu.org/gnu/gcc/gcc-7.3.0/gcc-7.3.0.tar.gz
tar zxvf  gcc-7.3.0.tar.gz
cd 
./contrib/download_prerequisites   #作用:下载一些需要依赖的库，以及做好配置工作
mkdir build  
cd build  
../configure -enable-checking=release -enable-languages=c,c++ -disable-multilib  
make  #（多cpu可考虑加-j cpunumber，另外编译时间会很久，终端断开比较恼火，建议使用screen虚拟终端下编译）
make install  
```

2，shell命令配置

```shell
npm cache clean --force
rm -rf node_modules
rm -rf package-lock.json
npm install
npm run build
```

#### docker 异常

```properties
Docker删除images,重新部署镜像时,ERROR,Unable to enable SKIP DNAT rule

重启docker服务:
service docker restart
```

#### 修改docker的默认存储位置

```
一、做软连接，关闭docker服务
    systemctl stop docker       ##关闭docker服务

    mv /var/lib/docker /var/lib/docker.bak   ##备份当前docker镜像文件目录

    ln -s /data/docker  /var/lib/docker         ##设置软连接，其中/data/docker目录为新的存放docker镜像目录
    cp -rp /var/lib/docker.bak /data/docker        ##将旧的docker文件拷贝过去

二、修改docker镜像存储位置
    关闭docker服务

    systemctl stop docker   

 1、可通过修改/etc/sysconfig/docker文件实现
        OPTIONS='–graph="/data/docker-data" –selinux-enabled –log-driver=journald –signature-verification=false –insecure-registry 10.168.168.27'

        其中–graph="/data/docker-data"  指定docker新存放路径为/data/docker-data

        mv /var/lib/docker /data/docker-data    ##将docker镜像迁移到新目录

        systemctl start docker       ##启动docker服务

        docker info  ##验证目录是否更改        

      [root@node34 ~]# docker info | grep 'Root Dir'

      Docker Root Dir: /data/docker-data
      从上面可以看出目录已经改变
        docker images    ##查看镜像是否存在
2、通过修改文件/etc/docker/daemon.json 实现
 
 

    vim  /etc/docker/daemon.json 

    {

        "graph":"/data/docker-data"

    }
   

       mv /var/lib/docker /data/docker-data    ##将docker镜像迁移到新目录

       systemctl start docker       ##启动docker服务

       docker info  ##验证目录是否更改        

      docker images    ##查看镜像是否存在

  注意事项: 最新版本docker中，变量由graph变为data-root
```

218.77.50.49:18089

218.77.50.49:18666

# docker-compose

配置公共变量：<https://www.cnblogs.com/sparkdev/p/9826520.html>

# 清理docker

<https://www.cnblogs.com/sparkdev/p/9177283.html>

# 网络通信

<https://www.hi-linux.com/posts/58668.html>

<https://blog.csdn.net/smooth00/article/details/82842234>

<https://blog.51cto.com/wzlinux/2112061>

<https://www.cnblogs.com/boshen-hzb/p/10108366.html>

<https://yeasy.gitbooks.io/docker_practice/compose/compose_file.html>

<https://github.com/YummyCookhouse/kubernetes/blob/master/flannel/entrypoint.sh> docker与flannel结合

![Docker è·¨ä¸"æºç½ç" overlay(åå­)](https://s1.51cto.com/images/blog/201805/03/2dfb2711749383bb3a4976982c2a42f0.jpg?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)

## 宿主机通信

### flannel网络模型

![img](https://images2015.cnblogs.com/blog/907596/201705/907596-20170516083247463-826250588.png)

### overlay网络模型

#### Docker Swarm

![img](https://images2018.cnblogs.com/blog/435188/201805/435188-20180508183904159-752875281.jpg)

# docker 原理

<http://www.alloyteam.com/2019/07/13885/>

<https://i4t.com/4248.html>

## docker 版本

#yum list docker-ce --showduplicates | sort -r　
#yum list docker-ce-cli --showduplicates | sort -r　
#yum list containerd.io --showduplicates | sort -r