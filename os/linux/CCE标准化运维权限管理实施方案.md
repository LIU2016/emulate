[TOC]

# 背景

当前我们公司里服务器很多的时候，各个服务器上的管理人员很多(开发+运维+架构+DBA+产品+市场)，在大家登录使用Linux服务器时，不同职能的员工水平不同，因此导致操作很不规范，root权限泛滥(几乎大多数人员都有root权限),经常导致文件等莫名其妙的丢失，老手和新手员工对服务器的熟知度也不同，这样使得公司服务器安全存在很大的不稳定性，及操作安全隐患，据调查企业服务器环境，50%以上的安全问题都来自内部，而不是外部。为了解决以上问题，单个用户管理权限过大现状，现提出针对Linux服务器用户权限集中管理的解决方案。

我们既希望超级用户root密码掌握在少数或唯一的管理员手中，又希望多个系统管理员或相关有权限的人员，能够完成更多更复杂的自身职能相关的工作，又不至于越权操作导致系统安全隐患。

那么，如何解决多个系统管理员都能管理系统而又不让超级权限泛滥的需求呢?这就需要sudo管理来代替或结合su 命令来完成这样的苛刻且必要的企业服务器用户管理需求。

# 用户权限分配

## 一、有用户以及用户组

```properties
root及用户组root：超级管理员，主要用于创建账号、账号授权
#twsm及用户组root: 基础软件安装 db建议：第三方安全公司一般都会检查这点的，为0的必须只给root
operation及用户组operation：应用软件安装权限  
ssh及用户组operation：用于远程登录服务器的账号
development及用户组development：研发
test及用户组test：测试
```

## 二、添加用户以及组、权限配置

权限控制目前大致从以下四个部分调整：

### 用户及用户组新增

在root用户下，新建高级运维账号、普通运维组以及供远程登录的ssh账号、开发组、测试组。

- #高级运维人员（twsm）db建议：第三方安全公司一般都会检查这点的，为0的必须只给root

  #分别到root用户组，并修改/etc/passwd：（将twsm的uid修改为0，提root权限）。若后期解决了基础软件#的非root权限安装问题，可以修改该账户的权限。

  ```properties
  twsm:x:0:0::/home/-u:/bin/csh
  development:x:503:502::/home/-g:/bin/csh
  ```

- 运维组（operation）

  - 远程登录账号（ssh）

    该组是用来远程登录的。所有的账号不允许远程登录到服务器，只有通过该组下的账号登录服务器后，通过su命令跳转到其他的用户组。

  - 其他运维账号权限根据维优的要求收集调整。

- 开发组（development）

  - 权限根据开发人员的要求收集调整。

- 测试组（test）

  - 权限根据测试人员的要求收集调整。

这里的账号新建以及权限配置，将提供统一的用户及用户组模板生成脚本（user-install.zip）。

### sudo权限配置

默认的sudo权限配置模板（使用twsm用户）（note:这里的只是目前收集到的权限，后面可以根据不同场景服务器的要求新增或者屏蔽权限）：

| 角色\|模块    | 网络                                                         | 软件                                                         | 服务                           | 数据库                                                       | 日志 |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------ | ------------------------------------------------------------ | ---- |
| twsm用户      | /sbin/route, /sbin/ifconfig, /bin/ping, /sbin/dhclient, /usr/bin/net, /sbin/iptables, /usr/bin/rfcomm, /usr/bin/wvdial, /sbin/iwconfig, /sbin/mii-tool | /bin/rpm, /usr/bin/up2date, /usr/bin/yum, /bin/sed, /usr/bin/tee, /bin/rm, /bin/chmod, /usr/bin/dos2unix, /bin/find, /bin/mkdir, /usr/bin/killall java | /sbin/service, /sbin/chkconfig | /usr/bin/killall twdbuser, /bin/rm -rf /opt/PostgreSQL /etc/init.d/twsm /etc/postgres-reg.ini, /usr/sbin/userdel twdbuser |      |
| operation组   |                                                              |                                                              |                                |                                                              |      |
| development组 |                                                              |                                                              |                                |                                                              |      |
| test          |                                                              |                                                              |                                |                                                              |      |
| ssh           |                                                              |                                                              |                                |                                                              |      |

### ACL权限配置

