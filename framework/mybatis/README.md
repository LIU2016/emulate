### mybatis xml操作

mybatis批量新增：

```xml
 <insert id="batchInsertHomeworkTask" parameterType="java.util.List" useGeneratedKeys="true"
            keyProperty="taskId">
        <!--<selectKey resultType="java.lang.String" keyProperty="taskId" order="BEFORE">-->
            <!--SELECT nextval_gdcode('aihomework.seq_taskid_t_e_offlinetask') as taskId-->
        <!--</selectKey>-->
        INSERT INTO aihomework.t_e_offlinetask(
            taskid,
            orgid,
            classid,
            tasktype,
            tasksubject,
            taskcontent,
            fileflag,
            tasklinkUrl,
            tasklinkTitle,
            starttime,
            endtime,
            evaltype,
            motivatetype,
            creatorid,
            createtime,
            lastmodifierId,
            lastmodifyTime,
            likecount,
            smsflag,
            taskbatch
        )
        VALUES
        <foreach collection="list" item="homeworkTask" separator=",">
            (
                nextval_gdcode('aihomework.seq_taskid_t_e_offlinetask'),
                #{homeworkTask.orgId},
                #{homeworkTask.classId},
                #{homeworkTask.taskType},
                #{homeworkTask.taskSubject},
                #{homeworkTask.taskContent},
                #{homeworkTask.fileFlag},
                #{homeworkTask.taskLinkUrl},
                #{homeworkTask.taskLinkTitle},
                #{homeworkTask.startTime},
                #{homeworkTask.endTime},
                #{homeworkTask.evalType},
                #{homeworkTask.motivateType},
                #{homeworkTask.creatorId},
                #{homeworkTask.createTime},
                #{homeworkTask.lastModifierId},
                #{homeworkTask.lastModifyTime},
                #{homeworkTask.likeCount},
                #{homeworkTask.smsFlag},
                #{homeworkTask.taskBatch}
            )
        </foreach>
    </insert>
```

