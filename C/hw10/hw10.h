/*
CS49C Spring 2015 Header file for HW10
T. Howell
4-30-2015
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <time.h>

#define MAXH 11
#define TRUE  1
#define FALSE 0
#define BC 'b'
#define GC 'g'

typedef enum color {blue, gold} player;
typedef enum direction {h, v} dir;

typedef struct hexPosition {
	char grid[MAXH][MAXH];  //maximum board size is 11 x 11
	int SizeV;		//board size - vertical
	int SizeH;		//board size - horizontal
	player toPlay;
	int playsLeft;
} hexPos;

void mymove(hexPos *hp, FILE *fpi);
void randomMove(hexPos *hp);
void printBoard(hexPos *hp);
char eval(hexPos *hp);
