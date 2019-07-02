#include <stdio.h>

int add(int x,int y)
{
	return x+y;
}

int main(void)
{
	int a,b;

	printf("enter a:\n");
	scanf("%d",&a);

	printf("enter b:\n");
	scanf("%d",&b);

	int rslt = add(a,b);
	printf("result:%d",rslt);

	return 0;
}