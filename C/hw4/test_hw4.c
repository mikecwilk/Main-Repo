/*
By Michael Wilk
2-25-15
CS 49C Section 2
Homework 4

*/
				
#include <stdio.h>
#include <stdlib.h>
#define NROW 100
#define NCOL 20

int PrintArray();
int TopStudent();
int NumHighest();
int ToughestHomework();
	
int hws[NROW][NCOL];
int totals[NROW];
double averages[NCOL];

int main(int argc, char *argv[]){
	int i, j, x;
		for (i = 0; i< NROW; i++){
			for (j = 0; j < NCOL; j++){

				x = rand() % 101;
				hws[i][j] = x;
			}
		}

	PrintArray();
//	TopStudent();
	printf("\nHighest student = %d\n", TopStudent());
	printf("\nThe toughest homework = %d\n", ToughestHomework());
	printf("\nThe highest score 100 appears %d times",NumHighest());

	printf("\n\nRan the programs :\n\nPrintArray\nTop Student\nToughest Homework\nNumHighest\n");		//print results
	return 0;
}