#include <stdio.h>
#include <pthread.h>
int sum = 0;
int n;

void* find_sum(void* arg) {
    int i;
    for (i = 1; i <= n; i++) sum += i;
    pthread_exit(NULL);
}

int main() {
    pthread_t t;

    printf("\tEnter a number: ");
    scanf("%d", &n);

    pthread_create(&t, NULL, find_sum, NULL);
    pthread_join(t, NULL);

    printf("\tSum of first %d numbers = %d\n", n, sum);

    return 0;
}
