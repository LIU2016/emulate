[TOC]

# 1，跨域

## 一、什么是跨域

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

## 二、nginx跨域

可以通过修改nginx下/conf/proxy/ 下的配置信息来解决这种问题。如访问服务器的nginx配置目录/usr/local/nginx/conf/proxy，找到相应服务端的location / 项目，在下面加上配置:

```properties
add_header 'Access-Control-Allow-Headers'  '*'; 
```


后续发现火狐等有些浏览器不支持通配符*的方式，所以更改配置为不使用通配符，需将需要的header都配置一遍。比如请求头包括下边几个则需要配置为：

```properties
add_header 'Access-Control-Allow-Headers' 'X-User-Account,X-Device-Id,X-Device-Type';
```

![1542778843429](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542778843429.png)

## 三、tomcat跨域

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

## **四、使用ajax的jsonp**

缺点就是：请求方式只能是get请求。

前端代码

![img](https://images2015.cnblogs.com/blog/1135647/201706/1135647-20170607172018200-1525203141.png)

 服务器代码

![img](https://images2015.cnblogs.com/blog/1135647/201706/1135647-20170607172045528-363980482.png)

## **五、使用cors**

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

## 六、flashplayer访问跨域

文件crossdomain.xml为安全策略文件，使用时需放置在网站根目录下。作用是定义该域名下面的xml文件，json文件，m3u8文件是否允许其它网站的flashplayer来访问。这个文件是格式是由adobe公司制定的。

Xml代码：

```xml
<?xml version="1.0" encoding="utf-8"?>
<cross-domain-policy> 
	<allow-access-from domain="*.ckplayer.com"/>  
	<allow-access-from domain="*.ckvcms.com"/> 
</cross-domain-policy>
```

# 2，位、字节、字符、字符集、编码的关系

## 1，位

> 数据存储的最小单位。每个二进制数字0或者1就是1个位；

## 2，字节

> 8个位构成一个字节；即：1 byte (字节)= 8 bit(位)；   
>
> 1 KB = 1024 B(字节)；   
>
> 1 MB = 1024 KB;   (2^10 B)   
>
> 1 GB = 1024 MB;  (2^20 B)   
>
> 1 TB = 1024 GB;   (2^30 B)

## 3，字符

> a、A、中、+、*、の......均表示一个字符；
>
> 一般 utf-8 编码下，一个汉字 字符 占用 3 个 字节；
>
> 一般 gbk 编码下，一个汉字  字符  占用 2 个 字节；

## 4、字符集

> 即各种各个字符的集合，也就是说哪些汉字，字母（A、b、c）和符号（空格、引号..）会被收入标准中；

## 5、编码

规定每个“字符”分别用一个字节还是多个字节存储，用哪些字节来存储，这个规定就叫做“编码”。（其实际是对字符集中字符进行编码，即：每个字符用二进制在计算中表示存储）；  

通俗的说：编码就是按照规则对字符进行翻译成对应的二进制数，在计算器中运行存储，用户看的时候（比如浏览器），用对应的编码解析出来用户能看懂的；  

（1）标准ASCii字符集：有96个打印字符，和32个控制字符组成；一共96+32=128个；用7位二进制数来对每1个字符进行编码；而由于7位还还不够1个字节，而电脑的内部常用字节来用处理，每个字节中多出来的最高位用0替代；

0 000   0000.........................0           

0 111   1111..........................127；   从0----127，来表示128个ACSii编码；           

比如：

字符 'A'----------在计算器内部用0100 0001 （65）来表示；                      

字符'a'-----------在计算器内部用0 110 0001 （97）来表示；           

注意：'10'在计算器内部是没有编码的，因为它是字符串，而不是单个字符。可以分别对1,0字符编码存储；   

（2）扩展ASCii字符集：将标准的ASCii最高位1，得到十进制代码128---255（1 000 0000----1 111 1111）；所以字符集一共有0---255,  256个字符；    

（3）gb2312字符集: 所有汉字字符在计算机内部采用2个字节来表示，每个字节的最高位规定为1【正好与标准ASCii字符（最高位是0）不重叠，并兼容】，不支持繁体字；           

所以：gb2312表示汉字的编码为：[129--255][129--255]  (两个字节，每个字节最高位是1)；小于127的字符，与ASCii编码相同；    

（4）gbk字符集：gb2312的扩充，兼容gb2312，除了收录gb2312所有的字符外，还收录了其他不常见的汉字、繁体字等；          

 gbk中字符是一个或两个字节，单字节字符00--7F（0---127）这个区间和ASCII是一样的；           

双字节字符的第一个字节是在81--FE（129--254）之间。通过这个可以判断是单字节还是双字节；                 

即：在gbk字符编码，如果第一个字节是>128的，则再往后找一个字节，组成汉字；如果第一个字节<128,则表示的是一个单字节（此时和ASCII是一样的）；