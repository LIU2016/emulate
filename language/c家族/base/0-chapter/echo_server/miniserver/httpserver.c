#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>
#include <ctype.h>
#include <arpa/inet.h>
#include <errno.h>
#include <stdlib.h>

#define SERVER_PORT 80

int get_line(int sock, char *buf , int size);
int parser_content(char *buf);
void do_repsonse(int client_sock);

int errormsg(const char * msg)
{
    fprintf(stderr,"%s error! reason:%s/n",msg , strerror(errno));
    exit(1);
}

int main(void){

    int sock;
    int i;
    int bindid;

    struct sockaddr_in server_addr;
    sock = socket(AF_INET, SOCK_STREAM, 0);

    if(sock == -1) {
	errormsg("create");
    }

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

    
    bindid=bind(sock, (struct sockaddr *)&server_addr, sizeof(server_addr));
    if (bindid == -1)
    {
	close(sock);
	errormsg("bind");
    }

    /**
    * 改变 系统限制的backlog 大小
    */
    listen(sock, 128);

    printf("监听地址:%d,监听端口:%d,等待客户端连接:\n",INADDR_ANY,SERVER_PORT); 

    int done =1 ;

    while(done)
    {
        struct sockaddr_in client;
        int client_sock,len;
        char client_ip[64];
        char buf[256];
       	int j=0;

        socklen_t client_addr_len;
        client_addr_len = sizeof(client);
   	    client_sock = accept(sock,(struct sockaddr *)&client,&client_addr_len);
          
        printf("client ip:%s \t port: %d \n",
               inet_ntop(AF_INET,&client.sin_addr.s_addr,client_ip,sizeof(client_ip)),
	           ntohs(client.sin_port));

      	do{
      		len=get_line(client_sock,buf,sizeof(buf));
      		printf("%s\n",&buf);
      		if (j==0)
      		{
      			parser_content(buf);
      		}
      		j++;
      		
      	}while(len>0);

		do_repsonse(client_sock);
        //write(client_sock,buf,len);

        close(client_sock); 
    }

	return 0;
   
}

void do_repsonse(int client_sock)
{
	const char *main_header =  "HTTP/1.0 200 OK Server: Martin Server Content-Type: text/html Connection: Close";
	const char *content_body="<html lang='zh-CN'><head><meta content='text/html; charset=utf-8' http-equiv='Content-Type'><title>This is a test</title></head><body><div>hello world!http server</div></body></html>";		

	char send_buf[64];
	int wc_len = strlen(content_body);
	int len = write(client_sock,main_header,strlen(main_header));
	len = snprintf(send_buf,64,"Content-Length:%d\r\n\r\n",wc_len);
	len = write(client_sock,send_buf,len);	
	len = write(client_sock,content_body,wc_len);												
}

int parser_content(char *buf)
{
	char method[16];
	char url[16];
	int count=0;
	int i=0;
	char sign='m';

	//printf("parser start!%s\n",buf);
	while(count<strlen(buf)-1)
	{
		//printf("%d,%c\n",strlen(buf)-1,buf[count]);
		if(!isspace(buf[count]))
		{
			if (sign=='m')
			{
				method[i]=buf[count];
			}
			else if (sign=='u')
			{
				//printf("%c,%c,%d\n",sign,buf[count],i);
				url[i]=buf[count];
			}
		}
		else
		{
			if (sign=='m'&&i!=0)
			{
				method[i]='\0';
				//printf("%c\n",sign);
				sign='u';
				i=0;
			}
			else if(sign=='u'&&i!=0)
			{
				url[i]='\0';
				i=0;
				sign='o';
			}
		}
		i++;
		count++;
	}

	printf("method:%s\n",&method);
	printf("url:%s\n",&url);
	return 0;
}

int get_line(int sock, char *buf , int size)
{
	char ch='\0';
	int count=0;
	int len =0;

	while(count<size-1&&ch!='\n')
	{
		len=read(sock,&ch,1);
		if (len!=1)
		{
			return 0;
		}

		if(ch=='\r')
		{
			continue;
		}
		else if (ch=='\n')
		{
			buf[count]='\0';
			break;
		}
		buf[count]=ch;
		count++;
	}
	return count;
}


