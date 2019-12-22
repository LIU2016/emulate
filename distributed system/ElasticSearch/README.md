### 参考文档

<https://zq99299.github.io/note-book/elasticsearch-core/>

### ElasticSearch与solr比较

```
1，当单纯的对已有数据进行搜索的时候，Solr更快
2，当实时建索引，Solr会产生io阻塞，查询性能较差，ElasticSearch具有明显优势
3，随着数据量的增加，Solr的搜索效率变得更低，而ElasticSearch却没有明显的变化
4，solr使用zookeeper进行分布式管理，而elasticSearch自身带有分布式协调管理功能
5，solr支持多种格式数据，ElasticSearch仅支持json格式

总之，solr不适合做实时搜索的应用。elasticSearch的效率是solr的50倍
```

### Elasticsearch工作原理

```
1，基于lucene
2，支持geo地图算法
3，api语法查询像数据库的语法一样，有where 有 and 有order 有过滤
```

| 关系型数据库  | ES                |
| ------------- | ----------------- |
| 建库（DB）    | 建库（Index）     |
| 建表（Table） | 建表（IndexType） |
| 建约束        | 主键（ID）        |

#### lucene

```
1，Document 行文本
2，Index 索引 （数据关键值） -->提高查询效率
3，Analyzer 分词器 （打标签） -->提高精准度
```

### Elasticsearch的注意地方

```
1，lucene版本差异决定了es的版本
5.5.0 - 2.3.4 （es）

2，ElasticSearch各版本差异


```

### Elasticsearch基于docker的安装

docker-compose.yml

```xml
version: '2.2'
services:
  cerebro:
    image: lmenezes/cerebro:0.8.3
    container_name: cerebro
    ports:
      - "9000:9000"
    command:
      - -Dhosts.0.host=http://elasticsearch:9200
  kibana:
    image: kibana:7.1.0
    container_name: kibana7
    environment:
      - I18N_LOCALE=zh-CN
      - XPACK_GRAPH_ENABLED=true
      - TIMELION_ENABLED=true
      - XPACK_MONITORING_COLLECTION_ENABLED="true"
    ports:
      - "5601:5601"
  elasticsearch:
    image: elasticsearch:7.1.0
    container_name: es7_01
    environment:
      - cluster.name=xttblog
      - node.name=es7_01
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - discovery.seed_hosts=es7_01
      - cluster.initial_master_nodes=es7_01,es7_02
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - es7data1:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
  elasticsearch2:
    image: elasticsearch:7.1.0
    container_name: es7_02
    environment:
      - cluster.name=xttblog
      - node.name=es7_02
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - discovery.seed_hosts=es7_01
      - cluster.initial_master_nodes=es7_01,es7_02
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - es7data2:/usr/share/elasticsearch/data
volumes:
  es7data1:
    driver: local
  es7data2:
    driver: local
```

#### 异常

```
Unexpected exception[UnknownHostException: elasticsearch: Name or service not known]
---------------
修改/etc/hosts，让elasticsearch的名称和127.0.0.1映射
```

#### 安装插件

```
#启动单节点
bin/elasticsearch -E node.name=node0 -E cluster.name=geektime -E path.data=node0_data

#安装插件
bin/elasticsearch-plugin install analysis-icu

#查看插件
bin/elasticsearch-plugin list
#查看安装的插件
GET http://localhost:9200/_cat/plugins?v

#start multi-nodes Cluster
bin/elasticsearch -E node.name=node0 -E cluster.name=geektime -E path.data=node0_data
bin/elasticsearch -E node.name=node1 -E cluster.name=geektime -E path.data=node1_data
bin/elasticsearch -E node.name=node2 -E cluster.name=geektime -E path.data=node2_data
bin/elasticsearch -E node.name=node3 -E cluster.name=geektime -E path.data=node3_data

#查看集群
GET http://localhost:9200
#查看nodes
GET _cat/nodes
GET _cluster/health
```

### logstash导入数据

```shell
1,下载（百度网盘:链接: https://pan.baidu.com/s/1_QFo3SP-2M0TJt-tq93w2A 提取码: q2iu）
logstash-7.3.1.tar.gz
ml-latest-small.zip
jdk-8u102-linux-x64.tar.gz

2，导入
cd /usr/work/
tar -xzvf logstash-7.3.1.tar.gz 
unzip ml-latest-small.zip 
cd logstash-7.3.1
vi ml-latest-small/logstash.conf 
./logstash-7.3.1/bin/logstash -f /usr/work/ml-latest-small/logstash.conf
tar xvf jdk-8u102-linux-x64.tar.gz -C /usr/
vi /etc/profile
. /etc/profile
[
export JAVA_HOME=/usr/jdk1.8.0_102
export PATH=$PATH:${JAVA_HOME}/bin
]
./logstash-7.3.1/bin/logstash -f /usr/work/ml-latest-small/logstash.conf
```

#### logstash.conf

```properties
input {
  file {
    path => "/usr/work/ml-latest-small/movies.csv"
    start_position => "beginning"
    sincedb_path => "/dev/null"
  }
}
filter {
  csv {
    separator => ","
    columns => ["id","content","genre"]
  }

  mutate {
    split => { "genre" => "|" }
    remove_field => ["path", "host","@timestamp","message"]
  }

  mutate {

    split => ["content", "("]
    add_field => { "title" => "%{[content][0]}"}
    add_field => { "year" => "%{[content][1]}"}
  }

#  mutate {

#    gsub => [
#      
#      "year", "\\)", ""
#    ]
#  }


  mutate {
    convert => {
      "year" => "integer"
    }
    strip => ["title"]
    remove_field => ["path", "host","@timestamp","message","content"]
  }



}
output {
   elasticsearch {
     hosts => "http://localhost:9200"
     index => "movies"
     document_id => "%{id}"
   }
  stdout {}
}

```

### elasticsearch安全通信

<https://blog.csdn.net/qq_38906421/article/details/88644315>

<https://blog.csdn.net/MicoMecy/article/details/90642163>

<https://www.elastic.co/cn/blog/getting-started-with-elasticsearch-security>

### elasticsearch性能压测

<https://blog.lyremelody.org/2018/01/31/esrally-03/>

<https://esrally.readthedocs.io/en/stable/docker.html>

<http://esrally.lyremelody.org/zh_CN/latest/summary_report.html>

<https://github.com/elastic/rally-tracks/tree/master/noaa> 测试数据集

<https://blog.csdn.net/u010824591/article/details/78123979>

<https://segmentfault.com/a/1190000011174694>

<https://www.bilibili.com/video/av27117279/>

```

docker run elastic/rally list tracks

mkdir -p $PWD/myrally
chmod 777 $PWD/myrally

docker run --rm -v $PWD/myrally:/rally/.rally elastic/rally --test-mode --pipeline=benchmark-only --target-hosts=192.168.130.27:9200 --client-options="basic_auth_user:'elastic',basic_auth_password:'xiao99@Twsm2019'" --track-path=

rally -- 拉力赛 
track -- 赛道 压测的方案、策略
car   -- index
race  -- 一场比赛 一次压测
tournament -- 规划的一次压力测试方案的目标
awards -- 总结并产生压测报告

esrally compase --baseline= --contender= 比较两次报告

race的报告分析：
time：花费的时间
latency ：请求到es后，返回的时间，有请求到es后的排队时间
service time ：请求的es处理开始到返回的时间，没有排队时间
Throughput ：吞吐量
```

##### 自定义数据集

```
路径测试或者执行
docker run -v /usr/twsm/earally/tw_es_earally_work_answer/:/usr/twsm/earally/tw_es_earally_work_answer/ elastic/rally list tracks --track-path=/usr/twsm/earally/tw_es_earally_work_answer/

docker run --rm -v /usr/twsm/earally/myrally:/rally/.rally -v /usr/twsm/earally/tw_es_earally_work_answer/:/usr/twsm/earally/tw_es_earally_work_answer/  elastic/rally  --pipeline=benchmark-only --target-hosts=192.168.130.27:9200 --client-options="basic_auth_user:'elastic',basic_auth_password:'xiao99@Twsm2019'" --track-path=/usr/twsm/earally/tw_es_earally_work_answer/

--report-file=result.csv
--report-fotmat=csv

输出到es
rally.ini
datasource.type=elasticsearch

```