对于这块，twsm账号根据目前已有的脚本对目录权限进行调整。

例如：cce产品中的/usr/twsm目录对测试、开发组的账号是没有w权限的。这个目录下的软件安装目录（usr/twm/install）只能对twsm这个账号有权限。普通应用安装包只能对operation这个组有权限。如下：

![1](C:\Users\lqd\Desktop\非root\1.png)

### Alias别名定义

```shell
chmod	sudo /bin/chmod
dos2unix	sudo /usr/bin/dos2unix
l.	ls -d .* --color=auto
ll	ls -l --color=auto
ls	ls --color=auto
rm	sudo /bin/rm
sed	sudo /bin/sed
tee	sudo /usr/bin/tee
userdel	sudo /usr/sbin/userdel
```

```properties
note：
非交互式的shell脚本不能使用别名。

参考：
https://unix.stackexchange.com/questions/1496/why-doesnt-my-bash-script-recognize-aliases#comment320110_1498

First of all, as ddeimeke said, aliases by default are not expanded in non-interactive shells.

Second, .bashrc is not read by non-interactive shells unless you set the BASH_ENV environment variable.

But most importantly: don't do that! Please? One day you will move that script somewhere where the necessary aliases are not set and it will break again.

Instead set and use environment variables as shortcuts in your script:

#!/bin/bash

CMDA=/path/to/gizmo
CMDB=/path/to/huzzah.sh

for file in "$@"
do
    $CMDA "$file"
    $CMDB "$file"
done
```

## 三、维护

- 不是特别紧急的需求，一律走申请流程用户。这个流程的制定需要大家一起确定。

- 服务器多了，可以通过分发软件批量分发/etc/sudoers(注意权限和语法检查)。

- 除了权限上的控制，**在账户有效时间上**也进行了限制，现在线上多数用户的权限为永久权限可以使用以下方式进行时间上的控制，这样才能让安全最大化。

### Sudo配置注意事项

> 1) 命令别名下的成员必须是文件或目录的绝对路径。
>
> 2) 别名名称是包含大写字母、数字、下划线，如果是字母都要大写。
>
> 3) 一个别名下有多个成员，成员与成员之间，通过半角”,” 号分隔；成员必须是有效实际存在的。
>
> 4) 别名成员受别名类型 Host_Alias、User_Alias、Runas_Alias、Cmnd_Alias制约，定义什么类型的别名，就要有什么类型的成员相匹配。
>
> 5) 别名规则是每行算一个规则，如果一个别名规则一行容不下时，可以通过”\”来续行。
>
> 6) 指定切换的用户要用()括号括起来。如果省略括号，则默认root用户;如果括号里是ALL,则代表能切换到所有用户;
>
> 7) 如果不需要密码直接运行命令的，应该加NOPASSWD:参数。
>
> 8) 禁止某类程序或命令执行，要在命令动作前面加上”!”号，并且放在允许执行命令的后面。
>
> 9) 用户组前面必须加%号。

# 用户日志审计

所谓日志审计，就是记录所有系统及相关用户行为的信息，并且可以自动分析、处理、展示(包括文本或者录像)。

这里采用sudo日志审计：专门使用sudo命令的系统用户来记录其执行的命令相关信息。

- 安装sudo命令，syslog服务

```shell
[root@root twsm]# rpm -qa|egrep "sudo|syslog"
```

如果没有安装则执行下面的命令安装:

```shell
[root@root twsm]# 
```

- 配置/etc/sudoers

增加配置”Defaults   logfile=/var/log/sudo.log”到/etc/sudoers中.

```shell
[root@root twsm]# visudo -c  #——>检查sudoers文件语法
/etc/sudoers: parsed OK
/etc/sudoers.d/90-cloud-init-users: parsed OK
/etc/sudoers.d/aiclass: parsed OK
/etc/sudoers.d/development: parsed OK
/etc/sudoers.d/operation: parsed OK
/etc/sudoers.d/twsm: parsed OK
```

- 配置系统日志文件/etc/rsyslog.conf

增加配置”local2.debug     /var/log/sudo.log”到/etc/rsyslog.conf中，并重启syslog内核日志记录器.

```shell
[root@root twsm]# vi /etc/rsyslog.conf 
[root@root twsm]# /etc/init.d/rsyslog restart
Shutting down system logger:                               [  OK  ]
Starting system logger:                                    [  OK  ]
```

