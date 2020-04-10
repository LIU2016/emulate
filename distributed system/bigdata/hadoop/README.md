hadoop启动以及配置

```xshell
cd etc/hadoop/
vi core-site.xml 
vi hdfs-site.xml 
vi yarn-site.xml
vi mapred-site.xml
vi workers
vi hadoop-env.sh
cd bin/
./hadoop namenode -format

手动启动：
cd ../sbin/
./hadoop-daemon.sh start namenode
./hadoop-daemon.sh start datanode
./hadoop-daemon.sh start secondarynamenode
./yarn-daemon.sh start resourcemanager
./yarn-daemon.sh start nodemanager

自动启动：
免密登录：
ssh-keygen
ssh-copy-id hadoop1 拷贝到目标主机
ssh hadoop1
root用户在/hadoop/sbin路径下： 
将start-dfs.sh，stop-dfs.sh两个文件顶部添加以下参数
HDFS_DATANODE_USER=root
              HADOOP_SECURE_DN_USER=hdfs
              HDFS_NAMENODE_USER=root
              HDFS_SECONDARYNAMENODE_USER=root
start-yarn.sh，stop-yarn.sh顶部也需添加以下
            YARN_RESOURCEMANAGER_USER=root
            HADOOP_SECURE_DN_USER=yarn
            YARN_NODEMANAGER_USER=root
./start-dfs.sh
./start-yarn.sh

集群：
1，配置域名IP映射
2，拷贝hadoop到其他服务器
3，配置workers
4，启动start-dfs\start-yarn即可。
5，若要新增则copy到新的节点后，手动启动datanode、datamanager即可。然后./start-balancer.sh

```

hadoop-env.sh配置：

```
export JAVA_HOME=/usr/jdk1.8.0_102/
```

core-site.xml配置：

```
<configuration>
<property>
<name>fs.defaultFS</name>
<value>hdfs://hadoop1:9000/</value>	
</property>
<property>
<name>hadoop.tmp.dir</name>
<value>/usr/hadoop/tmp</value>
</property>
</configuration>
```

hdfs-site.xml配置：

```
<configuration>
<property>
<name>dfs.replication</name>
<value>1</value>
</property>
</configuration>
```

yarn-site.xml配置：

```
<property>
<name>yarn.resourcemanager.hostname</name>
<value>hadoop1</value>
</property>
<property>
<name>yarn.nodemanager.aux-services</name>
<value>mapreduce_shuffle</value>
</property>
<property>
<name>yarn.resourcemanager.aux-services</name>
<value>mapreduce_shuffle</value>
</property>
<property>
<name>yarn.nodemanager.vmem-check-enabled</name>
<value>false</value>
<description>Whether virtual memory limits will be enforced for containers</description>
</property>
<property>
<name>yarn.nodemanager.vmem-pmem-ratio</name>
<value>4</value>
<description>Ratio between virtual memory to physical memory when setting memory limits for containers</description>
</property>
```

mapred-site.xml配置：

``` 
<configuration>
<property>
<name>mapreduce.framework.name</name>
<value>yarn</value>
</property>
<property>
<name>yarn.app.mapreduce.am.env</name>
<value>HADOOP_MAPRED_HOME=/usr/hadoop/hadoop-3.1.3/</value>
</property>
<property>
<name>mapreduce.map.env</name>
<value>HADOOP_MAPRED_HOME=/usr/hadoop/hadoop-3.1.3/</value>
</property>   
<property>
<name>mapreduce.reduce.env</name>
<value>HADOOP_MAPRED_HOME=/usr/hadoop/hadoop-3.1.3/</value>
</property>
</configuration>
```

运行mapreduce：

```properties
将程序提交给hadoop:
./hadoop jar ../../microservice-hadoop-1.1.1-SNAPSHOT.jar com.adm.springcloud.mapreduce.ObjectDriver

http://192.168.254.138:8088/cluster yarn监控页面


```

hdfs运行机制：

![17.Hdfs读数据流程](D:\自我提升\视频\bigdata\拓薪教育-大数据Hadoop第1章\截图\17.Hdfs读数据流程.png)

![17.Hdfs写数据流程](D:\自我提升\视频\bigdata\拓薪教育-大数据Hadoop第1章\截图\17.Hdfs写数据流程.png)

mapreduce运行机制：

![23.Mapreduce框架运行机制](D:\自我提升\视频\bigdata\大数据Hadoop第2章\截图\23.Mapreduce框架运行机制.png)