### elasticsearch的组成

```
table --》index（type） ，es7.0以后只有一个_doc的type
row   --》document
column--》field
schema--》mappings
sql   --》dsl
```



```
你也许已经注意到 索引 这个词在 Elasticsearch 语境中有多种含义， 这里有必要做一些说明：

索引（名词）：

如前所述，一个 索引 类似于传统关系数据库中的一个 数据库 ，是一个存储关系型文档的地方。 索引 (index) 的复数词为 indices 或 indexes 。

索引（动词）：

索引一个文档 就是存储一个文档到一个 索引 （名词）中以便被检索和查询。这非常类似于 SQL 语句中的 INSERT 关键词，除了文档已存在时，新文档会替换旧文档情况之外。

倒排索引：

关系型数据库通过增加一个 索引 比如一个 B树（B-tree）索引 到指定的列上，以便提升数据检索速度。Elasticsearch 和 Lucene 使用了一个叫做 倒排索引 的结构来达到相同的目的。

+ 默认的，一个文档中的每一个属性都是 被索引 的（有一个倒排索引）和可搜索的。一个没有倒排索引的属性是不能被搜索到的。我们将在 倒排索引 讨论倒排索引的更多细节。
```

#### 节点介绍

<https://www.cnblogs.com/37yan/p/9928748.html>

#### 分词器

安装ik分词器：<https://www.cnblogs.com/szwdun/p/10664348.html>

```
docker 安装ElasticSearch的中文分词器IK
首先确保ElasticSearch镜像已经启动

 

安装插件
 

方式一：在线安装
进入容器

docker exec -it elasticsearch /bin/bash
在线下载并安装

./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v6.5.4/elasticsearch-analysis-ik-6.5.4.zip


进入plugins可以看到IK分词器已经安装成功



方式二：离线安装
将IK分词器上传到/tmp目录中



将压缩包移动到容器中

docker cp /tmp/elasticsearch-analysis-ik-6.5.4.zip elasticsearch:/usr/share/elasticsearch/plugins
进入容器

docker exec -it elasticsearch /bin/bash
　　　　创建目录

mkdir /usr/share/elasticsearch/plugins/ik
将文件压缩包移动到ik中

mv /usr/share/elasticsearch/plugins/elasticsearch-analysis-ik-6.5.4.zip /usr/share/elasticsearch/plugins/ik
进入目录

cd /usr/share/elasticsearch/plugins/ik
解压

unzip elasticsearch-analysis-ik-6.5.4.zip
删除压缩包

rm -rf elasticsearch-analysis-ik-6.5.4.zip
 

退出并重启镜像
exit
docker restart elasticsearch
 测试

```

```xml


POST _analyze
{
  "analyzer": "ik_smart",
  "text": "七十周年大阅兵"

}
```

#### Mappings

参考：<https://elasticsearch.cn/article/6171>

```
null_value\数组、copy_to
---------------------------------

DELETE users

PUT users
{
  "mappings":{
      "properties":{
        "firstname":{
          "type":"text"
          , "copy_to": "fullName"
        }, 
        "lastname":{
          "type":"text",
          "copy_to":"fullName"
        },
        "mobile":{
          "type":"keyword",
          "null_value":"NULL"
        }
      }
  }
}

POST users/_doc/21
{
  "firstname":"beautiful",
  "lastname":"world",
  "mobile":null
}

GET users/_search?q=fullName:(beautiful world)

POST /users/_search
{
  "query":{
    "match":{
      "fullName":{
        "query":"beautiful world",
        "operator":"and"
      }
    }
  }
}


PUT users/_doc/1
{
  "name":"onebird",
  "interests":"reading"
}

PUT users/_doc/2
{
  "name":"twobirds",
  "interests":["reading","music"]
}

POST users/_search
{
  "query":{
    "match_all":{}
  }
}
```

#### 3，基于词项和全文的搜索

```
基于词项
------------------------
1，term查询不做分词，但默认会查询已经分词后的doc的词项。
2，term查询当你需要做精准查询的时候，加上keyword，会查询分词的doc的原词。
3，term查询添加constant_score跳过算分，提高效率

全文的搜索
------------------------
1，全文搜索是会对查询的内容进行分词的，然后根据每个词项去查询doc，然后进行算分，汇总后返回给用户
2，可以通过参数控制查询的 Precision & Recall
3，基于全文查找有Match Query\Match Phrase Query\Query String Query
```

##### 实例

```
DELETE products
PUT products
{
  "settings": {
    "number_of_shards": 1
  }
}

POST /products/_bulk
{ "index": { "_id": 1 }}
{ "productID" : "XHDK-A-1293-#fJ3","desc":"iPhone" }
{ "index": { "_id": 2 }}
{ "productID" : "KDKE-B-9947-#kL5","desc":"iPad" }
{ "index": { "_id": 3 }}
{ "productID" : "JODL-X-1937-#pV7","desc":"MBP" }

GET /products

POST /products/_search
{
  "query": {
    "term": {
      "desc": {
        //"value": "iPhone"
        "value":"iphone"
      }
    }
  }
}

POST /products/_search
{
  "query": {
    "term": {
      "desc.keyword": {
        "value": "iPhone"
        //"value":"iphone"
      }
    }
  }
}

##跳过算分，提高效率
POST /products/_search
{
  "explain":true,
  "query": {
    "constant_score":{
      "filter":{
         "term": {
            "desc.keyword": {
              "value": "iPhone"
              //"value":"iphone"
            }
          }
      }
    }
  }
}

POST /_analyze
{
  "analyzer":"standard",
  "text":"XHDK-A-1293-#fJ3"
}

POST /products/_search
{
  "query": {
    "term": {
      "productID": {
        "value": "XHDK-A-1293-#fJ3"
      }
    }
  }
}

POST /products/_search
{
  //"explain": true,
  "query": {
    "term": {
      "productID.keyword": {
        "value": "XHDK-A-1293-#fJ3"
      }
    }
  }
}


POST /products/_search
{
  "explain": true,
  "query": {
    "constant_score": {
      "filter": {
        "term": {
          "productID.keyword": "XHDK-A-1293-#fJ3"
        }
      }

    }
  }
}


#设置 position_increment_gap
DELETE groups
PUT groups
{
  "mappings": {
    "properties": {
      "names":{
        "type": "text",
        "position_increment_gap": 0
      }
    }
  }
}

GET groups/_mapping

POST groups/_doc
{
  "names": [ "John Water", "Water Smith"]
}

POST groups/_search
{
  "query": {
    "match_phrase": {
      "names": {
        "query": "water",
        "slop": 100
      }
    }
  }
}


POST groups/_search
{
  "query": {
    "match_phrase": {
      "names": "Water Smith"
    }
  }
}
```

#### 4，结构化的数据

```
什么是结构化的数据
-----------------------
1，时间、日期、数字、boolean、或者某些文本（例如颜色：red、green）。
就是分不词的。就是结构化的数据。
2，一般用term或者prefix前缀匹配。
3，支持range范围查询。
4，处理多值字段（一个字段的内容是数组），term 查询是包含，而不是等于。若要实现精准匹配，需要添加 "genre_count":"2"来匹配
```

##### 实例

