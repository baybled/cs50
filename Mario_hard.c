//This program prints out half a pyramid of a specified height

#include <stdio.h>

int main(void)
{
    int height;
    // Ask user to set height
    do
    {
        printf("Please enter a height for the pyramid\n");

        scanf("%d", &height);
    }
    while (height < 0 || height > 23);

    // draw pyramid

    int total = height + 1;

    for (int row = 0; row < total; row++)
    {
        // sets initial space at max len - 2, changes with row
        int spaces = (total - (1 + row));

        while (spaces > 0){
            printf("%s", " ");
            spaces--;
        }

        // sets initial hash at 2, changes with row
        int hashes = (total - (row + 1));

        while (hashes < total){
            printf("%s", "#");
            hashes++;}

        printf("\n");

    }



}
