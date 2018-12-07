[TOC]

# 一，简介

Nginx是俄罗斯人编写的一款高性能的HTTP和反向代理服务器，在高连接并发的情况下，它能够支持高达50000个并发连接数的响应，但是内存、CPU等系统资源消耗却很低，运行很稳定。 目前Nginx在国内很多大型企业都有应用，据最新统计，Nginx的市场占有率已经到33%左右了。而Apache的市场占有率虽然仍然是最高的，但是是呈下降趋势。而Nginx的势头很明显。 选择Nginx的理由也很简单： 第一，它可以支持5W高并发连接； 第二，内存消耗少； 第三，成本低，如果采用F5、NetScaler等硬件负载均衡设备的话，需要大几十万。 而Nginx是开源的，可以免费使用并且能用于商业用途。 

# **二，关于反向代理和正向代理**

正向代理的对象是客户端，反向代理代理的是服务端 

# **三，Nginx安装部署**

```shell
nginx安装 
1.tar -zxvf 安装包 
2../configure --prefix=/mic/data/program/nginx   默认安装到/usr/local/nginx 
3.make & make install 
4.启动停止 ./nginx -c /mic/data/program/nginx/conf/nginx.conf 
5.启动nginx   -c表示指定nginx.conf的文件。如果不指定，默认为NGINX_HOME/conf/nginx.conf 发送信号的方式 kill -QUIT  进程号   (快速结束) kill -TERM  进程号  (等待结束) 停止nginx ./nginx -s stop  停止 ./nginx -s quit   退出 ./nginx -s reload  重新加载nginx.conf 
6.安装过程中可能会出现的问题 
缺少pcre的依赖 
缺少openssl的依赖 
yum  -y install pcre-devel 
yum  -y install openssl-devel 
yum  -y install zlib-devel
yum -y install gcc gcc-c++ autoconf automake make 
```



# **四，Nginx内置变量**

