#include <stdio.h>

int global_var = 42;

int *get_global_ptr() {
    return &global_var;
}

int main() {
    int *ptr = get_global_ptr();
    printf("Global variable value: %d\n", *ptr);
    return 0;
}
