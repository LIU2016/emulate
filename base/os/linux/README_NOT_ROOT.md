# linux下非root安装

参考：

https://en.wikipedia.org/wiki/Sudo

http://blog.51cto.com/wbxue/1965545

https://www.cnblogs.com/huanglinxin/p/9154852.html

https://www.cnblogs.com/superlinux/p/1324d19f9d54eaac83247081c8362ee6.html

https://linux.cn/article-8145-1.html

http://www.linuxmysql.com/16/2017/475.htm

http://man.linuxde.net/sudo

http://blog.51cto.com/meiling/1894890 端口问题

https://rorschachchan.github.io/2018/04/18/%E4%BD%BF%E7%94%A8%E6%99%AE%E9%80%9A%E7%94%A8%E6%88%B7%E5%90%AF%E5%8A%A8tomcat/ 

http://www.hxiangyu.com/2017/10/%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%94%A8%E6%88%B7%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86%E4%B8%8E%E6%94%B9%E9%80%A0%E5%AE%9E%E6%96%BD%E9%A1%B9%E7%9B%AE%E4%BB%A5%E5%8F%8A%E5%A6%82%E4%BD%95%E9%80%9A%E8%BF%87rs/

## sudo配置规则

### 踩过的坑

1，sudoers.d目录下的配置的别名一定要使用*大写* 

2，/etc/sudoers.d目录下的文件没有后缀

3，cd是shell内建命令，不能用sudo的。如果想进入某个目录又没有权限，要么改目录权限，要么执行sudo -sH 切换成root用户。

4，sudo 操作命令设置成当前用户的别名，从而避免大量修改已有的安装代码。

5，安装cce异常：

```
psql.bin: could not connect to server: No such file or directory
	Is the server running locally and accepting
	connections on Unix domain socket "/opt/PostgreSQL/10/data/.s.PGSQL.8832"?
/usr/twsm/aischool-install/bin/common/random_pwd.sh: line 39: [: -eq: unary operator expected
```



## 非root安装流程

1，政通云上新建全新的192.168.131.26服务，基于centos6.9(6.5\6.7)、centos7.4

2，先使用root登录系统。（root ）

> a.创建/usr/twsm、/opt、/data目录，并进行挂载。
>
> b.解压user-install.zip。若没有安装unzip工具，执行命令
>
> ```shell
> yum install -y unzip
> ```
>
> b.执行用户、用户组、sudo权限配置、环境变量设置的脚本。
>
> c.在user-install目录下执行脚本，这里的aiclass为用户组名，默认情况下会在这个组下生成对应的一个同名用户：
>
> ```shell
> [root@root twsm]# cd user-install/
> [root@root user-install]# sh bin/twsm_operation_sudo.sh aiclass
> aiclass PASSWORD = AaV4nifa
> 1-----aiclass PASSWORD = AaV4nifa
> 2-----create group aiclass
> Changing password for user aiclass.
> passwd: all authentication tokens updated successfully.
> 3-----create user aiclass
> 4-----set sudo configuration , use default sudo configure
> 4.1--------validate sudo configure 
> 5-----set evn alias, use default env configure
> [root@root user-install]# cat log/userinstall.log 
> /etc/sudoers: parsed OK
> /etc/sudoers.d/90-cloud-init-users: parsed OK
> /etc/sudoers.d/aiclass: parsed OK
> 5-----set evn alias, use default env configure
> [root@root user-install]# cat log/userinstall.log 
> /etc/sudoers: parsed OK
> /etc/sudoers.d/90-cloud-init-users: parsed OK
> /etc/sudoers.d/aiclass: parsed OK
> 5-----set evn alias, use default env configure
> ```
>
> d.执行完后，查看日志。从日志中可以看出sudoers的配置文件解析正确。若不正确，修改你的配置。
>
> ```shell
> [root@root user-install]# cat log/userinstall.log
> /etc/sudoers: parsed OK
> /etc/sudoers.d/90-cloud-init-users: parsed OK
> /etc/sudoers.d/aiclass: parsed OK
> 5-----set evn alias, use default env configure
> ```
>
> e.关于安装目录twsm/的ACL权限设置,这里只针对安装账号设置。（本文假若安装账号为：aiclass）
>
> ```shell
> [root@root usr]# chown -R aiclass:aiclass twsm/
> [root@root usr]# chmod 770 twsm/
> ```
>
> ```shell
> note：
> 若没有设置twsm目录的权限，会导致登录aiclass账号后，没有ACL操作权限。将没法做文件拷贝等。
> 
> for instance：
> [aiclass@root twsm]$ scp root@192.168.102.112:/usr/twsm/CCE-V006R001C06B06SP02B03.zip ./
> The authenticity of host '192.168.102.112 (192.168.102.112)' can't be established.
> RSA key fingerprint is f6:8f:8b:75:06:4f:56:22:ef:07:6f:34:08:d8:b7:90.
> Are you sure you want to continue connecting (yes/no)? yes
> Warning: Permanently added '192.168.102.112' (RSA) to the list of known hosts.
> root@192.168.102.112's password: 
> .//CCE-V006R001C06B06SP02B03.zip: Permission denied
> 
> ```
>
> f. 关于data目录的权限设置
>
> ```shell
> [root@root sudoers.d]#  chown -R aiclass:aiclass /data
> [root@root sudoers.d]# chmod 770 /data
> ```
>
> g. 检测是否有如下安装工具，没有请安装：
>
> ```shell
>  yum install -y vsftpd
>  yum install -y dos2unix
>  yum -y install gcc-c++ 
> ```
>
>

