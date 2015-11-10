/*
 * hw8_test.c
 *
 *  Created on: Apr 18, 2015
 *      Author: Michael
 */
/*
*	T. Howell
*	3-30-15
*	test program for hw8
*/
#include <stdio.h>
//#include <ctype.h>   //for tolower (if needed)
#include "hw8.h"


//controls extra printing for debug mode
#ifdef DEBUG
	int pflag = 1;
#else
	int pflag = 0;
#endif

char game2 [ ][maxH] = {
			{'b', 'b', 'g', 'b', ' '},
			{'b', 'b', 'g', ' ', 'b'},
			{'b', 'g', 'b', 'g', 'b'},
			{'g', 'g', ' ', 'b', 'g'},
			{'b', 'g', 'g', 'b', ' '},
			{'b', 'g', 'b', 'g', ' '},
					};

char smallGame [ ][maxH] = {
		{'b', 'b', 'g', 'b', ' '},
		{' ', 'g', 'g', 'g', 'g'},
		{'g', ' ', 'b', 'g', 'b'},
		{'b', 'b', ' ', 'g', 'g'},
		{'b', 'b', 'g', ' ', 'b'},
				};

char game1[ ][maxH] = {
		{'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'g'},
		{' ', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'b', 'g'},
		{'g', ' ', 'b', 'b', 'b', 'b', 'b', 'b', 'g', 'b', 'g'},
		{'g', 'b', ' ', 'g', 'g', 'g', 'g', 'b', 'g', 'b', 'g'},
		{'g', 'b', 'g', ' ', 'b', 'b', 'g', 'b', 'g', 'b', 'g'},
		{'g', 'b', 'g', 'b', ' ', 'b', 'g', 'b', 'g', 'b', 'g'},
		{'g', 'b', 'g', 'b', 'g', 'b', 'b', ' ', 'g', 'b', 'g'},
		{'g', 'b', 'g', 'b', 'g', 'g', 'g', 'g', ' ', 'b', 'g'},
		{'g', 'b', 'g', 'b', 'b', 'b', 'b', 'b', 'b', ' ', 'g'},
		{'g', 'b', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', ' '},
		{'g', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'},
				};

int main(){
//	int SizeV = 11, SizeH = 11;
	int SmallV = 5, SmallH = 5;

	char winner;

	winner = eval(game2, SmallV, SmallH);
	printf("\nThe winner of the game is %c\n", winner);
	winner = eval(game1, SmallV, SmallH);
	printf("\nThe winner of the game is %c\n", winner);
	winner = eval(game2, SmallV, SmallH);
	printf("\nThe winner of the game is %c\n", winner);

	return 0;
}

