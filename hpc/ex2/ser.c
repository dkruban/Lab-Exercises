#include <stdio.h>
#include <stdlib.h>
#include <time.h>
void mul(int m, int n, int p, int *a, int *b, int *result){
	int i,j,k;
    for(i=0; i<m; i++) {
        for(j=0; j<p; j++) {
            result[i*p+j] = 0;
            for(k=0; k<n; k++) {
                result[i*p+j] += a[i*n+k] * b[k*p+j];
            }
	}
    }
    printf("\nMatrix multiplicatin done");
}
void add(int m, int p, int *a, int *b, int *result){
	int i,j;
    for(i=0; i<m; i++) {
        for(j=0; j<p; j++) {
            result[i*p+j] = a[i*p+j] + b[i*p+j];
        }
    }
    printf("\nMatrix addition done");
}
void trans(int m,int p,int *a,int *result){
	int i,j;
	for(i=0;i<m;i++){
		for(j=0;j<p;j++){
			result[i*p+j]=a[j*p+i];
		}
	}
	printf("\nMatrix transpose done");
}
void sub(int m, int p, int *a, int *b, int *result){
	int i,j;
    for(i=0; i<m; i++) {
        for(j=0; j<p; j++) {
            result[i*p+j] = a[i*p+j] - b[i*p+j];
        }
    }
    printf("\nMatrix subraction done");
}
double calc_determinant(int m, int *a) {
    if (m == 1) {
        return a[0];
    }   
    if (m == 2) {
        return a[0] * a[3] - a[1] * a[2];
    }
    int j,sub_i,sub_j;
    double det = 0.0;
    for (j = 0; j < m; j++) {
        int *submatrix = malloc((m-1)*(m-1)*sizeof(int));
        for (sub_i = 1; sub_i < m; sub_i++) {
            int sub_col = 0;
            for (sub_j = 0; sub_j < m; sub_j++) {
                if (sub_j != j) {
                    submatrix[(sub_i-1)*(m-1)+sub_col] = a[sub_i*m+sub_j];
                    sub_col++;
                }
            }
        }
        double sub_det = calc_determinant(m-1, submatrix);
        det += (j % 2 == 0 ? 1 : -1) * a[j] * sub_det;
        free(submatrix);
    }
    return det;
}
double determinant(int m, int *a) {
    return calc_determinant(m, a);
}

int main() {
    int m, n, p, i;   
    printf("Enter rows (m): "); 
    scanf("%d", &m);
    printf("Enter cols/rows (n): "); 
    scanf("%d", &n);
    printf("Enter cols (p): "); 
    scanf("%d", &p);
    int *a = malloc(m * n * sizeof(int));
    int *b = malloc(n * p * sizeof(int));
    int *mul_result = malloc(m * p * sizeof(int));
    int *add_result = malloc(m * p * sizeof(int));
    int *sub_result = malloc(m * p * sizeof(int));
    int *trans_result = malloc(m * p * sizeof(int));
    srand(time(0));
    for(i=0; i<m*n; i++) {
        a[i] = 10 + rand() % 90;
    }
    for(i=0; i<n*p; i++) {
        b[i] = 10 + rand() % 90;
    }
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    mul(m, n, p, a, b, mul_result);
    add(m, p, a, b, add_result);
    sub(m, p, a, b, sub_result);
    trans(m,p,a,trans_result);
    //double det_result = determinant(m, a);
    clock_gettime(CLOCK_MONOTONIC, &end);
    double serial_time = (end.tv_sec - start.tv_sec) + 
                        (end.tv_nsec - start.tv_nsec) / 1e9;
    
    printf("\nSerial Execution Time : %.9lf seconds", serial_time);
    printf("\n================================================\n");
    free(a);
    free(b);
    free(mul_result);
    free(add_result);
    free(sub_result);
    return 0;
}


