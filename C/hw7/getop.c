/*
 * getop.c
 *
 *  Created on: Apr 2, 2015
 *      Author: Michael
 */

#include <stdio.h>
#include <ctype.h> /* for atof() */
#include "calcf.h"

/* getop: get next character or numeric operand */
int getop(char s[],FILE *fpi) {

	int i, c;

	while ((s[0] = c = getch(fpi)) == ' ' || c == '\t');

	s[1] = '\0';

	if (!isdigit(c) && c != '.')

			return c; /* not a number */

	i = 0;

	if (isdigit(c)) /* collect integer part */

		while (isdigit(s[++i] = c = getch(fpi)));

	if (c == '.') /* collect fraction part */

		while (isdigit(s[++i] = c = getch(fpi)));

	s[i] = '\0';

	if (c != EOF)

		ungetch(c);
	return NUMBER;
}
