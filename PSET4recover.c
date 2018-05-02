/*
**	recovers jpeg files from a memory card image
*/

#include <stdlib.h>
#include <stdio.h>

#define FATBLOCK 512

int main(int argc, char *argv[])
{
	// ensure proper usage
	if (argc == 1 || argc > 2)
	{
		printf("Retry, but this time, trying writing something like this ./recover card.raw\n");
		return 1;
	}

	// open data stream
	FILE *file = fopen(argv[1], "r");

	// stream does not hold data, exit
	if (file == NULL)
	{
		printf("The file is empty\n");
		return 1;
	}

	// set character array and name for jpg
	char filename[8];
	int name = 0;

	// temporary storage
	unsigned char buffer[FATBLOCK];
	
	// Go through each 512 block of bytes until the end of a file
	while (!feof(file))
	{
		// check for jpeg header;
		if (buffer[0] == 0xff &&
			buffer[1] == 0xd8 &&
			buffer[2] == 0xff &&
			(buffer[3] & 0xf0) == 0xe0)
		{
			// make new file 000.jpg format
			sprintf(filename, "%03i.jpg", name);
			FILE *recover = fopen(filename, "w");
			name++;
			
		while (buffer[0] != 0xff &&
				buffer[1] != 0xd8 &&
				buffer[2] != 0xff &&
				(buffer[3] & 0xf0) != 0xe0)
			{
				fwrite(&buffer, FATBLOCK, 1, recover);
				fread(&buffer, FATBLOCK, 1, file);
			}

		fclose(recover);
		}

		fread(&buffer, FATBLOCK, 1, file);
	}
	fclose(file);
	return 0;
}