![24.Mapreduce运行机制的数据流程](D:\自我提升\视频\bigdata\大数据Hadoop第2章\截图\24.Mapreduce运行机制的数据流程.png)

yarn运行机制：

![44](D:\自我提升\视频\bigdata\大数据Hadoop第3章\截图\44.png)





mapreduce练习：

```
共同好友-->分两个map\reduce程序执行

连表查询-->map端join（利用distributeCache,适用于大小表join的情况）和reduce端join（容易出现数据倾斜，降低效率）

倒排索引-->
```



hadoop HA高可用集群搭建

```
1，配置zookeeper集群
2，配置hadoop，然后拷贝到多台服务器上。
3，启动journalname节点：
sbin/hadoop-daemon.sh start journalnode
4，start-yarn.sh\start-dfs.sh添加，然后启动：
HDFS_DATANODE_USER=root
HADOOP_SECURE_DN_USER=hdfs
HDFS_NAMENODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root
HDFS_JOURNALNODE_USER=root
HDFS_ZKFC_USER=root
5，启动zkfc：
 sbin/hadoop-daemon.sh start zkfc
6，验证：
停掉其中一台服务，需要手动切换~~
hdfs haadmin -transitionToActive --forcemanual --forceactive  nn2
原因配置文件配错了~~

```

```
kafka:
nohup sh /usr/kafka/kafka_2.11-2.3.0/bin/kafka-server-start.sh /usr/kafka/kafka_2.11-2.3.0/config/server.properties &

zookeeper:
sh /usr/zookeeper/apache-zookeeper-3.5.7-bin/bin/zkServer.sh start

hadoop:
/usr/hadoop/hadoop-3.1.3/sbin/hadoop-daemon.sh start journalnode
/usr/hadoop/hadoop-3.1.3/sbin/start-yarn.sh
/usr/hadoop/hadoop-3.1.3/sbin/start-dfs.sh

hbase:
/usr/hbase/hbase-2.1.9/bin/start-hbase.sh 

```

异常:

```
Cannot find any valid remote NN to service request


```

hbase:

```
1，修改hbase-env.sh
2，拷贝hadoop的hdfs-site.xml\core-site.xml到conf目录
3，拷贝lib/client-facing-thirdparty/htrace-core-3.1.0-incubating.jar lib/
4，配置hregions文件
5，启动hbase
6，获取数据
表名->rowkey->列族名->列->版本
7，创建表
create 't_e_user_info',{NAME => 'base_info',VERSIONS => 3},{NAME => 'extra_info'}
put 't_e_user_info','rk0001','base_info','name:lqd'
scan 't_e_user_info'
get 't_e_user_info','rk0001'
scan 't_e_user_info' ,{COLUMN=>'base_info:age',LIMIT=>1,STARTROW=>'rk0001'}
8，hbase按字典顺序排序
9，版本特性，不指定版本会返回最新的
get 't_e_user_info','rk0003',{COLUMN => 'base_info:id',VERSIONS =>5}
10，名称空间 == hdfs上（/hbase/data/名称空间） == 库（schema）
hbase(main):047:0> create_namespace 'adm'                       
hbase(main):048:0> create 'adm:t_e_order','o1','o2'
11，查看表结构：list

```

异常：

```
aused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at java.lang.reflect.Constructor.newInstance(Constructor.java:423)
	at org.apache.hadoop.hbase.util.ReflectionUtils.instantiate(ReflectionUtils.java:58)
	... 17 more
Caused by: org.apache.hbase.thirdparty.io.netty.channel.unix.Errors$NativeIoException: bind(..) failed: Cannot assign requested address
	at org.apache.hbase.thirdparty.io.netty.channel.unix.Errors.newIOException(Errors.java:117)
--------------------
检查下hostname对应主机名是否与conf/regionservers配置文件上的域名对应上。
```

hive:

![107.hive的设计思想和技术架构](D:\自我提升\视频\bigdata\大数据Hadoop第7章\截图\107.hive的设计思想和技术架构.png)

```
1,bin/hive --service metastore &
2,hive> create table t_order(
    > id int, product_id string, number int, amount double) 
    > row format delimited
    > fields terminated by ',';
3,编辑数据上传数据
/user/hive/warehouse/t_order (order.data.1)
3-1,hadoop fs -put order.data.1 /user/hive/warehouse/t_order
3-2,load data local inpath '/root/order.data.2' into table t_order;
4,统计
select * from t_order
5,外部表和内部表
即存储的路径是否是自定义的。

```

异常：

