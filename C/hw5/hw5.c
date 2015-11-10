/*
By Michael Wilk
3-11-15
CS 49C Section 2
Homework 5
program for notPalindrome
1 - takes a string of characters and removes the whitespace and punctuation marks in an new string
2 - concurrently replaces lower case alphabetic characters with their respective uppercase in a new string
3 - scans through this new string and compares the first and last char (then the 2nd and 2nd to last etc)
4 - if all the chars in the string match it returns 0
4 - if a mismatch occurs it returns the location in the original string where the mismatch occurred (from the Left Side of the string)
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int notPalindrome(const char *x){

	int length,i,j,y,mismatch,displaced,unmatched; //declare ints
	char *removedPtr; //declare pointer char

	removedPtr = (char *)malloc(sizeof(char)*1000000000);//allocates a lot of memory for the pointer "removedPtd"
	length = 0;
	unmatched = 0;
	mismatch = 0;
	displaced =0; //initial values for successive calls

	length = strlen(x);
	j = 0;
	i = 0;
	y = 0; //initial values for successive calls


	for (i = 0; i < length; ){//this loop checks the initial string for alphabetic characters and puts upper case equivalents in a new string

		if (isalpha(x[i])){ //check if char is alphabetic
		removedPtr[j] = toupper(x[i]); //makes the new string with an uppercase equivalent
		i++;
		j++;
		}else{//skips locations where punctuation or whitespace occurs

			i++;

			continue;
		}

	}


	y = strlen(removedPtr);//length of removedPtr variable assignment
//

	for(j = 0; j < y/2;){//This loop checks through the new string for mismatches

		if(removedPtr[j] == removedPtr[y - j - 1]){//checks the first and last char to see if they match 
			j++;


			continue;//if they match continue 
		}else{
			unmatched = 1;//if they dont match set a flag and break the loop.
			break;
		}
	}

for(mismatch = 0; mismatch<=j;){//this loop checks where the mismatch occurred while skipping over punctuation and whitespaces in original string

	if(isalpha(x[i])){//check if the string is an alphabetic char or not to properly locate the mismatched character on the leftside
		i--;
		j--; //alphabetic chars should evenly increment the loop like normal
		displaced = displaced + 1;
	}else{
		displaced = displaced + 1;
		i--;
		continue;//Here we have a whitespace or punctuation mark so we loop again without incrementing.
	}

}

if (unmatched == 1){//if there is an unmatched variable we return the location of the mismatch in the original string
	return length - displaced +1;
}else{
	return 0;//if we have a palindrone we return 0
}


}