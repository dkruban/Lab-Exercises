[23bcs102@mepcolinux ex5]$cat sum.c 
#include <stdio.h>
#include <pthread.h>

#define MAX 100
int arr[MAX];
int n;
int sum = 0;
pthread_mutex_t lock;

typedef struct {
    int start;
    int end;
    int local_sum; 
} Data;

void *sum_part(void *arg) {
    Data *d = (Data *)arg;
    d->local_sum = 0;
    for (int i = d->start; i < d->end; i++) {
        d->local_sum += arr[i];
    }
    
    pthread_mutex_lock(&lock);
    sum += d->local_sum;
    pthread_mutex_unlock(&lock);
    return NULL;
}

int main() {
    pthread_t t1, t2;
    printf("Enter number of elements (even): ");
    scanf("%d", &n);
    printf("Enter elements:\n");
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);
    Data d1,d2;
    pthread_mutex_init(&lock, NULL);
    if(n%2==0)
    {
	    Data d1 = {0, n/2, 0};
	    Data d2 = {n/2, n, 0};
    }
    else
    {
	    Data d1={0,n/2,0};
	    Data d2={n/2,n,0};
    }
    pthread_create(&t1, NULL, sum_part, &d1);
    pthread_create(&t2, NULL, sum_part, &d2);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Thread 1 Local Sum: %d\n", d1.local_sum);
    printf("Thread 2 Local Sum: %d\n", d2.local_sum);

    pthread_mutex_destroy(&lock);
    printf("Total Sum = %d\n", sum);
    return 0;
}


Enter number of elements (even): 5
Enter elements:
4
5
6
7
1
Thread 1 Local Sum: 9
Thread 2 Local Sum: 14
Total Sum = 23

