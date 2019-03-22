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

# 打包安装流程

-1，通过脚本zip-all.sh打包安装包（user-install\aischool-install或者aicloud-install\install等目录）

0，安装操作系统(centos6.9\centos7.4) ，安装如下软件：

```shell
a,yum install -y vsftpd dos2unix telnet unizp gcc-c++ csh perl patch nfs-utils rpcbind unzip perl-Module-Install.noarch libXext redhat-lsb
b,政通云openoffice需要安装 yum groupinstall "X Window System"  ，否则openoffice无法启动.
c,升级操作前，请保证/usr/twsm/install/public/install.cfg为777权限，否则升级失败.
d,有的centos7.4版本的fontconfig有问题，无法使用字体配置函数库。这时要重装fontconfig。yum remove fontconfig 后 yum install fontconfig 。
c,yum install -y rng-tools 如果没有安装，会导致随机码生成有问题，从而导致tomcat卡死
```

1，初次使用，登录root账号，进入/usr/twsm。

2，将安装包和reset-all.sh上传到/usr/twsm目录.

3，然后执行/usr/twsm/目录中的reset-all.sh脚本（直接输入sh reset-all.sh，查看命令使用方式。），这一步完成基础软件安装。

```shell
[root@NBACBA5 twsm]# sh reset-all.sh 
命令说明:该命令用于重置安装环境，会先全量卸载，然后全量安装。
reset-all命令格式: sh reset-all.sh version product bureaucode bureauip 
命令参数详情解释:
version : zip包的版本号，例如：CCE-V006R001C06B06SP01B01.zip就取版本号CCE-V006R001C06B06SP01B01 
product : 产品线区分，例如：如果是cce产品线，请输入cce ,若是ecp，则输入ecp
bureaucode : 局点编码，例如：NBACBA2 
bureauip : 局点IP，例如：192.168.131.26 
例子: 
sh reset-all.sh CCE-V006R001C06B06SP01B01 cce NBACBA2 192.168.131.26
```

4，进入http://IP:8080/AiWebConsole 管理平台 安装普通应用。和之前一样，没有变化。这步实际上已经调整到operation账号下完成普通软件安装和执行数据库脚本。

```properties
NOTE，执行完reset-all.sh脚本后，有2点要注意：
a，Aiwebconsole管理平台账号为admin，密码要在/usr/twsm/install/public/install.cfg获取。
b，会生成天闻的一系列账号，以及对应密码。可在/usr/twsm/user-install/log/userpassword.log查看.
```

5，安装完后，即可效验功能。

6，交付以后，禁用root账号的ssh登录功能。

```properties
修改  vi /etc/ssh/sshd_config
将PermitRootLogin yes 修改成 PermitRootLogin no
将AllowUsers root ssh 修改成 AllowUsers operation ssh
保存，重启sshd
/etc/init.d/sshd restart
```

7，交付以后的基础软件升级，通过ssh账号登录，上传要升级的基础软件，通过切换到root账号进行基础软件升级。

8，交付以后的普通应用升级，还是通过http://IP:8080/AiWebConsole 管理平台进行升级。和之前一样。

# 升级流程

1，和以前一样从给定的路径下载高版本的安装包

2，普通应用通过AiWebConsole执行升级安装。

3，基础软件要单独进行软件升级，不提供升级脚本。

```java
/**
	 * 系统升级
	 */
	public void upgrade()  throws UpgradeException
	{
		CmdUtil cmd = new CmdUtil();
		
    	//检查升级包是否正确
    	checkUpgradeFile(cmd, 2);
    	
    	//解压升级包
    	//这一步
    	//1，先备份当前的产品 ：/usr/twsm/aischool-install/upgrade-tool/application_manager.sh backup
    	//2，解压到指定目录 unzip -q twsm -o -P twsm sql.zip -d /usr/twsm/
    	unzipUpgradFile(cmd,4);
    	
    	//安装基础软件
    	//1, /usr/twsm/aischool-install.sh -u
    	//改成了/usr/twsm/aichool-install/install.sh -upgrade
    	upgradeBaseSoftware(cmd, 6);
    	this.initData.init();
    	
    	//升级数据库，执行升级脚本
    	//1，/usr/twsm/aischool-install/db_upgrade.sh
    	//增加数据库用户切换处理 sudo su - twdbuser -c "sh /usr/twsm/aischool-install/db_upgrade.sh"
    	upgradeDB(cmd, 8);
//    	
//    	//升级应用软件
        //1,重启缓存
        //2,/usr/twsm/aischool-install/install.sh -a
    	updateSoftware(cmd, 40);
//    	
//    	//升级应用数据
    	if (WebConstant.SYSTEM_MODEL_PROXY.equals(initData.getDisplayProperties("current_system_mode")))
        {
    		cmd.logProgress(true, 100,"代理服务器升级完成 ");
    		return;
        }
    	upgradeUserData(cmd, 80);
	}
```

