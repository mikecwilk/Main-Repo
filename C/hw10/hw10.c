
#include "hw10.h"

void randomMove(hexPos *hp){
	int i, j;
	printf("RandMove\n");
	i = rand() % hp->SizeV;
	j = rand() % hp->SizeH;

	while(hp ->grid[i][j] != ' '){
		i = rand() % hp->SizeV;
		j = rand() % hp->SizeH;
	}
	printf("i and j : %d %d\n", i, j);


	hp -> grid[i][j] = 'g';

}
void mymove(hexPos *hp, FILE *fpi){

	int row, column;
	printf("MyMove\n");
	printf("%d\n", hp->toPlay);


	fscanf(fpi, "%d %d", &row, &column);

	if(hp->grid[row][column] != ' '){
		fscanf(fpi, "%d %d", &row, &column);
	}

	if(hp->toPlay == blue){
		hp -> grid[row][column] = 'b';
	}
	else if(hp->toPlay == gold){
			hp -> grid[row][column] = 'g';
		}

}




