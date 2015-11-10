/*
 * hw10main_posted.c
 *
 *  Created on: May 02, 2015
 *  Modified from hex.c 4-15-15 version
 *  and hw10main.c 4-30-15 version
 *      Author: Tom Howell
 *
 *  Play the game of hex
 *  Sides are blue (b) and gold (g)
 *  b goes first and tries to complete a horizontal path
 *  g goes second and tries to complete a vertical path
 *
 *  interactive mode:  give sizes and b, g, or x when prompted
 *						to play b, g, or both by hand
 *
 *  automatic mode:  give sizes and n when prompted to play n games
 *                   and gather statistics
 *
 *  SizeV, SizeH are inside hexPos.  MAXH is the maximum value for each.
 *  Coordinates may be input from a file.  Here is an example.  The notes
 *  at the right are NOT part of the file.
 *		4 4			SizeV, SizeH
 *		x			Game type
 *		2 3			row col (blue)
 *		2 2			row col (gold)
 *		1 2
 *		1 3
 *		1 1
 *		0 3
 *		2 0
 *		3 1			row col (gold) Wins!
 *
 *  Parts of this program have been left for the student to complete:
 *  printBoard(hexPos), eval(hexPos), search or other helper functions
 *
 */


#include "hw10.h"

//extern void printBoard(hexPos *hp);
//extern char eval(hexPos *hp);

int pflag = 1;					//controls printing
int TotalPlaysLeft = 0;			//for statistics

/*
insert your printBoard, search and eval functions here.
make sure they are modified to use hexPos.
*/

//#include "print_eval.c"

int main(int argc, char *argv[]){

	char winner = ' ';		//initialize to blank
	int i = 0, nPlays = 1;
	int row, col;
	int SizeV, SizeH;
	char arg3[16];
	int iBlue = FALSE, iGold = FALSE;		//interactive flags
	int Bwins = 0, Gwins = 0;
	int NobodyWins = 0;
	unsigned int seed;
	FILE *fpi = stdin;

	hexPos hp;			//place to store game config
	hexPos *php = &hp;	//pointer to hp

	//  Command line interface changed to file input
	//  Leave the command line empty to use keyboard input
	//  Use ./hw10 example.txt
	//  to play the game with inputs from the example file.
	//  Students can make additional input files for testing
	//  specific parts of their programs.
	if (argc >= 2) {
		fpi = fopen(argv[1], "r");		//name of file to be used such as example.txt
	}

	while (!feof(fpi)){					//This allows for more than
										//one game per input file.
										//Make sure your file ends right after
										//the last input -- no spaces or \n

		nPlays = 1;									//reset for each group
		i = 0;
		iBlue = FALSE;
		iGold = FALSE;
		TotalPlaysLeft = 0;
		Bwins = 0;
		Gwins = 0;
		NobodyWins = 0;
		//seed = (unsigned long long int) time(NULL);  //for non-repeating random numbers
		seed = 17;			//make it repeatable
		srand(seed);

		fscanf(fpi, "%d %d", &SizeV, &SizeH);		//read board dimsnsions
		printf("Size %d x %d\n", SizeV, SizeH);


		if (SizeV > 11 || SizeH > 11){
			printf("Usage: SizeV SizeH [nPlays] or [b] [g] [x] for interactive play.\n");
			return -1;
		}

		fscanf(fpi, "%s", arg3);				//arg3 is "b", "g", "x", or nPlays
			if (strcmp(arg3, "b") == 0) iBlue = TRUE;
			if (strcmp(arg3, "g") == 0) iGold = TRUE;
			if (strcmp(arg3, "x") == 0) iBlue = iGold = TRUE;
			pflag = iBlue || iGold;			//print if playing interactively

			if(!iBlue && !iGold) {
				nPlays = atoi(arg3);
				pflag = (nPlays == 1);		//print only for nPlays == 1
			}

		while (i++ < nPlays){				//play nPlays games
											//nPlays will be 1 for interactive games
			for(row = 0; row < SizeV; row++){	//initialize the grid
				for(col = 0; col < SizeH; col++){
					php -> grid[row][col] = ' ';
				}
			}
			//initialize the rest of the hexPos
			php -> SizeV = SizeV;
			php -> SizeH = SizeH;
			php -> toPlay = blue;			//blue always goes first
			php -> playsLeft = SizeV * SizeH;

			while (php -> playsLeft > 0){
				printf("plays left: %d", php->playsLeft);
//				printf("blue/gold %d/%d\n", iBlue, iGold);
				printf("plays left: %d\n", php->playsLeft);
				if (iBlue || iGold){
					if(iBlue && php -> toPlay == blue) mymove(php, fpi);  //I play blue
					else if(iGold && php -> toPlay == gold) mymove(php, fpi);  //I play gold
					else randomMove(php);   //if playing only one side interactively
											//play the other side randomly
				}
				else {
					randomMove(php);		//play both sides randomly when nPlays > 1
				}

				php -> playsLeft--;				//update hexPos after the move
				php -> toPlay ^= 1;				//alternate blue/gold
				if (iBlue || iGold){
					printBoard(php);
					printf("\n%c to play  %d plays left\n", (php -> toPlay)? GC : BC, php -> playsLeft);
					//fflush(stdout);
				}
				winner = eval(php);			//remember to update your eval to use hexPos
				if (winner != 0) break;		//stop if somebody won
			}
			if (pflag) {
				printBoard(php);			//show winning position
			}
			//accumulate statistics
			if (winner == BC) Bwins++;
			else if (winner == GC) Gwins++;
			else NobodyWins++;
		}
		if (nPlays > 0){
			//print statistics
			printf("Games played:\t%d\n\n", nPlays);
			printf("Blue wins: %d  Gold wins: %d\n", Bwins, Gwins);
			printf("Average plays left: %.2lf\n\n", (double)TotalPlaysLeft/nPlays);
		}
	}
	fclose(fpi);
	return 0;
}
