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

struct sClient
{
	SOCKET s;
	SOCKADDR_IN sin;
};

/*设置字体颜色*/
void setColor(int a)
{
	SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),a);
}

/*客户端介绍消息的函数*/
DWORD WINAPI client_recevice_Thread(LPVOID lp)
{
	SOCKET *s = lp;
	while (true)
	{
		int inRecv;
		char cBuffer[1024];
		inRecv = recv(*s,cBuffer,1024,0);
		if (inRecv > 0)
		{
			cBuffer[inRecv] = '\0';
			setColor(14);
			printf("%s\n", cBuffer);
			setColor(8);
		}
		if (inRecv == SOCKET_ERROR)
		{
			printf("与服务器已经断开，请重新连接！");
		}
	}
	return 0;
}

void print_sock()
{
	char cAddress[50];
	int iModel = 0;

	setColor(7);

	printf("*******************************************\n");
	printf("************欢迎来到迷你聊天系统***********\n");
	printf("*******************************************\n");

	printf("请输入连接的ip地址:\n");
	scanf("%s", &cAddress, 50);

	printf("请输入你的昵称:\n");
	scanf("%s", &cName, 10);

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
		setColor(15);
		printf("已成功连接服务器，发送quit可以提出系统!");
		setColor(7);

		char cBuf[1024];//用户输入的内容
		char cSendBuf[256];//昵称

		memset(cBuf, 0, sizeof(cBuf)); //初始化字符数组
		memset(cSendBuf, 0, sizeof(cSendBuf)); //初始化字符数组

		/*
		拼接消息内容
		*/
		strcpy_s(cBuf,1024 ,"我连接了");
		strcpy_s(cSendBuf,58 , cName);
		strcat_s(cSendBuf, 10, '说');
		strcat_s(cSendBuf,1024, cBuf);

		/*
		发送消息
		*/
		ret=send(acceptSocket, cSendBuf, sizeof(cSendBuf), 0);
		if (ret == SOCKET_ERROR)
		{
			printf("消息发送失败，请重新发送！");
			return 0;
		}
	
		/*
		创建接受消息的线程指针变量
		*/
		LPVOID *lp = (LPVOID*) &acceptSocket;
		HANDLE hThread0;

		//建立接受消息线程并执行
		CreateThread(NULL,0, client_recevice_Thread,lp,0,NULL);

		//主线程发送数据
		while (true)
		{
			memset(cBuf, 0, sizeof(cBuf)); //初始化字符数组
			scanf_s("%s", cBuf, 1024);

			//判断是否是quit
			if (strcmp(cBuf,"quit")==0)
			{
				break;
			}

			memset(cBuf, 0, sizeof(cBuf));
			strcpy_s(cSendBuf,58, cName);
			strcat(cSendBuf, '说');
			strcat(cSendBuf, cBuf);

			/*
			发送消息
			*/
			ret = send(acceptSocket, cSendBuf, sizeof(cSendBuf), 0);
			if (ret == SOCKET_ERROR)
			{
				printf("消息发送失败，请重新发送！");
			}
		}

		if (iModel ==1)
		{
			u_long ul = 1;
			struct sClient c[80];
			WSAEVENT eventarray[80];
			int total = 0; //统计套接字的个数
			c[0].s = socket(AF_INET, SOCK_STREAM, 0);
			ioctlsocket(c[0].s, FIONBIO, &ul);

			//填充ip和端口
			SOCKADDR_IN sin;
			sin.sin_addr.S_un.S_addr = INADDR_ANY;
			sin.sin_family = AF_INET;
			sin.sin_port = htons(12266);
			c[0].sin = sin;

			//绑定地址和端口
			if (bind(c[0].s,(SOCKADDR *)&c[0].sin,sizeof(c[0].sin))==SOCKET_ERROR)
			{
				printf("绑定失败，请重新检查！");
				return 0;
			}

			//启动监听模式
			listen(c[0].s,5);
			WSAEVENT event = WSACreatEvent();
			WSAEventSelect(c[0].s,event,FD_ACCEPT | FD_CLOSE);
			eventarray[total] = event; //套接字加入数组
			total++;
		}

		closesocket(acceptSocket);
		WSACleanup();
		CloseHandle(hThread0);
	}
}
