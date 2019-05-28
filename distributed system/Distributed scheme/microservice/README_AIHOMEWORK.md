# AI作业C03SP02 设计文档

[TOC]

## 总体方案

```properties
1，代码结构调整 - 化繁为简、防止破溃
2，项目框架调整
3，性能（覆盖【调整详情中的12个场景】）、容错、安全
4，项目安装部署调整
```

## 一、代码结构调整

### 背景

```
sass应用Ai作业微服务项目有8个子项目,需要对AIhomework项目重组。
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
Ai作业项目重构后分5层项目：

1，业务契约层：api-aihomework

2，业务聚合层：openapi-selfstudy\openapi-errorquestion\openapi-homework\openapi-analysis

3，业务数据层（线上作业、线下作业、试题、错题本、知识点）：microservice-onlinehomework \ microservice-offlinehomework \ microservice-question \ microservice-knowledge \ microservice-mistakescollection

4，平台数据调用层：platform-aihomework 

5，业务定时任务工程：scheduled-aihomework 

具体步骤：
0，新建parent-aihomework项目，先后提交api-aihomework\openapi-selfstudy\openapi-errorquestion\openapi-homework\openapi-analysis\microservice-onlinehomework \ microservice-offlinehomework\platform-aihomework\scheduled-aihomework等modules。

1，将所有的数据层的接口（即微服务中api目录下的文件）迁移到tw-cloud-api-aihomework这个module。

2，迁移tw-cloud-microservice-aihomeworkpublish\tw-cloud-microservice-aiofflinehomework\tw-cloud-microservice-file\tw-cloud-microservice-knowledge项目的代码到microservice-onlinehomework \ microservice-offlinehomework \ microservice-question \ microservice-knowledge \ microservice-mistakescollection这5个module。

3，合并tw-cloud-openapi-aiofflinehomework\tw-cloud-openapi-aihomeworkanalyze项目的代码到openapi-selfstudy\openapi-errorquestion\openapi-homework\openapi-analysis这4个module。

4，ECO交互的数据拉通代码、UC、BASE代码调用统一抽到platform-aihomework项目 。

5，新建scheduled-aihomework这个module，用于做统计、定时任务等作用，集成ECO的lts工具。 

6，添加devtools工具提高开发效率 。

7，修改前端调用的服务名称。
```

## 二、项目框架调整

### 背景

```
有很多问题场景需要重新调整，以便达到SE的主表数据100w情况下满足1000~2000并发的性能要求。
```

### 调整总览

```properties
1，减少网络交互的次数。
	a，【发布、试卷、试题、知识点、文件】等能关联查询的就尽量关联查询。不要什么情况都是带着一堆ID为参数，发送个http请求到微服务去查询。

2，减少网络响应的大小，请求尽量多带条件和分页。
	a，访问第三方服务尽量多带参数，例如访问ECO的获取常量接口。

3，构建应用缓存和使用redis缓存
	a，将用户、班级、学校、常量等脚本信息存储到Ehcache应用缓存中去，减少与eco的网络交互。Ehcahe采用LRU的最近最少未使用的缓存回收策略。基本信息的更新通过ECO的消息进行更新。
	b，将前端对ECO的基础信息的获取调整到从ai作业获取，减少服务器和前端的重复请求。
	c，将试题、试卷、知识点等详情信息存储到redis远程缓存。

4，新建统计表（粗略设计）：
	a，发布记录表统计表（发布id、班级id、总人数、已提交人数、未批改、已批改、发回、平均正确率，创建时间、修改时间），以发布id和班级id为主键
	b，试题的统计表（字段有：试题ID，试卷发布ID，班级ID，正确人数、错误人数，创建时间、修改时间）以试题id为主键
	c，学生的作答统计表，字段：（发布id，班级ID，学生id，总题数，正确题数，总得分，创建时间、修改时间）,以发布id，班级ID，学生id为主键
	d，知识点掌握情况统计表，字段：（班级ID，学生id，知识点的掌握情况，创建时间、修改时间）,以学生id为主键
	
5，检查所有的附件请求，除了一定要用原图展示的地方外，其他的请带宽高，不能用原图（fs文件请求目前支持带宽高的压缩）
	a，合并图片请求（已咨询过ECO,fs不支持,建议ECO添加这个功能）

6，检查所有的没有数据的页面展示的情况和文字表达需要调整的情况，前端要对页面进行调整。不然太丑了，请参考【12，学生端--学习分析】点。

7，将数据拉通的代码、与eco交互的代码提取到tw-cloud-platform-aihomework工程，做异步、熔断处理。

8，整理下统计的需求、提升练习这种算法合理吗？统计是否要合入线下作业的学生作答情况。
```

### 调整详细

优化的模块：首页、学生作答、老师发布

#### 1，老师端--首页

进入首页会请求如下连接：

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\首页.png)

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\学生端首页.bmp)

##### 问题

###### /openapi-base/base/getTeachClassSubjectList 

作用：通过用户id去获取任教班级和科目

请求次数：2次（option、post）

请求参数

```javascript
{"id":"TWPAAS1200001438010","orgId":"CNHNNX0600000000099","tenantId":"E000003","access_token":"01683d19af2970c909ef2763d0b88568"}
```

响应参数

```javascript
{
    "serverResult": {
        "resultCode": "200",
        "resultMessage": "操作成功"
    },
    "pageInfo": {
        "startRow": 1,
        "lastPage": 1,
        "navigatepageNums": [
            1
        ],
        "prePage": 0,
        "hasNextPage": false,
        "nextPage": 0,
        "pageSize": 200,
        "endRow": 4,
        "list": [
            {
                "teachId": "E000003S600000002074_100000000001_TWPAAS1200001438010",
                "classId": "E000003S600000002074",
                "createTime": "2019-03-04 15:47:30",
                "userId": "TWPAAS1200001438010",
                "subjectId": "100000000001",
                "classType": "2"
            },
        .....
        ],
        ....
    }
}
```

###### /openapi-base/base/queryDictItemList

作用：获取用户所在机构的所有常量字段

请求次数：2次（POST，OPTIONS）

请求参数：

```javascript
{"id":"TWPAAS1200001438010","orgId":"CNHNNX0600000000099","tenantId":"E000003","access_token":"01683d19af2970c909ef2763d0b88568","dictTypeId":"SUBJECT"}
```

请求响应：

