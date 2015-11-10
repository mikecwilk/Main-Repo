/*
 * printboard.c
 *
 *  Created on: Apr 18, 2015
 *      Author: Michael
 */

#include <stdio.h>
#include "hw8.h"

printBoard(char game[][maxH], int SizeV, int SizeH){
//PrintBoard
	int i,j;
	for (i = 0; i < SizeV; i++){
		for (j = 0; j <= SizeH; j++){

			if (game[i][j] == 'g' && j != (SizeH)){
				printf(" ( g ) ");
			}

			else if (game[i][j] == 'b' && j != (SizeH)){
				printf(" ( b ) ");

			}
			else if (j == (SizeH)){
			printf("\n");
			}
			else{
			printf(" (%d %d) ", i , j);
			}
		}
	}
}
