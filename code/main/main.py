from code.build.build_main import Build_network
from code.trace.make_trace_naive import Make_trace
from code.cache.redis_cache.redis_cache import Redis_cache
import easygraph as eg
import networkx
import code.util.util as util
import code.util.SIR as SIR
from mininet.cli import CLI
import json
import os
import time
import random
import math
import numpy as np
import pickle

class Main:
    def __init__(self, trace_dir, use_http_server=False, if_debug=False):

        self.if_debug = if_debug

        self.build_network = Build_network()
        self.build_network.run(self.if_debug)

        self.topo = json.load(open('code/build/topo.json', 'r'))
        level_3_area_id = self.topo['level_3_id']
        self.level_3_area_location = []
        for area_id in level_3_area_id:
            self.level_3_area_location.append(self.topo["areaid2position"][str(area_id)])

        self.trace_dir = trace_dir
        os.system("mkdir -p data/traces/" + self.trace_dir)
        self.G = eg.DiGraph()
        self.G.add_edges_from_file("data/traces/" + self.trace_dir + "/relations.txt")

        self.use_http_server = use_http_server

        self.social_metric_dict_path = 'data/social_metric_dict/' + self.trace_dir + '/'
        os.system("mkdir -p %s"%(self.social_metric_dict_path))

    def start_http_server(self, host, db, host_ip, temp_picture_path):
        '''
            在每个节点启动HTTP server.
            The port number is 4333 + db
        '''

        '''清空temp文件夹，创建对应ip的result文件夹'''
        util.reflush_path(temp_picture_path)
        os.system('mkdir -p ' + self.result_path + 'http/' + host_ip)
        os.system('mkdir -p ' + self.result_path + 'curl/' + host_ip)
        os.system('mkdir -p ' + self.result_path + 'wget/' + host_ip)
        os.system('mkdir -p ' + self.result_path + 'flow/' + host_ip)
        
        host.cmdPrint('cd %s && nohup python3 /users/gtc/SocNet/code/util/simple_httpserver.py -l %s -p %s -n 1>> %s/http_log1.txt 2>> %s/http_log2.txt &'%(temp_picture_path, str(host_ip), str(4433+int(db)), self.result_path+'http/'+host_ip, self.result_path+'http/'+host_ip))
        

    '''更新实验配置，删除上一次实验记录'''
    def reflush_cache(self, use_LRU_cache=False):
        '''存储结果数据的文件夹'''
        self.result_path = '/proj/socnet-PG0/data/' + str(time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())) + '/'
        util.reflush_path(self.result_path)
        os.system("cp ./code/main/config.json %s"%(self.result_path)) ## 保存config文件，为了之后实验的分析方便
        
        os.system("ps -ef |grep simple_httpserver.py | grep -v grep | awk '{print $2}' | xargs sudo kill -9 > /dev/null 2>&1 && sleep 3") ## 删除之前的HTTP_server
        host_all = []
        for level_1_host_id in range(self.build_network.level_1_host_number):
            self.build_network.level_1_host[level_1_host_id].redis_cache = Redis_cache(
                db=len(host_all),
                host=self.build_network.level_1_host[level_1_host_id], 
                cache_size=CONFIG['cache_size_level_1'], 
                use_priority_queue=CONFIG['use_priority_queue'],
                use_LRU_cache=use_LRU_cache, 
                result_path=self.result_path,
                host_ip=self.build_network.level_1_host_ip[level_1_host_id],
                host_port=str(4433+len(host_all)),
                cache_level=1
            )

            if self.use_http_server:
                self.build_network.level_1_host[level_1_host_id].redis_cache.picture_root_path = '/proj/socnet-PG0/temp_media_data/' + str(len(host_all)) + '/picture/'
                self.start_http_server(host=self.build_network.level_1_host[level_1_host_id], db=len(host_all), host_ip=self.build_network.level_1_host_ip[level_1_host_id], temp_picture_path=self.build_network.level_1_host[level_1_host_id].redis_cache.picture_root_path)
            host_all.append(self.build_network.level_1_host[level_1_host_id])

        for level_2_host_id in range(self.build_network.level_2_host_number):
            self.build_network.level_2_host[level_2_host_id].redis_cache = Redis_cache(
                db=len(host_all), 
                host=self.build_network.level_2_host[level_2_host_id], 
                cache_size=CONFIG['cache_size_level_2'], 
                use_priority_queue=CONFIG['use_priority_queue'],
                use_LRU_cache=use_LRU_cache,
                result_path=self.result_path,
                host_ip=self.build_network.level_2_host_ip[level_2_host_id],
                host_port=str(4433+len(host_all)),
                cache_level=2
            )

            if self.use_http_server:
                self.build_network.level_2_host[level_2_host_id].redis_cache.picture_root_path = '/proj/socnet-PG0/temp_media_data/' + str(len(host_all)) + '/picture/'
                self.start_http_server(host=self.build_network.level_2_host[level_2_host_id], db=len(host_all), host_ip=self.build_network.level_2_host_ip[level_2_host_id], temp_picture_path=self.build_network.level_2_host[level_2_host_id].redis_cache.picture_root_path)
            host_all.append(self.build_network.level_2_host[level_2_host_id])

        for level_3_host_id in range(self.build_network.level_3_host_number):
            self.build_network.level_3_host[level_3_host_id].redis_cache = Redis_cache(
                db=len(host_all), 
                host=self.build_network.level_3_host[level_3_host_id], 
                cache_size=CONFIG['cache_size_level_3'], 
                use_priority_queue=CONFIG['use_priority_queue'],
                use_LRU_cache=use_LRU_cache,
                result_path=self.result_path,
                host_ip=self.build_network.level_3_host_ip[level_3_host_id],
                host_port=str(4433+len(host_all)),
                cache_level=3
            )

            if self.use_http_server:
                self.build_network.level_3_host[level_3_host_id].redis_cache.picture_root_path = '/proj/socnet-PG0/temp_media_data/' + str(len(host_all)) + '/picture/'
                self.start_http_server(host=self.build_network.level_3_host[level_3_host_id], db=len(host_all), host_ip=self.build_network.level_3_host_ip[level_3_host_id], temp_picture_path=self.build_network.level_3_host[level_3_host_id].redis_cache.picture_root_path)
            host_all.append(self.build_network.level_3_host[level_3_host_id])

        '''设置层级关系'''
        for level_3_host_id in range(self.build_network.level_3_host_number):
            bind_level_2_id = self.topo['up_bind_3_2'][level_3_host_id]
            self.build_network.level_3_host[level_3_host_id].redis_cache.higher_cache_redis = self.build_network.level_2_host[bind_level_2_id].redis_cache
            self.build_network.level_3_host[level_3_host_id].redis_cache.higher_cache_id = bind_level_2_id
            self.build_network.level_3_host[level_3_host_id].redis_cache.higher_cache_level = 2

        for level_2_host_id in range(self.build_network.level_2_host_number):
            bind_level_1_id = self.topo['up_bind_2_1'][level_2_host_id]
            self.build_network.level_2_host[level_2_host_id].redis_cache.higher_cache_redis = self.build_network.level_1_host[bind_level_1_id].redis_cache
            self.build_network.level_2_host[level_2_host_id].redis_cache.higher_cache_id = bind_level_1_id
            self.build_network.level_2_host[level_2_host_id].redis_cache.higher_cache_level = 1

        self.find_success_number = [0, 0, 0, 0]
        self.find_fail_number = [0, 0, 0, 0]
        
        if self.use_http_server:
            time.sleep(5) ## 等待5秒，让HTTP server启动


    def main(self, caching_policy):
        '''read_trace'''
        if caching_policy == "LRU":
            self.reflush_cache(use_LRU_cache=True)
        else:
            self.reflush_cache(use_LRU_cache=False)
        
        if caching_policy == "FIFO" or caching_policy == "RAND":
            need_update_cache = False
        else:
            need_update_cache = True
        
        '''SocCache + social network metrics'''
        if caching_policy == 'PageRank':
            curr_social_metric_path = self.social_metric_dict_path + 'PageRank.pkl'
            if os.path.exists(curr_social_metric_path):
                page_rank_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                page_rank_metrics = eg.functions.not_sorted.pagerank(self.G)
                pickle.dump(page_rank_metrics, open(curr_social_metric_path, "wb"))
            # print("page_rank_metrics: ", page_rank_metrics)

        elif caching_policy == "Degree":
            '''To use it, remember the key is str type, and the value is bool'''
            degree_metrics = self.G.in_degree()
            # print("degree_metrics: ", degree_metrics)

        elif caching_policy == "BetweennessCentrality":
            curr_social_metric_path = self.social_metric_dict_path + 'BetweennessCentrality.pkl'
            if os.path.exists(curr_social_metric_path):
                betweenness_centrality_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                betweenness_centrality_metrics = eg.functions.centrality.betweenness.betweenness_centrality(self.G)
                pickle.dump(betweenness_centrality_metrics, open(curr_social_metric_path, "wb"))
            # print("betweenness_centrality_metrics: ", betweenness_centrality_metrics)

        elif caching_policy == "LaplacianCentrality":
            curr_social_metric_path = self.social_metric_dict_path + 'LaplacianCentrality.pkl'
            if os.path.exists(curr_social_metric_path):
                laplacian_centrality_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                laplacian_centrality_metrics = eg.functions.not_sorted.laplacian(self.G)
                pickle.dump(laplacian_centrality_metrics, open(curr_social_metric_path, "wb"))
            # print("laplacian_centrality_metrics: ", laplacian_centrality_metrics)

        elif caching_policy == "EffectiveSize":
            curr_social_metric_path = self.social_metric_dict_path + 'EffectiveSize.pkl'
            if os.path.exists(curr_social_metric_path):
                effective_size_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                adj_matrix = util.generate_adj_matrix_graph("data/traces/" + self.trace_dir + "/relations.txt", len(self.G.nodes))
                networkx_graph = networkx.DiGraph(adj_matrix).reverse() ## 关注的方向，传播需要反向
                '''easygraph的constraint只能针对无向图，networkx的constraint可以针对有向图'''
                effective_size_metrics = networkx.effective_size(networkx_graph)
                pickle.dump(effective_size_metrics, open(curr_social_metric_path, "wb"))
            # print("effective_size_metrics: ", effective_size_metrics)

        elif caching_policy == "LRU-social":
            curr_social_metric_path = self.social_metric_dict_path + 'LRUSocial.pkl'
            if os.path.exists(curr_social_metric_path):
                spreading_power_list = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                all_degree_dict = self.G.degree()
                parameter_k = np.mean(list(all_degree_dict.values()))
                epidemic_threshold = parameter_k / (parameter_k * parameter_k - parameter_k)
                # print("epidemic_threshold: ", epidemic_threshold)

                adj_matrix = util.generate_adj_matrix_graph("data/traces/" + self.trace_dir + "/relations.txt", len(self.G.nodes))
                networkx_graph = networkx.DiGraph(adj_matrix)
                spreading_power_list = [0 for _ in range(len(self.G.nodes))]
                for i in range(len(self.G.nodes)):
                    spreading_number = SIR.SIR_network(networkx_graph, [i] , epidemic_threshold, 1, 1)
                    spreading_power_list[i] = (spreading_number - 1) / CONFIG['cache_size_level_3'] + 1 # 如果没有传播，设置为1，即和LRU等同。
                    # spreading_power_list[i] = SIR.SIR_network(networkx_graph, [i] , epidemic_threshold, 1, 1, 1)
                pickle.dump(spreading_power_list, open(curr_social_metric_path, "wb"))
                
            # print("spreading_power_list: ", spreading_power_list)

        f_in = open("data/traces/" + self.trace_dir + "/all_timeline.txt", "r")
        f_out_find = open(self.result_path + 'find_log.txt', 'w')
        f_out_insert = open(self.result_path + 'insert_log.txt', 'w')
        f_out_time = open(self.result_path + 'time_log.txt', 'w')
        start_time = time.time()
        print("start_time: %f"%(start_time), file=f_out_time)
        cnt_line = 0 
        print("cnt_line: ", cnt_line)
        last_timestamp = -1
        for line in f_in:
            cnt_line += 1
            if cnt_line % 10000 == 0:
                print("cnt_line: ", cnt_line)
            if CONFIG['max_trace_len'] and cnt_line > CONFIG['max_trace_len']:
               break 
            current_type = line.split('+')[-1].strip()
            current_location = eval(line.split('+')[2])
            current_timestamp = float(line.split('+')[0])
            if math.floor(current_timestamp) == math.floor(last_timestamp):
                current_timestamp = last_timestamp + 0.001
            last_timestamp = current_timestamp

            [selected_level_3_id, nearest_distance] = util.find_nearest_location(current_location, self.level_3_area_location)

            if current_type == "post":
                post_id = int(line.split('+')[4])
                user_id = int(line.split('+')[3])
                media_size = float(line.split('+')[1])

                if caching_policy == 'RAND':
                    sort_value = random.randint(0, 1000)

                elif caching_policy == 'FIFO' or caching_policy == 'LRU':
                    sort_value = current_timestamp

                elif caching_policy == 'PageRank':
                    sort_value = current_timestamp + \
                                int(nearest_distance) * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                page_rank_metrics[str(user_id)] * CONFIG['params'][2]

                elif caching_policy == "Degree":
                    sort_value = current_timestamp + \
                                int(nearest_distance) * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                degree_metrics[str(user_id)] * CONFIG['params'][2]

                elif caching_policy == "BetweennessCentrality":
                    sort_value = current_timestamp + \
                                int(nearest_distance) * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                betweenness_centrality_metrics[str(user_id)] * CONFIG['params'][2]
                    
                elif caching_policy == "LaplacianCentrality":
                    sort_value = current_timestamp + \
                                int(nearest_distance) * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                laplacian_centrality_metrics[str(user_id)] * CONFIG['params'][2]

                elif caching_policy == "EffectiveSize":
                    if math.isnan(effective_size_metrics[user_id]):
                        effective_size_metrics[user_id] = 0
                    sort_value = current_timestamp + \
                                int(nearest_distance) * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                effective_size_metrics[user_id] * CONFIG['params'][2]
                    
                elif caching_policy == "LRU-social" or caching_policy == "LRU-label":
                    '''LRU-social and LRU-label can adjust the sort_value automatically'''
                    sort_value = 0
                    
                '''记录redis_object，使用json形式保存'''
                temp_redis_object = {
                    'sort_value': sort_value,
                    'media_size': media_size,
                    'timestamp': current_timestamp
                }

                print(cnt_line, selected_level_3_id, temp_redis_object, file=f_out_insert)

                if self.if_debug:
                    print("post_id: ", post_id)
                    print("user_id: ", user_id)
                    print("selected_level_3_id: ", selected_level_3_id)
                    print("temp_redis_object: ", temp_redis_object)
                
                '''往第三层级插入，后续的调整都由redis内部完成'''
                if caching_policy == "LRU-social":
                    self.build_network.level_3_host[selected_level_3_id].redis_cache.insert(picture_hash=post_id, redis_object=temp_redis_object, need_uplift=True, use_LRU_label=False, use_LRU_social=True, first_insert=True, lru_social_parameter_sp=spreading_power_list[user_id])
                elif caching_policy == "LRU-label":
                    self.build_network.level_3_host[selected_level_3_id].redis_cache.insert(picture_hash=post_id, redis_object=temp_redis_object, need_uplift=True, use_LRU_label=True, use_LRU_social=False)
                else:
                    self.build_network.level_3_host[selected_level_3_id].redis_cache.insert(picture_hash=post_id, redis_object=temp_redis_object, need_uplift=True, use_LRU_label=False, use_LRU_social=False)

            elif current_type == "view":
                post_id = int(line.split('+')[1])
                # user_id = int(line.split('+')[3])
                '''往第三层级查询，后续的调整都由redis内部完成，这里先假设只有一个user节点'''
                if caching_policy == "LRU-social":
                    find_result = self.build_network.level_3_host[selected_level_3_id].redis_cache.find(picture_hash=post_id, user_host=self.build_network.user_host[0], current_timestamp=current_timestamp, need_update_cache=need_update_cache, config_timestamp=1, use_LRU_label=False, use_LRU_social=True)
                elif caching_policy == "LRU-label":
                    find_result = self.build_network.level_3_host[selected_level_3_id].redis_cache.find(picture_hash=post_id, user_host=self.build_network.user_host[0], current_timestamp=current_timestamp, need_update_cache=need_update_cache, config_timestamp=1, use_LRU_label=True, use_LRU_social=False)
                else:
                    find_result = self.build_network.level_3_host[selected_level_3_id].redis_cache.find(picture_hash=post_id, user_host=self.build_network.user_host[0], current_timestamp=current_timestamp, need_update_cache=need_update_cache, config_timestamp=1, use_LRU_label=False, use_LRU_social=False)
                result_level = find_result[0]
                
                if self.if_debug:
                    print(result_level)

                if result_level == 0:
                    '''所有level的cache都没有找到'''
                    print("!!!! ", cnt_line)
                    continue

                print(cnt_line, selected_level_3_id, result_level, find_result[1], file=f_out_find)
                
                for temp_level in range(3, result_level, -1):
                    self.find_fail_number[temp_level] += 1
                self.find_success_number[result_level] += 1
            else:
                print("ERROR!")
        end_time = time.time()
        print("end_time: %f"%(end_time), file=f_out_time)
        print("time_duration: %f"%(end_time - start_time), file=f_out_time)
        f_in.close()
        f_out_insert.close()
        f_out_find.close()
        f_out_time.close()

        if self.use_http_server == True:
            for level_3_host_id in range(self.build_network.level_3_host_number):
                for eth_port in range(self.build_network.level_2_host_number): # 对应第二层的每一个节点
                    util.calculate_flow(host=self.build_network.level_3_host[level_3_host_id], eth_name='c%s-eth%s'%(str(level_3_host_id), str(eth_port)), flow_direction='TX', result_path=self.result_path+'flow/'+self.build_network.level_3_host_ip[level_3_host_id])

            for level_2_host_id in range(self.build_network.level_2_host_number):
                for eth_port in range(self.build_network.level_1_host_number): # 对应第一层的每一个节点，以及自己的switch
                    util.calculate_flow(host=self.build_network.level_2_host[level_2_host_id], eth_name='b%s-eth%s'%(str(level_2_host_id), str(eth_port)), flow_direction='TX', result_path=self.result_path+'flow/'+self.build_network.level_2_host_ip[level_2_host_id])

            for level_1_host_id in range(self.build_network.level_1_host_number):
                for eth_port in range(1): # 对应自己的switch
                    util.calculate_flow(host=self.build_network.level_1_host[level_1_host_id], eth_name='a%s-eth%s'%(str(level_1_host_id), str(eth_port)), flow_direction='TX', result_path=self.result_path+'flow/'+self.build_network.level_1_host_ip[level_1_host_id])


    def run(self, caching_policy):
        self.main(caching_policy=caching_policy)

if __name__ == '__main__':
    CONFIG = json.load(open('./code/main/config.json', 'r'))
    main_program = Main(trace_dir=CONFIG['trace_dir'], use_http_server=CONFIG['use_http_server'], if_debug=CONFIG['mode']=='debug')
    main_program.run(caching_policy=CONFIG['caching_policy'])
