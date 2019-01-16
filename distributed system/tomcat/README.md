# 一、整体框架

![1543125108189](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1543125108189.png)

# 二、配置

## server.xml

## tomcat静态资源服务器配置|虚拟目录

一般情况：修改Tomcat服务器conf目录下server.xml文件，添加Context标签：

``` xml
<Host name="localhost" appBase="webapps" unpackWARs="true" autoDeploy="true">  
    <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs" prefix="localhost_access_log."   
        suffix=".txt" pattern="%h %l %u %t "%r" %s %b" />  
    <!--在Host标签下加入Context标签，path指的是服务器url请求地址（例如127.0.0.1/data），  
        docBase指的是服务器文件的路径，reloadable指的是在omcat不重启的情况下实时同步本地目录-->          
    <Context path="/data" docBase="E:/tmp" reloadable="true" debug="0" crossContext="true"/>  
</Host>  
```

设置web.xml，若有spring，这DispatcherServlet启动要比DefaultServlet这个慢 。

``` xml
<servlet>
<servlet-name>servlet_static</servlet-name>
<servlet-class>org.apache.catalina.servlets.DefaultServlet</servlet-class>
<load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
<servlet-name>servlet_static</servlet-name>
<url-pattern>*.css</url-pattern>
<url-pattern>*.js</url-pattern>
<url-pattern>*.htm</url-pattern>
<url-pattern>*.html</url-pattern>
<url-pattern>*.xhtml</url-pattern>
<url-pattern>*.ico</url-pattern>
<url-pattern>*.ICO</url-pattern>
<url-pattern>*.jpg</url-pattern>
<url-pattern>*.JPG</url-pattern>
<url-pattern>*.jpeg</url-pattern>
<url-pattern>*.JPEG</url-pattern>
<url-pattern>*.png</url-pattern>
<url-pattern>*.PNG</url-pattern>
<url-pattern>*.swf</url-pattern>
<url-pattern>*.SWF</url-pattern>
<url-pattern>*.gif</url-pattern>
<url-pattern>*.GIF</url-pattern>
</servlet-mapping>
```

