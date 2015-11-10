/*
By Michael Wilk
1-29-15
CS 49C Section 2
Homework 1
program for GCD
*/

 int GCD(int m, int n){
	int h;
	int r = 20;
	
//Convert all numbers to positive
	m = abs(m);
	n = abs(n);

//Check if "m" is the larger of the two integers and perform Euclid's Algorithm
	if ((m > n) && (n != 0)) {
	do
	{
	
	h = n;
	n = m % n;
	m = h;
	}while(n != 0);
	return m;	
	}

//Check if "n" is the larger of the two integers and perform Euclid's Algorithm	
	else if((n > m) && (m != 0)) {
	do
	{
	
	r = m;
	m = n % m;
	n = r;
	}while(m != 0);
	return n;	
	}
	
//Take care of the cases with 0 	
	else if (m == 0) return n;
	else if (n == 0) return m;
	
	


 }