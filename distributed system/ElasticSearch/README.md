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

