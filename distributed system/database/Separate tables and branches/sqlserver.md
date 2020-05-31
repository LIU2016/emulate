版本：

sqlserver2005之前(拆开了(数据库工具和查询分析器)

sqlserver2005-sqlserver2014(数据库工具和查询分析器合并)

sqlserver2017(数据库工具和查询分析器拆开/深度学习)



安装：

1，下载Sqlserver：

http://download.microsoft.com/download/E/B/7/EB70F1CF-2076-49A8-A648-9436D2E0E09F/SQLServer2014SP3-FullSlipstream-x64-CHS.box

http://download.microsoft.com/download/E/B/7/EB70F1CF-2076-49A8-A648-9436D2E0E09F/SQLServer2014SP3-FullSlipstream-x64-CHS.exe

2，密钥：27HMJ-GH7P9-X2TTB-WPHQC-RG79R

（<https://blog.csdn.net/bwzhang93/article/details/79014978>）

3，采用混合模式，有添加当前用户的地方添加即可，然后点下一步。

4，Sqlserver Dos命令操作：

```
net stop mssqlserver：关闭sqlserver服务
net start mssqlserver：开启sqlserver服务
Osql -S 服务器名称（ip,1433/域名/./localhost） -U sa -P 123456 
----------基本操作
use db
go
select * from table;
go
delete from table;
go
```

5，配置

```
1，安全性
登录名：强制密码去掉、sysadmin权限最大、用户映射（）、状态（启用）、还可以创建新的账号
若是windows模式登录的请修改右键sqlserver修改模式，再重新登陆。
2，若是客户端只需要安装sqlserver管理工具。
3，打开sqlserver managerment studio，查看 
```

6，分离、附加、备份、还原

```
1，删除数据库的时候，右键分离，删除连接勾选，删除对应的文件即可。
2，附加数据库的时候，右键附加即可。
3，备份
4，还原
```

7，T-SQL