##### 文档

用户角色:

<https://blog.51cto.com/wzlinux/2160778>

jacoco安装：

<https://cloud.tencent.com/developer/article/1430884>

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
TestAdmin        -- 转测试账号    
DevAdmin         -- 查看所有开发项目的账号，仅查看
ECOAdmin         -- ECO开发账号
默认密码:xiao99@Twsm2019

C.创建全局角色、项目角色、配置角色（正则表达式匹配角色，注意结尾用“.*”）

admin     -- 超级管理员 账号收回  
xiao8899@Twsm2019

```

![角色配置](E:\workspace_train1\emulate\common\角色配置.bmp)![角色](E:\workspace_train1\emulate\common\角色.bmp)



##### 迁移

```kotlin
迁移步骤为：
1）先关闭新老服务器的tomcat程序，确保迁移时新老机器的jenkins都处于关闭状态。jenkins程序关闭最好是直接kill掉jenkins的tomcat程序pid。
2）将老服务器jenkins主目录下的
config.xml文件以及jobs、users、workspace、plugins四个目录拷贝到新机器的jenkins主目录下。
3）重启新服务器jenkins的tomcat程序。
 
迁移的时候可以直接将jenkins主目录数据整个拷贝过去，也可以单独拷贝jenkins主目录下的config.xml文件以及jobs、users、workspace、plugins四个目录（这是主要的迁移数据）。一般来说，手动设置好jenkins主目录路径，启动jenkins后就会自动生成（但要确保jenkins用户有权限创建这个主目录，最好是提前手动创建并赋予jenkins启动用户的权限）
 
关闭老机器的jenkins程序
[root@code-server ~]# lsof -i:8080
COMMAND    PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
bundle   13481  git   15u  IPv4 2839661      0t0  TCP localhost:webcache (LISTEN)
[root@code-server ~]# kill -9 13481
 
新机器的jenkins程序也要同样关闭
 
拷贝老服务器的jenkins主目录或者上面说的那几个重要数据到新机器的jenkins主目录下
[root@code-server ~]# rsync -e "ssh -p22" -avpgolr --delete /data/jenkins/ root@10.0.8.60:/data/jenkins/
 
或者
[root@code-server ~]# rsync -e "ssh -p22" -avpgolr /data/jenkins/config.xml root@10.0.8.60:/data/jenkins/
[root@code-server ~]# rsync -e "ssh -p22" -avpgolr --delete /data/jenkins/users/ root@10.0.8.60:/data/jenkins/users/
[root@code-server ~]# rsync -e "ssh -p22" -avpgolr --delete /data/jenkins/plugins/ root@10.0.8.60:/data/jenkins/plugins/
[root@code-server ~]# rsync -e "ssh -p22" -avpgolr --delete /data/jenkins/jobs/ root@10.0.8.60:/data/jenkins/jobs/
[root@code-server ~]# rsync -e "ssh -p22" -avpgolr --delete /data/jenkins/workspace/ root@10.0.8.60:/data/jenkins/workspace/
 
尤其是plugins目录,最好保证新机器下的这个目录和老机器下的这个目录数据保持一致。否则容易造成新机器的jenkins访问报错
 
最后启动新机器的jenkins服务
[root@jenkins01 ~]$ /data/tomcat8.5/bin/startup.sh
[app@jenkins01 ~]$ lsof -i:8080
COMMAND    PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
java    101037  app   46u  IPv6 498942      0t0  TCP *:webcache (LISTEN)


迁移和备份
如果有jenkins服务在运行中，建议先停止jenkins服务。

备份Jenkins的配置

进入/root/.jenkins目录下,使用tar -cvf jenkins.tar .jenkins/*命令 对该目录下的所有文件进行打包。然后导出到本地（sz 文件名：导出文件/压缩包等）

然后拷贝数据到新路径，我迁移的路径为 /opt/ldkjdata/.jenkins，

cp /root/.jenkins /opt/ldkjdata/.jenkins

设置JENKINS_HOME环境变量参数
打开tomcat的bin目录，编辑catalina.sh文件，在第一行下面添加
export JENKINS_HOME=/opt/ldkjdata/.jenkins

并且在profile文件最后加入：
vi /etc/profile
在最后加入：
export JENKINS_HOME=/opt/ldkjdata/.jenkins
保存，退出后执行
source /etc/profile
让配置生效

然后启动jenkins，所有的插件，配置，job及备份全部已迁移。
```

##### 异常

```
jenkins 迁移 Unable to read /data/jenkins/.jenkins
------------------------------------------------------
当出现启动失败，抛出excption时，可以尝试进行如下操作：
将security禁用，具体操作步骤如下：


停止jenkins (最方便的方式就是直接stop容器.)
切换到 $JENKINS_HOME 目录，找到config.xml文件并打开 .
搜索 <useSecurity>true</useSecurity> 这个字段.将true改成false
去掉 authorizationStrategy 和 securityRealm 这两个字段
重启jenkins
jenkins重启后将处于无安全配置状态，任何人都拥有全部的操作权限。

如果上述操作仍未生效, 请尝试重命名或者删除 config.xml 文件.

------------------------------------------------------
There were errors checking the update sites: SSLHandshakeException: sun.secu解决方案
------------------------------------------------------
进入插件管理->Advanced,修改Update Site的URL，路径为“https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json”，修改完成，submit，然后checknow。问题解决。

```