```javascript
{
    "serverResult": {
        "resultCode": "200",
        "resultMessage": "操作成功"
    },
    "pageInfo": {
        "startRow": 1,
        "lastPage": 1,
        "navigatepageNums": [
            1
        ],
        "prePage": 0,
        "hasNextPage": false,
        "nextPage": 0,
        "pageSize": 200,
        "endRow": 70,
        "list": [
            {
                "dictValue": "100000000002",
                "sortNo": 1,
                "parentDictId": "100000000060",
                "isEditable": "0",
                "dictTypeId": "SUBJECT",
                "lastModifyTime": "2013-10-17 17:07:37",
                "dictName": "数学",
                "remark": "数学",
                "dictId": "100000000502",
                "lang": "zh_CN",
                "status": "1"
            }
            ....
        ],
       ....
    }
}
```

###### /openapi-base/base/joinSearchClasses

作用：获取班级详情

请求次数：4次（教学班、行政班信息）

请求参数：

```javascript
{"id":"TWPAAS1200001438010","orgId":"CNHNNX0600000000099","tenantId":"E000003","access_token":"01683d19af2970c909ef2763d0b88568","dictTypeId":"SUBJECT","classId":"E000003S600000002074","classType":"2"}
```

请求响应

```javascript
{
    "serverResult": {
        "resultCode": "200",
        "resultMessage": "操作成功"
    },
    "pageInfo": {
        "startRow": 1,
        "lastPage": 1,
        "navigatepageNums": [
            1
        ],
        "prePage": 0,
        "hasNextPage": false,
        "nextPage": 0,
        "pageSize": 200,
        "endRow": 4,
        "list": [
            {
                "teachId": "E000003S600000002074_100000000001_TWPAAS1200001438010",
                "classId": "E000003S600000002074",
                "createTime": "2019-03-04 15:47:30",
                "userId": "TWPAAS1200001438010",
                "subjectId": "100000000001",
                "classType": "2"
            },
          ..........
        ],
       .......
    }
}
```

###### /openapi-base/base/queryDictItemList

作用：获取常量数据

请求次数：4次

请求参数：

```javascript
{"id":"TWPAAS1200001438010","orgId":"CNHNNX0600000000099","tenantId":"E000003","access_token":"01683d19af2970c909ef2763d0b88568","dictTypeId":"SCHOOL_SECTION","classId":"E000003S600000002075","classType":"1","schoolSection":"PRIMARY_SCHOOL"}
```

请求响应：

```javascript
{
    "serverResult": {
        "resultCode": "200",
        "resultMessage": "操作成功"
    },
    "pageInfo": {
        "startRow": 1,
        "lastPage": 1,
        "navigatepageNums": [
            1
        ],
        "prePage": 0,
        "hasNextPage": false,
        "nextPage": 0,
        "pageSize": 200,
        "endRow": 6,
        "list": [
            {
                "dictValue": "1",
                "sortNo": 1,
                "parentDictId": "100000000060",
                "isEditable": "0",
                "dictTypeId": "SCHOOL_SECTION",
                "lastModifyTime": "2013-08-23 09:34:19",
                "dictName": "一年级",
                "remark": "小学一年级",
                "dictId": "100000000061",
                "lang": "zh_CN",
                "status": "1"
            },
          .....
        ],
       ....
    }
}
```

###### /openapi-aihomework/paperTask/getPublishList

作用：获取线上作业发布记录

请求次数：2次

请求参数：

```javascript
{"access_token":"e43e55366bd565f934beeaa606abcdf7","numPerPage":"10","pageNo":"0","type":"up","userId":"TWPAAS1200001438010","publishType":"0","status":"0","showload":true}
```

响应时间：

```
{
    "responseEntity": null,
    "pageInfo": {
        "pageNum": 1,
        "pageSize": 10,
        "size": 4,
        "startRow": 1,
        "endRow": 4,
        "total": 4,
        "pages": 1,
        "list": [
            {
                "creatorId": "TWPAAS1200001438010",
                "taskId": "248028",
                "taskBatch": "248028",
                "taskSubject": "语文",
                "taskType": "3",
                "createTime": "2019-03-05 11:40:19",
                "startTime": "2019-03-05 11:38:00",
                "endTime": "2019-03-08 11:38:00",
                "endStatus": "0",
                "teacherAnswerId": null,
                "classId": "E000003S600000002075",
                "className": "一年级001班",
                "doneStudentNum": 1,
                "totalStudentNum": 3,
                "smsFlag": "0",
                "status": "1"
            }
            .....
        ],
        .....
}
```

###### /openapi-aiofflinehomework/homework/searchteachertasklist

作用：获取线下作业发布记录

请求次数：2次

请求参数：

```javascript
{"pageNo":1,"numPerPage":"10","userId":"TWPAAS1200001438010","orgId":"CNHNNX0600000000099","role":"teacher","type":"up","showload":true}
```

响应时间：

```javascript
{
    "responseEntity": null,
    "pageInfo": {
        "pageNum": 1,
        "pageSize": 10,
        "size": 4,
        "startRow": 1,
        "endRow": 4,
        "total": 4,
        "pages": 1,
        "list": [
            {
                "creatorId": "TWPAAS1200001438010",
                "taskId": "248028",
                "taskBatch": "248028",
                "taskSubject": "语文",
                "taskType": "3",
                "createTime": "2019-03-05 11:40:19",
                "startTime": "2019-03-05 11:38:00",
                "endTime": "2019-03-08 11:38:00",
                "endStatus": "0",
                "teacherAnswerId": null,
                "classId": "E000003S600000002075",
                "className": "一年级001班",
                "doneStudentNum": 1,
                "totalStudentNum": 3,
                "smsFlag": "0",
                "status": "1"
            },
           .....
}
```

###### /openapi-aihomework/paperTask/getAnswerResultList

作用：获取线上学生作答信息

请求次数：2次

请求参数：

```javascript
{"classId":"E000003S600000002074","publishId":"E000003S600000025692"}
```

请求响应：

```javascript
{
    "responseEntity": null,
    "pageInfo": {
        "pageNum": 0,
        "pageSize": 0,
        "size": 0,
        "startRow": 0,
        "endRow": 0,
        "total": 3,
        "pages": 0,
        "list": [
            {
                "extInfo": null,
                "answerTime": "31",
                "status": 4,
                "totalScore": "0",
                "submitTime": "2019-03-05 11:48:51",
                "studentName": "nxxue01",
                "userFacePath": null,
                "studentId": "TWPAAS1200001438012",
                "rank": 1,
                "score": "6.0",
                "sex": null,
                "ratio": 50,
                "studentCode": "nxxue01",
                "className": "一年级001班"
            },
          .....
}
```

###### /openapi-aihomework/paperTask/getQuestionResultList

作用：获取作业学生作答信息

请求次数：2次

请求参数：

```javascript
{"classId":"E000003S600000002074","publishId":"E000003S600000025692"}
```

请求响应：