```
java.lang.NoSuchMethodError: com.google.common.base.Preconditions.checkArgument
--------------------
查看hadoop安装目录下share/hadoop/common/lib内guava.jar版本
查看hive安装目录下lib内guava.jar的版本 如果两者不一致，删除版本低的，并拷贝高版本的 问题解决！

Required table missing : "DBS" in Catalog "" Schema "". DataNucleus requires this table to perform its persistence operations. Either your MetaData is incorrect, or you need to enable "datanucleus.schema.autoCreateTables"
---------------------
将datanucleus.schema.autoCreateAll属性改为true。

MetaException(message:Version information not found in metastore. )
----------------------
conf/hive-site.xml 中的 “hive.metastore.schema.verification”  值为 false

IllegalArgumentException: java.net.URISyntaxException: Relative path in absolute URI: ${system:java.io.tmpdir%7D/$%7Bsystem:user.name%7D
----------------------
1.查看hive-site.xml配置，会看到配置值含有"system:java.io.tmpdir"的配置项
2.新建文件夹/home/grid/hive-0.14.0-bin/iotmp
3.将含有"system:java.io.tmpdir"的配置项的值修改为如上地址

FAILED: HiveException java.lang.RuntimeException: Unable to instantiate org.apache.hadoop.hive.ql.metadata.SessionHiveMetaStoreClient
-----------------------
bin/hive --service metastore &

ERROR XSDB6: Another instance of Derby may have already booted the database
-----------------------
切换数据库为mysql,参考文档:https://www.cnblogs.com/thisyan/p/9609497.html

impossible to write to binary log since BINLOG_FORMAT = STATEMENT and at least one table uses a storage engine limited to row-based logging. InnoDB is limited to row-logging when transaction isolation level is READ COMMITTED or READ UNCOMMITTED.
----------------------
set global binlog_format='MIXED'

YarnRuntimeException: java.lang.NullPointerException
----------------------
<property> 
<name>yarn.resourcemanager.webapp.address.rm1</name>  
<value>hadoop1:8088</value> 
</property>
<property> 
<name>yarn.resourcemanager.webapp.address.rm2</name>  
<value>hadoop2:8088</value> 
</property>


```

sqoop:

```
1，下载解压添加环境变量
2，使用工具即可：

***数据库中的数据导入到HDFS上
\#sqoop import --connect jdbc:mysql://192.168.254.137:3306/test --username "root" --password "123456" --table t_e_user_info
		
指定输出路径、指定数据分隔符
# sqoop import --connect jdbc:mysql://hdp-server-01:3306/baba --username root --password root --table bbs_detail --target-dir '/sqoop/td' --fields-terminated-by '\t'
		
指定MapTask数量 -m 
#sqoop import --connect jdbc:mysql://hdp-server-01:3306/baba --username root --password root  --table bbs_detail --target-dir '/sqoop/td1' --fields-terminated-by '\t' -m 1
		
增加where条件, 注意：条件必须用引号引起来
# sqoop import --connect jdbc:mysql://hdp-server-01:3306/baba --username root --password root  --table bbs_detail --where 'id>30' --target-dir '/sqoop/td2' --fields-terminated-by '\001' -m 1
		
增加query语句(使用 \ 将语句换行)
sqoop import --connect jdbc:mysql://hdp-server-01:3306/baba --username root --password root \
--query 'SELECT id,order_id,product_id FROM bbs_detail where id > 30 AND $CONDITIONS' --split-by bbs_detail.id --target-dir '/sqoop/td3'
		
注意：如果使用--query这个命令的时候，需要注意的是where后面的参数，AND $CONDITIONS这个参数必须加上
而且存在单引号与双引号的区别，如果--query后面使用的是双引号，那么需要在$CONDITIONS前加上\即\$CONDITIONS
如果设置map数量为1个时即-m 1，不用加上--split-by ${tablename.column}，否则需要加上
	
***从数据库中导入数据到hive
sqoop import --hive-import --connect jdbc:mysql://hdp-server-01:3306/baba --username root --password root --table bbs_detail
	
第二类：将HDFS上的数据导出到数据库中
sqoop export --connect jdbc:mysql://hdp-server-01:3306/test  --username root --password root --export-dir '/myorder/data' --table myorder --columns id,order_id --fields-terminated-by ','  -m 2

注意：以上测试要配置mysql远程连接
	GRANT ALL PRIVILEGES ON mytest.* TO 'root'@'192.168.0.104' IDENTIFIED BY 'itcast' WITH GRANT OPTION;
	FLUSH PRIVILEGES; 
	
	GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'itcast' WITH GRANT OPTION;
	FLUSH PRIVILEGES
```

