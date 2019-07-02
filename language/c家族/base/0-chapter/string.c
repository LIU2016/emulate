#include <stdio.h>
#include <string.h>

/**
字符串，是通过“字符数组”(元素类型为char的数组）来存储的！
**/
int main(void){

	/**第一课，字符数组**/
	/*char name[32];
	char passwd[16];
	printf("enter your name!");
	scanf("%s",name);
	printf("enter your passwd!");
	scanf("%s",passwd);

	printf("userName:%s",name);
	printf("passwd:%s",passwd);*/

	/**第二课，字符串存储方式**/
	/*char name[5];
	name[0]='d';
	name[1]='a';
	name[2]='y';
	name[3]='u';
	name[4]='p';
	name[5]='\0';
	printf("%s" ,name)  ;*/

	/*char name[10]="Rock";
	printf("name=%s\n",name);*/

	/*char name[]="LQD";
	printf("name=%s,namespace=%d\n",name,sizeof(name));
	name[1]=0;
	printf("name=%s,namespace=%d\n",name,sizeof(name));*/

	/**第三课，字符串输入，
	但遇到特殊的情况
	1,scanf不能读取空格、制表符，因为被当作“分隔符”处理了,
	2,采用gets能够读取 空格、制表符，但是不读取回车符,
	3,安全！当输入数据太多时，就只读取（第二个参数 -1）个字符,回车符也被读到字符串（除非输入数据太多）
	**/
	/**例如：I want **/
	/*char name[10];
	scanf("%s",name);
	printf("your name:%s",name);*/

	/*char name[10];
	gets(name);
	printf("your enter: %s" , name);*/

	/*char name[5];
	fgets(name,5,stdin);
	printf("your enter:[%s]\n", name);*/

	/**第四课：字符串函数**/
	/**计算长度**/
	/*	char name[64];
	int length;
	gets(name);
	length=strlen(name);
	printf("name=%s,length=%d",name,length);*/

	/**拷贝字符串**/
	/**
	strcpy的特点：把源字符串的“字符串结束符”也一同拷贝到目的字符串中，strcpy的缺点：可能导致字符串越界！不安全。
	strncpy
	**/
	/*char name[64];
	char copyname[64];
	gets(name);
	strcpy(copyname,name);
	printf("copyname=%s",copyname);*/

	/*char name[64];
	char copyname[64];
	gets(name);
	strncpy(copyname,name,5);
	printf("copyname=%s",copyname);*/

	/**字符串连接**/
	/*char name[64];
	char sex[64];
	gets(name);
	gets(sex);
	strcat(name,sex);
	printf("name=%s",name);
	printf("sex=%s",sex);	
	*/
	return 0;
}