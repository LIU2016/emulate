如何合理地估算线程池大小 (http://ifeve.com/how-to-calculate-threadpool-size/)

使用 Perf 和火焰图分析 CPU 性能 http://senlinzhan.github.io/2018/03/18/perf/

Linux之TCPIP内核参数优化 https://www.cnblogs.com/fczjuever/archive/2013/04/17/3026694.html

```
/etc/sysctl.conf文件
/etc/sysctl.conf是一个允许你改变正在运行中的Linux系统的接口。它包含一些TCP/IP堆栈和虚拟内存系统的高级选项，可用来控制Linux网络配置，由于/proc/sys/net目录内容的临时性，建议把TCPIP参数的修改添加到/etc/sysctl.conf文件, 然后保存文件，使用命令“/sbin/sysctl –p”使之立即生效。具体修改方案参照上文：

net.core.rmem_default = 256960

net.core.rmem_max = 513920

net.core.wmem_default = 256960

net.core.wmem_max = 513920

net.core.netdev_max_backlog = 2000

net.core.somaxconn = 60000

net.core.optmem_max = 81920

net.ipv4.tcp_mem = 131072  262144  524288

net.ipv4.tcp_rmem = 8760  256960  4088000

net.ipv4.tcp_wmem = 8760  256960  4088000

net.ipv4.tcp_keepalive_time = 1800

net.ipv4.tcp_keepalive_intvl = 30

net.ipv4.tcp_keepalive_probes = 3

net.ipv4.tcp_sack = 1

net.ipv4.tcp_fack = 1

net.ipv4.tcp_timestamps = 1

net.ipv4.tcp_window_scaling = 1

net.ipv4.tcp_syncookies = 1

net.ipv4.tcp_tw_reuse = 1

net.ipv4.tcp_tw_recycle = 1

net.ipv4.tcp_fin_timeout = 30

net.ipv4.ip_local_port_range = 1024  65000

net.ipv4.tcp_max_syn_backlog = 2048
```



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



```
perf安装
--------------------------------------

sudo yum install perf
```



```java
请求合并
-----------------------------------------------

package www.itbac.com;

import javax.annotation.PostConstruct;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.*;

public class CompletableFutureTest {

    //并发安全的阻塞队列，积攒请求。（每隔N毫秒批量处理一次）
    LinkedBlockingQueue<Request> queue = new LinkedBlockingQueue();

    // 定时任务的实现,每隔开N毫秒处理一次数据。
    @PostConstruct
    public void init() {
        // 定时任务线程池
        ScheduledExecutorService scheduledExecutorService = Executors.newScheduledThreadPool(1);
        scheduledExecutorService.scheduleAtFixedRate(new Runnable() {
            @Override
            public void run() {
//                捕获异常
                try {
                    //1.从阻塞队列中取出queue的请求，生成一次批量查询。
                    int size = queue.size();
                    if (size == 0) {
                        return;
                    }
                    List<Request> requests = new ArrayList<>(size);
                    for (int i = 0; i < size; i++) {
                        // 移出队列，并返回。
                        Request poll = queue.poll();
                        requests.add(poll);
                    }
                    //2.组装一个批量查询请求参数。
                    List<String> movieCodes = new ArrayList<>();
                    for (Request request : requests) {
                        movieCodes.add(request.getMovieCode());
                    }
                    //3. http 请求，或者 dubbo 请求。批量请求，得到结果list。
                    System.out.println("本次合并请求数量："+movieCodes.size());
                    List<Map<String, Object>> responses = new ArrayList<>();

                    //4.把list转成map方便快速查找。
                    HashMap<String, Map<String, Object>> responseMap = new HashMap<>();
                    for (Map<String, Object> respons : responses) {
                        String code = respons.get("code").toString();
                        responseMap.put(code,respons);
                    }
                    //4.将结果响应给每一个单独的用户请求。
                    for (Request request : requests) {
                        //根据请求中携带的能表示唯一参数，去批量查询的结果中找响应。
                        Map<String, Object> result = responseMap.get(request.getMovieCode());

                        //将结果返回到对应的请求线程。2个线程通信，异步编程赋值。
                        //complete(),源码注释翻译：如果尚未完成，则将由方法和相关方法返回的值设置为给定值
                        request.getFuture().complete(result);
                    }

                } catch (Exception e) {
                    e.printStackTrace();
                }

            }
            // 立即执行任务，并间隔10 毫秒重复执行。
        }, 0, 10, TimeUnit.MILLISECONDS);

    }

    // 1万个用户请求，1万个并发,查询电影信息
    public Map<String, Object> queryMovie(String movieCode) throws ExecutionException, InterruptedException {
        //请求合并，减少接口调用次数,提升性能。
        //思路：将不同用户的同类请求，合并起来。
        //并非立刻发起接口调用，请求 。是先收集起来，再进行批量请求。
        Request request = new Request();
        //请求参数
        request.setMovieCode(movieCode);
        //异步编程，创建当前线程的任务，由其他线程异步运算，获取异步处理的结果。
        CompletableFuture<Map<String, Object>> future = new CompletableFuture<>();
        request.setFuture(future);

        //请求参数放入队列中。定时任务去消化请求。
        queue.add(request);

        //阻塞等待获取结果。
        Map<String, Object> stringObjectMap = future.get();
        return stringObjectMap;
    }

}
    //请求包装类
    class Request {

    //请求参数： 电影id。
    private String movieCode;

    // 多线程的future接收返回值。
    //每一个请求对象中都有一个future接收请求。
    private CompletableFuture<Map<String, Object>> future;



    public CompletableFuture<Map<String, Object>> getFuture() {
        return future;
    }

    public void setFuture(CompletableFuture<Map<String, Object>> future) {
        this.future = future;
    }

    public Request() {
    }

    public Request(String movieCode) {
        this.movieCode = movieCode;
    }

    public String getMovieCode() {
        return movieCode;
    }

    public void setMovieCode(String movieCode) {
        this.movieCode = movieCode;
    }
}
```

工程优化

```
搭建脚手架
https://blog.csdn.net/IT_faquir/article/details/96146190


4-2，删除脚手架
找到C:\Users\用户名\.IntelliJIdea2017.2\system\Maven\Indices\UserArchetypes.xml文件，删除对应的脚手架。
```

