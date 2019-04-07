```c
[root@localhost server]# gcc echo_server.c -o echo_server
echo_server.c: In function ‘errormsg’:
echo_server.c:15:5: warning: incompatible implicit declaration of built-in function ‘exit’ [enabled by default]
     exit(1);

少了stdlib.h

直接通过man 命令查看就可以了
查看[root@localhost server]# man perror 命令依赖的头文件

```