3，使用新建的账号登录系统，执行cce版本安装。

> a.步骤2生成的日志可以查看到用户的密码：
>
> ```shell
> [root@root user-install]# cat log/userpassword.log 
> 2018-12-26+15:30:47 create aiclass random password!
> aiclass PASSWORD = AaV4nifa
> ```
>
> b.使用AaV4nifa密码登录aiclass账号。
>
> c. 解压cce的包，执行安装
>
> ```shell
> sh aischool-install.sh -a NBACBA2
> ```
>
>

# 产品安装

## CCE

### 安装流程

按照商讨结果，cce今后的安装分2部分：基础软件（-A 和普通应用（-B 安装；

- 基础软件登录twsm账号执行安装；

- 普通应用登录operation账号执行安装；

#### CCE安装包现状

![cce安装包](C:\Users\lqd\Desktop\非root\cce安装包.png)

#### 目前的安装

步骤如下：

- 上传安装文件

  - 登录ssh账号登录服务器，并把文件传到ssh的用户目录中。
  - 在ssh账号下，通过su切换到twsm账号。

- 切换到twsm账号后，执行基础软件安装

  - 修改语言环境

    ```shell
    echo 'LANG=zh_CN.UTF-8' > /etc/sysconfig/i18n
    echo 'LC_ALL=zh_CN.UTF-8' >> /etc/sysconfig/i18n
    ```

  - 安装基础软件（-A。

    ```shell
    [twsm@root twsm]# sh install/install.sh  -all
    ```

    ```properties
    note:
    安装过程中可能需要输入root密码。
    ```

  - 修改user-install安装目录权限/install安装目录，保证出root组和twsm账号的能访问操作外，其他账号都没有权限

    ```shell
    [root@root usr]# chmod 755 twsm/
    [root@root twsm]# chmod 700 user-install
    [root@root twsm]# chmod 700 install
    [root@root /]# chown -R operation:operation /data
    ```

  - 修改普通应用（-B 安装目录权限，命令如下：

    ```shell
    [root@root twsm]# chown -R operation:operation aischool-app-install/ aischool-install/ twgame-install/ upgrade-tool/
    [root@root twsm]# chmod -R 775 aischool-app-install/ aischool-install/ twgame-install/ upgrade-tool/
    ```

