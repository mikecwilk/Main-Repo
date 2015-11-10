/*
 * hw8.c
 *
 *  Created on: Apr 18, 2015
 *      Author: Michael
 */

#include <stdio.h>
#include "hw8.h"



char eval(char game[][maxH], int SizeV, int SizeH){

	int searched[SizeV][SizeH];
	int searchedg[SizeV][SizeH];

	int i, j;

//Initialize Searched Array

	for (i = 0; i < SizeV; i++){
		for(j = 0; j < SizeH; j++){

			searched[i][j] = 0;
			searchedg[i][j]= 0;

			}

		}

    j = 0;
	for(i = 0; i <= SizeV; i++){
		if (game[i][j] == 'b'){
			searched[i][j] = 1;
			checkSix(game, SizeV, SizeH, i, j, searched);
			}
		}

    i = 0;
	for(j = 0; j <= SizeH; j++){
		if (game[i][j] == 'g'){
			searchedg[i][j] = 2;
			checkSixG(game, SizeV, SizeH, i, j, searchedg);
		}
	}

//Check for a complete path for b
    j = (SizeH - 1);
	for(i = 0; i <= SizeV; i++){
		if (searched[i][j] == 1){
			return BC;
		}
	}

//Check for a complete path for g
    i = (SizeV - 1);
	for(j = 0; j <= SizeH; j++){
		if (searchedg[i][j] == 2){
			return GC;
		}
	}

return 0;

}

 checkSixG(char game[][maxH], int SizeV, int SizeH,int i, int j, int searchedg[][SizeH]){

	int n,m;

	n = i;
	m = j;

n = i - 1, m = j -1 ;
if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){

}
else {

		if(game[n][m] == 'g' && (searchedg[n][m] != 2)){

			searchedg[n][m] = 2;
			checkSixG(game, SizeV, SizeH, n, m, searchedg);

		}
		else {
//			printf("already checked\n");
		}
	}


//printf("top middle = ");
n = i - 1, m = j;
if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//	printf("off board\n");

	}
else {
//	printf("on board\n");
	if(game[n][m] == 'g' && (searchedg[n][m] != 2)){
//		printf("matched\n");
		searchedg[n][m] = 2;
		checkSixG(game, SizeV, SizeH, n, m, searchedg);
	}
	else {
//		printf("already checked\n");
	}
	}

//printf("top right = ");
n = i - 1, m = j + 1 ;
	if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//		printf("off board\n");

	}
	else {
//		printf("on board\n");
		if(game[n][m] == 'g' && (searchedg[n][m] != 2)){
//			printf("matched\n");
			searchedg[n][m] = 2;
			checkSixG(game, SizeV, SizeH, n, m, searchedg);
		}
		else {
//			printf("already checked\n");
		}
		}

//printf("right = ");
n = i, m = j + 1 ;
	if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//		printf("off board\n");

	}
	else {
//		printf("on board\n");
		if(game[n][m] == 'g' && (searchedg[n][m] != 2)){
//			printf("matched\n");
			searchedg[n][m] = 2;
			checkSixG(game, SizeV, SizeH, n, m, searchedg);
		}
		else {
//			printf("already checked\n");
		}
		}

//printf("bottom middle = ");

n = i + 1, m = j;
	if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//		printf("off board\n");

	}
	else {
//		printf("on board\n");
		if(game[n][m] == 'g' && (searchedg[n][m] != 2)){
//			printf("matched\n");
			searchedg[n][m] = 2;
			checkSixG(game, SizeV, SizeH, n, m, searchedg);
		}
		else {
//			printf("already checked\n");
		}
		}

//printf("bottom left = ");
n = i + 1, m = j - 1;
	if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//		printf("off board\n");

	}
	else {
//		printf("on board\n");
		if(game[n][m] == 'g' && (searchedg[n][m] != 2)){
//			printf("matched\n");
			searchedg[n][m] = 2;
			checkSixG(game, SizeV, SizeH, n, m, searchedg);
		}
		else {
//			printf("already checked\n");
		}
	}

//printf("left = ");
n = i, m = j - 1;
	if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//		printf("off board\n");

	}
	else {
//		printf("on board\n");
		if(game[n][m] == 'g' && (searchedg[n][m] != 2)){
//			printf("matched\n");
			searchedg[n][m] = 2;
			checkSixG(game, SizeV, SizeH, n, m, searchedg);
		}
		else {
//			printf("already checked\n");
		}
	}
}

void checkSix(char game[][maxH], int SizeV, int SizeH,int i, int j, int searched[][SizeH]){

//	printf("\nChecking Surround Locations\n");
//	printf("%d %d\n", i, j);

	int n,m;

	n = i;
	m = j;
//	Check Top Right ((i-1), (j-1))




//printf("top left = ");
n = i - 1, m = j -1 ;
if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//	printf("off board\n");
}
else {
//		printf("on board\n");
		if(game[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
			checkSix(game, SizeV, SizeH, n, m, searched);

		}
		else {
//			printf("already checked\n");
		}
	}


//printf("top middle = ");
n = i - 1, m = j;
if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//	printf("off board\n");
	}
else {
//	printf("on board\n");
	if(game[n][m] == 'b' && (searched[n][m] != 1)){
//		printf("matched\n");
		searched[n][m] = 1;
		checkSix(game, SizeV, SizeH, n, m, searched);
	}
	else {
//		printf("already checked\n");
	}
	}

//printf("top right = ");
n = i - 1, m = j + 1 ;
	if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//		printf("off board\n");
	}
	else {
//		printf("on board\n");
		if(game[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
			searched[n][m] = 1;
			checkSix(game, SizeV, SizeH, n, m, searched);
		}
		else {
//			printf("already checked\n");
		}
		}

//printf("right = ");
n = i, m = j + 1 ;
	if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//		printf("off board\n");
	}
	else {
//		printf("on board\n");
		if(game[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
			searched[n][m] = 1;
			checkSix(game, SizeV, SizeH, n, m, searched);
		}
		else {
//			printf("already checked\n");
		}
		}

//printf("bottom right = ");
//n = i + 1, m = j + 1 ;
//	if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//		printf("off board\n");
//	}
//	else {
//		printf("on board\n");
//		if(game[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
//			searched[n][m] = 1;
//			checkSix(game, SizeV, SizeH, n, m, searched);
//		}
//		else {
//			printf("already checked\n");
//		}
//		}

//printf("bottom middle = ");

n = i + 1, m = j;
	if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//		printf("off board\n");

	}
	else {
//		printf("on board\n");
		if(game[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
			searched[n][m] = 1;
			checkSix(game, SizeV, SizeH, n, m, searched);
		}
		else {
//			printf("already checked\n");
		}
		}

//printf("bottom left = ");
n = i + 1, m = j - 1;
	if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//		printf("off board\n");
	}
	else {
//		printf("on board\n");
		if(game[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
			searched[n][m] = 1;
			checkSix(game, SizeV, SizeH, n, m, searched);
		}
		else {
//			printf("already checked\n");
		}
	}

//printf("left = ");
n = i, m = j - 1;
	if (m < 0 || n < 0 || (m > (SizeH - 1)) || (n > (SizeV - 1))){
//		printf("off board\n");
	}
	else {
//		printf("on board\n");
		if(game[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
			searched[n][m] = 1;
			checkSix(game, SizeV, SizeH, n, m, searched);
		}
		else {
//			printf("already checked\n");
			}
		}

	}