```javascript
{
    "responseEntity": null,
    "pageInfo": {
        "pageNum": 0,
        "pageSize": 0,
        "size": 0,
        "startRow": 0,
        "endRow": 0,
        "total": 4,
        "pages": 0,
        "list": [
            {
                "questionId": "CNBJTW0200002035927",
                "childId": "",
                "totalNum": 3,
                "correctNum": 1,
                "incorrectNum": 0,
                "unApproved": 0,
                "undoNum": 2,
                "orderNo": "1"
            },
          .....
}
```

###### /openapi-aihomework/paperTask/getScoresDistribution

作用：获取得分分布

请求次数：2次

请求参数：

```javascript
{"classId":"E000003S600000002074","publishId":"E000003S600000025692"}
```

请求响应：

```javascript
{
    "responseEntity": {
        "extInfo": null,
        "averageScore": "6.0",
        "highestScore": "6.0",
        "lowestScore": "6.0",
        "totalNum": 1,
        "excellentNum": 0,
        "goodNum": 0,
        "fairNum": 1,
        "poorNum": 0,
        "totalScore": "9.0",
        "scoreDistributionList": [
            {
                "number": 0,
                "section": "8.1-9.0",
                "level": "1"
            },
      ....
}
```

```properties
1，一个首页共请求了22次，请求次数过多
2，/openapi-base/base/queryDictItemList 单个请求的数量量过大
3，大量的重复获取数据，
例如：/openapi-aihomework/paperTask/getPublishList获取发布列表的响应结果中本来就有了科目、班级、学生等基础信息。
4，/openapi-aihomework/paperTask/getPublishList接口的问题：
	a，t_con_publish_class表和t_e_paper_publish强关联的，还分开查。然后二个查询还分别关联了同一套表结构各自来了一发。
	b，这里有统计数据的填充。
```

##### 调整

```properties
1，去掉所有的请求连接，只保留/openapi-aihomework/paperTask/getPublishList接口请求。
这个接口要求：
	a,合并线下线上发布作业查询（即/openapi-aiofflinehomework/homework/searchteachertasklist去掉）
	b,合并学生作答的信息以及得分分布信息

2,使用应用Ehcache缓存
	a,由于Ai作业服务器也要用到班级、机构、常量、科目等信息，这样就造成了前后端重复去取基础数据。因此，前端所有的pass的base请求连接都从ai作业服务器去获取，而ai作业服务器从ECO上获取这些基础信息后保存到应用Ehcache缓存。
	b,当eco基础消息变化了，需要eco发送消息给ai作业去更新应用缓存。
	c,获取常量信息（/openapi-base/base/queryDictItemList)等，要在ai作业应用启动时做缓存预热到应用缓存。

3,/openapi-aihomework/paperTask/getPublishList接口重构要注意：
	a,合并t_con_publish_class表和t_e_paper_publish两个表的查询
	b,添加发布记录表统计表（发布id、班级id、总人数、已提交人数、未批改、已批改、发回、平均正确率等等），实时统计到发布表即可。这里要注意总人数会随着班级人数信息变化（ECO信息同步）进行实时修改。
```

#### 2，老师端--线上作业已作答/已结束作答统计/发回页面

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\试卷详情页面.png)

##### 问题

```properties
如上面分析的情况一样，获取作答详情的三个连接，请求次数6次：
/openapi-aihomework/paperTask/getAnswerResultList
/openapi-aihomework/paperTask/getQuestionResultList
/openapi-aihomework/paperTask/getScoresDistribution
/openapi-aihomework/answer/sendBack
```

```properties
1,前端请求没做分页啊。
2,三个请求的参数都是classID和publishID。
/openapi-aihomework/paperTask/getQuestionResultList：业务逻辑坑爹啊。
/openapi-aihomework/paperTask/getAnswerResultList：上个接口的业务逻辑又来一遍啊（例如：根据班级id查学生列表，通过发布ID获取试卷ID）。
/openapi-aihomework/paperTask/getScoresDistribution：好吧，又来了一遍（例如：班级学生列表，发布记录，学生作答）
接口逻辑的重复，造成整个链路的响应时间加长，不可取。
3，/openapi-aihomework/answer/sendBack接口，有CCE\ECP数据拉通代码，并且未做容错和异步处理。
```

##### 调整

```properties
1，前端一定要分页获取，因为当这里的班级的学生增多时，一把全部拿下来，对服务器和网络都是有压力的。
2，一次请求可以完成的事情没必要分多次请求。因为是相同，三个请求的接口业务逻辑大部分都是重合的。
3，/openapi-aihomework/paperTask/getAnswerResultList接口中会统计试题的（正确人数、错误人数、未批改人数、未提交人数）等字段，见下面的代码。
	a,新建试题的统计表（字段有：试题ID，试卷发布ID，班级ID，正确人数、错误人数），
	b,如上已经添加了发布记录统计表（未批改人数、未提交人数（总人数-已提交人数））
	c,班级详情、试卷详情存到缓存中，去掉接口中的通过试卷id获取试卷详情的查询。
4，/openapi-aihomework/paperTask/getQuestionResultList
    a,合并到getAnswerResultList接口
    b,构建学生的作答统计表，字段：（publishid,answeruserid,总得分,正确率）来计算学生的正确的题数,正确率。实时统计每个发布记录的每个学生的作答情况。 ？？
5，/openapi-aihomework/paperTask/getScoresDistribution  
	a,合并到getAnswerResultList接口
6，/openapi-aihomework/answer/sendBack接口的数据拉通代码迁移到平台数据调用层：tw-cloud-platform-aihomework，做容错和异步处理。	
```

/openapi-aihomework/paperTask/getQuestionResultList

