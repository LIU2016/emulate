[TOC]

# 一、背景

> http协议是无状态的；
> 用cookie 和 session 解决了无状态的问题。

# 二、关于cookie和session的联系

## cookie

cookie包含哪些信息：
名字、值、过期时间、路径、域
（路径和域控制了cookie的范围）。
cookie会带到http请求头中发送给服务器端 。
如果cookie没有设置过期时间的话，那么cookie的默认生命周期是浏览器的会话（关闭浏览器）。
cookie的过期时间大于浏览器的会话的时间，cookie就会存在磁盘中。

## session

1，session是容器对象，客户端在请求服务器的时候，服务端会根据客户端的请求判断是否包含了sessionid
2，存在，说明客户端之前建立了联系
3，没有，服务器会生产一个sessionid

# 三、session共享的解决方案

## session复制

服务器之间复制session

## 第三方统一存储（例如：数据库、redis）

## 基于cookie

App，登录成功后生产一个token，存放到cookie

### 基于JWT的解决方案（JSON WEB TOKEN）

客户端和服务端信息安全传递以及身份认证的一种解决方案；用在登录上。
jwt由3个部分组成：header，playload，signature

```json
header
{
type:"jwt",
    alg:"HS256"
}
playload
{
iss:
     iat:
    exp:
    sub:
    claims:
    {
     uid
    }
}
signature
{
Base64去编码
    会将header+playload组合成字符串加密
    Base64(header).Base64(payload) 通过密钥和签名生成一个字符串：str.签名字符串 = token
}
```

jjwt.jar
joda.time.jar