- 切换到operation账号后，执行普通应用安装

  - 修改upgradetool.sh脚本，将随机启动部分的脚本从install/install.sh文件中改到这个文件中。

  - 修改aischool-install中的install.sh脚本：

    - 将日志记录的文件转移到aischool-install目录下

    ```sh
    progress_log=/usr/twsm/aischoo-install/progress.txt
    ```

    - 修改aischool-install中的install.sh 脚本，数据库的定时任务处理迁移到install/install.sh文件中

      ```shell
      crontabconf()
      {
      
        dataDir=`sed 's/ //g' /etc/postgres-reg.ini | grep "DataDirectory" | awk -F "=" '{print $2}' | grep -v '^$'`
        
        if [ `cat  $dataDir/pg_hba.conf | grep local | grep all | grep trust | wc -l` -eq 0 ]; then   
          sed -i "`cat -n $dataDir/pg_hba.conf | grep local | grep all | grep md5 | grep -v replication | awk -F ' ' '{print $1}'`s/.*/local   all             all                                     trust/"   $dataDir/pg_hba.conf 
          sed -i "`cat -n $dataDir/pg_hba.conf | grep 127.0.0.1/32 | grep all | grep md5 | grep -v replication | awk -F ' ' '{print $1}'`s/.*/host    all             all             127.0.0.1\/32           trust/"  $dataDir/pg_hba.conf 
          sed -i "`cat -n $dataDir/pg_hba.conf | grep ::1/128 | grep all | grep md5 | grep -v replication | awk -F ' ' '{print $1}'`s/.*/host    all             all             ::1\/128           trust/"  $dataDir/pg_hba.conf 
      
      	if [[ `rpm -q centos-release|cut -d- -f3` = 7 ]]; 
          then
      		systemctl reload ${db_serviceid}.service
          else 
      		service $db_serviceid reload
          fi
      
        fi
        #配置备份信息
        mkdir -p /db_backup/
        mkdir -p /db_backup/log/
        mkdir -p /db_backup/scripts/
        cp /usr/twsm/aischool-install/bin/common/maintain_db.sh /db_backup/scripts/
        cp /usr/twsm/aischool-install/bin/common/auto_backup.sh /db_backup/scripts/
        cp /usr/twsm/aischool-install/bin/common/function.sh /db_backup/scripts/
        cp /usr/twsm/aischool-install/bin/common/function_18.sh /db_backup/scripts/
        cp /usr/twsm/aischool-install/bin/common/log_clean.sh /db_backup/scripts/
      
        chmod u+x /db_backup/scripts/*
      
        #加入crontab运行脚本,某些机器需要带空行才能追加进去
        crontab /usr/twsm/aischool-install/config/crontab.txt
        crontab /usr/twsm/aischool-install/config/crontab_blank.txt
      }
      ```

    - 

    - 

  - 在operation账号下，执行命令:

    ```shell
    [operation@root upgrade-tool]$ sh upgradetool.sh restart
    ```

  - 

- 

### 升级流程





## 事项

1,   磁盘目录大小、操作系统的适配

```properties
centos 6.9,7.4,7.5
假若 可用空间 2T
/          :  10% （200G以上）
/usr/twsm  ： 2.5%
/opt       ： 25% (500G)
/data      ： 其他
```

2，dls. (cce开发)

```properties
note:
  dls权限：770
  其他的chmod 目录权限控制修改
```

3，二进制文件（例如postgres、mysql的基础软件安装）需要root安装权限 （cce开发）

```properties
note：
在root的权限下，提前安装好基础软件。
-----基础软件安装和应用 安装分开。
a,确定哪些基础软件:postgres\mysql\jdk\memcache\图片压缩\openoffice\swftool\apache  ---root安装
b,应用安装                         ---安装账号
c,AiWebConsole（安装账号权限，脚本执行的sudo提权）
```

4，不同产品线各种账号的sudo权限问题（测试、开发、维优、）

```
先列出一个基础的sudo.config/
适配操作系统：centos6、centos7.4
```

5，读取证书的命令权限

```
note：
system.jar
添加命令到sudo、修改别名
```

6, linux 下的定时任务 - crontab

```properties
定时任务分开：
会后确认。
同步时间、数据库备份、数据库维护、业务函数
```

```shell
30 0 * * * /db_backup/scripts/auto_backup.sh >> /db_backup/log/backup.log 2>/dev/null （twsmdbuser账号下）
0 3 * * 0 /db_backup/scripts/maintain_db.sh >> /db_backup/log/maintain_db.log 2>/dev/null（twsmdbuser账号下）
0 23 * * * /usr/sbin/ntpdate asia.pool.ntp.org >/dev/null && /sbin/hwclock --systohc >/dev/null （root账号下）
0 4 * * * /db_backup/scripts/function.sh >/dev/null 2>/dev/null（twsmdbuser账号下）
0 18 * * * /db_backup/scripts/function_18.sh >/dev/null 2>/dev/null（twsmdbuser账号下）
*/5 * * * * /usr/twsm/install/kill_Daemon_Perl.sh > /dev/null （删除）
59 23 * * * /db_backup/scripts/log_clean.sh >/dev/null 2>/dev/null（非root账号下）
```