内置变量存放在 ngx_http_core_module 模块中，变量的命名方式和apache 服务器变量是一致的。 总而言之，这些变量代表着客户端请求头的内容，例如$http_user_agent, $http_cookie, 等等。 **下面是nginx支持的所有内置变量**： $arg_name 请求中的的参数名，即“?”后面的arg_name=arg_value形式的arg_name $args 请求中的参数值 $binary_remote_addr 客户端地址的二进制形式, 固定长度为4个字节 $body_bytes_sent 传输给客户端的字节数，响应头不计算在内；这个变量和Apache的mod_log_config模块中的“%B”参数保持兼容 $bytes_sent 传输给客户端的字节数 (1.3.8, 1.2.5) $connection TCP连接的序列号 (1.3.8, 1.2.5) $connection_requests TCP连接当前的请求数量 (1.3.8, 1.2.5) $content_length “Content-Length” 请求头字段 $content_type “Content-Type” 请求头字段 $cookie_name cookie名称 $document_root 当前请求的文档根目录或别名 $document_uri 同 $uri $host 优先级如下：HTTP请求行的主机名>”HOST”请求头字段>符合请求的服务器名 $hostname 主机名 $http_name 匹配任意请求头字段； 变量名中的后半部分“name”可以替换成任意请求头字段，如在配置文件中需要获取http请求头：“Accept-Language”，那么将“－”替换为下划线，大写字母替换为小写，形如：$http_accept_language即可。 $https 如果开启了SSL安全模式，值为“on”，否则为空字符串。 $is_args 如果请求中有参数，值为“?”，否则为空字符串。 $limit_rate 用于设置响应的速度限制，详见 limit_rate。 $msec 当前的Unix时间戳 (1.3.9, 1.2.6) $nginx_version nginx版本 $pid 工作进程的PID $pipe 如果请求来自管道通信，值为“p”，否则为“.” (1.3.12, 1.2.7) $proxy_protocol_addr 获取代理访问服务器的客户端地址，如果是直接访问，该值为空字符串。(1.5.12) $query_string 同 $args $realpath_root 当前请求的文档根目录或别名的真实路径，会将所有符号连接转换为真实路径。 $remote_addr 客户端地址 $remote_port 客户端端口 $remote_user 用于HTTP基础认证服务的用户名 $request 代表客户端的请求地址 $request_body 客户端的请求主体 此变量可在location中使用，将请求主体通过proxy_pass, fastcgi_pass, uwsgi_pass, 和 scgi_pass传递给下一级的代理服务器。 $request_body_file 将客户端请求主体保存在临时文件中。文件处理结束后，此文件需删除。如果需要之一开启此功能，需要设置client_body_in_file_only。如果将次文件传递给后端的代理服务器，需要禁用request body，即设置proxy_pass_request_body off，fastcgi_pass_request_body off, uwsgi_pass_request_body off, or scgi_pass_request_body off 。 $request_completion 如果请求成功，值为”OK”，如果请求未完成或者请求不是一个范围请求的最后一部分，则为空。 $request_filename 当前连接请求的文件路径，由root或alias指令与URI请求生成。 $request_length 请求的长度 (包括请求的地址, http请求头和请求主体) (1.3.12, 1.2.7) $request_method HTTP请求方法，通常为“GET”或“POST” $request_time 处理客户端请求使用的时间 (1.3.9, 1.2.6); 从读取客户端的第一个字节开始计时。 $request_uri 这个变量等于包含一些客户端请求参数的原始URI，它无法修改，请查看$uri更改或重写URI，不包含主机名，例如：”/cnphp/test.php?arg=freemouse”。 $scheme 请求使用的Web协议, “http” 或 “https” $sent_http_name 可以设置任意http响应头字段； 变量名中的后半部分“name”可以替换成任意响应头字段，如需要设置响应头Content-length，那么将“－”替换为下划线，大写字母替换为小写，形如：$sent_http_content_length 4096即可。 $server_addr 服务器端地址，需要注意的是：为了避免访问linux系统内核，应将ip地址提前设置在配置文件中。 $server_name服务器名，[www.cnphp.info](http://www.cnphp.info) $server_port服务器端口 $server_protocol服务器的HTTP版本, 通常为 “HTTP/1.0” 或 “HTTP/1.1” $status HTTP响应代码 (1.3.2, 1.2.2) $tcpinfo_rtt, $tcpinfo_rttvar, $tcpinfo_snd_cwnd, $tcpinfo_rcv_space客户端TCP连接的具体信息 $time_iso8601服务器时间的ISO 8610格式 (1.3.12, 1.2.7) $time_local服务器时间（LOG Format 格式） (1.3.12, 1.2.7) $uri 请求中的当前URI(不带请求参数，参数位于$args)，可以不同于浏览器传递的$request_uri的值，它可以通过内部重定向，或者使用index指令进行修改，$uri不包含主机名，如”/foo/bar.html”。 

 

# **五，使用配置**

**Nginx核心配置分析**

nginx的核心配置文件,主要包括三个段：Main、 Event 、 Http 

优化配置

```properties
----nginx.conf----------- 
main worker_rlimit_nofile event worker_connections accept_mutex off 惊群效应 
http charset utf-8 sendfile on ; -开启高效传输模式 
gzip on; 
gzip_min_length 5k; 
gzip_comp_level 8; 
gzip_buffers gzip_types gzip_vary on; 
include  default_type  access_log off; 
proxy_temp_path proxy_cache_path  
----upstream.conf 负载服务器配置 ----------- 
----server.conf  用域名做文件名 服务器配置 
proxy_pass proxy_set_header X-Real_IP $remote_addr; 
proxy_send_timeout : 请求发送到给
upstream的超时时间 静态文件配置： 
```

惊群

**虚拟主机的配置**

基于域名的虚拟主机 修改windows/system32/drivers/etc/hosts 基于端口的虚拟主机 基于ip的虚拟主机 

**关于Nginx日志配置和及切割处理**

Nginx日志配置

通过access_log进行日志记录 nginx中有两条是配置日志的：一条是log_format 来设置日志格式 ； 另外一条是access_log #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '     #                  '$status $body_bytes_sent "$http_referer" '     #                  '"$http_user_agent" "$http_x_forwarded_for"'; access_log  格式 #error_log  logs/error.log  notice; logo声明   路径及文件名 日志标识

切割处理

crontab mv access.log access.log.20171206 kill -USR1 Nginx 主进程号  让nginx重新生成一个日志文件access.log

**Rewrite的使用**

通过ngx_http_rewrite_module模块 支持url重写、支持if判断，但不支持else rewrite功能就是，使用nginx提供的全局变量或自己设置的变量，**结合正则表达式和标志位实现url重写以及重定向** rewrite只能放在server{},location{},if{}中，并且只能对域名后边的除去传递的参数外的字符串起作用 常用指令 If 空格 (条件) {设定条件进行重写} 条件的语法： 1.“=” 来判断相等，用于字符比较 2.“~” 用正则来匹配（表示区分大小写），“~*” 不区分大小写 3.“-f -d -e” 来判断是否为文件、目录、是否存在 

return 指令

语法：return code; 停止处理并返回指定状态码给客户端。 if ($request_uri ~ *\.sh ){   return 403 } 

set指令

set variable value;  定义一个变量并复制，值可以是文本、变量或者文本变量混合体 

rewrite指令

语法：rewrite regex replacement [flag]{last / break/ redirect 返回临时302/ permant  返回永久302} last: 停止处理后续的rewrite指令集、 然后对当前重写的uri在rewrite指令集上重新查找 break; 停止处理后续的rewrite指令集 ,并不会重新查找  **例子**：rewrite ^/(.*) <http://www.czlun.com/$1> permanent; 说明：                                         rewrite为固定关键字，表示开始进行rewrite匹配规则 regex部分是 ^/(.*) ，这是一个正则表达式，匹配完整的域名和后面的路径地址 replacement部分是<http://www.czlun.com/$1> $1，是取自regex部分()里的内容。匹配成功后跳转到的URL。 flag部分 permanent表示永久301重定向标记，即跳转到新的 <http://www.czlun.com/$1> 地址上 

综合实例

如上配置对于： /images/ttt/test.png 会重写到/mic?file=test.png, 于是匹配到 location /mic ; 通过try_files获取存在的文件进行返回。最后由于文件不存在所以直接 返回404错误 rewrite匹配规则 表面看rewrite和location功能有点像，都能实现跳转，主要区别在于rewrite是在同一域名内更改获取资源的路径，而location是对一类路径做控制访问或反向代理，可以proxy_pass到其他机器。很多情况下rewrite也会写在location里，它们的执行顺序是： ·执行server块的rewrite指令 ·执行location匹配 ·执行选定的location中的rewrite指令 如果其中某步URI被重写，则重新循环执行1-3，直到找到真实存在的文件；循环超过10次，则返回500 Internal Server Error错误 

**缓存配置及Gzip配置**

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml\wps7D1C.tmp.png)

Gzip压缩策略

