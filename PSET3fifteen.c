/**
 * fifteen.c
 *
 * Implements Game of Fifteen (generalized to d x d).
 *
 * Usage: fifteen d
 *
 * whereby the board's dimensions are to be d x d,
 * where d must be in [DIM_MIN,DIM_MAX]
 *
 * Note that usleep is obsolete, but it offers more granularity than
 * sleep and is simpler to use than nanosleep; `man usleep` for more.
 */
 
#define _XOPEN_SOURCE 500

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#include "cs50.h"

// constants
#define DIM_MIN 3
#define DIM_MAX 9

// dimensions
int d;

// board
int board[DIM_MAX][DIM_MAX];

// numbers and grid
int grid[DIM_MAX-1][DIM_MAX-1];

// prototypes
void clear(void);
void greet(void);
void init(void);
void draw(void);
void swap(int *a, int *b);
bool move(int tile);
bool won(void);

int main(int argc, char* argv[])
{
    int tile = 0;
    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    // ensure valid dimensions
    d = atoi(argv[1]);
    if (d < DIM_MIN || d > DIM_MAX)
    {
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
            DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    // open log
    FILE *file = fopen("log.txt", "w");
    if (file == NULL)
    {
        return 3;
    }

    // greet user with instructions
    greet();

    // initialize the board
    init();

    // accept moves until game is won
    while (true)
    {
        // clear the screen
        clear();

        // draw the current state of the board
        draw();

        // log the current state of the board (for testing)
        // i = rows, j = columns
        for (int i = 0; i < d; i++)
        {
            for (int j = 0; j < d; j++)
            {
                fprintf(file, "%i", board[i][j]);
                // If needed, print column
                if (j < d - 1)
                {
                    fprintf(file, "|");
                }
            }
            fprintf(file, "\n");
        }
        fflush(file);

        // check for win
        if (won())
        {
            printf("ftw!\n");
            break;
        }

        // prompt for move
        printf("Tile to move: ");
        scanf("%i", &tile);
        
        // quit if user inputs 0 (for testing)
        if (tile == 0)
        {
            break;
        }

        // log move (for testing)
        fprintf(file, "%i\n", tile);
        fflush(file);

        // move if possible, else report illegality
        if (!move(tile))
        {
            printf("\nIllegal move.\n");
            usleep(500000);
        }

        // sleep thread for animation's sake
        usleep(500000);
    }
    
    // close log
    fclose(file);

    // success
    return 0;
}

/**
 * Clears screen using ANSI escape sequences.
 */
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}

/**
 * Greets player.
 */
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(2000000);
};


/**
 * Initializes the game's board with tiles numbered 1 through d*d - 1
 * (i.e., fills 2D array with values but does not actually print them).  
 */
void init(void)
{
    int nums[DIM_MAX * DIM_MAX];
    srand(time(NULL));

    // Set initial array
    for (int i = 0; i < d * d; i++)
    {
        nums[i] = i;
    }

    // Shuffle array  
    for (int j = 0; j < d * d; j++)
    {
        int t = rand() % (d * d);
        int u = nums[j];
        nums[j] = nums[t];
        nums[t] = u;
    }
    printf("\n");

    // Allows game to be winnable if board is even
    if (d % 2)
    {
        for (int s = 0; s < d * d; s++)
        {
            if (nums[s] == 1)
            {
                nums[s] = 2;
            }
            else if (nums[s] == 2)
            {
                nums[s] = 1;
            }
        }
    }

    // Place array in grid
    for (int k = 0; k < d; k++)
    {
        for (int h = 0; h < d; h++)
        {
            grid[k][h] = nums[d * k + h];
        }
    }
}

/**
 * Prints the board in its current state.
 */
void draw(void)
{
    // Go row by row, column by column, include pipes and underscore
    for (int i = 0; i < d; i++)
    {
        for (int j = 0; j < d; j++)
        {
            if (grid[i][j] == 0)
            {
                printf("__");
            }
            else 
            {
                printf("%2i", grid[i][j]);
            }

            if (j != d - 1)
            {
                printf("|");
            }
        }
        printf("\n");
    }
}

/**
 * If tile borders empty space, moves tile and returns true, else
 * returns false. 
 */
bool move(int tile)
{
    // Find empty and move tiles' positions
    for (int i = 0; i < d; i++)
    {
        for (int j = 0; j < d; j++)
        {
            if (grid[i][j] == 0)
            {
                // checks if vertically or horizontally adjacent tiles are request for move and moves if case is found true
                if (grid[i-1][j] == tile)
                {
                    grid[i][j] = tile;
                    grid[i-1][j] = 0;
                    return true;
                }
                else if (grid[i+1][j] == tile)
                {
                    grid[i][j] = tile;
                    grid[i+1][j] = 0;
                    return true;
                }
                else if (grid[i][j-1] == tile)
                {
                    grid[i][j] = tile;
                    grid[i][j-1] = 0;
                    return true;
                }
                else if (grid[i][j+1] == tile)
                {
                    grid[i][j] = tile;
                    grid[i][j+1] = 0;
                    return true;
                }

            }
        }
    }

    return false;
}

/**
 * Returns true if game is won (i.e., board is in winning configuration), 
 * else false.
 */
bool won(void)
{
    for (int i = 0; i < d; i++)
    {
        for (int j = 0; j < d; j++)
        {
            // if tile is on end of row, checks against 0th tile in next row
            if (j == (d -1))
            {
                if (grid[i][j] > grid[i+j][0])
                {
                    return false;
                }
            }

            // if tile current tile is bigger than next tile, game not over
            if (grid[i][j] > grid[i][j+1])
            {
                return false;
            }
        }
    }
    return true;
}
