/*
 * hw7_test.c
 *
 *  Created on: Apr 2, 2015
 *      Author: Michael
 */

/*
 * mainf.c
 *
 *  Created on: Oct 7, 2012
 *  Updated 10-26-14 to separate main from RPNCalc and
 *  				take file input and output
 *  Author: Tom
 */
#include <stdio.h>
int RPNCalc(FILE *fpi, FILE *fpo);

/* test program for reverse Polish calculator*/
int main(int argc, char *argv[])
{
	FILE *fpi, *fpo;

	fpi = stdin;
	if (argc > 1) {
		fpi = fopen(argv[1], "r");
		if (fpi == NULL) {
			printf("%s failed to open\n", argv[1]);
			return -1;
		}
	}

	fpo = stdout;
	if (argc > 2) {
		fpo = fopen(argv[2], "w");
		if (fpo == NULL) {
			printf("%s failed to open\n", argv[2]);
			return -1;
		}
	}

	RPNCalc(fpi, fpo);

	return 0;
}

