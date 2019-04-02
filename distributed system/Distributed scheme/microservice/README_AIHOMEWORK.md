# AI作业优化方案

[TOC]

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
从学生端 和 老师端分析，通过以下手段达到目标：
1，减少网络交互的次数。
2，减少网络响应的大小，请求尽量多带条件。
3，降低每次请求的响应时间、提高吞吐量。
4，降低内存等服务器资源的消耗。
```

### 设计方案

优化的模块：首页、学生作答、老师发布

#### 1，老师端--首页

进入首页会请求如下连接：

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\首页.png)

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\学生端首页.bmp)

##### 现象

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

##### 问题分析

```properties
1，一个首页共请求了22次，请求次数过多
2，/openapi-base/base/queryDictItemList 单个请求的数量量过大
3，大量的重复获取数据，例如：/openapi-aihomework/paperTask/getPublishList获取发布列表的响应结果中本来就有了科目、班级、学生等基础信息。
4，很多请求可以合并，例如线上线下的发布列表，发布与学生作答、分数分布情况。
5，/openapi-aihomework/paperTask/getPublishList接口的问题：
	a，t_con_publish_class表和t_e_paper_publish强关联的，还分开查。然后二个查询还分别关联了同一套表结构各自来了一发。
	b，这里有统计数据的填充。
```

##### 解决方案

```properties
1，去掉所有的请求连接，只保留/openapi-aihomework/paperTask/getPublishList接口请求。
这个接口要求：
	a,合并线下线上发布作业查询
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

##### 现象

```properties
如上面分析的情况一样，获取作答详情的三个连接，请求次数6次：
/openapi-aihomework/paperTask/getAnswerResultList
/openapi-aihomework/paperTask/getQuestionResultList
/openapi-aihomework/paperTask/getScoresDistribution
/openapi-aihomework/answer/sendBack
```

##### 问题分析

```properties
1,前端请求没做分页啊。
2,三个请求的参数都是classID和publishID。
/openapi-aihomework/paperTask/getQuestionResultList：业务逻辑坑爹啊。
/openapi-aihomework/paperTask/getAnswerResultList：上个接口的业务逻辑又来一遍啊（例如：根据班级id查学生列表，通过发布ID获取试卷ID）。
/openapi-aihomework/paperTask/getScoresDistribution：好吧，又来了一遍（例如：班级学生列表，发布记录，学生作答）
接口逻辑的重复，造成整个链路的响应时间加长，不可取。
3，/openapi-aihomework/answer/sendBack接口，有CCE\ECP数据拉通代码，并且未做容错和异步处理。
```

##### 解决方案

```properties
1，前端一定要分页获取，因为当这里的班级的学生增多时，一把全部拿下来，对服务器和网络都是有压力的。
2，一次请求可以完成的事情没必要分多次请求。因为是相同，三个请求的接口业务逻辑大部分都是重合的。
3，/openapi-aihomework/paperTask/getAnswerResultList接口中会统计试题的（正确人数、错误人数、未批改人数、未提交人数）等字段，见下面的代码。
	a,新建试题的统计表（字段有：试题ID，试卷发布ID，班级ID，正确人数、错误人数），
	b,如上已经添加了发布记录统计表（未批改人数、未提交人数（总人数-已提交人数））
	c,班级详情、试卷详情存到缓存中，去掉接口中的通过试卷id获取试卷详情的查询。
4，/openapi-aihomework/paperTask/getAnswerResultList
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

##### 现象

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

##### 问题分析

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

##### 解决方案

```properties
1，发布作业-选择教辅
	a，分页获取教辅（/openapi-aihomework/Supplementary/getThemeList）
	b，通过教辅id获取章节详情列表（/openapi-aihomework/Supplementary/getCatalogList）
	
2，发布作业-配套试卷-选择试题
	a，去掉/openapi-aihomework/paper/getPaperQuestionList的调用。直接用试卷id去分页获取试题列表
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

##### 现象

```properties
/openapi-aihomework/Supplementary/getThemeList 获取教辅列表
/openapi-aihomework/Supplementary/getCatalogList 获取章节详情

大量的图片请求。
```

##### 问题分析

```properties
如上 3，老师端--线下作业/线上作业/智能测验发布页面，有做过分析，处理办法参考上面。
除了接口请求外，发现大量的附件请求。若网络较差，这里需要优化。
```

##### 解决方案

```properties
1，参考【3，老师端--线下作业/线上作业/智能测验发布页面】调整接口
2，附件请求请带宽高，不能用原图（fs文件请求目前支持带宽高的压缩）
例如：
http://192.168.102.204:9000/fs/media/CNBJTW0/content/2018/4/23/png/0189d35d-4a66-4370-9b11-af67dea88bad.png?height=100&width=100
3，合并图片请求（fs不支持）
```

#### 5，老师端--学习分析

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\分析.png)

![](C:\Users\lqd\Desktop\Ai作业\AI作业C03SP02\分析-自学.png)

##### 现象

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

##### 问题分析

```properties
1，/openapi-aihomeworkanalyze/publishAnalyze/getPaperAnalysisList 会查询试卷的发布信息、查询学生的作答信息、查询学生作答结果表等。
	a，发布记录表为了查询主任务id多关联了2个表（主任务表和子任务表） 
	b，作答信息和学生作答结果 多遍历了作答状态表，关键是sql没有用到索引。当作答数据大了后就会很慢。
2，/openapi-aihomeworkanalyze/userLearnAnalyze/getBookPracticeList 这是个相当啰嗦的接口，集中反映了微服务的乱用。
	a，先查询专题 -> 根据专题查关联的资源 -> 根据资源获取其中是书本的资源 -> 根据书本查封面文件的关联关系 -> 根据文件的关联关系查文件  -> 【组装教材列表】 -> 根据教材查询所有每个教材的章节 ->【组装章节到教材列表】 -> 查询章节下所有的知识点 -> 【组装知识点】 -> 获取所有知识点关联的试卷 -> 根据试卷获取发布记录 -> 查询知识点下的所有试题 -> 所有试题的学生作答 -> 【统计练题次数】 一个发了11次http请求。
3，openapi-aihomeworkanalyze/knowledgeAnalyze/getKnowledgeAnalyzeOutcomes 知识点总体统计
、/openapi-aihomeworkanalyze/knowledgeAnalyze/getKnowledgeAnalyzeStudentRank 知识点统计学生排名、/openapi-aihomeworkanalyze/knowledgeAnalyze/getKnowledgeAnalyzeList 知识点统计列表 这三个接口的代码居然惊人的相似，大段逻辑都是一样，只有最后的分析有些不同。
```

##### 解决方案

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





