#include <stdio.h>
#include <pthread.h>

/* Thread function */
void* greeting(void* arg) {
    printf("Hello! Greetings from Child Thread.\n");
    pthread_exit(NULL);
}

int main() {
    pthread_t t;

    printf("Greetings from Main Thread.\n");

    pthread_create(&t, NULL, greeting, NULL);
    pthread_join(t, NULL);

    printf("Main Thread finished execution.\n");
    return 0;
}

