//This is a simple shift key cipher using the ascii character set. This kind of cypher was used by Ceasar.
//Possible C idiosyncrasy. You learnt to filter by size, in terms of scope size AND filter result set size.

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main (int argc, char **argv) {

    //Do not start program if was not started from command line
    if (!argv[1]) {
        exit(0);
    }

    // set arrays for plaintext and cyphertext

    // Request plaintext from user and store in pt
    printf("plaintext: ");
    char pt[280];
    fgets (pt, 280, stdin);
    printf("ciphertext:");

    // go through each character, converting it from p(ascii) to cypher
    for (int c = 0, len = strlen(pt); c < len; c++) {

    // set value key for each letter
    long k = strtol(argv[1], NULL, 10);

    if (!isalpha(pt[c])) {
        // preserve punctuation
        printf("%c", pt[c]);

    } else if (isalpha(pt[c])) {
        // lower alpha char
        if (islower(pt[c])) {

            // wrap around if needed and k is pos
            if ((((pt[c] - 97) + k) % 26) > 26) {
                printf("%c", ((pt[c]-123) + k) % 26 + 97);

            // wrap around if needed and k is neg
            } else if ((((pt[c] - 97) + k) % 26) < 0) {
                printf("%c", ((pt[c]- 71) + k) % 26 + 97);

            // non wrap formula
            } else {
                printf("%c", ((pt[c]-97) + k) % 26 + 97);
            }

        // upper alpha char
        } else if (isupper(pt[c])) {

            // wrap around if needed and k is pos
            if ((((pt[c] - 65) + k) % 26) > 26) {
                printf("%c", ((pt[c]- 91) + k) % 26 + 65);

            // wrap around if needed and k is neg
            } else if ((((pt[c] - 65) + k) % 26) < 0) {
                printf("%c", ((pt[c]- 39) + k) % 26 + 65);

            // non wrap formula
            } else {
                printf("%c", ((pt[c]-65) + k) % 26 + 65);
                    }
                }
            }
        }
    }