```

#结构化搜索，精确匹配
DELETE products
POST /products/_bulk
{ "index": { "_id": 1 }}
{ "price" : 10,"avaliable":true,"date":"2018-01-01", "productID" : "XHDK-A-1293-#fJ3" }
{ "index": { "_id": 2 }}
{ "price" : 20,"avaliable":true,"date":"2019-01-01", "productID" : "KDKE-B-9947-#kL5" }
{ "index": { "_id": 3 }}
{ "price" : 30,"avaliable":true, "productID" : "JODL-X-1937-#pV7" }
{ "index": { "_id": 4 }}
{ "price" : 30,"avaliable":false, "productID" : "QQPX-R-3956-#aD8" }

GET products/_mapping



#对布尔值 match 查询，有算分
POST products/_search
{
  "profile": "true",
  "explain": true,
  "query": {
    "term": {
      "avaliable": true
    }
  }
}

POST products/_search
{
  "query": {
    "match_phrase": {
      "avaliable": true
    }
  }
}


#对布尔值，通过constant score 转成 filtering，没有算分
POST products/_search
{
  "profile": "true",
  "explain": true,
  "query": {
    "constant_score": {
      "filter": {
        "term": {
          "avaliable": true
        }
      }
    }
  }
}


#数字类型 Term
POST products/_search
{
  "profile": "true",
  "explain": true,
  "query": {
    "term": {
      "price": 30
    }
  }
}

#数字类型 terms
POST products/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "terms": {
          "price": [
            "20",
            "30"
          ]
        }
      }
    }
  }
}

#数字 Range 查询
GET products/_search
{
    "query" : {
        "constant_score" : {
            "filter" : {
                "range" : {
                    "price" : {
                        "gte" : 20,
                        "lte"  : 30
                    }
                }
            }
        }
    }
}


# 日期 range
POST products/_search
{
    "query" : {
        "constant_score" : {
            "filter" : {
                "range" : {
                    "date" : {
                      "gte" : "now-1y"
                    }
                }
            }
        }
    }
}



#exists查询
POST products/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "exists": {
          "field": "date"
        }
      }
    }
  }
}

#处理多值字段
POST /movies/_bulk
{ "index": { "_id": 1 }}
{ "title" : "Father of the Bridge Part II","year":1995, "genre":"Comedy"}
{ "index": { "_id": 2 }}
{ "title" : "Dave","year":1993,"genre":["Comedy","Romance"] }


#处理多值字段，term 查询是包含，而不是等于
POST movies/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "term": {
          "genre.keyword": "Comedy"
        }
      }
    }
  }
}


#字符类型 terms
POST products/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "terms": {
          "productID.keyword": [
            "QQPX-R-3956-#aD8",
            "JODL-X-1937-#pV7"
          ]
        }
      }
    }
  }
}



POST products/_search
{
  "profile": "true",
  "explain": true,
  "query": {
    "match": {
      "price": 30
    }
  }
}


POST products/_search
{
  "profile": "true",
  "explain": true,
  "query": {
    "term": {
      "date": "2019-01-01"
    }
  }
}

POST products/_search
{
  "profile": "true",
  "explain": true,
  "query": {
    "match": {
      "date": "2019-01-01"
    }
  }
}




POST products/_search
{
  "profile": "true",
  "explain": true,
  "query": {
    "constant_score": {
      "filter": {
        "term": {
          "productID.keyword": "XHDK-A-1293-#fJ3"
        }
      }
    }
  }
}

POST products/_search
{
  "profile": "true",
  "explain": true,
  "query": {
    "term": {
      "productID.keyword": "XHDK-A-1293-#fJ3"
    }
  }
}

#对布尔数值
POST products/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "term": {
          "avaliable": "false"
        }
      }
    }
  }
}

POST products/_search
{
  "query": {
    "term": {
      "avaliable": {
        "value": "false"
      }
    }
  }
}

POST products/_search
{
  "profile": "true",
  "explain": true,
  "query": {
    "term": {
      "price": {
        "value": "20"
      }
    }
  }
}

POST products/_search
{
  "profile": "true",
  "explain": true,
  "query": {
    "match": {
      "price": "20"
    }
    }
  }
}


POST products/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "bool": {
          "must_not": {
            "exists": {
              "field": "date"
            }
          }
        }
      }
    }
  }
}

```

#### 5，搜索相关性算分

```
1，搜索的相关性就是一个文档与查询语句的匹配程度。es会对每个匹配查询条件的结果进行算分。
2，打分的本质是排序，将符合用户需求的文档排在前面。
3，采用的是BM 25算法
4，词频（Term Frequery）：就是查询的词在doc中出现的频率（查询的次数除以doc的总字数）。度量一条查询与结果相关性的简单方法就是将搜索的每一个词的TF进行相加。TF(A)+TF(B)
5，[TF-IDF]本质就是TF求和变成了加权求和。（DF就是词在所有的文档中出现的频率，IDF就是log(全部文档总数/查询词出现过的文档数)）。TF(A)*IDF(A)+TF(B)*IDF(B)
算分公式：见附件
6，BM25算分公式
7，boosting query是相关度的一种手段，参数boost的含义
当大于1的时候，打分相关度提升；当小于1大于0的时候，打分的相关度降低；当小于0的时候，贡献负分。
```

##### 实例

```

PUT testscore
{
  "settings": {
    "number_of_shards": 1
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text"
      }
    }
  }
}

PUT testscore/_bulk
{ "index": { "_id": 1 }}
{ "content":"we use Elasticsearch to power the search" }
{ "index": { "_id": 2 }}
{ "content":"we like elasticsearch" }
{ "index": { "_id": 3 }}
{ "content":"The scoring of documents is caculated by the scoring formula" }
{ "index": { "_id": 4 }}
{ "content":"you know, for search" }


POST /testscore/_search
{
  "explain": true,
  "query": {
    "match": {
      //"content":"you"
      "content": "elasticsearch"
      //"content":"the"
      //"content": "the elasticsearch"
    }
  }
}

POST testscore/_search
{
    "explain":true,
    "query": {
        "boosting" : {
            "positive" : {
                "term" : {
                    "content" : "elasticsearch"
                }
            },
            "negative" : {
                 "term" : {
                     "content" : "like"
                }
            },
            "negative_boost" : "-0.2"
        }
    }
}


POST tmdb/_search
{
  "_source": ["title","overview"],
  "query": {
    "more_like_this": {
      "fields": [
        "title^10","overview"
      ],
      "like": [{"_id":"14191"}],
      "min_term_freq": 1,
      "max_query_terms": 12
    }
  }
}
```

#### 6，Query与Filtering与多字符串多字段的查询

```
1，query会有相关性算分；filter不需要算分，可以利用cache，性能更好。
2，bool query查询：支持一个或多个查询子句的组合。（总共有4种子句：must（必须匹配，算分。相对于and），should（(OR)选择性匹配，算分），must_not(必须不能匹配，不算分)，filter（必须匹配，不算分））。
3，支持嵌套
```

##### 实例

