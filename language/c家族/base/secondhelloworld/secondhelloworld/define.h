//宏定义
/*-----#define\#include\#if #else #endif-----*/
/*
以#开头
占单独行
不加;

#define带参的宏
#undef PRINT 取消宏定义
#include <> ""
#if #else #endif 
#ifdef #define #endif 前面定义了宏，则覆盖之前的
#ifndef #define #endif

*/
#define PRINT_MSG "helloworld \n"
#define PRINT printf("Helloworld define \n")
#define MYDEFINE(a) printf("arg :%s",a)