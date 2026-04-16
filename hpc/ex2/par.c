#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/wait.h>
#include <time.h>
void mul(int m,int p,int *a,int *b,int *rp, double *tmem, int idx) {
    struct timespec st, en;
    clock_gettime(CLOCK_MONOTONIC, &st);
    int i,k,j;
    for(j=0; j<p; j++) {
        rp[idx*p+j] = 0;
        for(k=0; k<m; k++) {
            rp[idx*p+j] += a[idx*m+k] * b[k*p+j];
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &en);
    tmem[idx] = (en.tv_sec - st.tv_sec) + (en.tv_nsec - st.tv_nsec) / 1e9;
    printf("\nMatrix multiplication done");
}
void add(int m,int p,int *a,int *b,int *rp,double *tmem,int idx)
{
    struct timespec st, en;
    clock_gettime(CLOCK_MONOTONIC, &st);
    int i,k,j;
    for(i=0; i<m; i++) {
        for(j=0; j<p; j++) {
            rp[i*p+j] = a[i*p+j] + b[i*p+j];
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &en);
    tmem[idx] = (en.tv_sec - st.tv_sec) + (en.tv_nsec - st.tv_nsec) / 1e9;
    printf("\nMatrix addition done");
}
void sub(int m,int p,int *a,int *b,int *rp,double *tmem,int idx)
{
    struct timespec st, en;
    clock_gettime(CLOCK_MONOTONIC, &st);
    int i,k,j;
    for(i=0; i<m; i++) {
        for(j=0; j<p; j++) {
            rp[i*p+j] = a[i*p+j] - b[i*p+j];
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &en);
    tmem[idx] = (en.tv_sec - st.tv_sec) + (en.tv_nsec - st.tv_nsec) / 1e9;
    printf("\nMatrix subraction done");
}
void trans(int m,int p,int *a,int *result,double *tmem,int idx){
	struct timespec st, en;
	clock_gettime(CLOCK_MONOTONIC, &st);
	int i,j;
	for(i=0;i<m;i++){
		for(j=0;j<p;j++){
			result[i*p+j]=a[j*p+i];
		}
	}
	clock_gettime(CLOCK_MONOTONIC, &en);
        tmem[idx] = (en.tv_sec - st.tv_sec) + (en.tv_nsec - st.tv_nsec) / 1e9;
	printf("\nMatrix transpose done");
}

double calc_determinant(int m, int *a) {
    if (m == 1) {
        return a[0];
    }
    if (m == 2) {
        return a[0] * a[3] - a[1] * a[2];
    }
    double det = 0.0;
    int j,sub_i,sub_j;
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
void determinant(int m, int *a, double *det_result, double *tmem, int idx)
{
    struct timespec st, en;
    clock_gettime(CLOCK_MONOTONIC, &st);
    det_result[0] = calc_determinant(m, a);
    clock_gettime(CLOCK_MONOTONIC, &en);
    tmem[idx] = (en.tv_sec - st.tv_sec) + (en.tv_nsec - st.tv_nsec) / 1e9;
}

int main() {
    int m, n, p, i, j, k;
    printf("Enter rows (m): "); scanf("%d", &m);
    printf("Enter cols/rows (n): "); scanf("%d", &n);
    printf("Enter cols (p): "); scanf("%d", &p);
    int sz = (m*n + n*p + m*p) * sizeof(int);
    int sid = shmget(IPC_PRIVATE, sz, IPC_CREAT | 0666);
    int *mem = shmat(sid, 0, 0);
    int tid = shmget(IPC_PRIVATE, m * sizeof(double), IPC_CREAT | 0666);
    double *tmem = shmat(tid, 0, 0);
    int did = shmget(IPC_PRIVATE, sizeof(double), IPC_CREAT | 0666);
    double *det_mem = shmat(did, 0, 0);

    int *a = mem;
    int *b = mem + m*n;
    int *rp = mem + m*n + n*p;

    srand(time(0));
    for(i=0; i<m*n; i++) a[i] = 10 + rand() % 90;
    for(i=0; i<n*p; i++) b[i] = 10 + rand() % 90;

    
    for(i=0; i<4; i++) {
        if(fork() == 0) {
            if(i==0)
            {
                mul(m, p, a, b, rp, tmem, 0);
            }
            else if(i==1)
            {
                add(m, p, a, b, rp, tmem, 1);
            }
            else if(i==2)
            {
                sub(m, p, a, b, rp, tmem, 2);
            }
            else
            {
                trans(m,p,a,rp,tmem, 3);
            }
            exit(0);
        }
    }

    for(i=0; i<4; i++) wait(NULL);

    double t_par = -1;
    for(i=0; i<4; i++) {
        if(t_par < tmem[i]) t_par = tmem[i];
    }
   
    printf("\nParallel Execution Time : %lf seconds", t_par);
    printf("\n================================================\n");
    shmdt(mem); 
    shmdt(tmem);
    shmdt(det_mem);
    shmctl(sid, IPC_RMID, NULL); 
    shmctl(tid, IPC_RMID, NULL);
    shmctl(did, IPC_RMID, NULL);
    return 0;
}