```
POST /products/_bulk
{ "index": { "_id": 1 }}
{ "price" : 10,"avaliable":true,"date":"2018-01-01", "productID" : "XHDK-A-1293-#fJ3" }
{ "index": { "_id": 2 }}
{ "price" : 20,"avaliable":true,"date":"2019-01-01", "productID" : "KDKE-B-9947-#kL5" }
{ "index": { "_id": 3 }}
{ "price" : 30,"avaliable":true, "productID" : "JODL-X-1937-#pV7" }
{ "index": { "_id": 4 }}
{ "price" : 30,"avaliable":false, "productID" : "QQPX-R-3956-#aD8" }



#基本语法
POST /products/_search
{
  "query": {
    "bool" : {
      "must" : {
        "term" : { "price" : "30" }
      },
      "filter": {
        "term" : { "avaliable" : "true" }
      },
      "must_not" : {
        "range" : {
          "price" : { "lte" : 10 }
        }
      },
      "should" : [
        { "term" : { "productID.keyword" : "JODL-X-1937-#pV7" } },
        { "term" : { "productID.keyword" : "XHDK-A-1293-#fJ3" } }
      ],
      "minimum_should_match" :1
    }
  }
}

#改变数据模型，增加字段。解决数组包含而不是精确匹配的问题
POST /newmovies/_bulk
{ "index": { "_id": 1 }}
{ "title" : "Father of the Bridge Part II","year":1995, "genre":"Comedy","genre_count":1 }
{ "index": { "_id": 2 }}
{ "title" : "Dave","year":1993,"genre":["Comedy","Romance"],"genre_count":2 }

#must，有算分
POST /newmovies/_search
{
  "query": {
    "bool": {
      "must": [
        {"term": {"genre.keyword": {"value": "Comedy"}}},
        {"term": {"genre_count": {"value": 1}}}

      ]
    }
  }
}

#Filter。不参与算分，结果的score是0
POST /newmovies/_search
{
  "query": {
    "bool": {
      "filter": [
        {"term": {"genre.keyword": {"value": "Comedy"}}},
        {"term": {"genre_count": {"value": 1}}}
        ]

    }
  }
}


#Filtering Context
POST _search
{
  "query": {
    "bool" : {

      "filter": {
        "term" : { "avaliable" : "true" }
      },
      "must_not" : {
        "range" : {
          "price" : { "lte" : 10 }
        }
      }
    }
  }
}


#Query Context
POST /products/_bulk
{ "index": { "_id": 1 }}
{ "price" : 10,"avaliable":true,"date":"2018-01-01", "productID" : "XHDK-A-1293-#fJ3" }
{ "index": { "_id": 2 }}
{ "price" : 20,"avaliable":true,"date":"2019-01-01", "productID" : "KDKE-B-9947-#kL5" }
{ "index": { "_id": 3 }}
{ "price" : 30,"avaliable":true, "productID" : "JODL-X-1937-#pV7" }
{ "index": { "_id": 4 }}
{ "price" : 30,"avaliable":false, "productID" : "QQPX-R-3956-#aD8" }


POST /products/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "term": {
            "productID.keyword": {
              "value": "JODL-X-1937-#pV7"}}
        },
        {"term": {"avaliable": {"value": true}}
        }
      ]
    }
  }
}


#嵌套，实现了 should not 逻辑
POST /products/_search
{
  "query": {
    "bool": {
      "must": {
        "term": {
          "price": "30"
        }
      },
      "should": [
        {
          "bool": {
            "must_not": {
              "term": {
                "avaliable": "true"
              }
            }
          }
        }
      ],
      "minimum_should_match": 1
    }
  }
}


#Controll the Precision
POST _search
{
  "query": {
    "bool" : {
      "must" : {
        "term" : { "price" : "30" }
      },
      "filter": {
        "term" : { "avaliable" : "true" }
      },
      "must_not" : {
        "range" : {
          "price" : { "lte" : 10 }
        }
      },
      "should" : [
        { "term" : { "productID.keyword" : "JODL-X-1937-#pV7" } },
        { "term" : { "productID.keyword" : "XHDK-A-1293-#fJ3" } }
      ],
      "minimum_should_match" :2
    }
  }
}



POST /animals/_search
{
  "query": {
    "bool": {
      "should": [
        { "term": { "text": "brown" }},
        { "term": { "text": "red" }},
        { "term": { "text": "quick"   }},
        { "term": { "text": "dog"   }}
      ]
    }
  }
}

POST /animals/_search
{
  "query": {
    "bool": {
      "should": [
        { "term": { "text": "quick" }},
        { "term": { "text": "dog"   }},
        {
          "bool":{
            "should":[
               { "term": { "text": "brown" }},
                 { "term": { "text": "brown" }},
            ]
          }

        }
      ]
    }
  }
}


DELETE blogs
POST /blogs/_bulk
{ "index": { "_id": 1 }}
{"title":"Apple iPad", "content":"Apple iPad,Apple iPad" }
{ "index": { "_id": 2 }}
{"title":"Apple iPad,Apple iPad", "content":"Apple iPad" }


POST blogs/_search
{
  "query": {
    "bool": {
      "should": [
        {"match": {
          "title": {
            "query": "apple,ipad",
            "boost": 1.1
          }
        }},

        {"match": {
          "content": {
            "query": "apple,ipad",
            "boost":
          }
        }}
      ]
    }
  }
}

DELETE news
POST /news/_bulk
{ "index": { "_id": 1 }}
{ "content":"Apple Mac" }
{ "index": { "_id": 2 }}
{ "content":"Apple iPad" }
{ "index": { "_id": 3 }}
{ "content":"Apple employee like Apple Pie and Apple Juice" }


POST news/_search
{
  "query": {
    "bool": {
      "must": {
        "match":{"content":"apple"}
      }
    }
  }
}

POST news/_search
{
  "query": {
    "bool": {
      "must": {
        "match":{"content":"apple"}
      },
      "must_not": {
        "match":{"content":"pie"}
      }
    }
  }
}

POST news/_search
{
  "query": {
    "boosting": {
      "positive": {
        "match": {
          "content": "apple"
        }
      },
      "negative": {
        "match": {
          "content": "pie"
        }
      },
      "negative_boost": 0.5
    }
  }
}

```

#### 7，单字符串多字段查询：Dis Max Query

```
1，dis Max Query 不会考虑多个字段的综合得分，仅仅会单个字段最匹配的情况算分。
2，若想在最匹配的基础上，综合其他的字段的得分需要tie_breaker参数（0-1区间）。（0表示最佳匹配、1表示同等重要）
```

##### 实例

```
PUT /blogs/_doc/1
{
    "title": "Quick brown rabbits",
    "body":  "Brown rabbits are commonly seen."
}

PUT /blogs/_doc/2
{
    "title": "Keeping pets healthy",
    "body":  "My quick brown fox eats rabbits on a regular basis."
}

POST /blogs/_search
{
    "query": {
        "bool": {
            "should": [
                { "match": { "title": "Brown fox" }},
                { "match": { "body":  "Brown fox" }}
            ]
        }
    }
}

POST blogs/_search
{
    "query": {
        "dis_max": {
            "queries": [
                { "match": { "title": "Brown fox" }},
                { "match": { "body":  "Brown fox" }}
            ]
        }
    }
}


POST blogs/_search
{
    "query": {
        "dis_max": {
            "queries": [
                { "match": { "title": "Quick pets" }},
                { "match": { "body":  "Quick pets" }}
            ],
            "tie_breaker": 0.2
        }
    }
}
```

#### 8，单字符多字段查询：Mutil Match

```
最佳字段、多数字段、混合字段
```

##### 实例

```
POST blogs/_search
{
    "query": {
        "dis_max": {
            "queries": [
                { "match": { "title": "Quick pets" }},
                { "match": { "body":  "Quick pets" }}
            ],
            "tie_breaker": 0.2
        }
    }
}

POST blogs/_search
{
  "query": {
    "multi_match": {
      "type": "best_fields",
      "query": "Quick pets",
      "fields": ["title","body"],
      "tie_breaker": 0.2,
      "minimum_should_match": "20%"
    }
  }
}



POST books/_search
{
    "multi_match": {
        "query":  "Quick brown fox",
        "fields": "*_title"
    }
}


POST books/_search
{
    "multi_match": {
        "query":  "Quick brown fox",
        "fields": [ "*_title", "chapter_title^2" ]
    }
}



DELETE /titles
PUT /titles
{
    "settings": { "number_of_shards": 1 },
    "mappings": {
        "my_type": {
            "properties": {
                "title": {
                    "type":     "string",
                    "analyzer": "english",
                    "fields": {
                        "std":   {
                            "type":     "string",
                            "analyzer": "standard"
                        }
                    }
                }
            }
        }
    }
}

PUT /titles
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "english"
      }
    }
  }
}

POST titles/_bulk
{ "index": { "_id": 1 }}
{ "title": "My dog barks" }
{ "index": { "_id": 2 }}
{ "title": "I see a lot of barking dogs on the road " }


GET titles/_search
{
  "query": {
    "match": {
      "title": "barking dogs"
    }
  }
}

DELETE /titles
PUT /titles
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "english",
        "fields": {"std": {"type": "text","analyzer": "standard"}}
      }
    }
  }
}

POST titles/_bulk
{ "index": { "_id": 1 }}
{ "title": "My dog barks" }
{ "index": { "_id": 2 }}
{ "title": "I see a lot of barking dogs on the road " }

GET /titles/_search
{
   "query": {
        "multi_match": {
            "query":  "barking dogs",
            "type":   "most_fields",
            "fields": [ "title", "title.std" ]
        }
    }
}

GET /titles/_search
{
   "query": {
        "multi_match": {
            "query":  "barking dogs",
            "type":   "most_fields",
            "fields": [ "title^10", "title.std" ]
        }
    }
}
```

