/*
 * sortfile.c
 *
 *  Created on: Apr 23, 2015
 *      Author: Michael
 */

#include <stdio.h>
#include <stdlib.h>
#include "hw9.h"
#define NSIZE 16

// global variables
struct ListNode *first, *last;
unsigned int id;
char iname[NSIZE], igrade;

int sortfile(FILE *fpi, FILE *fpo){
	while (3 == fscanf(fpi, "%u %s %c", &id, iname, &igrade)){
			insertList(first, id, iname, igrade);
	}

	//print the sorted list
	printList(fpo, first);

	//clean up
	freeList(first);
	first->next = last; //restore initial list link
	return 0;
}