此时，会自动建立一个/var/log/sudo.log文件(日志中配置的名字)并且文件权限为600，所有者和组均为root(如果看不见日志文件，就退出重新登录看看)。接下来可以通过用户操作sudo，查看/var/log/sudo.log文件的日志记录。

```shell
[root@root log]# cat sudo.log 
Dec 28 09:42:47 : operation : TTY=pts/0 ; PWD=/home/operation ; USER=root ;
    COMMAND=/bin/ping 192.168.102.112
```

# 整体流程规划

整个调整分以下几步：

1，用户及用户组规划、用户权限的规划。

2，脚本中涉及到的目录和用户目录ACL权限的规划。

3，安装脚本的修改以及瘦身。

4，因为脚本的修改导致的应用修改，例如：AiWebConsole。

5，整个产品在centos6.9\7.4\7.5下面的验证。

6，制定后期维护使用手册。

# 安装流程

1，安装操作系统(centos6.9\centos7.4)

2，初次使用，登录root账号，创建/usr/twsm /usr/twsm/user-install/等目录，上传user-install脚本。

3，执行user-install目录下的batch_create_user_group_acl_sudo.sh脚本创建账号、并相应赋权、创建必要目录以及目录控制。

4，交付后，禁用root账号的ssh登录功能。

5，通过ssh账号登录，上传install、aischool-install安装包。

6，通过ssh账号切换到root账号，进行基础软件安装。

- 安装数据库

  ```shell
  [root@root install]# pwd
  /usr/twsm/install
  [root@root install]# sh install.sh -d
  ```

7，通过ssh账号切换到operation账号，进行普通应用安装。

- 刷CCE应用脚本

  ```shell
  [operation@NBACBA2 aischool-install]$ pwd
  /usr/twsm/aischool-install
  [operation@NBACBA2 aischool-install]$ sh install.sh -db
  ```

- 安装应用

- 

8，应用管理平台

http://192.168.131.26:9122/AiWebConsole

# 相关安装脚本的解读

## 公共的脚本

### user-install安装包

- bin目录

  batch_create_user_group_acl_sudo.sh脚本作用 ：

  > 用于批量新增安装过程中需要的用户和用户组（例如：operation组、operation用户，development组，development用户，test组，test用户，ssh用户，以及其他的普通应用的用户），对用户以及用户组sudo提权，对目录acl控制。

  batch_delete_user_group.sh脚本作用 ：

  > 删除通过batch_create_user_group_acl_sudo生成的用户以及用户组，去掉sudo提权。

  create_user_group_acl_sudo.sh脚本作用 ：

  > 用于新增单个用户及用户组、用于修改用户及用户组的密码、sudo配置

- config目录

  sudo配置文件作用：

  > 用于配置组或者用户的sudo配置。一般使用默认的default配置。覆盖面广，若是需要调整的 ，可以去/etc/sudoers.d/目录下对应的【用户名或者用户组名】文件中修改。
  >
  > 然后，通过 visudo -c 命令检验你的修改是否正确。重新打开新窗口就会生效。
  >
  > note:
  >
  > 可以根据你的用户名命名配置文件，通过调用create_user_group_acl_sudo.sh单独生成这个用户的特殊的sudo配置。

  user目录下的配置文件作用：

  > 用于配置你需要额外添加的用户，统一新增到operation用户组下。

- log目录

  userpassword作用：

  > 生成了用户及密码对应关系的日志记录。重点这里有用户密码。重点这里有用户密码。重点这里有用户密码。

## cce脚本

### install安装包

### aischool-install安装包

## ecp脚本

## eco脚本

# 安装过程遇到的问题记录

- /etc/vsftpd/目录权限对当前安装用户开放

  ```shell
  [root@root aischool-install]# chown -R operation:operation /etc/vsftpd/ /usr/lib/
  [root@root vsftpd]# chmod -R 775 /etc/vsftpd/ /usr/lib/
  ```

- vsftpd非root下不能启动

  ```shell
  关闭 vsftpd：                                              [失败]
  为 vsftpd 启动 vsftpd：500 OOPS: vsftpd: must be started as root (see run_as_launching_user option)
                                                             [失败]
  ```

