#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <time.h>

#define QUEUE_SIZE 8
#define NUM_JOBS 10

typedef struct {
    int a, b;
    int op; 
} job_t;

job_t queue[QUEUE_SIZE];
int front = 0, rear = 0;

sem_t sem_empty; 
sem_t sem_full;  
sem_t sem_mutex; 

FILE *result_fp;

const char* op_to_str(int op) {
    if (op == 1) return "add";
    if (op == 2) return "sub";
    if (op == 3) return "mul";
    if (op == 4) return "div";
    return "?";
}

void enqueue(job_t j) {
    queue[rear] = j;
    rear = (rear + 1) % QUEUE_SIZE;
}

job_t dequeue() {
    job_t j = queue[front];
    front = (front + 1) % QUEUE_SIZE;
    return j;
}

void* producer(void* arg) {
    for (int i = 0; i < NUM_JOBS; ++i) {
        job_t job;
        job.a = rand() % 51;
        job.b = rand() % 51;
        job.op = (rand() % 4) + 1; 

        sem_wait(&sem_empty);  
        sem_wait(&sem_mutex);   

        enqueue(job);
        printf("PRODUCED: %d %s %d\n", job.a, op_to_str(job.op), job.b);

        sem_post(&sem_mutex);   
        sem_post(&sem_full);    

        usleep(100000); 
    }
    for (int k = 0; k < 4; ++k) {
        sem_wait(&sem_empty);
        sem_wait(&sem_mutex);
        enqueue((job_t){0, 0, 0});
        sem_post(&sem_mutex);
        sem_post(&sem_full);
    }

    return NULL;
}

void* consumer(void* arg) {
	int id = *(int*)arg;
	free(arg);
    while (1) {
        sem_wait(&sem_full);   
        sem_wait(&sem_mutex);  
        job_t job = dequeue();
        sem_post(&sem_mutex);  
        sem_post(&sem_empty);  

        if (job.op == 0) break; 

        int res;
        switch (job.op) {
            case 1: res = job.a + job.b; break;
            case 2: res = job.a - job.b; break;
            case 3: res = job.a * job.b; break;
            case 4: res = (job.b == 0 ? 0 : job.a / job.b); break;
            default: res = 0;
        }
	printf("Thread %d computing : %d %s %d \n", id, job.a, op_to_str(job.op), job.b);
        fprintf(result_fp, "%d %s %d = %d\n", job.a, op_to_str(job.op), job.b, res);
        fflush(result_fp);

        usleep(150000); 
    }
    return NULL;
}

int main() {
    srand(time(NULL));
    result_fp = fopen("result.txt", "w");
    if (!result_fp) {
        perror("result.txt");
        exit(1);
    }

    sem_init(&sem_empty, 0, QUEUE_SIZE); 
    sem_init(&sem_full,  0, 0);         
    sem_init(&sem_mutex, 0, 1);       

    pthread_t prod, cons[4];
    pthread_create(&prod, NULL, producer, NULL);
    for (int i = 0; i < 4; ++i){
	int *id = (int*)malloc(sizeof(int));
	if(id==NULL)
	{
		perror("error");
		exit(0);
	}
	*id = i; 
        pthread_create(&cons[i], NULL, consumer,id);

    }

    pthread_join(prod, NULL);
    for (int i = 0; i < 4; ++i)
        pthread_join(cons[i], NULL);

    fclose(result_fp);
    printf("Done. See result.txt\n");
    return 0;
}
