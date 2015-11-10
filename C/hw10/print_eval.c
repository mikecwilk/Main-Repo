

#include <stdio.h>
#include "extra.h"
#include "hw10.h"
void checkSixG(hexPos *hp,int i, int j, int searchedg[][hp->SizeH]);
void checkSix(hexPos *hp,int i, int j, int searched[][hp->SizeH]);

char eval(hexPos *hp){
printf("eval\n");

if(hp->playsLeft == 10){
	return BC;
}
return 0;
}
/*
	int searched[hp->SizeV][hp->SizeH];
	int searchedg[hp->SizeV][hp->SizeH];

	int i, j;

//Initialize Searched Array

	for (i = 0; i < hp->SizeV; i++){
		for(j = 0; j < hp->SizeH; j++){

			searched[i][j] = 0;
			searchedg[i][j]= 0;

			}

		}

    j = 0;
	for(i = 0; i <= hp->SizeV; i++){
		if (hp->grid[i][j] == 'b'){
			searched[i][j] = 1;
			checkSix(hp, i, j, searched);
			}
		}

    i = 0;
	for(j = 0; j <= hp->SizeH; j++){
		if (hp->grid[i][j] == 'g'){
			searchedg[i][j] = 2;
			checkSixG(hp, i, j, searchedg);
		}
	}

	for (i = 0; i < hp->SizeV; i++){
		printf("\n");
		for(j = 0; j < hp->SizeH; j++){

			printf("%d", searched[i][j]);
			//searchedg[i][j]= 0;

			}

		}printf("\n");

//Check for a complete path for b
    j = (hp->SizeH - 1);
	for(i = 0; i <= hp->SizeV; i++){
		if (searched[i][j] == 1){
			return BC;
			//return 0;
		}
	}

//Check for a complete path for g
    i = (hp->SizeV - 1);
	for(j = 0; j <= hp->SizeH; j++){
		if (searchedg[i][j] == 2){
			return GC;
			//return 0;
		}
	}
printf("no winner\n");
return 0;

}

void checkSixG(hexPos *hp,int i, int j, int searchedg[][hp->SizeH]){

	int n,m;

	n = i;
	m = j;

n = i - 1, m = j -1 ;
if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){

}
else {

		if(hp->grid[n][m] == 'g' && (searchedg[n][m] != 2)){

			searchedg[n][m] = 2;
			checkSixG(hp, n, m, searchedg);

		}
		else {
//			printf("already checked\n");
		}
	}


//printf("top middle = ");
n = i - 1, m = j;
if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//	printf("off board\n");

	}
else {
//	printf("on board\n");
	if(hp->grid[n][m] == 'g' && (searchedg[n][m] != 2)){
//		printf("matched\n");
		searchedg[n][m] = 2;
		checkSixG(hp, n, m, searchedg);
	}
	else {
//		printf("already checked\n");
	}
	}

//printf("top right = ");
n = i - 1, m = j + 1 ;
	if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//		printf("off board\n");

	}
	else {
//		printf("on board\n");
		if(hp->grid[n][m] == 'g' && (searchedg[n][m] != 2)){
//			printf("matched\n");
			searchedg[n][m] = 2;
			checkSixG(hp, n, m, searchedg);
		}
		else {
//			printf("already checked\n");
		}
		}

//printf("right = ");
n = i, m = j + 1 ;
	if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//		printf("off board\n");

	}
	else {
//		printf("on board\n");
		if(hp->grid[n][m] == 'g' && (searchedg[n][m] != 2)){
//			printf("matched\n");
			searchedg[n][m] = 2;
			checkSixG(hp, n, m, searchedg);
		}
		else {
//			printf("already checked\n");
		}
		}

//printf("bottom middle = ");

n = i + 1, m = j;
	if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//		printf("off board\n");

	}
	else {
//		printf("on board\n");
		if(hp->grid[n][m] == 'g' && (searchedg[n][m] != 2)){
//			printf("matched\n");
			searchedg[n][m] = 2;
			checkSixG(hp, n, m, searchedg);
		}
		else {
//			printf("already checked\n");
		}
		}

//printf("bottom left = ");
n = i + 1, m = j - 1;
	if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//		printf("off board\n");

	}
	else {
//		printf("on board\n");
		if(hp->grid[n][m] == 'g' && (searchedg[n][m] != 2)){
//			printf("matched\n");
			searchedg[n][m] = 2;
			checkSixG(hp, n, m, searchedg);
		}
		else {
//			printf("already checked\n");
		}
	}

//printf("left = ");
n = i, m = j - 1;
	if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//		printf("off board\n");

	}
	else {
//		printf("on board\n");
		if(hp->grid[n][m] == 'g' && (searchedg[n][m] != 2)){
//			printf("matched\n");
			searchedg[n][m] = 2;
			checkSixG(hp, n, m, searchedg);
		}
		else {
//			printf("already checked\n");
		}
	}
}

void checkSix(hexPos *hp ,int i, int j, int searched[][hp->SizeH]){

//	printf("\nChecking Surround Locations\n");


	int n,m;

	n = i;
	m = j;





//printf("top left = ");
n = i - 1, m = j -1 ;
if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//	printf("off board\n");
}
else {
//		printf("on board\n");
		if(hp->grid[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
			checkSix(hp, n, m, searched);

		}
		else {
//			printf("already checked\n");
		}
	}


//printf("top middle = ");
n = i - 1, m = j;
if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//	printf("off board\n");
	}
else {
//	printf("on board\n");
	if(hp->grid[n][m] == 'b' && (searched[n][m] != 1)){
//		printf("matched\n");
		searched[n][m] = 1;
		checkSix(hp, n, m, searched);
	}
	else {
//		printf("already checked\n");
	}
	}

//printf("top right = ");
n = i - 1, m = j + 1 ;
	if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//		printf("off board\n");
	}
	else {
//		printf("on board\n");
		if(hp->grid[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
			searched[n][m] = 1;
			checkSix(hp, n, m, searched);
		}
		else {
//			printf("already checked\n");
		}
		}

//printf("right = ");
n = i, m = j + 1 ;
	if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//		printf("off board\n");
	}
	else {
//		printf("on board\n");
		if(hp->grid[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
			searched[n][m] = 1;
			checkSix(hp, n, m, searched);
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
	if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//		printf("off board\n");

	}
	else {
//		printf("on board\n");
		if(hp->grid[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
			searched[n][m] = 1;
			checkSix(hp, n, m, searched);
		}
		else {
//			printf("already checked\n");
		}
		}

//printf("bottom left = ");
n = i + 1, m = j - 1;
	if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//		printf("off board\n");
	}
	else {
//		printf("on board\n");
		if(hp->grid[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
			searched[n][m] = 1;
			checkSix(hp, n, m, searched);
		}
		else {
//			printf("already checked\n");
		}
	}

//printf("left = ");
n = i, m = j - 1;
	if (m < 0 || n < 0 || (m > (hp->SizeH - 1)) || (n > (hp->SizeV - 1))){
//		printf("off board\n");
	}
	else {
//		printf("on board\n");
		if(hp->grid[n][m] == 'b' && (searched[n][m] != 1)){
//			printf("matched\n");
			searched[n][m] = 1;
			checkSix(hp, n, m, searched);
		}
		else {
//			printf("already checked\n");
			}
		}

	}
*/
void printBoard(hexPos *hp){

char buf[2048];
//char * hexBoard(int m, int n){

//
    char *bufp = buf;
	int i,f,s,g,h;

	printf("SizeV %d\n", hp-> SizeV);
	printf("SizeH %d\n", hp-> SizeH);
	g = 0;
	h = 0;

//Initial Blank Line
	bufp += sprintf(bufp, "\n");

//For Loop Iterating "m" number of Rows
	for ( f = 0; f < (hp->SizeV); f++ ) {
		if (g == 0) { // Variable Signals First Row In this Case
			for ( i = 0; i < (hp->SizeH); i++ ) {	//For Number of Columns "n" Create a Top Piece
//				bufp += sprintf(bufp, " / \\");//Creates A Single Top Piece
				printf(" / \\");//Creates A Single Top Piece
				}
		}
		printf("\n");//The String Now starts the second line on the string
		h = g; //This accounts for spacing required

		for (s = 0; s < h; s++){ //This For Loop iterates depending on which row its on thus creating the beginning spaces
			printf("  " ); //Inserts a space "h" times
		}
			for ( i = 0; i < (hp->SizeH); i++ ) { // This For Loop iterates through "n" columns creating the mid piece
				if (i == (hp->SizeH)-1) {
					if (hp->grid[s][i] == 'b'){
							printf("| b |" );//This is a mid piece specifically for the mid section
						}
						else if (hp->grid[s][i] == 'g'){
							printf("| g |" );//This is a mid piece specifically for the mid section
						}
						else{
							printf("|   |" );//This is a mid piece specifically for the mid section
						}
				}

				else{// where I should modify for gs and bs!!!!!!!!!!!!
					if (hp->grid[s][i] == 'b'){
						printf("| b " );//This is a mid piece specifically for the mid section
					}
					else if (hp->grid[s][i] == 'g'){
						printf("| g " );//This is a mid piece specifically for the mid section
					}
					else{
						printf("|   " );//This is a mid piece specifically for the mid section
					}
				}
			h = 0;// resets our variable for the spacing which is reused later
			}

		printf("\n"); //again we need a new line so we can make our bottom pieces
		h = g;

		for (s = 0; s < h; s++){//A for loop for the spacing of the bottom pieces
			printf("  " );//spacing
		}
			for ( i = 0; i < (hp->SizeH); i++ ) {//A for loop that iterates the "n" number of columns
				if ((i == (hp->SizeH)-1) && (f != ((hp->SizeV) - 1))){ //makes sure we arent in the last column of the last row
				printf(" \\ / \\" );// Normal bottom piece
				}

				else{

				printf(" \\ /" ); //A final bottom piece for the final row and column
				}
			h = 0;
			}
		g = g + 1;// This represents a shift to the next row this variable keeps track of spacing
		h = g;
	}
	printf("\n");//A final new line as requested by the assignment
//	return buf;
 }

