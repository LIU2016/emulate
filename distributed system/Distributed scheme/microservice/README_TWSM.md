## 关键字

### OAuth协议

是一个网络开放协议。为保证用户资源的安全授权提供了简易的标准，目前OAuth的版本是2.0即OAuth2.0，而且不向下兼容。

```
oauth的好处：
允许用户授权第三方网站或应用，访问用户存储在其它网站上的资源，而不需要将用户名和密码提供给第三方网站或分享他们数据的内容
对于用户:免去了繁琐的注册过程,降低了注册成本,提高了用户体验 
对于消费方:简化自身会员系统的同时又能够带来更多的用户和流量。 
对于服务提供者:围绕自身进行开发,增加用户粘性 
```

```
1，应用注册
应用程序注册完成之后，服务提供商会颁发给应用程序一个“客户端认证信息(client credentials)”。
Client Credential包括：
Client ID
提供给服务提供商，用于识别应用程序
用于构建提供给用户请求授权的URL
Client Secret
提供给服务提供商，用于验证应用程序
只有应用程序和服务提供商两者可知

2，授权模式
oauth2.0提供了四种授权模式，开发者可以根据自己的业务情况自由选择。
授权码授权模式：（Authorization Code Grant）
隐式授权模式（Implicit Grant）
密码授权模式（Resource Owner Password Credentials Grant）
客户端凭证授权模式（Client Credentials Grant）

授权码授权模式：
（A）用户访问客户端，客户端将用户引导向认证服务器。
（B）用户选择是否给予客户端授权。
（C）如用户给予授权，认证服务器将用户引导向客户端指定的redirection uri，同时加上授权码code。
（D）客户端收到code后，通过后台的服务器向认证服务器发送code和redirection uri。
（E）认证服务器验证code和redirection uri，确认无误后，响应客户端访问令牌（access token）和刷新令牌（refresh token）。
授权码模式是最常见的一种授权模式，在oauth2.0内是最安全和最完善的。适用于所有有Server端的应用，如Web站点、有Server端的手机客户端。 可以得到较长期限授权。

隐式授权模式：
（A）客户端将用户引导向认证服务器。
（B）用户决定是否给于客户端授权。
（C）假设用户给予授权，认证服务器将用户导向客户端指定的”重定向URI"，并在URI的Hash部分包含了访问令牌。
（D）浏览器向资源服务器发出请求，其中不包括上一步收到的Hash值。
（E）资源服务器返回一个网页，其中包含的代码可以获取Hash值中的令牌。
（F）浏览器执行上一步获得的脚本，提取出令牌。
（G）浏览器将令牌发给客户端。
适用于所有无Server端配合的应用。如手机/桌面客户端程序、浏览器插件。基于JavaScript等脚本客户端脚本语言实现的应用。
注意：因为Access token是附着在 redirect_uri 上面被返回的，所以这个 Access token就可能会暴露给资源所有者或者设置内的其它方（对资源所有者来说，可以看到redirect_uri，对其它方来说，可以通过监测浏览器的地址变化来得到 Access token）。

密码授权模式：
（A）用户向客户端提供用户名和密码。
（B）客户端将用户名和密码发给认证服务器，向后者请求令牌。
（C）认证服务器确认无误后，向客户端提供访问令牌。
这种模式适用于用户对应用程序高度信任的情况。比如是用户操作系统的一部分。认证服务器只有在其他授权模式无法执行的情况下，才能考虑使用这种模式。

客户端凭证授权模式：
（A）客户端向认证服务器进行身份认证，并要求一个访问令牌。
（B）认证服务器确认无误后，向客户端提供访问令牌。
客户端模式应用于应用程序想要以自己的名义与授权服务器以及资源服务器进行互动。例如使用了第三方的静态文件服务。

3，刷新TOKEN（根据过期时间定时刷新，或者失败了主动请求。）
从上面的四种授权流程可以看出，最终的目的是要获取用户的授权令牌（access_token）。而且授权令牌（access_token）的权限也非常之大，所以在协议中明确表示要设置授权令牌（access_token）的有效期。那么当授权令牌（access_token）过期要怎么办呢，协议里提出了一个刷新token的流程。
（A）--（D）通过授权流程获取access_token，并调用业务api接口。
（F）当调用业务api接口时响应“Invalid Token Error”时。
（G）调用刷新access_token接口，使用参数refresh_token（如果平台方提供，否则需要用户重新进行授权流程）。
（H）响应最新的access_token及refresh_token。
建议将access_token和refresh_token的过期时间保存下来，每次调用平台方的业务api前先对access_token和refresh_token进行一下时间判断，如果过期则执行刷新access_token或重新授权操作。refersh_token如果过期就只能让用户重新授权。

4，Oauth2.0安全性
4.1，安全漏洞回顾之授权码授权模式：针对应用方csrf劫持第三方账号。这里需要第三方应用在登录成功后将平台的账号与第三方账号绑定。（平台账号就是攻击者的账号信息，这样攻击者下次就可以通过自己的平台账号来登录该受攻击者的第三方应用）
解决方案：要么不绑定账号关系，要么带state参数
（
不可预测性：足够的随机，使得攻击者难以猜到正确的参数值
关联性：state参数值和当前用户会话（user session）是相互关联的
唯一性：每个用户，甚至每次请求生成的state参数值都是唯一的
时效性：state参数一旦被使用则立即失效
）
4.2，安全漏洞回顾之隐式授权模式：针对存储型xss劫持用户的access_token。
解决方案：无解，尽量不要用，同时做应用监控。
4.3，安全漏洞回顾之密码模式
解决方案：无解，尽量不要用
4.4，安全性建议
资源提供方: 
　　对client_id和回调地址做严格校验 
　　获取access token的code仅能使用一次，且与授权用户关联
　　尽量避免直接读取当前用户session进行绑定 
　　有效使用client_secret参数
资源使用方: 
　　使用Authorization Code方式进行授权 
　　授权过程使用state随机哈希,并在服务端进行判断 
　　尽量使用HTTPS保证授权过程的安全性 
最后，对oauth2.0有详细的了解，严格按照流程进行开发。

5，实现框架
OAuth2.0实现是基于shiro+ oltu框架

```

