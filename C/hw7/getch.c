/*
 * getch_ungetch.c
 *
 *  Created on: Apr 2, 2015
 *      Author: Michael
 */

#define BUFSIZE 100
#include <stdio.h>
#include <stdlib.h> /* for atof() */


char buf[BUFSIZE]; /* buffer for ungetch */
int bufp = 0;  /* next free position in buf */

int getch(FILE *fpi) /* get a (possibly pushed-back) character */
{
//	return (bufp > 0) ? buf[--bufp] : getchar();
	return (bufp > 0) ? buf[--bufp] : getc(fpi);
}

void ungetch(int c) /* push character back on input */
{
	if (bufp >= BUFSIZE)
		printf("ungetch: too many characters\n");
	else
		buf[bufp++] = c;
}
