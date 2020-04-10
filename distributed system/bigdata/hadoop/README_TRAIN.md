[1.  HADOOP入门	6](#_Toc421731811)

[1.1 大数据部分的课程介绍	6](#_Toc421731812)

[1.2 学习建议	6](#_Toc421731813)

[1.3 就业前景及发展规划	6](#_Toc421731814)

[1.4  HADOOP简介	7](#_Toc421731815)

[1.4.1 前言	7](#_Toc421731816)

[1.4.2  hadoop应用场景	7](#_Toc421731817)

[1.5 hadoop集群部署安装	7](#_Toc421731818)

[2. HDFS	9](#_Toc421731819)

[2.1  hdfs的shell操作	10](#_Toc421731820)

[2.2  HDFS的一些concept（概念）和特性	11](#_Toc421731821)

[2.3  HDFS的java操作	11](#_Toc421731822)

[2.4  hdfs的工作机制	12](#_Toc421731823)

[2.5  namenode工作机制	14](#_Toc421731824)

[2.6  datanode的工作机制	14](#_Toc421731825)

[2.7 一些补充	15](#_Toc421731826)

[3. 深入hdfs源码	16](#_Toc421731827)

[3.1 hdfs 读数据流程	16](#_Toc421731828)

[3.2 hdfs 写数据流程	16](#_Toc421731829)

[3.3 hadoop的RPC框架	16](#_Toc421731830)

[3.4 hdfs 读数据源码分析	18](#_Toc421731831)

[3.5 hdfs 写数据源码分析	18](#_Toc421731832)

[3.6 远程debug跟踪Hadoop服务端代码	18](#_Toc421731833)

[4. MAPREDUCE入门	22](#_Toc421731834)

[4.1 为什么要MAPREDUCE	22](#_Toc421731835)

[4.2 MAPREDUCE程序运行演示	22](#_Toc421731836)

[4.3 MAPREDUCE 编程规范	22](#_Toc421731837)

 

[4.5 MAPREDUCE程序提交运行模式及debug方法	24](#_Toc421731839)

[4.5.1 本地运行模式	24](#_Toc421731840)

[4.5.2 集群运行模式	25](#_Toc421731841)

[4.6 MAPREDUCE中的Combiner	25](#_Toc421731842)

[4.7 MAPREDUCE中的序列化	30](#_Toc421731843)

[4.8 Mapreduce的排序初步	31](#_Toc421731844)

[5. Mapreduce高级特性（一）	31](#_Toc421731845)

[5.1 Partitioner编程	31](#_Toc421731846)

[5.2 Mapreduce的排序	31](#_Toc421731847)

[5.2.1 partital排序示例，多reduce task 自动实现各输出文件有序	32](#_Toc421731848)

[5.2.3 total排序机制	32](#_Toc421731849)

[5.2.4 secondary排序机制	34](#_Toc421731850)

[5.3 shuffle详解	39](#_Toc421731851)

[5.4 mr程序map任务数的规划机制	40](#_Toc421731852)

[5.5 Mapreduce的join算法	40](#_Toc421731853)

[5.6 mapreduce的Distributed cache	44](#_Toc421731854)

[6. Mapreduce高级特性（二）	45](#_Toc421731855)

[6.1  Mapreduce输入格式组件	45](#_Toc421731856)

[6.1.1 由 map task数量的决定机制引入：	45](#_Toc421731857)

[6.1.2 InputFormat的继承体系	46](#_Toc421731858)

[6.2 MultipleInputs	48](#_Toc421731859)

[6.3 自定义Inputformat	49](#_Toc421731860)

[6.4 Mapreduce输出格式组件	52](#_Toc421731861)

[6.4.1 TextOutPutFormat源码结构解析：	52](#_Toc421731862)

[6.4.2 MultipleOutputs	52](#_Toc421731863)

[6.4.3 自定义FileOutPutFormat	52](#_Toc421731864)

[6.5 Configuration配置对象与Toolrunner	52](#_Toc421731865)

[6.6 mapreduce数据压缩	54](#_Toc421731866)

[6.7 mapreduce的计数器	56](#_Toc421731867)

[6.7.1 mapreduce框架自带计数器：	56](#_Toc421731868)

[6.7.2 用户自定义计数器：	56](#_Toc421731869)

[6.8 mapreduce的日志分析	56](#_Toc421731870)

[6.9 多job串联	57](#_Toc421731871)

[7. Yarn集群	58](#_Toc421731872)

[7.1 Yarn产生的原因	58](#_Toc421731873)

[7.2 Yarn的架构	58](#_Toc421731874)

[7.3 Yarn运行application的流程	59](#_Toc421731875)

[7.4 MapReduce程序向yarn提交执行的流程分析	60](#_Toc421731876)

[7.5 application生命周期	60](#_Toc421731877)

[7.5资源请求	60](#_Toc421731878)

[7.6 任务调度--capacity scheduler / fair scheduler	60](#_Toc421731879)

[7.6.1 Scheduler概述	61](#_Toc421731880)

[7.6.2 Capacity Scheduler配置	62](#_Toc421731881)

[7.6.3 Fair Scheduler配置	64](#_Toc421731882)

[7.7 yarn应用程序开发（仅做了解，通常不需要应用开发人员来做）	67](#_Toc421731883)

[8. zookeeper	67](#_Toc421731884)

[8.1 hadoop-sp问题及HA解决思路	67](#_Toc421731885)

[8.2 zookeeper简介	67](#_Toc421731886)

[8.3 zookeeper集群搭建	67](#_Toc421731887)

[8.4 zookeeper演示测试	68](#_Toc421731888)

[8.5 zookeeper-api应用	71](#_Toc421731889)

[8.5.1 基本使用	71](#_Toc421731890)

[8.5.2 demo增删改查	71](#_Toc421731891)

[8.6  zookeeper应用案例（分布式应用HA||分布式锁）	72](#_Toc421731892)

[9. Hadoop-HA	81](#_Toc421731893)

[9.2 Federation机制、配置	82](#_Toc421731894)

[9.3 CDH介绍，演示	82](#_Toc421731895)

[10. Hbase基础	82](#_Toc421731896)

[10.1 hbase数据库介绍	82](#_Toc421731897)

[10.2 hbase集群结构	84](#_Toc421731898)

[10.3 hbase集群搭建	84](#_Toc421731899)

[10.4 命令行演示	86](#_Toc421731900)

[10.4.1 基本shell命令	86](#_Toc421731901)

[10.4.2 建表高级属性	89](#_Toc421731902)

[10.5 hbase代码开发（基本，过滤器查询）	92](#_Toc421731903)

[10.6 hbase工作原理	96](#_Toc421731904)

[10.6.1  物理存储	96](#_Toc421731905)

[10.6.2  系统架构	98](#_Toc421731906)

[10.6.3  寻址机制	99](#_Toc421731907)

[10.6.4  Region管理	100](#_Toc421731908)

[10.6.5  Master工作机制	101](#_Toc421731909)

[11.  Hbase高级应用	102](#_Toc421731910)

[11.1 hbase应用案例看行键设计	102](#_Toc421731911)

[11.2 Hbase和mapreduce结合	102](#_Toc421731912)

[11.2.1 从Hbase中读取数据写入hdfs	102](#_Toc421731913)

[11.2.2 从Hbase中读取数据写入hdfs	104](#_Toc421731914)

[11.3 hbase高级编程	106](#_Toc421731915)

[11.3.1 协处理器	106](#_Toc421731916)

[11.3.2 二级索引demo	106](#_Toc421731917)

[12.  Hive基础	106](#_Toc421731918)

[12.1 hive引入	106](#_Toc421731919)

[12.2 hive技术架构	106](#_Toc421731920)

[12.3 hive原理----元数据、数据存储、核心机制	107](#_Toc421731921)

[12.4 Hive的安装部署	107](#_Toc421731922)

[12.5 Hive使用方式	107](#_Toc421731923)

[12.6 hql基本语法	108](#_Toc421731924)

[12.6.1 基本hql语法	108](#_Toc421731925)

[12.6.2  hql查询进阶	111](#_Toc421731926)

[12.7 hive数据类型	114](#_Toc421731927)

[13.  Hive高级应用	115](#_Toc421731928)

[13.1  Hive常用函数	115](#_Toc421731929)

[13.2  自定义函数	115](#_Toc421731930)

[13.3  hive高级操作	115](#_Toc421731931)

[13.4  hive优化	115](#_Toc421731932)

[13.5  hive对数据倾斜的优化	115](#_Toc421731933)

[13.5.1 数据倾斜的原因	115](#_Toc421731934)

[13.5.2 数据倾斜的解决方案	116](#_Toc421731935)

[13.5.3 典型的业务场景	117](#_Toc421731936)

[13.5.4 总结	118](#_Toc421731937)

[14.  数据采集工具	119](#_Toc421731938)

[14.1 flume介绍	119](#_Toc421731939)

[15.  Storm基础	137](#_Toc421731940)

[15.1 storm介绍	137](#_Toc421731941)

[15.2 storm基本概念	137](#_Toc421731942)

[15.3 storm集群搭建	137](#_Toc421731943)

[15.4 storm示例编程	137](#_Toc421731944)

[15.5 kafka介绍与应用开发	137](#_Toc421731945)

[16.  Storm高级特性	137](#_Toc421731946)

[16.1 Storm与kafka整合	137](#_Toc421731947)

[16.2 Storm的tuple树	138](#_Toc421731948)

[16.3 storm事务topo（Trident）	138](#_Toc421731949)

[16.3.1 TridentTopology简介	138](#_Toc421731950)

[16.3.2  应用举例	138](#_Toc421731951)

[16.3.3 引言	139](#_Toc421731952)

[16.3.4  newStream	140](#_Toc421731953)

[16.3.5  each	141](#_Toc421731954)

[16.3.6  build	143](#_Toc421731955)

[16.3.7  grouping	143](#_Toc421731956)

[16.4 Storm Topology的ack机制	145](#_Toc421731957)

[16.5  TridentTopology调用关系	146](#_Toc421731958)

[16.6  seeder tuple的状态机	148](#_Toc421731959)

[16.4 stormRPC	149](#_Toc421731960)

[17. 机器学习	149](#_Toc421731961)

[17.1 机器学习概念介绍	149](#_Toc421731962)

[17.2 电商推荐--协同过滤算法	149](#_Toc421731963)

[17.3 预测算法--简单线性回归	149](#_Toc421731964)

[18.  Hadoop综合项目	150](#_Toc421731965)

[19.  Hadoop综合练习	150](#_Toc421731966)

[20.  Spark基础之scala语言	150](#_Toc421731967)

[21.  Spark基础	151](#_Toc421731968)

[21.1 spark框架介绍	151](#_Toc421731969)

[21.2 spark集群概念	153](#_Toc421731970)

[21.3 spark优势简介	153](#_Toc421731971)

[21.4 spark集群搭建	154](#_Toc421731972)

[21.5 spark编程基础	154](#_Toc421731973)

[21.5.1 spark-shell编程	154](#_Toc421731974)

[21.5.2 ide编程	155](#_Toc421731975)

[22.  Spark原理深入	157](#_Toc421731976)

[22.1 spark-RDD原理深度解析	157](#_Toc421731977)

[22.2 spark内核源码阅读	157](#_Toc421731978)

[22.2.1 akka介绍，demo示例）	157](#_Toc421731979)

[22.2.2 RDD类	158](#_Toc421731980)

[22.2.3 SparkContext类	158](#_Toc421731981)

[22.3 任务调度流程	165](#_Toc421731982)

[22.3.1 stage划分	165](#_Toc421731983)

[22.3.2 task提交	165](#_Toc421731984)

[22.3.3 DAGScheduler	165](#_Toc421731985)

[22.3.4 TaskScheduler	165](#_Toc421731986)

[23.  Spark-Streaming应用	166](#_Toc421731987)

[23.1 spark-Streaming概念	166](#_Toc421731988)

[23.2 spark-streaming原理	166](#_Toc421731989)

[23.3 streaming应用开发实例	166](#_Toc421731990)

[23.3.1 hdfs源	166](#_Toc421731991)

[23.3.2 flume源	167](#_Toc421731992)

[23.3.3 socket源	168](#_Toc421731993)

[23.3.4 window操作	168](#_Toc421731994)

[23.3.5 stateful window操作	169](#_Toc421731995)

[24.  Spark-SQL应用	170](#_Toc421731996)

[24.1 sparksql概念	170](#_Toc421731997)

[24.2 sparksql开发示例	171](#_Toc421731998)

[24.3 MLlib介绍	173](#_Toc421731999)

[25.  Spark综合练习	173](#_Toc421732000)

 



# **1.**  **HADOOP入门**

## **1.1 大数据技术介绍**

大数据技术生态体系：

Hadoop  元老级分布式海量数据存储、处理技术系统，擅长离线数据分析

Hbase  基于hadoop的分布式海量数据库，离线分析和在线业务通吃

Hive sql 基于hadoop的数据仓库工具，使用方便，功能丰富，使用方法类似SQL

Zookeeper 集群协调服务

Sqoop数据导入导出工具

Flume数据采集框架

Storm 实时流式计算框架，流式处理领域头牌框架

Spark 基于内存的分布式运算框架，一站式处理 all in one，新秀，发展势头迅猛

sparkCore

SparkSQL

SparkStreaming

机器学习：

Mahout  基于mapreduce的机器学习算法库

MLLIB  基于spark机器学习算法库

## **1.2 学习建议**

一、理解该框架的功能和适用场景

二、使用（安装部署，编程规范，API）

三、运行机制

四、结构原理

五、源码

## **1.3 就业前景及发展规划**

BAT ---- 看运气<更强调基本功——数据结构，算法，JVM>，其他，一切皆有可能

薪水----初级8K，高级——心有多大薪水就有多高

发展路线---- 

应用开发 -- 高级开发人员

平台开发 -- 架构级别

|

|-----------------|--------- ----  ---- -------------|

|		    |                       |

架构师	 数据挖掘模型设计		 管理

## **1.4  HADOOP简介** 

### **1.4.1  hadoop基本概念** 

（1）hadoop是用于处理（运算分析）海量数据的技术平台，且是采用分布式集群的方式；

 

（2）hadoop两个大的功能：

ü **提供海量数据的****存储****服务；**

ü **提供****分析海量数据****的编程框架及运行平台；**

 

（3）Hadoop有**3大核心组件：**

ü HDFS---- hadoop分布式文件系统海量数据的存储(集群服务)，

 

ü MapReduce----分布式运算框架（编程框架）（导jar包写程序），海量数据运算分析（替代品：storm /spark等 ）

 

ü Yarn ----资源调度管理集群(可以理解为一个分布式的操作系统，管理和分配集群硬件资源)

 

 

（4） 使用Hadoop：

ü 可以把hadoop理解为一个编程框架（类比：structs、spring、hibernate/mybatis），有着自己特定的API封装和用户编程规范，用户可借助这些API来实现数据处理逻辑；

ü 从另一个角度，hadoop又可以理解为一个提供服务的软件（类比：数据库服务oracle/mysql、索引服务solr，缓存服务redis等），用户程序通过客户端向hadoop集群请求服务来实现特定的功能；

 

 

（5）Hadoop产生的历史

最早来自于google的三大技术论文：GFS/MAPREDUCE/BIG TABLE

（为什么google会需要这么一种技术？）

后来经过doug cutting的“山寨”，出现了java版本的 hdfs   mapreduce 和 hbase

并成为apache的顶级项目  hadoop ，hbase

经过演化，hadoop的组件又多出一个yarn（mapreduce+ yarn + hdfs）

而且，hadoop外围产生了越来越多的工具组件，形成一个庞大的hadoop生态体系

 

 

 

 

### **1.4.2为什么需要hadoop**

在数据量很大的情况下，单机的处理能力无法胜任，必须采用分布式集群的方式进行处理，而用分布式集群的方式处理数据，实现的复杂度呈级数增加，所以，在海量数据处理的需求下，一个通用的分布式数据处理技术框架能大大降低应用开发难度和减少工作量

 

 

 

先来写一个普通的单机java程序

观察程序处理的速度和能力

 

 

 

 

 

 

 

 

 

 

 

## 1.5 hadoop集群部署安装

（学习目标：掌握开发测试级别的hadoop集群安装部署）

1、准备linux服务器（centos 6.4 32位/64位；生产环境的服务器应该采用64位，可以支持更大的内存）

 

A. 解压centos虚拟机镜像压缩包到某个目录，并用vmware打开

B. 准备操作系统环境（主机名，ip地址配成static，域名和ip的本地映射hosts）

C. 关闭图形界面的启动   修改/etc/inittab中的启动级别为3

D. 配置防火墙（关闭） àà  service iptables stop

E. 为hadoop安装使用准备一个专门的linux用户（初学者建议直接用root用户）

可选：为hadoop用户设置sudo权限   /etc/sudoers

（在我们的linux系统镜像中，有用户hadoop，密码：hadoop）

 

 

2、准备java环境，安装jdk，配置环境变量等

ü 解压安装包

ü 修改环境变量：  

JAVA_HOME   

PATH

3、安装hadoop----（解压，修改配置文件，分发到集群，初始化，启动）

Hadoop的目录结构：

bin       		 #可执行文件（hadoop的功能操作命令）etc				 #配置文件include    lib				 #本地库文件（数据压缩编解码、本地文件系统操作）libexec    LICENSE.txtNOTICE.txt README.txtsbin				#可执行文件（hadoop集群进程管理的操作命令）share			#开发所需要的jar包及用户帮助文档

 

4、修改配置文件（参考现成的配置文件xxx-site.xml）

(1)hadoop-env.sh   JAVA_HOME = /home/hadoop/app/jdk_7u65

(2)core-site.xml	   

fs.defaultFS    指定hadoop所使用的文件系统

hadoop.tmp.dir  指定各节点上的hadoop进程所在的本地工作目录(父目录)

(3) mapred-site.xml    mapreduce.framework.name :  yarn

(4)yarn-site.xml    yarn.resourcemanager.hostname: server01 (yarn中的master节点所在主机)

​                 yarn.nodemanager.aux-services :  mapreduce_shuffle

(5)可选：

如果要让namenode单独配置一个工作目录，在hdfs-site.xml ：

 <name>dfs.namenode.name.dir</name>

 <value> /mnt/driver-meta/,nfs://</value>

如果要让datanode单独配置一个工作目录，在hdfs-site.xml ：

 <name>dfs.datanode.data.dir</name>

 <value> /mnt/driver-data-a/,/mnt/driver-data-b/,/mnt/driver-data-c/</value>

如果要让secondary namenode 在指定的机器上启动，则配置：

<name>dfs.namenode.secondary.http-address</name>

<value>hadoop-server02:50090</value>

 

 

(6)真实生产中部署一个中、大型集群的方式：

有些公司会借助一些自动化的网络拷贝工具加快配置速度

有些公司会采用一些商业发行版（CDH--cloudera公司的产品；HORTONWORKS；MICROSOFT，IBM，EMC，INTEL）

 

5、启动hadoop

l 首先，格式化namenode     bin/hadoop namenode -format

l 手动启动各服务进程

在相应服务器上启动hdfs的相关进程 ：

  启动namenode进程—— sbin/hadoop-daemon.sh start namenode

启动datanode进程 ——sbin/hadoop-daemon.sh start datanode

然后，验证hdfs的服务是否能正常提供：

bin/hdfs dfsadmin -report  查看hdfs集群的统计信息

 

l Shell脚本批量启动方式：

在任意一台服务器上执行命令：

启动hdfs服务：sbin/start-dfs.sh

启动yarn服务：sbin/start-yarn.sh

或者：直接启动hdfs+yarn服务： sbin/start-all.sh

 

6、集群内部的SSH密钥认证登陆机制配置(免密登陆)

配置的机制：在登陆方生成密钥对，然后将公钥复制给目标主机，在目标主机上将这个公钥加入授权文件 ~/.ssh/authorized_keys   (该文件的权限: 600)

 

真实大量配置的时候直接使用ssh工具箱的工具：

1/在登陆方生成密钥对，执行命令： ssh-keygen

2/执行这条指令：

ssh-copy-id   hadoop-server03

就可以免密登陆目标主机

 

 

7、从一个节点的“伪分布式”hadoop集群扩展为多节点分布式集群

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

# **2. HDFS**

总的设计思想：

​	设计目标：提高分布式并发处理数据的效率（提高并发度和移动运算到数据）

分而治之：将大文件、大批量文件，分布式存放在大量独立的服务器上，以便于采取分而治之的方式对海量数据进行运算分析；

重点概念：文件切块，副本存放，元数据，位置查询，数据读写流

 

## **2.1  hdfs的shell操作**

hadoop  fs  -操作命令  -参数

-ls                  #显示目录信息

-->hadoop  fs  -ls  hdfs://hadoop-server-00:9000/

这些参数中，所有的hdfs路径都可以简写

-->hadoop fs -ls /   等同于上一条命令的效果

 

-copyFromLocal    #从本地文件系统中拷贝文件到hdfs路径去

-->hadoop  fs  -copyFromLocal  ./jdk.tar.gz  /aaa/

-copyToLocal      #从hdfs拷贝到本地

-->hadoop fs -copyToLocal /aaa/jdk.tar.gz

-put      #等同于copyFromLocal

-get       #等同于copyToLocal，就是从hdfs下载文件到本地

-getmerge   #合并下载多个文件

--> 比如hdfs的目录 /aaa/下有多个文件:log.1, log.2,log.3,...

hadoop fs -getmerge /aaa/log.* ./log.sum

 

-moveFromLocal     #从本地移动到hdfs

-moveToLocal       #从hdfs移动到本地

 

-cp     #从hdfs的一个路径拷贝hdfs的另一个路径

-->hadoop fs -cp /aaa/jdk.tar.gz /bbb/jdk.tar.gz.2

 

-mv    #在hdfs目录中移动文件

 

-mkdir    #在hdfs上创建目录

-->hadoop fs -mkdir -p /aaa/bbb/cc/dd

-rm       #删除文件或文件夹

--> hadoop fs -rm -r /aaa/bbb/

-rmdir      #删除空目录

-cat  ---显示文件内容  

-->hadoop fs -cat /hello.txt

--appendToFile  ----追加一个文件到已经存在的文件末尾

-->hadoop  fs  -appendToFile  ./hello.txt  hdfs://hadoop-server01:9000/hello.txt

可以简写为：

Hadoop  fs  -appendToFile  ./hello.txt  /hello.txt

-chgrp 

-chmod

-chown

上面三个跟linux中的用法一样

-->hadoop fs -chmod 666 /hello.txt

-count         #统计一个指定目录下的文件节点数量

-->hadoop fs -count /aaa/

-createSnapshot

-deleteSnapshot

-renameSnapshot

以上三个用来操作hdfs文件系统目录信息快照

-->hadoop fs -createSnapshot /

-df               #统计文件系统的可用空间信息

-du 

-->hadoop fs -df -h /

-->hadoop fs -du -s -h /aaa/*

-help             #输出这个命令参数手册

-setrep                #设置hdfs中文件的副本数量

-->hadoop fs -setrep 3 /aaa/jdk.tar.gz

-stat                  #显示一个文件或文件夹的元信息

-tail                  #显示一个文件的末尾

-text                  #以字符形式打印一个文件的内容



## **2.2  HDFS的一些concept（概念）和特性**

**首先，它是一个文件系统**，有一个统一的命名空间——目录树, 客户端访问hdfs文件时就是通过指定这个目录树中的路径来进行

 

**其次，它是分布式的**，由很多服务器联合起来实现功能；

ü hdfs文件系统会给客户端提供一个统一的抽象目录树， Hdfs中的文件都是分块（block）存储的，块的大小可以通过配置参数( dfs.blocksize)来规定，默认大小在hadoop2.x版本中是128M，老版本中是64M

ü 文件的各个block由谁来进行真实的存储呢？----分布在各个datanode服务节点上，而且每一个block都可以存储多个副本（副本数量也可以通过参数设置dfs.replication，默认值是3）

ü Hdfs中有一个重要的角色：namenode，负责维护整个hdfs文件系统的目录树，以及每一个路径（文件）所对应的block块信息（block的id，及所在的datanode服务器）

ü hdfs是设计成适应一次写入，多次读出的场景，并不支持文件的修改

(hdfs并不适合用来做网盘应用，因为，不便修改，延迟大，网络开销大，成本太高)

 

**特性：**

容量可以线性扩展

数据存储高可靠

分布式运算处理很方便

数据访问延迟较大，不支持数据的修改操作

适合一次写入多次读取的应用场景

 



## **2.3  HDFS的java操作**

（1）搭建开发环境（eclipse，hdfs的jar包----hadoop的安装目录的share下）

<dependency>    <groupId>org.apache.hadoop</groupId>   <artifactId>hadoop-client</artifactId>    <version>2.4.1</version></dependency> 

建议在linux下进行客户端应用的开发，不会存在兼容性问题。

如果非要在window上做客户端应用开发，需要设置以下环境：

A、在windows的某个目录下解压一个hadoop的安装包

B、将安装包下的lib和bin目录用对应windows版本平台编译的本地库替换

C、在window系统中配置HADOOP_HOME指向你解压的安装包

D、在windows系统的path变量中加入hadoop的bin目录

 

 

（2）在java中操作hdfs，首先要获得一个客户端实例

Configuration conf = new Configuration()FileSystem fs = FileSystem.get(conf)

 

而我们的操作目标是HDFS，所以获取到的fs对象应该是DistributedFileSystem的实例；

get方法是从何处判断具体实例化那种客户端类呢？

----从conf中的一个参数 fs.defaultFS的配置值判断；

如果我们的代码中没有指定并且工程classpath下也没有给定相应的配置，conf中的默认值就来自于hadoop的jar包中的core-default.xml，默认值为： [file:///](file://)

 

fs所具备的方法：

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps1.jpg) 

 

 

 

可以随机定位读取位置：DFSInputStream.seek()

 

 

 

 

 

 

 

## **2.4  hdfs的工作机制**

HDFS集群分为两大角色：NameNode、DataNode

NameNode负责管理整个文件系统的元数据

DataNode 负责管理用户的文件数据块

 

## **2.5  namenode工作机制**

namenode职责：

响应客户端请求

维护目录树

管理元数据（查询，修改）

---- hdfs元数据是怎么存储的？

A、内存中有一份完整的元数据（特定数据结构）

B、磁盘有一个“准完整”的元数据的镜像文件

C、当客户端对hdfs中的文件进行新增或者修改操作，首先会在edits文件中记录操作日志，当客户端操作成功后，相应的元数据会更新到内存中；

每隔一段时间，会由secondary namenode将namenode上积累的所有edits和一个最新的fsimage下载到本地，并加载到内存进行merge（这个过程称为checkpoint）

D、checkpoint操作的触发条件配置参数：

dfs.namenode.checkpoint.check.period=60  #检查触发条件是否满足的频率，60秒

dfs.namenode.checkpoint.dir=file://${hadoop.tmp.dir}/dfs/namesecondary#以上两个参数做checkpoint操作时，secondary namenode的本地工作目录

dfs.namenode.checkpoint.edits.dir=${dfs.namenode.checkpoint.dir} dfs.namenode.checkpoint.max-retries=3  #最大重试次数

dfs.namenode.checkpoint.period=3600  #两次checkpoint之间的时间间隔3600秒

dfs.namenode.checkpoint.txns=1000000 #两次checkpoint之间最大的操作记录

E、namenode和secondary namenode的工作目录存储结构完全相同，所以，当namenode故障退出需要重新恢复时，可以从secondary namenode的工作目录中将fsimage拷贝到namenode的工作目录，以恢复namenode的元数据

 

F、可以通过hdfs的一个工具来查看edits中的信息

bin/hdfs oev -i edits -o edits.xml

 

## **2.6  datanode的工作机制**

Datanode工作职责：

存储管理用户的文件块数据

定期向namenode汇报自身所持有的block信息（通过心跳信息上报）

上传一个文件，观察文件的block具体的物理存放情况

在每一台datanode机器上的这个目录：

/home/hadoop/app/hadoop-2.4.1/tmp/dfs/data/current/BP-193442119-192.168.2.120-1432457733977/current/finalized

 

 

 

## **2.7 一些补充**

\1. HDFS的其他访问方式：

HDFS文件系统可以通过标准的hdfs shell / rest api / java api来操作，还可以利用fuse这种工具将hdfs挂载为一个unix标准文件系统，就可以使用标准的linux文件操作方式来操作hdfs文件系统

HDFS还可以挂载为一个NFS系统

 

FileUtil工具类

FileUtil.*copy*(**new** File("c:/test.tar.gz"), FileSystem.*get*(URI.*create*("hdfs://hadoop-server01:9000"), conf, "hadoop"), **new** Path("/test.tar.gz"), **true**, conf);

 

\2. hdfs的trash配置

Hdfs存在回收站机制，进入回收站的文件可以保存一段时间，过期后再清除

参数配置：

fs.trash.checkpoint.interval=0     #回收站过期机制检查频率（分钟）fs.trash.interval=0     #回收站中文件过期的时间限制（分钟）

 

 

\3. 通配符及过滤器选择文件

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps2.jpg) 

 

 

 

\4. Namenode的安全模式

（1）当nameonde发现文件block丢失的数量达到一个配置的门限时，就会进入安全模式，它在这个模式下等待datanode向它汇报block信息。

（2）在安全模式下，namenode可以提供元数据查询的功能，但是不能修改；

可以手动管理namenode的安全模式：

hdfs dfsadmin -safemode  <enter | leave | get | wait]>

 

 

 

 

 

 

# **3. 深入hdfs源码**

## **3.1 hdfs 读数据流程**

1、跟namenode通信查询元数据，找到文件块所在的datanode服务器

2、挑选一台datanode（就近原则，然后随机）服务器，请求建立socket流

3、datanode开始发送数据（从磁盘里面读取数据放入流，以packet为单位来做校验）

4、客户端以packet为单位接收，现在本地缓存，然后写入目标文件

## **3.2 hdfs 写数据流程**

1、根namenode通信请求上传文件，namenode检查目标文件是否已存在，父目录是否存在

2、namenode返回是否可以上传

3、client请求第一个 block该传输到哪些datanode服务器上

4、namenode返回3个datanode服务器ABC

5、client请求3台dn中的一台A上传数据（本质上是一个RPC调用，建立pipeline），A收到请求会继续调用B，然后B调用C，将真个pipeline建立完成，逐级返回客户端

6、client开始往A上传第一个block（先从磁盘读取数据放到一个本地内存缓存），以packet为单位，A收到一个packet就会传给B，B传给C；A每传一个packet会放入一个应答队列等待应答

7、当一个block传输完成之后，client再次请求namenode上传第二个block的服务器。

 

## **3.3 hadoop的RPC框架**

Hadoop中各节点之间存在大量的远程过程调用，hadoop为此封装了一个RPC基础框架

使用方法：

(1)定义一个接口，实例如下：

//RCP通信的两端共同遵守的协议（本质上就是业务实现类的接口）public interface ClientNameNodeProtocal {	//RPC通信双方一致的版本号	public static final long versionID = 1L;	//业务方法签名	public String getMetaData(String path); }

 

(2)编写接口的业务实现类

/** * 业务的具体实现类，应该运行在远端服务器上 * @author duanhaitao@itcast.cn * */public class NamNodeNameSystemImpl implements ClientNameNodeProtocal { 	@Override	public String getMetaData(String path) {				//many logic code to find the meta data in meta data pool		return "{/aa/bb/bian4.mp4;300M;[BLK_1,BLK_2,BLK_3];3;{[BLK_1:DN-A,DN-B,DN-E],[BLK_2:DN-A,DN-B,DN-C],[BLK_3:DN-A,DN-D,DN-E]}}";	}}

(3)使用RPC框架API将业务实现发布为RPC服务

/** * RCP服务发布工具 * @author duanhaitao@itcast.cn * */public class PublishServiceTool {		public static void main(String[] args) throws HadoopIllegalArgumentException, IOException {				//创建一个RPC服务builder		Builder builder = new RPC.Builder(new Configuration());		//将要发布的服务的信息设置到builder中		builder.setBindAddress("spark01").setPort(10000).setProtocol(ClientNameNodeProtocal.class).setInstance(new NamNodeNameSystemImpl());				//用builder构建出一个socket服务		Server server = builder.build();		//将服务启动，就可以等待客户端请求		server.start();	}}

 

(4)客户端通过RPC框架API获取跟RPC服务端通信的socket代理，调用远端服务

public class Client {		public static void main(String[] args) throws Exception {				//首先用RPC框架获得要调用的远端服务的引用（动态代理对象）		ClientNameNodeProtocal namenodeImpl = RPC.getProxy(ClientNameNodeProtocal.class, 1L, new InetSocketAddress("spark01",10000), new Configuration());		//因为这个动态代理对象实现了业务类的接口，所以可以直接通过这个引用来调用业务类的实现方法(本质上，具体实现在远端，走的是socket通信请求)		String metaData = namenodeImpl.getMetaData("/aa/bb/bian4.mp4");				System.out.println(metaData);			}}

 

 

## **3.4 hdfs 读数据源码分析**

 

 

## **3.5 hdfs 写数据源码分析**

 

 

 

 

 

 

 

## **3.6 远程debug跟踪Hadoop服务端代码**

（1）需要在$HADOOP_HOME/etc/hadoop/hadoop-env.sh文件的最后添加你想debug的进程

#远程调试namenodeexport HADOOP_NAMENODE_OPTS="-agentlib:jdwp=transport=dt_socket,address=8888,server=y,suspend=y"#远程调试datanodeexport HADOOP_DATANODE_OPTS="-agentlib:jdwp=transport=dt_socket,address=9888,server=y,suspend=y"

 

 

（2）在本地的eclipse中打开NameNode或者DataNode类，点击右键，添加远程debug配置，如图：

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps3.jpg) 

 

（3）添加一个远程debug调试配置

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps4.jpg) 

 

 

（4）填写远程服务端的debug地址和端口号

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps5.jpg) 

 

 

（5）接着在namenode类中添加断点，如图：

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps6.jpg) 

 

（1）回到集群服务器上启动hdfs

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps7.jpg) 

 

（2）回到eclipse之前配置的远程debug配置上，点击debug开始调试

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps8.jpg) 

 

（8）成功进入断点

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps9.jpg) 

 

 

 

 

 

 

 

 

# **4. MAPREDUCE入门**

Mapreduce是一个分布式的运算编程框架，核心功能是将用户编写的核心逻辑代码分布式地运行在一个集群的很多服务器上；

学习要求：掌握MR程序编程规范；

​		   掌握MR程序运行机制

​		   掌握MR常见需求解决方式

 

 

## **4.1 为什么要MAPREDUCE**

（1）海量数据在单机上处理因为硬件资源限制，无法胜任，因为需要采用分布式集群的方式来处理。

（2）而一旦将单机版程序扩展到集群来分布式运行，将极大地增加程序的复杂度和开发难度

（3）引入mapreduce框架后，开发人员可以将绝大部分工作集中在业务逻辑的开发上，而将分布式计算中的复杂性交由框架来处理

 

## **4.2 MAPREDUCE程序运行演示**

Hadoop的发布包中内置了一个hadoop-mapreduce-example-2.4.1.jar，这个jar包中有各种MR示例程序，可以通过以下步骤运行：

启动hdfs，yarn

然后在集群中的任意一台服务器上执行，（比如运行wordcount）：

hadoop jar hadoop-mapreduce-example-2.4.1.jar wordcount  /wordcount/data /wordcount/out

## **4.3 MAPREDUCE 编程规范**

（1）用户程序会分成三个部分：Mapper，Reducer，Driver

（2）Mapper的输入数据是KV对的形式，KV的类型可以设置

（3）Mapper的输出数据是KV对的形式，KV的类型可以设置

（4）Mapper中的业务逻辑写在map方法中

（5）map方法是每进来一个KV对调用一次

（6）Reducer的输入数据应该对应Mapper的输出数据，也是KV

（7）Reducer的业务逻辑写在reduce方法中

（8）reduce方法是对每一个<key,valueList>调用一次

（9）用户的Mapper和Reducer都要继承各自的父类

（10）整个程序需要一个Drvier来进行提交，提交的是一个描述了各种必要信息的job对象

## **4.4 wordcount示例编写**

(1)定义一个mapper类

//首先要定义四个泛型的类型//keyin:  LongWritable    valuein: Text//keyout: Text            valueout:IntWritable public class WordCountMapper extends Mapper<LongWritable, Text, Text, IntWritable>{	//map方法的生命周期：  框架每传一行数据就被调用一次	//key :  这一行的起始点在文件中的偏移量	//value: 这一行的内容	@Override	protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {		//拿到一行数据转换为string		String line = value.toString();		//将这一行切分出各个单词		String[] words = line.split(" ");		//遍历数组，输出<单词，1>		for(String word:words){			context.write(new Text(word), new IntWritable(1));		}	}}

 

(2)定义一个reducer类

​	//生命周期：框架每传递进来一个kv 组，reduce方法被调用一次	@Override	protected void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException { 		//定义一个计数器		int count = 0;		//遍历这一组kv的所有v，累加到count中		for(IntWritable value:values){			count += value.get();		}		context.write(key, new IntWritable(count));	}}

 

 

(3)定义一个主类，用来描述job并提交job

public class WordCountRunner {	//把业务逻辑相关的信息（哪个是mapper，哪个是reducer，要处理的数据在哪里，输出的结果放哪里。。。。。。）描述成一个job对象	//把这个描述好的job提交给集群去运行	public static void main(String[] args) throws Exception {		Configuration conf = new Configuration();		Job wcjob = Job.getInstance(conf);		//指定我这个job所在的jar包//		wcjob.setJar("/home/hadoop/wordcount.jar");		wcjob.setJarByClass(WordCountRunner.class);				wcjob.setMapperClass(WordCountMapper.class);		wcjob.setReducerClass(WordCountReducer.class);		//设置我们的业务逻辑Mapper类的输出key和value的数据类型		wcjob.setMapOutputKeyClass(Text.class);		wcjob.setMapOutputValueClass(IntWritable.class);		//设置我们的业务逻辑Reducer类的输出key和value的数据类型		wcjob.setOutputKeyClass(Text.class);		wcjob.setOutputValueClass(IntWritable.class);				//指定要处理的数据所在的位置		FileInputFormat.setInputPaths(wcjob, "hdfs://hdp-server01:9000/wordcount/data/big.txt");		//指定处理完成之后的结果所保存的位置		FileOutputFormat.setOutputPath(wcjob, new Path("hdfs://hdp-server01:9000/wordcount/output/"));				//向yarn集群提交这个job		boolean res = wcjob.waitForCompletion(true);		System.exit(res?0:1);	}

  

 

## **4.5 MAPREDUCE程序提交运行模式及debug方法**

### **4.5.1 本地运行模式**

（1）mapreduce程序是被提交给LocalJobRunner在本地运行

（2）而处理的数据及输出结果可以在本地文件系统，也可以在hdfs上

（3）怎样实现本地运行？：写一个程序，不要带集群的配置文件（本质是你的mr程序的conf中是否有mapreduce.framework.name=local以及yarn.resourcemanager.hostname参数）

 

### **4.5.2 集群运行模式**

（1）mapreduce程序会提交给yarn集群的resourcemanager，分发到很多的节点上并发执行

（2）处理的数据和输出结果应该位于hdfs文件系统

（3）怎样实现集群运行：

A、将程序打成JAR包，然后在集群的任意一个节点上用hadoop命令启动

$ hadoop jar wordcount.jar cn.itcast.bigdata.mrsimple.WordCountDriver inputpath outputpath

B、直接在linux的eclipse中运行main方法

**（项目中要带参数：mapreduce.framework.name=yarn以及yarn的两个基本配置）**

C、如果要在windows的eclipse中提交job给集群，则要修改YarnRunner类

## **4.6 MAPREDUCE中的Combiner**

（1）combiner是MR程序中Mapper和Reducer之外的一种组件

（2）combiner组件的父类就是Reducer

（3）Combiner和reducer的区别在于运行的位置：

Combiner是在每一个maptask所在的节点运行

Reducer是接收全局所有Mapper的输出结果；

 

 

## **4.7 MAPREDUCE中的序列化**

（1）Java的序列化是一个重量级序列化框架（Serializable），一个对象被序列化后，会附带很多额外的信息（各种校验信息，header，继承体系。。。。），所以很臃肿，不便于在网络中高效传输；

所以，hadoop自己开发了一套序列化机制（Writable），精简，高效

（3）简单代码验证两种序列化机制的差别：

public class TestSeri {	public static void main(String[] args) throws Exception {		//定义两个ByteArrayOutputStream，用来接收不同序列化机制的序列化结果		ByteArrayOutputStream ba = new ByteArrayOutputStream();		ByteArrayOutputStream ba2 = new ByteArrayOutputStream(); 		//定义两个DataOutputStream，用于将普通对象进行jdk标准序列化		DataOutputStream dout = new DataOutputStream(ba);		DataOutputStream dout2 = new DataOutputStream(ba2);		ObjectOutputStream obout = new ObjectOutputStream(dout2);		//定义两个bean，作为序列化的源对象		ItemBeanSer itemBeanSer = new ItemBeanSer(1000L, 89.9f);		ItemBean itemBean = new ItemBean(1000L, 89.9f); 		//用于比较String类型和Text类型的序列化差别		Text atext = new Text("a");		// atext.write(dout);		itemBean.write(dout); 		byte[] byteArray = ba.toByteArray(); 		//比较序列化结果		System.out.println(byteArray.length);		for (byte b : byteArray) { 			System.out.print(b);			System.out.print(":");		} 		System.out.println("-----------------------"); 		String astr = "a";		// dout2.writeUTF(astr);		obout.writeObject(itemBeanSer); 		byte[] byteArray2 = ba2.toByteArray();		System.out.println(byteArray2.length);		for (byte b : byteArray2) {			System.out.print(b);			System.out.print(":");		}	}}

 

 

## **4.8 Mapreduce的排序初步**

MR程序在处理数据的过程中会对数据排序，排序的依据是mapper输出的key

 

 

 

# **5. Mapreduce高级特性（一）**

## **5.1 Partitioner编程**

Partition就是对map输出的key进行分组，不同的组可以指定不同的reduce task处理；

Partition功能由partitioner的实现子类来实现

示例：不同省份流量数据汇总到不同文件中

 

## **5.2 Mapreduce的排序----重点**

MR中的常见排序机制：partial/total/secondary排序

MR中排序的基本要素：

排序是在map阶段输出之后，reduce处理之前

（通过无reduce的MR程序示例观察）

只针对key进行排序

Key要实现WritableComparable接口

简单示例：对流量汇总数据进行倒序排序

 

### **5.2.1 partital排序示例，多reduce task 自动实现各输出文件有序**

### **5.2.3 total排序机制**

（1）设置一个reduce task ，全局有序，但是并发度太低，单节点负载太大

（2）设置分区段partitioner，设置相应数量的reduce task，可以实现全局有序，但难以避免数据分布不均匀——数据倾斜问题，有些reduce task负载过大，而有些则过小；

（3）可以通过编写一个job来统计数据分布规律，获取合适的区段划分，然后用分区段partitioner来实现排序；但是这样需要另外编写一个job对整个数据集运算，比较费事

（4）利用hadoop自带的取样器，来对数据集取样并划分区段，然后利用hadoop自带的TotalOrderPartitioner分区来实现全局排序

 

示例：

/** * 全排序示例 * @author duanhaitao@itcast.cn * */public class TotalSort { 	static class TotalSortMapper extends Mapper<Text, Text, Text, Text> {		OrderBean bean = new OrderBean(); 		@Override		protected void map(Text key, Text value, Context context) throws IOException, InterruptedException { 			// String line = value.toString();			// String[] fields = line.split("\t");			// bean.set(fields[0], Double.parseDouble(fields[1]));			context.write(key, value);		}	} 	static class TotalSortReducer extends Reducer<Text, Text, Text, Text> { 		@Override		protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException { 			for (Text v : values) {				context.write(key, v);			}		}	} 	public static void main(String[] args) throws Exception { 		Configuration conf = new Configuration();		Job job = Job.getInstance(conf); 		job.setJarByClass(TotalSort.class); 		job.setMapperClass(TotalSortMapper.class);		job.setReducerClass(TotalSortReducer.class);//		job.setOutputKeyClass(OrderBean.class);//		job.setOutputValueClass(NullWritable.class); 		//用来读取sequence源文件的输入组件		job.setInputFormatClass(SequenceFileInputFormat.class);				FileInputFormat.setInputPaths(job, new Path(args[0]));		FileOutputFormat.setOutputPath(job, new Path(args[1])); //		job.setPartitionerClass(RangePartitioner.class);				//分区的逻辑使用的hadoop自带的全局排序分区组件		job.setPartitionerClass(TotalOrderPartitioner.class);				//系统自带的这个抽样器只能针对sequencefile抽样		RandomSampler randomSampler = new InputSampler.RandomSampler<Text,Text>(0.1,100,10);		InputSampler.writePartitionFile(job, randomSampler);				//获取抽样器所产生的分区规划描述文件		Configuration conf2 = job.getConfiguration();		String partitionFile = TotalOrderPartitioner.getPartitionFile(conf2);				//把分区描述规划文件分发到每一个task节点的本地		job.addCacheFile(new URI(partitionFile)); 		//设置若干并发的reduce task		job.setNumReduceTasks(3); 		job.waitForCompletion(true);	}}

 

### **5.2.4 secondary排序机制**

----就是让mapreduce帮我们根据value排序

 

 

考虑一个场景，需要取按key分组的最大value条目：

通常，shuffle只是对key进行排序

如果需要对value排序，则需要将value放到key中，但是此时，value就和原来的key形成了一个组合key，从而到达reducer时，组合key是一个一个到达reducer，想在reducer中输出最大value的那一个，不好办，它会一个一个都输出去，除非自己弄一个缓存，将到达的组合key全部缓存起来然后只取第一个

（或者弄一个访问标识？但是同一个reducer可能会收到多个key的组合key，无法判断访问标识）

此时就可以用到secondary sort，其思路：

（1）要有对组合key排序的比较器

（2）要有partitioner进行分区负载并行reducer计算

（3）要有一个groupingcomparator来重定义valuelist聚合策略——这是关键，其原理就是将相同key而不同组合key的数据进行聚合，从而把他们聚合成一组，然后在reducer中可以一次收到这一组key的组合key，并且，value最大的也就是在这一组中的第一个组合key会被选为迭代器valuelist的key，从而可以直接输出这个组合key，就实现了我们的需求

 

示例：输出每个item的订单金额最大的记录

（1）定义一个GroupingComparator

/** * 用于控制shuffle过程中reduce端对kv对的聚合逻辑 * @author duanhaitao@itcast.cn * */public class ItemidGroupingComparator extends WritableComparator { 	protected ItemidGroupingComparator() { 		super(OrderBean.class, true);	}	 	@Override	public int compare(WritableComparable a, WritableComparable b) {		OrderBean abean = (OrderBean) a;		OrderBean bbean = (OrderBean) b;				//将item_id相同的bean都视为相同，从而聚合为一组		return abean.getItemid().compareTo(bbean.getItemid());	}}

 

（2）定义订单信息bean

/** * 订单信息bean，实现hadoop的序列化机制 * @author duanhaitao@itcast.cn * */public class OrderBean implements WritableComparable<OrderBean>{	private Text itemid;	private DoubleWritable amount; 	public OrderBean() {	}	public OrderBean(Text itemid, DoubleWritable amount) {		set(itemid, amount);	} 	public void set(Text itemid, DoubleWritable amount) { 		this.itemid = itemid;		this.amount = amount; 	} 	public Text getItemid() {		return itemid;	} 	public DoubleWritable getAmount() {		return amount;	} 	@Override	public int compareTo(OrderBean o) {		int cmp = this.itemid.compareTo(o.getItemid());		if (cmp == 0) { 			cmp = -this.amount.compareTo(o.getAmount());		}		return cmp;	} 	@Override	public void write(DataOutput out) throws IOException {		out.writeUTF(itemid.toString());		out.writeDouble(amount.get());			} 	@Override	public void readFields(DataInput in) throws IOException {		String readUTF = in.readUTF();		double readDouble = in.readDouble();				this.itemid = new Text(readUTF);		this.amount= new DoubleWritable(readDouble);	}  	@Override	public String toString() {		return itemid.toString() + "\t" + amount.get();	}}

 

 

（3）自定义一个partitioner，以使相同id的bean发往相同reduce task

public class ItemIdPartitioner extends Partitioner<OrderBean, NullWritable>{ 	@Override	public int getPartition(OrderBean key, NullWritable value, int numPartitions) {		//指定item_id相同的bean发往相同的reducer task		return (key.getItemid().hashCode() & Integer.MAX_VALUE) % numPartitions;	}}

 

 

（4）定义mr主体流程

/** * 利用secondarysort机制输出每种item订单金额最大的记录 * @author duanhaitao@itcast.cn * */public class SecondarySort {		static class SecondarySortMapper extends Mapper<LongWritable, Text, OrderBean, NullWritable>{				OrderBean bean = new OrderBean();				@Override		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException { 			String line = value.toString();			String[] fields = StringUtils.split(line, "\t");						bean.set(new Text(fields[0]), new DoubleWritable(Double.parseDouble(fields[1])));						context.write(bean, NullWritable.get());					}			}		static class SecondarySortReducer extends Reducer<OrderBean, NullWritable, OrderBean, NullWritable>{						//在设置了groupingcomparator以后，这里收到的kv数据 就是：  <1001 87.6>,null  <1001 76.5>,null  .... 		//此时，reduce方法中的参数key就是上述kv组中的第一个kv的key：<1001 87.6>		//要输出同一个item的所有订单中最大金额的那一个，就只要输出这个key		@Override		protected void reduce(OrderBean key, Iterable<NullWritable> values, Context context) throws IOException, InterruptedException {			context.write(key, NullWritable.get());		}	}			public static void main(String[] args) throws Exception {				Configuration conf = new Configuration();		Job job = Job.getInstance(conf);				job.setJarByClass(SecondarySort.class);				job.setMapperClass(SecondarySortMapper.class);		job.setReducerClass(SecondarySortReducer.class);						job.setOutputKeyClass(OrderBean.class);		job.setOutputValueClass(NullWritable.class);				FileInputFormat.setInputPaths(job, new Path(args[0]));		FileOutputFormat.setOutputPath(job, new Path(args[1]));		//指定shuffle所使用的GroupingComparator类		job.setGroupingComparatorClass(ItemidGroupingComparator.class);		//指定shuffle所使用的partitioner类		job.setPartitionerClass(ItemIdPartitioner.class);				job.setNumReduceTasks(3);				job.waitForCompletion(true);			} }

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

### **5.3 shuffle详解**

Shuffle缓存流程：

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps10.jpg) 

----shuffle是MR处理流程中的一个过程，它的每一个处理步骤是分散在各个map task和reduce task节点上完成的，整体来看，分为3个操作：

1、分区partition

2、Sort根据key排序

3、Combiner进行局部value的合并

 

整个shuffle的大流程如下：

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps11.jpg) 

ü map task输出结果到一个内存缓存，并溢出为磁盘文件

ü combiner调用

ü 分区/排序

ü reduce task 拉取map输出文件中对应的分区数据

ü reduce端归并排序

产生聚合values迭代器来传递给reduce方法，并把这组聚合kv（**聚合的依据是GroupingComparator）**中排序最前的kv的key传给reduce方法的入参 key

 

### **5.4 mr程序map任务数的规划机制**

一个inputsplit对应一个map

而inputsplit切片规划是由InputFormat的具体实现子类来实现，就是调用

InputSplits[ ]  getSplits() 方法，这个方法的逻辑可以自定义

在默认情况下，由FileInputFormat来实现，它的核心逻辑：

（1） 规划切片的大小

   long minSize = Math.max(getFormatMinSplitSize(), getMinSplitSize(job));    long maxSize = getMaxSplitSize(job);    public static long getMaxSplitSize(JobContext context) {returncontext.getConfiguration().getLong(SPLIT_MAXSIZE, Long.MAX_VALUE);      } // mapreduce.input.fileinputformat.split.minsize  配置这个值可以让切片大小>块大小  // mapreduce.input.fileinputformat.split.maxsize 配置这个值可以让切片大小<块大小 long splitSize = computeSplitSize(blockSize, minSize, maxSize);//计算切片大小protected long computeSplitSize(long blockSize, long minSize,long maxSize) {    return Math.max(minSize, Math.min(maxSize, blockSize));}

 

(2)构造切片信息对象，并放入InputSplits[ ]中

splits.add(makeSplit(path,length-bytesRemaining,splitSize,blkLocations[blkIndex].getHosts()));

注：FileInputFormat的切片机制是针对一个一个的文件进行，因此，如果文件太小，则整个文件划分为一个切片

如果一个大文件被切成若干个切片后，剩下的长度如果在blocksize的1.1倍大小以内，则将剩下的长度全部规划为一个切片

 

 

### **5.5 Mapreduce的join算法**

（1）Reduce side join

示例：

订单数据

商品信息

 

实现机制：

通过将关联的条件作为map输出的key，将两表满足join条件的数据并携带数据所来源的文件信息，发往同一个reduce task，在reduce中进行数据的串联

 

 

public class OrderJoin { 	static class OrderJoinMapper extends Mapper<LongWritable, Text, Text, OrderJoinBean> { 		@Override		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException { 			// 拿到一行数据，并且要分辨出这行数据所属的文件			String line = value.toString(); 			String[] fields = line.split("\t"); 			// 拿到itemid			String itemid = fields[0]; 			// 获取到这一行所在的文件名（通过inpusplit）			String name = "你拿到的文件名"; 			// 根据文件名，切分出各字段（如果是a，切分出两个字段，如果是b，切分出3个字段） 			OrderJoinBean bean = new OrderJoinBean();			bean.set(null, null, null, null, null);			context.write(new Text(itemid), bean); 		} 	} 	static class OrderJoinReducer extends Reducer<Text, OrderJoinBean, OrderJoinBean, NullWritable> { 		@Override		protected void reduce(Text key, Iterable<OrderJoinBean> beans, Context context) throws IOException, InterruptedException {						 //拿到的key是某一个itemid,比如1000			//拿到的beans是来自于两类文件的bean			//  {1000,amount} {1000,amount} {1000,amount}   ---   {1000,price,name}						//将来自于b文件的bean里面的字段，跟来自于a的所有bean进行字段拼接并输出		}	}}

 

缺点：reduce端的处理压力太大，map节点的运算负载则很低，资源利用率不高

  容易产生数据倾斜

 

注：也可利用二次排序的逻辑来实现reduce端join

 

（2）Map side join

--原理阐述

适用于关联表中有小表的情形；

可以将小表分发到所有的map节点，这样，map节点就可以在本地对自己所读到的大表数据进行join并输出最终结果

可以大大提高join操作的并发度，加快处理速度

 

--示例：先在mapper类中预先定义好小表，进行join

--引入实际场景中的解决方案：一次加载数据库或者用distributedcache

public class TestDistributedCache {	static class TestDistributedCacheMapper extends Mapper<LongWritable, Text, Text, Text>{		FileReader in = null;		BufferedReader reader = null;		HashMap<String,String> b_tab = new HashMap<String, String>();		String localpath =null;		String uirpath = null;				//是在map任务初始化的时候调用一次		@Override		protected void setup(Context context) throws IOException, InterruptedException {			//通过这几句代码可以获取到cache file的本地绝对路径，测试验证用			Path[] files = context.getLocalCacheFiles();			localpath = files[0].toString();			URI[] cacheFiles = context.getCacheFiles();									//缓存文件的用法——直接用本地IO来读取			//这里读的数据是map task所在机器本地工作目录中的一个小文件			in = new FileReader("b.txt");			reader =new BufferedReader(in);			String line =null;			while(null!=(line=reader.readLine())){								String[] fields = line.split(",");				b_tab.put(fields[0],fields[1]);							}			IOUtils.closeStream(reader);			IOUtils.closeStream(in);					}				@Override		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException { 			//这里读的是这个map task所负责的那一个切片数据（在hdfs上）			 String[] fields = value.toString().split("\t");			 			 String a_itemid = fields[0];			 String a_amount = fields[1];			 			 String b_name = b_tab.get(a_itemid);			 			 // 输出结果  1001	98.9	banan			 context.write(new Text(a_itemid), new Text(a_amount + "\t" + ":" + localpath + "\t" +b_name ));			 		}					}			public static void main(String[] args) throws Exception {				Configuration conf = new Configuration();		Job job = Job.getInstance(conf);				job.setJarByClass(TestDistributedCache.class);				job.setMapperClass(TestDistributedCacheMapper.class);				job.setOutputKeyClass(Text.class);		job.setOutputValueClass(LongWritable.class);				//这里是我们正常的需要处理的数据所在路径		FileInputFormat.setInputPaths(job, new Path(args[0]));		FileOutputFormat.setOutputPath(job, new Path(args[1]));				//不需要reducer		job.setNumReduceTasks(0);		//分发一个文件到task进程的工作目录		job.addCacheFile(new URI("hdfs://hadoop-server01:9000/cachefile/b.txt"));				//分发一个归档文件到task进程的工作目录//		job.addArchiveToClassPath(archive); 		//分发jar包到task节点的classpath下//		job.addFileToClassPath(jarfile);				job.waitForCompletion(true);	}}

 

### **5.6 mapreduce的Distributed cache**

应用场景：map side join

工作原理：

通过mapreduce框架将一个文件（本地/HDFS）分发到每一个运行时的task(map task /reduce task)节点上（放到task进程所在的工作目录）

获取的方式： 在我们自己的mapper或者reducer的代码内，直接使用本地文件JAVA ----API 来访问这个文件

 

示例程序：

首先在 job对象中进行指定：  

job.addCacheFile(**new** URI("hdfs://hadoop-server01:9000/cachefile/b.txt"));//分发一个文件到task进程的工作目录job.addCacheFile(new URI("hdfs://hadoop-server01:9000/cachefile/b.txt"));//分发一个归档文件到task进程的工作目录//job.addArchiveToClassPath(archive);//分发jar包到task节点的classpath下//job.addFileToClassPath(jarfile);

 

然后在mapper或者reducer中直接使用：

in = new FileReader("b.txt");reader =new BufferedReader(in);String line = reader.readLine()

 

 

动手练习

 

 

 

 

# **6. Mapreduce高级特性（二）**

## **6.1  Mapreduce程序运行并发度**

### **6.1.1 reduce task数量的决定机制**

1、业务逻辑需要

2、数据量大小

设置方法：

job.setNumReduceTasks(5)

### **6.1.1  map task数量的决定机制：**

由于map task之间没有协作关系，每一个map task都是各自为政，在map task的处理中没法做“全局”性的聚合操作，所以map task的数量完全取决于所处理的数据量的大小

 

决定机制：

对待处理数据进行“切片”

每一个切片分配一个map task来处理

 

Mapreduce框架中默认的切片机制：

TextInputFormat.getSplits()继承自FileInputFormat.getSplits()

 

1：定义一个切片大小：可以通过参数来调节，默认情况下等于“hdfs中设置的blocksize”,通常是128M

2：获取输入数据目录下所有待处理文件List

3：遍历文件List，逐个逐个文件进行切片

​	for(file:List)

​	   对file从0偏移量开始切，每到128M就构成一个切片，比如a.txt（200M），就会被切成两个切片：   a.txt: 0-128M,  a.txt :128M-256M

​        再比如b.txt（80M），就会切成一个切片， b.txt :0-80M

 

Ø 如果要处理的数据是大量的小文件，使用上述这种默认切片机制，就会导致大量的切片，从而maptask进程数特别多，但是每一个切片又非常小，每个maptask的处理数据量就很小，从而，整体的效率会很低。

通用解决方案：就是将多个小文件划分成一个切片；实现办法就是自定义一个Inputformat子类重写里面的getSplits方法；

Mapreduce框架中自带了一个用于此场景的Inputformat实现类：CombineFileInputformat

 

 

 

 

 

 

 

 

 

数据切片与map任务数的机制

示例观察（多文件，大文件）

源码跟踪

TextInputFormat源码阅读

isSplitable() 判断要处理的数据是否可以做切片

getSplit()  规划切片信息(实现在FileInputFormat类中)

----TextInputformat切片逻辑： 对每一个文件单独切片；切片大小默认等于blocksize

但是有两个参数可以调整：

 

 

 

 

 

如果是大量小文件，这种切片逻辑会有重大弊端：切片数量太多,maptask太多

 



createRecordReader()  构造一个记录读取器

 

具体读取数据的逻辑是实现在LineRecordReader中 （按行读取数据，行起始偏移量作为key，行的内容作为value），比较特别的地方是：

LineRecordReader在读取一个具体的切片时，总是忽略掉第一行（针对的是：非第一切片），总是跨split多读一行(针对的是：非最末切片)

### **6.1.2 InputFormat的继承体系**

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps12.png) 

 

InputFormat子类介绍：

（1）TextInputFormat(默认的输入格式类)详解

-- 源码结构 getsplits()  reader

-- 为何不会出现一行被割断处理的原理

ü 在LineRecordReader中，对split的第一行忽略

  public void initialize(InputSplit genericSplit,                         TaskAttemptContext context) throws IOException {    FileSplit split = (FileSplit) genericSplit;    Configuration job = context.getConfiguration();		… ………..     // open the file and seek to the start of the split    final FileSystem fs = file.getFileSystem(job);    fileIn = fs.open(file);        CompressionCodec codec = new CompressionCodecFactory(job).getCodec(file);    if (null!=codec) {    … … … … //我们总是将第一条记录抛弃（文件第一个split除外）//因为我们总是在nextKeyValue ()方法中跨split多读了一行（文件最后一个split除外）    if (start != 0) {      start += in.readLine(new Text(), 0, maxBytesToConsume(start));    }    this.pos = start;  }

 

 

ü 在LineRecordReader中，nextKeyValue ()方法总是跨split多读一行

public boolean nextKeyValue() throws IOException {    if (key == null) {      key = new LongWritable();    }    key.set(pos);    if (value == null) {      value = new Text();    }    int newSize = 0;    // 使用<=来多读取一行    while (getFilePosition() <= end || in.needAdditionalRecordAfterSplit()) {      newSize = in.readLine(value, maxLineLength,          Math.max(maxBytesToConsume(pos), maxLineLength));      pos += newSize;      if (newSize < maxLineLength) {        break;	…. ….   }

 

 

（2） CombineTextInputFormat  

它的切片逻辑跟TextInputformat完全不同：

CombineTextInputFormat可以将多个小文件划为一个切片

这种机制在处理海量小文件的场景下能提高效率

(小文件处理的机制，最优的是将小文件先合并再处理)

思路

CombineFileInputFormat涉及到三个重要的属性：

mapred.max.split.size：同一节点或同一机架的数据块形成切片时，切片大小的最大值；

mapred.min.split.size.per.node：同一节点的数据块形成切片时，切片大小的最小值；

mapred.min.split.size.per.rack：同一机架的数据块形成切片时，切片大小的最小值。

切片形成过程：

（1）逐个节点（数据块）形成切片；

a.遍历并累加这个节点上的数据块，如果累加数据块大小大于或等于mapred.max.split.size，则将这些数据块形成一个切片，继承该过程，直到剩余数据块累加大小小于mapred.max.split.size，则进行下一步；

b.如果剩余数据块累加大小大于或等于mapred.min.split.size.per.node，则将这些剩余数据块形成一个切片，如果剩余数据块累加大小小于mapred.min.split.size.per.node，则这些数据块留待后续处理。

（2）逐个机架（数据块）形成切片；

a.遍历并累加这个机架上的数据块（这些数据块即为上一步遗留下来的数据块），如果累加数据块大小大于或等于mapred.max.split.size，则将这些数据块形成一个切片，继承该过程，直到剩余数据块累加大小小于mapred.max.split.size，则进行下一步；

b.如果剩余数据块累加大小大于或等于mapred.min.split.size.per.rack，则将这些剩余数据块形成一个切片，如果剩余数据块累加大小小于mapred.min.split.size.per.rack，则这些数据块留待后续处理。

（3）遍历并累加剩余数据块，如果数据块大小大于或等于mapred.max.split.size，则将这些数据块形成一个切片，继承该过程，直到剩余数据块累加大小小于mapred.max.split.size，则进行下一步；

（4）剩余数据块形成一个切片。

核心实现

// mapping from a rack name to the list of blocks it hasHashMap<String,List<OneBlockInfo>> rackToBlocks = new HashMap<String,List<OneBlockInfo>>();// mapping from a block to the nodes on which it has replicasHashMap<OneBlockInfo,String[]> blockToNodes = new HashMap<OneBlockInfo,String[]>();// mapping from a node to the list of blocks that it containsHashMap<String,List<OneBlockInfo>> nodeToBlocks = new HashMap<String,List<OneBlockInfo>>(); 

 

开始形成切片之前，需要初始化三个重要的映射关系：

rackToBlocks：机架和数据块的对应关系，即某一个机架上有哪些数据块；

blockToNodes：数据块与节点的对应关系，即一块数据块的“拷贝”位于哪些节点；

nodeToBlocks：节点和数据块的对应关系，即某一个节点上有哪些数据块；

初始化过程如下代码所示，其中每一个Path代表的文件被形成一个OneFileInfo对象，映射关系也在形成OneFileInfo的过程中被维护。

// populate all the blocks for all fileslong totLength = 0;for (int i = 0; i < paths.length; i++) {  files[i] = new OneFileInfo(paths[i], job,                              rackToBlocks, blockToNodes, nodeToBlocks, rackToNodes);  totLength += files[i].getLength();}

 

（1） 逐个节点（数据块）形成切片，代码如下：

// 保存当前切片所包含的数据块    ArrayList<OneBlockInfo> validBlocks = new ArrayList<OneBlockInfo>();    // 保存当前切片中的数据块属于哪些节点    ArrayList<String> nodes = new ArrayList<String>();    // 保存当前切片的大小long curSplitSize = 0;     // process all nodes and create splits that arelocalto a node.     // 依次处理每个节点上的数据块for (Iterator<Map.Entry<String, List<OneBlockInfo>>> iter = nodeToBlocks.entrySet().iterator(); iter.hasNext();) {      Map.Entry<String, List<OneBlockInfo>> one = iter.next();      nodes.add(one.getKey());      List<OneBlockInfo> blocksInNode = one.getValue();       // for each block, copy it into validBlocks. Delete it from blockToNodes so that the same block does not appear in// two different splits.      // 依次处理每个数据块，注意blockToNodes变量的作用，它保证了同一数据块不会出现在两个切片中for (OneBlockInfo oneblock : blocksInNode) {        if (blockToNodes.containsKey(oneblock)) {          validBlocks.add(oneblock);          blockToNodes.remove(oneblock);          curSplitSize += oneblock.length;// if the accumulated split size exceeds the maximum, then create this split.          // 如果数据块累积大小大于或等于maxSize，则形成一个切片if (maxSize != 0 && curSplitSize >= maxSize) {            //create an input split andadd it to the splits array            addCreatedSplit(job, splits, nodes, validBlocks);            curSplitSize = 0;            validBlocks.clear();          }        }      }      // if there were any blocks left over and their combined size is      // larger than minSplitNode, then combine them into one split.      // Otherwise add them back to the unprocessed pool. It is likely       // that they will be combined with other blocks from the same rack later on.      // 如果剩余数据块大小大于或等于minSizeNode，则将这些数据块构成一个切片；      // 如果剩余数据块大小小于minSizeNode，则将这些数据块归还给blockToNodes，交由后期“同一机架”过程处理if (minSizeNode != 0 && curSplitSize >= minSizeNode) {        //create an input split andadd it to the splits array        addCreatedSplit(job, splits, nodes, validBlocks);      } else {        for (OneBlockInfo oneblock : validBlocks) {          blockToNodes.put(oneblock, oneblock.hosts);        }      }      validBlocks.clear();      nodes.clear();      curSplitSize = 0;    }

 

 

（2）逐个机架（数据块）形成切片，代码如下：

// if blocks in a rack are below the specified minimum size, then keep them    // in 'overflow'. After the processing of all racks is complete, these overflow    // blocks will be combined into splits.    // overflowBlocks用于保存“同一机架”过程处理之后剩余的数据块    ArrayList<OneBlockInfo> overflowBlocks = new ArrayList<OneBlockInfo>();    ArrayList<String> racks = new ArrayList<String>();     // Process all racks over and over again until there is no more work to do.while (blockToNodes.size() > 0) {      //Create one split for this rack before moving over to the next rack.       // Come back to this rack after creating a single split for each of the       // remaining racks.      // Process one rack location at a time, Combine all possible blocks that      // reside on this rack as one split. (constrained by minimum and maximum      // split size).       // iterate over all racks       // 依次处理每个机架for (Iterator<Map.Entry<String, List<OneBlockInfo>>> iter =            rackToBlocks.entrySet().iterator(); iter.hasNext();) {        Map.Entry<String, List<OneBlockInfo>> one = iter.next();        racks.add(one.getKey());        List<OneBlockInfo> blocks = one.getValue();         // for each block, copy it into validBlocks. Delete it from// blockToNodes so that the same block does not appear in// two different splits.boolean createdSplit = false;// 依次处理该机架的每个数据块for (OneBlockInfo oneblock : blocks) {          if (blockToNodes.containsKey(oneblock)) {            validBlocks.add(oneblock);            blockToNodes.remove(oneblock);            curSplitSize += oneblock.length;// if the accumulated split size exceeds the maximum, then create this split.            // 如果数据块累积大小大于或等于maxSize，则形成一个切片if (maxSize != 0 && curSplitSize >= maxSize) {              //create an input split andadd it to the splits array              addCreatedSplit(job, splits, getHosts(racks), validBlocks);              createdSplit = true;              break;            }          }        }         // if we created a split, then just go to the next rackif (createdSplit) {          curSplitSize = 0;          validBlocks.clear();          racks.clear();          continue;        }         if (!validBlocks.isEmpty()) {          // 如果剩余数据块大小大于或等于minSizeRack，则将这些数据块构成一个切片if (minSizeRack != 0 && curSplitSize >= minSizeRack) {            // if there is a mimimum size specified, then create a single split            // otherwise, store these blocks into overflow data structure            addCreatedSplit(job, splits, getHosts(racks), validBlocks);          } else {            // There were a few blocks in this rack that remained to be processed.            // Keep them in 'overflow' block list. These will be combined later.            // 如果剩余数据块大小小于minSizeRack，则将这些数据块加入overflowBlocks            overflowBlocks.addAll(validBlocks);          }        }        curSplitSize = 0;        validBlocks.clear();        racks.clear();      }    }

 

（3）遍历并累加剩余数据块，代码如下：

// Process all overflow blocksfor (OneBlockInfo oneblock : overflowBlocks) { validBlocks.add(oneblock); curSplitSize += oneblock.length;// This might cause an exiting rack location to be re-added,// but it should be ok.for (int i = 0; i < oneblock.racks.length; i++) {   racks.add(oneblock.racks[i]); }// if the accumulated split size exceeds the maximum, then //create this split.// 如果剩余数据块大小大于或等于maxSize，则将这些数据块构成一个切片if (maxSize != 0 && curSplitSize >= maxSize) {//create an input split andadd it to the splits array   addCreatedSplit(job, splits, getHosts(racks), validBlocks);   curSplitSize = 0;   validBlocks.clear();   racks.clear(); }    }

 

 

（4）剩余数据块形成一个切片,代码如下：

// Process any remaining blocks, if any.if (!validBlocks.isEmpty()) {      addCreatedSplit(job, splits, getHosts(racks), validBlocks);    }

 

总结

CombineFileInputFormat形成切片过程中考虑数据本地性（同一节点、同一机架），首先处理同一节点的数据块，然后处理同一机架的数据块，最后处理剩余的数据块，可见本地性是逐步减弱的。另外CombineFileInputFormat是抽象的，具体使用时需要自己实现getRecordReader方法。

 

 

 

 

 

 

 

（3）SequenceFileInputFormat/SequenceFileOutputFormat

sequenceFile是hadoop中非常重要的一种数据格式

sequenceFile文件内部的数据组织形式是：K-V对

读入/写出为hadoop序列文件

 

示例代码：

 

 

 

 

 

## **6.2 MultipleInputs**

虽然FileInputFormat可以读取多个目录，但是有些场景下我们要处理的数据可能有不同的来源，或者经历过版本升级而产生格式的差别。比如一些文件是tab分隔，一些文件是逗号分隔，此时就可以使用MultipleInputs，可以为不同的路径指定不同的mapper类来处理；

 

应用示例：假如某数据分析系统需要分析的数据有两类文件格式，一类为普通Text文本，一类为SequenceFile格式文件

实现步骤：

（1） 对应不同格式文件，相应地要编写两个不同逻辑的mapper类

 

​	static class TextMapperA extends Mapper<LongWritable, Text, Text, LongWritable> {		@Override		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException { 			String line = value.toString();			String[] words = line.split(" ");			for (String w : words) {				context.write(new Text(w), new LongWritable(1));			}		}	}

 

​	static class SequenceMapperB extends Mapper<Text, LongWritable, Text, LongWritable> {		@Override		protected void map(Text key, LongWritable value, Context context) throws IOException, InterruptedException { 			context.write(key, value); 		}	}

 

（2）在job描述中使用MultipleInputs对不同类型数据设置不同的mapper类及inputformat来处理

​	public static void main(String[] args) throws Exception {		Configuration conf = new Configuration();		Job job = Job.getInstance(conf);		job.setJarByClass(WordCount.class);		// 为不同路径的文件指定不同的mapper类及inputformat类		MultipleInputs.addInputPath(job, new Path("c:/wordcount/textdata"), TextInputFormat.class, TextMapperA.class);		MultipleInputs.addInputPath(job, new Path("c:/wordcount/seqdata"), SequenceFileInputFormat.class, SequenceMapperB.class);		job.setReducerClass(SameReducer.class);		job.setMapOutputKeyClass(Text.class);		job.setMapOutputValueClass(LongWritable.class);		FileOutputFormat.setOutputPath(job, new Path("c:/wordcount/multiinouts"));		job.waitForCompletion(true);	}

 

 

 

 

## **6.3 自定义Inputformat**

当框架自带的TextInputformat，SequenceFileInputFormat不能满足需求时，可以自定义InputFormat来读取文件。

 

场景示例：将小文件整个合入大文件SequenceFile（在生产实际中常用，MR擅长处理大文件，而很多生产系统所产生的数据多为大量小文件，如果直接用hadoop来分析处理，效率较低，而通过SequenceFile可以方便地将小文件合并为大文件，从而提高处理效率）

通常做法是：将小文件的文件名作为key，将小文件的内容作为value，写入一个大的SequenceFile中）

 

代码实现：

（1）自定义一个InputFormat 

​	static class WholeFileInputFormat extends FileInputFormat<NullWritable, BytesWritable> {		@Override         //改写父类逻辑，总是返回false，从而让		protected boolean isSplitable(JobContext context, Path filename) {			return false;		} 		@Override		public RecordReader<NullWritable, BytesWritable> createRecordReader(InputSplit split, TaskAttemptContext context) throws IOException, InterruptedException {              //返回一个自定义的RecordReader用于读取数据			WholeFileRecordReader reader = new WholeFileRecordReader();			reader.initialize(split, context);			return reader;		}	}

（4）实现自定义的WholeFileRecordReader

class WholeFileRecordReader extends RecordReader<NullWritable, BytesWritable> { 		private FileSplit fileSplit;		private Configuration conf;		//定义一个bytes缓存，用来存储一个小文件的数据内容		private BytesWritable value = new BytesWritable();		private boolean processed = false; 		//初始化方法，将传入的文件切片对象和context对象赋值给类成员		@Override		public void initialize(InputSplit split, TaskAttemptContext context) throws IOException, InterruptedException {			fileSplit = (FileSplit) split;			conf = context.getConfiguration();		} 		@Override		//核心逻辑，用于从源数据中读取数据并封装为KEY  / VALUE		public boolean nextKeyValue() throws IOException, InterruptedException {			//当前小文件处理过，则processed为true			if (!processed) { 				byte[] contents = new byte[(int) fileSplit.getLength()];				Path filePath = fileSplit.getPath();				FileSystem fs = filePath.getFileSystem(conf);				FSDataInputStream in = fs.open(filePath);				IOUtils.readFully(in, contents, 0, contents.length);				value.set(contents, 0, contents.length);				IOUtils.closeStream(in);				processed = true;				return true; 			}			//如果当前小文件已经处理过，则返回false，以便调用者跳到下一个文件切片的处理			return false;		} 		@Override		//返回一个key		public NullWritable getCurrentKey() throws IOException, InterruptedException {			// TODO Auto-generated method stub			return NullWritable.get();		} 		@Override		//返回一个values		public BytesWritable getCurrentValue() throws IOException, InterruptedException {			// TODO Auto-generated method stub			return value;		} 		@Override		//用于返回进度信息，读完一个小文件即返回1		public float getProgress() throws IOException, InterruptedException {			// TODO Auto-generated method stub			return processed ? 1.0f : 0.0f;		} 		@Override		public void close() throws IOException {			// TODO Auto-generated method stub 		} 	}

 

 

## **6.4 Mapreduce输出格式组件**

### **6.4.1** **TextOutPutFormat源码结构解析：**

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps13.jpg) 

 

 

 

### **6.4.2 MultipleOutputs**

​	static class CountReducer extends Reducer<Text, LongWritable, Text, LongWritable> {		MultipleOutputs<Text, LongWritable> multipleOutputs = null; 		//在初始化方法中构造一个multipleOutputs		protected void setup(Context context) throws IOException, InterruptedException { 			multipleOutputs = new MultipleOutputs<Text, LongWritable>(context); 		}; 		@Override		protected void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException { 			long count = 0;			for (LongWritable value : values) {				count += value.get();			}			if (key.toString().startsWith("a")) {				//可以通过条件判断将不同内容写入不同文件				multipleOutputs.write(key, new LongWritable(count), "c:/multi/outputa/a");			} else {				multipleOutputs.write(key, new LongWritable(count), "c:/sb/outputb/b");			} 		}				//一定要对multipleOutputs进行close，否则内容不会真实写入文件		@Override		protected void cleanup(Context context) throws IOException, InterruptedException {			multipleOutputs.close();		} 	}

 

### **6.4.3 自定义FileOutPutFormat**

public class FlowOutputFormat extends FileOutputFormat<Text, NullWritable> { 	@Override	public RecordWriter<Text, NullWritable> getRecordWriter(			TaskAttemptContext context) throws IOException,			InterruptedException { 		FileSystem fs = FileSystem.get(context.getConfiguration()); 		Path enhancelog = new Path("hdfs://weekend01:9000/enhance/enhanced.log");		Path tocrawl = new Path("hdfs://weekend01:9000/enhance/tocrawl.log"); 		//构造两个不同的输出流		FSDataOutputStream enhanceOs = fs.create(enhancelog);		FSDataOutputStream tocrawlOs = fs.create(tocrawl); 				//通过构造函数将两个流传给FlowRecordWriter		return new FlowRecordWriter(enhanceOs, tocrawlOs);	} 	public static class FlowRecordWriter extends			RecordWriter<Text, NullWritable> { 		private FSDataOutputStream enhanceOs;		private FSDataOutputStream tocrawlOs; 		public FlowRecordWriter(FSDataOutputStream enhanceOs,				FSDataOutputStream tocrawlOs) { 			this.enhanceOs = enhanceOs;			this.tocrawlOs = tocrawlOs; 		} 		//具体的写出动作在write方法中完成		@Override		public void write(Text key, NullWritable value) throws IOException,				InterruptedException {			String line = key.toString();			if (line.contains("itisok")) {				enhanceOs.write(line.getBytes()); 			} else { 				tocrawlOs.write(line.getBytes()); 			} 		} 		@Override		public void close(TaskAttemptContext context) throws IOException,				InterruptedException {			if (enhanceOs != null) {				enhanceOs.close();			}			if (tocrawlOs != null) {				tocrawlOs.close();			} 		}	} }

 

 

 

 

 

## **6.5 Configuration配置对象与Toolrunner**

（1）配置参数的优先级：

集群*-site.xml < src/conf < conf.set()

（2）Toolrunner----可通过提交命令动态设置配置参数或文件

Configuration对象还可以用来分发少量数据到所有任务节点

 

示例：

/**可以通过运行时加参数来传递参数给conf对象-D	property=value-conf	filename	...-fs	uri  等价于 -D	fs.defaultFS=uri-jt	host:port 等价于 -D yarn.resourcemanager.address=host:port-files file1,file2,-archives archive1,archive2-libjars jar1,jar2,... * * @author duanhaitao@itcast.cn * */public class TestToolrunner extends Configured implements Tool { 	static {		Configuration.addDefaultResource("hdfs-default.xml");		Configuration.addDefaultResource("hdfs-site.xml");		Configuration.addDefaultResource("core-default.xml");		Configuration.addDefaultResource("core-site.xml");		Configuration.addDefaultResource("mapred-default.xml");		Configuration.addDefaultResource("mapred-site.xml");		Configuration.addDefaultResource("yarn-default.xml");		Configuration.addDefaultResource("yarn-site.xml");	} 	@Override	public int run(String[] args) throws Exception {		Configuration conf = getConf();		TreeMap<String, String> treeMap = new TreeMap<String,String>();		for (Entry<String, String> ent : conf) {			treeMap.put(ent.getKey(), ent.getValue());					}						for (Entry<String, String> ent : treeMap.entrySet()) { 			System.out.printf("%s=%s\n", ent.getKey(), ent.getValue()); 		} 		return 0;	}		public static void main(String[] args) throws Exception {		ToolRunner.run(new TestToolrunner(), args);	} }

 

 

 

## **6.6 mapreduce数据压缩**

运算密集型的job，少用压缩

IO密集型的job，多用压缩

 

 

通过压缩编码对mapper或者reducer的输出进行压缩，以减少磁盘IO，提供MR程序运行速度（但相应增加了cpu运算负担）

 

（1）MR支持的压缩编码

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps14.png) 

（2）Reducer输出压缩

----设置 

mapreduce.output.fileoutputformat.compress=false

mapreduce.output.fileoutputformat.compress.codec=org.apache.hadoop.io.compress.DefaultCodec

mapreduce.output.fileoutputformat.compress.type=RECORD

或在代码中设置

​		Job job = Job.getInstance(conf);		FileOutputFormat.setCompressOutput(job, true);		FileOutputFormat.setOutputCompressorClass(job, (Class<? extends CompressionCodec>) Class.forName(""));

 

（3）Mapper输出压缩

----设置

mapreduce.map.output.compress=false

mapreduce.map.output.compress.codec=org.apache.hadoop.io.compress.DefaultCodec

 

或者在代码中：

conf.setBoolean(Job.MAP_OUTPUT_COMPRESS, true);conf.setClass(Job.MAP_OUTPUT_COMPRESS_CODEC,                   GzipCodec.class, CompressionCodec.class);

 

 

 

（4）压缩文件的读取

Hadoop自带的InputFormat类内置支持压缩文件的读取，比如TextInputformat类，在其initialize方法中：

  public void initialize(InputSplit genericSplit,                         TaskAttemptContext context) throws IOException {    FileSplit split = (FileSplit) genericSplit;    Configuration job = context.getConfiguration();    this.maxLineLength = job.getInt(MAX_LINE_LENGTH, Integer.MAX_VALUE);    start = split.getStart();    end = start + split.getLength();    final Path file = split.getPath();     // open the file and seek to the start of the split    final FileSystem fs = file.getFileSystem(job);    fileIn = fs.open(file);    //根据文件后缀名创建相应压缩编码的codec    CompressionCodec codec = new CompressionCodecFactory(job).getCodec(file);    if (null!=codec) {      isCompressedInput = true;	      decompressor = CodecPool.getDecompressor(codec);	  //判断是否属于可切片压缩编码类型      if (codec instanceof SplittableCompressionCodec) {        final SplitCompressionInputStream cIn =          ((SplittableCompressionCodec)codec).createInputStream(            fileIn, decompressor, start, end,            SplittableCompressionCodec.READ_MODE.BYBLOCK);		 //如果是可切片压缩编码，则创建一个CompressedSplitLineReader读取压缩数据        in = new CompressedSplitLineReader(cIn, job,            this.recordDelimiterBytes);        start = cIn.getAdjustedStart();        end = cIn.getAdjustedEnd();        filePosition = cIn;      } else {		//如果是不可切片压缩编码，则创建一个SplitLineReader读取压缩数据，并将文件输入流转换成解压数据流传递给普通SplitLineReader读取        in = new SplitLineReader(codec.createInputStream(fileIn,            decompressor), job, this.recordDelimiterBytes);        filePosition = fileIn;      }    } else {      fileIn.seek(start);	   //如果不是压缩文件，则创建普通SplitLineReader读取数据      in = new SplitLineReader(fileIn, job, this.recordDelimiterBytes);      filePosition = fileIn;    }

 

## **6.7 mapreduce的计数器**

### **6.7.1 mapreduce框架自带计数器：** 

Task group

Inputformat group

Outputformat group

Framework group

 

### **6.7.2 用户自定义计数器**

ü 枚举方式

ü 动态设置

 

public class MultiOutputs {	//通过枚举形式定义自定义计数器	enum MyCounter{MALFORORMED,NORMAL} 	static class CommaMapper extends Mapper<LongWritable, Text, Text, LongWritable> { 		@Override		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException { 			String[] words = value.toString().split(","); 			for (String word : words) {				context.write(new Text(word), new LongWritable(1));			}			//对枚举定义的自定义计数器加1			context.getCounter(MyCounter.MALFORORMED).increment(1);			//通过动态设置自定义计数器加1			context.getCounter("counterGroupa", "countera").increment(1);		} 	}

 

 

计数器原理简述（由appmaster维护，是一个全局的）

 

 

## **6.8 mapreduce的日志分析**

日志存放位置

（1）系统服务进程的日志，默认存放在hadoop安装目录下的logs目录中

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps15.jpg) 

 

 

（2）用户应用输出的日志：

 

 

 

日志配置

 

 

 

## **6.9 多job串联**

借助jobControl类来建立job间顺序和依赖关系；

示例：

​      ControlledJob cJob1 = new ControlledJob(job1.getConfiguration());        ControlledJob cJob2 = new ControlledJob(job2.getConfiguration());        ControlledJob cJob3 = new ControlledJob(job3.getConfiguration());               // 设置作业依赖关系        cJob2.addDependingJob(cJob1);        cJob3.addDependingJob(cJob2);         JobControl jobControl = new JobControl("RecommendationJob");        jobControl.addJob(cJob1);        jobControl.addJob(cJob2);        jobControl.addJob(cJob3);         cJob1.setJob(job1);        cJob2.setJob(job2);        cJob3.setJob(job3);         // 新建一个线程来运行已加入JobControl中的作业，开始进程并等待结束        Thread jobControlThread = new Thread(jobControl);        jobControlThread.start();        while (!jobControl.allFinished()) {            Thread.sleep(500);        }        jobControl.stop();         return 0;

 

 

 

动手练习

 

 

 

 

 

## **附：MR常见算法练习**

### **1 数据去重----（预处理：清洗、过滤、去重）**

2012-3-1 a2012-3-2 b2012-3-3 c2012-3-4 d2012-3-5 a2012-3-6 b2012-3-7 c2012-3-3 c

 

### **2 数据排序**

A、 用一个reducer

B、 用多个reducer（自定义partitioner/用inputsampler抽样后生成partitioner，用totalorder）

变形：分组排序、topk（自己写一遍）

 

 

如原始数据：

23265432157566522359562265092

要求结果：

1    22    63    154    225    266    327    328    549    9210    65011    65412    75613    595614    65223

 

 

### **3 求均值**

 

原始数据：

1）math： 张三    88李四    99王五    66赵六    77 2）chinese： 张三    78李四    89王五    96赵六    67 3）english： 张三    80李四    82王五    84赵六    86

 

输出结果：

张三    82李四    90王五    82赵六    76

 

 

### **4 单表关联**

给出child-parent（孩子——父母）表，要求输出grandchild-grandparent（孙子——爷奶）表。

样例输入如下所示。

file：

child		parentTom		LucyTom		JackJone		LucyJone		JackLucy	MaryLucy	BenJack		AliceJack		JesseTerry	AliceTerry	JessePhilip	TerryPhilip	AlmaMark	TerryMark	Alma

输出结果：

grandchild	grandparentTom		AliceTom		JesseJone		AliceJone		JesseTom		MaryTom		BenJone		MaryJone		BenPhilip	AlicePhilip	JesseMark	AliceMark	Jesse

 

### **5 多表关联**

Map side join

Reduce side join

 

 

### **6 日志解析**

简单转换（如字段截取，字符串替代等）

外部字典替换

格式转换（如json，xml等格式转换为plain text）

 

 

### **7 共同好友**

原始数据：每个人的好友列表

A:B,C,D,F,E,OB:A,C,E,KC:F,A,D,ID:A,E,F,LE:B,C,D,M,LF:A,B,C,D,E,O,MG:A,C,D,E,FH:A,C,D,E,OI:A,OJ:B,OK:A,C,DL:D,E,FM:E,F,GO:A,H,I,J……

 

输出结果：每个人和其他各人所拥有的功能好友

A-B	C,E,A-C	D,F,A-D	E,F,A-E	B,C,D,A-F	B,C,D,E,O,A-G	C,D,E,F,A-H	C,D,E,O,A-I	O,A-J	B,O,A-K	C,D,A-L	D,E,F,A-M	E,F,B-C	A,B-D	A,E,……

 

### **8 其他杂例** 

#### **去哪儿网笔试题：**

去哪儿旅行的APP每天会产生大量的访问日志。用户【uuid-x】的每一次操作记录会产生一条日志记录，假设用户可以通过单程搜索【search-dancheng】，往返搜索【search-wangfan】等多个入口进入报价详情页【detail】选择航班并完成最后的下订单【submit】购票操作。日志格式如下，请编写Map/Reduce程序完成如下需求（伪代码完成即可）

a） 计算20140510这一天去哪儿旅行APP的订单有多少来自单程搜索，有多少来自往返搜索

 

日志示例（仅作示例【片段，每天数据量会非常大】）：

20140510	09:17:19	uuid-01	search-dancheng	dep=北京&arr=上海&date=20140529&pnvm=020140510	09:18:20	uuid-02	search-wangFan	dep=北京&arr=上海&sdate=20140529&edate=2014060520140510	09:18:23	uuid-01	detail	dep=北京&arr=上海&date=20140529&fcode=CA181020140510	09:20:29	uuid-02	detail	dep=北京&arr=上海&date=20140529&fcode=CA181020140510	09:21:19	uuid-01	submit	dep=北京&arr=上海&date=20140529&fcode=CA1810&price=128020140510	09:23:19	uuid-03	search-dancheng	dep=北京&arr=广州&date=20140529&pnvm=020140510	09:25:19	uuid-04	search-dancheng	dep=北京&arr西安&date=20140529&pnvm=020140510	09:25:30	uuid-05	search-dancheng	dep=北京&arr=天津&date=20140529&pnvm=020140510	09:26:29	uuid-04	detail	dep=北京&arr=西安&上海&date=20140529&fcode=CA181020140510	09:28:19	uuid-06	submit	dep=北京&arr=拉萨&date=20140529&fcode=CA1810&price=2260

 

#### **电力公司数据更新日志合并**

 

 

 

#### **某公司日志处理需求说明：**

​		根据系统和关键字查询日志，并将关键字所在行以下10行数据输出或保存到hdfs，最终是把这些数据展示到Web页面。

（关键字所在的数据行与它以下10行数据并没有关联关系，日志数据为很乱的原数据。）

 

java应用+shell脚本+spark.jar包

java应用负责用户登录后，输入系统、关键字等参数，提交查询，java调用shell脚本-->submit

结果数据保存到hdfs上。保存的该文件用随机数命名，最后在Web页面读取展示出来。

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps16.jpg)

样例数据如下：

15-06-10.23:58:02.321 [pool-22-thread-5] INFO  HttpPostMessageSender   -  HttpPostMessageSender resp statusCode: 200 content:success tradeno:201506101000100007065068315-06-10.23:58:02.321 [pool-22-thread-5] INFO  HttpPostMessageSender   - HttpPost 是否发送成功  true15-06-10.23:58:02.321 [pool-22-thread-5] INFO  NotificationServiceImpl  - ****进行入库操作****15-06-10.23:58:02.324 [pool-22-thread-5] INFO  NotificationServiceImpl  - ****没有此TRADE_NO,新增Notification****tradeNo=201506101000100007065068315-06-10.23:58:02.327 [pool-22-thread-5] INFO  NotifyServiceImpl       - ****enter--saveOrUpdateNotity****15-06-10.23:58:02.330 [pool-22-thread-5] INFO  NotifyServiceImpl       - ****没有此TRADE_NO,新增Notify****tradeNo=201506101000100007065068315-06-10.23:58:02.333 [pool-22-thread-5] INFO  ACCESS                  - 2015061010001000070650683,FINISHED_SUCCESS15-06-10.23:58:04.250 [pool-20-thread-2] INFO  NPPListener             - Received a new message OutTradeNotify{tradeInfo=TradeInfo{outTradeNo='150610263916206067998', tradeNo='2015061010001000070650827', originalTradeNo='null', bizTradeNo='9488771051', tradeType=TRADE_GENERAL, subTradeType=SALE, payMethod=CASHIERGATEMODE, tradeMoney=Money{currency=CNY, amount=10420}, tradeSubject='消费订单', submitter=ThinCustomer{merchantNo='23077370', customerNo='360080000230773708', customerLoginName='null', customerName='null', customerOutName='null'}, seller=ThinCustomer{merchantNo='23077370', customerNo='360080000230773708', customerLoginName='null', customerName='null', customerOutName='null'}, sellerAccountNo='360080000230773708000811', buyer=ThinCustomer{merchantNo='null', customerNo='360000000260175680', customerLoginName='null', customerName='null', customerOutName='null'}, tradeStatus=TRADE_FINISHED, createdDate=Wed Jun 10 23:57:32 CST 2015, deadlineTime=null, tradeFinishedDate='20150610', tradeFinishedTime='235802', payTool=EXPRESS, bankCode='CEB', exchangeDate='null', exchangeRate='null', returnParams='null', oldGWV60AuthCode='null', oldEXV10TerminalNo='null', clearingCurrency=null, clearingMoney=null, tradeExtInfo=TradeExtInfo{notifyStatus='NOT', outMessageId='null', cardSha1='null', signNo='null', returnParams='null', extendParams='null', pageBackUrl='null', serverNotifyUrl='http://gw.jd.com/payment/notify_chinabankReal.action', notifySmsMoible='null', notifyMailAddress='null', innerMessageFormat='XML', apiMessageFormat='EX_V1.0', requestCharset='UTF-8', encryptType='3DES', signType='MD5', requestModule='null', requestVersion='null', remoteIp='109.145.60.24', receivingChannel='JDSC', requestProtocol='HTTP', requestMethod='null', outTradeDate='20150610', outTradeTime='235731', outTradeIp='109.145.60.24', outRefererHosts='null', retryCount=1}, ext=null}}, OutMessageNotify{apiMessageFormat=null, messageFormat=null, notifyCharset='null', signType='null', encryptType='null'}, MessageNotify{responseModule='null', responseCode='null', responseDesc='null'}15-06-10.23:58:04.253 [pool-20-thread-2] INFO  KeyServiceImpl          - Calling SecurityService to get {} key for merchant {} with codeClass {}23077370KeyTypeEnum{code='3DES', cnName='三DES'}EXPRESS15-06-10.23:58:04.264 [pool-20-thread-2] INFO  CustomerCenterFacade    - [INVOCATION_LOG_C] 2015-06-10.23:58:04.264;pool-20-thread-2;172.17.92.48:0->172.17.87.47:20996;com.wangyin.customer.api.CustomerCenterFacade:1.1.6.getMerchantCustomerKeys(com.wangyin.customer.common.dto.customer.CustomerParamDTO);***;2015-06-10.23:58:04.253;RESULT:***;11,112,359;15-06-10.23:58:04.264 [pool-20-thread-2] INFO  KeyServiceImpl          - 获取的3DES 密钥值为20B0984A9B751F0B911A1AEA0738D557AE16548CCE029E2A15-06-10.23:58:04.264 [pool-20-thread-2] INFO  KeyServiceImpl          - Calling SecurityService to get {} key for merchant {} with codeClass {}23077370KeyTypeEnum{code='SALT', cnName='签名密钥'}EXPRESS15-06-10.23:58:04.270 [pool-24-thread-4] INFO  NPPListener             - Received a new message OutTradeNotify{tradeInfo=TradeInfo{outTradeNo='22015061023575751670871914', tradeNo='2015061010001000070651406', originalTradeNo='null', bizTradeNo='null', tradeType=TRADE_GENERAL, subTradeType=SALE, payMethod=APIEXPRESSMODE, tradeMoney=Money{currency=CNY, amount=500000}, tradeSubject='消费订单', submitter=ThinCustomer{merchantNo='22843776', customerNo='360080000228437761', customerLoginName='null', customerName='null', customerOutName='null'}, seller=ThinCustomer{merchantNo='22843776', customerNo='360080000228437761', customerLoginName='null', customerName='null', customerOutName='null'}, sellerAccountNo='360080000228437761000811', buyer=null, tradeStatus=TRADE_FINISHED, createdDate=Wed Jun 10 23:57:57 CST 2015, deadlineTime=null, tradeFinishedDate='20150610', tradeFinishedTime='235802', payTool=EXPRESS, bankCode='ICBC', exchangeDate='null', exchangeRate='null', returnParams='22894010', oldGWV60AuthCode='null', oldEXV10TerminalNo='00000002', clearingCurrency=null, clearingMoney=null, tradeExtInfo=TradeExtInfo{notifyStatus='NOT', outMessageId='API.150610.0ddf8c2f7ed94f3e9f741cd44500a866', cardSha1='5D72C7755A82576EE906BAB8314164ABAC513C9C', signNo='201505110010089270009113541', returnParams='22894010', extendParams='null', pageBackUrl='null', serverNotifyUrl='http://jrb-api.d.chinabank.com.cn/notify/quick.htm', notifySmsMoible='null', notifyMailAddress='null', innerMessageFormat='XML', apiMessageFormat='EX_V1.0', requestCharset='UTF-8', encryptType='3DES', signType='MD5', requestModule='null', requestVersion='null', remoteIp='172.17.80.168', receivingChannel='API', requestProtocol='HTTP', requestMethod='POST', outTradeDate='null', outTradeTime='null', outTradeIp='null', outRefererHosts='null', retryCount=1}, ext=null}}, OutMessageNotify{apiMessageFormat=null, messageFormat=null, notifyCharset='null', signType='null', encryptType='null'}, MessageNotify{responseModule='null', responseCode='null', responseDesc='null'}15-06-10.23:58:04.271 [pool-20-thread-2] INFO  CustomerCenterFacade    - [INVOCATION_LOG_C] 2015-06-10.23:58:04.271;pool-20-thread-2;172.17.92.48:0->172.17.91.104:20996;com.wangyin.customer.api.CustomerCenterFacade:1.1.6.getMerchantCustomerKeys(com.wangyin.customer.common.dto.customer.CustomerParamDTO);***;2015-06-10.23:58:04.264;RESULT:***;6,971,110;15-06-10.23:58:04.272 [pool-20-thread-2] INFO  KeyServiceImpl          - 获取MD5 TOKEN 密钥的值为1qaz2wsx3edc15-06-10.23:58:04.273 [pool-20-thread-2] INFO  NPPNotifyProcessorImpl  - ApiMessageFormatEX_V1.015-06-10.23:58:04.273 [pool-24-thread-4] INFO  KeyServiceImpl          - Calling SecurityService to get {} key for merchant {} with codeClass {}22843776KeyTypeEnum{code='3DES', cnName='三DES'}EXPRESS15-06-10.23:58:04.273 [pool-20-thread-2] INFO  NPPNotifyProcessorImpl  - 转化为NotificationDTO的结果为: com.wangyin.npp.notify.facade.dto.NotificationDTO@54b2789015-06-10.23:58:04.273 [pool-20-thread-2] INFO  NotificationServiceImpl  - 准备入库(可能会入库)的 notification=Notification [TRADE_NO=2015061010001000070650827, SOURCE_NAME=NPP_PAYMENT_COMPLETE, FROM_ADDRESS=EXPRESS, FROM_NAME=23077370, TO_ADDRESS=http://gw.jd.com/payment/notify_chinabankReal.action, CHANNEL=HTTP_POST, SUBJECT=null, CONTENT=resp=PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4NCjxDSElOQUJBTks%2BCiAgPFZFUlNJT04%2BMS4wLjA8L1ZFUlNJT04%2BCiAgPE1FUkNIQU5UPjIzMDc3MzcwPC9NRVJDSEFOVD4KICA8VEVSTUlOQUw%2BMDAwMDAwMDE8L1RFUk1JTkFMPgogIDxEQVRBPllFbm10T0Zkb0RBK0tHdmhVZmJBZTlKOVZDOC9ONGx1YW5uMlBTRFF0L0VNTUh3eHR6L29tYi9vdlArTjAybnlsTGdhbUhCVDBZYVpBMUxoSC9iV3RndmoxN0JMTDhPTFc3U3laZmMxMU5sczRqSFdGeUR1UHNsb3F4YU51aFdUUFFDTzljMCtrTFpDZkpuZHB6d2sxN3J4dU5mRGVuYmljZ21kWHphSlhQNElQZzFKQ2h1ZGRRNWdTQTQ4UWVPVEE0UUhJYUsyQVFJNTNZQU03RHdQWFBrZkNPMythRUgvMk5oeGJMRmtYMTEvalJWUUI0NDM1K2FtSm1zclE0UFJ5cVVSWmx6eGVJQk5XNU4xZnZjMUE1NXRVa1RmRjNWc1orWjU2WkdydFoyQzdnQ3BWNkxqOUNDUWlzbjhKMEd3Z2JLS0kvdUMyUVNDTHJOMUl3YU8waSsxUUFIVWdPRGRtTFZHUGxhSTBqTS85UWVmY0Q2R0FjaVJua214R

 

# **7. Yarn集群**

## **7.1 Yarn产生的原因**

（1）MapreduceV1中，jobtracker存在瓶颈：

​	集群上运行的所有mr程序都有jobtracker来调度

​	SPOF单点故障

​	职责划分不清晰

 

（2） 将jobtracker的职责划分成两个部分：

ü 资源调度与管理：由统一的资源调度平台（集群）来实现（yarn）

ü 任务监控与管理：

A、每一个application运行时拥有一个自己的任务监控管理进程AppMaster

B、AppMaster的生命周期：application提交给yarn集群之后，yarn负责启动该application的AppMaster，随后任务的执行监控调度等工作都交由AppMaster，待这个application运行完毕后，AppMaster向yarn注销自己。

C、AppMaster的具体实现由application所使用的分布式运算框架自己负责，比如Mapreduce类型的application有MrAppMaster实现类。Spark DAG应用则有SparkOnYarn的SparkContext实现

 

 

 

## **7.2 Yarn的架构**

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps17.jpg) 

（1）ResourceManager ----> master node，可配多个RM实现HA机制，

由两个核心组件构成：

Scheduler 和ApplicationsManager;

Scheduler：负责资源调度，调度策略可插拔（内置实现 CapacityScheduler / FairScheduler ），不提供对application运行的监控;

ApplicationsManager：负责响应任务提交请求，协商applicationMaster运行的container，重启失败的applicationMaster

 

 

（2）NodeManager ----> slave nodes，每台机器上一个

职责：加载containers，监控各container的资源使用情况，并向Resourcemanager/Scheduler汇报

 

 

（3）ApplicationMaster ----> 特定运算框架自己实现，接口为统一的AppMaster

职责：向Scheduler请求适当的资源，跟踪任务的执行，监控任务执行进度、状态等

 

 

## **7.3** **Yarn运行****application****的流程**

 详细参见《yarn运行application的流程图》

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps18.jpg) 

 

*Job提交流程详解

流程简述

源码跟踪：注重客户端与resourcemanager之间的交互

 

## **7.4 MapReduce程序向yarn提交执行的流程分析**

Job.waitForCompletion()

创建  yarnrunner

向resourcemanager提交请求，获取application id

Yarnrunner提交job资源

 

## **7.5 application生命周期**

Yarn支持短周期和长周期应用

MR：短周期应用，用户的每一个job为一个application

Spark：短周期应用，但比上一种效率要高，它是将一个工作流（DAG）转化为一个application，这样在job之间可以重用container及中间结果数据可以不用落地

 

Storm：long-running应用，应用为多用户共享，降低了资源调度的前期消耗，从而可以为用户提供低时延响应

 

 

## **7.5资源请求**

资源请求由Container对象描述，支持数据本地性约束，如处理hdfs上的数据，则container优先分配在block所在的datanode，如该datanode资源不满足要求，则优选同机架，还不能满足则随机分配

 

Application可以在其生命周期的任何阶段请求资源，可以在一开始就请求所需的所有资源，也可以在运行过程中动态请求资源；如spark，采用第一种策略；而MR则分两个阶段，map task的资源是在一开始一次性请求，而reduce task的资源则是在运行过程中动态请求；并且，任务失败后，还可以重新请求资源进行重试

 

 

 

## **7.6 任务调度****--capacity scheduler / fair scheduler**

由于集群资源有限，当无法满足众多application的资源请求时，yarn需要适当的策略对application的资源请求进行调度；

### **7.6.1 Scheduler概述**

Yarn中实现的调度策略有三种：FIFO/Capacity/Fair Schedulers

 （1）FIFO Scheduler：

将所有application按提交的顺序排队，先进先出

优点---->简单易懂且不用任何配置

缺点---->不适合于shared clusters；大的应用会将集群资源占满从而导致大量应用等待

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps19.jpg) 

 

（2）Capacity Scheduler

将application划分为多条任务队列，每条队列拥有相应的资源

在队列的内部，资源分配遵循FIFO策略

队列资源支持弹性调整：一个队列的空闲资源可以分配给“饥饿”队列（注意：一旦之前的空闲队列需求增长，因为不支持“先占”，不能强制kill资源container，则需要等待其他队列释放资源；为防止这种状况的出现，可以配置队列最大资源进行限制）

任务队列支持继承结构

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps20.jpg) 

 

（3）Fair Scheduler

不需要为特定small application保留资源，而是在需要执行时进行动态公平分配；

动态资源分配有一个延后，因为需要等待large job释放一部分资源

Small job资源使用完毕后，large job可以再次获得全部资源

Fair Scheduler也支持在application queue之间进行调度

 ![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps21.jpg)

 

  

### **7.6.2 Capacity Scheduler配置**

yarn的Scheduler机制，由yarn-site.xml中的配置参数指定：

<name>yarn.resourcemanager.scheduler.class</name>

默认值为：

<value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.fair.CapacityScheduler </value>

修改为：

<value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.FairScheduler</value>

 

CapacityScheduler的配置文件则位于：

etc/hadoop/capacity-scheduler.xml 

 

capacity-scheduler .xml示例

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps22.jpg) 

 

 

 

 

 

 

 

 

 

 

 

 

 

如果修改了capacity-scheduler.xml（比如添加了新的queue），只需要执行：

*yarn rmadmin -refreshQueues*即可生效

 

application中指定所属的queue使用配置参数：

​	mapreduce.job.queuename

在示例配置中，此处queuename即为prod或dev或science

如果给定的queue name不存在，则在submission阶段报错

如果没有指定queue name，则会被列入default queue

 

 

### **7.6.3 Fair Scheduler配置**

 

Fair Scheduler工作机制

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps23.jpg) 

 

 

 

 

 

启用Fair Scheduler，在yarn-site.xml中

<property> <name>yarn.resourcemanager.scheduler.class</name> <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.fair.FairScheduler</value></property>

 

配置参数--参考官网：

<http://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/FairScheduler.html>

一部分位于yarn-site.xml

| yarn.scheduler.fair.allocation.file                          | Path to allocation file. An allocation file is an XML manifest describing queues and their properties, in addition to certain policy defaults. This file must be in the XML format described in the next section. If a relative path is given, the file is searched for on the classpath (which typically includes the Hadoop conf directory). Defaults to fair-scheduler.xml. |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| yarn.scheduler.fair.user-as-default-queue                    | Whether to use the username associated with the allocation as the default queue name, in the event that a queue name is not specified. If this is set to “false” or unset, all jobs have a shared default queue, named “default”. Defaults to true. If a queue placement policy is given in the allocations file, this property is ignored. |
| yarn.scheduler.fair.preemption                               | Whether to use preemption. Defaults to false.                |
| yarn.scheduler.fair.preemption.cluster-utilization-threshold | The utilization threshold after which preemption kicks in. The utilization is computed as the maximum ratio of usage to capacity among all resources. Defaults to 0.8f. |
| yarn.scheduler.fair.sizebasedweight                          | Whether to assign shares to individual apps based on their size, rather than providing an equal share to all apps regardless of size. When set to true, apps are weighted by the natural logarithm of one plus the app’s total requested memory, divided by the natural logarithm of 2. Defaults to false. |
| yarn.scheduler.fair.assignmultiple                           | Whether to allow multiple container assignments in one heartbeat. Defaults to false. |
| yarn.scheduler.fair.max.assign                               | If assignmultiple is true, the maximum amount of containers that can be assigned in one heartbeat. Defaults to -1, which sets no limit. |
| yarn.scheduler.fair.locality.threshold.node                  | For applications that request containers on particular nodes, the number of scheduling opportunities since the last container assignment to wait before accepting a placement on another node. Expressed as a float between 0 and 1, which, as a fraction of the cluster size, is the number of scheduling opportunities to pass up. The default value of -1.0 means don’t pass up any scheduling opportunities. |
| yarn.scheduler.fair.locality.threshold.rack                  | For applications that request containers on particular racks, the number of scheduling opportunities since the last container assignment to wait before accepting a placement on another rack. Expressed as a float between 0 and 1, which, as a fraction of the cluster size, is the number of scheduling opportunities to pass up. The default value of -1.0 means don’t pass up any scheduling opportunities. |
| yarn.scheduler.fair.allow-undeclared-pools                   | If this is true, new queues can be created at application submission time, whether because they are specified as the application’s queue by the submitter or because they are placed there by the user-as-default-queue property. If this is false, any time an app would be placed in a queue that is not specified in the allocations file, it is placed in the “default” queue instead. Defaults to true. If a queue placement policy is given in the allocations file, this property is ignored. |

 

 

 

另外还可以制定一个allocation file来描述application queue

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps24.jpg) 

 

 

 

## **7.7 yarn应用程序开发（仅做了解，通常不需要应用开发人员来做）**

开发要点：参考文档《Yarn上的application开发规程》

Distributed-shell源码解读

 

# **8. zookeeper**

## **8.1 hadoop-spof问题及HA解决思路**

引入集群协调服务框架的必要性

## **8.2 zookeeper简介**

ZooKeeper是一个分布式应用程序协调服务，分布式应用程序可以基于它实现同步服务，配置维护和命名服务等。

目前zookeeper被广泛应用于hadoop生态体系中各种框架的分布式协调，我们也可以利用zookeeper来简化分布式应用开发

 

Zookeeper可以实现的分布式协调服务包括：

统一名称服务

配置管理

分布式锁

集群节点状态协调（负载均衡/主从协调）

 

## **8.3 zookeeper集群搭建**

（1）zookeeper集群组件：

同一个zookeeper服务下的server有三种，一种是leader server，另一种是follower server，还有一种叫observer server；

leader特殊之处在于它有决定权，具有Request Processor

（observer server 与follower server的区别就在于不参与leader选举）

 

（2）部署模式：

单节点

分布式（伪分布式）

 

（3）配置文件： 

​	3.1添加一个zoo.cfg配置文件	$ZOOKEEPER/conf	mv zoo_sample.cfg zoo.cfg		3.2修改配置文件（zoo.cfg）		dataDir=/itcast/zookeeper-3.4.5/data				server.1=itcast05:2888:3888		server.2=itcast06:2888:3888		server.3=itcast07:2888:3888		3.3在（dataDir=/itcast/zookeeper-3.4.5/data）创建一个myid文件，里面内容是server.N中的N（server.2里面内容为2）		echo "1" > myid		3.4将配置好的zk拷贝到其他节点		scp -r /itcast/zookeeper-3.4.5/ itcast06:/itcast/		scp -r /itcast/zookeeper-3.4.5/ itcast07:/itcast/		3.5注意：在其他节点上一定要修改myid的内容		在itcast06应该讲myid的内容改为2 （echo "6" > myid）		在itcast07应该讲myid的内容改为3 （echo "7" > myid）		4.启动集群	分别启动zk		./zkServer.sh start

 

 

## **8.4 zookeeper演示测试**

服务启动

bin/zkServer.sh status获取节点角色状态

服务状态详细信息查看(四字命令)：四字命令可以获取更多信息

Zookeeper支持一下四字节命令来进行交互，查询状态信息等；可以用telnet/nc

来发送命令，如：

echo ruok | nc server01 2181

echo conf | nc server01 2181

 

 

| conf | 输出相关服务配置的详细信息。                                 |
| ---- | ------------------------------------------------------------ |
| cons | 列出所有连接到服务器的客户端的完全的连接 / 会话的详细信息。包括“接受 / 发送”的包数量、会话 id 、操作延迟、最后的操作执行等等信息。 |
| dump | 列出未经处理的会话和临时节点。                               |
| envi | 输出关于服务环境的详细信息（区别于 conf 命令）。             |
| reqs | 列出未经处理的请求                                           |
| ruok | 测试服务是否处于正确状态。如果确实如此，那么服务返回“imok ”，否则不做任何相应。 |
| stat | 输出关于性能和连接的客户端的列表。                           |
| wchs | 列出服务器 watch 的详细信息。                                |
| wchc | 通过 session 列出服务器 watch 的详细信息，它的输出是一个与watch 相关的会话的列表。 |
| wchp | 通过路径列出服务器 watch 的详细信息。它输出一个与 session相关的路径。 |

 

shell客户端操作

bin/zkCli.sh -server server01 2181

操作命令：

​        connect host:port

​        get path [watch]

​        ls path [watch]

​        set path data [version]

​        rmr path

​        delquota [-n|-b] path

​        quit 

​        printwatches on|off

​        create [-s] [-e] path data acl

​        stat path [watch]

​        close 

​        ls2 path [watch]

​        history 

​        listquota path

​        setAcl path acl

​        getAcl path

​        sync path

​        redo cmdno

​        addauth scheme auth

​        delete path [version]

​        setquota -n|-b val path

 

ü **ZooKeeper数据模型和层次命名空间**

提供的命名空间与标准的文件系统非常相似。一个名称是由通过斜线分隔开的路径名序列所组成的。ZooKeeper中的每一个节点是都通过路径来识别。如图： 

​         ![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps25.jpg)

 

 

 

ü **ZooKeeper中的数据节点：**

每一个节点称为znode，通过路径来访问

每一个znode维护着：数据、stat数据结构（ACL、时间戳及版本号）

znode维护的数据主要是用于存储协调的数据，如状态、配置、位置等信息，每个节点存储的数据量很小，KB级别

znode的数据更新后，版本号等控制信息也会更新（增加）

znode还具有原子性操作的特点：写--全部替换，读--全部

znode有永久节点和临时节点之分：临时节点指创建它的session一结束，该节点即被zookeeper删除；

 

ü **zk性能****:**

Zookeeper 的读写速度非常快（基于内存数据库），并且读的速度要比写的速度更快。

顺序一致性：客户端的更新顺序与它们被发送的顺序相一致。

原子性：更新操作要么成功要么失败，没有第三种结果。

单系统镜像：无论客户端连接到哪一个服务器，客户端将看到相同的 ZooKeeper 视图。

可靠性：一旦一个更新操作被应用，那么在客户端再次更新它之前，它的值将不会改变。这个保证将会产生下面两种结果：

1 ．如果客户端成功地获得了正确的返回代码，那么说明更新已经成功。如果不能够获得返回代码（由于通信错误、超时等等），那么客户端将不知道更新操作是否生效。

2 ．当从故障恢复的时候，任何客户端能够看到的执行成功的更新操作将不会被回滚。

实时性：在特定的一段时间内，客户端看到的系统需要被保证是实时的。在此时间段内，任何系统的改变将被客户端看到，或者被客户端侦测到。

给予这些一致性保证， ZooKeeper 更高级功能的设计与实现将会变得非常容易，例如： leader 选举、队列以及可撤销锁等机制的实现。

 

 

## **8.5 zookeeper-api应用**

### **8.5.1 基本使用**

 org.apache.zookeeper.Zookeeper是客户端入口主类，负责建立与server的会话

它提供了表 1 所示几类主要方法  ：

| 功能         | 描述                                |
| ------------ | ----------------------------------- |
| create       | 在本地目录树中创建一个节点          |
| delete       | 删除一个节点                        |
| exists       | 测试本地是否存在目标节点            |
| get/set data | 从目标节点上读取 / 写数据           |
| get/set ACL  | 获取 / 设置目标节点访问控制列表信息 |
| get children | 检索一个子节点上的列表              |
| sync         | 等待要被传送的数据                  |

  表 1 ： ZooKeeper API 描述

 

 

### **8.5.2 demo增删改查**

 

public class SimpleDemo {	// 会话超时时间，设置为与系统默认时间一致	private static final int SESSION_TIMEOUT = 30000;	// 创建 ZooKeeper 实例	ZooKeeper zk;	// 创建 Watcher 实例	Watcher wh = new Watcher() {		public void process(org.apache.zookeeper.WatchedEvent event)		{			System.out.println(event.toString());		}	};	// 初始化 ZooKeeper 实例	private void createZKInstance() throws IOException	{		zk = new ZooKeeper("weekend01:2181", SimpleDemo.SESSION_TIMEOUT, this.wh);	}	private void ZKOperations() throws IOException, InterruptedException, KeeperException	{		System.out.println("/n1. 创建 ZooKeeper 节点 (znode ： zoo2, 数据： myData2 ，权限： OPEN_ACL_UNSAFE ，节点类型： Persistent");		zk.create("/zoo2", "myData2".getBytes(), Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);		System.out.println("/n2. 查看是否创建成功： ");		System.out.println(new String(zk.getData("/zoo2", false, null)));		System.out.println("/n3. 修改节点数据 ");		zk.setData("/zoo2", "shenlan211314".getBytes(), -1);		System.out.println("/n4. 查看是否修改成功： ");		System.out.println(new String(zk.getData("/zoo2", false, null)));		System.out.println("/n5. 删除节点 ");		zk.delete("/zoo2", -1);		System.out.println("/n6. 查看节点是否被删除： ");		System.out.println(" 节点状态： [" + zk.exists("/zoo2", false) + "]");	}	private void ZKClose() throws InterruptedException	{		zk.close();	}	public static void main(String[] args) throws IOException, InterruptedException, KeeperException {		SimpleDemo dm = new SimpleDemo();		dm.createZKInstance();		dm.ZKOperations();		dm.ZKClose();	}}

 

 

 

## 8.6  zookeeper应用案例（分布式应用HA||分布式锁）

（1）实现分布式应用的主节点HA及客户端动态更新主节点状态

A、客户端实现

public class AppClient {	private String groupNode = "sgroup";	private ZooKeeper zk;	private Stat stat = new Stat();	private volatile List<String> serverList; 	/**	 * 连接zookeeper	 */	public void connectZookeeper() throws Exception {		zk = new ZooKeeper("localhost:4180,localhost:4181,localhost:4182", 5000, new Watcher() {			public void process(WatchedEvent event) {				// 如果发生了"/sgroup"节点下的子节点变化事件, 更新server列表, 并重新注册监听				if (event.getType() == EventType.NodeChildrenChanged 					&& ("/" + groupNode).equals(event.getPath())) {					try {						updateServerList();					} catch (Exception e) {						e.printStackTrace();					}				}			}		}); 		updateServerList();	} 	/**	 * 更新server列表	 */	private void updateServerList() throws Exception {		List<String> newServerList = new ArrayList<String>(); 		// 获取并监听groupNode的子节点变化		// watch参数为true, 表示监听子节点变化事件. 		// 每次都需要重新注册监听, 因为一次注册, 只能监听一次事件, 如果还想继续保持监听, 必须重新注册		List<String> subList = zk.getChildren("/" + groupNode, true);		for (String subNode : subList) {			// 获取每个子节点下关联的server地址			byte[] data = zk.getData("/" + groupNode + "/" + subNode, false, stat);			newServerList.add(new String(data, "utf-8"));		} 		// 替换server列表		serverList = newServerList; 		System.out.println("server list updated: " + serverList);	} 	/**	 * client的工作逻辑写在这个方法中	 * 此处不做任何处理, 只让client sleep	 */	public void handle() throws InterruptedException {		Thread.sleep(Long.MAX_VALUE);	} 	public static void main(String[] args) throws Exception {		AppClient ac = new AppClient();		ac.connectZookeeper(); 		ac.handle();	}}

 

 

 

B、服务器端实现

public class AppServer {	private String groupNode = "sgroup";	private String subNode = "sub"; 	/**	 * 连接zookeeper	 * @param address server的地址	 */	public void connectZookeeper(String address) throws Exception {		ZooKeeper zk = new ZooKeeper("localhost:4180,localhost:4181,localhost:4182", 5000, new Watcher() {			public void process(WatchedEvent event) {				// 不做处理			}		});		// 在"/sgroup"下创建子节点		// 子节点的类型设置为EPHEMERAL_SEQUENTIAL, 表明这是一个临时节点, 且在子节点的名称后面加上一串数字后缀		// 将server的地址数据关联到新创建的子节点上		String createdPath = zk.create("/" + groupNode + "/" + subNode, address.getBytes("utf-8"), 			Ids.OPEN_ACL_UNSAFE, CreateMode.EPHEMERAL_SEQUENTIAL);		System.out.println("create: " + createdPath);	}		/**	 * server的工作逻辑写在这个方法中	 * 此处不做任何处理, 只让server sleep	 */	public void handle() throws InterruptedException {		Thread.sleep(Long.MAX_VALUE);	}		public static void main(String[] args) throws Exception {		// 在参数中指定server的地址		if (args.length == 0) {			System.err.println("The first argument must be server address");			System.exit(1);		}				AppServer as = new AppServer();		as.connectZookeeper(args[0]);		as.handle();	}}

 

（2）分布式共享锁的简单实现

ü 客户端A

public class DistributedClient {    // 超时时间    private static final int SESSION_TIMEOUT = 5000;    // zookeeper server列表    private String hosts = "localhost:4180,localhost:4181,localhost:4182";    private String groupNode = "locks";    private String subNode = "sub";     private ZooKeeper zk;    // 当前client创建的子节点    private String thisPath;    // 当前client等待的子节点    private String waitPath;     private CountDownLatch latch = new CountDownLatch(1);     /**     * 连接zookeeper     */    public void connectZookeeper() throws Exception {        zk = new ZooKeeper(hosts, SESSION_TIMEOUT, new Watcher() {            public void process(WatchedEvent event) {                try {                    // 连接建立时, 打开latch, 唤醒wait在该latch上的线程                    if (event.getState() == KeeperState.SyncConnected) {                        latch.countDown();                    }                     // 发生了waitPath的删除事件                    if (event.getType() == EventType.NodeDeleted && event.getPath().equals(waitPath)) {                        doSomething();                    }                } catch (Exception e) {                    e.printStackTrace();                }            }        });         // 等待连接建立        latch.await();         // 创建子节点        thisPath = zk.create("/" + groupNode + "/" + subNode, null, Ids.OPEN_ACL_UNSAFE,                CreateMode.EPHEMERAL_SEQUENTIAL);         // wait一小会, 让结果更清晰一些        Thread.sleep(10);         // 注意, 没有必要监听"/locks"的子节点的变化情况        List<String> childrenNodes = zk.getChildren("/" + groupNode, false);         // 列表中只有一个子节点, 那肯定就是thisPath, 说明client获得锁        if (childrenNodes.size() == 1) {            doSomething();        } else {            String thisNode = thisPath.substring(("/" + groupNode + "/").length());            // 排序            Collections.sort(childrenNodes);            int index = childrenNodes.indexOf(thisNode);            if (index == -1) {                // never happened            } else if (index == 0) {                // inddx == 0, 说明thisNode在列表中最小, 当前client获得锁                doSomething();            } else {                // 获得排名比thisPath前1位的节点                this.waitPath = "/" + groupNode + "/" + childrenNodes.get(index - 1);                // 在waitPath上注册监听器, 当waitPath被删除时, zookeeper会回调监听器的process方法                zk.getData(waitPath, true, new Stat());            }        }    }     private void doSomething() throws Exception {        try {            System.out.println("gain lock: " + thisPath);            Thread.sleep(2000);            // do something        } finally {            System.out.println("finished: " + thisPath);            // 将thisPath删除, 监听thisPath的client将获得通知            // 相当于释放锁            zk.delete(this.thisPath, -1);        }    }     public static void main(String[] args) throws Exception {        for (int i = 0; i < 10; i++) {            new Thread() {                public void run() {                    try {                        DistributedClient dl = new DistributedClient();                        dl.connectZookeeper();                    } catch (Exception e) {                        e.printStackTrace();                    }                }            }.start();        }         Thread.sleep(Long.MAX_VALUE);    }}

 

ü 客户端B

public class DistributedClient2 {	// 超时时间	private static final int SESSION_TIMEOUT = 5000;	// zookeeper server列表	private String hosts = "localhost:4180,localhost:4181,localhost:4182";	private String groupNode = "locks";	private String subNode = "sub"; 	private ZooKeeper zk;	// 当前client创建的子节点	private volatile String thisPath; 	private CountDownLatch latch = new CountDownLatch(1); 	/**	 * 连接zookeeper	 */	public void connectZookeeper() throws Exception {		zk = new ZooKeeper(hosts, SESSION_TIMEOUT, new Watcher() {			public void process(WatchedEvent event) {				try {					// 连接建立时, 打开latch, 唤醒wait在该latch上的线程					if (event.getState() == KeeperState.SyncConnected) {						latch.countDown();					} 					// 子节点发生变化					if (event.getType() == EventType.NodeChildrenChanged && event.getPath().equals("/" + groupNode)) {						// thisPath是否是列表中的最小节点						List<String> childrenNodes = zk.getChildren("/" + groupNode, true);						String thisNode = thisPath.substring(("/" + groupNode + "/").length());						// 排序						Collections.sort(childrenNodes);						if (childrenNodes.indexOf(thisNode) == 0) {							doSomething();						}					}				} catch (Exception e) {					e.printStackTrace();				}			}		}); 		// 等待连接建立		latch.await(); 		// 创建子节点		thisPath = zk.create("/" + groupNode + "/" + subNode, null, Ids.OPEN_ACL_UNSAFE,				CreateMode.EPHEMERAL_SEQUENTIAL); 		// wait一小会, 让结果更清晰一些		Thread.sleep(10); 		// 监听子节点的变化		List<String> childrenNodes = zk.getChildren("/" + groupNode, true); 		// 列表中只有一个子节点, 那肯定就是thisPath, 说明client获得锁		if (childrenNodes.size() == 1) {			doSomething();		}	} 	/**	 * 共享资源的访问逻辑写在这个方法中	 */	private void doSomething() throws Exception {		try {			System.out.println("gain lock: " + thisPath);			Thread.sleep(2000);			// do something		} finally {			System.out.println("finished: " + thisPath);			// 将thisPath删除, 监听thisPath的client将获得通知			// 相当于释放锁			zk.delete(this.thisPath, -1);		}	} 	public static void main(String[] args) throws Exception {		for (int i = 0; i < 10; i++) {			new Thread() {				public void run() {					try {						DistributedClient2 dl = new DistributedClient2();						dl.connectZookeeper();					} catch (Exception e) {						e.printStackTrace();					}				}			}.start();		} 		Thread.sleep(Long.MAX_VALUE);	}}

 

 

动手练习

 

 

 

 

 

 

 

 

 

# **9. Hadoop-HA**

（1）hadoop-ha集群运作机制介绍

所谓HA，即高可用（7*24小时不中断服务）

实现高可用最关键的是消除单点故障

hadoop-ha严格来说应该分成各个组件的HA机制

 

（2）HDFS的HA机制

通过双namenode消除单点故障

双namenode协调工作的要点：

​	A、元数据管理方式需要改变：

​	内存中各自保存一份元数据

​	Edits日志只能有一份，只有Active状态的namenode节点可以做写操作

​	两个namenode都可以读取edits

​	共享的edits放在一个共享存储中管理（qjournal和NFS两个主流实现）

​	B、需要一个状态管理功能模块

​	实现了一个zkfailover，常驻在每一个namenode所在的节点

​	每一个zkfailover负责监控自己所在的namenode节点，利用zk进行状态标识

​	当需要进行状态切换时，由zkfailover来负责切换

​	切换时需要防止brain split现象的发生

（3）hadoop-ha配置文件

core-site.xml

​				<configuration>					<!-- 指定hdfs的nameservice为ns1 -->					<property>						<name>fs.defaultFS</name>						<value>hdfs://ns1/</value>					</property>					<!-- 指定hadoop临时目录 -->					<property>						<name>hadoop.tmp.dir</name>						<value>/home/hadoop/app/hadoop-2.4.1/tmp</value>					</property>										<!-- 指定zookeeper地址 -->					<property>						<name>ha.zookeeper.quorum</name>						<value>weekend05:2181,weekend06:2181,weekend07:2181</value>					</property>				</configuration>

 

 

hdfs-site.xml

configuration><!--指定hdfs的nameservice为ns1，需要和core-site.xml中的保持一致 --><property>	<name>dfs.nameservices</name>	<value>ns1</value></property><!-- ns1下面有两个NameNode，分别是nn1，nn2 --><property>	<name>dfs.ha.namenodes.ns1</name>	<value>nn1,nn2</value></property><!-- nn1的RPC通信地址 --><property>	<name>dfs.namenode.rpc-address.ns1.nn1</name>	<value>weekend01:9000</value></property><!-- nn1的http通信地址 --><property>	<name>dfs.namenode.http-address.ns1.nn1</name>	<value>weekend01:50070</value></property><!-- nn2的RPC通信地址 --><property>	<name>dfs.namenode.rpc-address.ns1.nn2</name>	<value>weekend02:9000</value></property><!-- nn2的http通信地址 --><property>	<name>dfs.namenode.http-address.ns1.nn2</name>	<value>weekend02:50070</value></property><!-- 指定NameNode的元数据在JournalNode上的存放位置 --><property>	<name>dfs.namenode.shared.edits.dir</name>	<value>qjournal://weekend05:8485;weekend06:8485;weekend07:8485/ns1</value></property><!-- 指定JournalNode在本地磁盘存放数据的位置 --><property>	<name>dfs.journalnode.edits.dir</name>	<value>/home/hadoop/app/hadoop-2.4.1/journaldata</value></property><!-- 开启NameNode失败自动切换 --><property>	<name>dfs.ha.automatic-failover.enabled</name>	<value>true</value></property><!-- 配置失败自动切换实现方式 --><property>	<name>dfs.client.failover.proxy.provider.ns1</name>	<value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value></property><!-- 配置隔离机制方法，多个机制用换行分割，即每个机制暂用一行--><property>	<name>dfs.ha.fencing.methods</name>	<value>		sshfence		shell(/bin/true)	</value></property><!-- 使用sshfence隔离机制时需要ssh免登陆 --><property>	<name>dfs.ha.fencing.ssh.private-key-files</name>	<value>/home/hadoop/.ssh/id_rsa</value></property><!-- 配置sshfence隔离机制超时时间 --><property>	<name>dfs.ha.fencing.ssh.connect-timeout</name>	<value>30000</value></property>/configuration>

 

 

（4）集群搭建、测试

一些运维知识补充：

Datanode动态上下线

Namenode状态切换管理

数据块的balance

 

（5）HA下hdfs-api变化

客户端需要nameservice的配置信息

其他不变

 

## **9.2 Federation机制、配置**

扩大namenode容量

 

 

## **9.3 CDH介绍，演示**

动手练习（ha集群搭建及测试）

![85.hadoop-HA机制的实现原理](D:\自我提升\视频\bigdata\大数据Hadoop第5章\截图\85.hadoop-HA机制的实现原理.png)

```
hadoop2.0已经发布了稳定版本了，增加了很多特性，比如HDFS HA、YARN等。最新的hadoop-2.4.1又增加了YARN HA

注意：apache提供的hadoop-2.4.1的安装包是在32位操作系统编译的，因为hadoop依赖一些C++的本地库，
所以如果在64位的操作上安装hadoop-2.4.1就需要重新在64操作系统上重新编译
（建议第一次安装用32位的系统，我将编译好的64位的也上传到群共享里了，如果有兴趣的可以自己编译一下）

前期准备就不详细说了，课堂上都介绍了
1.修改Linux主机名
2.修改IP
3.修改主机名和IP的映射关系 /etc/hosts
	######注意######如果你们公司是租用的服务器或是使用的云主机（如华为用主机、阿里云主机等）
	/etc/hosts里面要配置的是内网IP地址和主机名的映射关系	
4.关闭防火墙
5.ssh免登陆
6.安装JDK，配置环境变量等

集群规划：
	主机名		IP				安装的软件					运行的进程
	hdp-ha-01	192.168.2.31	jdk、hadoop					NameNode、DFSZKFailoverController(zkfc)
	hdp-ha-02	192.168.2.32	jdk、hadoop					NameNode、DFSZKFailoverController(zkfc)
	hdp-ha-03	192.168.2.33	jdk、hadoop					ResourceManager
	hdp-ha-04	192.168.2.34	jdk、hadoop					ResourceManager
	hdp-ha-05	192.168.2.35	jdk、hadoop、zookeeper		DataNode、NodeManager、JournalNode、QuorumPeerMain
	hdp-ha-06	192.168.2.36	jdk、hadoop、zookeeper		DataNode、NodeManager、JournalNode、QuorumPeerMain
	hdp-ha-07	192.168.2.37	jdk、hadoop、zookeeper		DataNode、NodeManager、JournalNode、QuorumPeerMain
	
说明：
	1.在hadoop2.0中通常由两个NameNode组成，一个处于active状态，另一个处于standby状态。Active NameNode对外提供服务，而Standby NameNode则不对外提供服务，仅同步active namenode的状态，以便能够在它失败时快速进行切换。
	hadoop2.0官方提供了两种HDFS HA的解决方案，一种是NFS，另一种是QJM。这里我们使用简单的QJM。在该方案中，主备NameNode之间通过一组JournalNode同步元数据信息，一条数据只要成功写入多数JournalNode即认为写入成功。通常配置奇数个JournalNode
	这里还配置了一个zookeeper集群，用于ZKFC（DFSZKFailoverController）故障转移，当Active NameNode挂掉了，会自动切换Standby NameNode为standby状态
	2.hadoop-2.2.0中依然存在一个问题，就是ResourceManager只有一个，存在单点故障，hadoop-2.4.1解决了这个问题，有两个ResourceManager，一个是Active，一个是Standby，状态由zookeeper进行协调
安装步骤：
	1.安装配置zooekeeper集群（在hdp-ha-05上）
		1.1解压
			tar -zxvf zookeeper-3.4.5.tar.gz -C /root/app/
		1.2修改配置
			cd /root/app/zookeeper-3.4.5/conf/
			cp zoo_sample.cfg zoo.cfg
			vim zoo.cfg
			修改：dataDir=/root/app/zookeeper-3.4.5/tmp
			在最后添加：
			server.1=hdp-ha-05:2888:3888
			server.2=hdp-ha-06:2888:3888
			server.3=hdp-ha-07:2888:3888
			保存退出
			然后创建一个tmp文件夹
			mkdir /root/app/zookeeper-3.4.5/tmp
			echo 1 > /root/app/zookeeper-3.4.5/tmp/myid
		1.3将配置好的zookeeper拷贝到其他节点(首先分别在hdp-ha-06、hdp-ha-07根目录下创建一个hdp-ha-目录：mkdir /hdp-ha-)
			scp -r /root/app/zookeeper-3.4.5/ hdp-ha-06:/root/app/
			scp -r /root/app/zookeeper-3.4.5/ hdp-ha-07:/root/app/
			
			注意：修改hdp-ha-06、hdp-ha-07对应/hdp-ha-/zookeeper-3.4.5/tmp/myid内容
			hdp-ha-06：
				echo 2 > /root/app/zookeeper-3.4.5/tmp/myid
			hdp-ha-07：
				echo 3 > /root/app/zookeeper-3.4.5/tmp/myid
	
	2.安装配置hadoop集群（在hdp-ha-01上操作）
		2.1解压
			tar -zxvf hadoop-2.4.1.tar.gz -C /root/app/
		2.2配置HDFS（hadoop2.0所有的配置文件都在$HADOOP_HOME/etc/hadoop目录下）
			#将hadoop添加到环境变量中
			vim /etc/profile
			export JAVA_HOME=/root/app/jdk1.7.0_55
			export HADOOP_HOME=/hdp-ha-/hadoop-2.4.1
			export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin
			
			#hadoop2.0的配置文件全部在$HADOOP_HOME/etc/hadoop下
			cd /root/app/hadoop-2.4.1/etc/hadoop
			
			2.2.1修改hadoo-env.sh
				export JAVA_HOME=/root/app/jdk1.7.0_55
				
			2.2.2修改core-site.xml
				<configuration>
					<!-- 指定hdfs的nameservice为ns1 -->
					<property>
						<name>fs.defaultFS</name>
						<value>hdfs://ns1/</value>
					</property>
					<!-- 指定hadoop临时目录 -->
					<property>
						<name>hadoop.tmp.dir</name>
						<value>/root/app/hadoop-2.4.1/tmp</value>
					</property>
					
					<!-- 指定zookeeper地址 -->
					<property>
						<name>ha.zookeeper.quorum</name>
						<value>hdp-ha-05:2181,hdp-ha-06:2181,hdp-ha-07:2181</value>
					</property>
				</configuration>
				
			2.2.3修改hdfs-site.xml
				<configuration>
					<!--指定hdfs的nameservice为ns1，需要和core-site.xml中的保持一致 -->
					<property>
						<name>dfs.nameservices</name>
						<value>ns1</value>
					</property>
					<!-- ns1下面有两个NameNode，分别是nn1，nn2 -->
					<property>
						<name>dfs.ha.namenodes.ns1</name>
						<value>nn1,nn2</value>
					</property>
					<!-- nn1的RPC通信地址 -->
					<property>
						<name>dfs.namenode.rpc-address.ns1.nn1</name>
						<value>hdp-ha-01:9000</value>
					</property>
					<!-- nn1的http通信地址 -->
					<property>
						<name>dfs.namenode.http-address.ns1.nn1</name>
						<value>hdp-ha-01:50070</value>
					</property>
					<!-- nn2的RPC通信地址 -->
					<property>
						<name>dfs.namenode.rpc-address.ns1.nn2</name>
						<value>hdp-ha-02:9000</value>
					</property>
					<!-- nn2的http通信地址 -->
					<property>
						<name>dfs.namenode.http-address.ns1.nn2</name>
						<value>hdp-ha-02:50070</value>
					</property>
					<!-- 指定NameNode的元数据在JournalNode上的存放位置 -->
					<property>
						<name>dfs.namenode.shared.edits.dir</name>
						<value>qjournal://hdp-ha-05:8485;hdp-ha-06:8485;hdp-ha-07:8485/ns1</value>
					</property>
					<!-- 指定JournalNode在本地磁盘存放数据的位置 -->
					<property>
						<name>dfs.journalnode.edits.dir</name>
						<value>/root/app/hadoop-2.4.1/journaldata</value>
					</property>
					<!-- 开启NameNode失败自动切换 -->
					<property>
						<name>dfs.ha.automatic-failover.enabled</name>
						<value>true</value>
					</property>
					<!-- 配置失败自动切换实现方式 -->
					<property>
						<name>dfs.client.failover.proxy.provider.ns1</name>
						<value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value>
					</property>
					<!-- 配置隔离机制方法，多个机制用换行分割，即每个机制暂用一行-->
					<property>
						<name>dfs.ha.fencing.methods</name>
						<value>
							sshfence
							shell(/bin/true)
						</value>
					</property>
					<!-- 使用sshfence隔离机制时需要ssh免登陆 -->
					<property>
						<name>dfs.ha.fencing.ssh.private-key-files</name>
						<value>/root/.ssh/id_rsa</value>
					</property>
					<!-- 配置sshfence隔离机制超时时间 -->
					<property>
						<name>dfs.ha.fencing.ssh.connect-timeout</name>
						<value>30000</value>
					</property>
				</configuration>
			
			2.2.4修改mapred-site.xml
				<configuration>
					<!-- 指定mr框架为yarn方式 -->
					<property>
						<name>mapreduce.framework.name</name>
						<value>yarn</value>
					</property>
				</configuration>	
			
			2.2.5修改yarn-site.xml
				<configuration>
						<!-- 开启RM高可用 -->
						<property>
						   <name>yarn.resourcemanager.ha.enabled</name>
						   <value>true</value>
						</property>
						<!-- 指定RM的cluster id -->
						<property>
						   <name>yarn.resourcemanager.cluster-id</name>
						   <value>yrc</value>
						</property>
						<!-- 指定RM的名字 -->
						<property>
						   <name>yarn.resourcemanager.ha.rm-ids</name>
						   <value>rm1,rm2</value>
						</property>
						<!-- 分别指定RM的地址 -->
						<property>
						   <name>yarn.resourcemanager.hostname.rm1</name>
						   <value>hdp-ha-03</value>
						</property>
						<property>
						   <name>yarn.resourcemanager.hostname.rm2</name>
						   <value>hdp-ha-04</value>
						</property>
						<!-- 指定zk集群地址 -->
						<property>
						   <name>yarn.resourcemanager.zk-address</name>
						   <value>hdp-ha-05:2181,hdp-ha-06:2181,hdp-ha-07:2181</value>
						</property>
						<property>
						   <name>yarn.nodemanager.aux-services</name>
						   <value>mapreduce_shuffle</value>
						</property>
				</configuration>
			
				
			2.2.6修改slaves(slaves是指定子节点的位置，因为要在hdp-ha-01上启动HDFS、在hdp-ha-03启动yarn，所以hdp-ha-01上的slaves文件指定的是datanode的位置，hdp-ha-03上的slaves文件指定的是nodemanager的位置)
				hdp-ha-05
				hdp-ha-06
				hdp-ha-07

			2.2.7配置免密码登陆
				#首先要配置hdp-ha-01到hdp-ha-02、hdp-ha-03、hdp-ha-04、hdp-ha-05、hdp-ha-06、hdp-ha-07的免密码登陆
				#在hdp-ha-01上生产一对钥匙
				ssh-keygen -t rsa
				#将公钥拷贝到其他节点，包括自己
				ssh-coyp-id hdp-ha-01
				ssh-coyp-id hdp-ha-02
				ssh-coyp-id hdp-ha-03
				ssh-coyp-id hdp-ha-04
				ssh-coyp-id hdp-ha-05
				ssh-coyp-id hdp-ha-06
				ssh-coyp-id hdp-ha-07
				#配置hdp-ha-03到hdp-ha-04、hdp-ha-05、hdp-ha-06、hdp-ha-07的免密码登陆
				#在hdp-ha-03上生产一对钥匙
				ssh-keygen -t rsa
				#将公钥拷贝到其他节点
				ssh-coyp-id hdp-ha-04
				ssh-coyp-id hdp-ha-05
				ssh-coyp-id hdp-ha-06
				ssh-coyp-id hdp-ha-07
				#注意：两个namenode之间要配置ssh免密码登陆，别忘了配置hdp-ha-02到hdp-ha-01的免登陆
				在hdp-ha-02上生产一对钥匙
				ssh-keygen -t rsa
				ssh-coyp-id -i hdp-ha-01				
		
		2.4将配置好的hadoop拷贝到其他节点
			scp -r /hdp-ha-/ hdp-ha-02:/
			scp -r /hdp-ha-/ hdp-ha-03:/
			scp -r /hdp-ha-/hadoop-2.4.1/ hadoop@hdp-ha-04:/hdp-ha-/
			scp -r /hdp-ha-/hadoop-2.4.1/ hadoop@hdp-ha-05:/hdp-ha-/
			scp -r /hdp-ha-/hadoop-2.4.1/ hadoop@hdp-ha-06:/hdp-ha-/
			scp -r /hdp-ha-/hadoop-2.4.1/ hadoop@hdp-ha-07:/hdp-ha-/
		###注意：严格按照下面的步骤
		2.5启动zookeeper集群（分别在hdp-ha-05、hdp-ha-06、tcast07上启动zk）
			cd /hdp-ha-/zookeeper-3.4.5/bin/
			./zkServer.sh start
			#查看状态：一个leader，两个follower
			./zkServer.sh status
			
		2.6启动journalnode（分别在在hdp-ha-05、hdp-ha-06、hdp-ha-07上执行）
			cd /hdp-ha-/hadoop-2.4.1
			sbin/hadoop-daemon.sh start journalnode
			#运行jps命令检验，hdp-ha-05、hdp-ha-06、hdp-ha-07上多了JournalNode进程
		
		2.7格式化HDFS
			#在hdp-ha-01上执行命令:
			hdfs namenode -format
			#格式化后会在根据core-site.xml中的hadoop.tmp.dir配置生成个文件，这里我配置的是/hdp-ha-/hadoop-2.4.1/tmp，然后将/hdp-ha-/hadoop-2.4.1/tmp拷贝到hdp-ha-02的/hdp-ha-/hadoop-2.4.1/下。
			scp -r tmp/ hdp-ha-02:/root/app/hadoop-2.4.1/
			##也可以这样，建议hdfs namenode -bootstrapStandby
		
		2.8格式化ZKFC(在hdp-ha-01上执行即可)
			hdfs zkfc -formatZK
		
		2.9启动HDFS(在hdp-ha-01上执行)
			sbin/start-dfs.sh

		2.10启动YARN(#####注意#####：是在hdp-ha-03上执行start-yarn.sh，把namenode和resourcemanager分开是因为性能问题，因为他们都要占用大量资源，所以把他们分开了，他们分开了就要分别在不同的机器上启动)
			sbin/start-yarn.sh

		
	到此，hadoop-2.4.1配置完毕，可以统计浏览器访问:
		http://192.168.1.201:50070
		NameNode 'hdp-ha-01:9000' (active)
		http://192.168.1.202:50070
		NameNode 'hdp-ha-02:9000' (standby)
	
	验证HDFS HA
		首先向hdfs上传一个文件
		hadoop fs -put /etc/profile /profile
		hadoop fs -ls /
		然后再kill掉active的NameNode
		kill -9 <pid of NN>
		通过浏览器访问：http://192.168.1.202:50070
		NameNode 'hdp-ha-02:9000' (active)
		这个时候hdp-ha-02上的NameNode变成了active
		在执行命令：
		hadoop fs -ls /
		-rw-r--r--   3 root supergroup       1926 2014-02-06 15:36 /profile
		刚才上传的文件依然存在！！！
		手动启动那个挂掉的NameNode
		sbin/hadoop-daemon.sh start namenode
		通过浏览器访问：http://192.168.1.201:50070
		NameNode 'hdp-ha-01:9000' (standby)
	
	验证YARN：
		运行一下hadoop提供的demo中的WordCount程序：
		hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.4.1.jar wordcount /profile /out
	
	OK，大功告成！！！

	
			
		
测试集群工作状态的一些指令 ：
bin/hdfs dfsadmin -report	 查看hdfs的各节点状态信息

bin/hdfs haadmin -getServiceState nn1		 获取一个namenode节点的HA状态

sbin/hadoop-daemon.sh start namenode  单独启动一个namenode进程

./hadoop-daemon.sh start zkfc   单独启动一个zkfc进程	
		
```

 

# **10. Hbase基础**

## **10.1 hbase数据库介绍**

hbase是建立的hdfs之上，提供高可靠性、高性能、列存储、可伸缩、实时读写的数据库系统。

它介于nosql和RDBMS之间，仅能通过主键(row key)和主键的range来检索数据，仅支持单行事务(可通过hive支持来实现多表join等复杂操作)。主要用来存储非结构化和半结构化的松散数据。

与hadoop一样，Hbase目标主要依靠横向扩展，通过不断增加廉价的商用服务器，来增加计算和存储能力。

 

hbase表结构

HBase中的表一般有这样的特点：

1 大：一个表可以有上10亿行，上100万列

2 面向列:面向列(族)的存储和权限控制，列(族)独立检索。

3 稀疏:对于为空(null)的列，并不占用存储空间，因此，表可以设计的非常稀疏。

二、 逻辑视图

 

HBase以表的形式存储数据。表有行和列组成。列划分为若干个列族(row family)

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps26.jpg) 

Row Key

与nosql数据库们一样,row key是用来检索记录的主键。访问hbase table中的行，只有三种方式：

1 通过单个row key访问

2 通过row key的range

3 全表扫描

Row key行键 (Row key)可以是任意字符串(最大长度是 64KB，实际应用中长度一般为 10-100bytes)，在hbase内部，row key保存为字节数组。

存储时，数据按照Row key的字典序(byte order)排序存储。设计key时，要充分排序存储这个特性，将经常一起读取的行存储放到一起。(位置相关性)

注意：

字典序对int排序的结果是

1,10,100,11,12,13,14,15,16,17,18,19,2,20,21,…,9,91,92,93,94,95,96,97,98,99。要保持整形的自然序，行键必须用0作左填充。

行的一次读写是原子操作 (不论一次读写多少列)。这个设计决策能够使用户很容易的理解程序在对同一个行进行并发更新操作时的行为。

 

列族

hbase表中的每个列，都归属与某个列族。列族是表的chema的一部分(而列不是)，必须在使用表之前定义。列名都以列族作为前缀。例如courses:history ， courses:math 都属于 courses 这个列族。

访问控制、磁盘和内存的使用统计都是在列族层面进行的。实际应用中，列族上的控制权限能 帮助我们管理不同类型的应用：我们允许一些应用可以添加新的基本数据、一些应用可以读取基本数据并创建继承的列族、一些应用则只允许浏览数据（甚至可能因 为隐私的原因不能浏览所有数据）。

 

时间戳

HBase中通过row和columns确定的为一个存贮单元称为cell。每个 cell都保存着同一份数据的多个版本。版本通过时间戳来索引。时间戳的类型是 64位整型。时间戳可以由hbase(在数据写入时自动 )赋值，此时时间戳是精确到毫秒的当前系统时间。时间戳也可以由客户显式赋值。如果应用程序要避免数据版本冲突，就必须自己生成具有唯一性的时间戳。每个 cell中，不同版本的数据按照时间倒序排序，即最新的数据排在最前面。

为了避免数据存在过多版本造成的的管理 (包括存贮和索引)负担，hbase提供了两种数据版本回收方式。一是保存数据的最后n个版本，二是保存最近一段时间内的版本（比如最近七天）。用户可以针对每个列族进行设置。

 

Cell

由{row key, column( =<family> + <label>), version} 唯一确定的单元。cell中的数据是没有类型的，全部是字节码形式存贮。

 

 

## **10.2 hbase集群结构**

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps27.jpg) 

 

 

 

 

## **10.3 hbase集群搭建**

----先部署一个zookeeper集群

（1）上传hbase安装包

（2）解压

（3）配置hbase集群，要修改3个文件

​	注意：要把hadoop的hdfs-site.xml和core-site.xml 放到hbase/conf下

​	

​	（3.1）修改hbase-env.sh

​	export JAVA_HOME=/usr/java/jdk1.7.0_55	//告诉hbase使用外部的zk	export HBASE_MANAGES_ZK=false

​	

​	（3.2）修改 hbase-site.xml

​	<configuration>		<!-- 指定hbase在HDFS上存储的路径 -->        <property>                <name>hbase.rootdir</name>                <value>hdfs://ns1/hbase</value>        </property>		<!-- 指定hbase是分布式的 -->        <property>                <name>hbase.cluster.distributed</name>                <value>true</value>        </property>		<!-- 指定zk的地址，多个用“,”分割 -->        <property>                <name>hbase.zookeeper.quorum</name>                <value>hdp-server-01:2181, hdp-server-02:2181, hdp-server-03:2181</value>        </property>	</configuration>

 

（3.3）修改 regionservers - 启动hregionserver

​	weekend03	weekend04	weekend05	weekend06

​	

(3.4) 拷贝hbase到其他节点

​		scp -r /weekend/hbase-0.96.2-hadoop2/ weekend02:/weekend/

​		scp -r /weekend/hbase-0.96.2-hadoop2/ weekend03:/weekend/

​		scp -r /weekend/hbase-0.96.2-hadoop2/ weekend04:/weekend/

​		scp -r /weekend/hbase-0.96.2-hadoop2/ weekend05:/weekend/

​		scp -r /weekend/hbase-0.96.2-hadoop2/ weekend06:/weekend/

(4) 将配置好的HBase拷贝到每一个节点并同步时间。

 

(5) 启动所有的hbase进程

​	首先启动zk集群

​		./zkServer.sh start

​	启动hbase集群

​		start-dfs.sh

​	启动hbase，在主节点上运行 - 启动hmaster：

​		start-hbase.sh

(6) 通过浏览器访问hbase管理页面

​	192.168.1.201:60010

(7) 为保证集群的可靠性，要启动多个HMaster

​	hbase-daemon.sh start master

 

 

## **10.4 命令行演示**

### **10.4.1 基本shell命令**

进入hbase命令行./hbase shell 显示hbase中的表list 创建user表，包含info、data两个列族create 'user', 'info1', 'data1'create 'user', {NAME => 'info', VERSIONS => '3'} 向user表中插入信息，row key为rk0001，列族info中添加name列标示符，值为zhangsanput 'user', 'rk0001', 'info:name', 'zhangsan' 向user表中插入信息，row key为rk0001，列族info中添加gender列标示符，值为femaleput 'user', 'rk0001', 'info:gender', 'female' 向user表中插入信息，row key为rk0001，列族info中添加age列标示符，值为20put 'user', 'rk0001', 'info:age', 20 向user表中插入信息，row key为rk0001，列族data中添加pic列标示符，值为pictureput 'user', 'rk0001', 'data:pic', 'picture' 获取user表中row key为rk0001的所有信息get 'user', 'rk0001' 获取user表中row key为rk0001，info列族的所有信息get 'user', 'rk0001', 'info' 获取user表中row key为rk0001，info列族的name、age列标示符的信息get 'user', 'rk0001', 'info:name', 'info:age' 获取user表中row key为rk0001，info、data列族的信息get 'user', 'rk0001', 'info', 'data'get 'user', 'rk0001', {COLUMN => ['info', 'data']} get 'user', 'rk0001', {COLUMN => ['info:name', 'data:pic']} 获取user表中row key为rk0001，列族为info，版本号最新5个的信息get 'user', 'rk0001', {COLUMN => 'info', VERSIONS => 2}get 'user', 'rk0001', {COLUMN => 'info:name', VERSIONS => 5}get 'user', 'rk0001', {COLUMN => 'info:name', VERSIONS => 5, TIMERANGE => [1392368783980, 1392380169184]} 获取user表中row key为rk0001，cell的值为zhangsan的信息get 'people', 'rk0001', {FILTER => "ValueFilter(=, 'binary:图片')"} 获取user表中row key为rk0001，列标示符中含有a的信息get 'people', 'rk0001', {FILTER => "(QualifierFilter(=,'substring:a'))"} put 'user', 'rk0002', 'info:name', 'fanbingbing'put 'user', 'rk0002', 'info:gender', 'female'put 'user', 'rk0002', 'info:nationality', '中国'get 'user', 'rk0002', {FILTER => "ValueFilter(=, 'binary:中国')"}  查询user表中的所有信息scan 'user' 查询user表中列族为info的信息scan 'user', {COLUMNS => 'info'}scan 'user', {COLUMNS => 'info', RAW => true, VERSIONS => 5}scan 'persion', {COLUMNS => 'info', RAW => true, VERSIONS => 3}查询user表中列族为info和data的信息scan 'user', {COLUMNS => ['info', 'data']}scan 'user', {COLUMNS => ['info:name', 'data:pic']}  查询user表中列族为info、列标示符为name的信息scan 'user', {COLUMNS => 'info:name'} 查询user表中列族为info、列标示符为name的信息,并且版本最新的5个scan 'user', {COLUMNS => 'info:name', VERSIONS => 5} 查询user表中列族为info和data且列标示符中含有a字符的信息scan 'user', {COLUMNS => ['info', 'data'], FILTER => "(QualifierFilter(=,'substring:a'))"} 查询user表中列族为info，rk范围是[rk0001, rk0003)的数据scan 'people', {COLUMNS => 'info', STARTROW => 'rk0001', ENDROW => 'rk0003'} 查询user表中row key以rk字符开头的scan 'user',{FILTER=>"PrefixFilter('rk')"} 查询user表中指定范围的数据scan 'user', {TIMERANGE => [1392368783980, 1392380169184]} 删除数据删除user表row key为rk0001，列标示符为info:name的数据delete 'people', 'rk0001', 'info:name'删除user表row key为rk0001，列标示符为info:name，timestamp为1392383705316的数据delete 'user', 'rk0001', 'info:name', 1392383705316  清空user表中的数据truncate 'people'  修改表结构首先停用user表（新版本不用）disable 'user' 添加两个列族f1和f2alter 'people', NAME => 'f1'alter 'user', NAME => 'f2'启用表enable 'user'  ###disable 'user'(新版本不用)删除一个列族：alter 'user', NAME => 'f1', METHOD => 'delete' 或 alter 'user', 'delete' => 'f1' 添加列族f1同时删除列族f2alter 'user', {NAME => 'f1'}, {NAME => 'f2', METHOD => 'delete'} 将user表的f1列族版本号改为5alter 'people', NAME => 'info', VERSIONS => 5启用表enable 'user'  删除表disable 'user'drop 'user'  get 'person', 'rk0001', {FILTER => "ValueFilter(=, 'binary:中国')"}get 'person', 'rk0001', {FILTER => "(QualifierFilter(=,'substring:a'))"}scan 'person', {COLUMNS => 'info:name'}scan 'person', {COLUMNS => ['info', 'data'], FILTER => "(QualifierFilter(=,'substring:a'))"}scan 'person', {COLUMNS => 'info', STARTROW => 'rk0001', ENDROW => 'rk0003'} scan 'person', {COLUMNS => 'info', STARTROW => '20140201', ENDROW => '20140301'}scan 'person', {COLUMNS => 'info:name', TIMERANGE => [1395978233636, 1395987769587]}delete 'person', 'rk0001', 'info:name' alter 'person', NAME => 'ffff'alter 'person', NAME => 'info', VERSIONS => 10  get 'user', 'rk0002', {COLUMN => ['info:name', 'data:pic']}

 

### **10.4.2 建表高级属性**

下面几个shell 命令在后续的hbase 操作中可以起到很到的作用，且主要体现在建表的过程中，看下面几个create 属性

1、BLOOMFILTER  默认是NONE 是否使用布隆过虑 使用何种方式

​     布隆过滤可以每列族单独启用。使用 HColumnDescriptor.setBloomFilterType(NONE | ROW | ROWCOL) 对列族单独启用布隆。 Default = NONE 没有布隆过滤。对 ROW，行键的哈希在每次插入行时将被添加到布隆。对 ROWCOL，行键 + 列族 + 列族修饰的哈希将在每次插入行时添加到布隆

   使用方法: create 'table',{BLOOMFILTER =>'ROW'} 

   启用布隆过滤可以节省必须读磁盘过程，可以有助于改进读取延迟 

2、VERSIONS 默认是3 这个参数的意思是数据保留三个 版本，如果我们认为我们的数据没有这么大的必要保留这么多，随时都在更新，而老版本的数据对我们毫无价值，那将此参数设为1 能节约2/3的空间

​     使用方法: create 'table',{VERSIONS=>'2'}

3、COMPRESSION 默认值是NONE 即不使用压缩

​     这个参数意思是该列族是否采用压缩，采用什么压缩算法

​     使用方法: create 'table',{NAME=>'info',COMPRESSION=>'SNAPPY'} 

​     我建议采用SNAPPY压缩算法，个压缩算法的比较网上比较多，我从网上摘抄一个表格作为参考，具体的snappy 的安装后续会以单独章节进行描述。

​     这个表是Google几年前发布的一组测试数据，实际测试Snappy 和下表所列相差无几。

​    HBase中，在Snappy发布之前（Google 2011年对外发布Snappy），采用的LZO算法，目标是达到尽可能快的压缩和解压速度，同时减少对CPU的消耗；

​    在Snappy发布之后，建议采用Snappy算法（参考《HBase: The Definitive Guide》），具体可以根据实际情况对LZO和Snappy做过更详细的对比测试后再做选择。

​                    

| **Algorithm** | **% remaining** | **Encoding** | **Decoding** |
| ------------- | --------------- | ------------ | ------------ |
| GZIP          | 13.4%           | 21 MB/s      | 118 MB/s     |
| LZO           | 20.5%           | 135 MB/s     | 410 MB/s     |
| Zippy/Snappy  | 22.2%           | 172 MB/s     | 409 MB/s     |

 

  

 

 

 

如果建表之初没有 压缩，后来想要加入压缩算法，怎么办 hbase 有另外的一个命令alter

4、alter 

​     使用方法：

​     如 修改压缩算法      

​      disable 'table'

​      alter 'table',{NAME=>'info',COMPRESSION=>'snappy'} 

​      enable 'table'

​     删除列族

​     disable 'table'

​     alter 'table',{NAME=>'info',METHOD=>'delete'}

​     enable 'table'

​     但是这样修改之后发现表数据还是那么大，并没有发生多大变化。怎么办

​     major_compact 'table' 命令之后 才会做实际的操作。

 

5、TTL 默认是 2147483647 即:Integer.MAX_VALUE 值 大概是68年

​     这个参数是说明该列族数据的 存活时间 也就是数据的生命周期 单位是s 默写文章写的单位是ms　是错误的。

​     这个参数可以根据　具体的需求　对数据设定　存活时间，超过存过时间的数据将在表中不在显示，待下次major compact的时候再彻底删除数据

​     为什么在下次major compact的时候删除数据，后面会具体介绍到。

​     注意的是TTL设定之后 MIN_VERSIONS=>'0' 这样设置之后，TTL时间戳过期后，将全部彻底删除该family 下所有的数据，如果MIN_VERSIONS 不等于0 那将保留最新

​     的MIN_VERSIONS个版本的数据，其它的全部删除，比如MIN_VERSIONS=>'1' 届时将保留一个最新版本的数据，其它版本的数据将不再保存。

6、describe 'table' 这个命令查看了create table 的各项参数 或者是默认值。

7、disable_all 'toplist.*' disable_all 支持正则表达式，并列出当前匹配的表的如下：

​      toplist_a_total_1001                                                                                                                                                 

​      toplist_a_total_1002                                                                                                                                                

​      toplist_a_total_1008                                                                                                                                                

​      toplist_a_total_1009                                                                                                                                                

​      toplist_a_total_1019                                                                                                                                                

​      toplist_a_total_1035

​     ...

​     Disable the above 25 tables (y/n)? 并给出确认提示

8、drop_all 这个命令和disable_all的使用方式是一样的

9、hbase 表预分区 也就是手动分区

​     默认情况下，在创建HBase表的时候会自动创建一个region分区，当导入数据的时候，所有的HBase客户端都向这一个region写数据，直到这个region足够大了才进行切分。一种可以加快批量写入速度的方法是通过预先创建一些空的regions，这样当数据写入HBase时，会按照region分区情况，在集群内做数据的负载均衡。

​     使用方法:create 't1', 'f1', {NUMREGIONS => 15, SPLITALGO => 'HexStringSplit'}

​     也可以使用 api的方式 

​     hbase org.apache.hadoop.hbase.util.RegionSplitter test_table HexStringSplit -c 10 -f info  

​     参数很容易看懂 test_table  是表名 HexStringSplit 是split 方式 -c 是分10个region -f 是family

​     这样就可以将表预先分为10个区，减少数据达到storefile 大小的时候自动分区的时间消耗，并且还有以一个优势，就是合理设计rowkey 能让各个region 的并发请求 平均分配(趋于均匀) 使IO 效率达到最高，但是预分区需要将filesize 设置一个较大的值，设置哪个参数呢 hbase.hregion.max.filesize 这个值默认是10G 也就是说单个region 默认大小是10G

​     这个值发生从0.90 到0.92到0.94.3 从 256M--1G--10G 这个根据自己的需求将这个值修改。

​     但是如果MapReduce Input类型为TableInputFormat 使用hbase作为输入的时候，就要注意了，每个region一个map，如果数据小于10G 那只会启用一个map 造成很大的资源浪费，这时候可以考虑适当调小 该参数的值，或者采用预分配region 的方式，并将hbase.hregion.max.filesize 设为一个相对比较大的值，不容易达到的值比如1000G，检测如果达到这个值，再手动分配region。

 

 前面说到了 compact 为什么设置了TTL 超过存活时间的数据 就消失了，是如何消失的呢？是删除了吗？通过哪些参数删除的。

后面将要说到 hbase compact

 

 

## **10.5 hbase客户端API（基本，过滤器查询）**

10.5.1  基本增删改查java实现

public class HbaseDemo { 	private Configuration conf = null;		@Before	public void init(){		conf = HBaseConfiguration.create();		conf.set("hbase.zookeeper.quorum", "weekend05,weekend06,weekend07");	}		@Test	public void testDrop() throws Exception{		HBaseAdmin admin = new HBaseAdmin(conf);		admin.disableTable("account");		admin.deleteTable("account");		admin.close();	}		@Test	public void testPut() throws Exception{		HTable table = new HTable(conf, "person_info");		Put p = new Put(Bytes.toBytes("person_rk_bj_zhang_000002"));		p.add("base_info".getBytes(), "name".getBytes(), "zhangwuji".getBytes());		table.put(p);		table.close();	}	 	@Test	public void testDel() throws Exception{		HTable table = new HTable(conf, "user");		Delete del = new Delete(Bytes.toBytes("rk0001"));		del.deleteColumn(Bytes.toBytes("data"), Bytes.toBytes("pic"));		table.delete(del);		table.close();	} 	@Test	public void testGet() throws Exception{		HTable table = new HTable(conf, "person_info");		Get get = new Get(Bytes.toBytes("person_rk_bj_zhang_000001"));		get.setMaxVersions(5);		Result result = table.get(get);				List<Cell> cells = result.listCells();			for(Cell c:cells){		}				//result.getValue(family, qualifier);  可以从result中直接取出一个特定的value				//遍历出result中所有的键值对		List<KeyValue> kvs = result.list();		//kv  ---> f1:title:superise....      f1:author:zhangsan    f1:content:asdfasldgkjsldg		for(KeyValue kv : kvs){			String family = new String(kv.getFamily());			System.out.println(family);			String qualifier = new String(kv.getQualifier());			System.out.println(qualifier);			System.out.println(new String(kv.getValue()));					}		table.close();	}

 

 

（2）过滤器查询

​	/**	 * 多种过滤条件的使用方法	 * @throws Exception	 */	@Test	public void testScan() throws Exception{		HTable table = new HTable(conf, "person_info".getBytes());		Scan scan = new Scan(Bytes.toBytes("person_rk_bj_zhang_000001"), Bytes.toBytes("person_rk_bj_zhang_000002"));				//前缀过滤器----针对行键		Filter filter = new PrefixFilter(Bytes.toBytes("rk"));				//行过滤器  ---针对行键		ByteArrayComparable rowComparator = new BinaryComparator(Bytes.toBytes("person_rk_bj_zhang_000001"));		RowFilter rf = new RowFilter(CompareOp.LESS_OR_EQUAL, rowComparator);				/**         * 假设rowkey格式为：创建日期_发布日期_ID_TITLE         * 目标：查找  发布日期  为  2014-12-21  的数据         * sc.textFile("path").flatMap(line=>line.split("\t")).map(x=>(x,1)).reduceByKey(_+_).map((_(2),_(1))).sortByKey().map((_(2),_(1))).saveAsTextFile("")         *          *          */        rf = new RowFilter(CompareOp.EQUAL , new SubstringComparator("_2014-12-21_"));						//单值过滤器 1 完整匹配字节数组		new SingleColumnValueFilter("base_info".getBytes(), "name".getBytes(), CompareOp.EQUAL, "zhangsan".getBytes());		//单值过滤器2 匹配正则表达式		ByteArrayComparable comparator = new RegexStringComparator("zhang.");		new SingleColumnValueFilter("info".getBytes(), "NAME".getBytes(), CompareOp.EQUAL, comparator); 		//单值过滤器3 匹配是否包含子串,大小写不敏感		comparator = new SubstringComparator("wu");		new SingleColumnValueFilter("info".getBytes(), "NAME".getBytes(), CompareOp.EQUAL, comparator); 		//键值对元数据过滤-----family过滤----字节数组完整匹配        FamilyFilter ff = new FamilyFilter(                CompareOp.EQUAL ,                 new BinaryComparator(Bytes.toBytes("base_info"))   //表中不存在inf列族，过滤结果为空                );        //键值对元数据过滤-----family过滤----字节数组前缀匹配        ff = new FamilyFilter(                CompareOp.EQUAL ,                 new BinaryPrefixComparator(Bytes.toBytes("inf"))   //表中存在以inf打头的列族info，过滤结果为该列族所有行                );               //键值对元数据过滤-----qualifier过滤----字节数组完整匹配                filter = new QualifierFilter(                CompareOp.EQUAL ,                 new BinaryComparator(Bytes.toBytes("na"))   //表中不存在na列，过滤结果为空                );        filter = new QualifierFilter(                CompareOp.EQUAL ,                 new BinaryPrefixComparator(Bytes.toBytes("na"))   //表中存在以na打头的列name，过滤结果为所有行的该列数据        		);		        //基于列名(即Qualifier)前缀过滤数据的ColumnPrefixFilter        filter = new ColumnPrefixFilter("na".getBytes());                //基于列名(即Qualifier)多个前缀过滤数据的MultipleColumnPrefixFilter        byte[][] prefixes = new byte[][] {Bytes.toBytes("na"), Bytes.toBytes("me")};        filter = new MultipleColumnPrefixFilter(prefixes);         //为查询设置过滤条件        scan.setFilter(filter);                        		scan.addFamily(Bytes.toBytes("base_info"));		//一行//		Result result = table.get(get);		//多行的数据		ResultScanner scanner = table.getScanner(scan);		for(Result r : scanner){			/**			for(KeyValue kv : r.list()){				String family = new String(kv.getFamily());				System.out.println(family);				String qualifier = new String(kv.getQualifier());				System.out.println(qualifier);				System.out.println(new String(kv.getValue()));			}			*/			//直接从result中取到某个特定的value			byte[] value = r.getValue(Bytes.toBytes("base_info"), Bytes.toBytes("name"));			System.out.println(new String(value));		}		table.close();	}

 

 

## **10.6 hbase工作原理**

### **10.6.1  物理存储**

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps28.png)

 

 

 

 

 

 

 

 

 

 

 

 

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps29.jpg)

1 已经提到过，Table中的所有行都按照row key的字典序排列。

2 Table 在行的方向上分割为多个Hregion。

 

3 region按大小分割的，每个表一开始只有一个region，随着数据不断插入表，region不断增大，当增大到一个阀值的时候，Hregion就会等分会两个新的Hregion。当table中的行不断增多，就会有越来越多的Hregion。

 

4 Hregion是Hbase中分布式存储和负载均衡的最小单元。最小单元就表示不同的Hregion可以分布在不同的HRegion server上。但一个Hregion是不会拆分到多个server上的。

 

5 HRegion虽然是分布式存储的最小单元，但并不是存储的最小单元。

事实上，HRegion由一个或者多个Store组成，每个store保存一个columns family。

每个Strore又由一个memStore和0至多个StoreFile组成。如图：

StoreFile以HFile格式保存在HDFS上。

 

HFile的格式为：

 

Trailer部分的格式:

 

HFile分为六个部分：

Data Block 段–保存表中的数据，这部分可以被压缩

Meta Block 段 (可选的)–保存用户自定义的kv对，可以被压缩。

File Info 段–Hfile的元信息，不被压缩，用户也可以在这一部分添加自己的元信息。

Data Block Index 段–Data Block的索引。每条索引的key是被索引的block的第一条记录的key。

Meta Block Index段 (可选的)–Meta Block的索引。

Trailer–这一段是定长的。保存了每一段的偏移量，读取一个HFile时，会首先 读取Trailer，Trailer保存了每个段的起始位置(段的Magic Number用来做安全check)，然后，DataBlock Index会被读取到内存中，这样，当检索某个key时，不需要扫描整个HFile，而只需从内存中找到key所在的block，通过一次磁盘io将整个 block读取到内存中，再找到需要的key。DataBlock Index采用LRU机制淘汰。

HFile的Data Block，Meta Block通常采用压缩方式存储，压缩之后可以大大减少网络IO和磁盘IO，随之而来的开销当然是需要花费cpu进行压缩和解压缩。

目标Hfile的压缩支持两种方式：Gzip，Lzo。

 

 

Memstore与storefile

一个region由多个store组成，每个store包含一个列族的所有数据

Store包括位于把内存的memstore和位于硬盘的storefile

写操作先写入memstore,当memstore中的数据量达到某个阈值，Hregionserver启动flashcache进程写入storefile,每次写入形成单独一个storefile

当storefile大小超过一定阈值后，会把当前的region分割成两个，并由Hmaster分配奥相应的region服务器，实现负载均衡

客户端检索数据时，先在memstore找，找不到再找storefile

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps30.png)

 

HLog(WAL log)

WAL 意为Write ahead log(http://en.wikipedia.org/wiki/Write-ahead_logging)，类似mysql中的binlog,用来 做灾难恢复只用，Hlog记录数据的所有变更,一旦数据修改，就可以从log中进行恢复。

每个Region Server维护一个Hlog,而不是每个Region一个。这样不同region(来自不同table)的日志会混在一起，这样做的目的是不断追加单个 文件相对于同时写多个文件而言，可以减少磁盘寻址次数，因此可以提高对table的写性能。带来的麻烦是，如果一台region server下线，为了恢复其上的region，需要将region server上的log进行拆分，然后分发到其它region server上进行恢复。

HLog文件就是一个普通的Hadoop Sequence File，Sequence File 的Key是HLogKey对象，HLogKey中记录了写入数据的归属信息，除了table和region名字外，同时还包括 sequence number和timestamp，timestamp是”写入时间”，sequence number的起始值为0，或者是最近一次存入文件系统中sequence number。HLog Sequece File的Value是HBase的KeyValue对象，即对应HFile中的KeyValue，可参见上文描述。

 

 

### **10.6.2  系统架构**

Client

1 包含访问hbase的接口，client维护着一些cache来加快对hbase的访问，比如regione的位置信息。

 

Zookeeper

1 保证任何时候，集群中只有一个master

2 存贮所有Region的寻址入口。

3 实时监控Region Server的状态，将Region server的上线和下线信息实时通知给Master

4 存储Hbase的schema,包括有哪些table，每个table有哪些column family

 

Master

1 为Region server分配region

2 负责region server的负载均衡

3 发现失效的region server并重新分配其上的region

4 GFS上的垃圾文件回收

5 处理schema更新请求

 

Region Server

1 Region server维护Master分配给它的region，处理对这些region的IO请求

2 Region server负责切分在运行过程中变得过大的region

可以看到，client访问hbase上数据的过程并不需要master参与（寻址访问zookeeper和region server，数据读写访问regione server），master仅仅维护者table和region的元数据信息，负载很低。

 

### **10.6.3  寻址机制**

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps31.jpg) 

系统如何找到某个row key (或者某个 row key range)所在的region

bigtable 使用三层类似B+树的结构来保存region位置。

第一层是保存zookeeper里面的文件，它持有root region的位置。

第二层root region是.META.表的第一个region其中保存了.META.z表其它region的位置。通过root region，我们就可以访问.META.表的数据。

.META.是第三层，它是一个特殊的表，保存了hbase中所有数据表的region 位置信息。

 

说明：

1 root region永远不会被split，保证了最需要三次跳转，就能定位到任意region 。

2.META.表每行保存一个region的位置信息，row key 采用表名+表的最后一样编码而成。

3 为了加快访问，.META.表的全部region都保存在内存中。

假设，.META.表的一行在内存中大约占用1KB。并且每个region限制为128MB。

那么上面的三层结构可以保存的region数目为：

(128MB/1KB) * (128MB/1KB) = = 2(34)个region

4 client会将查询过的位置信息保存缓存起来，缓存不会主动失效，因此如果client上的缓存全部失效，则需要进行6次网络来回，才能定位到正确的region(其中三次用来发现缓存失效，另外三次用来获取位置信息)。

 

10.6.4 读写过程

读写过程

上文提到，hbase使用MemStore和StoreFile存储对表的更新。

数据在更新时首先写入Log(WAL log)和内存(MemStore)中，MemStore中的数据是排序的，当MemStore累计到一定阈值时，就会创建一个新的MemStore，并 且将老的MemStore添加到flush队列，由单独的线程flush到磁盘上，成为一个StoreFile。于此同时，系统会在zookeeper中 记录一个redo point，表示这个时刻之前的变更已经持久化了。(minor compact)

当系统出现意外时，可能导致内存(MemStore)中的数据丢失，此时使用Log(WAL log)来恢复checkpoint之后的数据。

前面提到过StoreFile是只读的，一旦创建后就不可以再修改。因此Hbase的更 新其实是不断追加的操作。当一个Store中的StoreFile达到一定的阈值后，就会进行一次合并(major compact),将对同一个key的修改合并到一起，形成一个大的StoreFile，当StoreFile的大小达到一定阈值后，又会对 StoreFile进行split，等分为两个StoreFile。

由于对表的更新是不断追加的，处理读请求时，需要访问Store中全部的 StoreFile和MemStore，将他们的按照row key进行合并，由于StoreFile和MemStore都是经过排序的，并且StoreFile带有内存中索引，合并的过程还是比较快。

写请求处理过程

 

1 client向region server提交写请求

2 region server找到目标region

3 region检查数据是否与schema一致

4 如果客户端没有指定版本，则获取当前系统时间作为数据版本

5 将更新写入WAL log

6 将更新写入Memstore

7 判断Memstore的是否需要flush为Store文件。

 

### **10.6.4  Region管理**

(1) region分配

任何时刻，一个region只能分配给一个region server。master记录了当前有哪些可用的region server。以及当前哪些region分配给了哪些region server，哪些region还没有分配。当存在未分配的region，并且有一个region server上有可用空间时，master就给这个region server发送一个装载请求，把region分配给这个region server。region server得到请求后，就开始对此region提供服务。

 

(2) region server上线

master使用zookeeper来跟踪region server状态。当某个region server启动时，会首先在zookeeper上的server目录下建立代表自己的文件，并获得该文件的独占锁。由于master订阅了server 目录上的变更消息，当server目录下的文件出现新增或删除操作时，master可以得到来自zookeeper的实时通知。因此一旦region server上线，master能马上得到消息。

 

(3)region server下线

当region server下线时，它和zookeeper的会话断开，zookeeper而自动释放代表这台server的文件上的独占锁。而master不断轮询 server目录下文件的锁状态。如果master发现某个region server丢失了它自己的独占锁，(或者master连续几次和region server通信都无法成功),master就是尝试去获取代表这个region server的读写锁，一旦获取成功，就可以确定：

1 region server和zookeeper之间的网络断开了。

2 region server挂了。

的其中一种情况发生了，无论哪种情况，region server都无法继续为它的region提供服务了，此时master会删除server目录下代表这台region server的文件，并将这台region server的region分配给其它还活着的同志。

如果网络短暂出现问题导致region server丢失了它的锁，那么region server重新连接到zookeeper之后，只要代表它的文件还在，它就会不断尝试获取这个文件上的锁，一旦获取到了，就可以继续提供服务。

 

 

### **10.6.5  Master工作机制**

master上线

master启动进行以下步骤:

1 从zookeeper上获取唯一一个代码master的锁，用来阻止其它master成为master。

2 扫描zookeeper上的server目录，获得当前可用的region server列表。

3 和2中的每个region server通信，获得当前已分配的region和region server的对应关系。

4 扫描.META.region的集合，计算得到当前还未分配的region，将他们放入待分配region列表。

 

master下线

由于master只维护表和region的元数据，而不参与表数据IO的过 程，master下线仅导致所有元数据的修改被冻结(无法创建删除表，无法修改表的schema，无法进行region的负载均衡，无法处理region 上下线，无法进行region的合并，唯一例外的是region的split可以正常进行，因为只有region server参与)，表的数据读写还可以正常进行。因此master下线短时间内对整个hbase集群没有影响。从上线过程可以看到，master保存的 信息全是可以冗余信息（都可以从系统其它地方收集到或者计算出来），因此，一般hbase集群中总是有一个master在提供服务，还有一个以上 的’master’在等待时机抢占它的位置。

 

 

 

动手练习（增删改查）

 

# **11.  Hbase高级应用**

## **11.1 hbase应用案例看行键设计**

表结构设计

列族高级配置--数据块/缓存、布隆过滤器、生存时间、压缩

Hbase行键设计

 

## **11.2 Hbase和mapreduce结合**

### **11.2.1 从Hbase中读取数据写入hdfs**

/**public abstract class TableMapper<KEYOUT, VALUEOUT>extends Mapper<ImmutableBytesWritable, Result, KEYOUT, VALUEOUT> {} * @author duanhaitao@itcast.cn * */public class HbaseReader { 	public static String flow_fields_import = "flow_fields_import";	static class HdfsSinkMapper extends TableMapper<Text, NullWritable>{ 		@Override		protected void map(ImmutableBytesWritable key, Result value, Context context) throws IOException, InterruptedException { 			byte[] bytes = key.copyBytes();			String phone = new String(bytes);			byte[] urlbytes = value.getValue("f1".getBytes(), "url".getBytes());			String url = new String(urlbytes);			context.write(new Text(phone + "\t" + url), NullWritable.get());					}			}		static class HdfsSinkReducer extends Reducer<Text, NullWritable, Text, NullWritable>{				@Override		protected void reduce(Text key, Iterable<NullWritable> values, Context context) throws IOException, InterruptedException {						context.write(key, NullWritable.get());		}	}		public static void main(String[] args) throws Exception {		Configuration conf = HBaseConfiguration.create();		conf.set("hbase.zookeeper.quorum", "spark01");				Job job = Job.getInstance(conf);				job.setJarByClass(HbaseReader.class);		//		job.setMapperClass(HdfsSinkMapper.class);		Scan scan = new Scan();		TableMapReduceUtil.initTableMapperJob(flow_fields_import, scan, HdfsSinkMapper.class, Text.class, NullWritable.class, job);		job.setReducerClass(HdfsSinkReducer.class);				FileOutputFormat.setOutputPath(job, new Path("c:/hbasetest/output"));				job.setOutputKeyClass(Text.class);		job.setOutputValueClass(NullWritable.class);				job.waitForCompletion(true);					}	}

 

 

 

 

 

 

### **11.2.2 从Hbase中读取数据写入hdfs**

/**public abstract class TableReducer<KEYIN, VALUEIN, KEYOUT>extends Reducer<KEYIN, VALUEIN, KEYOUT, Writable> {} * @author duanhaitao@itcast.cn * */public class HbaseSinker { 	public static String flow_fields_import = "flow_fields_import";	static class HbaseSinkMrMapper extends Mapper<LongWritable, Text, FlowBean, NullWritable>{		@Override		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException { 			String line = value.toString();			String[] fields = line.split("\t");			String phone = fields[0];			String url = fields[1];						FlowBean bean = new FlowBean(phone,url);						context.write(bean, NullWritable.get());		}	}		static class HbaseSinkMrReducer extends TableReducer<FlowBean, NullWritable, ImmutableBytesWritable>{				@Override		protected void reduce(FlowBean key, Iterable<NullWritable> values, Context context) throws IOException, InterruptedException {						Put put = new Put(key.getPhone().getBytes());			put.add("f1".getBytes(), "url".getBytes(), key.getUrl().getBytes());						context.write(new ImmutableBytesWritable(key.getPhone().getBytes()), put);					}			}		public static void main(String[] args) throws Exception {		Configuration conf = HBaseConfiguration.create();		conf.set("hbase.zookeeper.quorum", "spark01");				HBaseAdmin hBaseAdmin = new HBaseAdmin(conf);				boolean tableExists = hBaseAdmin.tableExists(flow_fields_import);		if(tableExists){			hBaseAdmin.disableTable(flow_fields_import);			hBaseAdmin.deleteTable(flow_fields_import);		}		HTableDescriptor desc = new HTableDescriptor(TableName.valueOf(flow_fields_import));		HColumnDescriptor hColumnDescriptor = new HColumnDescriptor ("f1".getBytes());		desc.addFamily(hColumnDescriptor);				hBaseAdmin.createTable(desc);						Job job = Job.getInstance(conf);				job.setJarByClass(HbaseSinker.class);				job.setMapperClass(HbaseSinkMrMapper.class);		TableMapReduceUtil.initTableReducerJob(flow_fields_import, HbaseSinkMrReducer.class, job);				FileInputFormat.setInputPaths(job, new Path("c:/hbasetest/data"));				job.setMapOutputKeyClass(FlowBean.class);		job.setMapOutputValueClass(NullWritable.class);				job.setOutputKeyClass(ImmutableBytesWritable.class);		job.setOutputValueClass(Mutation.class);				job.waitForCompletion(true);					}	}

 

 

 

## **11.3 hbase高级编程**

### **11.3.1 协处理器**

coprocessor

endpoint）

 

### **11.3.2 二级索引demo**

 

# **12.  Hive基础**

Hive是一种数据仓库工具，其功能是将SQL语法表达的数据运算逻辑转化成mapreduce程序在hadoop集群上对海量数据进行分析

## **12.1 hive技术架构**

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps32.jpg) 

## **12.3 hive原理----元数据、数据存储、核心机制**

## **12.4 Hive的安装部署**

----准备安装包

----默认配置和mysql meta store配置

 

<configuration><property><name>javax.jdo.option.ConnectionURL</name><value>jdbc:mysql://weekend01:3306/hive?createDatabaseIfNotExist=true</value></property><property><name>javax.jdo.option.ConnectionDriverName</name><value>com.mysql.jdbc.Driver</value></property><property><name>javax.jdo.option.ConnectionUserName</name><value>root</value></property><property><name>javax.jdo.option.ConnectionPassword</name><value>root</value></property></configuration>

 

 

## **12.5 Hive使用方式**

----shell/hiveserver/beeline/jdbc/hive -e -S

 Hiveserver2

Beeline客户端

JDBC配置

## **12.6 hql基本语法**

### **12.6.1 基本hql语法**

set hive.cli.print.header=true; CREATE TABLE page_view(viewTime INT, userid BIGINT,     page_url STRING, referrer_url STRING,     ip STRING COMMENT 'IP Address of the User') COMMENT 'This is the page view table' PARTITIONED BY(dt STRING, country STRING) ROW FORMAT DELIMITED   FIELDS TERMINATED BY '\001'STORED AS SEQUENCEFILE; //sequencefilecreate table tab_ip_seq(id int,name string,ip string,country string)     row format delimited    fields terminated by ','    stored as sequencefile; //external外部表CREATE EXTERNAL TABLE tab_ip_ext(id int, name string,     ip STRING,     country STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/external/user'; //从本地导入数据到hive的表中（实质就是将文件上传到hdfs中hive管理目录下）load data local inpath '/home/hadoop/ip.txt' into table tab_ext; //从hdfs上导入数据到hive表中（实质就是将文件从原始目录移动到hive管理的目录下）load data inpath 'hdfs://ns1/aa/bb/data.log' into table tab_user;  //使用select语句来批量插入数据insert overwrite table tab_ip_seq select * from tab_ext;  //create & loadcreate table tab_ip(id int,name string,ip string,country string)     row format delimited    fields terminated by ','    stored as textfile;     // CTAS  根据select语句建表结构CREATE TABLE tab_ip_ctas   ASSELECT id new_id, name new_name, ip new_ip,country new_countryFROM tab_ip_extSORT BY new_id;  //CLUSTER <--相对高级一点，你可以放在有精力的时候才去学习>create table tab_ip_cluster(id int,name string,ip string,country string)clustered by(id) into 3 buckets; load data local inpath '/home/hadoop/ip.txt' overwrite into table tab_ip_cluster;set hive.enforce.bucketing=true;insert into table tab_ip_cluster select * from tab_ip; select * from tab_ip_cluster tablesample(bucket 2 out of 3 on id);  //PARTITION  分区表create table tab_ip_part(id int,name string,ip string,country string)     partitioned by (year string)    row format delimited fields terminated by ',';    load data local inpath '/home/hadoop/data.log' overwrite into table tab_ip_part     partition(year='1990');        load data local inpath '/home/hadoop/data2.log' overwrite into table tab_ip_part     partition(year='2000'); select * from tab_ip_part; select * from tab_ip_part  where part_flag='part2';select count(*) from tab_ip_part  where part_flag='part2';  alter table tab_ip change id id_alter string;ALTER TABLE tab_cts ADD PARTITION (partCol = 'dt') location '/external/hive/dt'; show partitions tab_ip_part; //insert from select   通过select语句批量插入数据到别的表create table tab_ip_like like tab_ip;insert overwrite table tab_ip_like    select * from tab_ip;   //write to hdfs  将结果写入到hdfs的文件中insert overwrite local directory '/home/hadoop/hivetemp/test.txt' select * from tab_ip_part where part_flag='part1';    insert overwrite directory '/hiveout.txt' select * from tab_ip_part where part_flag='part1'; //cli shell  通过shell执行hive的hql语句hive -S -e 'select country,count(*) from tab_ext' > /home/hadoop/hivetemp/e.txt  select * from tab_ext sort by id desc limit 5;select a.ip,b.book from tab_ext a join tab_ip_book b on(a.name=b.name);  //array create table tab_array(a array<int>,b array<string>)row format delimitedfields terminated by '\t'collection items terminated by ','; select a[0] from tab_array;select * from tab_array where array_contains(b,'word');insert into table tab_array select array(0),array(name,ip) from tab_ext t;  //mapcreate table tab_map(name string,info map<string,string>)row format delimitedfields terminated by '\t'collection items terminated by ','map keys terminated by ':'; load data local inpath '/home/hadoop/hivetemp/tab_map.txt' overwrite into table tab_map;insert into table tab_map select name,map('name',name,'ip',ip) from tab_ext;  //structcreate table tab_struct(name string,info struct<age:int,tel:string,addr:string>)row format delimitedfields terminated by '\t'collection items terminated by ',' load data local inpath '/home/hadoop/hivetemp/tab_st.txt' overwrite into table tab_struct;insert into table tab_struct select name,named_struct('age',id,'tel',name,'addr',country) from tab_ext;   //UDFselect if(id=1,first,no-first),name from tab_ext; hive>add jar /home/hadoop/myudf.jar;hive>CREATE TEMPORARY FUNCTION fanyi AS 'cn.itcast.hive.Fanyi';select id,name,ip,fanyi(country) from tab_ip_ext;  

 

### **12.6.2  hql查询进阶**

MapReduce脚本

连接（join）

内连接（inner join）

外连接（outer join）

半连接（semi join）

Map连接（map join）

子查询（sub query）

视图（view）

通过Hive提供的order by子句可以让最终的输出结果整体有序。但是因为Hive是基于Hadoop之上的，要生成这种整体有序的结果，就必须强迫Hadoop只利用一个Reduce来完成处理。这种方式的副作用就是回降低效率。

如果你不需要最终结果整体有序，你就可以使用sort by子句来进行排序。这种排序操作只保证每个Reduce的输出是有序的。如果你希望某些特定行被同一个Reduce处理，则你可以使用distribute子句来完成。比如：

表student（classNo，stuNo，score）数据如下：

C01  N0101      82

C01  N0102      59

C02  N0201      81

C01  N0103      65

C03  N0302      92

C02  N0202      82

C02  N0203      79

C03  N0301      56

C03  N0306      72

 

我们希望按照成绩由低到高输出每个班级的成绩信息。执行以下语句：

Select classNo,stuNo,score from student distribute byclassNo sort by score;

输出结果为:

C02  N0203      79

C02  N0201      81

C02  N0202      82

C03  N0301      56

C03  N0306      72

C03  N0302      92

C01  N0102      59

C01  N0103      65

C01  N0101      82

我们可以看到每一个班级里所有的学生成绩是有序的。因为同一个classNo的记录会被分发到一个单独的reduce处理，而同时sort by保证了每一个reduce的输出是有序的。

注意：

为了测试上例中的distribute by的效果，你应该首先设置足够多的reduce。比如上例中有3个不同的classNo，则我们需要设置reduce个数至少为3或更多。如果设置的reduce个数少于3，将会导致多个不同的classNo被分发到同一个reduce，从而不能产生你所期望的输出。设置命令如下：

set mapred.reduce.tasks = 3;

MapReduce脚本

 

如果我们需要在查询语句中调用外部脚本，比如Python，则我们可以使用transform，map，reduce等子句。

比如，我们希望过滤掉所有不及格的学生记录，只输出及格学生的成绩信息。

新建一个Python脚本文件score_pass.py，内容如下：

\#! /usr/bin/env python

import sys

for line in sys.stdin:

​         (classNo,stuNo,score)= line.strip().split('\t')  

​         ifint(score) >= 60:

​                   print"%s\t%s\t%s" %(classNo,stuNo,score)

执行以下语句

add file /home/user/score_pass.py;

select transform(classNo,stuNo,score) using'score_pass.py' as classNo,stuNo,score from student;

输出结果为：

C01  N0101      82

C02  N0201      81

C01  N0103      65

C03  N0302      92

C02  N0202      82

C02  N0203      79

C03  N0306      72

注意：

1) 以上Python脚本中，分隔符只能是制表符(\t)。同样输出的分隔符也必须为制表符。这个是有hive自身决定的，不能更改，不要尝试使用其他分隔符，否则会报错。同时需要调用strip函数，以去除掉行尾的换行符。（或者直接使用不带参数的line.split()代替。

2) 使用脚本前，先使用add file语句注册脚本文件，以便hive将其分发到Hadoop集群。

3) Transfom传递数据到Python脚本，as语句指定输出的列。

连接（join）

 

直接编程使用Hadoop的MapReduce是一件比较费时的事情。Hive则大大简化了这个操作。

内连接（inner join）

 

和SQL的内连相似。执行以下语句查询每个学生的编号和教师名：

Select a.stuNo,b.teacherName from student a join teacherb on a.classNo = b.classNo;

输出结果如下：

N0203      Sun

N0202      Sun

N0201      Sun

N0306      Wang

N0301      Wang

N0302      Wang

N0103      Zhang

N0102      Zhang

N0101      Zhang

注意：

数据文件内容请参照上一篇文章。

不要使用select xx from aa,bb where aa.f=bb.f这样的语法，hive不支持这种写法。

如果需要查看hive的执行计划，你可以在语句前加上explain，比如：

explain Select a.stuNo,b.teacherName from student a jointeacher b on a.classNo = b.classNo;

外连接（outer join）

 

和传统SQL类似，Hive提供了left outer join，right outer join，full out join。

半连接（semi join）

 

Hive不提供in子查询。此时你可以用leftsemi join实现同样的功能。

执行以下语句：

Select * from teacher left semi join student onstudent.classNo = teacher.classNo;

输出结果如下：

C02  Sun

C03  Wang

C01  Zhang

可以看出，C04 Dong没有出现在查询结果中，因为C04在表student中不存在。

注意：

右表（student）中的字段只能出现在on子句中，不能出现在其他地方，比如不能出现在select子句中。

Map连接（map join）

 

当一个表非常小，足以直接装载到内存中去时，可以使用map连接以提高效率，比如：

Select /*+mapjoin(teacher) */ a.stuNo,b.teacherNamefrom student a join teacher b on a.classNo = b.classNo;

以上红色标记部分采用了C的注释风格。

当连接时用到不等值判断时，也比较适合Map连接。具体原因需要深入了解Hive和MapReduce的工作原理。

子查询（sub query）

 

运行以下语句将返回所有班级平均分的最高记录。

Select max(avgScore) as maScore

from

(Select classNo,avg(score) as avgScore from student group byclassNo) a;

输出结果：

80.66666666666667

以上语句中红色部分为一个子查询，且别名为a。返回的子查询结果和一个表类似，可以被继续查询。

视图（view）

 

和传统数据库中的视图类似，Hive的视图只是一个定义，视图数据并不会存储到文件系统中。同样，视图是只读的。

运行以下两个命令：

Create view avg_score as

Select classNo,avg(score) as avgScore from student groupby classNo;

Select max(avgScore) as maScore

From avg_score;

可以看到输出结果和上例中的结果是一样的。

 

## **12.7 hive数据类型**

---基本类型

---复合类型

 

 

 

动手练习（hql查询及udf编写）

 

# **13.  Hive高级应用**

## **13.1  Hive常用函数**

----参见youdao笔记《hive 优化总结》函数部分

----造数据做例子

## **13.2  自定义函数**

自定义函数的实现步骤

hive自定义函数UDF示例

hive自定义函数UDAF示例

 

## **13.3  hive高级操作**

分区表/桶表应用，skew，map-join

行列转换

## **13.4  hive优化**

hive优化思想

Explain的使用

经典案例(distinct count)

 

## **13.5  hive对数据倾斜的优化**

### **13.5.1 数据倾斜的原因**

1.1操作：

关键词	情形	后果

Join	其中一个表较小，

但是key集中	分发到某一个或几个Reduce上的数据远高于平均值

​	大表与大表，但是分桶的判断字段0值或空值过多	这些空值都由一个reduce处理，灰常慢

group by	group by 维度过小，

某值的数量过多	处理某值的reduce灰常耗时

Count Distinct	某特殊值过多	处理此特殊值的reduce耗时

1.2原因：

1)、key分布不均匀

2)、业务数据本身的特性

3)、建表时考虑不周

4)、某些SQL语句本身就有数据倾斜

 

1.3表现：

任务进度长时间维持在99%（或100%），查看任务监控页面，发现只有少量（1个或几个）reduce子任务未完成。因为其处理的数据量和其他reduce差异过大。

单一reduce的记录数与平均记录数差异过大，通常可能达到3倍甚至更多。 最长时长远大于平均时长。

 

### **13.5.2 数据倾斜的解决方案**

2.1参数调节：

hive.map.aggr=true

Map 端部分聚合，相当于Combiner

hive.groupby.skewindata=true

有数据倾斜的时候进行负载均衡，当选项设定为 true，生成的查询计划会有两个 MR Job。第一个 MR Job 中，Map 的输出结果集合会随机分布到 Reduce 中，每个 Reduce 做部分聚合操作，并输出结果，这样处理的结果是相同的 Group By Key 有可能被分发到不同的 Reduce 中，从而达到负载均衡的目的；第二个 MR Job 再根据预处理的数据结果按照 Group By Key 分布到 Reduce 中（这个过程可以保证相同的 Group By Key 被分布到同一个 Reduce 中），最后完成最终的聚合操作。

 

2.2 SQL语句调节：

如何Join：

关于驱动表的选取，选用join key分布最均匀的表作为驱动表

做好列裁剪和filter操作，以达到两表做join的时候，数据量相对变小的效果。

大小表Join：

使用map join让小的维度表（1000条以下的记录条数） 先进内存。在map端完成reduce.

大表Join大表：

把空值的key变成一个字符串加上随机数，把倾斜的数据分到不同的reduce上，由于null值关联不上，处理后并不影响最终结果。

count distinct大量相同特殊值

count distinct时，将值为空的情况单独处理，如果是计算count distinct，可以不用处理，直接过滤，在最后结果中加1。如果还有其他计算，需要进行group by，可以先将值为空的记录单独处理，再和其他计算结果进行union。

group by维度过小：

采用sum() group by的方式来替换count(distinct)完成计算。

特殊情况特殊处理：

在业务逻辑优化效果的不大情况下，有些时候是可以将倾斜的数据单独拿出来处理。最后union回去。

 

### **13.5.3 典型的业务场景**

3.1空值产生的数据倾斜

场景：如日志中，常会有信息丢失的问题，比如日志中的 user_id，如果取其中的 user_id 和 用户表中的user_id 关联，会碰到数据倾斜的问题。

解决方法1： user_id为空的不参与关联（红色字体为修改后）

 

select * from log a  join users b  on a.user_id is not null  and a.user_id = b.user_idunion allselect * from log a  where a.user_id is null;

 

 

解决方法2 ：赋与空值分新的key值

select *  from log a  left outer join users b  on case when a.user_id is null then concat(‘hive’,rand() ) else a.user_id end = b.user_id;

 

结论：方法2比方法1效率更好，不但io少了，而且作业数也少了。解决方法1中 log读取两次，jobs是2。解决方法2 job数是1 。这个优化适合无效 id (比如 -99 , ’’, null 等) 产生的倾斜问题。把空值的 key 变成一个字符串加上随机数，就能把倾斜的数据分到不同的reduce上 ,解决数据倾斜问题。

 

3.2不同数据类型关联产生数据倾斜

场景：用户表中user_id字段为int，log表中user_id字段既有string类型也有int类型。当按照user_id进行两个表的Join操作时，默认的Hash操作会按int型的id来进行分配，这样会导致所有string类型id的记录都分配到一个Reducer中。

解决方法：把数字类型转换成字符串类型

select * from users a  left outer join logs b  on a.usr_id = cast(b.user_id as string)

 

3.3小表不小不大，怎么用 map join 解决倾斜问题

使用 map join 解决小表(记录数少)关联大表的数据倾斜问题，这个方法使用的频率非常高，但如果小表很大，大到map join会出现bug或异常，这时就需要特别的处理。 以下例子:

select * from log a  left outer join users b  on a.user_id = b.user_id;

 

users 表有 600w+ 的记录，把 users 分发到所有的 map 上也是个不小的开销，而且 map join 不支持这么大的小表。如果用普通的 join，又会碰到数据倾斜的问题。

解决方法：

 

select /*+mapjoin(x)*/* from log a  left outer join (    select  /*+mapjoin(c)*/d.*      from ( select distinct user_id from log ) c      join users d      on c.user_id = d.user_id    ) x  on a.user_id = b.user_id; 

 

假如，log里user_id有上百万个，这就又回到原来map join问题。所幸，每日的会员uv不会太多，有交易的会员不会太多，有点击的会员不会太多，有佣金的会员不会太多等等。所以这个方法能解决很多场景下的数据倾斜问题。

### **13.5.4 总结**

使map的输出数据更均匀的分布到reduce中去，是我们的最终目标。由于Hash算法的局限性，按key Hash会或多或少的造成数据倾斜。大量经验表明数据倾斜的原因是人为的建表疏忽或业务逻辑可以规避的。在此给出较为通用的步骤：

1、采样log表，哪些user_id比较倾斜，得到一个结果表tmp1。由于对计算框架来说，所有的数据过来，他都是不知道数据分布情况的，所以采样是并不可少的。

2、数据的分布符合社会学统计规则，贫富不均。倾斜的key不会太多，就像一个社会的富人不多，奇特的人不多一样。所以tmp1记录数会很少。把tmp1和users做map join生成tmp2,把tmp2读到distribute file cache。这是一个map过程。

3、map读入users和log，假如记录来自log,则检查user_id是否在tmp2里，如果是，输出到本地文件a,否则生成<user_id,value>的key,value对，假如记录来自member,生成<user_id,value>的key,value对，进入reduce阶段。

4、最终把a文件，把Stage3 reduce阶段输出的文件合并起写到hdfs。

 

如果确认业务需要这样倾斜的逻辑，考虑以下的优化方案：

1、对于join，在判断小表不大于1G的情况下，使用map join

2、对于group by或distinct，设定 hive.groupby.skewindata=true

3、尽量使用上述的SQL语句调节进行优化 

 

动手练习（spark中订单数据统计模型的sql编写）

# **14.  数据采集工具**

## **14.1 flume介绍**

　　一、什么是Flume?

　　flume 作为 cloudera 开发的实时日志收集系统，受到了业界的认可与广泛应用。Flume 初始的发行版本目前被统称为 Flume OG（original generation），属于 cloudera。但随着 FLume 功能的扩展，Flume OG 代码工程臃肿、核心组件设计不合理、核心配置不标准等缺点暴露出来，尤其是在 Flume OG 的最后一个发行版本 0.94.0 中，日志传输不稳定的现象尤为严重，为了解决这些问题，2011 年 10 月 22 号，cloudera 完成了 Flume-728，对 Flume 进行了里程碑式的改动：重构核心组件、核心配置以及代码架构，重构后的版本统称为 Flume NG（next generation）；改动的另一原因是将 Flume 纳入 apache 旗下，cloudera Flume 改名为 Apache Flume。

 

​        flume的特点：

　　flume是一个分布式、可靠、和高可用的海量日志采集、聚合和传输的系统。支持在日志系统中定制各类数据发送方，用于收集数据;同时，Flume提供对数据进行简单处理，并写到各种数据接受方(比如文本、HDFS、Hbase等)的能力 。

　　flume的数据流由事件(Event)贯穿始终。事件是Flume的基本数据单位，它携带日志数据(字节数组形式)并且携带有头信息，这些Event由Agent外部的Source生成，当Source捕获事件后会进行特定的格式化，然后Source会把事件推入(单个或多个)Channel中。你可以把Channel看作是一个缓冲区，它将保存事件直到Sink处理完该事件。Sink负责持久化日志或者把事件推向另一个Source。

 

​        flume的可靠性 

　　当节点出现故障时，日志能够被传送到其他节点上而不会丢失。Flume提供了三种级别的可靠性保障，从强到弱依次分别为：end-to-end（收到数据agent首先将event写到磁盘上，当数据传送成功后，再删除；如果数据发送失败，可以重新发送。），Store on failure（这也是scribe采用的策略，当数据接收方crash时，将数据写到本地，待恢复后，继续发送），Besteffort（数据发送到接收方后，不会进行确认）。

 

​        flume的可恢复性：

　　还是靠Channel。推荐使用FileChannel，事件持久化在本地文件系统里(性能较差)。 

 

　　flume的一些核心概念：

Agent        使用JVM 运行Flume。每台机器运行一个agent，但是可以在一个agent中包含多个sources和sinks。

Client        生产数据，运行在一个独立的线程。

Source        从Client收集数据，传递给Channel。

Sink        从Channel收集数据，运行在一个独立线程。

Channel        连接 sources 和 sinks ，这个有点像一个队列。

Events        可以是日志记录、 avro 对象等。

 

 

Flume以agent为最小的独立运行单位。一个agent就是一个JVM。单agent由Source、Sink和Channel三大组件构成，如下图：

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps33.jpg)

值得注意的是，Flume提供了大量内置的Source、Channel和Sink类型。不同类型的Source,Channel和Sink可以自由组合。组合方式基于用户设置的配置文件，非常灵活。比如：Channel可以把事件暂存在内存里，也可以持久化到本地硬盘上。Sink可以把日志写入HDFS, HBase，甚至是另外一个Source等等。Flume支持用户建立多级流，也就是说，多个agent可以协同工作，并且支持Fan-in、Fan-out、Contextual Routing、Backup Routes，这也正是NB之处。如下图所示:

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps34.jpg)

 

 

　　二、flume的官方网站在哪里？

　　http://flume.apache.org/

 

　　三、在哪里下载？

　　http://www.apache.org/dyn/closer.cgi/flume/1.5.0/apache-flume-1.5.0-bin.tar.gz

 

　　四、如何安装？

　　　　1)将下载的flume包，解压到/home/hadoop目录中，你就已经完成了50%：）简单吧

　　　　2)修改 flume-env.sh 配置文件,主要是JAVA_HOME变量设置

root@m1:/home/hadoop/flume-1.5.0-bin# cp conf/flume-env.sh.template conf/flume-env.shroot@m1:/home/hadoop/flume-1.5.0-bin# vi conf/flume-env.sh# Licensed to the Apache Software Foundation (ASF) under one# or more contributor license agreements.  See the NOTICE file# distributed with this work for additional information# regarding copyright ownership.  The ASF licenses this file# to you under the Apache License, Version 2.0 (the# "License"); you may not use this file except in compliance# with the License.  You may obtain a copy of the License at##     http://www.apache.org/licenses/LICENSE-2.0## Unless required by applicable law or agreed to in writing, software# distributed under the License is distributed on an "AS IS" BASIS,# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.# See the License for the specific language governing permissions and# limitations under the License. # If this file is placed at FLUME_CONF_DIR/flume-env.sh, it will be sourced# during Flume startup. # Enviroment variables can be set here. JAVA_HOME=/usr/lib/jvm/java-7-oracle # Give Flume more memory and pre-allocate, enable remote monitoring via JMX#JAVA_OPTS="-Xms100m -Xmx200m -Dcom.sun.management.jmxremote" # Note that the Flume conf directory is always included in the classpath.#FLUME_CLASSPATH=""

   3)验证是否安装成功

 

root@m1:/home/hadoop# /home/hadoop/flume-1.5.0-bin/bin/flume-ng versionFlume 1.5.0Source code repository: https://git-wip-us.apache.org/repos/asf/flume.gitRevision: 8633220df808c4cd0c13d1cf0320454a94f1ea97Compiled by hshreedharan on Wed May  7 14:49:18 PDT 2014From source with checksum a01fe726e4380ba0c9f7a7d222db961froot@m1:/home/hadoop#

 

五、flume的案例

　　　　1)案例1：Avro

　　　　Avro可以发送一个给定的文件给Flume，Avro 源使用AVRO RPC机制。

a) 创建agent配置文件

root@m1:/home/hadoop#vi /home/hadoop/flume-1.5.0-bin/conf/avro.conf a1.sources = r1a1.sinks = k1a1.channels = c1 # Describe/configure the sourcea1.sources.r1.type = avroa1.sources.r1.channels = c1a1.sources.r1.bind = 0.0.0.0a1.sources.r1.port = 4141 # Describe the sinka1.sinks.k1.type = logger # Use a channel which buffers events in memorya1.channels.c1.type = memorya1.channels.c1.capacity = 1000a1.channels.c1.transactionCapacity = 100 # Bind the source and sink to the channela1.sources.r1.channels = c1a1.sinks.k1.channel = c1

b) 启动flume agent a1

root@m1:/home/hadoop# /home/hadoop/flume-1.5.0-bin/bin/flume-ng agent -c . -f /home/hadoop/flume-1.5.0-bin/conf/avro.conf -n a1 -Dflume.root.logger=INFO,console

 

c)创建指定文件

root@m1:/home/hadoop# echo "hello world" > /home/hadoop/flume-1.5.0-bin/log.00

 

d)使用avro-client发送文件

root@m1:/home/hadoop# /home/hadoop/flume-1.5.0-bin/bin/flume-ng avro-client -c . -H m1 -p 4141 -F /

 

f)在m1的控制台，可以看到以下信息，注意最后一行：

root@m1:/home/hadoop/flume-1.5.0-bin/conf# /home/hadoop/flume-1.5.0-bin/bin/flume-ng agent -c . -f /home/hadoop/flume-1.5.0-bin/conf/avro.conf -n a1 -Dflume.root.logger=INFO,consoleInfo: Sourcing environment configuration script /home/hadoop/flume-1.5.0-bin/conf/flume-env.shInfo: Including Hadoop libraries found via (/home/hadoop/hadoop-2.2.0/bin/hadoop) for HDFS accessInfo: Excluding /home/hadoop/hadoop-2.2.0/share/hadoop/common/lib/slf4j-api-1.7.5.jar from classpathInfo: Excluding /home/hadoop/hadoop-2.2.0/share/hadoop/common/lib/slf4j-log4j12-1.7.5.jar from classpath...2014-08-10 10:43:25,112 (New I/O  worker #1) [INFO - org.apache.avro.ipc.NettyServer$NettyServerAvroHandler.handleUpstream(NettyServer.java:171)] [id: 0x92464c4f, /192.168.1.50:59850 :> /192.168.1.50:4141] UNBOUND2014-08-10 10:43:25,112 (New I/O  worker #1) [INFO - org.apache.avro.ipc.NettyServer$NettyServerAvroHandler.handleUpstream(NettyServer.java:171)] [id: 0x92464c4f, /192.168.1.50:59850 :> /192.168.1.50:4141] CLOSED2014-08-10 10:43:25,112 (New I/O  worker #1) [INFO - org.apache.avro.ipc.NettyServer$NettyServerAvroHandler.channelClosed(NettyServer.java:209)] Connection to /192.168.1.50:59850 disconnected.2014-08-10 10:43:26,718 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 68 65 6C 6C 6F 20 77 6F 72 6C 64                hello world }

 

　　　　2)案例2：Spool

　　　　Spool监测配置的目录下新增的文件，并将文件中的数据读取出来。需要注意两点：

　　　　1) 拷贝到spool目录下的文件不可以再打开编辑。

　　　　2) spool目录下不可包含相应的子目录

 

 

　　　　　　a)创建agent配置文件

root@m1:/home/hadoop# vi /home/hadoop/flume-1.5.0-bin/conf/spool.conf a1.sources = r1a1.sinks = k1a1.channels = c1 # Describe/configure the sourcea1.sources.r1.type = spooldira1.sources.r1.channels = c1a1.sources.r1.spoolDir = /home/hadoop/flume-1.5.0-bin/logsa1.sources.r1.fileHeader = true # Describe the sinka1.sinks.k1.type = logger # Use a channel which buffers events in memorya1.channels.c1.type = memorya1.channels.c1.capacity = 1000a1.channels.c1.transactionCapacity = 100 # Bind the source and sink to the channela1.sources.r1.channels = c1a1.sinks.k1.channel = c1

b)启动flume agent a1

root@m1:/home/hadoop# /home/hadoop/flume-1.5.0-bin/bin/flume-ng agent -c . -f /home/hadoop/flume-1.5.0-bin/conf/spool.conf -n a1 -Dflume.root.logger=INFO,console

　c)追加文件到/home/hadoop/flume-1.5.0-bin/logs目录

 

root@m1:/home/hadoop# echo "spool test1" > /home/hadoop/flume-1.5.0-bin/logs/spool_text.log

d)在m1的控制台，可以看到以下相关信息：

14/08/10 11:37:13 INFO source.SpoolDirectorySource: Spooling Directory Source runner has shutdown.14/08/10 11:37:13 INFO source.SpoolDirectorySource: Spooling Directory Source runner has shutdown.14/08/10 11:37:14 INFO avro.ReliableSpoolingFileEventReader: Preparing to move file /home/hadoop/flume-1.5.0-bin/logs/spool_text.log to /home/hadoop/flume-1.5.0-bin/logs/spool_text.log.COMPLETED14/08/10 11:37:14 INFO source.SpoolDirectorySource: Spooling Directory Source runner has shutdown.14/08/10 11:37:14 INFO source.SpoolDirectorySource: Spooling Directory Source runner has shutdown.14/08/10 11:37:14 INFO sink.LoggerSink: Event: { headers:{file=/home/hadoop/flume-1.5.0-bin/logs/spool_text.log} body: 73 70 6F 6F 6C 20 74 65 73 74 31                spool test1 }14/08/10 11:37:15 INFO source.SpoolDirectorySource: Spooling Directory Source runner has shutdown.14/08/10 11:37:15 INFO source.SpoolDirectorySource: Spooling Directory Source runner has shutdown.14/08/10 11:37:16 INFO source.SpoolDirectorySource: Spooling Directory Source runner has shutdown.14/08/10 11:37:16 INFO source.SpoolDirectorySource: Spooling Directory Source runner has shutdown.14/08/10 11:37:17 INFO source.SpoolDirectorySource: Spooling Directory Source runner has shutdown.

 

3)案例3：Exec

　　　　EXEC执行一个给定的命令获得输出的源,如果要使用tail命令，必选使得file足够大才能看到输出内容

 

　　　　　　a)创建agent配置文件

root@m1:/home/hadoop# vi /home/hadoop/flume-1.5.0-bin/conf/exec_tail.conf a1.sources = r1a1.sinks = k1a1.channels = c1 # Describe/configure the sourcea1.sources.r1.type = execa1.sources.r1.channels = c1a1.sources.r1.command = tail -F /home/hadoop/flume-1.5.0-bin/log_exec_tail # Describe the sinka1.sinks.k1.type = logger # Use a channel which buffers events in memorya1.channels.c1.type = memorya1.channels.c1.capacity = 1000a1.channels.c1.transactionCapacity = 100 # Bind the source and sink to the channela1.sources.r1.channels = c1a1.sinks.k1.channel = c1

 

b)启动flume agent a1

root@m1:/home/hadoop# /home/hadoop/flume-1.5.0-bin/bin/flume-ng agent -c . -f /home/hadoop/flume-1.5.0-bin/conf/exec_tail.conf -n a1 -Dflume.root.logger=INFO,console

c)生成足够多的内容在文件里

root@m1:/home/hadoop# for i in {1..100};do echo "exec tail$i" >> /home/hadoop/flume-1.5.0-bin/log_

 

e)在m1的控制台，可以看到以下信息：

2014-08-10 10:59:25,513 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 20 74 65 73 74       exec tail test }2014-08-10 10:59:34,535 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 20 74 65 73 74       exec tail test }2014-08-10 11:01:40,557 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 31                   exec tail1 }2014-08-10 11:01:41,180 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 32                   exec tail2 }2014-08-10 11:01:41,180 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 33                   exec tail3 }2014-08-10 11:01:41,181 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 34                   exec tail4 }2014-08-10 11:01:41,181 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 35                   exec tail5 }2014-08-10 11:01:41,181 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 36                   exec tail6 }............2014-08-10 11:01:51,550 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 39 36                exec tail96 }2014-08-10 11:01:51,550 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 39 37                exec tail97 }2014-08-10 11:01:51,551 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 39 38                exec tail98 }2014-08-10 11:01:51,551 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 39 39                exec tail99 }2014-08-10 11:01:51,551 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 65 78 65 63 20 74 61 69 6C 31 30 30             exec tail100 }

 

　4)案例4：Syslogtcp

　　　　Syslogtcp监听TCP的端口做为数据源

 

　　　　　　a)创建agent配置文件

 

root@m1:/home/hadoop# vi /home/hadoop/flume-1.5.0-bin/conf/syslog_tcp.conf a1.sources = r1a1.sinks = k1a1.channels = c1 # Describe/configure the sourcea1.sources.r1.type = syslogtcpa1.sources.r1.port = 5140a1.sources.r1.host = localhosta1.sources.r1.channels = c1 # Describe the sinka1.sinks.k1.type = logger # Use a channel which buffers events in memorya1.channels.c1.type = memorya1.channels.c1.capacity = 1000a1.channels.c1.transactionCapacity = 100 # Bind the source and sink to the channela1.sources.r1.channels = c1a1.sinks.k1.channel = c1

 

　b)启动flume agent a1

root@m1:/home/hadoop# /home/hadoop/flume-1.5.0-bin/bin/flume-ng agent -c . -f /home/hadoop/flume-1.5.0-bin/conf/syslog_tcp.conf -n a1 -Dflume.root.logger=INFO,console

c)测试产生syslog

root@m1:/home/hadoop# echo "hello idoall.org syslog" | nc localhost 5140

 

d)在m1的控制台，可以看到以下信息

14/08/10 11:41:45 INFO node.PollingPropertiesFileConfigurationProvider: Reloading configuration file:/home/hadoop/flume-1.5.0-bin/conf/syslog_tcp.conf14/08/10 11:41:45 INFO conf.FlumeConfiguration: Added sinks: k1 Agent: a114/08/10 11:41:45 INFO conf.FlumeConfiguration: Processing:k114/08/10 11:41:45 INFO conf.FlumeConfiguration: Processing:k114/08/10 11:41:45 INFO conf.FlumeConfiguration: Post-validation flume configuration contains configuration for agents: [a1]14/08/10 11:41:45 INFO node.AbstractConfigurationProvider: Creating channels14/08/10 11:41:45 INFO channel.DefaultChannelFactory: Creating instance of channel c1 type memory14/08/10 11:41:45 INFO node.AbstractConfigurationProvider: Created channel c114/08/10 11:41:45 INFO source.DefaultSourceFactory: Creating instance of source r1, type syslogtcp14/08/10 11:41:45 INFO sink.DefaultSinkFactory: Creating instance of sink: k1, type: logger14/08/10 11:41:45 INFO node.AbstractConfigurationProvider: Channel c1 connected to [r1, k1]14/08/10 11:41:45 INFO node.Application: Starting new configuration:{ sourceRunners:{r1=EventDrivenSourceRunner: { source:org.apache.flume.source.SyslogTcpSource{name:r1,state:IDLE} }} sinkRunners:{k1=SinkRunner: { policy:org.apache.flume.sink.DefaultSinkProcessor@6538b14 counterGroup:{ name:null counters:{} } }} channels:{c1=org.apache.flume.channel.MemoryChannel{name: c1}} }14/08/10 11:41:45 INFO node.Application: Starting Channel c114/08/10 11:41:45 INFO instrumentation.MonitoredCounterGroup: Monitored counter group for type: CHANNEL, name: c1: Successfully registered new MBean.14/08/10 11:41:45 INFO instrumentation.MonitoredCounterGroup: Component type: CHANNEL, name: c1 started14/08/10 11:41:45 INFO node.Application: Starting Sink k114/08/10 11:41:45 INFO node.Application: Starting Source r114/08/10 11:41:45 INFO source.SyslogTcpSource: Syslog TCP Source starting...14/08/10 11:42:15 WARN source.SyslogUtils: Event created from Invalid Syslog data.14/08/10 11:42:15 INFO sink.LoggerSink: Event: { headers:{Severity=0, flume.syslog.status=Invalid, Facility=0} body: 68 65 6C 6C 6F 20 69 64 6F 61 6C 6C 2E 6F 72 67 hello idoall.org }

 

　5)案例5：JSONHandler

　　　　　　a)创建agent配置文件

root@m1:/home/hadoop# vi /home/hadoop/flume-1.5.0-bin/conf/post_json.conf a1.sources = r1a1.sinks = k1a1.channels = c1 # Describe/configure the sourcea1.sources.r1.type = org.apache.flume.source.http.HTTPSourcea1.sources.r1.port = 8888a1.sources.r1.channels = c1 # Describe the sinka1.sinks.k1.type = logger # Use a channel which buffers events in memorya1.channels.c1.type = memorya1.channels.c1.capacity = 1000a1.channels.c1.transactionCapacity = 100 # Bind the source and sink to the channela1.sources.r1.channels = c1a1.sinks.k1.channel = c1

b)启动flume agent a1

root@m1:/home/hadoop# /home/hadoop/flume-1.5.0-bin/bin/flume-ng agent -c . -f /home/hadoop/flume-1.5.0-bin/conf/post_json.conf -n a1 -Dflume.root.logger=INFO,console

 

c)生成JSON 格式的POST request

 

root@m1:/home/hadoop# curl -X POST -d '[{ "headers" :{"a" : "a1","b" : "b1"},"body" : "idoall.org_body"}]' http://localhost:8888

 

d)在m1的控制台，可以看到以下信息：

14/08/10 11:49:59 INFO node.Application: Starting Channel c114/08/10 11:49:59 INFO instrumentation.MonitoredCounterGroup: Monitored counter group for type: CHANNEL, name: c1: Successfully registered new MBean.14/08/10 11:49:59 INFO instrumentation.MonitoredCounterGroup: Component type: CHANNEL, name: c1 started14/08/10 11:49:59 INFO node.Application: Starting Sink k114/08/10 11:49:59 INFO node.Application: Starting Source r114/08/10 11:49:59 INFO mortbay.log: Logging to org.slf4j.impl.Log4jLoggerAdapter(org.mortbay.log) via org.mortbay.log.Slf4jLog14/08/10 11:49:59 INFO mortbay.log: jetty-6.1.2614/08/10 11:50:00 INFO mortbay.log: Started SelectChannelConnector@0.0.0.0:888814/08/10 11:50:00 INFO instrumentation.MonitoredCounterGroup: Monitored counter group for type: SOURCE, name: r1: Successfully registered new MBean.14/08/10 11:50:00 INFO instrumentation.MonitoredCounterGroup: Component type: SOURCE, name: r1 started14/08/10 12:14:32 INFO sink.LoggerSink: Event: { headers:{b=b1, a=a1} body: 69 64 6F 61 6C 6C 2E 6F 72 67 5F 62 6F 64 79    idoall.org_body }

 

6)案例6：Hadoop sink

　　　　　　a)创建agent配置文件

 

root@m1:/home/hadoop# vi /home/hadoop/flume-1.5.0-bin/conf/hdfs_sink.conf a1.sources = r1a1.sinks = k1a1.channels = c1 # Describe/configure the sourcea1.sources.r1.type = syslogtcpa1.sources.r1.port = 5140a1.sources.r1.host = localhosta1.sources.r1.channels = c1 # Describe the sinka1.sinks.k1.type = hdfsa1.sinks.k1.channel = c1a1.sinks.k1.hdfs.path = hdfs://m1:9000/user/flume/syslogtcpa1.sinks.k1.hdfs.filePrefix = Sysloga1.sinks.k1.hdfs.round = truea1.sinks.k1.hdfs.roundValue = 10a1.sinks.k1.hdfs.roundUnit = minute # Use a channel which buffers events in memorya1.channels.c1.type = memorya1.channels.c1.capacity = 1000a1.channels.c1.transactionCapacity = 100 # Bind the source and sink to the channela1.sources.r1.channels = c1a1.sinks.k1.channel = c1

 

b)启动flume agent a1

root@m1:/home/hadoop# /home/hadoop/flume-1.5.0-bin/bin/flume-ng agent -c . -f /home/hadoop/flume-1.5.0-bin/conf/hdfs_sink.conf -n a1 -Dflume.root.logger=INFO,console

 

 

c)测试产生syslog

root@m1:/home/hadoop# echo "hello idoall flume -> hadoop testing one" | nc localhost 5140

 

d)在m1的控制台，可以看到以下信息：

14/08/10 12:20:39 INFO instrumentation.MonitoredCounterGroup: Monitored counter group for type: CHANNEL, name: c1: Successfully registered new MBean.14/08/10 12:20:39 INFO instrumentation.MonitoredCounterGroup: Component type: CHANNEL, name: c1 started14/08/10 12:20:39 INFO node.Application: Starting Sink k114/08/10 12:20:39 INFO node.Application: Starting Source r114/08/10 12:20:39 INFO instrumentation.MonitoredCounterGroup: Monitored counter group for type: SINK, name: k1: Successfully registered new MBean.14/08/10 12:20:39 INFO instrumentation.MonitoredCounterGroup: Component type: SINK, name: k1 started14/08/10 12:20:39 INFO source.SyslogTcpSource: Syslog TCP Source starting...14/08/10 12:21:46 WARN source.SyslogUtils: Event created from Invalid Syslog data.14/08/10 12:21:49 INFO hdfs.HDFSSequenceFile: writeFormat = Writable, UseRawLocalFileSystem = false14/08/10 12:21:49 INFO hdfs.BucketWriter: Creating hdfs://m1:9000/user/flume/syslogtcp//Syslog.1407644509504.tmp14/08/10 12:22:20 INFO hdfs.BucketWriter: Closing hdfs://m1:9000/user/flume/syslogtcp//Syslog.1407644509504.tmp14/08/10 12:22:20 INFO hdfs.BucketWriter: Close tries incremented14/08/10 12:22:20 INFO hdfs.BucketWriter: Renaming hdfs://m1:9000/user/flume/syslogtcp/Syslog.1407644509504.tmp to hdfs://m1:9000/user/flume/syslogtcp/Syslog.140764450950414/08/10 12:22:20 INFO hdfs.HDFSEventSink: Writer callback called.

 

e)在m1上再打开一个窗口，去hadoop上检查文件是否生成

root@m1:/home/hadoop# /home/hadoop/hadoop-2.2.0/bin/hadoop fs -ls /user/flume/syslogtcpFound 1 items-rw-r--r--   3 root supergroup        155 2014-08-10 12:22 /user/flume/syslogtcp/Syslog.1407644509504root@m1:/home/hadoop# /home/hadoop/hadoop-2.2.0/bin/hadoop fs -cat /user/flume/syslogtcp/Syslog.1407644509504SEQ!org.apache.hadoop.io.LongWritable"org.apache.hadoop.io.BytesWritable^;>Gv$hello idoall flume -> hadoop testing one

 

7)案例7：File Roll Sink

　　　　　　a)创建agent配置文件

root@m1:/home/hadoop# vi /home/hadoop/flume-1.5.0-bin/conf/file_roll.conf a1.sources = r1a1.sinks = k1a1.channels = c1 # Describe/configure the sourcea1.sources.r1.type = syslogtcpa1.sources.r1.port = 5555a1.sources.r1.host = localhosta1.sources.r1.channels = c1 # Describe the sinka1.sinks.k1.type = file_rolla1.sinks.k1.sink.directory = /home/hadoop/flume-1.5.0-bin/logs # Use a channel which buffers events in memorya1.channels.c1.type = memorya1.channels.c1.capacity = 1000a1.channels.c1.transactionCapacity = 100 # Bind the source and sink to the channela1.sources.r1.channels = c1a1.sinks.k1.channel = c1

b)启动flume agent a1

root@m1:/home/hadoop# /home/hadoop/flume-1.5.0-bin/bin/flume-ng agent -c . -f /home/hadoop/flume-1.5.0-bin/conf/file_roll.conf -n a1 -Dflume.root.logger=INFO,console

c)测试产生log

 

root@m1:/home/hadoop# echo "hello idoall.org syslog" | nc localhost 5555root@m1:/home/hadoop# echo "hello idoall.org syslog 2" | nc localhost 5555

d)查看/home/hadoop/flume-1.5.0-bin/logs下是否生成文件,默认每30秒生成一个新文件

 

root@m1:/home/hadoop# ll /home/hadoop/flume-1.5.0-bin/logs总用量 272drwxr-xr-x 3 root root   4096 Aug 10 12:50 ./drwxr-xr-x 9 root root   4096 Aug 10 10:59 ../-rw-r--r-- 1 root root     50 Aug 10 12:49 1407646164782-1-rw-r--r-- 1 root root      0 Aug 10 12:49 1407646164782-2-rw-r--r-- 1 root root      0 Aug 10 12:50 1407646164782-3root@m1:/home/hadoop# cat /home/hadoop/flume-1.5.0-bin/logs/1407646164782-1 /home/hadoop/flume-1.5.0-bin/logs/1407646164782-2hello idoall.org sysloghello idoall.org syslog 2

8)案例8：Replicating Channel Selector

　　　　Flume支持Fan out流从一个源到多个通道。有两种模式的Fan out，分别是复制和复用。在复制的情况下，流的事件被发送到所有的配置通道。在复用的情况下，事件被发送到可用的渠道中的一个子集。Fan out流需要指定源和Fan out通道的规则。

 

　　　　这次我们需要用到m1,m2两台机器

 

　　　　　　a)在m1创建replicating_Channel_Selector配置文件

 

root@m1:/home/hadoop# vi /home/hadoop/flume-1.5.0-bin/conf/replicating_Channel_Selector.conf a1.sources = r1a1.sinks = k1 k2a1.channels = c1 c2 # Describe/configure the sourcea1.sources.r1.type = syslogtcpa1.sources.r1.port = 5140a1.sources.r1.host = localhosta1.sources.r1.channels = c1 c2a1.sources.r1.selector.type = replicating # Describe the sinka1.sinks.k1.type = avroa1.sinks.k1.channel = c1a1.sinks.k1.hostname = m1a1.sinks.k1.port = 5555 a1.sinks.k2.type = avroa1.sinks.k2.channel = c2a1.sinks.k2.hostname = m2a1.sinks.k2.port = 5555 # Use a channel which buffers events in memorya1.channels.c1.type = memorya1.channels.c1.capacity = 1000a1.channels.c1.transactionCapacity = 100 a1.channels.c2.type = memorya1.channels.c2.capacity = 1000a1.channels.c2.transactionCapacity = 100

b)在m1创建replicating_Channel_Selector_avro配置文件

 

root@m1:/home/hadoop# vi /home/hadoop/flume-1.5.0-bin/conf/replicating_Channel_Selector_avro.conf a1.sources = r1a1.sinks = k1a1.channels = c1 # Describe/configure the sourcea1.sources.r1.type = avroa1.sources.r1.channels = c1a1.sources.r1.bind = 0.0.0.0a1.sources.r1.port = 5555 # Describe the sinka1.sinks.k1.type = logger # Use a channel which buffers events in memorya1.channels.c1.type = memorya1.channels.c1.capacity = 1000a1.channels.c1.transactionCapacity = 100 # Bind the source and sink to the channela1.sources.r1.channels = c1a1.sinks.k1.channel = c1

 

c)在m1上将2个配置文件复制到m2上一份

root@m1:/home/hadoop/flume-1.5.0-bin# scp -r /home/hadoop/flume-1.5.0-bin/conf/replicating_Channel_Selector.conf root@m2:/home/hadoop/flume-1.5.0-bin/conf/replicating_Channel_Selector.confroot@m1:/home/hadoop/flume-1.5.0-bin# scp -r /home/hadoop/flume-1.5.0-bin/conf/replicating_Channel_Selector_avro.conf root@m2:/home/hadoop/flume-1.5.0-bin/conf/replicating_Channel_Selector_avro.conf

 

d)打开4个窗口，在m1和m2上同时启动两个flume agent

root@m1:/home/hadoop# /home/hadoop/flume-1.5.0-bin/bin/flume-ng agent -c . -f /home/hadoop/flume-1.5.0-bin/conf/replicating_Channel_Selector_avro.conf -n a1 -Dflume.root.logger=INFO,consoleroot@m1:/home/hadoop# /home/hadoop/flume-1.5.0-bin/bin/flume-ng agent -c . -f /home/hadoop/flume-1.5.0-bin/conf/replicating_Channel_Selector.conf -n a1 -Dflume.root.logger=INFO,console

 

 

e)然后在m1或m2的任意一台机器上，测试产生syslog

root@m1:/home/hadoop# echo "hello idoall.org syslog" | nc localhost 5140

 

f)在m1和m2的sink窗口，分别可以看到以下信息,这说明信息得到了同步：

14/08/10 14:08:18 INFO ipc.NettyServer: Connection to /192.168.1.51:46844 disconnected.14/08/10 14:08:52 INFO ipc.NettyServer: [id: 0x90f8fe1f, /192.168.1.50:35873 => /192.168.1.50:5555] OPEN14/08/10 14:08:52 INFO ipc.NettyServer: [id: 0x90f8fe1f, /192.168.1.50:35873 => /192.168.1.50:5555] BOUND: /192.168.1.50:555514/08/10 14:08:52 INFO ipc.NettyServer: [id: 0x90f8fe1f, /192.168.1.50:35873 => /192.168.1.50:5555] CONNECTED: /192.168.1.50:3587314/08/10 14:08:59 INFO ipc.NettyServer: [id: 0xd6318635, /192.168.1.51:46858 => /192.168.1.50:5555] OPEN14/08/10 14:08:59 INFO ipc.NettyServer: [id: 0xd6318635, /192.168.1.51:46858 => /192.168.1.50:5555] BOUND: /192.168.1.50:555514/08/10 14:08:59 INFO ipc.NettyServer: [id: 0xd6318635, /192.168.1.51:46858 => /192.168.1.50:5555] CONNECTED: /192.168.1.51:4685814/08/10 14:09:20 INFO sink.LoggerSink: Event: { headers:{Severity=0, flume.syslog.status=Invalid, Facility=0} body: 68 65 6C 6C 6F 20 69 64 6F 61 6C 6C 2E 6F 72 67 hello idoall.org }

 

 

 

 

 

Flume作用

Flume工作机制

Flume架构、组件

flume常用配置

Spooldir source

Exec source

Netcat source

Avro source

 

Hdfs sink

Log console sink

 

flume扩展编程

 

sqoop介绍

sqoop常用配置

Sqoop导入数据到hive

Sqoop导入数据到hbase

Sqoop导入数据到hdfs

动手练习（flume采集数据到hdfs，再导入hive）

 

 

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps35.png) 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

## **.Sqoop**

### Ø **Sqoop是什么？（\****了解*****）**

Sqoop是一款开源的工具，主要用于在HADOOP(HDFS/HBASE/Hive)与传统的数据库(mysql、 postgresql...)间进行数据的传递，可以将一个关系型数据库（例如 ： MySQL ,Oracle ,Postgres等）中的数据导进到Hadoop的HDFS中，也可以将HDFS的数据导进到关系型数据库中。

Sqoop项目开始于2009年，最早是作为Hadoop的一个第三方模块存在，后来为了让使用者能够快速部署，也为了让开发人员能够更快速的迭代开发，Sqoop独立成为一个Apache项目。

 

简单来说：sqoop是一款数据迁移工具。

工作机制：就是通过内置一些数据导入导出的MR程序，来为我们的数据迁移需求提供便利

 

官方网址：http://sqoop.apache.org/

下载：<http://archive.apache.org/dist/sqoop/>

 

### Ø **Sqoop安装：****（要有hadoop环境）**

1.上传安装包 sqoop-1.4.4.bin__hadoop-2.0.4-alpha.tar.gz，并解压

 \# tar -zxvf sqoop-1.4.4.bin__hadoop-2.0.4-alpha.tar.gz -C /itcast/

 

2.安装和配置

​	2.1在/etc/profile添加sqoop到环境变量

export SQOOP_HOME=/itcast/sqoop-1.4.4.bin__hadoop-2.0.4-alpha

export PATH=$PATH:$SQOOP_HOME/bin

2.2让配置生效

source /etc/profile

3.将数据库连接驱动拷贝到$SQOOP_HOME/lib里

### Ø **测试Sqooq使用（\*****会用*****）**

 

第一类：数据库中的数据导入到HDFS上

\# sqoop import --connect jdbc:mysql://hdp-server-01:3306/baba --username root --password root --table bbs_detail 

​		

​		指定输出路径、指定数据分隔符

​		# sqoop import --connect jdbc:mysql://hdp-server-01:3306/baba --username root --password root --table bbs_detail --target-dir '/sqoop/td' --fields-terminated-by '\t'

​		

​		指定MapTask数量 -m 

​		#sqoop import --connect jdbc:mysql://hdp-server-01:3306/baba --username root --password root  --table bbs_detail --target-dir '/sqoop/td1' --fields-terminated-by '\t' -m 1

 

​		增加where条件, 注意：条件必须用引号引起来

​		# sqoop import --connect jdbc:mysql://hdp-server-01:3306/baba --username root --password root  --table bbs_detail --where 'id>30' --target-dir '/sqoop/td2' --fields-terminated-by '\001' -m 1

 

​		增加query语句(使用 \ 将语句换行)

​		sqoop import --connect jdbc:mysql://hdp-server-01:3306/baba --username root --password root \

--query 'SELECT id,order_id,product_id FROM bbs_detail where id > 30 AND $CONDITIONS' --split-by bbs_detail.id --target-dir '/sqoop/td3'		

​		注意：如果使用--query这个命令的时候，需要注意的是where后面的参数，AND $CONDITIONS这个参数必须加上

​		而且存在单引号与双引号的区别，如果--query后面使用的是双引号，那么需要在$CONDITIONS前加上\即\$CONDITIONS

​		如果设置map数量为1个时即-m 1，不用加上--split-by ${tablename.column}，否则需要加上

​		

***从数据库中导入数据到hive

sqoop import --hive-import --connect jdbc:mysql://hdp-server-01:3306/baba --username root --password root --table bbs_detail

 

 

 

​	第二类：将HDFS上的数据导出到数据库中

​		sqoop export --connect jdbc:mysql://hdp-server-01:3306/test  --username root --password root --export-dir '/myorder/data' --table myorder --columns id,order_id --fields-terminated-by ','  -m 2

 

 

 

注意：以上测试要配置mysql远程连接

​	GRANT ALL PRIVILEGES ON mytest.* TO 'root'@'192.168.0.104' IDENTIFIED BY 'itcast' WITH GRANT OPTION;

​	FLUSH PRIVILEGES; 

​	

​	GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'itcast' WITH GRANT OPTION;

​	FLUSH PRIVILEGES

## 2.**Storm**

### Ø **Storm简介：（\****了解****）**

官方网址：<http://storm.apache.org/>

Apache Storm是一个免费、开源的分布式实时计算系统。使用它可以轻松实现数据流的实时处理。Strom很简单，可以用任何编程语言！

 

**Storm用例：**实时在线分析，机器学习，连续计算，分布式RPC，ETL等。

**Strom特点：**

快速：基准时钟在超过一百万元组每秒处理的每个节点。

简易的设置：有可扩展性、容错性，保证了数据的处理能力，并且易于设置和操作。

 

### Ø **Storm的发展（\***了解****）**

**流式计算的历史**

​    早在7、8年前诸如UC伯克利、斯坦福等大学就开始了对流式数据处理的研究，但是由于更多的关注于金融行业的业务场景或者互联网流量监控的业务场景，以及当时互联网数据场景的限制，造成了研究多是基于对传统数据库处理的流式化，对流式框架本身的研究偏少。目前这样的研究逐渐没有了声音，工业界更多的精力转向了实时数据库。

　　2010年Yahoo！对S4的开源，2011年twitter对Storm的开源，改变了这个情况。以前互联网的开发人员在做一个实时应用的时候，除了要关注应用逻辑计算处理本身，还要为了数据的实时流转、交互、分布大伤脑筋。但是现在情况却大为不同，以Storm为例，开发人员可以快速的搭建一套健壮、易用的实时流处理框架，配合SQL产品或者NoSQL产品或者MapReduce计算平台，就可以低成本的做出很多以前很难想象的实时产品：比如一淘数据部的量子恒道品牌旗下的多个产品就是构建在实时流处理平台上的。

 

**流式计算的最新进展**

在数据处理时间和方式上，Storm与Hadoop MapReduce基本上是两个对立面，而这两个技术具备整合可能性极大程度该归结于YARN这个集群管理层。Hortonworks当下正在致力于通过新型处理框架Tez 来 提高Hive的速度，同时YARN还允许Hadoop用户 运行Spark内存处理框架。同时， 微软也在使用YARN让Hadoop更加适合机器学习用例。

　　此外，通过YARN，同集群上同时运行HBase、 Giraph等不同技术也成为可能。此外，集群管理技术Mesos(加州大学伯克利分校出品，现已成为Apache项目) 同样支持了类似YARN功能，尽管其不是像YARN这样与HDFS捆绑。

更多技术的整合预示Hadoop这个大数据处理平台绝不是昙花一现，同时也会让Hadoop在大数据应用程序领域获得更高的统治力。

 

### Ø **Storm与Hadoop的对比（\****理解****）**

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps36.jpg) 

 

 

**Topology 与 Mapreduce** 

一个关键的区别是： 一个MapReduce job最终会结束， 而一个topology永远会运行（除非你手动kill掉）

 

Nimbus 与 ResourManager

在Storm的集群里面有两种节点： 控制节点（master node）和工作节点（worker node）。控制节点上面运行一个叫Nimbus后台程序，它的作用类似Hadoop里面的JobTracker。Nimbus负责在集群里面分发代码，分配计算任务给机器， 并且监控状态。

 

Supervisor (worker进程)与NodeManager(YarnChild)

每一个工作节点上面运行一个叫做Supervisor的节点。Supervisor会监听分配给它那台机器的工作，根据需要启动/关闭工作进程。每一个工作进程执行一个topology的一个子集；一个运行的topology由运行在很多机器上的很多工作进程组成。 

 

 

 

 

 

 

 

 

 

 

 

 

### **Storm的运作机制**

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps37.jpg) 

 

 

 

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps38.jpg) 

 

 

 

 

 

 

 

 

 

 

 

 

 

Strom集群：

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps39.jpg) 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps40.png) 

 

 

 

 

 

 

 

 

 

 

 

 

 

### Ø **Storm集群架构体系：（\****理解*****）**

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps41.png) 

 

### Ø **Storm集群部署（\***必须掌握****）**

**1、安装一个zookeeper集群**

 

**2、上传storm的安装包，解压**

 

**3、修改配置文件storm.yaml**

 

\#所使用的zookeeper集群主机

storm.zookeeper.servers:

​     \- "zookeeperServer1"

​     \- "zookeeperServer2"

​     \- "zookeeperServer3"

 

\#nimbus所在的主机名

nimbus.host: "zookeeperServer1"

 

//可以指定worker数量,如果不指定默认为4个

supervisor.slots.ports:- 6701- 6702- 6703- 6704- 6705- 6706

 

**4.将配置好的storm环境复制到zookeeperServer2，zookeeperServer3**

\# scp -r /itcast/apache-storm-0.9.2-incubating  zookeeperServer2:/itcast

\# scp -r /itcast/apache-storm-0.9.2-incubating  zookeeperServer3:/itcast

**启动storm** 

\# cd /itcast/apache-storm-0.9.2-incubating/bin

在nimbus主机上

//启动协调管理nimbus

./storm nimbus 1>/dev/null 2>&1 &

//启动web管理界面 启动后可以通过nimbus主机名：8080端口进行仿问

./storm ui 1>/dev/null 2>&1 &

 

在supervisor主机上

./storm supervisor 1>/dev/null 2>&1 &

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

### Ø **Storm的基本概念（\****理解****）**

在深入理解Storm之前，需要了解一些概念：

Topologies ： 拓扑，也俗称一个任务，类似于mapreduce中的job

Spouts ： 拓扑的消息源

Bolts ： 拓扑的处理逻辑单元

tuple：消息元组

Streams ： 流

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps42.jpg) 

Stream groupings ：流的分组策略

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps43.jpg) 

 

 

Tasks ： 任务处理单元

Executor :工作线程

Workers ：工作进程

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps44.jpg) 

 

 

 

 

 

Configuration ： topology的配置

 

**Topologies 逻辑单元：Spouts 与 Bolts 消息**

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps45.jpg) 

 

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps46.jpg) 

 

### Ø **电信实时统计例子：（\****扩展****）**

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps47.jpg) 

RandomWordSpout.java

**package** cn.itcast.stormdemo;

**import** java.util.Map;

**import** java.util.Random;

**import** backtype.storm.spout.SpoutOutputCollector;

**import** backtype.storm.task.TopologyContext;

**import** backtype.storm.topology.OutputFieldsDeclarer;

**import** backtype.storm.topology.base.BaseRichSpout;

**import** backtype.storm.tuple.Fields;

**import** backtype.storm.tuple.Values;

**import** backtype.storm.utils.Utils;

**public** **class** RandomWordSpout **extends** BaseRichSpout{

​	**private** SpoutOutputCollector collector;

​	//模拟一些数据

​	String[] words = {"iphone","xiaomi","mate","sony","sumsung","moto","meizu"};

​	

​	//不断地往下一个组件发送tuple消息

​	//这里面是该spout组件的核心逻辑

​	@Override

​	**public** **void** nextTuple() {

​		//可以从kafka消息队列中拿到数据,简便起见，我们从words数组中随机挑		//选一个商品名发送出去

​		Random random = **new** Random();

​		**int** index = random.nextInt(words.length);

​		//通过随机数拿到一个商品名

​		String godName = words[index];

​		//将商品名封装成tuple，发送消息给下一个组件

​		collector.emit(**new** Values(godName));

​		//每发送一个消息，休眠500ms

​		Utils.*sleep*(500);

​	}

​	//初始化方法，在spout组件实例化时调用一次

​	@Override

​	**public** **void** open(Map conf, TopologyContext context, SpoutOutputCollector collector) {

​		**this**.collector = collector;

​	}

​	//声明本spout组件发送出去的tuple中的数据的字段名

​	@Override

​	**public** **void** declareOutputFields(OutputFieldsDeclarer declarer) {

​		declarer.declare(**new** Fields("orignname"));

​	}

}

SuffixBolt.java

**package** cn.itcast.stormdemo;

**import** java.io.FileWriter;

**import** java.io.IOException;

**import** java.util.Map;

**import** java.util.UUID;

**import** backtype.storm.task.TopologyContext;

**import** backtype.storm.topology.BasicOutputCollector;

**import** backtype.storm.topology.OutputFieldsDeclarer;

**import** backtype.storm.topology.base.BaseBasicBolt;

**import** backtype.storm.tuple.Tuple;

**public** **class** SuffixBolt **extends** BaseBasicBolt{

​	FileWriter fileWriter = **null**;

​	//在bolt组件运行过程中只会被调用一次

​	@Override

​	**public** **void** prepare(Map stormConf, TopologyContext context) {

​		**try** {

​			fileWriter = **new** FileWriter("/root/stormoutput/"+UUID.*randomUUID*());

​		} **catch** (IOException e) {

​			**throw** **new** RuntimeException(e);

​		}

​	}

​	//该bolt组件的核心处理逻辑

​	//每收到一个tuple消息，就会被调用一次

​	@Override

​	**public** **void** execute(Tuple tuple, BasicOutputCollector collector) {

​		//先拿到上一个组件发送过来的商品名称

​		String upper_name = tuple.getString(0);

​		String suffix_name = upper_name + "_itisok";

​		//为上一个组件发送过来的商品名称添加后缀

​		**try** {

​			fileWriter.write(suffix_name);

​			fileWriter.write("\n");

​			fileWriter.flush();

​			

​		} **catch** (IOException e) {

​			**throw** **new** RuntimeException(e);

​		}

​	}

​	//本bolt已经不需要发送tuple消息到下一个组件，所以不需要再声明tuple	//的字段

​	@Override

​	**public** **void** declareOutputFields(OutputFieldsDeclarer arg0) {

​	}

}

UpperBolt.java

**package** cn.itcast.stormdemo;

**import** backtype.storm.topology.BasicOutputCollector;

**import** backtype.storm.topology.OutputFieldsDeclarer;

**import** backtype.storm.topology.base.BaseBasicBolt;

**import** backtype.storm.tuple.Fields;

**import** backtype.storm.tuple.Tuple;

**import** backtype.storm.tuple.Values;

**public** **class** UpperBolt **extends** BaseBasicBolt{

​	//业务处理逻辑

​	@Override

​	**public** **void** execute(Tuple tuple, BasicOutputCollector collector) {

​		//先获取到上一个组件传递过来的数据,数据在tuple里面

​		String godName = tuple.getString(0);

​		//将商品名转换成大写

​		String godName_upper = godName.toUpperCase();

​		//将转换完成的商品名发送出去

​		collector.emit(**new** Values(godName_upper));

​		

​	}

​	//声明该bolt组件要发出去的tuple的字段

​	@Override

​	**public** **void** declareOutputFields(OutputFieldsDeclarer declarer) {

​		declarer.declare(**new** Fields("uppername"));

​	}

}

TopoMain.java

**package** cn.itcast.stormdemo;

**import** backtype.storm.Config;

**import** backtype.storm.StormSubmitter;

**import** backtype.storm.generated.StormTopology;

**import** backtype.storm.topology.TopologyBuilder;

/**

 \* 组织各个处理组件形成一个完整的处理流程，就是所谓的topology(类似于                            mapreduce程序中的job)

 \* 并且将该topology提交给storm集群去运行，topology提交到集群后就将永无休止地运行，除非人为或者异常退出

 *

 */

**public** **class** TopoMain {

​	**public** **static** **void** main(String[] args) **throws** Exception {

​		TopologyBuilder builder = **new** TopologyBuilder();

​		//将我们的spout组件设置到topology中去 

​		//parallelism_hint ：4  表示用4个excutor来执行这个组件

​		//setNumTasks(8) 设置的是该组件执行时的并发task数量，也就意味着1个excutor会运行2个task

​		builder.setSpout("randomspout", **new** RandomWordSpout(), 4).setNumTasks(8);

​		//将大写转换bolt组件设置到topology，并且指定它接收randomspout组件的消息

​		//.shuffleGrouping("randomspout")包含两层含义：

​		//1、upperbolt组件接收的tuple消息一定来自于randomspout组件

​		//2、randomspout组件和upperbolt组件的大量并发task实例之间收发消息时采用的分组策略是随机分组shuffleGrouping

​		builder.setBolt("upperbolt", **new** UpperBolt(), 4).shuffleGrouping("randomspout");

​		//将添加后缀的bolt组件设置到topology，并且指定它接收upperbolt组件的消息

​		builder.setBolt("suffixbolt", **new** SuffixBolt(), 4).shuffleGrouping("upperbolt");

​		//用builder来创建一个topology

​		StormTopology demotop = builder.createTopology();

​		

​		

​		//配置一些topology在集群中运行时的参数

​		Config conf = **new** Config();

​		//这里设置的是整个demotop所占用的槽位数，也就是worker的数量

​		conf.setNumWorkers(4);

​		conf.setDebug(**true**);

​		conf.setNumAckers(0);

​		//将这个topology提交给storm集群运行

​		StormSubmitter.*submitTopology*("demotopo", conf, demotop);

​	}

}

 

把工程打成jar包，提交集群运行。

提交的Topologies命令格式如下：

 

命令格式：storm jar 【jar路径】 【拓扑包名.拓扑类名】【参数】

如：

storm jar /home/storm/storm-starter.jar storm.starter.WordCountTopology wordcountTop;

 

\#提交storm-starter.jar到远程集群，并启动wordcountTop拓扑。

 

 

### Ø **Storm 常用命令（\****记住****）**

1、 **启动nimbus后台程序**

2、 命令格式：storm nimbus

 

3、 **启动supervisor后台程序**

 

4、 命令格式：storm supervisor

 

4、**启动ui服务**

命令格式：storm ui

 

5、 **提交Topologies**

命令格式：storm jar 【jar路径】 【拓扑包名.拓扑类名】【stormIP地址】【storm端口】【拓扑名称】【参数】

eg：

storm jar /home/storm/storm-starter.jar storm.starter.WordCountTopology wordcountTop;


\#提交storm-starter.jar到远程集群，并启动wordcountTop拓扑。

 

 

**5、停止Topologies**

查看当前运行的topo： storm list

命令格式：storm kill 【拓扑名称】

样例：storm kill wordcountTop

\#杀掉wordcountTop拓扑。

 

### Ø **Storm 相关配置项（\***知道****）**

在storm.yaml中常用的几个选项

storm.zookeeper.root

Storm在zookeeper集群中的根目录，默认是“/”

 

topology.workers

每个Topology运行时的worker的默认数目，若在代码中设置，则此选项值被覆盖

 

storm.zookeeper.servers

zookeeper集群的节点列表

 

storm.local.dir

Storm用于存储jar包和临时文件的本地存储目录

 

ui.port   

Storm集群的UI地址端口号，默认是8080

 

nimbus.host:

Nimbus节点的host

 

supervisor.slots.ports

Supervisor节点的worker占位槽，集群中的所有Topology公用这些槽位数，即使提交时设置了较大数值的槽位数，系统也会按照当前集群中实际剩余的槽位数来进行分配，当所有的槽位数都分配完时，新提交的Topology只能等待，系统会一直监测是否有空余的槽位空出来，如果有，就再次给新提交的Topology分配。

 

### Ø **Storm编程接口（\****理解****）**

l **Spouts**

Spout是Stream的消息产生源， Spout组件的实现可以通过继承BaseRichSpout类或者其他*Spout类来完成，也可以通过实现IRichSpout接口来实现。

 

需要根据情况实现Spout类中重要的几个方法有：

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps48.jpg) 

**open方法**

​    当一个Task被初始化的时候会调用此open方法。一般都会在此方法中对发送Tuple的对象SpoutOutputCollector和配置对象TopologyContext初始化。

 

示例如下：

1 public void open(Map conf, TopologyContext context, SpoutOutputCollector collector) {

​	this._collector = collector; 

}

**getComponentConfiguration方法**

​    此方法用于声明针对当前组件的特殊的Configuration配置。

示例如下：

public Map<String, Object> getComponentConfiguration() { 

​      if(!_isDistributed) {

​	Map<String, Object> ret = new HashMap<String, Object>(); 

 	ret.put(Config.TOPOLOGY_MAX_TASK_PARALLELISM, 3); 

 	return ret;10 11 

​      } else {

​	return null;

​     }

}

这里便是设置了Topology中当前Component的线程数量上限。

 **nextTuple方法**

​    这是Spout类中最重要的一个方法。发射一个Tuple到Topology都是通过这个方法来实现的。

示例如下：

public void nextTuple() { 

​     Utils.sleep(100); 

​     final String[] words = new String[] {"twitter","facebook","google"}; 

​     final Random rand = new Random(); 

​     final String word = words[rand.nextInt(words.length)];

​     _collector.emit(new Values(word));

} 

​    这里便是从一个数组中随机选取一个单词作为Tuple，然后通过_collector发送到Topology。

**declareOutputFields方法**

此方法用于声明当前Spout的Tuple发送流。

Stream流的定义是通过OutputFieldsDeclare.declare方法完成的，其中的参数包括了发送的域Fields。

示例如下：

 

public void declareOutputFields(OutputFieldsDeclarer declarer) {

​	declarer.declare(new Fields("word"));

 }

 

​    另外，除了上述几个方法之外，还有ack、fail和close方法等;

Storm在监测到一个Tuple被成功处理之后会调用ack方法，处理失败会调用fail方法;

这两个方法在BaseRichSpout等类中已经被隐式的实现了。

 

l **Bolts**

​    Bolt类接收由Spout或者其他上游Bolt类发来的Tuple，对其进行处理。Bolt组件的实现可以通过继承BasicRichBolt类或者IRichBolt接口来完成。

​    Bolt类需要实现的主要方法有：

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps49.jpg) 

**prepare方法**

​    此方法和Spout中的open方法类似，为Bolt提供了OutputCollector，用来从Bolt中发送Tuple。Bolt中Tuple的发送可以在prepare方法中、execute方法中、cleanup等方法中进行，一般都是些在execute中。

​    示例如下：

public void prepare(Map conf, TopologyContext context, OutputCollector collector) {

​	 this. _collector = collector;

}

**getComponentConfiguration方法**

​    和Spout类一样，在Bolt中也可以有getComponentConfiguration方法。

​    示例如下：

public Map<String, Object> getComponentConfiguration() {

​     Map<String, Object> conf = new HashMap<String, Object>();

​     conf.put(Config.TOPOLOGY_TICK_TUPLE_FREQ_SECS,      

​     emitFrequencyInSeconds);

​     return conf;

 } 

​    此例定义了从系统组件“_system”的“_tick”流中发送Tuple到当前Bolt的频率，当系统需要每隔一段时间执行特定的处理时，就可以利用这个系统的组件的特性来完成。

**execute方法**

​    这是Bolt中最关键的一个方法，对于Tuple的处理都可以放到此方法中进行。具体的发送也是在execute中通过调用emit方法来完成的。

 

有两种情况，一种是emit方法中有两个参数，另一个种是有一个参数。

(1)emit有一个参数：此唯一的参数是发送到下游Bolt的Tuple，此时，由上游发来的旧的Tuple在此隔断，新的Tuple和旧的Tuple不再属于同一棵Tuple树。新的Tuple另起一个新的Tuple树。

 

(2)emit有两个参数：第一个参数是旧的Tuple的输入流，第二个参数是发往下游Bolt的新的Tuple流。此时，新的Tuple和旧的Tuple是仍然属于同一棵Tuple树，即，如果下游的Bolt处理Tuple失败，则会向上传递到当前Bolt，当前Bolt根据旧的Tuple流继续往上游传递，申请重发失败的Tuple。保证Tuple处理的可靠性。

**declareOutputFields方法**

用于声明当前Bolt发送的Tuple中包含的字段，和Spout中类似。

​    示例如下：

public void declareOutputFields(OutputFieldsDeclarer declarer) {

 	declarer.declare(new Fields("obj", "count", 	"actualWindowLengthInSeconds"));

 } 

​    此例说明当前Bolt类发送的Tuple包含了三个字段："obj", "count", "actualWindowLengthInSeconds"。

l **Topology**

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps50.jpg) 

### Ø **Topology运行机制（\***理解****）**

(1)Storm提交后，会把代码首先存放到Nimbus节点的inbox目录下，之后，会把当前Storm运行的配置生成一个stormconf.ser文件放到Nimbus节点的stormdist目录中，在此目录中同时还有序列化之后的Topology代码文件；

 

(2)在设定Topology所关联的Spouts和Bolts时，可以同时设置当前Spout和Bolt的executor数目和task数目，默认情况下，一个Topology的task的总和是和executor的总和一致的。之后，系统根据worker的数目，尽量平均的分配这些task的执行。worker在哪个supervisor节点上运行是由storm本身决定的；

(3)任务分配好之后，Nimbes节点会将任务的信息提交到zookeeper集群，同时在zookeeper集群中会有workerbeats节点，这里存储了当前Topology的所有worker进程的心跳信息；

 

(4)Supervisor节点会不断的轮询zookeeper集群，在zookeeper的assignments节点中保存了所有Topology的任务分配信息、代码存储目录、任务之间的关联关系等，Supervisor通过轮询此节点的内容，来领取自己的任务，启动worker进程运行；

 

(5)一个Topology运行之后，就会不断的通过Spouts来发送Stream流，通过Bolts来不断的处理接收到的Stream流，Stream流是无界的。

 

最后一步会不间断的执行，除非手动结束Topology。

 

   Topology中的Stream处理时的方法调用过程如下：

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps51.jpg) 

有几点需要说明的地方：

   (1)每个组件(Spout或者Bolt)的构造方法和declareOutputFields方法都只被调用一次。

   (2)open方法、prepare方法的调用是多次的。入口函数中设定的setSpout或者setBolt里的并行度参数指的是executor的数目，是负责运行组件中的task的线程 的数目，此数目是多少，上述的两个方法就会被调用多少次，在每个executor运行的时候调用一次。相当于一个线程的构造方法。

   (3)nextTuple方法、execute方法是一直被运行的，nextTuple方法不断的发射Tuple，Bolt的execute不断的接收Tuple进行处理。只有这样不断地运行，才会产生无界的Tuple流，体现实时性。相当于线程的run方法。

   (4)在提交了一个topology之后，Storm就会创建spout/bolt实例并进行序列化。之后，将序列化的component发送给所有的任务所在的机器(即Supervisor节 点)，在每一个任务上反序列化component。

   (5)Spout和Bolt之间、Bolt和Bolt之间的通信，是通过zeroMQ的消息队列实现的。

   (6)上图没有列出ack方法和fail方法，在一个Tuple被成功处理之后，需要调用ack方法来标记成功，否则调用fail方法标记失败，重新处理这个Tuple。

**终止Topology**

**通过在Nimbus节点利用如下命令来终止一个Topology的运行：**

**bin/storm kill topologyName**

**kill之后，可以通过UI界面查看topology状态，会首先变成KILLED状态，在清理完本地目录和zookeeper集群中的和当前Topology相关的信息之后，此Topology就会彻底消失**

 

 

 

 

 

 

 

 

 

 

## 3.**Kafka**

官方网址：<https://kafka.apache.org/>

源码下载：http://archive.apache.org/dist/kafka/

 

### Ø **Kafka简介：（\****了解***）**

Kafka是一个分布式的消息缓存系统，用于日志处理的分布式消息队列。日志数据容量大，但对可靠性要求不高，其日志数据主要包括用户行为（登录、浏览、点击、分享、喜欢）以及系统运行日志（CPU、内存、磁盘、网络、系统及进程状态）。

当前很多的消息队列服务提供可靠交付保证，并默认是即时消费（不适合离线）。高可靠交付对日志不是必须的，故可通过降低可靠性来提高性能，同时通过构建分布式的集群，允许消息在系统中累积，使得kafka同时支持离线和在线日志处理。

 

### Ø **Kafka架构（\***理解***）**

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps52.jpg)

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps53.jpg)

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml14396\wps54.jpg)

l kafka集群中的服务器都叫做broker

l kafka有两类客户端，一类叫producer（消息生产者），一类叫做consumer（消息消费者），客户端和broker服务器之间采用tcp协议连接

l kafka中不同业务系统的消息可以通过topic进行区分，而且每一个消息topic都会被分区，以分担消息读写的负载

l 每一个分区都可以有多个副本，以防止数据的丢失

l 某一个分区中的数据如果需要更新，都必须通过该分区所有副本中的leader来更新

l 消费者可以分组，比如有两个消费者组A和B，共同消费一个topic：order_info,A和B所消费的消息不会重复

比如 order_info 中有100个消息，每个消息有一个id,编号从0-99，那么，如果A组消费0-49号，B组就消费50-99号

l 消费者在具体消费某个topic中的消息时，可以指定起始偏移量

### Ø **集群安装(\***实践***)**

1、上传kafka安装文件到zookeeperServer1进行解压

\# tar -zxvf kafka_2.10-0.8.1.1.tgz -C /itcast/

\# mkdir /itcast/kafka_2.10-0.8.1.1/kafka-logs

2、修改server.properties

broker.id=0

zookeeper.connect=zookeeperServer1:2181,zookeeperServer2:2181,zookeeperServer3:2181

log.dirs=/itcast/kafka_2.10-0.8.1.1/kafka-logs

3、将zookeeperServer1的kafka复制到其它机器（zookeeperServer2，zookeeperServer3）

\# scp -r /itcast/kafka_2.10-0.8.1.1 zookeeperServer2:/itcast/

\# vim /itcast/kafka_2.10-0.8.1.1/config/server.properties

broker.id=1 //修改broder.id

 

\# scp -r /itcast/kafka_2.10-0.8.1.1 zookeeperServer3:/itcast/

\# vim /itcast/kafka_2.10-0.8.1.1/config/server.properties

broker.id=2 //修改broder.id

 

3、将zookeeper集群启动

 

4、在每一台节点上启动broker

bin/kafka-server-start.sh config/server.properties

或在后台启动

bin/kafka-server-start.sh config/server.properties 1>/dev/null 2>&1 &

 

如果启动报错：

Unrecognized VM option 'UseCompressedOops'Error: Could not create the Java Virtual Machine.Error: A fatal exception has occurred. Program will exit.

则需要修改脚本： kafka-run-class.sh

把113行的“-XX:+UseCompressedOops”去掉。

这是因为32位jvm不支持参数“-XX:+UseCompressedOops”

 

 

 

5、在kafka集群中创建一个topic

bin/kafka-topics.sh --create --zookeeper  hdp-server-01:2181 --replication-factor 3 --partitions 1 --topic urls

 

6、用一个producer向某一个topic中写入消息

bin/kafka-console-producer.sh --broker-list hdp-server-01:9092 --topic urls

 

7、用一个comsumer从某一个topic中读取信息

bin/kafka-console-consumer.sh --zookeeper hdp-server-01:2181 --from-beginning --topic urls

 

8、查看一个topic的分区及副本状态信息

bin/kafka-topics.sh --describe --zookeeper hdp-server-01:2181 --topic urls

 

 

 

### Ø **发送业务消息客户端编写（\***实践***）**

Java工程中导入${KAFKA_HOME}/lib下所有jar包

 

ProducerDemo.javad

package cn.itcast.kafka;

 

import java.util.Properties;

 

import kafka.javaapi.producer.Producer;

import kafka.producer.KeyedMessage;

import kafka.producer.ProducerConfig;

 

public class ProducerDemo {

​	public static void main(String[] args) throws Exception {

​		Properties props = new Properties();

​		props.put("zk.connect", "zookeeperServer1:2181,zookeeperServer2:2181,zookeeperServer3:2181");

​		props.put("metadata.broker.list","zookeeperServer1:9092,zookeeperServer2:9092,zookeeperServer3:9092");

​		props.put("serializer.class", "kafka.serializer.StringEncoder");

​		ProducerConfig config = new ProducerConfig(props);

​		Producer<String, String> producer = new Producer<String, String>(config);

 

​		// 发送业务消息

​		// 读取文件 读取内存数据库 读socket端口

​		for (int i = 1; i <= 100; i++) {

​			Thread.sleep(500);

​			producer.send(new KeyedMessage<String, String>("order",

​					"我是第" + i + "次来买东本西！"));

​		}

 

​	}

}

 

 

### Ø **接收业务消息客户端编写（\***实践***）**

ConsumerDemo.java

 

package cn.itcast.kafka;

 

import java.util.HashMap;

import java.util.List;

import java.util.Map;

import java.util.Properties;

 

import kafka.consumer.Consumer;

import kafka.consumer.ConsumerConfig;

import kafka.consumer.ConsumerIterator;

import kafka.consumer.KafkaStream;

import kafka.javaapi.consumer.ConsumerConnector;

import kafka.message.MessageAndMetadata;

 

public class ConsumerDemo {

​	private static final String topic = "order";

​	private static final Integer threads = 1;

 

​	public static void main(String[] args) {

​		

​		Properties props = new Properties();

​		props.put("zookeeper.connect", "zookeeperServer1:2181,zookeeperServer2:2181,zookeeperServer3:2181");

​		props.put("group.id", "1111");

​		props.put("auto.offset.reset", "smallest");

 

​		ConsumerConfig config = new ConsumerConfig(props);

​		ConsumerConnector consumer =Consumer.createJavaConsumerConnector(config);

​		Map<String, Integer> topicCountMap = new HashMap<String, Integer>();

​		topicCountMap.put(topic, threads);

​		topicCountMap.put("order", 1);

​		Map<String, List<KafkaStream<byte[], byte[]>>> consumerMap = consumer.createMessageStreams(topicCountMap);

​		List<KafkaStream<byte[], byte[]>> streams = consumerMap.get("order");

​		

​		for(final KafkaStream<byte[], byte[]> kafkaStream : streams){

​			new Thread(new Runnable() {

​				@Override

​				public void run() {

​					for(MessageAndMetadata<byte[], byte[]> mm : kafkaStream){

​						String msg = new String(mm.message());

​						System.out.println(msg);

​					}

​				}

​			

​			}).start();

​		

​		}

​	}

}

 