#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);
    int i=n+1;
    printf("hello\n");
    do {
        if (i<8) {
            printf("bye\n");
        }
        else {
            printf("hello\n");
        }
        i++;
    } while (i < 10);
    return 0;
}
