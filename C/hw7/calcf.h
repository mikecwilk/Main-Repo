/*
 * calcf.h
 *
 *  Created on: Apr 4, 2015
 *      Author: Michael
 */

/*
 * calcf.h
 *
 *  Created on: Oct 7, 2012
 *  Updated on: Oct 12, 2014
 *      Author: Tom
 */

#define NUMBER '0'
void push(double);
double pop(void);
int getop(char s[], FILE *fp);
int getch(FILE *fp);
void ungetch(int);
