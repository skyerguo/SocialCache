#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FILE_NAME ("./relations.txt")

typedef struct neighbor_info
{
    int nei_num;
    int *neighbors;
}neighbor_info_t;

typedef struct effective_size {
    char **adj_matrix;  //memory used to store adj_matrix
    int node_num; // number of nodes
    float *effective_size_arr; // array of effective size for each node
    neighbor_info_t *neighbors_arr; // array of neighbor info for each node
}effective_size_t;