异常：

```
缺少各种包
------------
添加到lib下

java.sql.SQLException: Access denied for user 'root'@'hadoop2' (using password: YES)
------------
grant all privileges on *.* to root@'hadoop2' identified by '123456';


```

storm 实时流式计算：

```
1，下载
2，配置然后分发到其他节点
storm.zookeeper.servers:
     - "hadoop1"
     - "hadoop2"
     - "hadoop3"
# 
nimbus.seeds: ["hadoop1"]
supervisor.slots.ports:
     - 6701 
     - 6702 
     - 6703 
     - 6704 
     - 6705 
     - 6706 
3，启动zk
4，
bin/storm nimbus &
bin/storm supervisor &
bin/storm ui &
5，
增加supervisor.slots.ports槽点
6，提交到storm执行
apache-storm-2.1.0/bin/storm jar microservice-storm-1.1.1-SNAPSHOT.jar com.adm.springcloud.ObjectTopologyApplication "storm"
```

异常：

```
java.lang.NoClassDefFoundError: com/codahale/metrics/JmxReporter
-------------------------------
<dependency>
<groupId>com.codahale.metrics</groupId>
<artifactId>metrics-core</artifactId>
<version>3.0.2</version>
</dependency>

java.lang.StackOverflowError
-------------------------------
前者将log4j桥接到slf4j，后者将slf4j桥接到log4j，循环桥接，当第一个通过slf4j或log4j获取的logger被调用时，就会出现StackOverflowError。
解决：明确到底使用哪个日志框架，如果使用slf4j做日志API和输出，则去掉slf4j-log4j12；如果使用log4j做日志记录和输出，则去掉log4j-over-slf4j。

Could not find leader nimbus from seed hosts [hadoop1]. Did you specify a valid list of nimbus hosts for config nimbus.seeds
-----------------------------
一般是zk出问题了

Exception in thread "main" java.lang.NoClassDefFoundError: org/apache/commons/pool2/impl/GenericObjectPoolConfig
	at com.adm.springcloud.ObjectTopologyApplication.main(ObjectTopologyApplication.java:105)
Caused by: java.lang.ClassNotFoundException: org.apache.commons.pool2.impl.GenericObjectPoolConfig
	at java.net.URLClassLoader.findClass(URLClassLoader.java:381)
-----------------------
直接运行jar，会少包，要将对应的包放到storm的lib下面
```

spark：

