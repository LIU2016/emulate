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
