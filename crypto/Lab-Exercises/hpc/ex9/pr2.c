#include <stdio.h>
#include <omp.h>

int main() {
    int n, target, count = 0;

    printf("Array size: ");
    scanf("%d", &n);
    int arr[n];

    printf("Elements: ");
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);

    printf("Target: ");
    scanf("%d", &target);

    #pragma omp parallel for reduction(+:count)
    for (int i = 0; i < n; i++) {
        if (arr[i] > target) count++;
    }

    printf("Count: %d\n", count);
    return 0;
}

