#include <stdio.h>
#include <omp.h>

int main() {
    int n;

    printf("Array size: ");
    scanf("%d", &n);
    int arr[n];

    printf("Elements: ");
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);

    int max_val = arr[0];

    #pragma omp parallel for reduction(max:max_val)
    for (int i = 0; i < n; i++) {
        if (arr[i] > max_val) max_val = arr[i];
    }

    printf("Max: %d\n", max_val);
    return 0;
}

