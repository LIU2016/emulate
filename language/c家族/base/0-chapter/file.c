#include <stdio.h>
#include <string.h>

int main(void)
{
	char name[32];
	char password[16];
	FILE *file;
	char line[128];
	char name_tmp[32];
	char password_tmp[16];
	char *ret;

	//从文件中取账号和密码
	//打开文件
	file = fopen("user.txt","r");
	if (!file){ //等效于 file==NULL （0）
		printf("file not exists!\n");
		return 1;
	}

	while(1)
	{
		printf("enter yourname:");
		gets(name);
		printf("enter password:");
		gets(password);

		while(1)
		{
			ret = fgets(line,sizeof(line),file);
			if (!ret){
				break;
			}
			sscanf(line,"%s %s",name_tmp,password_tmp);
			printf("name=%s,name_tmp=%s\n",name,name_tmp);
			printf("password=%s,password_tmp=%s\n",password,password_tmp );
			if (strcmp(name,name_tmp) == 0 && !strcmp(password,password_tmp))
			{
				break;
			}
		}

		if (ret)
		{
			printf("login success!");
			break;
		}	
		else
		{
			printf("login fail!");
			system("pause");
			system("cls");
			fseek(file,0,SEEK_SET); //好比翻书 -- java中没有？ 同样，流也一样。把指针指向头。
		}
	}
	

	system("cls") ;

	printf("=======menu============\n");
	printf("1,start game!\n");
	printf("2,over game!\n");


	return 0;
}