#### 9，中文分词与搜索

```
参考前面的安装
```

##### 实例

```
POST _analyze
{
  "analyzer": "ik_smart",
  "text": "七十周年大阅兵"

}
```

#### 10，search Template 和 Index Alias查询

```
search Template
---------------------
搜索的模板

Index Alias
----------------------
index 起别名
```

##### 实例

```
POST _scripts/tmdb
{
  "script": {
    "lang": "mustache",
    "source": {
      "_source": [
        "title","overview"
      ],
      "size": 20,
      "query": {
        "multi_match": {
          "query": "{{q}}",
          "fields": ["title","overview"]
        }
      }
    }
  }
}
DELETE _scripts/tmdb

GET _scripts/tmdb

POST tmdb/_search/template
{
    "id":"tmdb",
    "params": {
        "q": "basketball with cartoon aliens"
    }
}


PUT movies-2019/_doc/1
{
  "name":"the matrix",
  "rating":5
}

PUT movies-2019/_doc/2
{
  "name":"Speed",
  "rating":3
}

GET movies-2019

GET movies-2019/_search

POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "movies-2019",
        "alias": "movies-latest"
      }
    }
  ]
}

POST movies-latest/_search
{
  "query": {
    "match_all": {}
  }
}

POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "movies-2019",
        "alias": "movies-lastest-highrate",
        "filter": {
          "range": {
            "rating": {
              "gte": 4
            }
          }
        }
      }
    }
  ]
}

POST movies-lastest-highrate/_search
{
  "query": {
    "match_all": {}
  }
}
```

#### 11，综合排序：Function Score Query 优化算分

##### 实例

```
DELETE blogs
PUT /blogs/_doc/1
{
  "title":   "About popularity",
  "content": "In this post we will talk about...",
  "votes":   0
}

PUT /blogs/_doc/2
{
  "title":   "About popularity",
  "content": "In this post we will talk about...",
  "votes":   100
}

PUT /blogs/_doc/3
{
  "title":   "About popularity",
  "content": "In this post we will talk about...",
  "votes":   1000000
}


POST /blogs/_search
{
  "query": {
    "function_score": {
      "query": {
        "multi_match": {
          "query":    "popularity",
          "fields": [ "title", "content" ]
        }
      },
      "field_value_factor": {
        "field": "votes"
      }
    }
  }
}

POST /blogs/_search
{
  "query": {
    "function_score": {
      "query": {
        "multi_match": {
          "query":    "popularity",
          "fields": [ "title", "content" ]
        }
      },
      "field_value_factor": {
        "field": "votes",
        "modifier": "log1p"
      }
    }
  }
}


POST /blogs/_search
{
  "query": {
    "function_score": {
      "query": {
        "multi_match": {
          "query":    "popularity",
          "fields": [ "title", "content" ]
        }
      },
      "field_value_factor": {
        "field": "votes",
        "modifier": "log1p" ,
        "factor": 0.1
      }
    }
  }
}


POST /blogs/_search
{
  "query": {
    "function_score": {
      "query": {
        "multi_match": {
          "query":    "popularity",
          "fields": [ "title", "content" ]
        }
      },
      "field_value_factor": {
        "field": "votes",
        "modifier": "log1p" ,
        "factor": 0.1
      },
      "boost_mode": "sum",
      "max_boost": 3
    }
  }
}

POST /blogs/_search
{
  "query": {
    "function_score": {
      "random_score": {
        "seed": 911119
      }
    }
  }
}
```

#### 12，排序及Doc Values & Fielddata

```
 排序
 ---------------------
 指定字段排序用的是正排索引。默认的排序会根据function score query算分，用的是倒排索引。
 
 Fielddata
 ---------------------
 text类型需要打开fielddata
 
 Doc Values
 ---------------------
 是列式存储，对Text类型无效。
```

##### 实例

```
#单字段排序
POST /kibana_sample_data_ecommerce/_search
{
  "size": 5,
  "query": {
    "match_all": {

    }
  },
  "sort": [
    {"order_date": {"order": "desc"}}
  ]
}

#多字段排序
POST /kibana_sample_data_ecommerce/_search
{
  "size": 5,
  "query": {
    "match_all": {

    }
  },
  "sort": [
    {"order_date": {"order": "desc"}},
    {"_doc":{"order": "asc"}},
    {"_score":{ "order": "desc"}}
  ]
}

GET kibana_sample_data_ecommerce/_mapping

#对 text 字段进行排序。默认会报错，需打开fielddata
POST /kibana_sample_data_ecommerce/_search
{
  "size": 5,
  "query": {
    "match_all": {

    }
  },
  "sort": [
    {"customer_full_name": {"order": "desc"}}
  ]
}

#打开 text的 fielddata
PUT kibana_sample_data_ecommerce/_mapping
{
  "properties": {
    "customer_full_name" : {
          "type" : "text",
          "fielddata": true,
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
  }
}

#关闭 keyword的 doc values
PUT test_keyword
PUT test_keyword/_mapping
{
  "properties": {
    "user_name":{
      "type": "keyword",
      "doc_values":false
    }
  }
}

DELETE test_keyword

PUT test_text
PUT test_text/_mapping
{
  "properties": {
    "intro":{
      "type": "text",
      "doc_values":true
    }
  }
}

DELETE test_text


DELETE temp_users
PUT temp_users
PUT temp_users/_mapping
{
  "properties": {
    "name":{"type": "text","fielddata": true},
    "desc":{"type": "text","fielddata": true}
  }
}

Post temp_users/_doc
{"name":"Jack","desc":"Jack is a good boy!","age":10}

#打开fielddata 后，查看 docvalue_fields数据
POST  temp_users/_search
{
  "docvalue_fields": [
    "name","desc"
    ]
}

#查看整型字段的docvalues
POST  temp_users/_search
{
  "docvalue_fields": [
    "age"
    ]
}
```

#### 13，分页与遍历 - From, Size, Search_after & Scroll API

```
深度分页的问题：用Search_after处理
------------------------------
1，es设置的深度分页的上限：index_max_result_window
2，为什么有这个问题，因为页数太多消耗内存。
3，search_after后添加的是上一次搜索的sort内容。
POST users/_search
{
    "size": 2,
    "query": {
        "match_all": {}
    },
    
    "search_after":
        [
        30,
          "6O83bG0BCrF_vjCbSLDO"],
    "sort": [
        {"age": "desc"} ,
        {"_id": "asc"}    
    ]
}

4，scroll Api设置后不能及时刷新新增的记录。

```

##### 实例

```
POST tmdb/_search
{
  "from": 10000,
  "size": 1,
  "query": {
    "match_all": {

    }
  }
}

#Scroll API
DELETE users

POST users/_doc
{"name":"user1","age":10}

POST users/_doc
{"name":"user2","age":11}


POST users/_doc
{"name":"user2","age":12}

POST users/_doc
{"name":"user2","age":13}

POST users/_count

POST users/_search
{
    "size": 1,
    "query": {
        "match_all": {}
    },
    "sort": [
        {"age": "desc"} ,
        {"_id": "asc"}    
    ]
}

POST users/_search
{
    "size": 1,
    "query": {
        "match_all": {}
    },
    "search_after":
        [
          10,
          "ZQ0vYGsBrR8X3IP75QqX"],
    "sort": [
        {"age": "desc"} ,
        {"_id": "asc"}    
    ]
}


#Scroll API
DELETE users
POST users/_doc
{"name":"user1","age":10}

POST users/_doc
{"name":"user2","age":20}

POST users/_doc
{"name":"user3","age":30}

POST users/_doc
{"name":"user4","age":40}

POST /users/_search?scroll=5m
{
    "size": 1,
    "query": {
        "match_all" : {
        }
    }
}


POST users/_doc
{"name":"user5","age":50}
POST /_search/scroll
{
    "scroll" : "1m",
    "scroll_id" : "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAWAWbWdoQXR2d3ZUd2kzSThwVTh4bVE0QQ=="
}
```