# 相关安装脚本的解读

## 公共的脚本

### os-install安装包

```shell
#! /bin/sh
########################################################################################
#  @description:  安全加固设置 ，这个脚本要在batch_create_user_group_acl_sudo.sh脚本执行之后                                                     
#  @author:  lqd	                                                                  #
#  @date:  2019.01.28                 
#  @see： batch_create_user_group_acl_sudo.sh                                           #
########################################################################################

source /usr/twsm/os-setting/bin/readcfg.sh
##sh $ABSOLTEPATH/bin/create_sshchroot.sh
#1，添加口令策略
#新建用户的密码最长使用天数
#新建用户的密码最小长度
#新建用户的密码到期提前提醒天数
sed -i -r 's/(PASS_MAX_DAYS\s+)[0-9]+$/\190/;s/(PASS_MIN_LEN\s+)[0-9]+$/\110/;s/(PASS_WARN_AGE\s+)[0-9]+$/\17/' $PATH_LIGON
#验证：
#chage -l 用户名
#设置连续输错三次密码，账号锁定五分钟
if [[ $(cat $PATH_PAM_SYSTEMAUTH | grep -E  'auth\s+required\s+pam_tally2.so\s+' | wc -l) = 0 ]];then
	sed -i -r '/^#%PAM-1.0$/a\auth        required      pam_tally2.so        deny=3        unlock_time=300        even_deny_root' $PATH_PAM_SYSTEMAUTH
else
	sed -i -r 's/(auth\s+required\s+pam_tally2.so\s+).*/\1deny=3        unlock_time=300        even_deny_root/' $PATH_PAM_SYSTEMAUTH
fi	
if [[ $(cat $PATH_PAM_SSHD | grep -E  'auth\s+required\s+pam_tally2.so\s+' | wc -l) = 0 ]];then
	sed -i -r '/^#%PAM-1.0$/a\auth        required      pam_tally2.so        deny=3        unlock_time=300        even_deny_root' $PATH_PAM_SSHD
else
	sed -i -r 's/(auth\s+required\s+pam_tally2.so\s+).*/\1deny=3        unlock_time=300        even_deny_root/' $PATH_PAM_SYSTEMAUTH
fi
#设置口令复杂度策略，至少10位，必须包括数字、大小写字符和特殊符号，用下面的替换
if [[ $CENTOS_VERSION < 7 ]];then
        if [[ $(cat $PATH_PAM_SYSTEMAUTH | grep -E  'password\s+requisite\s+pam_cracklib.so\s+' | wc -l) != 0 ]];then
		sed -i -r 's/(password\s+requisite\s+pam_cracklib.so\s+).*/\1retry=3  minlen=10 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1/' $PATH_PAM_SYSTEMAUTH
        else
		echo "password        requisite        pam_cracklib.so        retry=3  minlen=10 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1" >>  $PATH_PAM_SYSTEMAUTH
        fi
else
	if [[ $(cat $PATH_PAM_SYSTEMAUTH | grep -E  'password\s+requisite\s+pam_pwquality.so\s+' | wc -l) != 0 ]];then
		sed -i -r 's/(password\s+requisite\s+pam_pwquality.so\s+).*/\1retry=3  minlen=10 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1/' $PATH_PAM_SYSTEMAUTH
        else
		echo "password        requisite        pam_pwquality.so        retry=3 minlen=10 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1" >>  $PATH_PAM_SYSTEMAUTH
        fi
fi	
#验证：
#root无效 --
#当前用户自己修改自己的时候

#2，SSH服务安全
#修改允许密码错误次数为3次（默认6次）
sed -i -r 's/#+MaxAuthTries/MaxAuthTries/;s/(^MaxAuthTries\s+)[0-9]+/\13/' $PATH_SSH_SSHD
#修改SSH端口
sed -i -r 's/#+Port/Port/;s/(^Port\s+)[0-9]+/\18822/' $PATH_SSH_SSHD
#禁用除twssh外的其他登录账号ssh权限
if [ `cat $PATH_SSH_SSHD | grep  -E  "AllowUsers\s+.*" | wc -l` -eq 0 ];then
	echo "AllowUsers twssh">> $PATH_SSH_SSHD
else
	sed -i -r 's/(^AllowUsers\s+).*/\1twssh/' $PATH_SSH_SSHD 	
fi
sed -i -r 's/#PermitRootLogin/PermitRootLogin/;s/(^PermitRootLogin\s+)[A-Za-z]+.*/\1no/' $PATH_SSH_SSHD
#现在SSH登录的IP源(可选)
\cp -fp $ABSOLTEPATH/config/hosts.allow /etc/
\cp -fp $ABSOLTEPATH/config/hosts.deny /etc/

#3，设置登录超时
if [[ $(cat $PATH_PROFILE | grep -E "TMOUT=[0-9]+" | wc -l ) != 0 ]];then
       sed -i -r 's/(^TMOUT=)[0-9]+/\1600/' $PATH_PROFILE
else
       echo "TMOUT=600" >> $PATH_PROFILE	
fi

#4，日志审计，记录所有用户的登录和操作日志
#验证 ： /va/log/下面会产生登录用户的名的文件夹，该文件夹下每次用户退出后都会产生以用户名、登录IP、时间的文件。里面包含此用户本次的所以操作
if [[ $(cat $PATH_PROFILE | grep "$ABSOLTEPATH/bin/os_user_login_log.sh" | wc -l ) = 0 ]]; then
      echo "source $ABSOLTEPATH/bin/os_user_login_log.sh" >> $PATH_PROFILE		
fi

#5，防火墙必须开启，把默认的业务端口都配置进去，注意数据端口不对外开放
#验证：查看端口 more /etc/sysconfig/iptables
if [[ $CENTOS_VERSION < 7 ]];then
	iptables -F
	iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT	
	iptables -A OUTPUT -j ACCEPT
	iptables -A INPUT -j REJECT
	iptables -A FORWARD -j REJECT
else
	systemctl restart firewalld.service	
fi
FIREWALLD_OPEN_PORT_ARRAY=(${FIREWALLD_OPEN_PORTS//,/ })
for port in ${FIREWALLD_OPEN_PORT_ARRAY[@]}
do
    if [[ $CENTOS_VERSION < 7 ]];then
	iptables -I INPUT -p tcp --dport $port -j ACCEPT
    else
	firewall-cmd --permanent --add-port=$port/tcp
    fi	
done

if [[ $CENTOS_VERSION = 7 ]];then
   firewall-cmd --reload
fi

#6，只运行root添加定时任务
\cp -fp $ABSOLTEPATH/config/cron.allow /etc/

#----------------------------linux沙箱-------------------------------------
#twsmssh远程登录账号
#sh $ABSOLTEPATH/bin/create_user_group_acl_sudo.sh -g twsmssh
#\cp -f /etc/passwd $CHROOT_PATH/etc
#\cp -f /etc/group $CHROOT_PATH/etc
#if [ `cat $PATH_SSH_SSHD | grep -o "\s+twsmssh\s+" | wc -l` -eq 0 ];then
#	if [ `cat $PATH_SSH_SSHD | grep "Match User" | wc -l` -eq 0 ];then
#		echo "Match User twsmssh" >> $PATH_SSH_SSHD
#	else
#		sed -i 's/Match User.*/& twsmssh/g' $PATH_SSH_SSHD
#	fi
#fi

source $PATH_PROFILE

if [ $CENTOS_VERSION -lt 7 ] ; then
   service sshd restart
   /etc/init.d/iptables save
   service iptables restart
   chkconfig iptables on
else
   systemctl restart sshd.service
   systemctl restart firewalld.service
   systemctl enable firewalld.service
fi


```

