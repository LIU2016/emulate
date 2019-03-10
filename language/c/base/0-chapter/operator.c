#include <stdio.h>
#include <string.h>

int main(void){

	/**第一课：
	   strcmp:
	   strncmp:最多比较字符串str1和str2的前count个字符.
	   其他数据类型的比较运算:
	    大于：       	>    
		大于或等于:  	>=  
		小于：      	<
		小于或等于：	<=
		不等于：		!=      
		等于：  		==     （注意：不是 = ）

		
		比较运算的结果：（逻辑值）
		结果为“真”：  1
		结果为“假”：  0
		
		版本	说明
		C89/C90	 两者差别很小，一般都统称为C89,“老版本”,变量的声明必须放在语句的开头
		C99	支持布尔类型,支持运行时才确定数组的长度
		C11	最新版本

		C89标准中的逻辑值
		使用0和1表示逻辑值
		真	1
		假	0
		非0值	真
		
		C99标准中的逻辑值（兼容C89）
		使用bool类型表示逻辑类型
		使用 true 表示真
		使用 false表示假
		注意：需要包含头文件 stdbool.h

		运算符优先级
		一共有15个级别！
		不需强制记忆，只需要掌握以下常用的优先级：
		最高优先级：( )和[ ]
		倒数第二低优先级：赋值和复合赋值(=， +=,  -=  ...)
		最低优先级：逗号表达式
		！ > 算术运算符 > 关系运算符 > && > || > 赋值运算符

		x =  ! 3 + 4 < 5 && 6 > 7 || 8 > 7;
		等效于：
		x =  ((!3 + 4 < 5) && (6 > 7)) || (8 > 7); 

	**/

	/*char name[32];
	char password[16];

	gets(name);	
	gets(password);

	if ( strcmp(name,"admin") == 0 && strcmp(password,"123456") == 0 ){
		printf("login success!") ;
	}else{
		printf("login fail!");
	}
	*/

	/*int a ,b ;
	scanf("%d%d",&a,&b);
	printf("%d",a>b);*/

	

}