#### 14，处理并发读写操作

```
并发更新的情况下版本控制：
-----------------
if_seq_no=9&if_primary_term=1
version=30008&version_type=external

```

##### 实例

```

DELETE products
PUT products

PUT products/_doc/1
{
  "title":"iphone",
  "count":100
}

GET products/_search

PUT products/_doc/1?if_seq_no=9&if_primary_term=1
{
  "title":"iphone",
  "count":106
}

PUT products/_doc/1?version=30008&version_type=external
{
  "title":"iphone",
  "count":100
}
```

#### 15，Bucket & Metric Aggregation

```
1，group by 相对于 Bucket 分类统计，可以对term分桶、对range、histogram进行分桶（即区间分桶）
2，sum等聚合 相对于 Metric Arregation，其中cardinate相对于distinct
3，打开eager_global_ordinls : ture ，在做terms聚合的时候性能提升
```

##### 实例

```
DELETE /employees
PUT /employees/
{
  "mappings" : {
      "properties" : {
        "age" : {
          "type" : "integer"
        },
        "gender" : {
          "type" : "keyword"
        },
        "job" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 50
            }
          }
        },
        "name" : {
          "type" : "keyword"
        },
        "salary" : {
          "type" : "integer"
        }
      }
    }
}

PUT /employees/_bulk
{ "index" : {  "_id" : "1" } }
{ "name" : "Emma","age":32,"job":"Product Manager","gender":"female","salary":35000 }
{ "index" : {  "_id" : "2" } }
{ "name" : "Underwood","age":41,"job":"Dev Manager","gender":"male","salary": 50000}
{ "index" : {  "_id" : "3" } }
{ "name" : "Tran","age":25,"job":"Web Designer","gender":"male","salary":18000 }
{ "index" : {  "_id" : "4" } }
{ "name" : "Rivera","age":26,"job":"Web Designer","gender":"female","salary": 22000}
{ "index" : {  "_id" : "5" } }
{ "name" : "Rose","age":25,"job":"QA","gender":"female","salary":18000 }
{ "index" : {  "_id" : "6" } }
{ "name" : "Lucy","age":31,"job":"QA","gender":"female","salary": 25000}
{ "index" : {  "_id" : "7" } }
{ "name" : "Byrd","age":27,"job":"QA","gender":"male","salary":20000 }
{ "index" : {  "_id" : "8" } }
{ "name" : "Foster","age":27,"job":"Java Programmer","gender":"male","salary": 20000}
{ "index" : {  "_id" : "9" } }
{ "name" : "Gregory","age":32,"job":"Java Programmer","gender":"male","salary":22000 }
{ "index" : {  "_id" : "10" } }
{ "name" : "Bryant","age":20,"job":"Java Programmer","gender":"male","salary": 9000}
{ "index" : {  "_id" : "11" } }
{ "name" : "Jenny","age":36,"job":"Java Programmer","gender":"female","salary":38000 }
{ "index" : {  "_id" : "12" } }
{ "name" : "Mcdonald","age":31,"job":"Java Programmer","gender":"male","salary": 32000}
{ "index" : {  "_id" : "13" } }
{ "name" : "Jonthna","age":30,"job":"Java Programmer","gender":"female","salary":30000 }
{ "index" : {  "_id" : "14" } }
{ "name" : "Marshall","age":32,"job":"Javascript Programmer","gender":"male","salary": 25000}
{ "index" : {  "_id" : "15" } }
{ "name" : "King","age":33,"job":"Java Programmer","gender":"male","salary":28000 }
{ "index" : {  "_id" : "16" } }
{ "name" : "Mccarthy","age":21,"job":"Javascript Programmer","gender":"male","salary": 16000}
{ "index" : {  "_id" : "17" } }
{ "name" : "Goodwin","age":25,"job":"Javascript Programmer","gender":"male","salary": 16000}
{ "index" : {  "_id" : "18" } }
{ "name" : "Catherine","age":29,"job":"Javascript Programmer","gender":"female","salary": 20000}
{ "index" : {  "_id" : "19" } }
{ "name" : "Boone","age":30,"job":"DBA","gender":"male","salary": 30000}
{ "index" : {  "_id" : "20" } }
{ "name" : "Kathy","age":29,"job":"DBA","gender":"female","salary": 20000}

# Metric 聚合，找到最低的工资
POST employees/_search
{
  "size": 0,
  "aggs": {
    "min_salary": {
      "min": {
        "field":"salary"
      }
    }
  }
}

# Metric 聚合，找到最高的工资
POST employees/_search
{
  "size": 0,
  "aggs": {
    "max_salary": {
      "max": {
        "field":"salary"
      }
    }
  }
}

# 多个 Metric 聚合，找到最低最高和平均工资
POST employees/_search
{
  "size": 0,
  "aggs": {
    "max_salary": {
      "max": {
        "field": "salary"
      }
    },
    "min_salary": {
      "min": {
        "field": "salary"
      }
    },
    "avg_salary": {
      "avg": {
        "field": "salary"
      }
    }
  }
}

# 一个聚合，输出多值
POST employees/_search
{
  "size": 0,
  "aggs": {
    "stats_salary": {
      "stats": {
        "field":"salary"
      }
    }
  }
}




# 对keword 进行聚合
POST employees/_search
{
  "size": 0,
  "aggs": {
    "jobs": {
      "terms": {
        "field":"job.keyword"
      }
    }
  }
}


# 对 Text 字段进行 terms 聚合查询，失败
POST employees/_search
{
  "size": 0,
  "aggs": {
    "jobs": {
      "terms": {
        "field":"job"
      }
    }
  }
}

# 对 Text 字段打开 fielddata，支持terms aggregation
PUT employees/_mapping
{
  "properties" : {
    "job":{
       "type":     "text",
       "fielddata": true
    }
  }
}


# 对 Text 字段进行 terms 分词。分词后的terms
POST employees/_search
{
  "size": 0,
  "aggs": {
    "jobs": {
      "terms": {
        "field":"job"
      }
    }
  }
}

POST employees/_search
{
  "size": 0,
  "aggs": {
    "jobs": {
      "terms": {
        "field":"job.keyword"
      }
    }
  }
}


# 对job.keyword 和 job 进行 terms 聚合，分桶的总数并不一样
POST employees/_search
{
  "size": 0,
  "aggs": {
    "cardinate": {
      "cardinality": {
        "field": "job"
      }
    }
  }
}


# 对 性别的 keyword 进行聚合
POST employees/_search
{
  "size": 0,
  "aggs": {
    "gender": {
      "terms": {
        "field":"gender"
      }
    }
  }
}


#指定 bucket 的 size
POST employees/_search
{
  "size": 0,
  "aggs": {
    "ages_5": {
      "terms": {
        "field":"age",
        "size":3
      }
    }
  }
}



# 指定size，不同工种中，年纪最大的3个员工的具体信息
POST employees/_search
{
  "size": 0,
  "aggs": {
    "jobs": {
      "terms": {
        "field":"job.keyword"
      },
      "aggs":{
        "old_employee":{
          "top_hits":{
            "size":3,
            "sort":[
              {
                "age":{
                  "order":"desc"
                }
              }
            ]
          }
        }
      }
    }
  }
}



#Salary Ranges 分桶，可以自己定义 key
POST employees/_search
{
  "size": 0,
  "aggs": {
    "salary_range": {
      "range": {
        "field":"salary",
        "ranges":[
          {
            "to":10000
          },
          {
            "from":10000,
            "to":20000
          },
          {
            "key":">20000",
            "from":20000
          }
        ]
      }
    }
  }
}


#Salary Histogram,工资0到10万，以 5000一个区间进行分桶
POST employees/_search
{
  "size": 0,
  "aggs": {
    "salary_histrogram": {
      "histogram": {
        "field":"salary",
        "interval":5000,
        "extended_bounds":{
          "min":0,
          "max":100000

        }
      }
    }
  }
}


# 嵌套聚合1，按照工作类型分桶，并统计工资信息
POST employees/_search
{
  "size": 0,
  "aggs": {
    "Job_salary_stats": {
      "terms": {
        "field": "job.keyword"
      },
      "aggs": {
        "salary": {
          "stats": {
            "field": "salary"
          }
        }
      }
    }
  }
}

# 多次嵌套。根据工作类型分桶，然后按照性别分桶，计算工资的统计信息
POST employees/_search
{
  "size": 0,
  "aggs": {
    "Job_gender_stats": {
      "terms": {
        "field": "job.keyword"
      },
      "aggs": {
        "gender_stats": {
          "terms": {
            "field": "gender"
          },
          "aggs": {
            "salary_stats": {
              "stats": {
                "field": "salary"
              }
            }
          }
        }
      }
    }
  }
}
```

