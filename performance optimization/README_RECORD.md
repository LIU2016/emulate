如何合理地估算线程池大小 (http://ifeve.com/how-to-calculate-threadpool-size/)

使用 Perf 和火焰图分析 CPU 性能 http://senlinzhan.github.io/2018/03/18/perf/

Linux之TCPIP内核参数优化 https://www.cnblogs.com/fczjuever/archive/2013/04/17/3026694.html

strace -o out.strace -e trace=write -s 200 -f -p 10707

lsof -i:端口 查看端口的进程

lsof -p 进程：查看进程打开的文件



```
<Connector port="8012" protocol="org.apache.coyote.http11.Http11NioProtocol" 
		   connectionTimeout="20000" URIEncoding="UTF-8" maxThreads="200"
		   redirectPort="9012" acceptCount="10000" enableLookups="false" maxHttpHeaderSize="65536" compression="on" compressableMimeType="text/*,application/javascript,image/png,image/jpg,image/gif" />


# -----------------------------------------------------------------------------
JAVA_OPTS="$JAVA_OPTS -server -Xms2048M -Xmx2048M  -verbose:gc -Djava.awt.headless=true -Xloggc:gc.log -XX:-UseGCOverheadLimit -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+HeapDumpOnOutOfMemoryError"

```



```
broken pipline:
---------------------------
请求端主动断掉连接，而服务端还在写。服务端处理请求太长，超时导致。
检查各个连接的超时设置。
```



```
该版本下的网络测试工具iperf3

下载gz包
#wget http://downloads.es.net/pub/iperf/iperf-3.0.6.tar.gz
#tar zxvf iperf-3.0.6.tar.gz
# cd iperf-3.0.6
# ./configure
# make
# make install
```

```
linux系统dig和nslookup的安装
---------------------------------------
Ubuntu:
# sudo apt-get install dnsutils

Debian:
# apt-get update
# apt-get install dnsutils

Fedora / Centos:
# yum install bind-utils
```

