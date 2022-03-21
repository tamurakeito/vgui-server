#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

void* func1(void* ptr) {
    char cmd[1024];
    sprintf(cmd, "python3 test.py");
    system(cmd);
    return NULL;
}

void* func2(void* ptr) {
    int second = 5;
    sleep(second);
    printf("Hello!\n");
    char cmd2[1024];
    sprintf(cmd2, "testtesttest!!!");
    system(cmd2);
    return NULL;
}

int main()
{
    pthread_t thread1, thread2;

    pthread_create(&thread1, NULL, func1, NULL);
    pthread_create(&thread2, NULL, func2, NULL);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    return 0;
}