# 1.引言

## 1.1 设计背景

- 由于目前采用了微服务架构，很多业务的数据是通过远程服务获取。远程服务调用比较耗时，特别是一个业务接口需要多个远程服务支持的情况下，会影响整个系统的性能。同时远程服务由于网络延迟，网络波动会导致系统不可用，不稳定。

- 现在的业务架构是拆分颗粒很细，导致之前的简单的表关联查询都是调用远程服务。虽然可以添加冗余字段去处理相关业务，但过多的字段会影响关系型数据库的查询、存储。

- 作业中心有搜索业务、和大量的统计业务，以往我们通过数据库去实时统计，搜索，性能不太理想。上1000w的作答数据，跨多个表，在已有的架构上要做实时统计分析基本不太可能。

- 作业中心的数据的特点：查询多、更新少，统计多。

  基于以上的原因，我们引入了Elasticsearch来做实时查询、聚合分析。

  至于elastic的查询和聚合分析的性能指标可以参考官网的例子 ，地址如下：<https://benchmarks.elastic.co/index.html>

# 2.软件支持

| 软件                | 版本                       | 配置                                                         |
| ------------------- | -------------------------- | ------------------------------------------------------------ |
| Centos              | 7.0以上                    | 32G内存，500G SSD, Intel(R) Xeon(R) CPU E5-2407 v2 @ 2.40GHz |
| Elasticsearch Xpack | 7.1.0                      | 安装ik分词、repository-hdfs插件、xpack插件                   |
| Kibana              | 7.1.0                      | 安装xpack，联通elastic                                       |
| Logstash            | 7.1.0                      | 安装xpack，联通elastic                                       |
| Cerebro             | 0.8.3                      | 安装xpack，联通elastic                                       |
| HDFS                | 2.8.1（使用eco的HDFS服务） |                                                              |
| Docker              | 18.09.7                    |                                                              |
| Docker-Compose      | 1.24.0                     |                                                              |

# 3.总体功能概述

## 3.1 功能总体需求

- 满足作业中心的快速搜索、快速统计
- 满足作业中心的业务数据快速DSL
- Elastic服务高可用、高性能、快速水平扩展、索引无缝切换零宕机
- Elastic技术服务快速搭建，快速安装。
- 保证Elatic数据安全。
- Elastic数据灾备。
- 历史数据快速导入。
- 保证业务数据索引不丢失。

## 3.2 整体框架视图

![](E:\workspace_ai\test\server-install\registry\proxy\profiles\elasticsearch\ELK架构图(1).png)

## 3.3 实现

### 3.3.1 Elastic+Xpack+Kibana+Cerebro服务搭建

为了能实现快速搭建稳定的EKC服务，我们通过docker的服务构建整个服务。

1. 构建elastic单个服务，安装ik、repository-hdfs，打成镜像上传到镜像仓库。镜像地址参考6.附录

   ```shell
   [root@aiclassplus elasticsearch]# docker exec -it es01 bash
   [root@3a97be9f3a51 elasticsearch]# bin/elasticsearch-plugin list
   ik
   repository-hdfs
   [root@3a97be9f3a51 elasticsearch]#
   ```

2. 构建kibana单个服务，打成镜像上传到镜像仓库。镜像地址参考6.附录

3. 构建Cerebro单个服务，打成镜像上传到镜像仓库。镜像地址参考6.附录

   ```shell
   [root@aiclassplus elasticsearch]# docker images
   REPOSITORY                                           TAG                 IMAGE ID            CREATED             SIZE
   192.168.133.31:8089/elasticsearch/elasticsearch      7.1.0               00dc9a9f409b        19 minutes ago      933MB
   192.168.133.31:8089/elasticsearch/kibana             7.1.0               714b175e84e8        5 months ago        745MB
   192.168.133.31:8089/elasticsearch/lmenezes/cerebro   0.8.3               3a2daf87f0c7        6 months ago        333MB
   [root@aiclassplus elasticsearch]# 
   
   ```

