/*

变量的存储位置就是该变量的地址，该地址就是”指针“，变量存取都是通过”指针“

*变量[指针变量]：存放另外一个变量的地址，指针变量的类型就是另外一个变量的类型，指针变量作为函数的地址传递，否则就是值传递。

&运算符 与 *运算符 ：*运算符是取值，&运算符是取地址，他们是互逆运算。优先级为：2

数组与指针：数组名是数组的首地址，用指针变量指向所找的数组元素，占内存少，速度快 a[] , *p=&a[0]<=>*p=a , 数组元素的两种表达法：a[i]=*(a+i)

*/
#include <stdio.h>

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
	rintf("指针 --------- array[1]=%d \n", pa+1);
	printf("*(pa +1)=%d \n", *(pa + 1));
}
