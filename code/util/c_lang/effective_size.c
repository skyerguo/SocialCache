//**********************************************************************
//*                                                                    *
//*     Using multi-core computing for effectvie size                  *
//*                                                                    *
//**********************************************************************
//
//  Algorithm:
//  
//  1. Construct Graph
//      [1] Reading graph from edge files
//      [2] Initiating adjencent array
//  2. Rank with node degree
//  3. Divide the tasks
//  4. Multi-core computing
//
//
#include "effective_size.h"

#define MUTUAL_WEIGHT(context, node_i, node_j) \
    ((float)((context)->adj_matrix[(node_i)][(node_j)] == '1' ? 1 : 0) + \
     (float)((context)->adj_matrix[(node_j)][(node_i)] == '1' ? 1 : 0))

#define NORMALIZED_MUTUAL_WEIGHT(context, node_i, node_j, max) \
    ({ \
        float nmw = 0; \
        neighbor_info_t node_i_nei = (context)->neighbors_arr[(node_i)]; \
        for (int i = 0; i < node_i_nei.nei_num; i++) \
        { \
            int node_nei = node_i_nei.neighbors[i]; \
            float mw = MUTUAL_WEIGHT(context, (node_i), (node_nei)); \
            if ((max) == 1) \
            { \
                nmw = (nmw < mw) ? mw : nmw; \
            } \
            else \
            { \
                nmw += mw; \
            } \
        } \
        (nmw == 0) ? 0 : MUTUAL_WEIGHT(context, (node_i), (node_j)) / nmw; \
    })

/*
 * Construct Graph
 */
int load_graph_from_file(effective_size_t *context, int reverse)
{
    printf("$func: %s\n", __FUNCTION__);
    FILE *file;
    file = fopen(context->file_name, "r");
    if (file == NULL)
    {
        perror("Unable to open file.\n");
        return -1;
    }

    int num_nodes = 0;
    int num_lines = 0;
    int node1, node2;

    // find the biggest ID to determine the dimension of the adjecent matrix
    while (fscanf(file, "%d %d", &node1, &node2) == 2)
    {
        num_lines++;
        if (num_lines % 1000000 == 0)
        {
            printf("# totally %d lines handled.\n", num_lines);
        }
        num_nodes = (node1 > num_nodes)? node1:num_nodes;
        num_nodes = (node2 > num_nodes)? node2:num_nodes;
    }

    num_nodes++;
    context->node_num = num_nodes;
    printf("# get %d nodes.\n", num_nodes);

    // init adj array
    context->nei_num_arr = (int *)malloc(num_nodes*sizeof(int));

    // alloc memroy for adjecent matrix
    char **adj_matrix = (char **)malloc(num_nodes*sizeof(char*));
    for (int i=0; i<num_nodes; i++)
    {
        adj_matrix[i] = (char *)malloc(num_nodes * sizeof(char));
        for (int j=0; j<num_nodes; j++)
        {
            adj_matrix[i][j] = '0';
        }
    }
    printf("# memeory alloced for adjecent matrix.\n");

    // go back to head of file and read edges
    fseek(file, 0, SEEK_SET);
    num_lines = 0;
    while(fscanf(file, "%d %d", &node1, &node2) == 2)
    {
        if ((++num_lines % 1000000) == 0)
        {
            printf("# totally %d lines handled.\n", num_lines);
        }
        if (reverse == 1)
        {
            adj_matrix[node2][node1] = '1';
        }else{
            adj_matrix[node1][node2] = '1';
        }
#if 0
        if (!context->is_directed)
        {
            adj_matrix[node2][node1] = '1';
        }
#endif
    }

    context->adj_matrix = adj_matrix;

    fclose(file);
    return num_nodes;
}

int init_graph_neighbor_arr(effective_size_t* effective_size)
{
    printf("$func: %s\n", __FUNCTION__);
    char **adj_matrix = effective_size->adj_matrix;;
    int num_nodes = effective_size->node_num;

    effective_size->neighbors_arr = (neighbor_info_t*)malloc(num_nodes*sizeof(neighbor_info_t));

    int process_bar = 0;
    for (int i=0; i<num_nodes; i++)
    {
        process_bar++;
        // get neighbor number
        neighbor_info_t *nei_info = &(effective_size->neighbors_arr[i]);
        memset(nei_info, 0, sizeof(neighbor_info_t));
        for (int j=0; j<num_nodes; j++)
        {
            // in edge and out edge
            if (adj_matrix[i][j] == '1' || adj_matrix[j][i] == '1')
            {
                nei_info->nei_num++;
            }
        }

        //printf("# Node %d with %d neighbors. \n", i, nei_info->nei_num);
        // alloc memory for neighbors id
        nei_info->neighbors = (int*)malloc(nei_info->nei_num * sizeof(int));
        for (int j=0,k=0; j<num_nodes; j++)
        {
            if (adj_matrix[i][j] == '1' || adj_matrix[j][i] == '1')
            {
                nei_info->neighbors[k++] = j;
            }
        }
        if (process_bar % 10000 == 0)
        {
            printf("# [%d/%d] nodes handled.\n", process_bar, effective_size->node_num);
        }
    }

    return 1;
}

