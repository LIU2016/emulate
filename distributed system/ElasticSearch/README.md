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

