#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

int main() {
    int n = 1000,i;
    long sum = 0;
    srand(time(NULL));

    int *a = malloc(n * sizeof(int));

    #pragma omp parallel for
    for (i = 0; i < n; i++) {
        a[i] = rand() % 100;
    }

    #pragma omp parallel for reduction(+:sum)
    for (i = 0; i < n; i++) {
        sum += a[i];
    }

    printf("Array Sum: %ld\n", sum);

    free(a);
    return 0;
}

