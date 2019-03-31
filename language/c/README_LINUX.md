# Linux服务器开发

## 搭建开发环境

### 安装samba服务器

[参考文档](https://blog.csdn.net/learner198461/article/details/77651949)

``` properties
安装：
yum install -y samba samba-common

添加/etc/samba/smb.conf的配置且新建lqd账号：
[share]
       comment = this is samba dir
       path = /home/lqd/share
       writable = yes
       browseable = yes

添加用户[root账号下面执行]：
sudo smbpasswd -a lqd
sudo smbpasswd -a root
setsebool -P samba_enable_home_dirs 1

启动：
systemctl start smb.service

```

## 入门必备命令

## 开启linux编程之旅

```
只编译执行一个C程序
$ gcc hello.c                                                                     
$ ./a.out                                                                         
$Hello world!                                                                    

默认的a.out 并不友好，gcc 提供 -o 选项指定执行文件的文件名：
$gcc -o hello  hello.c       ##编译源代码，并把可执行文件命名为 hello                
$Hello world!                                                                     

编译C++程序，我们可以直接用GCC 编译其中的g++命令，用法同 gcc；当然g++ 和 gcc 都可以用来编译 c 和 c++程序。gcc 编译c++程序需要带上 -lstdc++  指定使用c++库。
```

### **编译常用选项**

| 选   项 | 功   能                                          |
| ------- | ------------------------------------------------ |
| -c      | 只激活预处理、编译和汇编,生成.o 目标代码文件     |
| -S      | 只激活预处理和编译，生成扩展名为.s的汇编代码文件 |
| -E      | 只激活预处理，并将结果输出至标准输出             |
| -g      | 为调试程序(如gdb)生成相关信息                    |
| -O      | 等同-O1,常用的编译优化选项                       |
| -Wall   | 打开一些很有用的警告选项，建议编译时加此选项。   |

注意：-c 选项在编写大型程序是必须的，多个文件的源代码首先需要编译成目标代码，再链接成执行文件。如果由多个源文件，工程做法建议采用 makefile 。

## 网络服务器开发

### 回声服务器实例

#### 服务器端

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>
#include <ctype.h>
#include <arpa/inet.h>

#define SERVER_PORT 666

int main(void){

    int sock;
    int i;

    struct sockaddr_in server_addr;
    sock = socket(AF_INET, SOCK_STREAM, 0);
    	
    bzero(&server_addr,sizeof(server_addr));

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(SERVER_PORT);

    bind(sock, (struct sockaddr *)&server_addr, sizeof(server_addr));

    listen(sock, 128);

    printf("等待客户端连接:\n"); 

    int done =1 ;

    while(done)
    {
        struct sockaddr_in client;
        int client_sock,len;
        char client_ip[64];
        char buf[256];

        socklen_t client_addr_len;
        client_addr_len = sizeof(client);
   	    client_sock = accept(sock,(struct sockaddr *)&client,&client_addr_len);
          
        printf("client ip:%s \t port: %d \n",
               inet_ntop(AF_INET,&client.sin_addr.s_addr,client_ip,sizeof(client_ip)),
	           ntohs(client.sin_port));

        len=read(client_sock,buf,sizeof(buf)-1);

        buf[len]='\0';
        printf("recive[%d]:%s\n",len,buf);

      /*  len=write(client_sock,buf,len);
        printf("write finished. len: %d\n", len);*/

       /* for(i=0;i<len;i++)
        {
            if (buf[i]>='a' && buf[i]<='z') buf[i]=buf[i]-32;
        }*/

        for (i=0;i<len;i++)
        {
            buf[i]=toupper(buf[i]);
        }

        write(client_sock,buf,len);

        close(client_sock); 
    }

	return 0;
   
}

```

#### 客户端

```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdlib.h>

#define SERVER_PORT 666
#define SERVER_IP "192.168.254.138"

int main(int argc , char *argv[])
{
	int sockfd;
	struct sockaddr_in serveraddr;
	char *message;
	int n;
	char buf[64];
	//char str[64];

	if (argc !=2)
	{
		fputs("Usage: ./echo_client message \n" , stderr);
		exit(1);
	}

	message = argv[1];

	printf("meeage: %s\n", message);
	sockfd=socket(AF_INET,SOCK_STREAM,0);

	memset(&serveraddr,'\0',sizeof(struct sockaddr_in));

	serveraddr.sin_family = AF_INET;
	inet_pton(AF_INET,SERVER_IP,&serveraddr.sin_addr);
	serveraddr.sin_port=htons(SERVER_PORT);

	connect(sockfd,(struct sockaddr *)&serveraddr , sizeof(serveraddr));

	write(sockfd,message,strlen(message));

	n=read(sockfd,buf,sizeof(buf)-1);

	if (n>0)
	{
		buf[n]='\0';
		printf("recevie:%s\n",buf);
	}
	else
	{
		perror("error!!");
	}

	printf("finished . \n");

	close(sockfd) ;

	return 0;
}

```

#### 实例讲解

socket套接字

```properties
linux环境下，用于表示进程间网络通信的特殊文件类型，本质为内核借助缓冲区形成的伪文件。用整数表示。

既然是文件，那么理所当然的，我们可以使用文件描述符引用套接字。Linux系统将其封装成文件的目的是为了统一接口，使得读写套接字和读写文件的操作一致。区别是文件主要应用于本地持久化数据的读写，而套接字多应用于网络进程间数据的传递。

在TCP/IP协议中，“IP地址+TCP或UDP端口号”唯一标识网络通讯中的一个进程。“IP地址+端口号”就对应一个socket。欲建立连接的两个进程各自有一个socket来标识，那么这两个socket组成的socket pair就唯一标识一个连接。因此可以用Socket来描述网络连接的一对一关系。

在网络通信中，套接字一定是成对出现的。一端的发送缓冲区对应对端的接收缓冲区。我们使用同一个文件描述符索发送缓冲区和接收缓冲区。

```

函数

```
inet_pton\inet_ntop\sockaddr\htonl\ntohl\htons\ntohs
```

socket编程函数







## 多线程并发服务器