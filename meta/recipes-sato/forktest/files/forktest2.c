#include <unistd.h>
#include <stdio.h>

int
main (int argc, char **argv)
{
    pid_t childPID;

    childPID = fork();

    if (childPID)
        printf("Forked 1");
    else
        printf("Forked 2");

    return 0;
}
