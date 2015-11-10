/*
 * hw8.h
 *
 *  Created on: Apr 18, 2015
 *      Author: Michael
 */

#define TRUE  1
#define FALSE 0
#define BC 'b'
#define GC 'g'
#define maxH 11
#define maxV 11
typedef enum color {blue, gold} player;
typedef enum direction {h, v} dir;
char eval(char game[][maxH], int SizeV, int SizeH);
void checkSixG(char game[][maxH], int SizeV, int SizeH,int i, int j, int searchedg[][SizeH]);
