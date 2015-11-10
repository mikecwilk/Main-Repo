/*
By Michael Wilk
test program for BCD
*/
				
#include <stdio.h>

//int notPalindrome(char *x);
void main (){
	int a = notPalindrome("Neil, a trap! Sidffagea is part alien!");
	printf("%d", a);
}
/*int main( int argc, char *argv[] )  {
   
   char m;
   sscanf(argv[1], "%s", &m);
   if( argc == 2 )
   {
	  
      printf("The argument supplied is %s\n", argv[1]);
	  notPalindrome(m);
   }
   else if( argc > 2 )
   {
      printf("Too many arguments supplied.\n");
   }
   else
   {
      printf("One argument expected.\n");
   }
   return 0;
}
*/