```shell
#! /bin/sh
########################################################################################
#  @description:  用户登录日志审计                                                    
#  @author:  lqd	                                                                  #
#  @date:  2019.01.28                 
#  @see： os_security_setting.sh                                           #
########################################################################################
history
USER=`whoami`
USER_IP=`who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g'`
if [ "$USER_IP" = "" ]; then
    USER_IP=`hostname`
fi
if [ ! -d /var/log/history ]; then
    mkdir /var/log/history
    chmod 777 /var/log/history
fi
if [ ! -d /var/log/history/${LOGNAME} ]; then
    mkdir /var/log/history/${LOGNAME}
    chmod 300 /var/log/history/${LOGNAME}
fi
export HISTSIZE=4096
DT=`date +"%Y%m%d_%H%M%S"`
export HISTFILE="/var/log/history/${LOGNAME}/${USER}_${USER_IP}_$DT"
chmod 600 /var/log/history/${LOGNAME}/*history* 2>/dev/null
```

```shell
#! /bin/sh
########################################################################################
#  描    述:  非root的账号创建  ,不同产品线、不同类型的组以及用户的权限配置,每个默认的组下新建一个同名的默认账号                                                         #
#  修 改 人:  lqd	                                                                  #
#  修改时间:  2018.12.25                                                            #
########################################################################################
ABSOLTEPATH=/usr/twsm/os-setting
INSTALL_LOG=$ABSOLTEPATH/log/os_setting.log
FIREWALLD_OPEN_PORTS=$(cat $ABSOLTEPATH/config/firewalld_open_ports | grep -v "^#" | sed ':a; N; s/\n/,/; t a;')
CENTOS_VERSION=$(rpm -q "centos-release"| cut -d- -f3)

#安全控制文件
PATH_LIGON=/etc/login.defs
PATH_PAM_SYSTEMAUTH=/etc/pam.d/system-auth
PATH_PAM_SSHD=/etc/pam.d/sshd
PATH_SSH_SSHD=/etc/ssh/sshd_config
PATH_PROFILE=/etc/profile
PATH_CENTOS_6_9_IPTABLES=/etc/sysconfig/iptables

```

创建crow.allow、firewalld_open_ports、hosts.allow、hosts.deny配置文件

```shell
crow.allow内容：
root

firewalld_open_ports内容：
###
#开发的端口列表
###
8822
80
9090
5222
5432
8832
1936
8999
8008
7008
8080
8002
8003
8004
8005
8010
8012
8088
11211
3306

hosts.allow内容：
#
# hosts.allow	This file contains access rules which are used to
#		allow or deny connections to network services that
#		either use the tcp_wrappers library or that have been
#		started through a tcp_wrappers-enabled xinetd.
#
#		See 'man 5 hosts_options' and 'man 5 hosts_access'
#		for information on rule syntax.
#		See 'man tcpd' for information on tcp_wrappers
#
sshd:192.168.,10.107.:allow

hosts.deny
#
# hosts.deny	This file contains access rules which are used to
#		deny connections to network services that either use
#		the tcp_wrappers library or that have been
#		started through a tcp_wrappers-enabled xinetd.
#
#		The rules in this file can also be set up in
#		/etc/hosts.allow with a 'deny' option instead.
#
#		See 'man 5 hosts_options' and 'man 5 hosts_access'
#		for information on rule syntax.
#		See 'man tcpd' for information on tcp_wrappers
#
sshd:ALL


```



### user-install安装包

- bin目录

  batch_create_user_group_acl_sudo.sh脚本作用 ：

  > 用于批量新增安装过程中需要的用户和用户组（例如：operation组、operation用户，development组，development用户，test组，test用户，ssh用户，以及其他的普通应用的用户），对用户以及用户组sudo提权，对目录acl控制。

  ```shell
  #! /bin/sh
  ########################################################################################
  #  描    述:  统一批量生成账号脚本                                                         #
  #  修 改 人:  lqd	                                                                  #
  #  修改时间:  2019.01.02                                                            #
  ########################################################################################
  
  source /usr/twsm/user-install/bin/readcfg.sh
  
  #目录权限控制
  directory_acl()
  {
  	mkdir -p /data /usr/twsm/install/ /usr/twsm/$PRODUCTNAME/
  	#data目录对operation组有权限
  	cd / && chown -R operation:operation /data && chmod -R 775 /data
  	cd /usr && chmod 755 twsm/
  	cd /usr/twsm/
  	#user-install目录仅仅对root有权限
  	chmod 700 user-install/
  	#aischool-install目录对operation组有权限
  	chown -R operation:operation /usr/twsm/$PRODUCTNAME/
  	chmod -R 770 /usr/twsm/$PRODUCTNAME/
  	#install目录对twsm账号有权限
  	#chown -R root:root install/ 
  	chmod 755 install/
  }
  
  #ECO目录权限控制
  directory_acl_eco()
  {
  	mkdir -p /data /usr/twsm/tweco-install/install/ /usr/twsm/tweco-install/twpaas-install/ /usr/twsm/tweco-install/twdaas-install/ /usr/twsm/tweco-install/twasp-install/
  	#data目录对operation组有权限
  	cd / && chown -R operation:operation /data && chmod -R 775 /data
  	cd /usr && chmod 755 /usr/twsm/tweco-install
  	cd /usr/twsm/tweco-install
  	#user-install目录仅仅对root有权限
  	chmod 700 user-install/
  	#aischool-install目录对operation组有权限
  	chown -R operation:operation tweco-install/
  	chown -R operation:operation twpaas-install/
  	chown -R operation:operation twdaas-install/	
  	chown -R operation:operation twasp-install/
  	chmod -R 770 twpaas-install/
  	chmod -R 770 twdaas-install/
  	chmod -R 770 twasp-install/
  	#install目录对twsm账号有权限
  	#chown -R twsm:root install/ 
  	chmod 700 install/
  }
  
  if [ $# -ne 1 ];then
    echo "Usage: sh batch_create_user_group_acl_sudo.sh [cce|ecp|eco]"
    exit 1
  fi
  
  echo "初始化系统账号" > $PASSWORD_LOG
  echo "批量添加用户" > $INSTALL_LOG
  
  #用户和用户组的初始化、sudo配置、
  #创建twsm账号：基础软件安装
  #sh $ABSOLTEPATH/bin/create_user_group_acl_sudo.sh -u twsm root
  #echo "创建twsm账号" | tee -a $INSTALL_LOG
  #创建operation及用户组operation：应用软件安装权限
  sh $ABSOLTEPATH/bin/create_user_group_acl_sudo.sh -g operation
  echo "创建operation及用户组operation" | tee -a $INSTALL_LOG
  #ssh及用户组operation：用于远程登录服务器的账号
  sh $ABSOLTEPATH/bin/create_user_group_acl_sudo.sh -u ssh operation
  echo "ssh及用户组operation" | tee -a $INSTALL_LOG 
  #development及用户组development：研发
  sh $ABSOLTEPATH/bin/create_user_group_acl_sudo.sh -g development
  echo "development及用户组development" | tee -a $INSTALL_LOG 
  #test及用户组test
  sh $ABSOLTEPATH/bin/create_user_group_acl_sudo.sh -g test
  echo "test及用户组test" | tee -a $INSTALL_LOG 
  #读取需要统一生成账号的配置文件，生成账号。都放置到operation用户组下
  BATCH_ADD_USERARRAY=(${BATCH_ADD_USERS//,/ })
  for user in ${BATCH_ADD_USERARRAY[@]}
  do
  	sh $ABSOLTEPATH/bin/create_user_group_acl_sudo.sh -u $user operation
  	echo "$user及用户组operation" | tee -a $INSTALL_LOG 
  done
  
  #目录的acl控制
  case $1 in
  cce)
  directory_acl
  echo "cce目录的acl控制" | tee -a $INSTALL_LOG 
  ;;
  ecp)
  directory_acl
  echo "ecp目录的acl控制" | tee -a $INSTALL_LOG 
  ;;
  eco)
  directory_acl_eco
  echo "eco目录的acl控制" | tee -a $INSTALL_LOG 
  ;;
  *)
  echo "没有指定产品线，无法控制目录权限" | tee -a $INSTALL_LOG 
  ;;
  esac
  
  #禁用除ssh\root外的其他登录账号ssh权限
  if [ `cat /etc/ssh/sshd_config | grep "AllowUsers root ssh" | wc -l` -eq 0 ];then
  	echo "AllowUsers root ssh">> /etc/ssh/sshd_config
  	/etc/init.d/sshd restart
  fi
  
  if [ -z "`whereis csh | awk -F ":" '{printf $2}'`" ];then
  	yum install -y csh
  fi
  
  ```

  batch_delete_user_group.sh脚本作用 ：

  > 删除通过batch_create_user_group_acl_sudo生成的用户以及用户组，去掉sudo提权。

  ```shell
  #! /bin/sh
  ########################################################################################
  #  描    述:  统一批量删除账号脚本                                                         #
  #  修 改 人:  lqd	                                                                  #
  #  修改时间:  2019.01.02                                                            #
  ########################################################################################
  
  source /usr/twsm/user-install/bin/readcfg.sh
  
  echo "初始化系统账号" > $PASSWORD_LOG
  echo "批量卸载用户" > $DEL_INSTALL_LOG
  cd /etc/sudoers.d/
  
  BATCH_ADD_USERARRAY=(${BATCH_ADD_USERS//,/ })
  for user in ${BATCH_ADD_USERARRAY[@]}
  do
  	userdel -r $user
  	rm -rf $user
  	rm -rf /home/$user
  	echo "删除$user" | tee -a $DEL_INSTALL_LOG
  done
  
  #用户和用户组的初始化、sudo配置
  #创建twsm账号：基础软件安装
  #userdel -r twsm
  #rm -rf twsm
  #echo "删除twsm" | tee -a $INSTALL_LOG
  #创建operation及用户组operation：应用软件安装权限
  userdel -rf operation
  rm -rf operation
  echo "删除operation" | tee -a $DEL_INSTALL_LOG
  #ssh及用户组operation：用于远程登录服务器的账号
  userdel -r ssh
  rm -rf ssh
  echo "删除ssh" | tee -a $DEL_INSTALL_LOG
  #development及用户组development：研发
  userdel -rf development
  rm -rf development
  echo "删除development" | tee -a $DEL_INSTALL_LOG
  #test及用户组test
  userdel -rf test
  rm -rf test
  echo "删除test" | tee -a $DEL_INSTALL_LOG
  
  
  
  ```

  create_user_group_acl_sudo.sh脚本作用 ：

  > 用于新增单个用户及用户组、用于修改用户及用户组的密码、sudo配置

  ```shell
  #! /bin/sh
  ########################################################################################
  #  描    述:  非root的账号创建  ,不同产品线、不同类型的组以及用户的权限配置,每个默认的组下新建一个同名的默认账号                                                         #
  #  修 改 人:  lqd	                                                                  #
  #  修改时间:  2018.12.25                                                            #
  ########################################################################################
  if [ $# -lt 2 ];then
    echo "Usage: sh create_user_group_acl_sudo.sh [-g groupname|-u username groupname]"
    exit 1
  fi
  
  source /usr/twsm/user-install/bin/readcfg.sh
  
  #-----------------------------用户信息获取处理------------------------
  #
  #用户配置规则有用户的若干项组成如下:
  #---------------------------------------------------
  #用户:用户密码:用户组:用户路径:用户路径的权限设置:用户SHELL
  #username##:0:0:0:0:0
  #
  #除用户名外 其他项的值可以为0，即当前项为空，此时将采用默认方式配置如下：
  #---------------------------------------------------
  #用户密码将随机产生,注意当前密码不能有:字符，否则生成有问题
  #用户组为operation
  #用户路径为/home/用户名
  #用户路径权限为770
  #用户SHELL为/bin/bash
  case $1 in 
  -g)
  	USERNAME=$2
  	GROUPNAME=$2
  ;;
  -u)
  	USERNAME=$2
  	GROUPNAME=$3
  ;;
  *)
  echo "Usage: sh create_user_group_acl_sudo.sh [-g groupname|-u username groupname]"
  exit 1
  ;;
  esac
  USERPASSWORD=`strings /dev/urandom | grep -o '[0-9a-zA-Z_@]' | head -n 8 | tr -d '\n';echo`
  GROUPNAME_UPPER=`echo "$GROUPNAME" | tr '[a-z]' '[A-Z]'`
  USERNAME_UPPER=`echo "$USERNAME" | tr '[a-z]' '[A-Z]' `
  USERPATH=/home/$USERNAME
  USERCHMOD=770
  SHELLSCRIPT=/bin/bash
  
  #若用户扩展的配置文件中有对应的用户信息，则取此用户信息覆盖前面的配置
  USERDETAIL=`cat $USERDETAIL_CONFIG | grep "^$USERNAME[\d\D]*"`
  USERDETAILARRAY=(${USERDETAIL//:/ })
  INDEX=0
  for info in ${USERDETAILARRAY[@]}
  do
      if [ $info != 0 ];then
  		case $INDEX in 
  			0)
  			;;
  			1)
  				#用户密码
  				USERPASSWORD=$info
  			;;
  			2)
  				#用户组
  				GROUPNAME=$info
  			;;
  			3)
  				#用户路径
  				USERPATH=$info
  			;;
  			4)
  				#用户权限
  				USERCHMOD=$info
  			;;
  			5)
  				#用户SHELL
  				SHELLSCRIPT=$info
  			;;
  		esac
  	fi
  	echo $info
  	INDEX=`expr $INDEX + 1`
  done
  #-----------------------------用户信息获取处理-----------------------
  
  #-----------------------------用户信息生成---------------------------
  #创建用户 、用户组
  echo `date +%Y-%m-%d+%H:%M:%S` "create $USERNAME random password!" | tee -a $PASSWORD_LOG
  echo "$USERNAME PASSWORD = $USERPASSWORD" | tee -a $PASSWORD_LOG
  
  group_count=`cat /etc/group | grep -w $GROUPNAME | awk -F '\r' '{print $1}' | awk -F ':' '{print $1}' | grep -w '^'$GROUPNAME'$' | wc -l`
  user_count=`cat /etc/passwd | grep -w $USERNAME | awk -F '\r' '{print $1}' | awk -F ':' '{print $1}' | grep -w '^'$USERNAME'$' | wc -l`
  
  if [ $group_count -eq 0 ];then
      groupadd $GROUPNAME
      echo "create group $GROUPNAME" | tee -a $INSTALL_LOG
  else
      echo "group $GROUPNAME exists" | tee -a $INSTALL_LOG
  fi
  
  if [ $user_count -eq 0 ];then
      useradd -m -d $USERPATH -g $GROUPNAME -s $SHELLSCRIPT $USERNAME && echo $USERPASSWORD | passwd --stdin $USERNAME
      echo "create user $USERNAME" | tee -a $INSTALL_LOG
  else
      echo $USERPASSWORD | passwd --stdin $USERNAME
      echo "$USERNAME exists" | tee -a $INSTALL_LOG
  fi
  
  chmod $USERCHMOD $USERPATH
  
  #-----------------------------用户信息生成---------------------------
  
  #默认配置default ，若配置了自定义的username.config ,则使用自定义的配置
  #SUDO 
  SUDOFILENAME=$USERNAME
  if [ ! -f "$SUDO_CONFIG/$USERNAME" ];then
  	SUDOFILENAME="default"
  fi
  echo "set sudo configuration , use $SUDOFILENAME sudo configure" | tee -a $INSTALL_LOG
  mkdir -p $TMP_CONFIG
  cp -r -f $SUDO_CONFIG/$SUDOFILENAME $TMP_CONFIG/$SUDOFILENAME.bak
  case $1 in
  -g)
  sed -i s/\#GROUPNAME\#/$GROUPNAME/g $TMP_CONFIG/$SUDOFILENAME.bak
  sed -i s/\#GROUPNAME_UPPER\#/$GROUPNAME_UPPER/g $TMP_CONFIG/$SUDOFILENAME.bak
  ;;
  -u)
  sed -i s/\%\#GROUPNAME\#/$USERNAME/g $TMP_CONFIG/$SUDOFILENAME.bak
  sed -i s/\#GROUPNAME_UPPER\#/$USERNAME_UPPER/g $TMP_CONFIG/$SUDOFILENAME.bak
  ;;
  esac
  cp -r -f $TMP_CONFIG/$SUDOFILENAME.bak /etc/sudoers.d/$USERNAME 
  cd /etc/sudoers.d/ && chmod 0440 $USERNAME
  echo "validate sudo configure " | tee -a $INSTALL_LOG
  cd /etc/sudoers.d/ | visudo -c >> $INSTALL_LOG 2>&1
  ```

  readcfg.sh读取配置文件

  ```shell
  #! /bin/sh
  ########################################################################################
  #  描    述:  非root的账号创建  ,不同产品线、不同类型的组以及用户的权限配置,每个默认的组下新建一个同名的默认账号                                                         #
  #  修 改 人:  lqd	                                                                  #
  #  修改时间:  2018.12.25                                                            #
  ########################################################################################
  ABSOLTEPATH=/usr/twsm/user-install
  PASSWORD_LOG=$ABSOLTEPATH/log/userpassword.log
  INSTALL_LOG=$ABSOLTEPATH/log/userinstall.log
  DEL_INSTALL_LOG=$ABSOLTEPATH/log/useruninstall.log
  USERDETAIL_CONFIG=$ABSOLTEPATH/config/user/userdetail
  SUDO_CONFIG=$ABSOLTEPATH/config/sudo
  TMP_CONFIG=$ABSOLTEPATH/tmp
  BATCH_ADD_USERS=`cat $USERDETAIL_CONFIG | grep -v "^#[\d\D]*" | grep -o "^[A-Za-z]*" | sed ':a ; N;s/\n/,/; t a;'`
  PRODUCTABSULOTEPATH=`cat /usr/twsm/install/public/install.cfg | grep "absolutepath"| awk -F '\r' '{ print $1; }' | awk -F "=" '{printf $2}'`
  PRODUCTNAME=`echo $PRODUCTABSULOTEPATH | awk -F '/' '{print $NF}'` 
  
  
  ```

- config目录

  sudo配置文件作用：

  > 用于配置组或者用户的sudo配置。一般使用默认的default配置。覆盖面广，若是需要调整的 ，可以去/etc/sudoers.d/目录下对应的【用户名或者用户组名】文件中修改。
  >
  > 然后，通过 visudo -c 命令检验你的修改是否正确。重新打开新窗口就会生效。
  >
  > note:
  >
  > 可以根据你的用户名命名配置文件，通过调用create_user_group_acl_sudo.sh单独生成这个用户的特殊的sudo配置。

  ```properties
  #
  User_Alias #GROUPNAME_UPPER#_USERS = %#GROUPNAME#
  #
  Cmnd_Alias #GROUPNAME_UPPER#_NETWORKING = /sbin/route, /sbin/ifconfig, /bin/ping, /sbin/dhclient, /usr/bin/net, /sbin/iptables, /usr/bin/rfcomm, /usr/bin/wvdial, /sbin/iwconfig, /sbin/mii-tool, /bin/netstat, /usr/sbin/sshd
  Cmnd_Alias #GROUPNAME_UPPER#_SOFTWARE = /bin/rpm, /usr/bin/up2date, /usr/bin/yum, /bin/sed, /usr/bin/tee, /bin/rm, /bin/chmod, /usr/bin/dos2unix, /bin/find, /bin/mkdir, /usr/sbin/usermod, /usr/bin/passwd, /usr/sbin/vsftpd 
  Cmnd_Alias #GROUPNAME_UPPER#_SERVICES = /sbin/service, /usr/bin/systemctl, /sbin/chkconfig, /bin/su, /bin/kill, /bin/cp, !/bin/su root, !/bin/su - root
  #
  #GROUPNAME_UPPER#_USERS ALL = (ALL)NOPASSWD: #GROUPNAME_UPPER#_NETWORKING, #GROUPNAME_UPPER#_SOFTWARE, #GROUPNAME_UPPER#_SERVICES
  
  ```

  user目录下的配置文件作用：

  > 用于配置你需要额外添加的用户，统一新增到operation用户组下。

  ```properties
  #
  #用户配置规则有用户的若干项组成如下:
  #---------------------------------------------------
  #用户名:用户密码:用户组:用户路径:用户路径的权限设置:用户SHELL
  #username:0:0:0:0:0
  #
  #除用户名外 其他项的值可以为0，即当前项为空，此时将采用默认方式配置如下：
  #---------------------------------------------------
  #用户密码将随机产生,注意当前密码不能有:字符，否则生成有问题
  #用户组为operation
  #用户路径为/home/用户名
  #用户路径权限为770
  #用户SHELL为/bin/bash
  
  openfire:0:0:0:0:/bin/csh
  portal:0:0:0:0:/bin/csh
  eshop:0:0:0:0:/bin/csh
  drmportal:0:0:0:0:/bin/csh
  resserver:0:0:0:0:/bin/csh
  cloudzone:0:0:0:0:/bin/csh
  manager:0:0:0:0:/bin/csh
  dls:0:0:0:0:/bin/csh
  activity:0:0:0:0:/bin/csh
  presidentReport:0:0:0:0:/bin/csh
  contentftp:contentftp:operation:/data/contentftp:0:/bin/csh
  ```

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


- 安装zip命令，否则游戏模块的脚本执行有问题。

  ```shell
  yum install -y zip
  ```

- centos7安装

  ```
  /usr/jdk1.8.0_102/jre/bin/java: symbol lookup error: /lib64/libfontconfig.so.1: undefined symbol: FT_Get_Advance
  ```

- sudo: effective uid is not 0, is sudo installed setuid root

  ```shell
  证明/usr/bin/sudo文件没有设置s权限（用户在执行文件的时候，临时拥有文件所有者的权限。）
  解决方法：
  chmod u+s /usr/bin/sudo
  ```

- 用户删除不了

  ```shell
  [root@NBACBA5 user-install]# sh bin/batch_delete_user_group.sh 
  userdel: user openfire is currently used by process 11393
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

## 2019.01.28

> ```properties
> 1、添加口令策略
> vi /etc/login.defs
> PASS_MAX_DAYS 90 #新建用户的密码最长使用天数
> PASS_MIN_LEN 10   #新建用户的密码最小长度
> PASS_WARN_AGE 7  #新建用户的密码到期提前提醒天数
> 
> 2、设置连续输错三次密码，账号锁定五分钟
> vi /etc/pam.d/system-auth
> vi /etc/pam.d/sshd
> 添加到 #%PAM-1.0 下面
> auth        required      pam_tally2.so        deny=3        unlock_time=300        even_deny_root
> 
> 3、设置口令复杂度策略，至少10位，必须包括数字字符和特殊符号，用下面的替换
> CentOS 6
> vi /etc/pam.d/system-auth
> password    requisite     pam_cracklib.so retry=3  minlen=10 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1
> 
> CentOS 7
> vi /etc/pam.d/system-auth
> password    requisite     pam_pwquality.so retry=3 minlen=10 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1
> 
> 4、SSH服务安全
> Xxxxxxxx不允许root账号直接登录系统
> PermitRootLogin no
> 
> Xxxxxxxx只允许管理员账号operation远程登录系统
> AllowUsers operation
> 
> 修改允许密码错误次数（默认6次）
> MaxAuthTries 3
> 
> 修改SSH端口
> sed -i 's/#Port 22/Port 8822/g' /etc/ssh/sshd_config
> 
> 5、设置登录超时
> 设置系统登录后，连接超时时间，增强安全性
> vi /etc/profile
> TMOUT=600
> 
> 6、日志审计，记录所有用户的登录和操作日志
> 通过脚本代码实现记录所以用户的登录操作日志，防止出现安全事件后无据可查。
> vi /etc/profile
> 在配置文件中追加以下内容：
> history
> USER=`whoami`
> USER_IP=`who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g'`
> if [ "$USER_IP" = "" ]; then
>     USER_IP=`hostname`
> fi
> if [ ! -d /var/log/history ]; then
>     mkdir /var/log/history
>     chmod 777 /var/log/history
> fi
> if [ ! -d /var/log/history/${LOGNAME} ]; then
>     mkdir /var/log/history/${LOGNAME}
>     chmod 300 /var/log/history/${LOGNAME}
> fi
> export HISTSIZE=4096
> DT=`date +"%Y%m%d_%H%M%S"`
> export HISTFILE="/var/log/history/${LOGNAME}/${USER}_${USER_IP}_$DT"
> chmod 600 /var/log/history/${LOGNAME}/*history* 2>/dev/null
> 
> 7、防火墙必须开启，把默认的业务端口都配置进去，注意数据端口不对外开放
> CentOS 6 可配置文件/etc/sysconfig/iptables
> chkconfig iptables on
> service restart iptables
> 
> CentOS 7 示例
> firewall-cmd --permanent --add-port=8832/tcp
> systemctl restart firewalld.service
> systemctl enable firewalld.service
> 
> 8、只运行root添加定时任务
> touch /etc/cron.allow
> 
> 9、现在SSH登录的IP源(可选)
> vi /etc/hosts.allow
> sshd:192.168.,10.107.:allow
> ```