```
1，配置conf/spark-env.sh
export HADOOP_CONF_DIR=/usr/hadoop/hadoop-3.1.3/etc/hadoop/ (独立模式和YARN运行的区别)
export SPARK_DIST_CLASSPATH=$(/usr/hadoop/hadoop-3.1.3/bin/hadoop classpath)
export SPARK_MASTER_IP=192.168.254.138
export JAVA_HOME=/usr/jdk1.8.0_102/
##其他配置
SPARK_MASTER_HOST=localhost.localdomain
SPARK_MASTER_PORT=7077
SPARK_MASTER_WEBUI_PORT=8080
SPARK_WORKER_CORES=1
SPARK_WORKER_MEMORY=1024M
SPARK_WORKER_PORT=7078
SPARK_WORKER_WEBUI_PORT=8081

2，配置conf/slaves,并分发到其他服务器

3，在master服务器启动start-all.sh

4，动态添加,先分发后执行
/sbin/start-slave.sh spark://192.168.254.138:7077

5，spark-shell
scala> var textFile = spark.read.textFile("../README.md") # 创建RDD
scala> textFile.count()
scala> val subTextFile = textFile.filter(line=>line.contains("spark")) # 创建RDD 
scala> subTextFile.count()
scala> subTextFile.cache() #提高速度
scala> var data = Array(1,2,3,4,5)
scala> val distData = sc.parallelize(data) #创建RDD

6，闭包（Spark的难点之一是在跨集群执行代码时了解变量和方法的范围和生命周期）
scala> val data = Array(1, 2, 3, 4, 5)
scala> var rdd = sc.parallelize(data)
// Wrong: Don't do this!!
scala> rdd.foreach(x => counter += x)
scala> println("Counter value: " + counter)

7，键值对
scala> val lines = sc.textFile("data.txt")
scala> val pairs = lines.map(x => (x.split(" ")(0), x))
scala> pairs.foreach(println)
scala> val counts = pairs.reduceByKey((x,y) => x+y) # 计算相同key出现的次数
scala> counts.foreach(println)
scala> val lines = sc.textFile("data.txt")
scala> val pairs = lines.map(x => (x.split(" ")(0), x))
scala> pairs.foreach(println)
scala> val rdd = sc.parallelize(Seq((1, 2), (3, 4), (3, 6))) 
scala> val rdd1= rdd.reduceByKey((x, y) => x + y)
scala> rdd1.foreach(println)
scala> val rdd2 = rdd.groupByKey()
scala> rdd2.foreach(println)
scala> val rdd = sc.parallelize(Seq((1, 2), (3, 4), (3, 6)))
scala> val rdd1 = rdd.countByKey()
scala> rdd1.foreach(println)

8，累加变量（类似java中的原子变量）和广播变量
#广播变量  
scala> val factor = 3  
scala> val broadcast = sc.broadcast(factor)  
scala> val numbers = Array(1,2,3,4,5)  
scala> val numberRDD = sc.parallelize(numbers,1)  
scala> val nRDD = numberRDD.map(row => { row * broadcast.value})  
scala> nRDD.foreach(item => {println(item)})  
scala> val broadcastVar = sc.broadcast(3)
scala> val data = Array(1, 2, 3, 4, 5)
scala> val RDD = sc.parallelize(data ,1) 
scala> val nRDD = RDD .map(line => { line * broadcastVar.value}) 
scala> nRDD.foreach(item => {println(item)}) 
#累加变量 
scala> val sum = sc.longAccumulator("My Accumulator")  
scala> val numberRDD = sc.parallelize(Array(1,2,3,4,5),1)  
scala> numberRDD.foreach(item => {sum.add(item)})  
scala> numberRDD.foreach(item => {println(sum)}) 
#保存文件
scala> val input = sc.textFile("/user/README.md")
scala> val result = input.map(s => s.length)
scala> result.saveAsTextFile("data")

9，提交应用
cd /usr/spark/spark-3.0.0/examples
#9-1
spark-submit   --class org.apache.spark.examples.SparkPi  --master spark://192.168.254.138:7077   --executor-memory 1G   --total-executor-cores 100   jars/spark-examples*.jar 1
#非集群的模式，结果可以在http://192.168.254.138:8080/的spark上查看到应用.

#9-2
spark-submit --class org.apache.spark.examples.SparkPi  --master yarn     --deploy-mode cluster     --driver-memory 2g     --executor-memory 1g     --executor-cores 1     --queue default     ../examples/jars/spark-examples*.jar     3
#集群模式下，结果可以在http://hadoop2:8088/cluster上查看到.
可以用--jars指定jar路径

#9-3
bin/spark-shell --master yarn --deploy-mode client 除了提交外的另外一种交互模式spark
#集群模式下，结果可以在http://hadoop2:8088/cluster上查看到.

10，spark sql
#10-1 dataframe
spark-shell --master yarn --deploy-mode client
scala> import org.apache.spark.sql.SparkSession
scala> val spark = SparkSession.builder().appName("Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()
scala> import spark.implicits._
scala> val df = spark.read.json("/user/root/data.json")
scala> df.show()

#10-2 dataframe的操作。 有连表嘛？
scala> df.groupBy("sex").count().show() #分组
scala> df.filter($"sex" > "0").show() #过滤
scala> df.select($"name", $"sex"+"123").show() #修改列名
scala> df.select("name").show() #选择列名
scala> df.printSchema() #对应数据结构

#10-3 视图
scala> df.createOrReplaceTempView("people")
scala> val sqlDF = spark.sql("SELECT * FROM people")
scala> sqlDF.show()

#10-4 dataset
scala> case class Person(name: String, age: Long)
scala> val caseClassDS = Seq(Person("Andy", 32)).toDS()
scala> caseClassDS.show()

scala> case class Peson(name: String, sex: String)
scala> val p = spark.read.json("/user/root/data.json").as[Peson]
scala> p.show()

#10-5 RDD与dataset的转换
Spark SQL支持两种将现有RDD转换为Dataset的方法。第一种方法使用反射来推断包含特定对象类型的RDD的Schema。这种基于反射的方法可以使代码更简洁，并且当您在编写Spark应用程序时已经了解Schema时，可以很好地工作。创建Dataset的第二种方法是通过编程界面，该界面允许您构造模式，然后将其应用于现有的RDD。尽管此方法较为冗长，但可以让您在运行时才知道列及其类型的情况下构造Dataset。
#10-5-1  第一种
scala> import spark.implicits._
scala> val peopleDF = spark.sparkContext.textFile("/user/root/human.data").map(_.split(",")).map(attributes => Peson(attributes(0), attributes(1))).toDF()
scala> peopleDF.createOrReplaceTempView("people")
scala> val teenagersDF = spark.sql("SELECT name, sex FROM people WHERE sex=90")
scala> teenagersDF.show()
#10-5-2 第二种
1.从原始RDD创建Rows RDD；
2.创建由与步骤1中创建的RDD中的行结构匹配的结构类型表示的Schema。
3.通过SparkSession提供的createDataFrame方法将Schema应用于Rows RDD。
scala> import org.apache.spark.sql.types._
scala> import org.apache.spark.sql.Row
scala> val peopleRDD = spark.sparkContext.textFile("/user/root/human.data")
scala> val schemaString = "name age"
scala> val fields = schemaString.split(" ").map(fieldName => StructField(fieldName, StringType, nullable = true))
scala> val schema = StructType(fields)
scala> val rowRDD = peopleRDD.map(_.split(",")).map(attributes => Row(attributes(0), attributes(1).trim))
scala> val peopleDF = spark.createDataFrame(rowRDD, schema)
scala> peopleDF.createOrReplaceTempView("people")
scala> val results = spark.sql("SELECT name FROM people")
scala> results.map(attributes => "Name: " + attributes(0)).show()

#10-6 跳过
内置的DataFrames函数提供了常见的聚合，例如count()，countDistinct()，avg()，max()，min()等。虽然这些函数是专为DataFrames设计的，但是Spark SQL在Scala和Java中也有一些类型安全的版本，用于处理强类型。此外，用户不仅限于预定义的聚合函数，还可以创建自己的聚合函数

#11
#11-1 数据源加载保存功能
scala> val pDF = spark.read.format("json").load("/user/root/data.json")
scala> pDF.select("name").write.format("parquet").save("data.parquet.1")
scala> pDF.select("name","sex").write.format("csv").save("data.csv.3")
scala> val peopleDFCsv = spark.read.format("csv").option("sep", ";").option("inferSchema", "true").option("header", "true").load("/user/root/data.csv.3")
scala> peopleDFCsv.write.format("orc").option("orc.bloom.filter.columns", "favorite_color").option("orc.dictionary.key.threshold", "1.0").save("users_with_options.orc")

#12 直接在文件上运行SQL
scala> spark.sql("SELECT * FROM parquet.`/user/root/data.parquet`").show()

#13 保存到表，分组，排序和分区. 对于基于文件的数据源，也可以对输出进行存储和分类或分区。存储桶和排序仅适用于持久表
scala> pDF.write.partitionBy("favorite_color").bucketBy(32, "name").saveAsTable("users_partitioned_bucketed")
scala> pDF.write.bucketBy(32,"name").sortBy("sex").saveAsTable("sql_bucket")

#14 Parquet


```

