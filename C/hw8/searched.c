/*
 * searched.c
 *
 *  Created on: Apr 18, 2015
 *      Author: Michael
 */

#include <stdio.h>
#include "hw8.h"



searchedArray(int SizeV, int SizeH, int searched[][SizeH]){

	int i, j;


	printf("\n Searched Array \n");
	for (i = 0; i < SizeV; i++){
		for(j = 0; j <= SizeH; j++){
			if (j == SizeH) {
				printf("\n");
			}
			else{
//			printf("(%d %d)", i, j);
			printf(" %d ",searched[i][j]);
			}

		}
	}

}
