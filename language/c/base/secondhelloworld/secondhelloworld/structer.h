/*

结构体嵌套：

结构体数组：

联合体(也叫公用体)： 与结构体区别：
	结构体的成员占用内存不同，互不影响，
	而共用体的所有成员占用同一个内存，修改一个影响其他的所有成员。联合体的内存是最长成员的占用内存，使用内存覆盖技术，同一时刻只能保存一个成员的值。有新成员赋值就会覆盖就的成员。
union 共用体名
{

}

枚举：
enum DAY
{
	
}

字节对齐规则：pragma pack(5) 对齐5 ，如果对齐的内存能够存储多个变量，就不用每个变量都去申请内存重新从0对齐，就会多个变量地址求和后对齐。默认是用类型最长的为标准对齐数。
	需要字节对齐的根本原因：在于CPU访问数据的效率问题
	数组：按基本数据类型对齐，第一个对齐后面的都对齐了。
	联合：按最大长度的数据类型对齐。
	结构体：每个数据类型都要按类型对齐。
	基本数据类型：只要地址是是它的长度的整数倍
	在设计不同CPU的通信协议（嵌入式开发）或者编写硬件驱动的寄存器的结构时需要对齐，即使看起来自然对齐的也要对齐，避免不同德编译器生产的代码不一样

typedef：重命名已有的类型名称 ; typedef int MY_INT


*/
#pragma pack(4)
#include <stdio.h>

struct sBirthday
{
	int year;
	int month;
	int day;

	char sex1;
	char sex2;
};

struct personInfo
{
	char name[10];
	char sex[4];
	/*c++ 不用加struct*/
	// struct sBirthday birthday;
	// 结构体嵌套
	struct ssBirthday
	{
		int year;
		int month;
		int day;
	} birthday;
	char addr[200];
} sperson = { "lqd01", "boy1", { 1996, 12, 4 }, "湖南雨花区万家丽路" };

void print_structer()
{
	// struct personInfo personInfo = { "lqd", "boy", { 1986, 12, 4 }, "湖南雨花区万家丽路" };
	//birthday.year = 1986;
	//birthday.month = 12;
	//birthday.day = 4;
	//struct personInfo person;
	//person.birthday = birthday;
	// struct personInfo *person = &sperson;// &personInfo;
	struct sBirthday bday;
	bday.year = 1988;
	//person->name 
	printf("year:%d \n", bday.year);
	//printf("name=%s,birthday year:%d \n", personInfo.name, personInfo.birthday.year);
}

void print_structer1()
{
	struct personInfo personInfo[2] = { { "lqd", "boy", { 1986, 12, 4 }, "湖南雨花区万家丽路" }, { "lqd01", "bo01", { 1999, 12, 4 }, "湖南雨花区万家丽路" } };
	struct personInfo *person = &personInfo;
	printf("name=%s,birthday year:%d \n", (person+1)->name, (person+1)->birthday.year);
	printf("name=%s,birthday year:%d \n", personInfo[0].name, personInfo->birthday.year);
}

//typedef
typedef int MY_INT;
typedef union dataType
{
	MY_INT i;
	char ch;
	double dou;
} dt;

void print_union()
{
	dt dtype = { 'a' };
	printf("union:%d \n",dtype.i);
	printf("union:%d \n", sizeof(dtype));
}

enum STATUS_TYPE
{
	RUNNING='A',//自动补齐后面的值 STOP为’C‘
	BLOCKING,
	STOP
};

enum FLAG{ true, false } end, match;

void print_enum()
{
	enum STATUS_TYPE status_type;
	status_type = RUNNING;
	printf("union:%c \n", status_type);
	printf("flag:%d", end);
}

void print_duiqi()
{
	struct personInfo person;
	printf("占用的字节 :%d \n", sizeof(person));
	printf("%p %p", &person.name , &person.sex);
}