## 参考文档

http://dev.teewon.net:8088/dev 开发者必读

https://www.cnblogs.com/maoxiaolv/p/5838680.html OAuth2.0

https://www.jianshu.com/p/c7c8f51713b6 OAuth2.0的csrf劫持

## 环境信息

### 开发环境信息

```
ECO访问地址	http://dev.teewon.net:8088 创建租户
网关地址	dev.teewon.net:7000
kafka地址	dev.teewon.net:7092
能力平台地址	 http://dev.teewon.net:9999
EK	http://192.168.210.52:9100 

数据库连接
192.168.210.54:8832
twpaas
twpaasuseR@2017
天闻租户连接
192.168.210.54:8832
cjtwbs1
cjTWbs1@2017

Ai作业Web
APPID：e61781c02e6c4445bd59914723bbf612
APPKEY：ef2c67fac32b0e5d

Ai作业app
APPID：eaee13ae2a7c47a0bb0be2c796167bd3
APPKEY：3298192096145356

校管理员
超级管理员：administrator/123qwe
开发者帐号：13904302496/123qwe

学生账号/密码：31/123Aa@
老师账号/密码：555/123456

校方管理员：55/123456

TwaspPropertySources

ConfigServicePropertySourceLocator
```

## 问题

1，文档没更新，例如：http://dev.teewon.net:8088/dev/#/integrate/quick/createApp 没有集成。

2，oauth2.0验证没有加state，任意被攻击者劫持第三方账号。

3，登录退出有问题，例如：http://dev.teewon.net:8088 退出了还展示用户信息。

4，文档不全，开发者要注意：

```
1，应用被管理员审核后要分配给租户，而且审核后要上架才看得到。应用要配置正确服务器访问地址。
2，租户的管理员（校方管理员）要分配给用户。用户登录后才能看到进入应用页面。
3，前端页面要设置应用id和应用key。
```





