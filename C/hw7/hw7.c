/*
By Michael Wilk
4-12-15
CS 49C Section 2
Homework 6
program for reverse polish calculator borrowed from Kernigan and Ritchie's Book "The C Programming Language"
*/

#include <stdio.h>
#include <stdlib.h> /* for atof() */
#include "calcf.h"
#define MAXOP 100 /* max size of operand or operator */


/* reverse Polish calculator  */
int RPNCalc(FILE *fpi, FILE *fpo){ //For actual class program
//main(){
	int type;
	double op2;
	char s[MAXOP];
	double pop1;
	double pop2;
	double store;
	double keep;

	while ((type = getop(s,fpi)) != EOF) {

		switch (type) {

		case NUMBER:

			push(atof(s));

			break;

		case '+':

			push(pop() + pop());
			break;

		case '*':

			push(pop() * pop());
			break;

		case '-':

			op2 = pop();
			push(pop() - op2);
			break;

		case '/':

			op2 = pop();

			if (op2 != 0.0)
				push(pop() / op2);

			else

			fprintf(fpo, "error: zero divisor\n");

			break;

		case '\n':

			keep = pop();
			push(keep);
			fprintf(fpo, "\t%.16g\n", pop());
			push(keep);

			break;

		case '=':

			keep = pop();
			push(keep);
			fprintf(fpo, "\t%.16g\n", pop());
			push(keep);
			break;

		case 'X':

			pop1 = pop();
			pop2 = pop();
			push(pop1);
			push(pop2);


			break;

		case 'S':

			store = pop();

			break;

		case 'R':

			push(store);

			break;

		case '\r':


			break;




		default:

			fprintf(fpo, "error: unknown command %s\n", s);
			break;

		}

	}



return 0;
}


