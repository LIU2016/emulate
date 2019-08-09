现象 -- loadrunner出现大量的失败事务和error，说明连接数太少了。需要调整nginx和linux参数

socket

- nginx
  - 子进程允许打开的连接(work_connections)
- 系统层面
  - 最大连接数 somaxconn
  - 加快tcp连接的回收 recycle
  - 空的tcp是否允许回收利用 reuse
  - 洪水攻击 不做洪水抵御

文件

- nginx
  - 子进程允许打开的文件（worker_rlimit_nofiles）
    Changes the limit on the largest size of a core file (RLIMIT_CORE) for worker processes. Used to increase the limit without restarting the main process.
    Syntax:worker_rlimit_nofile number;
    Default:—Context:main
- 系统
  - ulimit -n （-a 查看 | -n 修改）

实战

![img](https://img.mubu.com/document_image/e711ae52-b47a-43c7-b547-17ec7de0b0c6-862021.jpg)

![img](https://img.mubu.com/document_image/57fc238c-3ddb-431e-aab3-94b01687fa20-862021.jpg)

ulimit -n 655555

```
正确的修改方式是修改/etc/security/limits.d/90-nproc.conf文件中的值。先看一下这个文件包含什么：

$ cat /etc/security/limits.d/90-nproc.conf 
# Default limit for number of user's processes to prevent
# accidental fork bombs.
# See rhbz #432903 for reasoning.

*          soft    nproc    4096
我们只要修改上面文件中的4096这个值，即可。

------------------------------------------

有时候在程序里面需要打开多个文件，进行分析，系统一般默认数量是1024，（用ulimit -a可以看到）对于正常使用是够了，但是对于程序来讲，就太少了。
修改2个文件。
1) /etc/security/limits.conf
vi /etc/security/limits.conf
加上：
* soft nofile 8192
* hard nofile 20480

不用重启
```

echo 50000 > /proc/sys/net/core/somaxconn 
echo 1> /proc/sys/net/ipv4/tcp_tw_recycle 
echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle 
cat /proc/sys/net/ipv4/tcp_tw_reuse
cat /proc/sys/net/ipv4/tcp_syncookies





