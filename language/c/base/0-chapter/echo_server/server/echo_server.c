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

    //选择协议组IPV4
    server_addr.sin_family = AF_INET;
    //解决大端和小端字节序
    /**
    大端字节序 - 低地址高字节,高地址低字节
    小段字节序 - 低地址低字节,高地址高字节
    */
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(SERVER_PORT);

    
    bind(sock, (struct sockaddr *)&server_addr, sizeof(server_addr));

    listen(sock, 128);

    printf("监听地址:%d,监听端口:%d,等待客户端连接:\n",INADDR_ANY,SERVER_PORT); 

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
