#include <stdio.h>
#include <pthread.h>

#define MAX 10

int A[MAX][MAX], B[MAX][MAX];
int add[MAX][MAX], mul[MAX][MAX];
int n;

void* matrix_addition(void* arg) {
    int i, j;
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            add[i][j] = A[i][j] + B[i][j];
        }
    }
    pthread_exit(NULL);
}

void* matrix_multiplication(void* arg) {
    int i, j, k;
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            mul[i][j] = 0;
            for (k = 0; k < n; k++) {
                mul[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    pthread_exit(NULL);
}

int main() {
    pthread_t t1, t2;
    int i, j;

    printf("Enter matrix size (N): ");
    scanf("%d", &n);

    printf("\nEnter Matrix A:\n");
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            scanf("%d", &A[i][j]);

    printf("\nEnter Matrix B:\n");
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            scanf("%d", &B[i][j]);


    pthread_create(&t1, NULL, matrix_addition, NULL);
    pthread_create(&t2, NULL, matrix_multiplication, NULL);


    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("\nMatrix Addition Result:\n");
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++)
            printf("%d ", add[i][j]);
        printf("\n");
    }

    printf("\nMatrix Multiplication Result:\n");
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++)
            printf("%d ", mul[i][j]);
        printf("\n");
    }

    return 0;
}

