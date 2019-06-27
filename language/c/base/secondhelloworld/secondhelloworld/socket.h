/*
 sockaddr sockaddr_in
*/
/*
	sin_family : 地址族
	USHORT sin_port;
	IN_ADDR sin_addr;
	CHAR sin_zero[8];
	#include <Winsock2.h> 将 这个引用定义到second.c里面
	*/

#pragma comment(lib,  "ws2_32.lib")

char cName[10];
void print_sock()
{
	char cAddress[50];
	int iModel = 0;
	printf("*******************************************\n");
	printf("************欢迎来到迷你聊天系统***********\n");
	printf("*******************************************\n");

	printf("请输入连接的ip地址:\n");
	scanf("%c", &cAddress, 50);

	printf("请输入你的昵称:\n");
	scanf("%c", &cName, 10);

	//初始化套接字
	WSADATA wsadata;
	int ret;
	/*
	为了在应用程序当中调用任何一个Winsock API函数，
	首先第一件事情就是必须通过WSAStartup函数完成对Winsock服务的初始化，因此需要调用WSAStartup函数。
	使用Socket的程序在使用Socket之前必须调用WSAStartup函数。
	该函数的第一个参数指明程序请求使用的Socket版本，其中高位字节指明副版本、低位字节指明主版本；
	操作系统利用第二个参数返回请求的Socket的版本信息。
	当一个应用程序调用WSAStartup函数时，操作系统根据请求的Socket版本来搜索相应的Socket库，
	然后绑定找到的Socket库到该应用程序中。以后应用程序就可以调用所请求的Socket库中的其它Socket函数了。
	*/
	if ((ret = WSAStartup(MAKEWORD(2, 2), &wsadata)) != 0)
	{
		printf("初始化失败!");
		return 0;
	}

	// 1,创建套接字
	SOCKET acceptSocket;
	acceptSocket = socket(AF_INET, SOCK_STREAM, 0);

	if (acceptSocket == INVALID_SOCKET) {
		
		printf("创建套接字失败!");
		return 0;
	}

	// 2,定义IP和端口
	SOCKADDR_IN server;
	server.sin_family = AF_INET;
	server.sin_port = htons(12266);
	server.sin_addr.s_addr = inet_addr(acceptSocket);

	// 3,连接
	if (connect(acceptSocket, (SOCKADDR *)&server, sizeof(server)) == INVALID_SOCKET)
	{
		printf("连接失败，将自身转换成服务器!");
		iModel = 1;
	}

	//客户端
	if (iModel == 0)
	{
		printf("已成功连接服务器，发送quit可以提出系统!");
	}

	//服务器
	if (iModel == 1)
	{

	}

}