7, 产品版本升级（cce开发）

```properties
note:

```

8, 除了天闻管理员组外其他的所有的账号禁用ssh权限

9, 

```
cce\ecp nginx修改
eco 
```

10，sudo配置

```shell
#
User_Alias #GROUPNAME_UPPER#_USERS = %#GROUPNAME#
#
Cmnd_Alias #GROUPNAME_UPPER#_NETWORKING = /sbin/route, /sbin/ifconfig, /bin/ping, /sbin/dhclient, /usr/bin/net, /sbin/iptables, /usr/bin/rfcomm, /usr/bin/wvdial, /sbin/iwconfig, /sbin/mii-tool
Cmnd_Alias #GROUPNAME_UPPER#_SOFTWARE = /bin/rpm, /usr/bin/up2date, /usr/bin/yum, /bin/sed, /usr/bin/tee, /bin/rm, /bin/chmod, /usr/bin/dos2unix, /bin/find, /bin/mkdir, /usr/local/ffmpeg, /usr/local/ffprobe, /usr/local/ffmpeg-segement 
Cmnd_Alias #GROUPNAME_UPPER#_SERVICES = /sbin/service, /sbin/chkconfig 
Cmnd_Alias #GROUPNAME_UPPER#_JAVA = /usr/bin/killall java
Cmnd_Alias #GROUPNAME_UPPER#_DATABASE = /usr/bin/killall twdbuser, /bin/rm -rf /opt/PostgreSQL /etc/init.d/twsm /etc/postgres-reg.ini, /usr/sbin/userdel twdbuser
Cmnd_Alias #GROUPNAME_UPPER#_DATA = /usr/bin/killall contentftp
Cmnd_Alias #GROUPNAME_UPPER#_APPLICATION = /usr/sbin/userdel cloudzone, /usr/sbin/userdel dls, /usr/sbin/userdel drmportal, /usr/sbin/userdel eshop, /usr/sbin/userdel manager, /usr/sbin/userdel portal, /usr/sbin/userdel resserver, /usr/sbin/userdel contentftp, /usr/sbin/userdel openfire, /usr/sbin/userdel activity, /usr/sbin/userdel presidentReport
Cmnd_Alias #GROUPNAME_UPPER#_CACHESERVER = /bin/kill -9 `cat /tmp/memcached.pid`
Cmnd_Alias #GROUPNAME_UPPER#_PROXYSERVER = /usr/local/nginx/sbin/nginx, /bin/rm -rf /usr/local/nginx
#
#GROUPNAME_UPPER#_USERS ALL = (ALL)NOPASSWD: #GROUPNAME_UPPER#_NETWORKING, #GROUPNAME_UPPER#_SOFTWARE, #GROUPNAME_UPPER#_SERVICES, #GROUPNAME_UPPER#_JAVA, #GROUPNAME_UPPER#_DATABASE, #GROUPNAME_UPPER#_DATA, #GROUPNAME_UPPER#_APPLICATION, #GROUPNAME_UPPER#_CACHESERVER, #GROUPNAME_UPPER#_PROXYSERVER

```

11，AiWebConsole 安装

