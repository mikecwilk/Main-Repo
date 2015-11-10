/*
By Michael Wilk
4-23-15
CS 49C Section 2
Homework 9
program for insertList

*/

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>
#include "hw9.h"

typedef struct ListNode Lnode;
#define NSIZE 16
// global variables
struct ListNode *first, *last;
unsigned int id;
char iname[NSIZE], igrade;


void insertList(struct ListNode *lptr, unsigned int idata, char *iname, char igrade){

	struct ListNode* NewNode = (struct ListNode*) malloc(sizeof(Lnode));
	struct ListNode* current;


//	printf("%09u  \t%s  \t%c\n ", lptr->next->data, lptr->next->name, lptr->next->grade);

	NewNode->data = idata;
	strcpy(NewNode->name, iname);
	NewNode->grade = igrade;

	if ((lptr->next->data) == UINT_MAX){

        first = lptr;
        first->next = NewNode;
//        last = NewNode;
    	current = first;

    }else{

//    	printf("----------------------------------------------------------\n");
    	current = first;

//    	printf("\nNewNode data: %9u current data: %u current next data %u , last data%u\n", NewNode-> data, current->data, current->next->data, last->data);
    	if (((NewNode->data) > (current->data)) && ((NewNode->data) < (current->next->data))){

			NewNode->next = current->next;
			current->next = NewNode;


    	}else if(((NewNode->data) > (current->data)) && ((NewNode->data) > (current->next->data))){



    		while (current->next != NULL){

    			current = current ->next;
//    			printf("\ncurrent->data %u\n",current -> data);
//    			printf("NewNode->data %u\n",NewNode ->data);
    			if (current->next != NULL){
					if((NewNode ->data) < (current -> next-> data)){
//						printf("break");
						break;
					}
    			}

    		}



    		if (current->next == NULL){
//				printf("poop");
				current->next = NewNode;
				NewNode->next = NULL;




    	}else if ((NewNode ->data) < (current -> next -> data)){
//    			printf("break");
//				printf("\ncurrent->data %u\n",current -> data);
//				printf("NewNode->data %u\n",NewNode ->data);
//				printf("\ncurrent->next %u\n",current -> next->data);
//				printf("NewNode->next %u\n",NewNode ->next->data);
				NewNode->next = current->next;
				current->next = NewNode;


    	}


    }
	current = first;

//	while(current->next != NULL){
//		current = current->next;
//		printf("%09u  \t%s  \t%c\n", current->data, current->name, current->grade);


//	}


 }

}


void printList(FILE *fpo, struct ListNode *lptr) {


	struct ListNode* printNode;
	lptr = first;
	printNode = lptr;


//printf("Printing...");
	while( printNode->next != 0){
		if(printNode->data == 0){
			printNode = printNode->next;
		}
//		printf("%09u  \t%s  \t%c\n ", printNode->data, printNode->name, printNode->grade);
		fprintf(fpo, "%09u  \t%s  \t%c\n ", printNode->data, printNode->name, printNode->grade);
		printNode = printNode->next;

	}
	fprintf(fpo, "%09u  \t%s  \t%c\n ", printNode->data, printNode->name, printNode->grade);


}

void freeList(struct ListNode *lptr){

	struct ListNode* temp ;


//printf("\nfreeing\n");
	while( lptr->next->next != NULL){

		if(lptr->data == 0){
			lptr = lptr->next;
		}else{
			temp = lptr;
//			printf("%09u  \t%s  \t%c\n ", temp->data, temp->name, temp->grade);
			free(temp);
			lptr = lptr->next;

		}


	}
	temp = lptr;
//	printf("%09u  \t%s  \t%c\n ", temp->data, temp->name, temp->grade);




}