浏览器请求 -> 告诉服务端当前浏览器可以支持压缩类型->服务端会把内容根据浏览器所支持的压缩策略去进行压缩返回->浏览器拿到数据以后解码；   常见的压缩方式：gzip、deflate 、sdch Gzip on|off 是否开启gzip压缩 Gzip_buffers 4 16k #设置系统获取几个单位的缓存用于存储gzip的压缩结果数据流。4 16k代表以16k为单位，安装原始数据大小以16k为单位的4倍申请内存。 Gzip_comp_level[1-9] 压缩级别， 级别越高，压缩越小，但是会占用CPU资源 Gzip_disable #正则匹配UA 表示什么样的浏览器不进行gzip Gzip_min_length #开始压缩的最小长度（小于多少就不做压缩） Gzip_http_version 1.0|1.1 表示开始压缩的http协议版本 Gzip_proxied  （nginx 做前端代理时启用该选项，表示无论后端服务器的headers头返回什么信息，都无条件启用压缩） Gzip_type text/pliain,application/xml  对那些类型的文件做压缩 （conf/mime.conf） Gzip_vary on|off  是否传输gzip压缩标识 注意点 1.图片、mp3这样的二进制文件，没必要做压缩处理，因为这类文件压缩比很小，压缩过程会耗费CPU资源 2.太小的文件没必要压缩，因为压缩以后会增加一些头信息，反而导致文件变大 Nginx默认只对text/html进行压缩 ，如果要对html之外的内容进行压缩传输，我们需要手动来配置 

注意点

\1. 图片、mp3这样的二进制文件，没必要做压缩处理，因为这类文件压缩比很小，压缩过程会耗费CPU资源 2. 太小的文件没必要压缩，因为压缩以后会增加一些头信息，反而导致文件变大 3. Nginx默认只对text/html进行压缩 ，如果要对html之外的内容进行压缩传输，我们需要手动来配置 

动静分离

语法： expires 60s|m|h|d 操作步骤 ·在html目录下创建一个images文件，在该文件中放一张图片 ·修改index.html, 增加<img src=”图片”/> ·修改nginx.conf配置。配置两个location实现动静分离，并且在静态文件中增加expires的缓存期限

**nginx反向代理实战**

Proxy_pass 通过反向代理把请求转发到百度 Proxy_pass 既可以是ip地址，也可以是域名，同时还可以指定端口 Proxy_pass指定的地址携带了URI，看我们前面的配置【/s】，那么这里的URI将会替换请求URI中匹配location参数部分；如上代码将会访问到<http://www.baidu.com/s> underscores_in_header on HTTP头是可以包含英文字母([A-Za-z])、数字([0-9])、连接号(-)hyphens, 也可义是下划线(_)。在使用nginx的时候应该避免使用包含下划线的HTTP头。主要的原因有以下2点。 1.默认的情况下nginx引用header变量时**不能使用带下划线的变量**。要解决这样的问题只能单独配置underscores_in_headers on。 2.默认的情况下**会忽略掉带下划线的变量**。要解决这个需要配置ignore_invalid_headers off。 

限流

**Location匹配规则剖析**

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml\wps7D2C.tmp.jpg)

location [~|=|^~|~*] /uri {   } location的匹配规则： 1，精准匹配 location=/uri{} 优先级最高的匹配规则 2，普通匹配 location /uri{ } 普通匹配的优先级要高于正则匹配 如果存在多个相同的前缀的一般匹配，那么最终会按照最大长度来做匹配 3，正则匹配 

**负载均衡配置**

upstream是Nginx的HTTP Upstream模块，这个模块通过一个简单的调度算法来实现客户端IP到后端服务器的负载均衡 Upstream常用参数介绍  语法：server address [parameters] 其中关键字server必选。 address也必选，可以是主机名、域名、ip或unix socket，也可以指定端口号。 parameters是可选参数，可以是如下参数： down：表示当前server已停用 backup：表示当前server是备用服务器，只有其它非backup后端服务器都挂掉了或者很忙才会分配到请求 weight：表示当前server负载权重，权重越大被请求几率越大。默认是1 max_fails和fail_timeout一般会关联使用，如果某台server在fail_timeout时间内出现了max_fails次连接失败，那么Nginx会认为其已经挂掉了，从而在fail_timeout时间内不再去请求它，fail_timeout默认是10s，max_fails默认是1，即默认情况是只要发生错误就认为服务器挂掉了，如果将max_fails设置为0，则表示取消这项检查。 ups支持的调度算法 ip_hash  根据ip的hash值来做转发 默认是轮询机制 权重 weight=x fair 根据服务器的响应时间来分配请求 url_hash 

**Nginx配置https的请求**

·https基于SSL/TLS这个协议； ·非对称加密、对称加密、 hash算法 ·crt的证书->返回给浏览器 

openssl创建证书

创建证书

