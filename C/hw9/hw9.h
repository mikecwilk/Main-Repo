/*
 * hw9.h
 *
 *  Created on: Nov 13, 2012
 *  Updated on: Nov 19, 2014
 *      Author: Tom
 */

struct ListNode {
	unsigned int data;
	char name[16];
	char grade;
	struct ListNode *next;
};

typedef struct ListNode * Lptr;
typedef unsigned int ID_t;

#define NSIZE 16
// global variables
struct ListNode *first, *last;
unsigned int id;
char iname[NSIZE], igrade;

void insertList(Lptr lptr, ID_t idata, char *iname, char igrade);
void printList(FILE *fpo, Lptr lptr);
void freeList(Lptr lptr);
