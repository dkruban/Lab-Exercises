#include <mpi.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_STRING_LENGTH 100
#define TAG_TYPE1 1
#define TAG_TYPE2 2
#define MASTER 0

// Function to convert string to uppercase
void toUpperCase(char *str) {
    for (int i = 0; str[i] != '\0'; i++) {
        str[i] = toupper(str[i]);
    }
}

// Function to check if string is palindrome
int isPalindrome(char *str) {
    int len = strlen(str);
    int i, j;
    
    // Remove spaces and convert to lowercase for comparison
    char temp[MAX_STRING_LENGTH];
    int k = 0;
    for (i = 0; str[i] != '\0'; i++) {
        if (!isspace(str[i])) {
            temp[k++] = tolower(str[i]);
        }
    }
    temp[k] = '\0';
    
    // Check palindrome
    for (i = 0, j = k - 1; i < j; i++, j--) {
        if (temp[i] != temp[j]) {
            return 0;
        }
    }
    return 1;
}

int main(int argc, char *argv[]) {
    int rank, size;
    char message[MAX_STRING_LENGTH];
    MPI_Status status;
    
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    if (rank == MASTER) {
        // Master process
        printf("Master process (rank %d) is ready to receive messages from %d processes\n\n", rank, size - 1);
        
        // Receive messages from all other processes
        for (int i = 1; i < size; i++) {
            MPI_Recv(message, MAX_STRING_LENGTH, MPI_CHAR, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
            
            int source = status.MPI_SOURCE;
            int tag = status.MPI_TAG;
            
            if (tag == TAG_TYPE1) {
                // Type 1: Convert to uppercase
                toUpperCase(message);
                printf("[Type 1] Rank %d (Odd): Original message converted to UPPERCASE: \"%s\"\n", source, message);
            } else if (tag == TAG_TYPE2) {
                // Type 2: Check palindrome
                int is_palin = isPalindrome(message);
                printf("[Type 2] Rank %d (Even): Message \"%s\" is %s palindrome\n", 
                       source, message, is_palin ? "a" : "NOT a");
            }
        }
        
        printf("\nAll messages processed by master.\n");
        
    } else {
        // Non-master processes
        if (rank % 2 == 1) {
            // Odd ranked process - send Type 1 message
            sprintf(message, "hello from process %d", rank);
            printf("Rank %d (Odd) sending: \"%s\" with Type 1\n", rank, message);
            MPI_Send(message, strlen(message) + 1, MPI_CHAR, MASTER, TAG_TYPE1, MPI_COMM_WORLD);
        } else {
            // Even ranked process - send Type 2 message
            // Using palindromes and non-palindromes for demonstration
            if (rank % 4 == 0) {
                sprintf(message, "racecar");  // palindrome
            } else {
                sprintf(message, "process %d", rank);  // not palindrome
            }
            printf("Rank %d (Even) sending: \"%s\" with Type 2\n", rank, message);
            MPI_Send(message, strlen(message) + 1, MPI_CHAR, MASTER, TAG_TYPE2, MPI_COMM_WORLD);
        }
    }
    
    MPI_Finalize();
    return 0;
}