创建服务器私钥 openssl genrsa -des3 -out server.key 1024 ·创建签名请求的证书（csr）; csr核心内容是一个公钥 openssl req -new -key server.key -out server.csr ·去除使用私钥是的口令验证 cp server.key [server.key.org](http://server.key.org) openssl rsa -in [server.key.org](http://server.key.org) -out server.key ·标记证书使用私钥和csr openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt x509是一种证书格式 server.crt就是我们需要的证书 

nginx配置

nginx配置文件在git上的www.gupao.com.conf文件

tomcat增加对https的支持 

Connector 8080节点加入 redirectPort="443" proxyPort="443" redirectPort ：当http请求有安全约束才会转到443端口使用ssl传输



# **六，Nginx的进程模型**

**1，Master进程**

充当整个进程组与用户的交互接口，同时对进程进行监护。

它不需要处理网络事件，不负责业务的执行，只会通过管理**work进程来实现重启服务、平滑升级、更换日志文件、配置文件实时生效**等功能。 主要是用来管理worker进程 

1.接收来自外界的信号 （前面提到的 kill -HUP 信号等） 我们要控制nginx，只需要通过kill向master进程发送信号就行了。比如kill -HUP pid，则是告诉nginx，从容地重启nginx，我们一般用这个信号来重启nginx，或重新加载配置，因为是从容地重启，因此服务是不中断的。

master进程在接收到HUP信号后是怎么做的呢？首先master进程在接到信号后，会先重新加载配置文件，然后再启动新的worker进程，并向所有老的worker进程发送信号，告诉他们可以光荣退休了。新的worker在启动后，就开始接收新的请求，而老的worker在收到来自master的信号后，就不再接收新的请求，并且在当前进程中的所有未处理完的请求处理完成后，再退出 2.向各个worker进程发送信号 

\3. 监控worker进程的运行状态 

\4. .当worker进程退出后（异常情况下），会自动重新启动新的worker进程 

**2，Work进程**

主要是完成具体的任务逻辑。它的主要关注点是客户端和后端真实服务器之间的数据可读、可写等I/O交互事件。 

各个worker进程之间是对等且相互独立的，他们同等竞争来自客户端的请求，一个请求只可能在一个worker进程中处理，worker进程个数一般设置为cpu核数。 

master进程先建好需要listen的socket后，然后再fork出多个woker进程，这样每个work进程都可以去accept这个socket。当一个client连接到来时，所有accept的work进程都会受到通知，但只有一个进程可以accept成功，其它的则会accept失败。 

**3，IO多路复用**

一个线程多个进程work

多进程+多路复用 

master 进程 、 worker 进程 

root      7473     1  0 20:09 ?        00:00:00 nginx: master process .

/nginx 

nobody    7474  7473  0 20:09 ?        00:00:00 nginx: worker process 

worker_processes 1 cpu 总核心数 **epoll** . select .... 

\#user  nobody;          用户 worker_processes  1;    工作进程数 

\#error_log  logs/error.log; 

\#error_log  logs/error.log  notice; #error_log  logs/error.log  info; 

\#pid        logs/nginx.pid;        

 events { 

​    use epoll ;  io 模型 

worker_connections  1024；  理论上  processes* connections 

} ![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml\wps7D2D.tmp.jpg)



# **七，Nginx+keepalived实现高可用**

每台nginx对应的机器上也要安装好对应的keepalive。（master -- backup）

## **1，LVS**

LVS 是 Linux Virtual Server 的缩写，也就是 Linux 虚拟服务器，在 linux2.4 内核 以后，已经完全内置了 LVS 的各个功能模块。 

它是工作在四层的负载均衡，类似于 Haproxy, 主要用于实现对服务器集群的负载均衡。 

关于四层负载，我们知道 osi 网络层次模型的 7 层模模型（应用层、表示层、会话 层、传输层、网络层、数据链路层、物理层）；四层负载就是基于传输层，也就是 ip+端口的负载；而七层负载就是需要基于 URL 等应用层的信息来做负载，同时还有二层负载（基于 MAC）、三层负载（IP）； 

常见的四层负载有：LVS、F5； 七层负载有:Nginx、HAproxy; 在软件层面，Nginx/LVS/HAProxy 是使用得比较广泛的三种负载均衡软件。 

对于中小型的 Web 应用，可以使用 Nginx、大型网站或者重要的服务并且服务比较多的时候，可以考虑使用 LVS 

轻量级的高可用解决方案 

LVS 四层负载均衡软件（Linux virtual server） 监控 lvs 集群系统中的各个服务节点的状态 。VRRP 协议（虚拟路由冗余协议） 

linux2.4 以后，是内置在 linux 内核中的 

lvs(四层) -> HAproxy 七层 

lvs(四层) -> Nginx(七层) 

## **2，Nginx+keepalived**

keepalived – >VRRP(虚拟路由器冗余协议) VRRP全称 Virtual Router Redundancy Protocol，即 虚拟路由冗余协议。

可以认为它是实现路由器高可用的容错协议，即将N台提供相同功能的路由器组成一个路由器组(Router Group)，这个组里面有一个master和多backup，但在外界看来就像一台一样，构成虚拟路由器，拥有一个虚拟IP（vip，也就是路由器所在局域网内其他机器的默认路由），占有这个IP的master实际负责ARP相应和转发IP数据包，组中的其它路由器作为备份的角色处于待命状态。master会发组播消息，当backup在超时时间内收不到vrrp包时就认为master宕掉了，这时就需要根据VRRP的优先级来选举一个backup当master，保证路由器的高可用。

VRRP 出现的目的就 是为了解决静态路由单点故障问题的，它能够保证当个别节点宕机时，整个网络可 以不间断地运行;(简单来说，vrrp 就是把两台或多态路由器设备虚拟成一个设备，

实现主备高可用) 

所以，Keepalived 一方面具有配置管理 LVS 的功能，同时还具有对 LVS 下面节点 进行健康检查的功能，另一方面也可实现系统网络服务的高可用功能  ![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml\wps7D3E.tmp.jpg)

## **3，安装keepalived**

```shell
\1. 在/data/nginx , wget http://www.keepalived.org/software/keepalived-2.0.9.tar.gz  

\2. tar -zxvf  keepalived-2.0.9.tar.gz 

\3. 

\4. cd 到 keepalived-2.0.9 目录下，

执行./configure --prefix=/usr/local/keepalived --sysconf=/etc  

\5. 如果缺少依赖库，则 

yum install gcc; 

yum install openssl-devel ; 

yum install libnl libnl-devel 

\6. 编译安装 make && make install 

\7. 进入安装后的路径 cd /usr/local/keepalived, 

创建软连接: ln -s sbin/keepalived /sbin 

\8.  cp /data/nginx/keepalived-2.0.9/keepalived/etc/init.d/keepalived /etc/init.d 

\9. chkconfig --add keepalived 

\10. chkconfig keepalived on 

\11. service keepalived start 
```

![](C:\Users\lqd\Desktop\1.png)

### keepalived 的配置 - master 

vi /etc/keepalived/keepalived.conf，编辑keepalived的配置内容：

```properties
! Configuration File for keepalived global_defs { 

   router_id LVS_DEVEL   运行 keepalived 服务器的标识，在一个网络内应该是唯 一的 

} 

vrrp_instance VI_1 {   #vrrp 实例定义部分 

    state MASTER  #设置 lvs 的状态，MASTER 和 BACKUP 两种，必须大写 

    interface ens33   #设置对外服务的接口 

    virtual_router_id 51   #设置虚拟路由标示，这个标示是一个数字，同一个 vr rp 实例使用唯一标示 

    priority 100 #定义优先级，数字越大优先级越高，在一个 vrrp——instance 下， master 的优先级必须大于 backup 

    advert_int 1 #设定 master 与 backup 负载均衡器之间同步检查的时间间隔，单 位是秒 

    authentication {  #设置验证类型和密码 

        auth_type PASS 

        auth_pass 1111   #验证密码，同一个 vrrp_instance 下 MASTER 和 BACKU

P 密码必须相同 

    } 

    virtual_ipaddress { #设置虚拟 ip 地址，可以设置多个，每行一个 ，要求和真实主机的网段一样。

        192.168.11.100 

    } } 

virtual_server 192.168.11.100 80 { #设置虚拟服务器，需要指定虚拟 ip 和服务 端口 

    delay_loop 6  #健康检查时间间隔 

    lb_algo rr  #负载均衡调度算法 

    lb_kind NAT  #负载均衡转发规则 

    persistence_timeout 50  #设置会话保持时间 

    protocol TCP #指定转发协议类型，有 TCP 和 UDP 两种 

 

    real_server 192.168.11.160 80 { #配置服务器节点 1，需要指定 real serve

r 的真实 IP 地址和端口 

        weight 1  #设置权重，数字越大权重越高 

TCP_CHECK {  #realserver 的状态监测设置部分单位秒 

           connect_timeout 3  #超时时间 

           delay_before_retry 3 #重试间隔 

           connect_port 80   #监测端口 

        } 

    } } 
```

```properties
! Configuration File for keepalived

global_defs {
   router_id LVS_DEVEL
}

vrrp_instance VI_1 {
    state MASTER
    interface ens33
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.254.100
    }
}

virtual_server 192.168.254.100 80 {
    delay_loop 6
    lb_algo rr
    lb_kind NAT
    persistence_timeout 50
    protocol TCP

    real_server 192.168.254.136 80 {
        weight 1
        TCP_CHECK {
           connect_timeout 3  
           delay_before_retry 3 
           connect_port 80   
		}
    }
}

```



### keepalived 的配置 - backup 

```properties
! Configuration File for keepalived

global_defs {
   router_id LVS_DEVEL
}

vrrp_instance VI_1 {
    state BACKUP
    interface ens33
    virtual_router_id 51
    priority 50
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.254.100
    }
}

virtual_server 192.168.254.100 80 {
    delay_loop 6
    lb_algo rr
    lb_kind NAT
    persistence_timeout 50
    protocol TCP

    real_server 192.168.254.129 80 {
        weight 1
        TCP_CHECK {
           connect_timeout 3  
           delay_before_retry 3 
           connect_port 80   
		}
    }
} 
```

验证：

访问地址http://192.168.254.100/ ，可以正常访问到nginx首页。

### keepalived 日志文件配置 

```shell
\1. 首先看一下/etc/sysconfig/keepalived 文件 
vi /etc/sysconfig/keepalived 
KEEPALIVED_OPTIONS="-D -d -S 0" 
“-D” 就是输出日志的选项 
这里的“-S 0”表示 local0.* 具体的还需要看一下/etc/syslog.conf 文件 
\2. 在/etc/rsyslog.conf 里添加:local0.* /var/log/keepalived.log 
\3. 重新启动 keepalived 和 rsyslog 服务： 
service rsyslog restart 
service keepalived restart 
```



### 通过脚本实现动态切换

```shell
\1. 在 master 和 slave 节点的 /data/program/nginx/sbin/nginx-ha-check.sh 目录 下增加一个脚本 
–no-headers 不打印头文件 
Wc –l  
统计行数 
#!bin/sh   #! /bin/sh 是指此脚本使用/bin/sh 来执行 
A=`ps -C nginx --no-header |wc -l` if [ $A -eq 0 ] 
   then 
   echo 'nginx server is died' 
   service keepalived stop fi 
\2. 修改 keepalived.conf 文件，增加如下配置 track_script: #执行监控的服务。 chknginxservice # 
```

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml\wps7D4F.tmp.jpg)