```java
@SystemServiceLog(description = "获取作答统计列表")
    public Response<QuestionResult> getQuestionResultList(PublishBaseReq req) {
        ValidatorUtil.parameterValidate(req);

        // 1. 通过试卷结果服务获取试卷按题统计结果
        GetQuestionResultStatisListReq getQuestionResultStaticListReq = new GetQuestionResultStatisListReq();
        getQuestionResultStaticListReq.setClassId(req.getClassId());
        getQuestionResultStaticListReq.setPublishId(req.getPublishId());

        Response<QuestionResultStatisInfo> questionResultRsp = paperResultMicroApi
                .getQuestionResultStatisList(getQuestionResultStaticListReq);
        if (!ValidatorUtil.validateResponse(questionResultRsp)) {
            return new Response<>(IStateCode.SYSTEM_ERORR, "获取试题作答统计列表失败！",
                    ResponseUtils.getInternalErrorMsg(questionResultRsp));
        }

        List<QuestionResultStatisInfo> listStatus = ResponseUtils.isPageListEmpty(questionResultRsp.getPageInfo())
                ? new ArrayList<>() : questionResultRsp.getPageInfo().getList();

        // 2. 通过发布ID获取试卷ID，获取试卷详情
        String paperId = MicroApiHelper.getPaperIdByPublishId(publishInfoMicroApi, req.getPublishId());
        Response<PaperQuestionInfo> paperQuestionRsp = MicroApiHelper.getPaperQuestionList(paper2QuestionMicroApi,
                paperId);
        if (!ValidatorUtil.validateResponsePage(paperQuestionRsp)) {
            return new Response<>(IStateCode.SYSTEM_ERORR, "获取试卷试题列表失败！",
                    ResponseUtils.getInternalErrorMsg(paperQuestionRsp));
        }
        List<PaperQuestionInfo> listPaperQuestion = paperQuestionRsp.getPageInfo().getList();

        // 3. 获取班级学生列表
        Response<Student> studentRsp = MicroApiHelper.getClassStudents(studentMicroApi, req.getClassId());
        if (!ValidatorUtil.validateResponsePage(studentRsp)) {
            return new Response<>(IStateCode.SYSTEM_ERORR, "获取班级学生列表失败！",
                    ResponseUtils.getInternalErrorMsg(studentRsp));
        }

        // 得到班级学生总数
        int iTotalNum = studentRsp.getPageInfo().getList().size();

        serverLogger.debug("getQuestionResultList	遍历试卷试题，结合作答结果组装数据");
        // 4. 遍历试卷试题，结合作答结果组装数据
        List<QuestionResult> listResult = getQuestionResultStatics(listPaperQuestion, listStatus, iTotalNum);

        serverLogger.debug("getQuestionResultList	response");
        return new Response<>(listResult);
    }

```

#### 3，老师端--线下作业/线上作业/智能测验发布页面

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\作业发布页面.png)

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\作业发布页面-选择教辅.png)

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\作业发布-配套试卷-试题选择.png)

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\作业预览.png)

##### 问题

```properties
线上作业/智能测验 选择教辅页面
/openapi-aihomework/Supplementary/getThemeList 获取教辅
/openapi-aihomework/Supplementary/getCatalogList 根据教辅的每个章节id去获取章节信息

线上作业/智能测验 配套试卷-选择试题
/openapi-aihomework/Supplementary/getPaperList 获取试卷列表
/openapi-aihomework/Supplementary/getKnowledgePointList 根据章节获取知识点列表
/openapi-aihomework/paper/getPaperQuestionList 根据试卷id获取试卷的试题列表
/openapi-aihomework/paper/getQuestionInformation 根据试题列表查询试题详情列表 

线上作业/智能测验 同步试题-选择试题
/openapi-aihomework/Supplementary/getQuestionList 获取知识点下的试题列表
/openapi-aihomework/paper/getQuestionInformation 获取试题详情列表

线上作业/智能测验 作业预览
/openapi-aihomework/paper/getQuestionInformation 作业预览

线上作业/智能测验 发布作业-作业预览-点击“确认”
/openapi-aihomework/paper/addPaper

线上作业/智能测验 发布作业-点击“发布”
/openapi-aihomework/paperTask/publishTask
```

```properties
1，线上作业/智能测验 发布作业-选择教辅
	a，没有分页
	b，/openapi-aihomework/Supplementary/getCatalogList 肯定不能单个章节就去请求一次。
	
2，线上作业/智能测验 发布作业-选择试题-配套试卷
	a，没有分页
	b，/openapi-aihomework/paper/getPaperQuestionList接口明显多余。
	c，这个页面没有用到知识点
	
3，线上作业/智能测验 发布作业-选择试题-同步试题
	a，获取知识点下的试题列表和获取试题详情列表可以合并为一个接口，没必要分开查。
	
4，线上作业/智能测验 发布作业-作业预览
	a，请求参数有问题，一把试题id的list查的

5，线上作业/智能测验 发布作业-作业预览-点击“确认”
	a，请求参数的试题列表将试题的详情信息都放在请求次数集合里，若试题较多，整个请求参数的数据包就比较大。

6，线上作业/智能测验 发布作业-点击“发布”
	/openapi-aihomework/paperTask/publishTask
	a，有与eco数据拉通的代码
```

##### 调整

```properties
1，发布作业-选择教辅
	a，分页获取教辅（/openapi-aihomework/Supplementary/getThemeList）
	b，通过教辅id获取章节详情列表（/openapi-aihomework/Supplementary/getCatalogList）
	
2，发布作业-配套试卷-选择试题
	a，去掉/openapi-aihomework/paper/getPaperQuestionList的调用。直接用试卷id去调用/openapi-aihomework/paper/getQuestionInformation分页获取试题列表
	b，/openapi-aihomework/Supplementary/getPaperList加分页
	c，/openapi-aihomework/Supplementary/getKnowledgePointList接口要放到【发布作业-选择试题-同步试题】去触发。
	d，知识点详情可以添加到redis缓存中去。
	
3，发布作业-选择试题-同步试题
	a，通过知识点列表查询试题详情列表，修改/openapi-aihomework/paper/getQuestionInformation接口添加知识点筛选参数。

4，发布作业-作业预览
    a，麻烦将/openapi-aihomework/paper/getQuestionInformation接口的请求参数的试题列表的集合的试题个数控制在每次10个范围内

5，发布作业-作业预览-点击“确认”
	a，将/openapi-aihomework/paper/addPaper请求参数的试题详情列表修改为试题列表。服务器根据试题列表去redis缓存中批量获取整个试题详情列表做业务逻辑操作。
	b，将/openapi-aihomework/paper/addPaper保存的数卷详情保存到redis缓存服务器

6，发布作业-点击“发布”
	a，/openapi-aihomework/paperTask/publishTask的数据拉通代码迁移到平台数据调用层：tw-cloud-platform-aihomework，做容错和异步处理。	
	b，/openapi-aihomework/paperTask/publishTask在取试卷的详情的时候，通过redis缓存服务器取（上面保存的时候已经存到redis缓存中了）
```

#### 4，老师端--推荐

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\老师端-推荐.png)

##### 问题

```properties
/openapi-aihomework/Supplementary/getThemeList 获取教辅列表
/openapi-aihomework/Supplementary/getCatalogList 获取章节详情

大量的图片请求。
```

```properties
如上 3，老师端--线下作业/线上作业/智能测验发布页面，有做过分析，处理办法参考上面。
除了接口请求外，发现大量的附件请求。若网络较差，这里需要优化。
```

##### 调整

