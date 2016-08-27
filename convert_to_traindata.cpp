#include<stdio.h>
#include<string.h>
FILE *fin=fopen("input.txt","r");
FILE *fout=fopen("output.txt","w");
char str[110];
int arr[20][20], cnt;
void print(int x, int y)
{
    fprintf(fout, "%d ", (x-1)*15 + (y-1));
    for(int i=1; i<=15; ++i)
    {
        for(int j=1; j<=15; ++j) fprintf(fout, "%d ", arr[i][j]);
    }
    fprintf(fout, "\n");
    //printf("%d\n", ++cnt);
    return;
}
int main()
{
    int i, j, turn;
    fscanf(fin, "%s", str);
    while(1)
    {
        ++cnt;
        for(i=1; i<=15; ++i)
        {
            for(j=1; j<=15; ++j) arr[i][j]=0;
        }
        fscanf(fin, "%s", str);
        if(strcmp(str, "white")==0)
        {
            turn = -1;
            while(1)
            {
                if(fscanf(fin, "%s", str)==0) return 0;
                if(str[0]=='h' && str[1]=='t' && str[2]=='t' && str[3]=='p') break;
                i = str[0]-'a'+1;
                if(str[2]!=NULL) j = 10+(str[2]-'0');
                else j = (str[1]-'0');

                if(turn==1) print(i, j);
                arr[i][j] = turn;
                turn = -turn;
            }
        }
        else if(strcmp(str, "black")==0)
        {
            turn = 1;
            while(1)
            {
                if(fscanf(fin, "%s", str)==0) return 0;
                if(str[0]=='h' && str[1]=='t' && str[2]=='t' && str[3]=='p') break;
                i = str[0]-'a'+1;
                if(str[2]!=NULL) j = 10+(str[2]-'0');
                else j = (str[1]-'0');

                if(turn==1) print(i, j);
                arr[i][j] = turn;
                turn = -turn;
            }
        }
        else
        {
            while(1)
            {
                if(fscanf(fin, "%s", str)==0) return 0;
                if(str[0]=='h' && str[1]=='t' && str[2]=='t' && str[3]=='p') break;
            }
        }
        printf("%d\n", cnt);
        if(cnt==1191) break;
    }
}