### 注意点

1，nginx down掉后 ，对应的keepalive也要down掉。 这样才能负载nginx。 怎么检测： 在keepalive中配置vrrp_script 

2，keepalive日志记录

 

# **八，图片缩放插件 **

## http_image_filter_module

red参数，不然，不会生成共享库 5.安装GD tar zxvf gd-2.0.33.tar.gz cd gd-2.0.33 ./configure --with-png --with-freetype --with-jpeg make install 如果GD报错:configure.ac:64: warning: macro `AM_ICONV' not found in library 你就make clean一下，然后再make 如果你安装别的出现libtool没有找到，你就从/usr/bin/libtool cp 一个过来用就好了！ 在64位下编译GD 如果/usr/bin/ld: /usr/local/lib/libz.a(compress.o): relocation R_X86_64_32 against `a local symbol' can not be used when making a shared object; recompile with -fPIC 这说明zlib没用用-fPIC进行编译修改zlib的Makefile CFLAGS=-O3 -DUSE_MMAP -fPIC make;make install然后再编译gd 就过去了！ 

**实例**

请求地址：<http://192.168.131.32/dls/download/images/a.png?height=940&width=240> 规则书写： location ~* .*\.(jpg|gif|png)$ {      set $image_w $arg_width;      set $image_h $arg_height;           #image resize      set $resizeflag 0;      #project      set $subflag 0;           if ($args ~* "(height=\d+&width=\d+$|width=\d+&height=\d+$)")      {         set $resizeflag 1;      }           set $subflag 0;      #dls      if ($request_uri ~* "/dls/download/")      {         set $subflag 1;      }      #cloudzone      if ($request_uri ~* "/cloudzone/")      {         set $subflag 2;      }      set $flag "$resizeflag$subflag";      if ($flag = "01")      {         rewrite "/dls/download/(.*\.(jpg|gif|png))(.*)$" /imagefile_dls/$1;      }      if ($flag = "11")      {     rewrite "/dls/download/(.*\.(jpg|gif|png))(.*)$" /imagefileresize/$1;      }      if ($flag = "02")      {         rewrite "(.*\.(jpg|gif|png))(.*)$" /pic_cloudzone/$1;      } } location ^~ /pic_cloudzone/ {         alias /home/cloudzone/apache-tomcat-8.5.20/webapps/; } location ^~ /imagefile_dls/ {         alias /data/contentftp/;         gzip on; gzip_min_length 5k; gzip_comp_level 8; gzip_buffers 10 160k; gzip_types *; gzip_vary on;         gzip_proxied any;         expires 1d; } location ^~ /imagefileresize/ {         image_filter resize $image_w $image_h;         image_filter_buffer 100M;         image_filter_jpeg_quality 75;         alias /data/contentftp/;         gzip on;         gzip_min_length 5k;         gzip_comp_level 8;         gzip_buffers 10 160k;         gzip_types *;         gzip_proxied any;         gzip_vary on;         expires 1d; } 

 