```properties
1，参考【3，老师端--线下作业/线上作业/智能测验发布页面】调整接口
2，附件请求请带宽高，不能用原图（fs文件请求目前支持带宽高的压缩）
例如：
http://192.168.102.204:9000/fs/media/CNBJTW0/content/2018/4/23/png/0189d35d-4a66-4370-9b11-af67dea88bad.png?height=100&width=100
3，合并图片请求（已咨询过ECO,fs不支持,建议ECO添加这个功能）
```

#### 5，老师端--学习分析

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\分析.png)

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\分析-自学.png)

##### 问题

###### /openapi-aihomeworkanalyze/publishAnalyze/getPaperAnalysisList

作用：获取用户作业、测验学习分析正确率-分析指定时间段内老师在指定班级发布的作业测验统计情况

请求次数：2次（option、post）

请求参数：

```javascript
{"classId":"CJTWBS1S600000015813","subjectId":"100000000002","startTime":"2019-03-03 19:30:53","endTime":"2019-04-02 19:30:53","papaerType":"0"}
```

响应：

```javascript
{
"responseEntity": {
"paperAnalysisList": [
{
"paperType": "2",
"count": "0",
"rate": "0.0",
"sendBackCount": "0",
"submitTime": "0",
"averageCorrectRatio": "0"
}
.....
}
```

###### /openapi-aihomeworkanalyze/userLearnAnalyze/getBookPracticeList

作用：获取自学教辅统计列表 - 根据查询条件，获取学生的自学使用过的教辅列表信息，里面带了学生的学习情况 老师端

请求次数：2次

请求参数：

```properties
{"classId":"CJTWBS1S600000015813","subjectId":"100000000002","startTime":"2019-03-03 19:30:53","endTime":"2019-04-02 19:30:53"}
```

响应：

```
{
"responseEntity": {
"bookInfoList": [
{
"coverPath": "CNBJTW0/content/2015/8/26/jpg/344f35da-a62d-4e6a-90b6-205d3936efd1.jpg",
"yaer": "",
"practicePersonTime": "0",
"bookId": "CNBJTW006025109200000694708",
"origin": "",
"bookName": "人教版小学数学《同步学练测》四年级上册_天闻数媒",
"practicePersonTotal": "0",
"gradeId": "4",
"termId": "1",
"subjectId": "100000000002",
"bookType": "2"
}
......
}
```

###### 分析-知识点

```properties
/openapi-aihomeworkanalyze/knowledgeAnalyze/getKnowledgeAnalyzeOutcomes 知识点总体统计
/openapi-aihomeworkanalyze/knowledgeAnalyze/getKnowledgeAnalyzeStudentRank 知识点统计学生排名
/openapi-aihomeworkanalyze/knowledgeAnalyze/getKnowledgeAnalyzeList 知识点统计列表
```

```properties
1，/openapi-aihomeworkanalyze/publishAnalyze/getPaperAnalysisList 会查询试卷的发布信息、查询学生的作答信息、查询学生作答结果表等。
	a，发布记录表为了查询主任务id多关联了2个表（主任务表和子任务表） 
	b，作答信息和学生作答结果 多遍历了作答状态表，关键是sql没有用到索引。当作答数据大了后就会很慢。
2，/openapi-aihomeworkanalyze/userLearnAnalyze/getBookPracticeList 这是个相当啰嗦的接口，集中反映了微服务的乱用。
	a，先查询专题 -> 根据专题查关联的资源 -> 根据资源获取其中是书本的资源 -> 根据书本查封面文件的关联关系 -> 根据文件的关联关系查文件  -> 【组装教材列表】 -> 根据教材查询所有每个教材的章节 ->【组装章节到教材列表】 -> 查询章节下所有的知识点 -> 【组装知识点】 -> 获取所有知识点关联的试卷 -> 根据试卷获取发布记录 -> 查询知识点下的所有试题 -> 所有试题的学生作答 -> 【统计练题次数】 一个发了11次http请求。
3，openapi-aihomeworkanalyze/knowledgeAnalyze/getKnowledgeAnalyzeOutcomes 知识点总体统计
、/openapi-aihomeworkanalyze/knowledgeAnalyze/getKnowledgeAnalyzeStudentRank 知识点统计学生排名、/openapi-aihomeworkanalyze/knowledgeAnalyze/getKnowledgeAnalyzeList 知识点统计列表 这三个接口的代码居然惊人的相似，大段逻辑都是一样，只有最后的分析有些不同。
```

##### 调整

```properties
1，对/openapi-aihomeworkanalyze/publishAnalyze/getPaperAnalysisList接口，我们给发布记录表添加冗余字段（主任务id），其次统计信息可以在作答发布统计表（该表是新增的）中获取。
2，/openapi-aihomeworkanalyze/userLearnAnalyze/getBookPracticeList 
	a，这个接口重写。
	b，在点击【分析-自学】的时候调用这个接口。
	c，删除知识点相关的多余逻辑
3，针对第三点
	a，设计知识点的统计表（字段：）
	b，将分析的统计设计为非实时的，这个失效性不高
```

#### 6，学生端--首页

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\学生端-首页.png)



##### 问题

```properties
/openapi-uc/uc/getUserByToken/16751a47cb2afd7be8a11dc26c946f2b 通过token获取用户信息
/openapi-base/base/queryStudents 
/openapi-base/base/classQuerySubject
/openapi-base/base/queryDictItemList
/openapi-base/base/joinSearchClasses
/openapi-base/base/queryTermList
/openapi-aihomework/paperTask/getPublishList
/openapi-aiofflinehomework/homework/searchstudenttasklist 学生线下作业发布列表

总共发送了http请求23次
```

```properties
1，以下接口获取的信息是有重复的。
/openapi-uc/uc/getUserByToken/16751a47cb2afd7be8a11dc26c946f2b 
/openapi-base/base/queryStudents 

2，以下接口分析同【1，老师端--首页】分析
/openapi-base/base/classQuerySubject
/openapi-base/base/queryDictItemList
/openapi-base/base/joinSearchClasses
/openapi-base/base/queryTermList

3，以下接口分析同【1，老师端--首页】分析
/openapi-aihomework/paperTask/getPublishList
/openapi-aiofflinehomework/homework/searchstudenttasklist
```

##### 调整

```properties
1，
/openapi-base/base/queryStudents 的学生信息获取放到服务器端应用缓存里头去，把前端页面需要的信息组装好。这样就不必要每次查发送多个http请求去获取信息了。

2，其他2点同【1，老师端--首页】解决方案
```

#### 7，学生端--线上作业/智能测验作答结果

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\学生端-作答.png)

##### 问题