- operation账号下contentftp 切换账号失败

  ```shell
  [operation@root aischool-install]$  sudo passwd -d contentftp
  [sudo] password for operation: 
  ```

  su在普通用户之间的切换

  通过su可以在用户之间切换，如果超级权限用户root向普通或虚拟用户切换不需要密码，而普通用户切换到其它任何用户都需要密码验证。

  ```shell
  su - openfire -c "restart"
  ```

  怎么解决这个问题？

  临时解决办法，将operation加入到wheel组，如下修改pam配置：

  （风险点：operation会无密切换到root的，解决办法能否通过指定组，组内能无密码切换。

  参考：https://www.tecmint.com/configure-pam-in-centos-ubuntu-linux/）

  ```shell
  [root@root twsm]# vi /etc/pam.d/su
  
  将 auth这一列的注释号 去除
  # Uncomment the following line to implicitly trust users in the "wheel" group.
  auth            sufficient      pam_wheel.so trust use_uid
  然后将登陆用户加入 wheel组
  [root@root twsm]# usermod -G wheel operation
  ```

- chown的权限限制--普通用户无法将owner改成其他用户,如root

   Linux/Unix 是多人多工作业系统，所有的档案皆有拥有者。利用 chown 可以将档案的拥有者加以改变。一般来说，这个指令只有是由系统管理者(root)所使用，一般使用者没有权限可以改变别人的档案拥有者，也没有权限可以将自己的档案拥有者改设为别人。只有系统管理者(root)才有这样的权限。

  ```shell
  [operation@root aischool-install]$ chown ssh:operation progress.txt 
  chown: 正在更改"progress.txt" 的所有者: 不允许的操作
  [operation@root aischool-install]$ sudo chown ssh:operation progress.txt 
  [sudo] password for operation: 
  对不起，用户 operation 无权以 root 的身份在 root.novalocal 上执行 /bin/chown ssh:operation progress.txt。
  ```

- /tmp目录必须设置为root用户组，不然数据库安装后卸载有问题，会导致再次安装不了。

  ```shell
  WARNING --> PERL_INSTALL_PATH is not set in /opt/PostgreSQL/10/etc/sysconfig/plLanguages.config file
  WARNING --> PYTHON_INSTALL_PATH is not set in /opt/PostgreSQL/10/etc/sysconfig/plLanguages.config file
  WARNING --> TCL_INSTALL_PATH is not set in /opt/PostgreSQL/10/etc/sysconfig/plLanguages.config file
  2019-01-05 12:31:13.277 CST [12027] LOG:  listening on IPv4 address "0.0.0.0", port 8832
  2019-01-05 12:31:13.277 CST [12027] LOG:  listening on IPv6 address "::", port 8832
  2019-01-05 12:31:13.285 CST [12027] FATAL:  could not remove old lock file "/tmp/.s.PGSQL.8832.lock": 不允许的操作
  2019-01-05 12:31:13.285 CST [12027] HINT:  The file seems accidentally left over, but it could not be removed. Please remove the file by hand and try again.
  2019-01-05 12:31:13.285 CST [12027] LOG:  database system is shut down
  
  ```

- 数据执行脚本要添加参数 ，不然执行不了。如下（必须加上-W -h -p -d -U）：

  ```shell
   $pghome/bin/psql -W $airead_dbpasswd -p $db_port -h $host -qAtX -f /usr/twsm/aischool-install/sql/airead/03_init_system.sql -U $airead_dbuser -d $airead_dbname -L /usr/twsm/aischool-install/log/03_init_system_airead.log
  ```

- 

# 会议记录

## 2018.12.27 

2018.12.27会议统计出来的问题以及解决办法：

- 硬件要求
- 

| 操作系统 | 版本    |
| -------- | ------- |
| centos   | 6.9,7.4 |

假若 可用空间 2T ，磁盘分配可用建议：

| 目录      | 分配比例         |
| --------- | ---------------- |
| /         | 10% （200G以上） |
| /usr/twsm | 2.5%             |
| /opt      | 25% (500G)       |
| /data     |                  |

-  /data/contentftp 目录 的ACL权限分配问题

```properties
dls权限：770， 其他的chmod 目录权限控制修改
```

- 二进制文件（例如postgres、mysql的基础软件安装）需要root安装权限 （cce开发）

