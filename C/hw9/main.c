/*
 * main.c
 *
 *  Created on: Apr 23, 2015
 *      Author: Michael
 */

/*
 * main for hw9.c
 *
 *  Created on: Nov 4, 2012
 *  Updated on: Nov 20, 2014
 *      Author: Tom
 */
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include "hw9.h"
#define NSIZE 16



int main(int argc, char *argv[]){

		FILE *fpi, *fpo; //pointers to the files input.txt and output.txt
		fpi = stdin;
		fpo = stdout;
		struct ListNode *first, *last; //pointers to the first and last names in the linked list
		int id;
		char iname[NSIZE], igrade;



		if (argc > 1) {
			fpi = fopen(argv[1], "r");
			if (fpi == NULL) {printf("%s failed to open\n", argv[1]); return -1;}
		}
		if (argc > 2) {
				fpo = fopen(argv[2], "w");
				if (fpo == NULL) {printf("%s failed to open\n", argv[2]); return -1;}
		}

//set up initial list
//I left some work for students to do here.
//allocate and set up the "anchor" nodes
//		typedef struct ListNode Lnode;


		first = (struct ListNode*) malloc(sizeof(struct ListNode));
		last  = (struct ListNode*) malloc(sizeof(struct ListNode));



		first->data = 0;
		first->name;
		first->grade = 'A';
		first->next = last;
		last-> data  = UINT_MAX;
		last-> name;
		last-> grade = 'B';
		last-> next  = NULL;
		printf("list initialized\n");

		//build the list

		while (3 == fscanf(fpi, "%u %s %c", &id, iname, &igrade)){
			//printf("inserting:%p \t%09u \t%s \t%c\n",first , id, iname, igrade);
			insertList(first, id, iname, igrade);
//			printList(fpo, last);

		}

		//print the sorted list

		printList(fpo, first);

		//clean up

		freeList(first);
//		printf("%p",last);
		first->next = last;	//this is important  freeList destroyed this link

		//Do it again  This will help insure you pass on the server.
		//If you fail on the second round the likely cause is that
		//you forgot to initialize something.

		if (argc > 3) {
			fpi = fopen(argv[3], "r");
			if (fpi == NULL) {printf("%s failed to open\n", argv[3]); return -1;}
		}
		if (argc > 4) {
				fpo = fopen(argv[4], "w");
				if (fpo == NULL) {printf("%s failed to open\n", argv[4]); return -1;}
		}


		while (3 == fscanf(fpi, "%u %s %c", &id, iname, &igrade)){
			//printf("inserting: %09u \t%s \t%c\n", id, iname, igrade);
			insertList(first, id, iname, igrade);

		}

		//print the sorted list
		printList(fpo, last);

		//clean up

		freeList(first);
		first->next = last;

		free(last);
		free(first);

		fclose(fpi);
		fclose(fpo);

		return 0;

}