```properties
/openapi-aihomework/paper/getPaperQuestionList 根据试卷id查试题id

/openapi-aihomework/paper/getQuestionInformation 根据试题id列表获取试题详情列表

/openapi-aihomeworkanalyze/paperQuestionAnalyze/getPaperStatisInfo 获取试卷批改结果统计接口 - 作业、测试完成后，查看我的作答信息和班级作答统计信息 学生端

/openapi-aihomework/paperTask/getPublishKnowledgeInfo 根据发布记录获取知识点

/openapi-aihomework/answer/getStudentQuestionAnswer 获取学生作答信息
```

```properties
1，/openapi-aihomework/answer/getStudentQuestionAnswer 获取学生作答信息（每道题请求一次，麻蛋，是不是100道题要请求100次）

2，/openapi-aihomework/paperTask/getPublishKnowledgeInfo 为了查询知识点，通过发布id获取试卷id，再由试卷id获取试题id，再由试题id获取知识点集合，再根据知识点的掌握情况返回信息。逻辑有点多余。

3，这两个接口的情况可以参考【3，老师端--线下作业/线上作业/智能测验发布页面】
/openapi-aihomework/paper/getPaperQuestionList 根据试卷id查试题id
/openapi-aihomework/paper/getQuestionInformation 根据试题id列表获取试题详情列表

4，openapi-aihomeworkanalyze/paperQuestionAnalyze/getPaperStatisInfo 这个接口 代码重构！！！（传了试卷id，还通过发布id去查试卷id，获取作答状态和作答结果分2次查，要去获取了一把学生信息）
```

##### 调整

```properties
1，/openapi-aihomework/answer/getStudentQuestionAnswer 要分页。

2，/openapi-aihomework/paperTask/getPublishKnowledgeInfo 
	a，可以直接传试卷id，不用传发布id。
	b，不用在【作答详情】页面去加载，麻烦放到作答统计去加载。
	
3，参考【3，老师端--线下作业/线上作业/智能测验发布页面】，通过试卷id调用/openapi-aihomework/paper/getQuestionInformation分页获取试题。

4，openapi-aihomeworkanalyze/paperQuestionAnalyze/getPaperStatisInfo 这个接口 代码重构
	a，用学生id、试卷id去缓存中取学生信息，试题列表
	b，作答状态查询和作答结果合并做一次查询
```

#### 8，学生端--线上作业作答页面

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\学生端-正在作答.png)

##### 问题

```properties
1，/openapi-aihomework/paper/getPaperQuestionList、/openapi-aihomework/paper/getQuestionInformation 问题同【7，学生端--线上作业/智能测验作答结果】

2，/openapi-aihomework/answer/submitPaper 不用传试题详情列表
```

##### 调整

```properties
1，参考【7，学生端--线上作业/智能测验作答结果】获取试卷方案
/openapi-aihomework/paper/getPaperQuestionList、/openapi-aihomework/paper/getQuestionInformation

2，/openapi-aihomework/answer/submitPaper 提交接口
	a，将请求参数中的试题详情列表改成试题id列表
	b，此处代码必须重构，太乱了。粗略的计算了下，有20多个http请求。

```

#### 9，学生端--线下作业作答结果

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\学生端-线下作业作答.png)

##### 问题

```properties
/openapi-aiofflinehomework/homework/searchtaskdetail
```

```properties
/openapi-aiofflinehomework/homework/searchtaskdetail 线下作业的查询http请求太多了、查询班级、查询老师这2个http就是获取了一个班级名称和老师名称。
```

##### 调整

```properties
/openapi-aiofflinehomework/homework/searchtaskdetail
	a，合并线下作业基础信息、附件信息、作答信息查询到一个http请求
	b，老师、班级、学生信息去应用缓存中去取
```

#### 10，学生端--线下作业作答

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\学生端-自学.png)

##### 问题

```properties
/openapi-aihomeworkanalyze/knowledgeAnalyze/getRecentlyKnowledgeList 获取最近有练习的知识点，一两条sql就能搞定的事情，分了成4个http请求,总是一个知识点列表传来传去。

/openapi-aihomework/Supplementary/getThemeList 没做分页
```

##### 调整

```properties
1，/openapi-aihomework/Supplementary/getThemeList 做分页获取
2，/openapi-aihomeworkanalyze/knowledgeAnalyze/getRecentlyKnowledgeList 合起来
	a，根据学生查询发布记录的试卷列表
	b，根据试卷列表查询知识点详情列表
```

#### 11，学生端--提升试卷

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\学生端-提升试卷.png)

##### 问题

```properties
/openapi-aihomework/paper/getElevatePaperInform 生成提升练习
生成提升练习规则：
	a,查t_con_student_knowledge表获取该用户的该知识点掌握水平值,获取不到默认为0.6 取试题难度为(0.3 0.7)之间的试题.
	b,查t_e_knowledge_question_rule表获取试题推送规则
	c,获取知识点下所有的试题详情列表（排除测评题库（t_e_theme_information的subthemetype为3的试题）的试题）
	d,获取试题难度范围：0-0.3，0.3-0.7,0.7-1.0 （默认0.7-1.0）
	e,筛选试题（1，先判断是否符合难度；2，判断是否满足题型（推送的试题数量大于0，主题型和副题型相同；3，若试题少了就加大难度去试题））
	f,若试题大于10个，取列表中的前10个
	g,生成提升试卷
	
/openapi-aihomework/paper/getQuestionInformation 获取试卷的试题列表
```

##### 调整

```properties
1，/openapi-aihomework/paper/getElevatePaperInform 生成提升练习，
	a，应该是在学生作答以后自动生成的，不应该放到获取提升练习的场景下。
	
2，/openapi-aihomework/paper/getQuestionInformation 修改
	a，根据知识点获取提升练习的试题列表.
{"knowledgeId":"CNBJTW0100000003012","chapterId":"CNBJTW0610000403585","classId":"CJTWBS1S600000023932","userId":"TWPAAS1200001438005","gradeId":"1","subjectId":"100000000002","paperType":"2"}
```

#### 12，学生端--学习分析

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\学生端-学习分析.png)

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\学生端-学习分析-知识点.png)

##### 问题