```CQL
2018-12-27 20:38:02,913 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-15] 信息:sh: /usr/twsm/progress.txt: Permission denied
2018-12-27 20:38:03,909 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [http-nio-8080-exec-10] 执行脚本异常终止：返回1 script:echo 1=10.0=开始初始化数据库。  $(date +%Y年%m月%d日%H时%M分%S秒) >> /usr/twsm/progress.txt
2018-12-27 20:38:03,950 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:(Not all processes could be identified, non-owned process info
2018-12-27 20:38:03,950 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息: will not be shown, you would have to be root to see it all.)
2018-12-27 20:38:04,014 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:cp: cannot stat `/opt/PostgreSQL/10/data/postgresql.conf': Permission denied
2018-12-27 20:38:04,021 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:cat: /opt/PostgreSQL/10/data/pg_hba.conf: Permission denied
2018-12-27 20:38:04,022 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:/usr/twsm/aischool-install/bin/config-db.sh: line 36: /opt/PostgreSQL/10/data/pg_hba.conf: Permission denied
2018-12-27 20:38:04,119 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:standard in must be a tty
2018-12-27 20:38:04,119 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-16] 信息:Restarting PostgreSQL 10: 
2018-12-27 20:38:04,123 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:standard in must be a tty
2018-12-27 20:38:04,124 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-16] 信息:PostgreSQL 10 did not start in a timely fashion, please see /opt/PostgreSQL/10/data/pg_log/startup.log for details
2018-12-27 20:38:07,129 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:/usr/twsm/aischool-install/bin/config-db.sh: line 52: /usr/twsm/progress.txt: Permission denied
2018-12-27 20:38:07,223 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:psql.bin: could not connect to server: Permission denied
2018-12-27 20:38:07,223 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	Is the server running locally and accepting
2018-12-27 20:38:07,224 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	connections on Unix domain socket "/opt/PostgreSQL/10/data/.s.PGSQL.8832"?
2018-12-27 20:38:07,229 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:/usr/twsm/aischool-install/bin/config-db.sh: line 67: /usr/twsm/progress.txt: Permission denied
2018-12-27 20:38:07,253 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:psql.bin: could not connect to server: Permission denied
2018-12-27 20:38:07,253 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	Is the server running locally and accepting
2018-12-27 20:38:07,253 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	connections on Unix domain socket "/opt/PostgreSQL/10/data/.s.PGSQL.8832"?
2018-12-27 20:38:07,258 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:/usr/twsm/aischool-install/bin/config-db.sh: line 80: /usr/twsm/progress.txt: Permission denied
2018-12-27 20:38:07,268 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:psql.bin: could not connect to server: Permission denied
2018-12-27 20:38:07,268 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	Is the server running locally and accepting
2018-12-27 20:38:07,268 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	connections on Unix domain socket "/opt/PostgreSQL/10/data/.s.PGSQL.8832"?
2018-12-27 20:38:07,272 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:/usr/twsm/aischool-install/bin/config-db.sh: line 84: /usr/twsm/progress.txt: Permission denied
2018-12-27 20:38:07,280 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:psql.bin: could not connect to server: Permission denied
2018-12-27 20:38:07,280 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	Is the server running locally and accepting
2018-12-27 20:38:07,281 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	connections on Unix domain socket "/opt/PostgreSQL/10/data/.s.PGSQL.8832"?
2018-12-27 20:38:07,283 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:/usr/twsm/aischool-install/bin/config-db.sh: line 88: /usr/twsm/progress.txt: Permission denied
2018-12-27 20:38:08,243 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:psql.bin: could not connect to server: Permission denied
2018-12-27 20:38:08,243 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	Is the server running locally and accepting
2018-12-27 20:38:08,243 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	connections on Unix domain socket "/opt/PostgreSQL/10/data/.s.PGSQL.8832"?
2018-12-27 20:38:08,386 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:psql.bin: could not connect to server: Permission denied
2018-12-27 20:38:08,386 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	Is the server running locally and accepting
2018-12-27 20:38:08,386 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	connections on Unix domain socket "/opt/PostgreSQL/10/data/.s.PGSQL.8832"?
2018-12-27 20:38:08,397 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:psql.bin: could not connect to server: Permission denied
2018-12-27 20:38:08,397 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	Is the server running locally and accepting
2018-12-27 20:38:08,397 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	connections on Unix domain socket "/opt/PostgreSQL/10/data/.s.PGSQL.8832"?
2018-12-27 20:38:08,408 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:psql.bin: could not connect to server: Permission denied
2018-12-27 20:38:08,408 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	Is the server running locally and accepting
2018-12-27 20:38:08,408 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	connections on Unix domain socket "/opt/PostgreSQL/10/data/.s.PGSQL.8832"?
2018-12-27 20:38:08,411 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:/usr/twsm/aischool-install/bin/config-db.sh: line 104: /usr/twsm/progress.txt: Permission denied
2018-12-27 20:38:08,420 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:psql.bin: could not connect to server: Permission denied
2018-12-27 20:38:08,420 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	Is the server running locally and accepting
2018-12-27 20:38:08,420 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:	connections on Unix domain socket "/opt/PostgreSQL/10/data/.s.PGSQL.8832"?
2018-12-27 20:38:08,423 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:/usr/twsm/aischool-install/bin/config-db.sh: line 108: /usr/twsm/progress.txt: Permission denied
2018-12-27 20:38:08,505 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:standard in must be a tty
2018-12-27 20:38:08,506 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-16] 信息:Restarting PostgreSQL 10: 
2018-12-27 20:38:08,510 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:standard in must be a tty
2018-12-27 20:38:08,511 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-16] 信息:PostgreSQL 10 did not start in a timely fashion, please see /opt/PostgreSQL/10/data/pg_log/startup.log for details
2018-12-27 20:38:08,546 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:Warning: Using a password on the command line interface can be insecure.
2018-12-27 20:38:08,580 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
2018-12-27 20:38:08,584 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:Warning: Using a password on the command line interface can be insecure.
2018-12-27 20:38:08,588 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
2018-12-27 20:38:08,591 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:Warning: Using a password on the command line interface can be insecure.
2018-12-27 20:38:08,595 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
2018-12-27 20:38:08,599 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:Warning: Using a password on the command line interface can be insecure.
2018-12-27 20:38:08,603 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
2018-12-27 20:38:08,606 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:Warning: Using a password on the command line interface can be insecure.
2018-12-27 20:38:08,610 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
2018-12-27 20:38:08,629 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:Warning: Using a password on the command line interface can be insecure.
2018-12-27 20:38:08,633 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-17] 信息:ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
2018-12-27 20:38:08,644 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [Thread-19] 信息:sh: /usr/twsm/progress.txt: Permission denied
2018-12-27 20:38:09,640 ERROR [AiWebConsole] [com.tianwen.eeducation.console.web.controller.LoginController] [http-nio-8080-exec-10] 执行脚本异常终止：返回1 script:echo 1=40.0=数据库初始化完成。  $(date +%Y年%m月%d日%H时%M分%S秒) >> /usr/twsm/progress.txt

