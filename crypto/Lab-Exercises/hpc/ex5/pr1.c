#include<stdio.h>
#include<pthread.h>
int n=0;
void *greetings(void *args){
	printf("Hello from thread %d \n",n++);
	pthread_exit(NULL);
}

int main(){
   printf("Enter no of process : ");
   int size;
   scanf("%d",&size);
   printf("Main Thread starting\n");
   pthread_t p[size];
   for(int i=0;i<size;i++)
      pthread_create(&p[i],NULL,greetings,NULL);   
   for(int i=0;i<size;i++)
      pthread_join(p[i],NULL);
   printf("Main thread exiting\n");
   return 0;
}