```properties
基础软件安装和应用 安装分开,在twsm的权限下，
先提前安装好基础软件。
其次，新建普通应用安装账号。
```

- 不同产品线各种账号的sudo权限问题（测试、开发、维优、）

```properties
先列出一个基础的sudo.config/
适配操作系统：centos6、centos7.4
```

- 读取证书的命令权限

```properties
添加命令到sudo、修改别名
```

- linux 下的定时任务 - crontab的账号分配

```shell
30 0 * * * /db_backup/scripts/auto_backup.sh >> /db_backup/log/backup.log 2>/dev/null （twsmdbuser账号下）
0 3 * * 0 /db_backup/scripts/maintain_db.sh >> /db_backup/log/maintain_db.log 2>/dev/null（twsmdbuser账号下）
0 23 * * * /usr/sbin/ntpdate asia.pool.ntp.org >/dev/null && /sbin/hwclock --systohc >/dev/null （root账号下）
0 4 * * * /db_backup/scripts/function.sh >/dev/null 2>/dev/null（twsmdbuser账号下）
0 18 * * * /db_backup/scripts/function_18.sh >/dev/null 2>/dev/null（twsmdbuser账号下）
*/5 * * * * /usr/twsm/install/kill_Daemon_Perl.sh > /dev/null （删除）
59 23 * * * /db_backup/scripts/log_clean.sh >/dev/null 2>/dev/null（非root账号下）
```

- nginx软件安装的默认目录以及脚本需要调整。

- 普通应用安装脚本中的数据库的配置需要调整。

- AiWebConsole一键安装需要调整。

- 产品版本升级

  ```properties
  a.基础软件安装升级单独处理。 -- 开发、维优处理
  b.应用安装升级兼容root和非root安装
  c.root升级到非root安装的手册
  ```

## 2018.12.29

安装脚本整理以及拆分，分两部分：基础软件安装、普通应用安装。

本次调整只涉及到CCE的标准单校安装，安装目录以后就剩2个：install、aischool-install 。

```properties
a,基础软件安装：
在twsm账号下进行安装，安装目录及脚本做如下处理：
1,将nginx的安装迁移到普通应用安装包里，其他的保留。 不处理
2,install.sh脚本做修改。
3,aischool-install.sh脚本迁移到基础软件安装包。

b,普通应用安装：
在operation账号下进行安装，去掉冗余文件，CCE整个普通应用安装目录及脚本做如下拆分：
1,aischool-app-install目录保留以下脚本：
install-activity.sh
install-ccejar.sh
install-office2pdf.sh
random_pwd.sh
上述脚本迁移到aischool-install目录，去掉aischool-app-install目录。

2,aischool-install目录保留脚本：
db_upgrade.sh
install-proxy.sh
install.sh
deluser.sh

3,aischool-install\bin目录保留以下脚本：
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
上述的关于安装war包的脚本合并成一个脚本，且调整调用的shell脚本代码。

4，aischool-install\bin\common目录保留以下脚本：
function.sh
copytomcat.sh
random_pwd.sh
auto_backup.sh
maintain_db.sh
createuser.sh
function_18.sh
log_clean.sh
readcfg.sh
replace.sh

5，aischool-install\template目录：
ScienceWord.cab、maischool.apk 删掉
dotnetframework.exe 替换版本
将保留目录迁移到基础软件包。

6，aischool-install\config
除了：vsftpd-suse.conf，全部保留，除了：drm-server.xml、install.cfg、crossdomain.xml，都迁移到基础软件包

7，aischool-install\cms_smartcampus 删除

8，aischool-install\tools
迁移到基础软件包

9，aischool-install\tomcat
删除多余文件

10，twgame-install\目录迁移到应用安装目录aischool-install中，调整脚本。

11，upgrade-tool
将authplugin.war、collectclient.war、AiWebConsole.war集中放置到apache-tomcat-8.5.20的tomcat下，其他去掉。
这个工具放到应用安装包aischool-install目录中，package、python去掉。
修改collect_cce_start.sh、upgradetool.sh逻辑。

12，在基础软件包下，新增check目录处理服务检测，迁移以下脚本到此目录：
checkMemcache.sh
checkhttp.sh
checkOpenOffice.sh
```