```properties
/openapi-aihomeworkanalyze/paperQuestionAnalyze/getLearnAnalysis(获取用户作业、测验学习分析正确率) 按类型【作业和测验】分别查了2次。
	a，统计一个月内和一个学期内获取学生和班级在作业、测验学习上面的正确率
    计算：获取一个月内和一个学期内的发布记录id，然后通过发布记录获取作答结果表中的作答结果统计个人和班级的正确率。

/openapi-aihomeworkanalyze/userLearnAnalyze/getSelfLearnAnalysis
	a，统计一个月内和一个学期内班级的平均题量、个人做题量、班级正确率、个人正确率
	计算：这里是逻辑很混乱啊 根据登录的学生id获取学生的班级信息->根据班级信息获取学生列表 ->根据学生列表查询（关联t_e_paper_result，t_e_paper_status，t_e_paper_publish）查询作答统计。t_e_paper_status这个表是有班级信息的，学生列表没有必要去查。

/openapi-aihomeworkanalyze/knowledgeAnalyze/getLearnCompositeAnalysis （根据学科 时间分析个人知识点掌握情况）
	a，统计一个月内和一个学期内个人知识点掌握情况
	计算：坑了个跌，这里先把全班每个学生的知识点掌握情况查出来，再获取个人的，再统计每个区间的总人数，再统计个人所在的掌握的区间。

/openapi-aihomeworkanalyze/knowledgeAnalyze/getWeeklessKnowledgeList
	a，与/openapi-aihomeworkanalyze/knowledgeAnalyze/getLearnCompositeAnalysis的代码逻辑惊人相似。
	计算：小于60分的算薄弱知识点
	
```

##### 调整

```properties
1，没有数据的时候，学习分析界面丑吗？ 正确率 和 知识点 ~ ~
2，围绕知识点、试题设计统计表
3，去掉/openapi-aihomeworkanalyze/userLearnAnalyze/getSelfLearnAnalysis、/openapi-aihomeworkanalyze/knowledgeAnalyze/getWeeklessKnowledgeList接口 。只用2个接口处理，一个查正确率、一个查知识点。分别在正确率 和 知识点 点击后触发对应接口。

```

#### 13，学生端--错题本

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\学生端-错题本.png)

##### 问题

```properties
/openapi-aihomework/wrongQuestion/getWrongSubjectCount
/openapi-aihomeworkanalyze/knowledgeAnalyze/getWrongKnowledgeCount
/openapi-aihomework/wrongQuestion/getWrongStudentQuestionList

三个接口都是分得太细了，查询知识点后再查询知识点下面的试题列表，再根据试题列表查试题详情列表。
```

##### 调整

```properties
1，重写，都没超过3个表，要合起来查
```

### 其他优化

###### 框架优化

1，配置项优化

以前的工程会有一堆配置，一个工程5个文件，7个微服务就是30多个文件，想一想这种项目要是我改一个配置是不是要改30多个文件，怎么以后维护，其实很多都没什么用，重复率很高，这次简化了所有普通应用的配置，普通应用只留一个注解，集中放到了aihomework-common工程，若是普通项目有特殊配置，还是可以定义单独的application.properties来覆盖我给出的初始配置。如下：

![](C:\Users\lqd\Desktop\aichange\config.bmp)

2，main函数配置的精简

main函数之前总是一堆注解，一堆七七八八的东西，不够精简，这次将main函数的注解全部提出来变成二个组合注解。分别是AiHomeworkMicroServiceMain、AiHomeworkOpenapiMain。可以看出一个是用作微服务、一个是用于服务聚合的，只要添加对应的服务实例名称即可。

```java
@AiHomeworkOpenapiMain(instanceId = "openapi-selfstudy")
@AiHomeworkMicroServiceMain(instanceId = "question-service")
```

3，日志配置的精简

同配置优化一样，将日志的配置统一放到了aihomework-common工程，不用每个工程单独重复定义。

各个工程可以通过以下配置调整日志级别：

```properties
aihomework.logback.logging.level=error
```

生成的日志进行了分项目、分层、分类型处理，同时简化了日志输入的内容。

![](C:\Users\lqd\Desktop\aichange\logs.bmp)

![](C:\Users\lqd\Desktop\aichange\logs1.png)

注意：ai作业里头的log不要单独定义，统一使用@Slf4j注解。

4，版本号的优化处理

a,支持一键修改所有项目的版本号，若是要放版本，进入aihomework-parent的目录，在terminal中输入：

```
mvn versions:set
等几秒后，弹出：
Enter the new version to set 1.3.2.0508_alpha: :
此时输入你的版本号即可修改全局版本。
```

b,ai作业全新版本从1.3.2开始，不跟随eco版本走。当前版本为1.3.2.0508_alpha（采用国际标准），版本转测后alpha变成beta，发布后变成release。

c,统一版本管理，所有的引入的jar包，必须将在父pom中声明，版本的引用。子module不能带版本号，除非同即module。如下，加入到dependencyManagement标签下。

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>io.springfox</groupId>
      <artifactId>springfox-swagger2</artifactId>
      <version>2.9.2</version>
