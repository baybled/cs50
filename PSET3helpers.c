/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <stdbool.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
	//Set left, right and middle
	int l = 0;
	int r = n-1;
	int m = (l + r)/2;

	// Cut search range if middle is left or right of value until range is 1
	while ((r - l) != 1)
	{
		if (values[m] < value)
		{
			l = m + 1;
		} 
		else if (values[m] > value)
		{
			r = m - 1;
		}

		// Check for needle in haystack of 1
		if (r == value||l == value)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
	// Go through the loop, each position as p
	for (int i = 0; i < (n -1); i++)
	{
		// Record current position as minumum
		int min = i;

		// Find smaller number by going through the loop till end
		for (int j = i + 1; j < n; j++)
		{
			if (values[j] < values[min])
			{
				min = j;
			}
		}
		
		// Swap if current is not minumum
		if (min != i)
		{
			int temp = values[i];
			values[min] = values[i];
			values[i] = temp;
		}
	} 
    return;
}
