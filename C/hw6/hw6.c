/*
By Michael Wilk
3-18-15
CS 49C Section 2
Homework 6
program for bit sequence
*/

#include <stdio.h>

int checkMatch(int bitWidth, int n, unsigned long long int start_x, int start){//This function checks for a match of the "start" variable with the current "n" bits
	int  i;
	int msb, lsb;//In theory start should be the MSB and the number we are comparing is the LSB of the bit sequence generated
	for (i = 0; i <n; i++){//loops through the bits of the "start" variable and "n" least significat bits of the sequence called "start_x"
		msb = (start >> (n - i - 1));//cycles through the bits one per loop iteration of the "start" variable
		lsb = (start_x >> (n - i -1));//cycles through the bits one per loop iteration of the lsb of the sequence (start_x)

		msb = msb & 1;//forces binary values of start variable
		lsb = lsb & 1;//forces binary values of the lsb of the sequence

//		printf("%d %d", msb, lsb);
		if((msb ^ lsb) == 0){//xor's the current bits in start and the sequence and continue the loop
//			printf("|");

		}else{// returns a zero for the function if there is not a full match through the bits
//			printf("|");
//			printf("X X");
//			printf("\n");
			return 0;
		}
	}
return 1;//if the loop is completed we return a 1 confirming a match of bits for variable start and the "n" least significant bits
}

int bitList(int len, int word){//This function is not used for the assignment but it helped trouble shoot by converting ints to binary numbers of length "len"
{
  int c, k;
  for (c = len; c >= 0; c--){//loop for the desired length of the binary equivalent to an int
    k = word >> c;//We need to start with the MSB of our word

    if ((k & 1) == 1)//bitwise & forces binary
     printf("1");
    else
     printf("0");
  }
  printf("\n");

  return 0;
}
}
int bitAndXor1(int n, unsigned long long int start, int pattern){//This function provides logical & and XOR to the bits currently in the sequence window

	int c,s,p,prev,xor;
	prev = 0;

	for (c = n; c > 0; c--){//loop through the window width of "n"

		s = start >> (c - 1);//this is the MSB of variable start and cycles one bit to the right each iteration of the loop
		p = pattern >> c;//conveniently the patteran was one bit longer than the start variable so this is the equivalent bit in the pattern

		s = s & 1; //forces a binary output of start bits
		p = p & 1; //forces a binary output of pattern bits

	    if (c <= n - 1){//This is from one bit right of the MSB until the LSB
	    xor = prev ^ (s & p);//Bitwise XOR of the current bitwise & of start and pattern bits with the previous bitwise & result(at third iteration it is previous previous XOR)
	    prev = xor;

	    }
	    else{//This is only for the MSB of both pattern and start. Bitwise &ing occurs but only one bit at this point so no XOR
	    prev = s & p;
	    }
	}
	return xor;//Returns the value of XOR
}



int bits(int n, unsigned int start, unsigned int pattern, char *fn){

	int xor = 0;
	int bitWidth;
	long long int start_x;

	FILE *fptr;//a new one for me that initializes a file pointer
	fptr = fopen(fn,"wt");//the pointer opens a file with parameters fn(filename) and wt(write text)
	start_x = start;
	bitWidth = n;

	xor = bitAndXor1(n,start_x,pattern); //first iteration we need to add to the sequence but not compare with start variable because it is the start variable
	fprintf(fptr, "%d ", xor);//writes the result of the bitwise xor in the file pointer

	if (xor == 0){
		start_x = start_x << 1;//append a zero to the right hand side of the bit sequence (new lsb)
	}else{
		start_x = (start_x << 1) + 1;//append a 1 to the right hand side of the bit sequence (new lsb)

	}
	bitWidth = bitWidth + 1;//count the width of bit sequence

	while (checkMatch(bitWidth, n, start_x, start) == 0){//If the bit sequence does not match the start bits continue the process
	xor = bitAndXor1(n,start_x,pattern);//bitwise & with the bitwise XOR like before
	fprintf (fptr, "%d ", xor);//print each result of the bitwise XOR to the output file

	if (xor == 0){
		start_x = start_x << 1;//append a zero to the right hand side of the bit sequence (new lsb)
	}else{
		start_x = (start_x << 1) + 1;//append a 1 to the right hand side of the bit sequence (new lsb)
	}

	bitWidth = bitWidth + 1;//with each iteration we increment the width of the bit sequence
	}


	fclose(fptr);//closes the write file pointed to by fptr

return (bitWidth - n);//returns the period of the sequence (length of the bit sequence)


}