4. 编写docker-compose容器编排文件。

   1. 配置多个elastic节点，搭建hot-warm的elastic集群框架，其中2个master节点兼数据节点用于处理hot数据。1个node节点用于处理warm数据。
   2. 配置EKC之间的Xpack ，配置服务之间的证书等，以保证elastic服务的数据安全。这里使用的是basic license。

   docker-compose文件如下：

   ```properties
   version: '2.2'
   services:
     cerebro:
       image: 192.168.133.31:8089/elasticsearch/lmenezes/cerebro:0.8.3
       container_name: cerebro
       restart: always
       ports:
         - "9990:9000"
       command:
         - -Dhosts.0.host=http://elasticsearch:9200
       networks:
         - elasticsearch_network
     kibana:
       image: 192.168.133.31:8089/elasticsearch/kibana:7.1.0
       container_name: kibana7
       restart: always
       environment:
         - I18N_LOCALE=zh-CN
         - XPACK_GRAPH_ENABLED=true
         - TIMELION_ENABLED=true
         - XPACK_MONITORING_COLLECTION_ENABLED="true"
       volumes:
         - /etc/localtime:/etc/localtime
         - /usr/twsm/elasticsearch/kibana/kibana.yml:/usr/share/kibana/config/kibana.yml
       ports:
         - "5601:5601"
       networks:
         - elasticsearch_network
     elasticsearch:
       image: 192.168.133.31:8089/elasticsearch/elasticsearch:7.1.0
       container_name: es01
       restart: always
       environment:
         - cluster.name=aieval
         - node.name=es01
         - bootstrap.memory_lock=true
         - "ES_JAVA_OPTS=-Xms6g -Xmx6g"
         - discovery.seed_hosts=es01,es02,es03
         - cluster.initial_master_nodes=es01,es02
         - ELASTIC_PASSWORD=xiao99@Twsm2019
       ulimits:
         memlock:
           soft: -1
           hard: -1
       volumes:
         - /etc/localtime:/etc/localtime
         - /data/es01:/usr/share/elasticsearch/data
         - /usr/twsm/elasticsearch/es01/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml
         - /usr/twsm/elasticsearch/certs/elastic-certificates.p12:/usr/share/elasticsearch/config/elastic-certificates.p12
       ports:
         - 9200:9200
       networks:
         - elasticsearch_network
     elasticsearch2:
       image: 192.168.133.31:8089/elasticsearch/elasticsearch:7.1.0
       container_name: es02
       restart: always
       environment:
         - cluster.name=aieval
         - node.name=es02
         - bootstrap.memory_lock=true
         - "ES_JAVA_OPTS=-Xms6g -Xmx6g"
         - discovery.seed_hosts=es01,es02,es03
         - cluster.initial_master_nodes=es01,es02
         - ELASTIC_PASSWORD=xiao99@Twsm2019
       ulimits:
         memlock:
           soft: -1
           hard: -1
       volumes:
         - /etc/localtime:/etc/localtime
         - /data/es02:/usr/share/elasticsearch/data
         - /usr/twsm/elasticsearch/es02/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml
         - /usr/twsm/elasticsearch/certs/elastic-certificates.p12:/usr/share/elasticsearch/config/elastic-certificates.p12
       networks:
         - elasticsearch_network
     elasticsearch3:
       image: 192.168.133.31:8089/elasticsearch/elasticsearch:7.1.0
       container_name: es03
       restart: always
       environment:
         - cluster.name=aieval
         - node.name=es03
         - bootstrap.memory_lock=true
         - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
         - discovery.seed_hosts=es01,es02,es03
         - cluster.initial_master_nodes=es01,es02
         - ELASTIC_PASSWORD=xiao99@Twsm2019
       ulimits:
         memlock:
           soft: -1
           hard: -1
       volumes:
         - /etc/localtime:/etc/localtime
         - /data/es03:/usr/share/elasticsearch/data
         - /usr/twsm/elasticsearch/es03/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml
         - /usr/twsm/elasticsearch/certs/elastic-certificates.p12:/usr/share/elasticsearch/config/elastic-certificates.p12
       networks:
         - elasticsearch_network
   networks:
     elasticsearch_network:
       external: true
   ```

通过以上步骤，基本完成了整个EKC的服务搭建，完成了hot-warm集群的elastic架构搭建，完成了基于Xpack的EKC安全架构搭建。如下，