# **九，向linux服务器注册服务**

LINUXVERSION=`rpm -q centos-release|cut -d- -f3` NGX_DIR=/usr/local/nginx/ if [[ $LINUXVERSION < 7 ]];then   cp $NGX_DIR/nginx /etc/init.d/nginx   chmod a+x /etc/init.d/nginx   #centos    if [ -n "`whereis yum | awk -F ':' '{print $2}'`" ]; then    if [ `cat /etc/rc.local |grep "/etc/init.d/nginx" | wc -l` -eq 0 ];then      echo "/etc/init.d/nginx" >> /etc/rc.local    fi   fi    #reboot   chkconfig --add nginx   chkconfig --level 2345 nginx on   service nginx restart else cp $NGX_DIR/nginx.service /lib/systemd/system/ systemctl enable nginx systemctl restart nginx fi 

**centos6**

\#!/bin/sh  #  # nginx - this script starts and stops the nginx daemon  #  # chkconfig:   - 85 15  # description: Nginx is an HTTP(S) server, HTTP(S) reverse \  #               proxy and IMAP/POP3 proxy server  # processname: nginx  # config:      /etc/nginx/nginx.conf  # config:      /etc/sysconfig/nginx  # pidfile:     /var/run/nginx.pid  # Source function library.  . /etc/rc.d/init.d/functions  # Source networking configuration.  . /etc/sysconfig/network  # Check that networking is up.  [ "$NETWORKING" = "no" ] && exit 0  nginx="/usr/local/nginx/sbin/nginx"  prog=$(basename $nginx)  NGINX_CONF_FILE="/usr/local/nginx/conf/nginx.conf"  [ -f /etc/sysconfig/nginx ] && . /etc/sysconfig/nginx  lockfile=/var/lock/subsys/nginx  start() {      [ -x $nginx ] || exit 5      [ -f $NGINX_CONF_FILE ] || exit 6      echo -n $"Starting $prog: "      daemon $nginx -c $NGINX_CONF_FILE      retval=$?      echo      [ $retval -eq 0 ] && touch $lockfile      return $retval  }  stop() {      echo -n $"Stopping $prog: "      killproc $prog -QUIT      retval=$?      echo      [ $retval -eq 0 ] && rm -f $lockfile      return $retval  killall -9 nginx  }  restart() {      configtest || return $?      stop      sleep 1      start  }  reload() {      configtest || return $?      echo -n $"Reloading $prog: "      killproc $nginx -HUP  RETVAL=$?      echo  }  force_reload() {      restart  }  configtest() {  $nginx -t -c $NGINX_CONF_FILE  }  rh_status() {      status $prog  }  rh_status_q() {      rh_status >/dev/null 2>&1  }  case "$1" in      start)          rh_status_q && exit 0      $1          ;;      stop)          rh_status_q || exit 0          $1          ;;      restart|configtest)          $1          ;;      reload)          rh_status_q || exit 7          $1          ;;      force-reload)          force_reload          ;;      status)          rh_status          ;;      condrestart|try-restart)          rh_status_q || exit 0              ;;      *)           echo $"Usage: $0 {start|stop|status|restart|condrestart|try-restart|reload|force-reload|configtest}"          exit 2  esac   

