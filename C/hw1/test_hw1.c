/*
By Michael Wilk
1-29-15
CS 49C Section 2
Homework 1
test program for GCD
*/
				
#include <stdio.h>
//#include <stdlib.h> for abs!!
int GCD(int m, int n);	

int main(int argc, char *argv[]){
	
	if (argc < 3) {
		printf("Give two integer arguments\n");
		return -1;
	}
	int m, n;

	sscanf(argv[1], "%d", &m);
	sscanf(argv[2], "%d", &n);

	printf("The Greatest Common Denominator of %d and %d = %d\n", m, n, GCD(m, n));		//print results
	return 0;
}