```shell
[root@aiclassplus elasticsearch]# docker ps
CONTAINER ID        IMAGE                                                      COMMAND                  CREATED             STATUS              PORTS                              NAMES
15334edc05fe        192.168.133.31:8089/elasticsearch/elasticsearch:7.1.0      "/usr/local/bin/dock…"   15 minutes ago      Up 15 minutes       9200/tcp, 9300/tcp                 es02
4027999be0f8        192.168.133.31:8089/elasticsearch/kibana:7.1.0             "/usr/local/bin/kiba…"   15 minutes ago      Up 15 minutes       0.0.0.0:5601->5601/tcp             kibana7
0ba8b2314e2d        192.168.133.31:8089/elasticsearch/lmenezes/cerebro:0.8.3   "/opt/cerebro/bin/ce…"   15 minutes ago      Up 15 minutes       0.0.0.0:9990->9000/tcp             cerebro
3a97be9f3a51        192.168.133.31:8089/elasticsearch/elasticsearch:7.1.0      "/usr/local/bin/dock…"   15 minutes ago      Up 15 minutes       0.0.0.0:9200->9200/tcp, 9300/tcp   es01
a182261ded3b        192.168.133.31:8089/elasticsearch/elasticsearch:7.1.0      "/usr/local/bin/dock…"   15 minutes ago      Up 15 minutes       9200/tcp, 9300/tcp                 es03
```

以后可以通过只需输入如下命令，就可以快速安装单机环境的3个节点的Elastic+xpack+kibana+cerebro的服务架构。

以后可以通过只需输入如下命令，就可以快速安装单机环境的3个节点、水平扩展N个节点（每个节点可以部署多个实例）的Elastic+xpack+kibana+cerebro的服务架构。

1，安装主节点 ，依次执行以下命令：
curl -sSL <http://192.168.133.31:8666/install/app-install.sh> |sh -xs network -confignetwork
curl -sSL <http://192.168.133.31:8666/install/app-install.sh> |sh -xs elasticsearch -installelastic

2，水平扩展N个节点，依次执行以下命令：
curl -sSL <http://192.168.133.31:8666/install/app-install.sh> |sh -xs network -confignetworknode
获取主节点的es01、es02的容器IP地址，修改/etc/hosts中的映射关系。
curl -sSL <http://192.168.133.31:8666/install/app-install.sh> |sh -xs elasticsearch -installelasticnode

![](C:\Users\lqd\Desktop\lsb.bmp)

### 3.3.2 Logstash服务搭建及运维

为了保证数据的不丢失、保证历史数据的快速导入，我们通过logstash来采集数据库中的业务数据（例如老师的发布记录、学生作答记录以及作答详情信息）。

1. 构建logstash单个服务，配置xpack，打成镜像上传到镜像仓库。镜像地址参考6.附录。