**centos7**

[Unit] Description=nginx After=network.target    [Service] Type=forking ExecStart=/usr/local/nginx/sbin/nginx ExecReload=/usr/local/nginx/sbin/nginx -s reload ExecStop=/usr/local/nginx/sbin/nginx -s quit PrivateTmp=true    [Install] WantedBy=multi-user.target

# 十，Openresty

OpenResty 是一个通过 Lua 扩展 Nginx 实现的可伸缩的 Web 平台，内部集成了大 量精良的 Lua 库、第三方模块以及大多数的依赖项。用于方便地搭建能够处理超高并发、扩展性极高的动态 Web 应用、Web 服务和动态网关。 

## 安装

```shell
\1. 下载安装包 
https://openresty.org/cn/download.html
\2. 安装软件包 
tar -zxvf openresty-1.13.6.2.tar.gz 
cd openrestry-1.13.6.2 
./configure [默认会安装在/usr/local/openresty 目录] --prefix= 指定路径 make && make install 
\3. 可能存在的错误，第三方依赖库没有安装的情况下会报错 
yum install readline-devel / pcre-devel / openssl-devel 
安装过程和 Nginx 是一样的，因为他是基于 Nginx 做的扩展 
```

##  HelloWorld

```properties
开始第一个程序，HelloWorld 
cd /usr/local/openresty/nginx/conf 
location / { 
   default_type  text/html; 
   content_by_lua_block { 
      ngx.say("helloworld"); 
  } 
} 
在 sbin 目录下执行.nginx 命令就可以运行，看到 helloworld
```

验证访问：http://192.168.254.136

## 建立工作空间 

### 创建目录 

```shell
或者为了不影响默认的安装目录，我们可以创建一个独立的空间来练习，先到在安 装目录下创建 demo 目录,安装目录为
/data/program/openresty/demo 
mkdir demo 
然后在 demo 目录下创建两个子目录，一个是 logs 、一个是 conf 
```

### 创建配置文件

```properties
worker_processes 1; 
error_log logs/error.log; 
events { 
        worker_connections 1024; } 
http { 
   server { 
        listen 8888; 
        location / { 
                default_type text/html; 
                content_by_lua_block { 
                        ngx.say("Hello world") 
                } 
        } 
   } } 
执行：./nginx -p /data/program/openresty/demo 【-p 主要是指明 nginx 启动时 的配置目录】 
```

验证访问：http://192.168.254.136:8888/

## 总结

```
我们刚刚通过一个helloworld的简单案例来演示了 nginx+lua 的功能，其中用到 了 ngx.say 这个表达式，通过在 contentbyluablock 这个片段中进行访问；这个表达式属于ngxlua 模块提供的api， 用于向客户端输出一个内容。
```

## 库文件使用

通过上面的案例，我们基本上对 openresty 有了一个更深的认识，其中我们用到了 自定义的 lua 模块。实际上 openresty 提供了很丰富的模块。让我们在实现某些场 景的时候更加方便。可以在 /openresty/lualib 目录下看到；比如在 resty 目录下可 以看到 redis.lua、mysql.lua 这样的操作 redis 和操作数据库的模块。

### 使用 redis 模块连接 redis 

```properties
worker_processes 1;  
error_log       logs/error.log;  events {  
  worker_connections 1024;  }  
http {  
    lua_package_path '$prefix/lualib/?.lua;;'; 添加”;;”表示默认路径下的 l ualib  
    lua_package_cpath '$prefix/lualib/?.so;;';  
   server {  
      location /demo {  
         content_by_lua_block {  
               local redisModule=require "resty.redis";  
               local redis=redisModule:new();   # lua 的对象实例  
               redis:set_timeout(1000);  
               ngx.say("=======begin connect redis server");  
               local ok,err = redis:connect("127.0.0.1",6379);  #连接 re dis  
               if not ok then  
                  ngx.say("==========connection redis failed,error mess age:",err);  
               end  
               ngx.say("======begin set key and value");  
               ok,err=redis:set("hello","world");  
               if not ok then  
                  ngx.say("set value failed");  
                  return;  
               end  
               ngx.say("===========set value result:",ok);  
               redis:close();  
         }  
      }  
   }  } 
```

演示效果

到 nginx 路径下执行 ./nginx -p /data/program/openresty/redisdemo 在浏览器中输入：http://192.168.11.160/demo 即可看到输出内容 并且连接到 redis 服务器上以后，可以看到 redis 上的结果 redis 的所有命令操作，在 lua 中都有提供相应的操作 .比如 redis:get(“key”)、 redis:set()等 .

# 网关

通过扩展以后的，在实际过程中应该怎么去应用呢？一般的使用场景： 网关、 web 防火墙、缓存服务器（对响应内容进行缓存，减少到达后端的请求，来提升 性能），接下来重点讲讲网关的概念以及如何通过 Openresty 实现网关开发 

从一个房间到另一个房间，必须必须要经过一扇门，同样，从一个网络向另一个网 络发送信息，必须经过一道“关口”，这道关口就是网关。顾名思义，网关(Gateway)就是一个网络连接到另一个网络的“关口”。 

那什么是 api 网关呢？ 

