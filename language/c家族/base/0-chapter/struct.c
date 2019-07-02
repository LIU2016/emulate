#include <stdio.h>
#include <string.h>

/**
*一般不建议把结构体直接作为函数参数。
因为结构体的size比较大，直接传递，消耗性能！
解决方案（使用指针）
**/
struct student{
	char name[16];
	int age;
};

int main(void)
{
	/**完整的类型名称是  struct  student **/
	struct student s1={
		"Rock",18
	};

	struct student s2={
		"LQD",23
	};

	struct student s3;
	strcpy(s3.name,"chaijuanjuan");
	s3.age=21;

	printf("%s,%d\n",s1.name,s1.age);
	printf("%s,%d\n",s2.name,s2.age);
	printf("%s,%d\n",s3.name,s3.age);

	return 0;

}