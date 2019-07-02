/*

变量的存储位置就是该变量的地址，该地址就是”指针“，变量存取都是通过”指针“，指针有两个属性，指向变量/对象的地址和长度

*变量[指针变量]：存放另外一个变量的地址，指针变量的类型就是另外一个变量的类型，指针变量作为函数的地址传递，否则就是值传递。
	**变量：二级指针？？？

&运算符 与 *运算符 ：*运算符是取值，&运算符是取地址，他们是互逆运算。优先级为：2 。 字符数组（字符串）的指针可以 做 ++ 运算。

数组与指针：数组名是数组的首地址，用指针变量指向所找的数组元素，占内存少，速度快 a[] , *p=&a[0]<=>*p=a , 数组元素的两种表达法：a[i]=*(a+i) ，指针可以看成数组的下标
	数组指针：还是指针变量，指向数组 并不是数组的首地址（a[] ,*p=a），定义：(*p)[n]  (**p)[n]:数组二级指针
	指针数组：还是数组，存放的是指针，定义：*p[n]

字符串与指针：字符串指针就是字符串的首地址，即第一个字符的地址，可以使用字符串指针来保存这个地址。char *str = "learning C language!" ;

函数指针与指针函数：
	函数指针：{类型名 (*函数名)(函数参数列表)} 指向函数，实质上还是指针，占4个字节。
	指针函数：实质上是函数，返回某个类型的指针，{类型名 *函数名(函数参数列表)} 。 节约内存 。
	int(*(*pFunc)(int,int))(int);

void指针：没有类型，可以指向任何类型，赋值给其他类型的时候要转型. type *p = (type *)voidp . void指针不能参与运算，除非强制转换。不能复引用

指针与引用：地址和值、const

*/
#include <stdio.h>
#include <string.h>

void print_pointer()
{
	printf("-------指针---------------\n");
	int x = 500;
	int *y = NULL;
	y = &x;
	printf("x的值是：%d \n", x);
	printf("x的地址是：%d \n", &x);
	printf("y的值是：%d \n", y);
	printf("y的进行了*运算后的值是：%d \n", *y);
	printf("y的地址是：%d \n", &y);
	//  printf("y的进行&*运算后的值是：%d \n", &*y);
	//  printf("y的进行*y++运算后的值是：%d \n", ++y);
	//  printf("y的进行*y++运算后的值是：%d \n", *y++);
	//  printf("x的值是：%d \n", x);
	printf("y的进行(*y)++运算后的值是：%d \n", ++(*y));
}

void print_pointer1()
{
	int x = 980;

	int *px = &x;
	// 覆盖了x的地址内的值 ，*px此时是值了。
    *px = 489;
	//px = 498;
	printf("%d\n",x);
}

void swap(int *a, int *b)
{
	int temp;
	temp = *a;
	*a = *b;
	*b = temp;
}

void swap1(int a, int b)
{
	int temp;
	temp = a;
	a = b;
	b = temp;
	printf("a=%d,b=%d \n", a, b);
}

void print_pointer2()
{

	printf("---------------");
	int a =90, b =80;
	printf("------1---------");
	// if (a > b) swap(&a,&b);
	if (a > b) swap1(a, b);

	printf("a=%d,b=%d \n", a, b);
}

void print_pointer3()
{
	int array[] = { 23, 22, 33, 56, 67, 11, 21 };
	int *pa = NULL;
	pa = &array[0];

	// --------数组方法
	printf("数组方法 --------- array[1]=%d \n", array[1]);
	printf("*(array+1)=%d \n", *(array + 1));

	//---------------指针
	printf("指针 --------- array[1]=%d \n", pa + 1);
	printf("*(pa +1)=%d \n", *(pa + 1));
}

void copy(char *originalarr, char *copyarr)
{
	/*
	int i=0;
	for (; *(originalarr + i) != '\0'; i++)
	{
	*(copyarr + i) = *(originalarr + i);
	}
	*(copyarr + i) = '\0';*/

	for (; *originalarr != '\0'; originalarr++, copyarr++)
		*copyarr = *originalarr;
	*copyarr = '\0';
}

void print_pointer5()
{
	char array[] = "learning C language ! \n" ;
	printf("字符数组打印结果:%s" , array+8);

	char *str = "learning C language! \n";
	printf("字符串指针:%s", str+8);

	char *tmp = NULL;
	tmp = str;

	tmp = tmp + 3;
	while (*tmp)
	{
		putchar(*tmp);
		tmp++;
	}

	char copyarray[50];
	copy(array,copyarray);
	printf("复制后的值:%s", copyarray);
}

void point_pointer6()
{
	char *username = "admin";
	char *password = "123456";

	char input_username[64];
	char input_password[64];

	printf("请输入用户名:\n");
	// scanf_s("%s",&input_username,20);
	gets(input_username);
	printf("请输入密码:\n");
	gets(input_password);

	if (strcmp(input_username, username) == 0 && strcmp(input_password, password) == 0)
	{
		printf("用户名及密码验证成功！");
	}
	else
	{
		printf("用户名及密码验证失败！");
	}

}

//定义函数指针
void(*pointFunc)(int a, int b);

// 函数指针被调用的方法
void point_pointer(int a,int b)
{
	printf("point_pointer 被调用了,输入参数:%d ,%d！\n ",a,b);
}

void point_pointer7(void)
{
	//指向被调用的函数
	pointFunc = point_pointer;
	//调用函数 - 相当于 point_pointer();
	(*pointFunc)(1,2);
}

//指针函数  -
int * sum(int n)
{
	int static sum = 0;
	for (int i = 0; i < n; i++)
	{
		sum += i;
	}
	int *p = &sum;
	return p;
}

void point_pointer8(void)
{
	//int *total = NULL;
	//total = sum(10);
	printf("rslt:%d", *sum(10));
}

void point_pointer9(void)
{
	char array[] = { 'a', 'b', 'd', 'e', 'g' };
	char(*p)[] = array;
	//数组指针
	printf("数组指针[3]:%c",(*p)[2]);
	printf("数组指针[3]的地址:%p \n", &((*p)[2]));

	//指针数组
	char a = 'a';
	char b = 'b';
	char c = 'c';
	char d = '\0';
	char *pp[4];
	pp[0] = &a;
	pp[1] = &b;
	pp[2] = &c;
	printf("指针数组[2]:%c \n", *pp[2]);

	//void、
	int aa = 55;
	void *k = NULL;
	k = &aa;
	int *ppp = (int *)k;
	printf("%d \n", *ppp);

	//
	int array9[50];
	int length = sizeof(array9) / sizeof(int);
	printf("%d \n", length);

}

void point_pointer10(void)
{
	//const 定义常变量 ，只有读的权限
	const int x = 10;
	const int *p = &x;
	int *pp = &x;
	*pp = 100;
	printf("%d", x);

}
