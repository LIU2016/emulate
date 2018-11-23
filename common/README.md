# 一，跨域

## 什么是跨域

> 浏览器从一个域名的网页去请求另一个域名的资源时，域名、端口、协议任一不同，都是跨域。 
>
> 域名： 
>
> 　主域名不同 http://www.baidu.com/index.html –>http://www.sina.com/test.js 
> 　子域名不同 http://www.666.baidu.com/index.html –>http://www.555.baidu.com/test.js 
> 　域名和域名ip http://www.baidu.com/index.html –>http://180.149.132.47/test.js 
>
> 端口： 
>
> 　http://www.baidu.com:8080/index.html–> http://www.baidu.com:8081/test.js 
>
> 协议： 
>
> 　http://www.baidu.com:8080/index.html–> https://www.baidu.com:8080/test.js 
>
> 备注： 
>
> 　1、端口和协议的不同，只能通过后台来解决 
>
> ​    2、localhost和127.0.0.1虽然都指向本机，但也属于跨域

1) ajax请求信息如下：

```javascript
$.ajax({
    type:"post",
    url:"http://192.168.102.241/portal/ClientApi/getPictureCatalog",
    headers: {
        'X-User-Account': "C05CCE6600000001315",
        "X-Device-Id": "Android_eb8ceaefd1e7c9a9",
        "X-Device-Type": "1"
    },
    data:JSON.stringify({
        "catalogType":'2'
    }),
    success: function(data) {
        alert(data)
    },
    error: function(err) {
        alert(2)
    }
})
```

2) 浏览器控制台报错如图：

![1542778729200](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542778729200.png)

# 二、nginx跨域

可以通过修改nginx下/conf/proxy/ 下的配置信息来解决这种问题。如访问服务器的nginx配置目录/usr/local/nginx/conf/proxy，找到相应服务端的location / 项目，在下面加上配置:

```properties
add_header 'Access-Control-Allow-Headers'  '*'; 
```


后续发现火狐等有些浏览器不支持通配符*的方式，所以更改配置为不使用通配符，需将需要的header都配置一遍。比如请求头包括下边几个则需要配置为：

```properties
add_header 'Access-Control-Allow-Headers' 'X-User-Account,X-Device-Id,X-Device-Type';
```

![1542778843429](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542778843429.png)

# 三、tomcat跨域

项目添加依赖包：

```xml
<dependency>
   <groupId>com.thetransactioncompany</groupId>
   <artifactId>java-property-utils</artifactId>
   <version>1.9.1</version>
</dependency>
<dependency>
   <groupId>com.thetransactioncompany</groupId>
   <artifactId>cors-filter</artifactId>
   <version>2.5</version>
</dependency>
```

项目的web.xml配置：

```xml
<!--跨域 start-->
<filter>
   <filter-name>CORS</filter-name>
   <filter-class>com.thetransactioncompany.cors.CORSFilter</filter-class>
   <init-param>
      <param-name>cors.allowOrigin</param-name>
      <param-value></param-value>
   </init-param>
   <init-param>
      <param-name>cors.supportedMethods</param-name>
      <param-value>GET, POST, HEAD, PUT, DELETE,OPTIONS,TRACE</param-value>
   </init-param>
   <init-param>
      <param-name>cors.supportedHeaders</param-name>
      <param-value>
         Accept, Origin, X-Requested-With, Content-Type, Last-Modified,X-User-Account,X-Device-Id,X-Device-Type,X-Schedule-ID,X-PC-Authenticate-key
      </param-value>
   </init-param>
   <init-param>
      <param-name>cors.exposedHeaders</param-name>
      <param-value>Set-Cookie</param-value>
   </init-param>
   <init-param>
      <param-name>cors.supportsCredentials</param-name>
      <param-value>true</param-value>
   </init-param>
</filter>
<filter-mapping>
   <filter-name>CORS</filter-name>
   <url-pattern>/</url-pattern>
</filter-mapping>
<!--跨域 end-->
```

# **四、使用ajax的jsonp**

缺点就是：请求方式只能是get请求。

前端代码

![img](https://images2015.cnblogs.com/blog/1135647/201706/1135647-20170607172018200-1525203141.png)

 服务器代码

![img](https://images2015.cnblogs.com/blog/1135647/201706/1135647-20170607172045528-363980482.png)

# **五、使用cors**

前端代码

![img](https://images2015.cnblogs.com/blog/1135647/201706/1135647-20170607172341575-2077889877.png)

使用该方式的特点：与前两种方式相比，前端代码和未处理跨域前一样，即普通的ajax请求，但服务器代码添加了一段解决跨域的代码   

```java
// 设置：Access-Control-Allow-Origin头，处理Session问题
        response.setHeader("Access-Control-Allow-Origin", request.getHeader("Origin"));
        response.setHeader("Access-Control-Allow-Credentials", "true");
        response.setHeader("P3P", "CP=CAO PSA OUR");
        if (request.getHeader("Access-Control-Request-Method") != null && "OPTIONS".equals(request.getMethod())) {
            response.addHeader("Access-Control-Allow-Methods", "POST,GET,TRACE,OPTIONS");
            response.addHeader("Access-Control-Allow-Headers", "Content-Type,Origin,Accept");
            response.addHeader("Access-Control-Max-Age", "120");
        }
```

**在springmvc中配置拦截器**
创建跨域拦截器实现HandlerInterceptor接口，并实现其方法，在请求处理前设置头信息，并放行。

![img](https://images2015.cnblogs.com/blog/1135647/201706/1135647-20170607172500653-793475022.png)

在springmvc的配置文件中配置拦截器，注意拦截的是所有的文件

![img](https://images2015.cnblogs.com/blog/1135647/201706/1135647-20170607172515887-1312141011.png)

# 六、flashplayer访问跨域

文件crossdomain.xml为安全策略文件，使用时需放置在网站根目录下。作用是定义该域名下面的xml文件，json文件，m3u8文件是否允许其它网站的flashplayer来访问。这个文件是格式是由adobe公司制定的。

Xml代码：

```xml
<?xml version="1.0" encoding="utf-8"?>
<cross-domain-policy> 
	<allow-access-from domain="*.ckplayer.com"/>  
	<allow-access-from domain="*.ckvcms.com"/> 
</cross-domain-policy>
```