2. 配置logstash的各个租户的pipeline，编写不同业务的采集SQL。如下：

   ```properties
   input {
       jdbc {
         jdbc_driver_class => "org.postgresql.Driver"
         jdbc_connection_string => "jdbc:postgresql://192.168.210.54:8832/e000003"
         jdbc_user => "e000003"
         jdbc_password => "123qwe"
         jdbc_driver_library => "/usr/share/logstash/database/postgresql-42.2.5.jar"
         jdbc_paging_enabled => "true"
         jdbc_page_size => "50000"
         clean_run => false
         use_column_value => "true"
         tracking_column => "publishtime"
         tracking_column_type => "timestamp"
         record_last_run => true
         last_run_metadata_path => "/usr/share/logstash/pipeline/e000003/position/es_work_publish.txt"
         statement_filepath => "/usr/share/logstash/database/aievaluation/es_work_publish.sql"
         schedule => "00 00 * * *"
         type => "es_work_publish"
         jdbc_default_timezone =>"Asia/Shanghai"
       }
       jdbc {
         jdbc_driver_class => "org.postgresql.Driver"
         jdbc_connection_string => "jdbc:postgresql://192.168.210.54:8832/e000003"
         jdbc_user => "e000003"
         jdbc_password => "123qwe"
         jdbc_driver_library => "/usr/share/logstash/database/postgresql-42.2.5.jar"
         jdbc_paging_enabled => "true"
         jdbc_page_size => "50000"
         clean_run => false
         use_column_value => "true"
         tracking_column => "starttime"
         tracking_column_type => "timestamp"
         record_last_run => true
         last_run_metadata_path => "/usr/share/logstash/pipeline/e000003/position/es_work_answer.txt"
         statement_filepath => "/usr/share/logstash/database/aievaluation/es_work_answer.sql"
         schedule => "00 00 * * *"
         type => "es_work_answer"
         jdbc_default_timezone =>"Asia/Shanghai"
       }
       jdbc {
         jdbc_driver_class => "org.postgresql.Driver"
         jdbc_connection_string => "jdbc:postgresql://192.168.210.54:8832/e000003"
         jdbc_user => "e000003"
         jdbc_password => "123qwe"
         jdbc_driver_library => "/usr/share/logstash/database/postgresql-42.2.5.jar"
         jdbc_paging_enabled => "true"
         jdbc_page_size => "50000"
         clean_run => false
         use_column_value => "true"
         tracking_column => "lastmodifytime"
         tracking_column_type => "timestamp"
         record_last_run => true
         last_run_metadata_path => "/usr/share/logstash/pipeline/e000003/position/es_work_answer_result.txt"
         statement_filepath => "/usr/share/logstash/database/aievaluation/es_work_answer_result.sql"
         schedule => "00 00 * * *"
         type => "es_work_answer_result"
         jdbc_default_timezone =>"Asia/Shanghai"
       }
   }
   
   filter {
       fingerprint {
           method => "MD5"
           source => "primaryid"
           target => "indexid"
           concatenate_sources => true
       }
       if [type] == "es_work_publish" {
   	    mutate {
   		remove_field =>["@version"]
   		remove_field =>["primaryid"]
   		remove_field =>["@timestamp"]
   	    }
       }	    
       if [type] == "es_work_answer" {
   	    mutate {
   		remove_field =>["@version"]
   		remove_field =>["primaryid"]
   		remove_field =>["@timestamp"]
   	    }
       }
       if [type] == "es_work_answer_result" {   
   	    mutate {
   		remove_field =>["@version"] 
   		remove_field =>["@timestamp"]
   		remove_field =>["primaryid"]
   		remove_field =>["lastmodifytime"]
   	    }	
       }
   }
   
   output {
       if [type] == "es_work_publish" {
   	    elasticsearch {
   		hosts => ["http://192.168.130.27:9200"]
   		user => "elastic"
   		password => "xiao99@Twsm2019"
   		index => "es_work_publish-e000003"
   		document_id => "%{indexid}"
   	    }
       }
       if [type] == "es_work_answer" {
   	    elasticsearch {
   		hosts => ["http://192.168.130.27:9200"]
   		user => "elastic"
   		password => "xiao99@Twsm2019"
   		index => "es_work_answer-e000003"
   		document_id => "%{indexid}"
   	    }
       }
       if [type] == "es_work_answer_result" {
   	    elasticsearch {
   		hosts => ["http://192.168.130.27:9200"]
   		user => "elastic"
   		password => "xiao99@Twsm2019"
   		index => "es_work_answer_result-e000003"
   		document_id => "%{indexid}"
   	    } 
       }
       stdout {
           codec => json_lines
       }
   }
   ```

3. 配置docker-compose.yml容器编排文件。

   1. 要求网络桥接到elasticsearch的网桥上。
   2. 启动容器即可实现数据从Pgsql导入Elastic。

   docker-compse.yml如下：

   ```xml
   version: '2.2'
   services:
     logstash:
       image: 192.168.133.31:8089/elasticsearch/logstash:7.1.0
       container_name: logstash
       ports:
       - 5602:4560
       volumes:
       - /etc/localtime:/etc/localtime
       - ./pipeline/:/usr/share/logstash/pipeline/
       - ./config/:/usr/share/logstash/config/
       - ./database/:/usr/share/logstash/database/
       networks:
       - elasticsearch_network
   networks:
     elasticsearch_network:
       external: true
   
   ```

### 3.3.3 Elastic业务索引创建及运维

```
1，索引策略   基于不同功能
2，索引模板   基于不同租户、不同产品 , 指定到同个产品
3，索引租户模板   基于不同租户、不同产品 , 同一个租户多个日期索引

1，创建索引的脚本 ，
	a，
	b，定义一级索引模板，满足业务的表结构来定义。这步需要对应的产品
	c，定义租户的二级索引模板，满足每个租户的索引以及使用索引策略。这步需要对应的租户以及对应的产品
	d，生成租户索引（以-000001结尾）。这步需要对应的租户
2，创建角色以及用户的脚本
	a，创建租户、产品的角色以及账号
3，初始化数据脚本

```

