/*
By Michael Wilk
1-29-15
CS 49C Section 2
Homework 2
test program for hexBoard
*/
				
#include <stdio.h>
#include <math.h>


char * hexBoard(int m, int n);

int main(int argc, char *argv[]){
	
	if (argc < 3) {
		printf("Give two integer arguments\n");
		return -1;
	}
	int m, n;
	
	sscanf(argv[1], "%d", &m);
	sscanf(argv[2], "%d", &n);

	printf("For an entry of %d rows and %d columns hexBoard is: \n%s\n", m , n, hexBoard(m,n));		//print results
	return 0;
}