```

## 工作量

```properties
a，脚本：
1，为各个命令添加sudo。
2，将命令进行sudo提权，后面的脚本基本可以不用做这个事。
3，当前用户下新建的目录或者操作的目录没有权限，调整。
4，脚本中涉及到的基础软件安装要抽离。

b，AiWebConsole：
b.1，一键安装流程，要分为单校、区级部署、云化验证
其中的引用到的命令要sudo提权、有些目录Acl权限控制、执行验证

c，在centos6.9，用户以及用户组权限配置、日志审计生成脚本
c.1，这里脚本写完，但要在centos7上验证还有默认模板上sudo的规则收集以及别名收集修改

d，在centos6.9，证书执行权限处理（目前没有找不到源码）、定时任务（5个）调整
d.1，非root的账号下执行定时任务要调整。例如目录权限
d.2，这个执行账号同样需要/sbin/service的权限

e，整个安装包安装在centos6.9、centos7.4、centos7.5安装验证以及调整
e.1，环境centos7.5环境搭建
e.2，前面对脚本和AiWebConsole进行了调整，没有做全量安装

```

非root需要修改的脚本：

```
1,aischool-app-install目录：
install-activity.sh
install-ccejar.sh
install-office2pdf.sh
random_pwd.sh

2,aischool-install目录：
db_upgrade.sh
install-proxy.sh
install.sh
deluser.sh

3,aischool-install\bin目录：
config-db.sh（删掉cms的部分）
install_monitor.sh
install-cloudzone.sh
install-dls.sh
install-drmportal.sh
install-eshop.sh
install-ftp.sh
install-manager.sh
install-portal.sh
install-presidentReport.sh
install-resserver.sh

4，aischool-install\bin\common目录：
全部 10

5，aischool-install\template目录：
部分放入基础软件包，确认。
ScienceWord.cab、maischool.apk 删掉
dotnetframework.exe 替换版本

6，aischool-install\config
全要，除了：vsftpd-suse.conf
迁移到基础软件包，除了：drm-server.xml、install.cfg、crossdomain.xml

7，aischool-install\cms_smartcampus 删除

8，aischool-install\tools
迁移到基础软件包

9，aischool-install\tomcat
删除多余文件

10，aischool-tw-install删除

11，twgame-install迁移

12，upgrade-tool
authplugin.war
collectclient.war
AiWebConsole.war
集中放置到apache-tomcat-8.5.20的tomcat下，其他去掉
这个工具放到应用安装包，package、python去掉。
collect_cce_start.sh

13，新增目录处理服务检测
checkMemcache.sh
checkhttp.sh
checkOpenOffice.sh

```



