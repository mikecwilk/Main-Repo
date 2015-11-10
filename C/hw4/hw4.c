/*
By Michael Wilk
2-25-15
CS 49C Section 2
Homework 4
program for TopStudent
program for ToughestHomework
program for NumHighest
*/
#include <stdio.h>
#include <stdlib.h>
#define NROW 100
#define NCOL 20

int hws[NROW][NCOL];
int totals[NROW];
double averages[NCOL] = {0};
int i, j;
int x, y, z;
double q;
double r;

int PrintArray(){
	printf("\n");
	printf("          col");
	for (i = 0; i < NCOL - 1; i++) {
		printf(" col");
	}
	for (i = 0; i< NROW; i++){
		printf("\nrow = %d ",i);
		for (j = 0; j < NCOL; j++){

			printf(" %d ", hws[i][j]);
		}
			
		}
	
	printf("\n\n");
	return 0;	
}

int TopStudent(){
	
	x = 0;
	y = 0;
	z = 0;
	
	for (i = 0; i < NROW; i++){ // loops through the columns
		for (j = 0; j < NCOL ; j++){ // loops through the rows and updates the total for each column
//			printf("\n%d", hws[i][j]);
			x = x + hws[i][j];
//			printf("\n%d",x);
		}


		totals[i] = x; // updates the totals array
		x = 0;
	}
//	printf("\nTotals = ");
	for (i = 0; i < NCOL; i++){ // prints the totals
//		printf(" \n[%d]", totals[i]);
		
	}
//	printf("\n\n");
	y = totals[0];
	for (i = 0; i < NROW; i++){//loops through to find the highest total
		if (totals[i] > y){
			y = totals[i];
		} else {
			y = y;
		}
	}
	for (i = 0; i <= NROW; i++){//finds the row number of the highest total
		if (totals[i] == y){
			z = i;
			break;
		}
	}
//	printf("Highest Total = %d located at row %d\n", y, z);
	return z;
}
int ToughestHomework(){
	
	x = 0; 
	y = 0;
	z = 0;
	q = 0;
	
	for (j = 0; j < NCOL; j++){// loop that caluculates the averages for each column
		for (i = 0; i < NROW; i++){
			q = q + hws[i][j];
//			printf("\n%lf",q);
		}
		q = q/NROW; // per column average
//		printf("\n\n%lf",q);
		averages[j] = q; // builds up the averages array
		q = 0;
//		printf("\n");
		
	}
	for (i = 0; i < NCOL; i++){//loop that prints the averages
//		printf(" [%lf]", averages[i]);
	}
//	printf("\n\n");
	r = averages[0];
	for (i = 0; i < NCOL; i++){//loops for each average in array averages of length NCOL
		if (averages[i] < r){ //checks if the value is less than that of the 
			r = averages[i]; // set r = to that average if it is smaller than the previous
		} else {
			r = r;
		}
	}
	for (i = 0; i < NCOL; i++){//find the column number the lowest average is at
		if (averages[i] == r){
			z = i;
			break;
		}
	}
//	printf("Lowest average = %lf located at col %d\n\n", r, z);
	return z;
}

int NumHighest(){
	
	x = hws[0][0]; 
	y = 0;
	z = 0;	
	
	for (j = 0; j < NCOL; j++){ // loops through the columns
		for (i = 0; i < NROW; i++){ // loops through the rows and updates the total for each column
			if (hws[i][j] > x){
					x = hws[i][j];
			} else {
				x = x;
			}
			
		}
	
	}
	z = 0;
	for (j = 0; j < NCOL ; j++){ // loops through the columns
		for (i = 0; i < NROW; i++){ // loops through the rows and updates the total for each column
			if (hws[i][j] == x){
					z = z + 1;
//					printf("[%d][%d]",i,j);
			} else {
				z = z;
			}
			
		}
	
	}
//	printf("the highest number is %d\n", x);
//	printf("It appeared %d times", z);
	return z;
}