在微服务流行起来之前，api 网关就一直存在，最主要的应用场景就是开放平台， 也就是 open api; 这种场景大家接触的一定比较多，比如阿里的开放平台；当微服 务流行起来以后，api 网关就成了上层应用集成的标配组件.

API 网关意味着你要把 API 网关放到你的微服务的最前端，并且要让 API 网关变成 由应用所发起的每个请求的入口。这样就可以简化客户端实现和微服务应用程序之 间的沟通方式 .

当服务越来越多以后，我们需要考虑一个问题，就是对某些服务进行安全校验以及 用户身份校验。甚至包括对流量进行控制。 我们会对需要做流控、需要做身份认 证的服务单独提供认证功能，但是服务越来越多以后，会发现很多组件的校验是重 复的。***这些东西很明显不是每个微服务组件需要去关心的事情。微服务组件只需要 负责接收请求以及返回响应即可。可以把身份认证、流控都放在 API 网关层进行 控制***.

在单一架构中，随着代码量和业务量不断扩大，版本迭代会逐步变成一个很困难的 事情，哪怕是一点小的修改，都必须要对整个应用重新部署。 但是在微服务中，各个模块是是一个独立运行的组件，版本迭代会很方便，影响面很小。 同时，为服务化的组件节点，对于我们去实现灰度发布（金丝雀发布：将一部分流 量引导到新的版本）来说，也会变的很简单； 所以***通过 API 网关，可以对指定调用的微服务版本，通过版本来隔离***。

## OpenResty 实现 API 网关限流及登录授权

前面我们了解到了网关的作用，通过网关，可以对 api 访问的前置操作进行统一的 管理，比如鉴权、限流、负载均衡、日志收集、请求分片等。所以 API 网关的核 心是所有客户端对接后端服务之前，都需要统一接入网关，通过网关层将所有非业 务功能进行处理。 

OpenResty 为什么能实现网关呢？ OpenResty 有一个非常重要的因素是，对于每 一个请求，***Openresty 会把请求分为不同阶段，从而可以让第三方模块通过挂载行 为来实现不同阶段的自定义行为***。而这样的机制能够让我们非常方便的设计 api 网关 .

![](C:\Users\lqd\Desktop\1.png)

```properties
Nginx 本身在处理一个用户请求时，会按照不同的阶段进行处理，总共会分为 11 个阶段。而 openresty 的执行指令，就是在这 11 个步骤中挂载 lua 执行脚本实现 扩展，我们分别看看每个指令的作用 
initbylua : 当 Nginx master 进程加载 nginx 配置文件时会运行这段 lua 脚本，一般 
用来注册全局变量或者预加载 lua 模块 
initwokerby_lua: 每个 Nginx worker 进程启动时会执行的 lua 脚本，可以用来做 健康检查 
setbylua:设置一个变量 
rewritebylua:在 rewrite 阶段执行，为每个请求执行指定的 lua 脚本 accessbylua:为每个请求在访问阶段调用 lua 脚本 
contentbylua:前面演示过，通过 lua 脚本生成 content 输出给 http 响应 
balancerbylua:实现动态负载均衡，如果不是走 contentbylua，则走 proxy_pass,再 通过 upstream 进行转发 
headerfilterby_lua: 通过 lua 来设置 headers 或者 cookie 
bodyfilterby_lua:对响应数据进行过滤 
logbylua ： 在 log 阶段执行的脚本，一般用来做数据统计，将请求数据传输到后 端进行分析 
```

### 灰度发布的实现

```properties
1.文件件目录， /data/program/openresty/gray [conf、logs、lua] 
2.编写 Nginx 的配置文件 nginx.conf 

worker_processes 1;  
error_log  logs/error.log;  
events{  
  worker_connections 1024;  }  
http{  
   lua_package_path "$prefix/lualib/?.lua;;";  
   lua_package_cpath "$prefix/lualib/?.so;;";  
   upstream prod {  
       server 192.168.11.156:8080;  
   }  
   upstream pre {  
       server 192.168.11.156:8081;  
   }  
   server {  
       listen 80;  
       server_name localhost;  
       location /api {  
          content_by_lua_file lua/gray.lua;  
       }  
       location @prod {  
          proxy_pass http://prod;  
       }  
       location @pre {  
          proxy_pass http://pre;  
       }  
   }  
   server {  
       listen 8080;  
       location / {  
          content_by_lua_block {  
             ngx.say("I'm prod env");  
          }  
           }  
   }  
   server {  
       listen 8081;  
       location / {  
          content_by_lua_block {  
             ngx.say("I'm pre env");  
          }  
       }  
   }  } 
```

```lua
3.编写 gray.lua 文件 
local redis=require "resty.redis";  
local red=redis:new();  
red:set_timeout(1000);  
local ok,err=red:connect("192.168.11.156",6379);  
if not ok then  
   ngx.say("failed to connect redis",err);  
   return;  
end  
local_ip=ngx.var.remote_addr;  
local ip_lists=red:get("gray");  
if string.find(ip_lists,local_ip) == nil then  
   ngx.exec("@prod");  
else  
   ngx.exec("@pre");  
end  
local ok,err=red:close(); 
```

```
4.
\1. 执行命令启动 nginx: [./nginx -p /data/program/openresty/gray] 
\2. 启动 redis，并设置 set gray 192.168.11.160 
\3. 通过浏览器运行: http://192.168.11.160/api 查看运行结果 
修改 redis gray 的值， 讲客户端的 ip 存储到 redis 中 set gray 1. 再次运行结果，
即可看到访问结果已经发生了变化 
```

