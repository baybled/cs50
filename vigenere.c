//This is a more complicated shift key cipher using the ascii character set. This kind of cypher was used by Vigenère.
//You sorted out a C idiosyncracy of argv being a char pointer, you did this in 2 hours.

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main (int argc, char **argv) {

    //Do not start program if was not started from command line
    if (!argv[1] || argv[2]) {
        exit(0);
    }

    // counter for key
    int alphaC = 0;

    // Request plaintext from user and store in pt
    printf("plaintext: ");
    char pt[280];
    fgets (pt, 280, stdin);
    printf("ciphertext:");

    // go through each character, converting it from p(ascii) to cypher
    for (int c = 0, len = strlen(pt); c < len; c++) {

    if (!isalpha(pt[c])) {
        // preserve punctuation
        printf("%c", pt[c]);

    } else if (isalpha(pt[c])) {

        // find key char and value of key first
        int key = argv[1][alphaC % strlen(argv[1])];
        // add to counter
        alphaC++;

        // change key value if upper or lower
        if (isalpha(key)) {
            if (isupper(key)) {
                key = key - 65;
            } else {
                 key = key - 97;
            }
        }
        // lower alpha char
        if (islower(pt[c])) {

            // wrap around if needed
            if ((((pt[c] - 97) + key) % 26) > 26) {
                printf("%c", ((pt[c]-123) + key) % 26 + 97);

            // non wrap formula
            } else {
                printf("%c", ((pt[c]-97) + key) % 26 + 97);
            }

        // upper alpha char
        } else if (isupper(pt[c])) {

            // wrap around if needed
            if ((((pt[c] - 65) + key) % 26) > 26) {
                printf("%c", ((pt[c]- 91) + key) % 26 + 65);

            // non wrap formula
            } else {
                printf("%c", ((pt[c]-65) + key) % 26 + 65);
                    }
                }
            }
        }
    }
