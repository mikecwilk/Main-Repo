/*
By Michael Wilk
2-4-15 version 1.0
2-6-15 version 1.1
2-11-15 version 1.2
CS 49C Section 2
Homework 2
program for hexBoard
*/
#include <stdio.h>

char buf[2048];
char * hexBoard(int m, int n){

//	
    char *bufp = buf;
	int i,f,s,g,h;

	
	g = 0;
	h = 0;
	
//Initial Blank Line	
	bufp += sprintf(bufp, "\n");
	
//For Loop Iterating "m" number of Rows
	for ( f = 0; f < m; f++ ) {
		if (g == 0) { // Variable Signals First Row In this Case
			for ( i = 0; i < n; i++ ) {	//For Number of Columns "n" Create a Top Piece					
				bufp += sprintf(bufp, " / \\");//Creates A Single Top Piece
				}				
		}	
		bufp += sprintf(bufp, "\n");//The String Now starts the second line on the string
		h = g; //This accounts for spacing required

		for (s = 0; s < h; s++){ //This For Loop iterates depending on which row its on thus creating the beginning spaces				
			bufp += sprintf(bufp, "  " ); //Inserts a space "h" times	
		}
			for ( i = 0; i < n; i++ ) { // This For Loop iterates through "n" columns creating the mid piece
				if (i == n-1) {	//A check for the last column		
				bufp += sprintf(bufp, "|   |" );//This is a normal mid piece
				}
				
				else{

				bufp += sprintf(bufp, "|   " );//This is a mid piece specifically for the mid section
				}
			h = 0;// resets our variable for the spacing which is reused later
			}
		
		bufp += sprintf(bufp, "\n"); //again we need a new line so we can make our bottom pieces
		h = g;
		
		for (s = 0; s < h; s++){//A for loop for the spacing of the bottom pieces				
			bufp += sprintf(bufp, "  " );//spacing 	
		}
			for ( i = 0; i < n; i++ ) {//A for loop that iterates the "n" number of columns
				if ((i == n-1) && (f != (m - 1))){ //makes sure we arent in the last column of the last row			
				bufp += sprintf(bufp, " \\ / \\" );// Normal bottom piece
				}
				
				else{

				bufp += sprintf(bufp, " \\ /" ); //A final bottom piece for the final row and column
				}
			h = 0;	
			}
		g = g + 1;// This represents a shift to the next row this variable keeps track of spacing
		h = g;
	}
	bufp += sprintf(bufp, "\n");//A final new line as requested by the assignment
	return buf;
 }