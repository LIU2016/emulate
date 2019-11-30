##### 文档

用户角色:

<https://blog.51cto.com/wzlinux/2160778>

##### 实践

1，安装插件[Role-based Authorization Strategy](https://wiki.jenkins.io/display/JENKINS/Role+Strategy+Plugin)

2，设计规范

```
A.项目创建名称规范：
开发环境的项目请以“Dev项目名”为前缀 ，例如 Dev_ECR_ecrapi
转测试环境的项目请以“Test项目名”为前缀 例如  Test_ECR_ecr-activity-service

B.账号设置：
ECRAdmin         -- ECR开发账号       
AIEvalAdmin      -- 测评开发账号
AiclassPlusAdmin -- AiclassPlus开发账号
TestAdmin        -- 转测试账号。    
DevAdmin         -- 查看所有开发项目的账号，仅查看。
默认密码:xiao99@Twsm2019

C.创建全局角色、项目角色、配置角色（正则表达式匹配角色，注意结尾用“.*”）

admin     -- 超级管理员 账号收回  
xiao8899@Twsm2019

```

![角色配置](E:\workspace_train1\emulate\common\角色配置.bmp)![角色](E:\workspace_train1\emulate\common\角色.bmp)