搭建服务后，登录Kibana服务，地址参考6.附录。对创建业务索引。

1. 创建索引生命周期策略。这里我们设计的策略是：当索引的文件数大于1000W或者索引存储大小大于15G的时候会进行rollover。rollover后的数据进去warm节点，会对这些数据设置为只读，合并segment，优化shard。同时降低这部分数据的索引优先级为50.

   ```json
   #---------------------------------------------------
   #@program: 测评产品
   #@author: Mr.LQDing
   #@create: 2019-10-08 16:02
   #@description: 索引生命周期管理策略twsm_index_policy
   #@policyName: twsm_index_policy
   
   PUT _ilm/policy/twsm_index_policy
   {
       "policy" : {
         "phases" : {
           "hot" : {
             "min_age" : "0ms",
             "actions" : {
               "rollover" : {
                 "max_size" : "15gb",
                 "max_docs" : 10000000
               },
               "set_priority" : {
                 "priority" : 100
               }
             }
           },
           "warm" : {
             "min_age" : "0ms",
             "actions" : {
               "allocate" : {
                 "number_of_replicas" : 1,
                 "include" : { },
                 "exclude" : { },
                 "require" : {
                   "box_type" : "warm"
                 }
               },
               "forcemerge" : {
                 "max_num_segments" : 2
               },
               "set_priority" : {
                 "priority" : 50
               },
               "shrink" : {
                 "number_of_shards" : 1
               }
             }
           }
         }
       }
   }
   
   ```

2. 创建发布、作答、作答结果索引模板。

   构建业务的一级索引模板，具体的字段设计不再详细列举，模板参考如下：

   ```json
   #---------------------------------------------------
   #@program: 测评产品
   #@author: Mr.LQDing
   #@create: 2019-10-08 16:02
   #@description: 作业发布mapping 索引模板设计 （对应t_e_publish表的内容，以及扩展）
   #@content: 作业发布id:publishid,作业发布班级id:classid,作业发布的班级名称:classname,批改状态。0: 未批改 1：已批改:markstatus,提交状态。0:未提交 1 已提交:submitstatus,作业标题:worktitle,作业类型。类型：1-线上作业；2-线下作业；3-扫描作业；4-提升练习。:worktype,作业科目:subjectid,发布者id:creatorid,发布人姓名:creatorname,状态：0-删除；1-正常；4-禁用。:status,发布时间:publishtime,作业生效时间:startime,作业结束时间:endtime,作业最后修改时间:lastmodifytime,学生id:studentid,学生姓名:studentname,是否发回。发回状态: 0-未发回；1-已发回。:issendback,提交时间:submittime"
   #@indexName: es_template_work_publish为索引名称
   
   DELETE _template/es_template_work_publish
   PUT _template/es_template_work_publish
   {
       "index_patterns" : "es_work_publish-*",
       "order":0,
       "settings": {
         "index.number_of_shards": "2",
         "number_of_replicas" : "1"
       },
       "mappings": {
               "_meta": {
                   "version": {
                     "min": "1.1.1",
                     "max": "1.1.1"
                   }
               },
               "_source": {
         		    "enabled": false
         	     },
               "dynamic" : "false",
               "properties": {
                 
             		"publishid":{
             			"type":"keyword",
           				"eager_global_ordinals": "true",
           				"store":"true"
             		},
             	
             		"classid":{
             			"type":"keyword",
           				"eager_global_ordinals": "true",
           				"store":"true"
             		},
   
             		"papertitle":{
             			"type":"text",
           				"store":"true",
           				"analyzer":"ik_max_word",
           				"doc_values":"false"
             		},
             	
             		"publishtype":{
             			"type":"byte",
           				"store":"true"
             		},
   			
   			"tasktype":{
             			"type":"byte",
           				"store":"true",
           				"null_value":-1
             		},
             
             		"subjectid":{
             			"type":"keyword",
           				"store":"true",
           				"null_value":"NULL"
             		},
   		
             		"creatorid":{
             			"type":"keyword",
           				"store":"true"
             		},
          
             		"publishtime":{
             			"type":"date",
             			"format": "yyyy-MM-dd HH:mm:ss",
           				"store":"true",
           				"null_value":"today"
             		},
   			
             		"endtime":{
             			"type":"date",
             			"format": "yyyy-MM-dd HH:mm:ss",
           				"store":"true",
           				"null_value":"today"
             		}
   		}
   	}
   }
   
   ```

   基于一级索引模板，构建二级模板如下：

   ```json
   # 租户cjtwbs1的发布索引模板
   DELETE _template/es_work_publish-cjtwbs1
   PUT _template/es_work_publish-cjtwbs1
   {
       "index_patterns" : "es_work_publish-cjtwbs1-*",
       "order":1,
       "settings": {
         "index" : {
           "lifecycle" : {
             "name" : "twsm_index_policy",
             "rollover_alias" : "es_work_publish-cjtwbs1"
           },
           "routing" : {
             "allocation" : {
               "include" : {
                 "box_type" : "hot"
               }
             }
           }
   	}
       }
   }   
   ```

