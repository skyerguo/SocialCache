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
            if (adj_matrix[i][j] == '1') nei_info->nei_num++;
        }

        printf("# Node %d with %d neighbors. \n", i, nei_info->nei_num);
        // alloc memory for neighbors id
        nei_info->neighbors = (int*)malloc(nei_info->nei_num * sizeof(int));
        for (int j=0,k=0; j<num_nodes; j++)
        {
            if (adj_matrix[i][j] == '1') nei_info->neighbors[k++] = j;
        }
    }

    return 1;
}

int mutal_weight(char** matrix, int node_i, int node_j)
{
    return (matrix[node_i][node_j] == '1'?1:0) + (matrix[node_j][node_i] == '1'?1:0);
}

int redundancy(char **matrix, int node_i, int node_j)
{
    float r = 0;
    int node_j = nei_info.neighbors[j];
    int mutual_ij = (matrix[i][node_j] == '1' ? 1 : 0) + (matrix[node_j][i] == '1' ? 1 : 0);
    neighbor_info_t j_nei_info = effective_size->neighbors_arr[node_j];
    // printf("# Processing neighbor %d\n", node_j);

    for (int q = 0; q < j_nei_info.nei_num; q++)
    {
        // printf("# compute r\n");
        int node_q = j_nei_info.neighbors[q];
        // compute p_{iq}
        int sum_z_iq_qi = (matrix[i][node_q] == '1' ? 1 : 0) + (matrix[node_q][i] == '1' ? 1 : 0);
        if (sum_z_iq_qi == 0)
            continue;

        float p_iq = (float)sum_z_iq_qi / (sum_mutual_ij - mutual_ij);

        // compute m_{jq}
        int max_z_jk = 0;
        for (int k = 0; k < j_nei_info.nei_num; k++)
        {
            // printf("# compute the max mutal weight\n");
            int node_k = j_nei_info.neighbors[k];
            if (node_k == node_q)
                continue;
            int z_jk = (matrix[node_j][node_k] == '1' ? 1 : 0) + (matrix[node_k][node_j] == '1' ? 1 : 0);
            max_z_jk = (max_z_jk < z_jk) ? z_jk : max_z_jk;
        }
        int sum_z_jq_qj = (matrix[node_j][node_q] == '1' ? 1 : 0) + (matrix[node_q][node_j] == '1' ? 1 : 0);
        float m_jq = (float)sum_z_jq_qj / max_z_jk;

        r += p_iq * m_jq;
    }

    effective += 1 - r;
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

        float effective = 0;
        int sum_mutual_ij = 0;
        for (int j=0; j<nei_info.nei_num; j++)
        {
            int node_j = nei_info.neighbors[j];
            sum_mutual_ij += (matrix[i][node_j] == '1'? 1:0);
            sum_mutual_ij += (matrix[node_j][i] == '1'? 1:0);
        }
        printf("# Node %d with mutual weight %d\n", i, sum_mutual_ij);
    
        // ###### 2. do for each neighbors ######
        // process neighbors
        for (int j=0; j<nei_info.nei_num; j++)
        {
            int node_j = nei_info.neighbors[j];
            effective += 1 - redundancy(matrix, i, node_j);
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