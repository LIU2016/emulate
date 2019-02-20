# 一、性能监控及基础知识

## 性能优化

性能优化就是发挥机器本来的性能

## 性能的维度以及linux服务器下分析方法、工具

### cpu

[top]( http://man7.org/linux/man-pages/man1/top.1.html)

#### 定位高cpu的问题

```shell
A. top 找到 CPU 高的进程 （原理：方法是由线程执行的，线程是在进程下的，找到进程下 cpu 最高的线程就能定位到方法）
B. Shift + H 切换到线程模型 找到线程执行 cpu 高的线程号
C. Jstack pid > p.txt 用 jstack 导出线程的 dump (记住这个问题有时候没有那么明显一直 cpu100%，可能是间歇性的 cpu 高所以这个能抓住这个线程还是要看运气)
D. 把线程号转 16 进制 printf “%x \n” 40437
E. 到刚刚导出的 p.txt 里面检索定位到
```

### memory

[vmstat](http://www.man7.org/linux/man-pages/man8/vmstat.8.html)

```
buffer与cache的区别（提高系统的速度）：写在buffer，读在cache
查看linux的内存命令：
free -m
vmstat 1
```

### io

[iostat](http://www.man7.org/linux/man-pages/man1/iostat.1.html) （%util ：表示io在这段时间使用cpu百分比）

```
df -h  看可使用磁盘
du -h 
```

### network

[nicstat](http://sourceforge.net/projects/nicstat/files/nicstat-1.92.tar.gz)

```
tar -zxvf nicstat-1.92.tar.gz
sudo vim Makefile
CFLAGS = $(COPT) -m32#将此行修改为如下：
CFLAGS = $(COPT)
sudo make -f Makefile install
```

## 性能的监控软件以及术语

### 监控软件

<https://www.zabbix.com/documentation/2.0/manual/appendix/api/api>
服务器层监控软件

```
zabbix 
nagios 
prometheus
http层监控\rpc
zipkin
```

### 术语 QPS、tps

吞吐量：对单位时间内完成的工作量的度量
平均响应时间：提交请求和返回该请求的响应之间使用的时间平均响应时间越短，系统吞吐量越大；平均响应时间越长，系统吞吐量越小；但是，系统吞吐量越大，未必平均响应时间越短；因为在某些情况（例
如，不增加任何硬件配置）吞吐量的增大，有时会把平均响应时间作为牺牲，来换取一段时间处理更多的请求。
tps: Transactions per Second （包含：qps 和 wps(写)）
qps: Queries per Second
QPS: 经过全链路压测，计算单机极限QPS，集群 QPS = 单机 QPS * 集群机器数量 * 可靠性比率（多次压测）
全链路压测 除了压 极限QPS，还有错误数量
全链路：一个完整的业务流程操作
JMeter：可调整型比较灵活

### JDK自带的 监控工具

<https://docs.oracle.com/javase/8/docs/technotes/tools/windows/toc.html>
jmap -heap pid 堆使用情况
jstat  -gcutil pid 1000
jstack  线程dump 
jvisualvm
jconsole
死锁不会影响CPU，但会影响资源消耗，线程数有限

### MAT - java内存查看工具

```
1.看GC日志  126719K->126719K(126720K)
2.dump 
3.MAT
\>1.占用Retained Heap
\>2.看有没有GC Root指向
```

[参考文档](http://help.eclipse.org/photon/index.jsp?topic=/org.eclipse.mat.ui.help/welcome.html)

dump获取方法

```
1，java虚拟机打印：
jmap -dump:live,format=b,file=provider.hprof

2，服务器配置：
-XX:+HeapDumpOnOutOfMemoryError 
-XX:HeapDumpPath=/home/administrator/james/error.hprof
```

#### 使用mat查找内存使用情况步骤

1，找面积最大的

![img](https://img.mubu.com/document_image/d6f0ad5e-ee5c-421d-885b-a934b25334f0-862021.jpg)

2，点击dominator_tree，找到关键字

![img](https://img.mubu.com/document_image/48899359-8492-4473-8d7f-bfbaed5a5516-862021.jpg)

注意，若是文件太大，打开太慢，加大MemoryAnalyzer.ini的内存大小。

### VisualVM - 远程java监控工具

1,[下载](https://visualvm.github.io/download.html)

2,配置

```properties
tomcat服务器配置：
-Dcom.sun.management.jmxremote=true 
-Dcom.sun.management.jmxremote.port=8099（配置远程 connection 的端口号的） 
-Dcom.sun.management.jmxremote.ssl=false(指定了 JMX 是否启用 ssl) 
-Dcom.sun.management.jmxremote.authenticate=false（ 指定了JMX 是否启用鉴权（需要用户名，密码鉴权）） 
-Djava.rmi.server.hostname=192.168.0.1（配置 server 的 IP）
例子：
JAVA_OPTS="$JAVA_OPTS -Dcom.sun.management.jmxremote=true -Dcom.sun.management.jmxremote.port=9999 -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false -Djava.rmi.server.hostname=192.168.118.243"
```

```properties
visualvm 监控jar启动的vm:
nohup java -Djava.rmi.server.hostname=192.168.210.14 -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=9999 -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false -jar /home/openapi-aihomework/tw-cloud-openapi-aihomework-1.1.5-exc.jar --twasp.config.uri=http://dev.teewon.net:9300/configs --eureka.client.serviceUrl.defaultZone=http://dev.teewon.net:9100/eureka/ --server.port=9628 --spring.redis.cluster.nodes=dev.teewon.net:7001,dev.teewon.net:7002,dev.teewon.net:7003,dev.teewon.net:7004,dev.teewon.net:7005,dev.teewon.net:7006 > console.log 2>&1 &

```

3,使用

增加内存 : 在visualvmxx\conf\visualvm.conf 文件中，查找visualvm_default_options="-J-client ，修改Xms和Xmx，如：

```
visualvm_default_options="-J-client -J-Xms512m -J-Xmx1024m -J-Dnetbeans.accept_license_class=com.sun.tools.visualvm.modules.startup.AcceptLicense -J-Dsun.jvmstat.perdata.syncWaitMs=10000 -J-Dsun.java2d.noddraw=true -J-Dsun.java2d.d3d=false -J-Dorg.netbeans.core.TimeableEventQueue.quantum=360000 -J--add-exports=java.desktop/sun.awt=ALL-UNNAMED -J--add-exports=jdk.internal.jvmstat/sun.jvmstat.monitor.event=ALL-UNNAMED -J--add-exports=jdk.internal.jvmstat/sun.jvmstat.monitor=ALL-UNNAMED -J--add-exports=java.desktop/sun.swing=ALL-UNNAMED -J--add-exports=jdk.attach/sun.tools.attach=ALL-UNNAMED -J--add-modules=java.activation -J--add-opens=java.base/[java.net](http://java.net)=ALL-UNNAMED -J--add-opens=java.base/java.lang.ref=ALL-UNNAMED -J--add-opens=java.base/java.lang=ALL-UNNAMED -J--add-opens=java.desktop/javax.swing=ALL-UNNAMED -J--add-opens=java.desktop/javax.swing.plaf.basic=ALL-UNNAMED -J-XX:+IgnoreUnrecognizedVMOptions"
```



### Jconsole - 远程java监控工具

### Spotlight - linux服务器监控工具

### 数据库监控

#### pgsql

1,安装pgadmin监控

2,show max_connections; 查询最大连接数
最大连接数也可以在pg配置文件中配置：
在postgresql.conf中设置:max_connections = 500

3,select count(*) from pg_stat_activity; 查询当前连接数



# 二、性能测试

## 性能测试是什么

![1549854361479](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1549854361479.png)性能测试是为了验证在一定环境下系统满足性能需求的测试，主要是验证性能指标（响应时间，吞吐量，资源利用率）

## 性能测试TPC

```
TPC(Transactionprocessing Performance Council)
事务处理性能委员会)是由数十家会员公司创建的非盈利组织，总部设在美国。TPC的成员主要是计算机软硬件厂家，而非计算机用户，其功能是制定商务应用基准程序的标准规范、性能和价格度量，并管理测试结果的发布。
>TPC不给出基准程序的代码，而只给出基准程序的标准规范。任何厂家或其他测试者都可以根据规范，最优地构造出自己的测试系统(测试平台和测试程序)。为保证测试结果的完整性，被测试者(通常是厂家)必须提交给TPC一套完整的报告(Full Disclosure Report)，包括被测系统的详细配置、分类价格和包含5年维护费用在内的总价格。该报告必须由TPC授权的审核员核实(TPC本身并不做审计)。TPC在全球只有不到10名审核员，全部在美国。
>TPC推出过11套基准程序，分别是正在使用的TPC-App、TPC-H、TPC-C、TPC-W，过时的TPC-A、TPC-B、TPC-D和TPC-R，以及因为不被业界接受而放弃的TPC-S（Server专门测试基准程序）、TPC-E（大型企业信息服务测试基准程序）和TPC-Client/Server。而目前最为“流行”的TPC-C是在线事务处理(OLTP)的基准程序，于1992年7月完成，后被业界逐渐接受。
```

## 性能测试SPEC

```
SPEC指标体系由Standard Performance Evaluation Corp.制定，目前主要包括针对CPU性能的SPEC CPU2000（已有CPU2006，但尚无数据）、针对Web服务器的SPECweb2005、针对高性能计算的SPEC HPC2002与SPEC MPI2006、针对Java应用的jAppServer2004与JBB2005以及对图形系统、网络和邮件服务器的测试指标。
```

## TPC VS SPEC

![1549854511719](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1549854511719.png)

## 性能测试的难点

![1549854537324](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1549854537324.png)

## 性能测试的原理

模拟客户端对服务器进行多连接，伪造报文欺骗服务器认证机制
>1.了解服务器认证机制
>2.了解客户<->服务器之间的交流报文结构
>3.合理的技术构造报文结构

## 性能测试技术

![1549854678683](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1549854678683.png)

## 性能工具

### Jmeter简介

![img](https://img.mubu.com/document_image/74d7129f-4a43-4df4-aa6c-63c9bdce6a73-862021.jpg)

[参考文档](https://blog.csdn.net/github_27109687/article/details/71968662)

### loadrunner工具

安装、使用 参考百度网盘，注册证书时要以管理员启动

#### 脚本阅读

```java
web_reg_save_param
int web_reg_save_param(const char *ParamName, <list of Attributes>, LAST);
参数说明:
· ParamName: 存放得到的动态内容的参数名称
· list of Attributes: 其它属性，包括：Notfound, LB, RB, RelFrameID, Search, ORD, SaveOffset, Convert, SaveLen。属性值不分大小写
o Notfound: 当在返回信息中找不到要找的内容时应该怎么处理
o Notfound=error: 当在返回信息中找不到要找的内容时，发出一个错误讯息。这是缺省值。
o Notfound=warning: 当在返回信息中找不到要找的内容时，只发出警告，脚本也会继续执行下去不会中断。
o LB( Left Boundary ) : 返回信息的左边界字串。该属性必须有，并且区分大小写。
o RB( Right Boundary ): 返回信息的右边界字串。该属性必须有，并且区分大小写。
o RelFrameID: 相对于URL而言，欲查找的网页的Frame。此属性质可以是All或是数字，该属性可有可无。
o Search : 返回信息的查找范围。可以是Headers，Body，Noresource，All(缺省)。该属性质可有可无。
o ORD : 说明第几次出现的左边界子串的匹配项才是需要的内容。该属性可有可无，缺省值是1。如为All，则将所有找到的内容储存起来。
o SaveOffset : 当找到匹配项后，从第几个字元开始存储到参数中。该属性不能为负数，缺省值为0。
o SaveLen ：当找到匹配项后，偏移量之后的几个字元存储到参数中。缺省值是-1，表示一直到结尾的整个字串都存入参数。
```

#### 常见设置

![img](https://img.mubu.com/document_image/f9a39e2f-4b11-44f1-823a-1e33545f3375-862021.jpg)

设置多台服务器压测 - 连接的服务器要开启Agent

![img](https://img.mubu.com/document_image/c067bcf3-36f5-4b4b-9b9e-76f1afea7902-862021.jpg)

![img](https://img.mubu.com/document_image/65051014-8151-4128-b64e-15ba4bed5b16-862021.jpg)

![img](https://img.mubu.com/document_image/71154ed0-4aae-41b0-9b17-41503dc3582d-862021.jpg)

设置日志输出

![img](https://img.mubu.com/document_image/049c2bf3-9de1-45cb-aefd-91eb79dd5ab5-862021.jpg)

查看错误日志

可以查看error提示，点击右侧的error查看，里边是按类型去区分的：

![img](https://img.mubu.com/document_image/9661b9a3-19e0-44f5-9f4f-8426130f9ef1-862021.jpg)

可以根据运行日志查看，点击Vusers,选择一个用户，点击右上角的日志图标，下方会显示具体日志：

![img](https://img.mubu.com/document_image/47cc75dc-c5ab-4db2-8199-1b6b64f152c1-862021.jpg)

#### 查看分析报告

当运行完后点击菜单栏的Results-》Analysis Results

![img](https://img.mubu.com/document_image/2e5ebc0d-54a4-4607-bf67-62ed4caecd26-862021.jpg)

![img](https://img.mubu.com/document_image/02b56ff8-fdfc-4f15-8b4a-fed6c8591ecf-862021.jpg)

![img](https://img.mubu.com/document_image/a34b2665-27a9-49ad-b330-05027915b237-862021.jpg)

![img](https://img.mubu.com/document_image/d18a23c2-2c35-47fe-9de2-a53382800654-862021.jpg)

1.Vuser 
2.Transactions 
3.Web Resources 
4.Web Page Breakdown 
5.System Resources

首先，查看分析综述（Analysis Summary）
包括：统计综述（Statistics Summary）、事务综述（Transaction Summary）、HTTP 响应综述（HTTP Responses Summary）三部分。
统计综述查看Total Errors的数量
事务综述查看事务成功数量和平均时间等
http响应综述查看http 404数量

统计综述
Maximum Running Vusers：最大的运行并发数
Total Throughput（bytes）：总吞吐量（字节）
Average Throughput（bytes/second）：平均吞吐量（字节/秒）
Total Hits：总点击量
Average Hits per Second：平均每秒点击率

事务综述（Transaction Summary）：
该图可以直观地看出在测试时间内事务的成功与失败情况，所以比第一步更容易判断出被测系统运行是否正常
Transaction Name：事务名称
Minimum：最小时间
Average:平均时间
Maximum：最大时间
90 percent：90%的最大时间
Pass：通过事务数量
Fail：失败事务数量
Stop：停止事务个数

HTTP 响应综述（HTTP Responses Summary）：
HTTP Responses Summary：http 响应总数
Total：总数
Per second：每秒响应数

TPS中有Action_Transaction 和 vuser_init_Transaction

![img](https://img.mubu.com/document_image/5e3c3a9a-c8dd-4977-9492-1067e563dc96-862021.jpg)

Runtime-Settings-Miscellaneous--Automatic Transactions把这两个复选框点上---保存.然后再取消---保存即可...

## 性能测试实施

![1549855126900](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1549855126900.png)

## 性能分析模型

![1549855148384](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1549855148384.png)



通过理发师模型了解性能模型

```
负载与响应时间的关系
负载与吞吐量的关系
负载状态的判断
```

## 性能配置测试与基准测试

![1549855235598](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1549855235598.png)

# 三、性能优化

Java代码优化、sql优化、表设计、框架优化

## 宗旨

![img](https://img.mubu.com/document_image/87571f81-d8b7-48a6-8130-bdd8e130141a-862021.jpg)

## 1，应用程序

### 代码优化-算法

参考算法，此处略

### sql优化

#### sql执行顺序

```
SQL Select语句完整的执行顺序【从DBMS使用者角度】：
1、from子句组装来自不同数据源的数据；
2、where子句基于指定的条件对记录行进行筛选；
3、group by子句将数据划分为多个分组；
4、使用聚集函数进行计算；
5、使用having子句筛选分组；
6、计算所有的表达式；
7、使用order by对结果集进行排序。

SQL Select语句的执行步骤【从DBMS实现者角度，这个对我们用户意义不大】：
1）语法分析，分析语句的语法是否符合规范，衡量语句中各表达式的意义。
2）语义分析，检查语句中涉及的所有数据库对象是否存在，且用户有相应的权限。
3）视图转换，将涉及视图的查询语句转换为相应的对基表查询语句。
4）表达式转换， 将复杂的SQL 表达式转换为较简单的等效连接表达式。
5）选择优化器，不同的优化器一般产生不同的“执行计划”
6）选择连接方式， ORACLE 有三种连接方式，对多表连接 ORACLE 可选择适当的连接方式。
Nested Loops，Hash Join 和 Sort Merge Join
参考文档<https://www.cnblogs.com/xqzt/p/4469673.html>
7）选择连接顺序， 对多表连接 ORACLE 选择哪一对表先连接，选择这两表中哪个表做为源数据表。
8）选择数据的搜索路径，根据以上条件选择合适的数据搜索路径，如是选用全表搜索还是利用索引或是其他的方式。
9）运行“执行计划”。
```

执行过程中也会相应的产生多个虚拟表（下面会有提到），以配合最终的正确查询。

![img](https://img.mubu.com/document_image/da231485-ec3a-4f51-9a1f-0a440353b3d8-862021.jpg)

#### 实践

pgsql 查看执行计划 通过pgadmin可以分析。

![img](https://img.mubu.com/document_image/cdcf0f9b-b5c4-4ca5-a5a3-b427711e338d-862021.jpg)

参考文档

<https://blog.csdn.net/bitcarmanlee/article/details/51004767>

<https://www.cnblogs.com/huminxxl/p/3149097.html>

执行计划

```
relationship中的inner initplan
```

1，最蠢也最不负责，同时最快的途径是建立索引。

2，尽量使用索引，主键、唯一键（特别注意联合）都是走索引的，如
t_e_resources表是resourcesid + resourcestype 是组合索引 。加粗后就会利用到索引，查询速度要快很多。

```sql
select
t1.paperId,t1.title,t1.type,t1.status,t1.subjectId,t1.totalScore,t1.grade,t1.term,t1.passScore,
t1.excellentScore,t1.isbn,t1.detail,t1.papercode,
t1.versionno,
t1.refertimes,
t1.clicktimes,
t1.downtimes,
( SELECT r.createtime FROM t_e_resources r WHERE r.resourcesid = t1.paperid and r.resourcestype = '2' LIMIT 1 ) AS createDate,
t1.creatorId,
t1.updateDate,
t1.lastmodifier,t1.paragraphId,t1.publishVersion,t1.orgid,t1.jsonpath,t1.wordpath,t1.sourceid,t1.editiontypeid,
t1.keyword,t1.avgDegree,t1.share,t1.useTime,t1.startDate,t1.endDate,t1.delTime,t1.delUser,t1.pmodel,t1.isallowedit,t1.json_md5 as papermd5
from
t_e_paper t1 
where 1=1
and	t1.paperId='S000586600000087663'
```

3，去掉 * 号查询。

4，根据传参去掉多余的sql动作。去掉多余的表关联。-- 去掉这种关联,sql的优化 ，可以通过业务的流程上处理，减少查询条件和关联表的去掉上。例如状态：

![img](https://img.mubu.com/document_image/165cfcdd-29f0-4275-9d9d-cebdb6251df1-862021.jpg)

优化后：

```sql
explain analyze
SELECT 
  catalogid,
count(picid)
FROM
t_con_catalog_picture 
where
catalogid IN ( 'S000586200000005411' ) 
GROUP BY catalogid;
```

5，减少sql嵌套查询 -- 用java代码处理。

6，动态分析sql，压测工程中可能关联的表的数据由于压测不停激增，这时会导致TPS不停增加 。 

### java代码优化

```
能用异步处理就异步。
减少for sql 的操作。
注意流关闭的问题。
注意池是否满的问题。
尽量使用缓存。
缓存服务器的反复调用的性能问题。
```

### 存储设计

凡是统计字段都应该用冗余字段存储（db存，也可以是缓存来存）

### 框架优化

#### mybatis优化 - 添加缓存

对于分布式环境，建议：要使用mybatis+memcached的方式

具体操作如下：

1，添加依赖包

```xml
<dependency>
<groupId>net.spy</groupId>
<artifactId>spymemcached</artifactId>
<version>2.10.6</version>
<scope>compile</scope>
</dependency>
<dependency>
<groupId>com.github.jsqlparser</groupId>
<artifactId>jsqlparser</artifactId>
<version>1.2</version>
</dependency>
```

2，参考<http://www.mybatis.org/memcached-cache/> 获取源码，修改成符合目前框架的结构。

3，添加mybatis拦截器（由于mybatis自己的框架只能支持清楚mapper的缓存，所以修改为：自动收集 缓存的sql的namespace与关联表的映射关系，方便当关联表被修改时，清空这些对应的mapper缓存）

配置

```xml
<plugins>
<plugin interceptor="com.huawei.imp.framework.cache.memcached.TWSMMemcachedInterceptor" />
</plugins>
```

需要添加缓存的配置开启config.xml

```xml
<settings>
<setting name="cacheEnabled" value="true" />
<setting name="localCacheScope" value="SESSION" />
</settings>
```

mapper上添加配置

```xml
<cache type="com.huawei.imp.framework.cache.memcached.TWSMMemcachedCache"/>
```

## 2，linux服务器优化



## 3，中间件优化

### nginx

参考NGINX.md

### memcached

参考MEMCACHED.md

## 4，运行环境优化

参考jvm，此处略

## 5，其他优化

```
许多研究发现，页面速度和访客的滞留时间，跳出率以及收入都有直接的关系。另外，谷歌的排名算法中也把页面加载速度作为其中一项考虑因素。因此，你网站的页面加载时间是至关重要的。从访问者的角度看，测试你的浏览器速度的一个很好的方法是清除你的浏览器缓存，然后加载页面。小于2秒的页载入时间被认为是优良的，而且高达4秒是可接受的。而大于5秒的页面载入时间不仅影响你网站的搜索引擎排名，还会严重影响用户体验。这里列出了10种方法，可以快速提升你网站的性能。
1. 优化图像
图像对于吸引访客的关注是很重要的。但是你添加到页面上的每一张图片都需要用户从你的服务器下载到他们的电脑上。这无疑增加了页面的加载时间，因此很可能让用户离开你的网站。所以，优化图像是非常必要的。
过大的图像需要的下载时间更多，因此要确保图像尽可能的小。可以使用图像处理工具如PS来减小颜色深度、剪切图像到合适的尺寸等。
2. 去掉不必要的插件
一个非常值得关注但经常被忽略的因素是你网站安装的插件。如今，大量免费的插件诱导网站开发者添加很多不必要的功能。您安装的每个插件都需要服务器处理，从而增加了页面加载时间。所以禁用和删除不必要的插件。
然而，有些插件是必须的，如社交分享插件，你可以选择CMS内置的社交分享功能来代替安装插件。
3. 减少DNS查询(DNS lookups)
减少DNS查询是一个WEB开发人员可以用了页面加载时间快速有效的方法。DNS查询需要话费很长的时间来返回一个主机名的IP地址。而浏览器在查询结束前不会进行任何操作。对于不同的元素可以使用不同的主机名，如URL、图像、脚本文件、样式文件、FLASH元素等。具有多种网络元素的页面经常需要进行多个DNS查询，因而花费的时间更长。
减少不同域名的数量将减少并行下载的数量，加速你的网站
4. 最小化重定向
重定向增加了额外的HTTP请求，因此也增加了页面加载时间。然而有时重定向却是不可避免的，如链接网站的不同部分、保存多个域名、或者从不存在的页面跳转到新页面。
重定向增加了延迟时间，因此要尽量避免使用它。检查是否有损坏的链接，并立即修复。
5. 使用内容分发网络（Content Delivery Network CDN）
服务器处理大流量是很困难的，这最终会导致页面加载速度变慢。而使用CDN就可以解决这一问题，提升页面加载速度。
CDN是位于全球不同地方的高性能网络服务，复制你网站的静态资源，并以最有效的方式来为访客服务。
6. 把CSS文件放在页面顶部，而JS文件放在底部
把CSS文件在页面底部引入可以禁止逐步渲染，节省浏览器加载和重绘页面元素的资源。
JavaScript是用于功能和验证。把JS文件放在页面底部可以避免代码执行前的等待时间，从而提升页面加载速度。
这些都是一些减少页面加载时间和提高转换率的方法。在某些情况下，需要JavaScript在页面的顶部加载（如某些第三方跟踪脚本）。
7. 利用浏览器缓存
浏览器缓存是允许访客的浏览器缓存你网站页面副本的一个功能。这有助于访客再次访问时，直接从缓存中读取内容而不必重新加载。这节省了向服务器发送HTTP请求的时间。此外，通过优化您的网站的缓存系统往往也会降低您的网站的带宽和托管费用。
8. 使用 CSS Sprites 整合图像
多图像的网站加载时间比较久。其中一个解决方法就是把多个图像整合到少数几个输出文件中。你可以使用 CSS Sprites 来整合图像文件。这样就减少了在下载其他资源时的往返次数和延迟，从而提高了站点的速度。
9. 压缩CSS和JavaScript
压缩是通过移除不必要的字符（如TAB、空格、回车、代码注释等），以帮助减少其大小和网页的后续加载时间的过程。这是非常重要的，但是，你还需要保存JS和CSS的原文件，以便更新和修改代码。
10. 启用GZIP压缩
在服务器上压缩网站的页面是提升网站访问速度非常有效的一种方法。你可以用gzip压缩做到这一点。Gzip是一个减小发送给访客的HTML文件、JS和CSS体积的工具。压缩的文件减少了HTTP响应时间。据Yahoo报道，这大概可以减少70%的下载时间。而目前90%的通过浏览器的流量都支持Gzip压缩，因此，这是一个提示网站性能有效的选项。
优化你的网站是留住你的访客和提升搜索引擎排名有效的途径。使用上面提到的10种方法来提高你的网站性能。
```

