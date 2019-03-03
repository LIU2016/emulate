# 安装

1，设置MinGW的环境变量

2，notepad++编写代码

3，命令提示符下gcc hello.c

# 语法

变量：是内存中的一块存储空间，一小块内存

数据类型：char，int，long，double，float

方法：scanf，getchar，putchar，getc，putc

```c
#include <stdio.h>

int main(void) {
	
	char name;
	int pwd;
	double test_double;
	char getcharname;
	float test_float;
	long test_long;
	
	/*//输入用户名和密码
	printf("please enter name:");
	scanf("%c", &name);
	printf("please enter pwd:");
	scanf("%d", &pwd);
	printf("name:%c ; pwd:%d \n",name, pwd);
	printf("%d\n" , name);
	scanf("%lf",&test_double);
	printf("test_double=%f",test_double);*/
	
	//getcharname=getchar();
	//getcharname=getc(stdin);
	
	//printf("getcharname=%c \n",getcharname) ;
	//putchar(getcharname);
	//putc(getcharname,stdout);
	
	//判断用户名和密码是否正确
	
	
	//登录成功后的界面
	//printf("----交换机后台管理");
	//printf("1,登录\n");
	//printf("2,创建账号\n");
	//printf("1,退出\n");
	return 0 ;
}

```

```c
#include <stdio.h>

int main(void){
	
	/**让用户输入一个圆的半径，然后输出这个圆的面积和周长。
	double r ,s;
	scanf("%lf", &r) ;
	s=3.14159*r*r;
	printf("s:%lf\n",s) ;**/
	
	/**让用户输入一个小写字母，然后输出对应的大写字母。**/
	char a,A;
	scanf("%c", &a) ;
	A=a-32;
	printf("%c\n",A);
}
```

