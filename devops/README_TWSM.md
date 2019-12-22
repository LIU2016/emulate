## 测评测评-转测试流程

### 一，新租户全量构建

按照Devops自动化转测试流程：

#### SDV1转测步骤:

1，在新的租户下，刷ai作业的全量脚本，脚本目录如下：

http://192.168.111.244:8888/svn/aischool/doc/01.项目文档/Ai作业/V001R001C03SP02/03.发布区/SDV1/01.安装包/DB/全量脚本

2，在新的租户下，刷测评的全量脚本，脚本目录如下（发邮件给DB要求上传转测试脚本）：

http://192.168.111.244:8888/svn/aischool/doc/01.项目文档/Ai测评/V001R001C01/03.发布区/SDV1/01.安装包/DB

3，若没有elasticsearch服务，请先安装。

基于容器技术安装，依次执行下面步骤：

1. 在安装elasticsearch服务的主节点上输入如下命令安装docker以及docker-compose。

   ```shell
   curl -sSL http://192.168.133.29:8666/install/docker-install.sh |sh -xs baseinstall 192.168.133.29 8666
   ```

2. 在需要安装elasticsearch服务的主节点上输入如下命令，搭建swarm网络。

   ```shell
   curl -sSL http://192.168.133.29:8666/install/swarm-install.sh |sh -xs confignetwork 192.168.133.29 8666 twsm_aievaluation_network 172.62.0.1
   ```

3. 在需要安装elasticsearch服务的主节点上输入如下命令，安装ELKC+Xpack 搜索引擎全家桶。

   ```shell
   curl -sSL http://192.168.133.29:8666/install/elasticsearch-install.sh |sh -xs installelastic 192.168.133.29 8666 elasticsearch
   ```

4. 若后续硬件资源不够，建议水平扩容，在子节点上输入如下命令安装：

   ```shell
   a，curl -sSL http://192.168.133.29:8666/install/swarm-install.sh |sh -xs confignetworknode 192.168.133.29 8666 twsm_aievaluation_network 
   
   b，获取主节点的es01、es02的容器IP地址，修改/etc/hosts中的映射关系。
   
   c，curl -sSL http://192.168.133.29:8666/install/elasticsearch-install.sh |sh -xs installelasticnode 192.168.133.29 8666 elasticsearch
   ```

4，使用登录kibana服务，刷elasticsearch索引脚本（这里刷的租户索引的租户参考的是现网Ai作业已经有的租户）。脚本目录如下：

http://192.168.111.244:8888/svn/aischool/doc/01.项目文档/Ai测评/V001R001C01/03.发布区/SDV1/01.安装包/ELASTICSEARCH

1. 当某个产品第一次使用，
   a，**登录【elastic/Xiao99@Twsm2019】管理员账号，**拿产品目录的base目录下的base.json（例如：aihomework/base/base.json）在kibana下控制台执行，生成对应的策略、产品账号（都是以产品名称为目录名称，所以账号就是目录名称）、产品角色
   （注意：kibana的控制台查看要用管理员账号去角色下开启，账号的默认密码是：Xiao99@Twsm2019）
   b，登录指定的产品的账号（例如：aihomework），拿init_[index].json（例如：aihomework/init目录下的业务索引的脚本），在kibana下控制台执行创建索引.
2. 当某个产品添加了新租户，
   a，重复1-b)步骤完成索引创建。
3. 当某产品升级某租户索引结构时，
   a，使用[version]_upgrade_[index].json（例如：aihomework/V001R001C01_upgrade目录下的业务索引的脚本），登录指定的产品账号，去kibana控制台执行修改索引。

注意：去如图所示的控制台刷脚本：![elasticsearch](C:\Users\lqd\Desktop\elasticsearch.png)

5，登录微服务治理平台（例如：DEV环境对应的就是<http://192.168.210.52:9999/>）

1. 检查是否有：aihomework-service 和 openapi-aihomework 。没有就去【服务管理-服务列表】加这两个服务。

2. 选择【服务管理-服务配置】，检查配置是否正确，没有就有配置。

   ```
   aihomework-service 应该有的配置：db，kafka，lts，redis，other
   openapi-aihomework 应该有的配置：kafka，lts，redis，other
   ```

3. 注意：【新增Namespace】，新加elasticsearch的Namespace，配置其配置项如下：

   ```properties
   elasticsearch的访问地址，例如：
   elasticsearch.host 192.168.130.27:9200,192.168.130.27:9500
   
   elasticsearch的端口，例如：
   elasticsearch.port 9200
   
   elasticsearch的账号（这里先用这个管理员账号，后面调整为租户账号），例如：
   elasticsearch.username elastic 
   
   elasticsearch的密码，例如：
   elasticsearch.password xiao99@Twsm2019
   
   ```

4. 在aihomework-service和openapi-aihomework服务配置上关联elasticsearch Namespace。


6，使用ProvAdmin账号（密码参考之前的邮件），登录jenkins，配置转测试安装任务。参考192.168.130.69，配置好任务后，点击构建发布（这里不会打包，只是安装到指定服务器），完成应用安装。

![jenkins](C:\Users\lqd\Desktop\jenkins.png)

- 注意：先要发邮件给jenkins管理人员添加服务节点。
- 注意：首次安装，构建完状态展示为黄色，根据控制台的日志提示，要登录部署节点根据提示要修改服务的配置文件（指定ECO的环境、镜像仓库的环境地址等等）。

#### SDV2..N后续转测步骤:

使用ProvAdmin账号（密码参考之前的邮件），登录jenkins，点击构建发布，完成应用更新安装。

### 二，旧租户升级

一，数据脚本升级操作旧租户。

二，logstash将旧数据导入elasticsearch租户索引。