#### 16，Pipeline 聚合分析

```
在bucket的基础上做二次聚合分析。
```

##### 实例

```
DELETE employees
PUT /employees/_bulk
{ "index" : {  "_id" : "1" } }
{ "name" : "Emma","age":32,"job":"Product Manager","gender":"female","salary":35000 }
{ "index" : {  "_id" : "2" } }
{ "name" : "Underwood","age":41,"job":"Dev Manager","gender":"male","salary": 50000}
{ "index" : {  "_id" : "3" } }
{ "name" : "Tran","age":25,"job":"Web Designer","gender":"male","salary":18000 }
{ "index" : {  "_id" : "4" } }
{ "name" : "Rivera","age":26,"job":"Web Designer","gender":"female","salary": 22000}
{ "index" : {  "_id" : "5" } }
{ "name" : "Rose","age":25,"job":"QA","gender":"female","salary":18000 }
{ "index" : {  "_id" : "6" } }
{ "name" : "Lucy","age":31,"job":"QA","gender":"female","salary": 25000}
{ "index" : {  "_id" : "7" } }
{ "name" : "Byrd","age":27,"job":"QA","gender":"male","salary":20000 }
{ "index" : {  "_id" : "8" } }
{ "name" : "Foster","age":27,"job":"Java Programmer","gender":"male","salary": 20000}
{ "index" : {  "_id" : "9" } }
{ "name" : "Gregory","age":32,"job":"Java Programmer","gender":"male","salary":22000 }
{ "index" : {  "_id" : "10" } }
{ "name" : "Bryant","age":20,"job":"Java Programmer","gender":"male","salary": 9000}
{ "index" : {  "_id" : "11" } }
{ "name" : "Jenny","age":36,"job":"Java Programmer","gender":"female","salary":38000 }
{ "index" : {  "_id" : "12" } }
{ "name" : "Mcdonald","age":31,"job":"Java Programmer","gender":"male","salary": 32000}
{ "index" : {  "_id" : "13" } }
{ "name" : "Jonthna","age":30,"job":"Java Programmer","gender":"female","salary":30000 }
{ "index" : {  "_id" : "14" } }
{ "name" : "Marshall","age":32,"job":"Javascript Programmer","gender":"male","salary": 25000}
{ "index" : {  "_id" : "15" } }
{ "name" : "King","age":33,"job":"Java Programmer","gender":"male","salary":28000 }
{ "index" : {  "_id" : "16" } }
{ "name" : "Mccarthy","age":21,"job":"Javascript Programmer","gender":"male","salary": 16000}
{ "index" : {  "_id" : "17" } }
{ "name" : "Goodwin","age":25,"job":"Javascript Programmer","gender":"male","salary": 16000}
{ "index" : {  "_id" : "18" } }
{ "name" : "Catherine","age":29,"job":"Javascript Programmer","gender":"female","salary": 20000}
{ "index" : {  "_id" : "19" } }
{ "name" : "Boone","age":30,"job":"DBA","gender":"male","salary": 30000}
{ "index" : {  "_id" : "20" } }
{ "name" : "Kathy","age":29,"job":"DBA","gender":"female","salary": 20000}



# 平均工资最低的工作类型
POST employees/_search
{
  "size": 0,
  "aggs": {
    "jobs": {
      "terms": {
        "field": "job.keyword",
        "size": 10
      },
      "aggs": {
        "avg_salary": {
          "avg": {
            "field": "salary"
          }
        }
      }
    },
    "min_salary_by_job":{
      "min_bucket": {
        "buckets_path": "jobs>avg_salary"
      }
    }
  }
}


# 平均工资最高的工作类型
POST employees/_search
{
  "size": 0,
  "aggs": {
    "jobs": {
      "terms": {
        "field": "job.keyword",
        "size": 10
      },
      "aggs": {
        "avg_salary": {
          "avg": {
            "field": "salary"
          }
        }
      }
    },
    "max_salary_by_job":{
      "max_bucket": {
        "buckets_path": "jobs>avg_salary"
      }
    }
  }
}


# 平均工资的平均工资
POST employees/_search
{
  "size": 0,
  "aggs": {
    "jobs": {
      "terms": {
        "field": "job.keyword",
        "size": 10
      },
      "aggs": {
        "avg_salary": {
          "avg": {
            "field": "salary"
          }
        }
      }
    },
    "avg_salary_by_job":{
      "avg_bucket": {
        "buckets_path": "jobs>avg_salary"
      }
    }
  }
}


# 平均工资的统计分析
POST employees/_search
{
  "size": 0,
  "aggs": {
    "jobs": {
      "terms": {
        "field": "job.keyword",
        "size": 10
      },
      "aggs": {
        "avg_salary": {
          "avg": {
            "field": "salary"
          }
        }
      }
    },
    "stats_salary_by_job":{
      "stats_bucket": {
        "buckets_path": "jobs>avg_salary"
      }
    }
  }
}


# 平均工资的百分位数
POST employees/_search
{
  "size": 0,
  "aggs": {
    "jobs": {
      "terms": {
        "field": "job.keyword",
        "size": 10
      },
      "aggs": {
        "avg_salary": {
          "avg": {
            "field": "salary"
          }
        }
      }
    },
    "percentiles_salary_by_job":{
      "percentiles_bucket": {
        "buckets_path": "jobs>avg_salary"
      }
    }
  }
}



#按照年龄对平均工资求导
POST employees/_search
{
  "size": 0,
  "aggs": {
    "age": {
      "histogram": {
        "field": "age",
        "min_doc_count": 1,
        "interval": 1
      },
      "aggs": {
        "avg_salary": {
          "avg": {
            "field": "salary"
          }
        },
        "derivative_avg_salary":{
          "derivative": {
            "buckets_path": "avg_salary"
          }
        }
      }
    }
  }
}


#Cumulative_sum
POST employees/_search
{
  "size": 0,
  "aggs": {
    "age": {
      "histogram": {
        "field": "age",
        "min_doc_count": 1,
        "interval": 1
      },
      "aggs": {
        "avg_salary": {
          "avg": {
            "field": "salary"
          }
        },
        "cumulative_salary":{
          "cumulative_sum": {
            "buckets_path": "avg_salary"
          }
        }
      }
    }
  }
}

#Moving Function
POST employees/_search
{
  "size": 0,
  "aggs": {
    "age": {
      "histogram": {
        "field": "age",
        "min_doc_count": 1,
        "interval": 1
      },
      "aggs": {
        "avg_salary": {
          "avg": {
            "field": "salary"
          }
        },
        "moving_avg_salary":{
          "moving_fn": {
            "buckets_path": "avg_salary",
            "window":10,
            "script": "MovingFunctions.min(values)"
          }
        }
      }
    }
  }
}
```

#### 17，作用范围与排序

```

```

##### 实例