3. 创建租户的索引，后续的查询基于index alias进行查询，方便以后索引切换能够做到无缝切换、零宕机。

   ```json
   #创建索引
   DELETE es_work_publish-cjtwbs1-*
   PUT es_work_publish-cjtwbs1-000001
   {
     "aliases": {
   	  "es_work_publish-cjtwbs1": {
   	      "is_write_index": true
   	  }
     }	
   }
   ```

### 3.3.4 Elastic服务代码框架

搭建代码框架，在microservice-framework框架上，我们构建了microservice-elasticsearch新的module工程，用于提供elastic的Dsl操作以及聚合分析。

1. 不建议用spring-data相关的elasticsearch的包，因为对spring boot相关依赖太多，需要同步升级相应的版本。我们这里采用resthighclient的操作api，于是需要引用以下jar版本：

2. 构建config\factory\model等目录。编写对应服务配置、服务操作等api。

   ```java
   /**
    * @program: aihomework
    * @description: elasticsearch high rest
    * @author: Mr.LQDing
    * @create: 2019-10-08 16:02
    **/
   
   @Slf4j
   @Repository
   public class ElasticsearchHighRestFactory extends AbstractElasticsearchFactory {
   
       protected final RestHighLevelClient xclient;
       
       private final String OPERATOR = "-";
   
       public ElasticsearchHighRestFactory(RestHighLevelClient xclient) {
           this.xclient = xclient;
       }
   
       @Override
       public <T extends IElasticSearchModel> String insert(String index , T bean) throws Exception {
   
           index = getIndexName(index);
           if (index == null) {
               return null;
           }
           IndexRequest request = new IndexRequest(index).id(bean.getIndexId());
           Map<String,T> beanMap = objectToMap(bean);
           request.source(beanMap, XContentType.JSON);
           IndexResponse response = xclient.index(request, RequestOptions.DEFAULT);
           return response.toString();
       }
   
       private String getIndexName(String index) {
           String tenantId = getTenantIdByContext();
           if (StringUtils.isBlank(tenantId) || StringUtils.isBlank(index))
           {
               return null;
           }
           index = index.concat(OPERATOR).concat(tenantId.toLowerCase());
           return index;
       }
       ............
   ```

   具体的代码就不再列举了。详细参考：6.附录.elastic的api框架svn地址

# 4.安全设计

搭建基于Xpack的ELKC服务架构。访问Elastic服务的数据包都进行了加密，同时对数据访问需要用户鉴权。

# 5.性能测试

对集群的压测，采用Elastic官方给出的工具ElaticRally。

简单

# 6.附录

镜像仓库地址：<http://192.168.133.31:8089/harbor/projects> 

ELKC服务的运维地址：（Kibana）http://192.168.130.27:5601/  和（Cerebro） http://192.168.130.27:9990/ 

Logstash的数据导入配置：192.168.102.241（/usr/twsm/logstash）

elastic的api框架svn地址：http://192.168.111.244/svn/aischool/code/AIEvaluation/trunk/common/microservice-framework/microservice-elasticsearch

破解：<https://www.ipyker.com/2019/03/13/elastic-x-pack>





