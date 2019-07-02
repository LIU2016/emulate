#pragma once
#include <stdio.h>
#define SIZE 3
/**
fopen_s(&file,"test.txt","r");
fclose(fp);

文本文件
------------------------------
r  : 打开一个文件 <=> rt
w : 写一个文件
a  : 追加一段内容

二进制文件
------------------------------
rb  : 打开一个文件
wb : 写一个文件
ab  : 追加一段内容

r+
w+
a+


函数比较
-------------------------------
puts putc putchar fputc fputs printf内存到终端、磁盘
gets getc getchar fgetc fgets scanf 终端、磁盘到内存

fprintf_s:类似put系列 fscanf_s:类似get系列 rewind():移动位置指针到开始位置  fseek():移动位置指针到任意位置
-------------------------------

**/

void print_file_r()
{
	FILE* file;
	fopen_s(&file, "text.txt", "r+");
	if (file == NULL)
	{
		printf("文件打开失败!\n");
		exit(1);
	}
	else {
		printf("文件打开成功!\n");
		char ch = fgetc(file);
		while (ch!=EOF)
		{
			putchar(ch);
			ch = fgetc(file);
		}
	}
	fclose(file);
}

void print_file_w()
{
	FILE* file;
	char array[65];

	scanf("%s", array);

	fopen_s(&file, "text.txt", "a");

	for (int i = 0; i < sizeof(array); i++)
	{
		if (array[i]=='#' || array[i]==NULL)
		{
			break;
		}
		fputc(array[i], file);
	}
	
	fclose(file);
}

void print_file_s_r()
{
	FILE *file;
	fopen_s(&file, "text.txt", "r+");
	if (file!=NULL)
	{
		char arr[65];
		fgets(arr, 65, file);
		printf("%s", arr);
	}
	fclose(file);
}

void print_file_s_w()
{
	FILE *file;
	fopen_s(&file, "text.txt", "w+");
	if (file!=NULL)
	{
		char arr[68];
		//scanf("%s",arr);
		gets_s(arr,68);
		fputs(arr, file);
	}
	fclose(file);
}



struct Student {
	char name[10];
	int sex;
}t_student[SIZE];

void print_br_w_r()
{
	FILE *fp = NULL;

	/*
	for (int j=0; j<SIZE ; j++)
	{
		printf("请输入学生的姓名和性别\n");
		scanf("%s", &t_student[j].name);
		scanf("%d", &t_student[j].sex);
	}
	
	fopen_s(&fp, "textrb", "wb");
	for (int i=0; i<SIZE; i++)
	{
		if (fwrite(&t_student[i],sizeof(struct Student),1,fp) != 1)
		{
			printf("数据存储到了二进制文件中");
		}
	}
	fclose(fp);*/
	
	fopen_s(&fp, "textrb", "rb");
	for (int k=0; k<SIZE; k++)
	{
		fread(&t_student[k], sizeof(struct Student), 1, fp);
		printf("%s,%d \n", t_student[k].name, t_student[k].sex);
	}
	fclose(fp);
}

print_fscanf_s()
{
	//fscanf_s(,);
}