```
DELETE /employees
PUT /employees/
{
  "mappings" : {
      "properties" : {
        "age" : {
          "type" : "integer"
        },
        "gender" : {
          "type" : "keyword"
        },
        "job" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 50
            }
          }
        },
        "name" : {
          "type" : "keyword"
        },
        "salary" : {
          "type" : "integer"
        }
      }
    }
}

PUT /employees/_bulk
{ "index" : {  "_id" : "1" } }
{ "name" : "Emma","age":32,"job":"Product Manager","gender":"female","salary":35000 }
{ "index" : {  "_id" : "2" } }
{ "name" : "Underwood","age":41,"job":"Dev Manager","gender":"male","salary": 50000}
{ "index" : {  "_id" : "3" } }
{ "name" : "Tran","age":25,"job":"Web Designer","gender":"male","salary":18000 }
{ "index" : {  "_id" : "4" } }
{ "name" : "Rivera","age":26,"job":"Web Designer","gender":"female","salary": 22000}
{ "index" : {  "_id" : "5" } }
{ "name" : "Rose","age":25,"job":"QA","gender":"female","salary":18000 }
{ "index" : {  "_id" : "6" } }
{ "name" : "Lucy","age":31,"job":"QA","gender":"female","salary": 25000}
{ "index" : {  "_id" : "7" } }
{ "name" : "Byrd","age":27,"job":"QA","gender":"male","salary":20000 }
{ "index" : {  "_id" : "8" } }
{ "name" : "Foster","age":27,"job":"Java Programmer","gender":"male","salary": 20000}
{ "index" : {  "_id" : "9" } }
{ "name" : "Gregory","age":32,"job":"Java Programmer","gender":"male","salary":22000 }
{ "index" : {  "_id" : "10" } }
{ "name" : "Bryant","age":20,"job":"Java Programmer","gender":"male","salary": 9000}
{ "index" : {  "_id" : "11" } }
{ "name" : "Jenny","age":36,"job":"Java Programmer","gender":"female","salary":38000 }
{ "index" : {  "_id" : "12" } }
{ "name" : "Mcdonald","age":31,"job":"Java Programmer","gender":"male","salary": 32000}
{ "index" : {  "_id" : "13" } }
{ "name" : "Jonthna","age":30,"job":"Java Programmer","gender":"female","salary":30000 }
{ "index" : {  "_id" : "14" } }
{ "name" : "Marshall","age":32,"job":"Javascript Programmer","gender":"male","salary": 25000}
{ "index" : {  "_id" : "15" } }
{ "name" : "King","age":33,"job":"Java Programmer","gender":"male","salary":28000 }
{ "index" : {  "_id" : "16" } }
{ "name" : "Mccarthy","age":21,"job":"Javascript Programmer","gender":"male","salary": 16000}
{ "index" : {  "_id" : "17" } }
{ "name" : "Goodwin","age":25,"job":"Javascript Programmer","gender":"male","salary": 16000}
{ "index" : {  "_id" : "18" } }
{ "name" : "Catherine","age":29,"job":"Javascript Programmer","gender":"female","salary": 20000}
{ "index" : {  "_id" : "19" } }
{ "name" : "Boone","age":30,"job":"DBA","gender":"male","salary": 30000}
{ "index" : {  "_id" : "20" } }
{ "name" : "Kathy","age":29,"job":"DBA","gender":"female","salary": 20000}



# Query
POST employees/_search
{
  "size": 0,
  "query": {
    "range": {
      "age": {
        "gte": 20
      }
    }
  },
  "aggs": {
    "jobs": {
      "terms": {
        "field":"job.keyword"
        
      }
    }
  }
}


#Filter
POST employees/_search
{
  "size": 0,
  "aggs": {
    "older_person": {
      "filter":{
        "range":{
          "age":{
            "from":35
          }
        }
      },
      "aggs":{
         "jobs":{
           "terms": {
        "field":"job.keyword"
      }
      }
    }},
    "all_jobs": {
      "terms": {
        "field":"job.keyword"
        
      }
    }
  }
}



#Post field. 一条语句，找出所有的job类型。还能找到聚合后符合条件的结果
POST employees/_search
{
  "aggs": {
    "jobs": {
      "terms": {
        "field": "job.keyword"
      }
    }
  },
  "post_filter": {
    "match": {
      "job.keyword": "Dev Manager"
    }
  }
}


#global
POST employees/_search
{
  "size": 0,
  "query": {
    "range": {
      "age": {
        "gte": 40
      }
    }
  },
  "aggs": {
    "jobs": {
      "terms": {
        "field":"job.keyword"
        
      }
    },
    
    "all":{
      "global":{},
      "aggs":{
        "salary_avg":{
          "avg":{
            "field":"salary"
          }
        }
      }
    }
  }
}


#排序 order
#count and key
POST employees/_search
{
  "size": 0,
  "query": {
    "range": {
      "age": {
        "gte": 20
      }
    }
  },
  "aggs": {
    "jobs": {
      "terms": {
        "field":"job.keyword",
        "order":[
          {"_count":"asc"},
          {"_key":"desc"}
          ]
        
      }
    }
  }
}


#排序 order
#count and key
POST employees/_search
{
  "size": 0,
  "aggs": {
    "jobs": {
      "terms": {
        "field":"job.keyword",
        "order":[  {
            "avg_salary":"desc"
          }]
        
        
      },
    "aggs": {
      "avg_salary": {
        "avg": {
          "field":"salary"
        }
      }
    }
    }
  }
}


#排序 order
#count and key
POST employees/_search
{
  "size": 0,
  "aggs": {
    "jobs": {
      "terms": {
        "field":"job.keyword",
        "order":[  {
            "stats_salary.min":"desc"
          }]
        
        
      },
    "aggs": {
      "stats_salary": {
        "stats": {
          "field":"salary"
        }
      }
    }
    }
  }
}
```

#### 18，文档的父子关系

#### 19，数据建模

```
1，数据需求
1-1，实体属性
字段类型、是否搜索及分词、是否聚合排序、是否额外存储
字段类型------------------------
Text适用于全文本字段、要被分词的，默认不支持分析及排序。需要设置fielddata为true。
keyword适用于id、枚举及不需要分词的文本，例如手机号码等，用于filter（精准匹配），sorting和聚合分析。
byte适用于数字类型，还有日期、地理位置，布尔。

是否搜索及分词-------------------
不需要检索、排序、聚合分析：将enable设置为false。
不需要检索：将index设置为false。
对于需要检索的字段，设定存储的粒度：index_options/Norms:

聚合排序------------------------
不需要检索、排序、聚合分析：将enable设置为false。
不需要排序、聚合：doc_values\fielddata设置为false。
更新频繁、聚合查询频繁的keyword类型字段将eager_global_ordinals设置为true。

是否额外存储---------------------
store设置为true，存储该字段原始信息。一般结合_source为false时候使用。

1-2，实体之间的关系
1-3，搜索相关配置
2，索引模板
分片数量
3，索引Mapping
字段配置
关系处理
4，index Template 及dynamic template
5，index alias
6，update by query 及reindex
7，如何处理关联关系。
denormalization、nested、child/parent
8，文档字段不能过多。默认是1000，一般我们要将dynamic设置为false\strict。
9，不要使用正则查询（例如将7.1.1分成3个字段）。
10，避免空值，导致聚合不准。定义类型的时候，设置null_value的默认值。
11，加入meta信息，进行版本管理。

```

#### 20，备份HDFS 

很慢

```
PUT _snapshot/backup
{
  "type": "hdfs",
  "settings": {
    "uri": "hdfs://192.168.130.33:9090/",
    "path":"/dev_elasticsearch/repositories/backup"
  }
}

PUT _snapshot/backup/users
{
  "indices": "users",
  "ignore_unavailable": true,
  "include_global_state": false
}

PUT _snapshot/backup/product
{
  "indices": "product",
  "ignore_unavailable": true,
  "include_global_state": false
}

GET _snapshot/backup/_all

GET _snapshot/backup/product

POST product/_search
{
  
}

DELETE product

POST _snapshot/backup/product/_restore
{
  "indices": "product",
  "ignore_unavailable": true,
  "include_global_state": false
}

POST product/_search
{
  
}

DELETE _snapshot/backup


```



参考：

<https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-params.html>

### IK分词器

<https://github.com/medcl/elasticsearch-analysis-ik>

### 性能优化

<https://blog.51cto.com/tchuairen/1861603>