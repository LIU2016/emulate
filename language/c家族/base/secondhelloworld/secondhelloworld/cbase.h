#include <stdio.h>
#include "define.h"
/*

------------------------------------------

基础--类型

------------------------------------------

short \ int \long \
float \ double \
char
enum

字节和位

原码、反码、补码 （二进制表达）

溢出 (int -32768~32767 long 2147483647)

ASCII (A-Z 65-90 a-z 97-122 0-9 48-57)

字符char算术运算实际上就是对ASCII进行运算，用二进制存储

-----------------------------------------------------

基础--数值数据间的混合运算

------------------------------------------

自动转换：
char、short - > int

float -> double

int->unsigned -> long -> double

强制转换：

------------------------------------------

基础--算术运算符和算术表达式

---------------------------------------

指针运算符：* &
求字节数：sizeof
分量运算符：. ->
位运算符：>> << ~ | ^ &

---------------------------------------

基础--[顺序、选择、循环]结构程序设计

---------------------------------------

C程序（若干个源程序文件）
源程序文件（预处理命令、全局变量声明、函数）
函数（函数首部、函数体）
函数体（局部变量、执行语句）

goto语句

---------------------------------------

基础--字符数组\指针\

--------------------------------------

字符串就是字符数组加'\0'来表示
char[5] string = {'i','a','b','c'}
char[5] string = {"iabc"}
char[5] string = "iabc"


*/

void go_loof_if()
{
	int sum = 0;
	int i = 0;
	loop_if:if (i <= 100)
	{
		sum = sum + i;
		i++;
		goto loop_if;
	}
	printf("rslt:%d", sum);
}

//#undef PRINT

void print_string()
{
	#ifdef PRINT_MSG
		#define PRINT_MSG "SAY \n"
	#endif
	char str[] = PRINT_MSG;
	printf("%s", str);
	PRINT;
	MYDEFINE("world\n");
}

void print_()
{
	long a, b;
	a = 32767;
	b = a + 1;
	printf("%d", b);
}