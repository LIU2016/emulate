#include <stdio.h>

int main(void)
{
	
	/**文本**/
	/**第一节课：fgetc\fputc**/
	/*
	FILE *file;
	FILE *filew;
	char c;*/
	/*file=fopen("user.txt","r");
	if(!file)
	{
		printf("file not exists!");
		return 1;
	}

	filew=fopen("user1.txt","w");
	while((c=fgetc(file))!=EOF)
	{
		printf("%c",c);
		fputc(c,filew);
	}*/
	/**
	*特别注意：
	对文件执行写操作以后，并不会马上写入文件，而只是写入到了这个文件的输出缓冲区中！
	只有当这个输出缓冲区满了，或者执行了fflush，或者执行了fclose函数以后，或者程序结束，
	才会把输出缓冲区中的内容正真写入文件！
	*/
	/*fclose(file);
	fclose(filew);*/


	/**第二节课：fgets\fputs**/
	/*
	FILE *file;
	FILE *filew;
	char tmp[64];
	file=fopen("user.txt","r");
	filew=fopen("userw.txt","w");
	while(fgets(tmp,sizeof(tmp),file)!=NULL)
	{
		//printf("%s",tmp);
		fputs(tmp,filew);
	}
	fclose(file);*/


	/**第三节课：fscanf\fprintf 格式化读写**/
	/*FILE *file;
	char tmp[64];
	int age;
	char c;

	file=fopen("user_fprintf.txt","w");

	while(1)
	{
		printf("enter name:");
		scanf("%s",tmp);

		printf("enter password:");
		scanf("%d",&age);

		fprintf(file,"姓名:%s\t\t年龄:%d\n",tmp,age);

		printf("again?Y/N\n");
		while((c=getchar())!='\n');
		
		scanf("%c",&c);
		if (c=='Y'||c=='y'){
			continue;
		}else{
			break;
		}
		
	}
	fclose(file);*/

	/*FILE *file;
	char name[64];
	int age;
	int rslt;

	file=fopen("user_fprintf.txt","r");

	while(1)
	{
		rslt=fscanf(file,"姓名:%s 年龄:%d\n", name, &age);
		if (rslt==EOF) {break;}
		printf("%s,%d\n",name,age);
	}
	fclose(file);*/

	/**二进制**/

	/**fwrite/fread**/
	/*FILE *file;
	char name[64];
	int age;
	file=fopen("binaryFile","wb");
	printf("enter name:\n");
	scanf("%s",name);
	printf("enter age:\n");
	scanf("%d",&age);
	fwrite(name,sizeof(char),sizeof(name),file);
	fwrite(&age,sizeof(int),1,file);
	fclose(file);*/

	/*FILE *file;
	char name[32];
	int age;
	int ret;
	file=fopen("binaryFile","rb");	
	fread(name,sizeof(char),sizeof(name),file);
	fread(&age,sizeof(int),1,file);
	printf("%s , %d \n" ,name ,age);
	fclose(file);*/

	/**putw/getw**/
	/*FILE *file;
	int data[]={1,2,3,4,5} ;
	int i;
	file=fopen("intfile","wb");
	for(i=0;i<sizeof(data);i++)
	{	
		putw(data[i],file);
	}
	fclose(file);*/

	/*FILE *file;
	int value;

	file=fopen("intfile","rb");

	while(1)
	{
		value=getw(file);
		if (value==-1 && feof(file)) break;
		printf("%d",value);

	}
	fclose(file);*/

	/**feof/ferror/clearerr/ftell/fseek/rewind**/
	FILE *file;
	long offset;

	file=fopen("user.txt","rb");
	offset=ftell(file);
	printf("%ld",offset);
	fgetc(file);
	offset=ftell(file);
	printf("%ld",offset);
	fclose(file);


	return 0;
}