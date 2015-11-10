/*
 * test_hw6.c
 *
 *  Created on: Mar 16, 2015
 *      Author: Michael
 */

#include <stdio.h>
#include "hw6.h" //this just declares the bits() function

int main(){


	printf("\n");
	printf("n = 4, start = 0x01, pattern = 0x19");
	printf("\n");
	printf("%d\n", bits(4, 0x01, 0x19, "p1.txt"));
	printf("\n");

	printf("n = 6, start = 0x01, pattern = 0x4f");
	printf("\n");
	printf("%d\n", bits(6, 0x01, 0x4f, "output6.txt"));
	printf("\n");

	printf("n = 6, start = 0x01, pattern = 0x43");
	printf("\n");
	printf("%d\n", bits(6, 0x01, 0x43, "big6.txt"));
	printf("\n");

	printf("n = 10, start = 0x249, pattern = 0x481");
	printf("\n");
	printf("%d\n", bits(10, 0x249, 0x481, "output10.txt"));
	printf("\n");

	printf("n = 3, start = 0x5, pattern = 0xd");
	printf("\n");
	printf("%d\n", bits(3, 0x5, 0xd, "temp.txt"));
	printf("\n");

return 0;

}
