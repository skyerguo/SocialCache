#include "effective_size.h"

int load_graph_from_file(const char* file_name, char ***matrix)
{
    printf("$func: %s\n", __FUNCTION__);
    FILE *file;
    file = fopen(file_name, "r");

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
    printf("# get %d nodes.\n", num_nodes);

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

    // go back to head of file
    fseek(file, 0, SEEK_SET);

    num_lines = 0;
    while(fscanf(file, "%d %d", &node1, &node2) == 2)
    {
        if ((++num_lines % 1000000) == 0)
        {
            printf("# totally %d lines handled.\n", num_lines);
        }
        adj_matrix[node1][node2] = '1'; // set edge
    }

    fclose(file);

    *matrix = adj_matrix;

    return num_nodes;
}

int init_graph_neighbor_arr(effective_size_t* effective_size)
{
    printf("$func: %s\n", __FUNCTION__);
    char **adj_matrix;
    int num_nodes;

    adj_matrix = effective_size->adj_matrix;
    num_nodes = effective_size->node_num;
    effective_size->neighbors_arr = (neighbor_info_t*)malloc(num_nodes*sizeof(neighbor_info_t));
    for (int i=0; i<effective_size->node_num; i++)
    {
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

        printf("# Node %d with %d neighbors. \n", i, nei_info->nei_num);
        // alloc memory for neighbors id
        nei_info->neighbors = (int*)malloc(nei_info->nei_num * sizeof(int));
        for (int j=0,k=0; j<num_nodes; j++)
        {
            if (adj_matrix[i][j] == '1' || adj_matrix[j][i] == '1')
            {
                nei_info->neighbors[k++] = j;
            }
        }
    }

    return 1;
}

float mutal_weight(effective_size_t *context, int node_i, int node_j)
{
    char **matrix = context->adj_matrix;
    int w_ij = (matrix[node_i][node_j] == '1')?1:0;
    int w_ji = (matrix[node_j][node_i] == '1')?1:0;

    return (float)(w_ij+w_ji);
}

float normalized_mutual_weight(effective_size_t *context, int node_i, int node_j, int max)
{
    float nmw = 0;
    neighbor_info_t node_i_nei = context->neighbors_arr[node_i];
    for (int i=0; i<node_i_nei.nei_num; i++)
    {
        int node_nei = node_i_nei.neighbors[i];
        float mw = mutal_weight(context, node_i, node_nei);
        if (max == 1)
        {
            //max
            nmw = (nmw<mw)?mw:nmw;
        }else
        {
            //sum
            nmw += mw;
        }
    }
    if (nmw == 0) return 0;
    return mutal_weight(context, node_i, node_j)/nmw;
}

float redundancy(effective_size_t *context, int node_i, int node_j)
{
    char **matrix = context->adj_matrix;
    neighbor_info_t node_i_nei = context->neighbors_arr[node_i];

    float r = 0;
    for (int i=0; i<node_i_nei.nei_num; i++)
    {
        int node_w = node_i_nei.neighbors[i];
        r += normalized_mutual_weight(context, node_i, node_w, 0) * normalized_mutual_weight(context, node_j, node_w, 1);    
    }

    return 1 - r;
}

int compute_effective_size_for_each_node(effective_size_t* effective_size)
{
    printf("$func: %s\n", __FUNCTION__);
    char **matrix = effective_size->adj_matrix;
    int num_nodes = effective_size->node_num;
    effective_size->effective_size_arr = (float *)malloc(num_nodes*sizeof(float));

    for(int i=0; i<num_nodes; i++)
    {
        printf("# Processing node : %d\n", i);
        // ###### 1. Get neighbors info ######
        // get neighbors
        neighbor_info_t nei_info = effective_size->neighbors_arr[i];
        if (nei_info.nei_num <= 0)
        {
            effective_size->effective_size_arr[i] = -1;
            continue;
        }
    
        // ###### 2. compute effective size of node i
        float effective = 0;
        for (int j=0; j<nei_info.nei_num; j++)
        {
            int node_j = nei_info.neighbors[j];
            effective += redundancy(effective_size, i, node_j);
        }
        printf("# Node effective size : %f\n", effective);
        effective_size->effective_size_arr[i] = effective;
    }
}

int main()
{
    effective_size_t effsize;

    effsize.node_num = load_graph_from_file(FILE_NAME, &(effsize.adj_matrix));

    // head matrix
    for (int i=0; i<4; i++)
    {
        for (int j=0; j<4; j++)
        {
            printf("%c ", effsize.adj_matrix[i][j]);
        }
        printf("\n");
    }

    init_graph_neighbor_arr(&effsize);

    compute_effective_size_for_each_node(&effsize);

    return 0;
}