操作的数据

```
human.data：
lqd,32
cjj,29
lcf,63
lxl,59
llk,39
谢谢,90



```

异常：

```
Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources
---------------------
资源不够

WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
---------------------
https://blog.csdn.net/u013310025/article/details/52853941

Call From hadoop1/192.168.254.138 to hadoop1:8032 failed on connection exception\
---------------------
检查 yarn-resourcemanager是否启动，查看yarn-site.xml的配置是否正确：
<property>
<name>yarn.resourcemanager.address</name>
<value>master:8032</value>
</property>


```

调整虚拟机的内存大小

1，kafka

```
bin/kafka-server-start.sh
export KAFKA_HEAP_OPTS="-Xmx512m -Xms512m -XX:+UseG1GC -XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35 -XX:G1HeapRegionSize=16M -XX:MinMetaspaceFreeRatio=50 -XX:MaxMetaspaceFreeRatio=80"

```

2，hadoop

```
HDFS的JVM参数配置文件： /etc/hadoop/hadoop-env.sh 
Namenode进程的JVM配置: HADOOP_NAMENODE_OPTS 
Datanode进程的JVM配置: HADOOP_DATANODE_OPTS 
client命令行的JVM配置: HADOOP_CLIENT_OPTS

YARN的JVM参数配置文件：/etc/hadoop/yarn-env.sh
```

3，storm

```
在配置文件storm.yaml中，有：
# to nimbus 
nimbus.childopts: "-Xmx1024m" 
# to supervisor 
supervisor.childopts: "-Xmx1024m" 
# to worker 
worker.childopts: "-Xmx768m" 
```

