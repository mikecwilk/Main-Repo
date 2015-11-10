/*
By Michael Wilk
2-21-15 version 1.0
CS 49C Section 2
Homework 3
program for lim and catalan
Lim checks min and max values for integer types
*/
#include <stdio.h>
#include <limits.h>

long long int lim(int s, int max, char t){

//'c' = char, 's' = short int, 'd' = int, 'l' = long int, 'z' = long long int
long long int m;
 switch (t) {
      case 'c': //char

		 if (s == 0){ //Unsigned
			 if (max == 0){//set the minimum value	(Char Unsigned)
				 m = 0;				 
			 }
			 else if (max != 0){//set the maximum value	(Char Unsigned)
				 m = UCHAR_MAX;
			 }
		 }
		 if (s != 0){ //signed
			 if (max == 0){//set the minimum value	(Char signed)
				 m = CHAR_MIN;				 
			 }
			 else if (max != 0){//set the maximum value	(Char signed)
				 m = SCHAR_MAX;
			 }
		 }
         break;

      case 's':
	  
         if (s == 0){
			 if (max == 0){//set the minimum value	(Short Int Unsigned)
				 m = 0;				 
			 }
			 else if (max != 0){//set the maximum value	(Short Int Unsigned)
				 m = USHRT_MAX;
			 }
		 }
		 if (s != 0){
			 if (max == 0){//set the minimum value	(Short Int signed)
				 m = SHRT_MIN;				 
			 }
			 else if (max != 0){//set the maximum value	(Short Int signed)
				 m = SHRT_MAX;
			 }
		 }
         break;

      case 'd':
         if (s == 0){//unsigned
			 if (max == 0){
				 m = 0;	//set the minimum value	(Int Unsigned)		 
			 }
			 else if (max != 0){ 
				 m =  UINT_MAX;//set the maximum value (Int Unsigned)	
			 }
		 }
		 if (s != 0){//signed
			 if (max == 0){
				 m = INT_MIN;//set the minimum value (Int Signed)					 
			 }
			 else if (max != 0){
				 m = INT_MAX;//set the maximum value (Int Signed)	
			 }
		 }
         break;

      case 'l':
         if (s == 0){//unsigned
			 if (max == 0){
				 m = 0;	//set the minimum value (LONG Unsigned)		 
			 }
			 else if (max != 0){ 
				 m =  ULONG_MAX;//set the maximum value (LONG Unsigned)
			 }
		 }
		 if (s != 0){//signed
			 if (max == 0){
				 m = LONG_MIN;//set the minimum value (LONG Signed)				 
			 }
			 else if (max != 0){
				 m = LONG_MAX;//set the maximum value (LONG Signed)
			 }
		 }
         break;

      case 'z':
         if (s == 0){//unsigned
			 if (max == 0){
				 m = 0;	//set the minimum value	(LONG LONG Unsigned)		 
			 }
			 else if (max != 0){ 
				 m =  ULONG_MAX;//set the maximum value (LONG LONG Unsigned)
			 }
		 }
		 if (s != 0){//signed
			 if (max == 0){
				 m = LLONG_MIN;//set the minimum value (LONG LONG Signed)				 
			 }
			 else if (max != 0){
				 m = LLONG_MAX;//set the maximum value (LONG LONG Signed)
			 }
		 }
         break;


      default:
         printf("not a type of integer");
         break;
   }

	return m;
 }
 /*
By Michael Wilk
2-21-15 version 1.0
2-22-15 version 1.1 added array support
CS 49C Section 2
Homework 3
program for catalan
Catalan runs the catalan triangle equation for two inputs
*/
#include <stdio.h>
#include <limits.h>

long long int Catalan(int n, int k){

//Integers needed for program
int q = 0;
long long int z = 1;
int x[100];
int c[100];
int i, j, h, g, m, d, w;

if(n < 0 || k <0){//checks if n is 0 or k is 0 and returns -1 if this is the case
	return -1;
}

else if (n < k) {//checks if n is less than k and returns 0 if this is the case
	return 0;
}

else{

//array for n+k factorial divided by n + 1 factorial
for (i = k+n; i >= n+2; i--){
	x[q] = i;
	q = q + 1;
	z = 1;
		}
		
//one extra numerator		
x[q] = n - k + 1;


q = 0;


//array for k factorial
for (j = k; j > 0; j--){
	c[q] = j;

	q = q + 1;
	}	


q = 0;
g = 0;
for(h = k; h > 0; h--){//loop through the denominator

	for(i = k+n; i >= n+1; i--){//loop through the numerator until denominator index = 1

		
		//find the GCD of x[g] and c[q]
		m = x[g];
		d = c[q];
		while (m != 0) {
			w = m;
			m = d % m;
			d = w;
		} 		

		if (d == 1){
			
		}
		//divide x[g] and c[q] by the GCD 
		x[g] = x[g]/d;
		c[q] = c[q]/d;

		
		g = g + 1;
		
	}

	g = 0;
	q = q+1;
}	
g = 0;
for(i = k + n; i > n ; i--){//multiplies out the remaining numerator

	z = z * x[g];
	g = g + 1;

	}
  }
return z;
}