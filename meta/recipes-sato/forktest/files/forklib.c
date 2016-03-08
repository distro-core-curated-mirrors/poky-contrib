#include <unistd.h>
#include <stdio.h>
#include "forklib.h"

int
forklib(void)
{
    pid_t childPID;

    childPID = fork();

    if (childPID)
        printf("Forked 1");
    else
        printf("Forked 2");

    return 0;
}