```

d,ai作业的maven的版本号修改是全局的，你不要调整其他任何地方。项目启动后环境的版本号，eureka上注册的版本号等都会随之变化。

只上述四点我们做到了以后加入任何的子工程微服务，只需要在main函数中加上对应的注解以及引用对应的jar包即完成了项目工程的搭建，不需要其他任何的配置。

5，调试

有时候我们需要进行openapi和微服务之间联调，传统做法是在@FeignClient指定url。看得出这种方式不够灵活，配置麻烦，还是install~~。当我们要联调多个微服务多个controller的时候是不好用的。

于是，做了下改进，支持本地多个openapi和多个微服务联调。只不过要先启动微服务后再启动openapi。启动openapi的时候有提示，如下：

```properties
2019-05-24 10:30:14.168 entConfigurationBeanFactoryPostProcessor : -_-本地aihomework-service服务没有启动，当前应用无法和aihomework-service微服务调试。
2019-05-24 10:30:15.176 entConfigurationBeanFactoryPostProcessor : -_-本地question-service服务没有启动，当前应用无法和question-service微服务调试。
2019-05-24 10:30:16.181 entConfigurationBeanFactoryPostProcessor : -_-本地aiofflinehomework-service服务没有启动，当前应用无法和aiofflinehomework-service微服务调试。
2019-05-24 10:30:17.186 entConfigurationBeanFactoryPostProcessor : -_-本地mistakescollection-service服务没有启动，当前应用无法和mistakescollection-service微服务调试。
2019-05-24 10:30:18.189 entConfigurationBeanFactoryPostProcessor : -_-本地knowledge-service服务没有启动，当前应用无法和knowledge-service微服务调试。
2019-05-24 10:30:19.195 entConfigurationBeanFactoryPostProcessor : -_-本地file-service服务没有启动，当前应用无法和file-service微服务调试。
```

当然，该功能只能用于dev的开发环境。

6，启动优化

项目启动可能要很久，也可能一会儿，什么时候已经启动完了，之前的项目是没有给出提示的，这次利用boot的command优化输出，测试也可以根据提示判断项目是否启动完成。提示如下：

```properties
2019-05-24 10:30:03.019 t.s.m.l.AihomeworkApplicationRunListener : Ai作业【线上作业openapi】启动中，请耐心等待.....
2019-05-24 10:31:03.645 t.s.m.l.AihomeworkApplicationRunListener : Ai作业【线上作业openapi】启动中，请耐心等待.....
2019-05-24 10:31:17.564 omeworkApplicationReadyApplicationRunner : Ai作业【线上作业openapi】启动完成
```

7，新的swagger管理界面

以前的swagger页面，操作起来不够顺畅，这次对这个页面做了优化。

在浏览器中输入：http://IP:9528/doc.html 即可使用到新的swagger。

a,支持请求参数的缓存。只要不刻意删掉这个页面浏览器缓存，下次重新启动服务的时候，对应的上次输入的请求参数还会保留。

b,支持中英文接口文档下载。《- - 重点重点

至于带来的其他优化，可以自己去体验了。

8，eureka注册的优化

a,以往，我们同个应用无法区分版本，因为我们再同个eureka总是注册同样的服务名称。这次做了调整，可以满足在同一套环境上同个应用多个版本同时存在。这意味着我们新旧版本可以同时开发而不要搭建多套PASS环境。提高了资源利用率，支持我们的服务多样化。

b，instanceid的调整

如eureka注册上的status一栏，调整了名称标识，让人一眼就能识别出来。同时修改了跳转地址，点击后直接跳转到对应服务的doc.html文档页面。

eureka的注册如：

![](C:\Users\lqd\Desktop\aichange\ek.png)

注意：其他使用ai作业的微服务的api的，请在配置文档中配置对应的配置项即可使用对应版本的api，例如：

```properties
aihomework.project.Cversion=1-3-2-0508-ALPHA ##1.3.2.0508_ALPHA版本号中的.和_改成-即可
```

9，简化了远程配置

以往我们加个服务就要去能力平台去配置一把。这次我们简化eco注册的远程配置的配置项，ai作业应用只保留aihomework-service和openapi-aihomework两个配置项（之前已经存在的）。新加的项目不需要添加额外的配置。

其实也建议其他项目也调整下。不需要新建那么多配置。怎么做的？

查看能力平台代码可知，twasp.config.name配置项是优化获取的名称。所以只要在环境配置中配置twasp.config.name即可指定获取对应的远程配置。

![](C:\Users\lqd\Desktop\aichange\config11.png)

10，优化banner的输出

优化banner的输出：服务信息、服务配置、jvm配置信息，让开发更舒服。如下：

```
////////////////////////////////////////////////////////////////////
//                          _ooOoo_                               //
//                         o8888888o                              //
//                         88" . "88                              //
//                         (| ^_^ |)                              //
//                         O\  =  /O                              //
//                      ____/`---'\____                           //
//                    .'  \\|     |//  `.                         //
//                   /  \\|||  :  |||//  \                        //
//                  /  _||||| -:- |||||-  \                       //
//                  |   | \\\  -  /// |   |                       //
//                  | \_|  ''\---/''  |   |                       //
//                  \  .-\__  `-`  ___/-. /                       //
//                ___`. .'  /--.--\  `. . ___                     //
//              ."" '<  `.___\_<|>_/___.'  >'"".                  //
//            | | :  `- \`.;`\ _ /`;.`/ - ` : | |                 //
//            \  \ `-.   \_ __\ /__ _/   .-` /  /                 //
//      ========`-.____`-.___\_____/___.-`____.-'========         //
//                           `=---='                              //
//      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^        //
//            佛祖保佑       永不宕机      永无BUG                　　//
////////////////////////////////////////////////////////////////////
欢迎来到AI作业！-- 效率源于改进，创新源于追求
服务信息
----------------------------------
    当前服务为：线上作业openapi
    服务的端口：9528
    所处环境：开发环境【dev】
    应用版本：1.3.2.0508_alpha
    服务本地的文档和调试地址：http://localhost:9528/doc.html
    服务注册的实例名称：Ai作业_线上作业openapi[1.3.2.0508_alpha]
    服务类型：openapi
----------------------------------
配置信息
----------------------------------
    注册中心：http://192.168.210.52:9100/eureka/
    远程配置中心：http://dev.teewon.net:9300/configs
    docker镜像仓库：http://192.168.133.27:8089
----------------------------------
jvm参数配置
----------------------------------
    已用内存：123M
    最大内存：1801M
```

11，项目分环境

ai作业目前启动后，默认的都是dev环境。新加入的项目，默认也是dev环境。不需要你任何的手动添加。

###### 集成部署优化

1，切换不同环境打包、替换远程项目配置文件

a,ai作业后续的打包分三个环境，combine开发联调环境、test测试环境、prov生成环境。只需要在对应的打包命令下输入-P环境编号即可。

例如：

```
mvn clean deploy -Pcombine 就是生成开发联调环境对应的服务
```

b,ai作业无论前端、还是后端打包都会用远程服务器上的配置覆盖掉应用的配置，保证生成环境的配置的安全性，保证各个环境配置的统一性。

2，所有的服务，无论前后端都支持了生成docker镜像，都支持了推送到harbor镜像仓库。每个镜像除了当前版本外，还保留其他的版本镜像。

3，前端打包必须在jenkins上打包，切勿在本地打包。

4，所有的脚本不放除了指定的一台服务器上外的任何的其他的服务器上，保证脚本统一维护管理。

5，支持一键安装等。

这块的详情参考：http://192.168.133.27:8666/ 

## 三、性能、容错、安全

```properties
1，性能
在8核cpu、32g内存、1000M网卡、主表数据量（试卷表、试题表）100W，vu（1000~2000）的情况下：
在上述功能开发完后编写压测脚本，对项目的以上场景进行链路压测。
	1，对单个实例进行上述13个场景压测
	2，对多个实例进行压测，保证能够水平扩容
目标：
	1，每个接口的qps 1s。
	2，调整压测参数，得到性能瓶颈。

2，容错
	1，网络带宽限速1M内（3G网络），测试系统性能。
	2，停掉平台数据调用层tw-cloud-platform-aihomework的相关服务（消息、数据拉通等），系统能否正常使用。
	3，停掉redis缓存服务器能否正常使用。

3，安全
	安全漏洞扫描，保证无高危、中危漏洞。
```

## 四、项目安装部署调整

```properties
1，整理安装脚本（全量安装脚本、升级脚本），目前这里是混乱的。
2，支持多套部署方案，可以前后端部署在一台服务器上、也可以放开部署在不同服务器上。
3，配合架构部的自动运维的方案，添加项目的dockerfile，支持docker部署。
4，调整前端的部署方式（从tomcat迁移到nginx）
```

