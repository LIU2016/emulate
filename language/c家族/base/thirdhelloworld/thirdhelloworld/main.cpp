#include <cstdio>
#include <iostream>
#include "first.h"
#include <string>

/*
	1,using namespace
	2,class object
	3,public private
	4,析构、友元
	5,this指针
	6,内联函数（提升执行效率，节省编译时间，耗内存，空间换时间的方式。inline）
	7,static（类的静态成员，）
	8,指向类的指针
	9,动态内存技术（内存分配） （栈 + 堆） 
		栈：在函数内部声明的所有变量都将占用栈的内存。
		堆：(不确定内存需要多少)在程序中未使用的内存，用于运行时动态分配内存。new 分配堆内存，delete释放new的内存
    10，string
*/

using namespace std;

class Math
{
public:
	int compare(int a, int b);
	Math(int *p);
	void print();
private:
	int *k;
};

int Math::compare(int a, int b)
{
	if (a>b)
	{
		return 1;
	}
	else if (a==b)
	{
		return 0;
	}
	else
	{
		return -1;
	}
}

Math::Math(int *p)
{
	k = p;
}

void Math::print()
{
	cout << *k << endl;
}

class Number
{
public :
	Number(int i);
	~Number();/*析构函数*/
	Number(Number&copyObj); /*拷贝构造函数*/
	void print();
    void print(Number number);
	friend void print(Number number); /*友元函数是非成员函数，可以使用对象的私有变量*/
	friend class MyNumber; /*友元类 可以访问其他对象的私有变量*/
private:
	int *u;
};

Number::Number(int i)
{
	u = new int;
	*u = i;
}

Number::Number(Number&copy)
{
	u = new int;
	*u = *copy.u;
}

Number::~Number()
{
	u = NULL;
	cout << "析构函数，释放内存!" << endl;
}

void Number::print()
{
	cout << *u << endl;
}

void Number::print(Number number)
{
	cout << *number.u << endl;
}

void print(Number number)
{
	cout << *number.u << endl;
}

class MyNumber {
public:
	void print(Number nu);
};

void MyNumber::print(Number nu)
{
	cout << "友元类:" << *nu.u << endl;
}

class MyThis {
public:
	MyThis(char *name);
	void print();
	void say();
	static int count;
	static void useStatic() {
		cout << "静态" << count << endl;
	};
private:
	char name[10];
};

int MyThis::count = 0;

MyThis::MyThis(char *name)
{
	name = name;
	count++;
}

void MyThis::say()
{
	cout << "this 调用的函数" << endl;
}

void MyThis::print()
{
	cout << "this指针调用的成员变量:" << this->name << endl;
	this->say();
}

inline int compare(int a,int b)
{
	return (a > b ? a : b) ;
}

int main(void)
{
	int a = 9;
	Math math(&a);
	int rslt = math.compare(23,68);
	cout << rslt << endl;
	math.print();

	cout << "=====" << endl;
	Number number(10);
	Number numberCopy(number);
	print(numberCopy);

	cout << "=====" << endl;
	MyNumber ber;
	ber.print(numberCopy);

	cout << "=====" << endl;
	char name[6] = "adfsa";
	MyThis mythis(name);
	MyThis mythis1(name);
	mythis.print();

	cout << compare(10, 20) << endl;

	MyThis::useStatic();

	cout << "指向类的指针" << endl;
	MyThis *clazz;
	clazz = &mythis1;
	cout << "" << clazz->count << endl;
		
	cout << "动态内存技术" << endl;
	int *girl = NULL;
	girl = new int(32);
	delete girl;

	int *girls = new int[10];
	delete[] girls;

	int **boys = new int*[10];
	for (int i = 0; i < 10; i++)
	{
		boys[i] = new int[10];
	}
	for (int i = 0; i < 10; i++)
	{
		delete[] boys[i];
	}

	cout << "string" << endl;
	string s2;
	string s1 = "12312313";
	string s3(3, 'C');
	s2 = s1;
	cout << s3 << s3.length() << s2 << endl;

	//getchar();
	return 0;
}
