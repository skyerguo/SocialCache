def get_neareast_friend_post(curr_user_id, curr_adj_post_list, curr_viewed_post_list):
    '''
        curr_user_id：当前用户的user_id，类别为int
        curr_adj_post_list：当前用户的邻居节点的publish的post的列表，按照时间从小到大排序，列表中每个点存储一个数字，表示post_id
        curr_viewed_post_list：当前用户访问过的post列表，列表中每个点存储一个数字
    '''
    # flag_get_result = False
    for i in range(len(curr_adj_post_list) -1, 0, -1):
        if curr_adj_post_list[i] not in curr_viewed_post_list:
            # flag_get_result = False
            return curr_adj_post_list[i]
    return None    