/*
By Michael Wilk
2-21-15
CS 49C Section 2
Homework 3
test program for lim and catalan
*/
				
#include <stdio.h>
#include <math.h>


long long int lim(int s, int max, char t);

int main(int argc, char *argv[]){
	printf("This program will check for min and max values for different primitives (1/0 = signed/unsigned), (1/0 = ) and a character(c = char, s = short, d = int, l = long int, z = long long int)\n");
	if (argc < 4) {
		printf("\nGive two integer arguments and a character\n");
		return -1;
	}
	int s, max;
	char t;
	
	sscanf(argv[1], "%d", &s);
	sscanf(argv[2], "%d", &max);
	sscanf(argv[3], "%c", &t);
	if (s == 1){
		printf("\n1 = signed, 0 = unsigned\nsign? = %d\n\n1 = maximum, 0 = minimum\nMax? = %d\n\n'c' = char, 's' = short int, 'd' = int, 'l' = long int, 'z' = long long int\ntype = %c\n\nlim is: \n%lld\n", s , max, t, lim(s,max,t));		//print results signed
	}else{
		printf("\n1 = signed, 0 = unsigned\nsign? = %d\n\n1 = maximum, 0 = minimum\nMax? = %d\n\n'c' = char, 's' = short int, 'd' = int, 'l' = long int, 'z' = long long int\ntype = %c\n\nlim is: \n%lld\n", s , max, t, lim(s,max,t));		//print results signed
	}
	return 0;
}