float redundancy(effective_size_t *context, int node_i, int node_j)
{
    char **matrix = context->adj_matrix;
    neighbor_info_t node_i_nei = context->neighbors_arr[node_i];

    float r = 0;
    for (int i=0; i<node_i_nei.nei_num; i++)
    {
        int node_w = node_i_nei.neighbors[i];
        //printf("# comput pm and wm of neighbor %d\n", node_w);
        r += NORMALIZED_MUTUAL_WEIGHT(context, node_i, node_w, 0) * NORMALIZED_MUTUAL_WEIGHT(context, node_j, node_w, 1);    
    }

    return 1 - r;
}

int compute_effective_size_for_each_node(effective_size_t* context)
{
    printf("$func: %s\n", __FUNCTION__);
    char **matrix = context->adj_matrix;
    int num_nodes = context->node_num;
    context->effective_size_arr = (float *)malloc(num_nodes*sizeof(float));

    for (int i = 0; i < num_nodes; i++)
    {
        printf("# Processing node : %d\n", i);
        float effective = 0;
        neighbor_info_t nei_info = context->neighbors_arr[i];
        if (nei_info.nei_num <= 0)
        {
            context->effective_size_arr[i] = -1;
            continue;
        }

        if (context->is_directed == 1)
        {
            // ###### 1. compute effective size of node in
            for (int j = 0; j < nei_info.nei_num; j++)
            {
                int node_j = nei_info.neighbors[j];
                // printf("# calculating redundancy of neighbor %d\n", node_j);
                effective += redundancy(context, i, node_j);
            }
        }
        else
        {
            // ###### 1. count number of edges of ego network ######
            int num_ties = 0;
            for (int p=0; p<nei_info.nei_num; p++)
            {
                int node_p = nei_info.neighbors[p];
                for (int q=p; q<nei_info.nei_num; q++)
                {
                    int node_q = nei_info.neighbors[q];
                    if (context->adj_matrix[node_p][node_q] == '1' || context->adj_matrix[node_q][node_p] == '1')
                    {
                        num_ties++;
                    }

                }
            }

            effective = nei_info.nei_num - (float)(2*num_ties) / nei_info.nei_num;
        }

        printf("# Node effective size : %f\n", effective);
        context->effective_size_arr[i] = effective;
    }
}

int save_to_csv(float *effective_size_arr, int len)
{
    printf("$func %s \n", __FUNCTION__);
    if (!effective_size_arr) return 0;

    FILE *file;
    file = fopen("./effective_size.csv", "w+");

    fprintf(file, "NodeID,EffectiveSize\n");
    for (int i=0; i<len; i++)
    {
        fprintf(file, "%d,%f\n", i, effective_size_arr[i]);
    }
    
    fclose(file);
}



int main(int argc, char *argv[])
{
    int opt;
    int reverse_option = 0;
    char *file_name_option = NULL;

    // parse command line
    while ((opt = getopt(argc, argv, "r:f:")) != -1)
    {
        switch (opt)
        {
        case 'r':
            reverse_option = atoi(optarg);
            break;
        case 'f':
            file_name_option = optarg;
            break;
        default:
            fprintf(stderr, "Usage: %s -r <integer> -f <string>\n", argv[0]);
            exit(EXIT_FAILURE);
            break;
        }
    }

    effective_size_t effsize;
    effsize.is_directed = 0;
    snprintf(effsize.file_name, sizeof(effsize.file_name), file_name_option);

    load_graph_from_file(&effsize, reverse_option);
    printf("$ Success to read graph with %d nodes.\n", effsize.node_num);

    init_graph_neighbor_arr(&effsize);

    compute_effective_size_for_each_node(&effsize);

    save_to_csv(effsize.effective_size_arr, effsize.node_num);

    return 0;
}