# AI作业优化方案

## 总体方案

```properties
1，调整项目结构 - 化繁为简、防止破溃
2，调整问题场景
3，调整安装部署 
```

## 项目结构调整

### 背景

```
sass应用Ai作业一个微服务项目有8个子项目！！！需要对AIhomework项目重组。
他们分别是：
业务聚合层：tw-cloud-openapi-aihomework\tw-cloud-openapi-aiofflinehomework\tw-cloud-openapi-aihomeworkanalyze
业务数据层：tw-cloud-microservice-aihomework\tw-cloud-microservice-aihomeworkpublish\tw-cloud-microservice-aiofflinehomework\tw-cloud-microservice-file\tw-cloud-microservice-knowledge 。

1，维护难度大。
2，开发调试难度大，跨服务调试业务要开启多个项目。
3，业务之间本来就强关联的（作业与作业发布与作业的附件与知识点），项目之前还有相互的调度。
4，代码重复率高，同样的一份配置要配置5份或者8份。
5，对服务器资源浪费（重复依赖的jar包、开启的进程对内存、cpu的重复消耗）。
```

### 调整步骤

```
Ai作业项目重构后分5个项目（调整后部署2个项目：一个聚合的openapi、一个数据的microservice、一个处理定时任务的scheduled）：
1，业务契约层：tw-cloud-api-aihomework 
2，业务聚合层：tw-cloud-openapi-aihomework 
3，业务数据层：tw-cloud-microservice-aihomework 
4，平台数据调用层：tw-cloud-platform-aihomework
5，业务定时任务工程：tw-cloud-scheduled-aihomework

具体步骤：
0，新建tw-cloud-parent-aihomework项目，先后提交tw-cloud-api-aihomework、tw-cloud-openapi-aihomework、tw-cloud-microservice-aihomework、tw-cloud-platform-aihomework、tw-cloud-scheduled-aihomework等modules。
1，将所有的数据层的接口（即微服务中api目录下的文件）迁移到tw-cloud-api-aihomework这个module。
2，合并tw-cloud-microservice-aihomeworkpublish\tw-cloud-microservice-aiofflinehomework\tw-cloud-microservice-file\tw-cloud-microservice-knowledge项目的代码到tw-cloud-microservice-aihomework这个module。
3，合并tw-cloud-openapi-aiofflinehomework\tw-cloud-openapi-aihomeworkanalyze项目的代码到tw-cloud-openapi-aihomework这个module。
4，ECO交互的数据拉通代码、UC、BASE代码调用统一抽到tw-cloud-platform-aihomework项目 。
5，新建tw-cloud-scheduled-aihomework这个module，用于做统计、定时任务等作用 。
6，添加devtools工具提高开发效率 。
7，修改前端调用的服务名称。
```

## 问题场景

### 背景

```
有很多问题场景需要重新调整，以便达到SE的性能要求。
```

### 设计方案

```
涉及到改动的接口有：

/paperTask/getPublishList

/homework/searchteachertasklist

/homework/searchstudenttasklist

/paper/getPaperQuestionList

/paper/getQuestionInformation

/answer/submitPaper

/knowledgeAnalyze/getRecentlyKnowledgeList

/Supplementary/getKnowledgePointList

/Supplementary/getCatalogList(这里获取教材的章节会根据章节id反复调用接口，前端调用要重新处理 ，页面：推荐-自学-获取章节列表)
```

#### /paperTask/getPublishList

```
目前存在的问题：
1，t_con_publish_class表和t_e_paper_publish强关联的，还分开查。然后二个查询还分别关联了同一套表结构各自来了一发。
2，这里有统计数据的填充。

解决办法：
1，合并t_con_publish_class表和t_e_paper_publish两个表的查询
2，发布记录表添加冗余数据信息（总人数、已提交人数、学生得分、学生状态等等），实时统计到发布表即可。

```

#### /homework/searchteachertasklist

