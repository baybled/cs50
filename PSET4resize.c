/**
 * resizes a BMP piece by piece.
 */
   
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int resize;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        printf("Please enter the command correctly e.g. 'resize 4 small.bmp large.bmp'\n");
        fprintf(stderr, "Usage: ./resize infile outfile\n");
        return 1;
    }

    // remember file info
    char *infile = argv[2];
    char *outfile = argv[3];

    // remember resize info
    int resize = atoi(argv[1]);


    // Make sure the resize number is betwene one and a hundred
    if (resize > 100 || resize < 0)
    {
        printf("Please ensure the resize number is within 100 e.g. 'resize 4 small.bmp large.bmp'\n");
        fprintf(stderr, "Integer outside range\n");
        return 1;
    }

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("File could not be opened\n");
        fprintf(stderr, "Could not open https://en.wikipbiedia.org/wiki/BMP_file_format#DIB_header_(bitmap_information_header)infile.\n");
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("File could not be created.\n");
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        printf("Please check file is an BOTH uncorrupted AND 24-bit BMP.\n");
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // save old and set new image info 
    BITMAPINFOHEADER old_bi;
    old_bi.biWidth = bi.biWidth;
    old_bi.biHeight = bi.biHeight;
    bi.biWidth = bi.biWidth * resize;
    bi.biHeight = bi.biHeight * resize;

    // determine padding for scanlines
    int old_padding = (4 - (old_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // determine new image padding

    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // resize info header
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + old_padding * abs(bi.biHeight));
    
    // resize file header
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    int c = resize;

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {

        // iterate over pixels in scanline
        for (int j = 0; j < old_bi.biWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // repeat triple for resize
            for (int l = 0; l < resize; l++) //!!3
            {
                
            // repeatedly write RGB triple to outfile, based on resize number
            fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }


        }

            // skip over padding, if any
            fseek(inptr, old_padding, SEEK_CUR);

            // add new padding
            for (int m = 0; m < old_padding * resize; m++)
                {
                    fputc(0x00, outptr);
                }

            if (c != 0)
            {
                // send inptr back to the beginning of line
                fseek(inptr, -(old_bi.biWidth * sizeof(RGBTRIPLE) + old_padding), SEEK_CUR);
            }
            else
            {
                c = resize;
            }
                       
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
