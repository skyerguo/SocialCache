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
import multiprocessing

def calculate_spreading_power(i, networkx_graph, epidemic_threshold, n):
    spreading_number = SIR.SIR_network(networkx_graph, [i], epidemic_threshold, 1, 1)
    spreading_power = (spreading_number - 1) / n + 1
    return i, spreading_power

class Main:
    def __init__(self, trace_dir, use_http_server=False, if_debug=False):

        self.if_debug = if_debug

        self.build_network = Build_network()
        self.build_network.run(self.if_debug)

        self.topo = json.load(open('code/build/topo.json', 'r'))
        level_CDN_1_area_id = self.topo['level_CDN_1_id']
        self.level_CDN_1_area_location = []
        for area_id in level_CDN_1_area_id:
            self.level_CDN_1_area_location.append(self.topo["areaid2position"][str(area_id)])

        self.trace_dir = trace_dir
        os.system("mkdir -p data/traces/" + self.trace_dir)
        self.G = eg.DiGraph()
        self.G.add_edges_from_file("data/traces/" + self.trace_dir + "/relations.txt")

        self.use_http_server = use_http_server

        self.social_metric_dict_path = 'data/social_metric_dict/' + self.trace_dir + '/'
        os.system("mkdir -p %s"%(self.social_metric_dict_path))

        # being valid only if when using Second-Hit-LRU
        self.post_history = set()

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
    def reflush_cache(self, use_LRU_cache=False, use_OPT=False):
        '''存储结果数据的文件夹'''
        self.result_path = '/proj/socnet-PG0/data/' + str(time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())) + '/'
        util.reflush_path(self.result_path)
        os.system("cp ./code/main/config.json %s"%(self.result_path)) ## 保存config文件，为了之后实验的分析方便
        os.system("cp ./code/build/topo.json %s"%(self.result_path)) ## 保存topo文件
        
        os.system("ps -ef |grep simple_httpserver.py | grep -v grep | awk '{print $2}' | xargs sudo kill -9 > /dev/null 2>&1 && sleep 3") ## 删除之前的HTTP_server
        host_all = []
        for level_data_center_host_id in range(self.build_network.level_data_center_host_number):
            self.build_network.level_data_center_host[level_data_center_host_id].redis_cache = Redis_cache(
                db=len(host_all),
                host=self.build_network.level_data_center_host[level_data_center_host_id], 
                cache_size=CONFIG['cache_size_level_data_center'], 
                use_priority_queue=CONFIG['use_priority_queue'],
                use_LRU_cache=use_LRU_cache, 
                result_path=self.result_path,
                host_ip=self.build_network.level_data_center_host_ip[level_data_center_host_id],
                host_port=str(4433+len(host_all)),
                cache_level=1,
                cache_id=level_data_center_host_id,
                use_OPT=use_OPT,
                trace_dir=self.trace_dir
            )

            if self.use_http_server:
                self.build_network.level_data_center_host[level_data_center_host_id].redis_cache.picture_root_path = '/proj/socnet-PG0/temp_media_data/' + str(len(host_all)) + '/picture/'
                self.start_http_server(host=self.build_network.level_data_center_host[level_data_center_host_id], db=len(host_all), host_ip=self.build_network.level_data_center_host_ip[level_data_center_host_id], temp_picture_path=self.build_network.level_data_center_host[level_data_center_host_id].redis_cache.picture_root_path)
            host_all.append(self.build_network.level_data_center_host[level_data_center_host_id])

        for level_CDN_2_host_id in range(self.build_network.level_CDN_2_host_number):
            self.build_network.level_CDN_2_host[level_CDN_2_host_id].redis_cache = Redis_cache(
                db=len(host_all), 
                host=self.build_network.level_CDN_2_host[level_CDN_2_host_id], 
                cache_size=CONFIG['cache_size_level_CDN_2'], 
                use_priority_queue=CONFIG['use_priority_queue'],
                use_LRU_cache=use_LRU_cache,
                result_path=self.result_path,
                host_ip=self.build_network.level_CDN_2_host_ip[level_CDN_2_host_id],
                host_port=str(4433+len(host_all)),
                cache_level=2,
                cache_id=level_CDN_2_host_id,
                use_OPT=use_OPT,
                trace_dir=self.trace_dir
            )

            if self.use_http_server:
                self.build_network.level_CDN_2_host[level_CDN_2_host_id].redis_cache.picture_root_path = '/proj/socnet-PG0/temp_media_data/' + str(len(host_all)) + '/picture/'
                self.start_http_server(host=self.build_network.level_CDN_2_host[level_CDN_2_host_id], db=len(host_all), host_ip=self.build_network.level_CDN_2_host_ip[level_CDN_2_host_id], temp_picture_path=self.build_network.level_CDN_2_host[level_CDN_2_host_id].redis_cache.picture_root_path)
            host_all.append(self.build_network.level_CDN_2_host[level_CDN_2_host_id])

        for level_CDN_1_host_id in range(self.build_network.level_CDN_1_host_number):
            self.build_network.level_CDN_1_host[level_CDN_1_host_id].redis_cache = Redis_cache(
                db=len(host_all), 
                host=self.build_network.level_CDN_1_host[level_CDN_1_host_id], 
                cache_size=CONFIG['cache_size_level_CDN_1'], 
                use_priority_queue=CONFIG['use_priority_queue'],
                use_LRU_cache=use_LRU_cache,
                result_path=self.result_path,
                host_ip=self.build_network.level_CDN_1_host_ip[level_CDN_1_host_id],
                host_port=str(4433+len(host_all)),
                cache_level=3,
                cache_id=level_CDN_1_host_id,
                use_OPT=use_OPT,
                level_CDN_1_area_location=self.level_CDN_1_area_location,
                trace_dir=self.trace_dir
            )

            if self.use_http_server:
                self.build_network.level_CDN_1_host[level_CDN_1_host_id].redis_cache.picture_root_path = '/proj/socnet-PG0/temp_media_data/' + str(len(host_all)) + '/picture/'
                self.start_http_server(host=self.build_network.level_CDN_1_host[level_CDN_1_host_id], db=len(host_all), host_ip=self.build_network.level_CDN_1_host_ip[level_CDN_1_host_id], temp_picture_path=self.build_network.level_CDN_1_host[level_CDN_1_host_id].redis_cache.picture_root_path)
            host_all.append(self.build_network.level_CDN_1_host[level_CDN_1_host_id])

        '''设置层级关系'''
        for level_CDN_1_host_id in range(self.build_network.level_CDN_1_host_number):
            bind_level_CDN_2_id = self.topo['up_bind_3_2'][level_CDN_1_host_id]
            self.build_network.level_CDN_1_host[level_CDN_1_host_id].redis_cache.higher_CDN_redis = self.build_network.level_CDN_2_host[bind_level_CDN_2_id].redis_cache
            self.build_network.level_CDN_1_host[level_CDN_1_host_id].redis_cache.higher_CDN_id = bind_level_CDN_2_id
            self.build_network.level_CDN_1_host[level_CDN_1_host_id].redis_cache.higher_CDN_level = 2
            self.build_network.level_CDN_1_host[level_CDN_1_host_id].redis_cache.higher_CDN_delay = self.topo["delay_topo"][self.topo["level_CDN_1_id"][level_CDN_1_host_id]][self.topo["level_CDN_2_id"][bind_level_CDN_2_id]]
            self.build_network.level_CDN_1_host[level_CDN_1_host_id].redis_cache.higher_CDN_bandwidth = self.topo["bandwidth_topo"][self.topo["level_CDN_1_id"][level_CDN_1_host_id]][self.topo["level_CDN_2_id"][bind_level_CDN_2_id]]

        for level_CDN_2_host_id in range(self.build_network.level_CDN_2_host_number):
            bind_level_data_center_id = self.topo['up_bind_2_1'][level_CDN_2_host_id]
            self.build_network.level_CDN_2_host[level_CDN_2_host_id].redis_cache.higher_CDN_redis = self.build_network.level_data_center_host[bind_level_data_center_id].redis_cache
            self.build_network.level_CDN_2_host[level_CDN_2_host_id].redis_cache.higher_CDN_id = bind_level_data_center_id
            self.build_network.level_CDN_2_host[level_CDN_2_host_id].redis_cache.higher_CDN_level = 1
            self.build_network.level_CDN_2_host[level_CDN_2_host_id].redis_cache.higher_CDN_delay = self.topo["delay_topo"][self.topo["level_CDN_2_id"][level_data_center_host_id]][self.topo["level_data_center_id"][bind_level_data_center_id]]
            self.build_network.level_CDN_2_host[level_CDN_2_host_id].redis_cache.higher_CDN_bandwidth = self.topo["bandwidth_topo"][self.topo["level_CDN_2_id"][level_data_center_host_id]][self.topo["level_data_center_id"][bind_level_data_center_id]]

        self.find_success_number = [0, 0, 0, 0]
        self.find_fail_number = [0, 0, 0, 0]
        
        if self.use_http_server:
            time.sleep(5) ## 等待5秒，让HTTP server启动
            
    def ego_betweenness(self, G, node):
        """
        ego networks are networks consisting of a single actor (ego) together with the actors they are connected to (alters) and all the links among those alters.[1]
        Burt (1992), in his book Structural Holes, provides ample evidence that having high betweenness centrality, which is highly correlated with having many structural holes, can bring benefits to ego.[1]
        Returns the betweenness centrality of a ego network whose ego is set
        Parameters
        ----------
        G : graph
        node : int
        Returns
        -------
        sum : float
            the betweenness centrality of a ego network whose ego is set
        Examples
        --------
        Returns the betwenness centrality of node 1.
        >>> ego_betweenness(G,node=1)
        Reference
        ---------
        .. [1] Martin Everett, Stephen P. Borgatti. "Ego network betweenness." Social Networks, Volume 27, Issue 1, Pages 31-38, 2005.
        """
        g = G.ego_subgraph(node)
        n = len(g) + 1
        A = np.matlib.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if g.has_edge(str(i), str(j)):
                    A[i, j] = 1
        B = A * A
        C = 1 - A
        sum = 0
        flag = G.is_directed()
        for i in range(n):
            for j in range(n):
                if i != j and C[i, j] == 1 and B[i, j] != 0:
                    sum += 1.0 / B[i, j]
        if flag == False:
            sum /= 2
        return 2 * sum / ((n - 1) * (n - 2)) 

    def main(self, caching_policy):
        '''read_trace'''
        if caching_policy in ["LRU", "Second-Hit-LRU"]:
            self.reflush_cache(use_LRU_cache=True)
        elif caching_policy == "OPT":
            self.reflush_cache(use_LRU_cache=True, use_OPT=True) ## datacenter和L1 CDN Layer使用LRU，仅在L2 CDN Layer使用OPT。
        else:
            self.reflush_cache()
        
        if caching_policy in ["FIFO", "RAND", "OPT"]:
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
            
        elif caching_policy == 'HITS':
            curr_social_metric_path = self.social_metric_dict_path + 'HITS.pkl'
            if os.path.exists(curr_social_metric_path):
                hits_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                adj_matrix = util.generate_adj_matrix_graph("data/traces/" + self.trace_dir + "/relations.txt", len(self.G.nodes))
                networkx_graph = networkx.DiGraph(adj_matrix)
                hits_metrics = networkx.hits(networkx_graph, max_iter=500)[0]
                pickle.dump(hits_metrics, open(curr_social_metric_path, "wb"))
            # print("hits_metrics: ", hits_metrics)
            
        elif caching_policy == 'ClusteringCoefficient':
            curr_social_metric_path = self.social_metric_dict_path + 'ClusteringCoefficient.pkl'
            if os.path.exists(curr_social_metric_path):
                clustering_coefficient_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                adj_matrix = util.generate_adj_matrix_graph("data/traces/" + self.trace_dir + "/relations.txt", len(self.G.nodes))
                networkx_graph = networkx.DiGraph(adj_matrix)
                clustering_coefficient_metrics = networkx.clustering(networkx_graph)
                pickle.dump(clustering_coefficient_metrics, open(curr_social_metric_path, "wb"))
            # print("clustering_coefficient_metrics: ", clustering_coefficient_metrics)
            
        elif caching_policy == "Degree":
            '''To use it, remember the key is str type, and the value is bool'''
            degree_metrics = self.G.in_degree()
            # print("degree_metrics: ", degree_metrics)
        
        elif caching_policy == "DegreeCentrality":
            curr_social_metric_path = self.social_metric_dict_path + 'DegreeCentrality.pkl'
            if os.path.exists(curr_social_metric_path):
                degree_centrality_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                adj_matrix = util.generate_adj_matrix_graph("data/traces/" + self.trace_dir + "/relations.txt", len(self.G.nodes))
                networkx_graph = networkx.DiGraph(adj_matrix)
                degree_centrality_metrics = networkx.in_degree_centrality(networkx_graph)
                pickle.dump(degree_centrality_metrics, open(curr_social_metric_path, "wb"))
            # print("degree_centrality_metrics: ", degree_centrality_metrics)   
            
        elif caching_policy == "ClosenessCentrality":
            curr_social_metric_path = self.social_metric_dict_path + 'ClosenessCentrality.pkl'
            if os.path.exists(curr_social_metric_path):
                closeness_centrality_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                adj_matrix = util.generate_adj_matrix_graph("data/traces/" + self.trace_dir + "/relations.txt", len(self.G.nodes))
                networkx_graph = networkx.DiGraph(adj_matrix)
                closeness_centrality_metrics = networkx.closeness_centrality(networkx_graph)
                pickle.dump(closeness_centrality_metrics, open(curr_social_metric_path, "wb"))
            # print("closeness_centrality_metrics: ", closeness_centrality_metrics)

        elif caching_policy == "BetweennessCentrality":
            curr_social_metric_path = self.social_metric_dict_path + 'BetweennessCentrality.pkl'
            if os.path.exists(curr_social_metric_path):
                betweenness_centrality_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                betweenness_centrality_metrics = eg.functions.centrality.betweenness.betweenness_centrality(self.G)
                pickle.dump(betweenness_centrality_metrics, open(curr_social_metric_path, "wb"))
            # print("betweenness_centrality_metrics: ", betweenness_centrality_metrics)
        
        elif caching_policy == "EigenvectorCentrality":
            curr_social_metric_path = self.social_metric_dict_path + 'EigenvectorCentrality.pkl'
            if os.path.exists(curr_social_metric_path):
                eigenvector_centrality_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                adj_matrix = util.generate_adj_matrix_graph("data/traces/" + self.trace_dir + "/relations.txt", len(self.G.nodes))
                networkx_graph = networkx.DiGraph(adj_matrix)
                eigenvector_centrality_metrics = networkx.algorithms.centrality.eigenvector_centrality(networkx_graph, max_iter=500)
                pickle.dump(eigenvector_centrality_metrics, open(curr_social_metric_path, "wb"))
            # print("eigenvector_centrality_metrics: ", eigenvector_centrality_metrics)

        elif caching_policy == "LaplacianCentrality":
            curr_social_metric_path = self.social_metric_dict_path + 'LaplacianCentrality.pkl'
            if os.path.exists(curr_social_metric_path):
                laplacian_centrality_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                laplacian_centrality_metrics = eg.functions.not_sorted.laplacian(self.G)
                pickle.dump(laplacian_centrality_metrics, open(curr_social_metric_path, "wb"))
            # print("laplacian_centrality_metrics: ", laplacian_centrality_metrics)
            
        elif caching_policy == "EgoBetweennessCentrality":
            curr_social_metric_path = self.social_metric_dict_path + 'EgoBetweennessCentrality.pkl'
            if os.path.exists(curr_social_metric_path):
                ego_betweenness_centrality_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                ego_betweenness_centrality_metrics = {}
                for curr_node in self.G.nodes:
                    ego_betweenness_centrality_metrics[curr_node] = self.ego_betweenness(self.G, curr_node)
                pickle.dump(ego_betweenness_centrality_metrics, open(curr_social_metric_path, "wb"))
            # print("ego_betweenness_centrality_metrics: ", ego_betweenness_centrality_metrics)

        elif caching_policy == "LRU-Social":
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

                num_processes = multiprocessing.cpu_count()
                pool = multiprocessing.Pool(processes=num_processes)
                results = pool.starmap(calculate_spreading_power, [(i, networkx_graph, epidemic_threshold, CONFIG['cache_size_level_CDN_1']) for i in range(len(self.G.nodes))])
                pool.close()
                pool.join()

                spreading_power_list = [0] * len(self.G.nodes)
                for i, spreading_power in results:
                    spreading_power_list[i] = spreading_power
                    
                # for i in range(len(self.G.nodes)):
                #     spreading_number = SIR.SIR_network(networkx_graph, [i] , epidemic_threshold, 1, 1)
                #     spreading_power_list[i] = (spreading_number - 1) / CONFIG['cache_size_level_CDN_1'] + 1 # 如果没有传播，设置为1，即和LRU等同。
                #     if i % 1 == 0:
                #         print("calculated: ", i)
                pickle.dump(spreading_power_list, open(curr_social_metric_path, "wb"))
            # print("spreading_power_list: ", spreading_power_list)
            
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
            
        elif caching_policy == "Efficiency":
            curr_social_metric_path = self.social_metric_dict_path + 'Efficency.pkl'
            if os.path.exists(curr_social_metric_path):
                efficiency_metrics = pickle.load(open(curr_social_metric_path, "rb"))
            else:
                adj_matrix = util.generate_adj_matrix_graph("data/traces/" + self.trace_dir + "/relations.txt", len(self.G.nodes))
                networkx_graph = networkx.DiGraph(adj_matrix).reverse() ## 关注的方向，传播需要反向
                '''easygraph的constraint只能针对无向图，networkx的constraint可以针对有向图'''
                effective_size_metrics = networkx.effective_size(networkx_graph)
                efficiency_metrics = {n: v / networkx_graph.degree(n) for n, v in effective_size_metrics.items()}
                pickle.dump(efficiency_metrics, open(curr_social_metric_path, "wb"))
            # print("efficiency_metrics: ", efficiency_metrics)

        f_in = open("data/traces/" + self.trace_dir + "/all_timeline.txt", "r")
        f_out_find = open(self.result_path + 'find_log.txt', 'w')
        f_out_insert = open(self.result_path + 'insert_log.txt', 'w')
        f_out_time = open(self.result_path + 'time_log.txt', 'w')
        f_out_latency = open(self.result_path + 'latency_log.txt', 'w')
        start_time = time.time()
        print("start_time: %f"%(start_time), file=f_out_time)
        print("caching_policy: ", caching_policy)
        cnt_line = 0 
        print("cnt_line: ", cnt_line)
        last_timestamp = -1
        for line in f_in:
            cnt_line += 1
            if cnt_line % 100000 == 0:
                print("cnt_line: ", cnt_line)
            if CONFIG['max_trace_len'] and cnt_line > CONFIG['max_trace_len']:
               break 
            current_type = line.split('+')[-1].strip()
            current_location = eval(line.split('+')[2])
            current_timestamp = float(line.split('+')[0])
            if math.floor(current_timestamp) == math.floor(last_timestamp):
                current_timestamp = last_timestamp + 0.001
            last_timestamp = current_timestamp

            [selected_level_CDN_1_id, nearest_distance] = util.find_nearest_location(current_location, self.level_CDN_1_area_location)
            if int(nearest_distance) == 0:
                nearest_distance = 2
            else:
                nearest_distance = 1 / int(nearest_distance)

            if current_type == "post":
                post_id = int(line.split('+')[4])
                user_id = int(line.split('+')[3])
                media_size = float(line.split('+')[1])

                '''如果使用networkx，图中用户的编号是数字；如果使用easygraph，图中用户的编号是字符串，记得类型转换'''

                if caching_policy == 'RAND':
                    sort_value = random.randint(0, 1000)

                elif caching_policy in ['FIFO', 'LRU', 'Second-Hit-LRU', 'OPT']:
                    sort_value = current_timestamp

                elif caching_policy == 'PageRank':
                    sort_value = current_timestamp + \
                                nearest_distance * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                page_rank_metrics[str(user_id)] * CONFIG['params'][2]
                                
                elif caching_policy == 'HITS':
                    sort_value = current_timestamp + \
                                nearest_distance * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                hits_metrics[user_id] * CONFIG['params'][2]
                                
                elif caching_policy == 'ClusteringCoefficient':
                    sort_value = current_timestamp + \
                                nearest_distance * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                clustering_coefficient_metrics[user_id] * CONFIG['params'][2]

                elif caching_policy == "Degree":
                    sort_value = current_timestamp + \
                                nearest_distance * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                degree_metrics[str(user_id)] * CONFIG['params'][2]
                
                elif caching_policy == "DegreeCentrality":
                    sort_value = current_timestamp + \
                                nearest_distance * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                degree_centrality_metrics[user_id] * CONFIG['params'][2]
                                
                elif caching_policy == "ClosenessCentrality":
                    sort_value = current_timestamp + \
                                nearest_distance * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                closeness_centrality_metrics[user_id] * CONFIG['params'][2]

                elif caching_policy == "BetweennessCentrality":
                    sort_value = current_timestamp + \
                                nearest_distance * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                betweenness_centrality_metrics[str(user_id)] * CONFIG['params'][2]
                                
                elif caching_policy == "EigenvectorCentrality":
                    sort_value = current_timestamp + \
                                nearest_distance * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                eigenvector_centrality_metrics[user_id] * CONFIG['params'][2]
                    
                elif caching_policy == "LaplacianCentrality":
                    sort_value = current_timestamp + \
                                nearest_distance * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                laplacian_centrality_metrics[str(user_id)] * CONFIG['params'][2]
                            
                elif caching_policy == "LRU-Social" or caching_policy == "LRU-label":
                    '''LRU-Social and LRU-label can adjust the sort_value automatically'''
                    sort_value = 0
                    
                elif caching_policy == "EgoBetweennessCentrality":
                    sort_value = current_timestamp + \
                                nearest_distance * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                ego_betweenness_centrality_metrics[str(user_id)] * CONFIG['params'][2]          

                elif caching_policy == "EffectiveSize":
                    if math.isnan(effective_size_metrics[user_id]):
                        effective_size_metrics[user_id] = 0
                    # print(current_timestamp, nearest_distance, media_size, effective_size_metrics[user_id])
                    sort_value = current_timestamp + \
                                nearest_distance * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                effective_size_metrics[user_id] * CONFIG['params'][2]
                                
                elif caching_policy == "Efficiency":
                    if math.isnan(efficiency_metrics[user_id]):
                        efficiency_metrics[user_id] = 0
                    # print(current_timestamp, nearest_distance, media_size, efficiency_metrics[user_id])
                    sort_value = current_timestamp + \
                                nearest_distance * CONFIG['params'][0] + \
                                media_size * CONFIG['params'][1] + \
                                efficiency_metrics[user_id] * CONFIG['params'][2]

                '''记录redis_object，使用json形式保存'''
                temp_redis_object = {
                    'sort_value': sort_value,
                    'media_size': media_size,
                    'timestamp': current_timestamp
                }

                print(cnt_line, selected_level_CDN_1_id, temp_redis_object, file=f_out_insert)

                if self.if_debug:
                    print("post_id: ", post_id)
                    print("user_id: ", user_id)
                    print("selected_level_CDN_1_id: ", selected_level_CDN_1_id)
                    print("temp_redis_object: ", temp_redis_object)
                
                '''往第三层级插入，后续的调整都由SocialCDN内部完成'''
                if caching_policy == "LRU-Social":
                    self.build_network.level_CDN_1_host[selected_level_CDN_1_id].redis_cache.insert(picture_hash=post_id, redis_object=temp_redis_object, need_uplift=True, use_LRU_social=True, first_insert=True, lru_social_parameter_sp=spreading_power_list[user_id])
                elif caching_policy == "LRU-label":
                    self.build_network.level_CDN_1_host[selected_level_CDN_1_id].redis_cache.insert(picture_hash=post_id, redis_object=temp_redis_object, need_uplift=True, use_LRU_label=True)
                elif caching_policy == "Second-Hit-LRU":
                    self.build_network.level_CDN_1_host[selected_level_CDN_1_id].redis_cache.insert(picture_hash=post_id, redis_object=temp_redis_object, need_uplift=True, ignore_cache=True)
                elif caching_policy == "OPT":
                    self.build_network.level_CDN_1_host[selected_level_CDN_1_id].redis_cache.insert(picture_hash=post_id, redis_object=temp_redis_object, need_uplift=True, use_OPT=True)
                else:
                    self.build_network.level_CDN_1_host[selected_level_CDN_1_id].redis_cache.insert(picture_hash=post_id, redis_object=temp_redis_object, need_uplift=True)

            elif current_type == "view":
                post_id = int(line.split('+')[1])
                # curr_view_start_time = time.time()
                # user_id = int(line.split('+')[3])
                
                # if post_id == 13 and current_timestamp < 250000:
                #     print(selected_level_CDN_1_id, current_timestamp, "!!!!!!")
                '''往第三层级查询，后续的调整都由redis内部完成，这里先假设只有一个user节点'''
                if caching_policy == "LRU-Social":
                    find_result = self.build_network.level_CDN_1_host[selected_level_CDN_1_id].redis_cache.find(picture_hash=post_id, user_host=self.build_network.user_host[0], current_timestamp=current_timestamp, need_update_cache=need_update_cache, use_LRU_social=True, request_delay=util.distance_to_delay(1/nearest_distance), request_bandwidth=util.distance_to_bandwidth(1/nearest_distance))
                    
                elif caching_policy == "LRU-label":
                    find_result = self.build_network.level_CDN_1_host[selected_level_CDN_1_id].redis_cache.find(picture_hash=post_id, user_host=self.build_network.user_host[0], current_timestamp=current_timestamp, need_update_cache=need_update_cache, use_LRU_label=True, request_delay=util.distance_to_delay(1/nearest_distance), request_bandwidth=util.distance_to_bandwidth(1/nearest_distance))
                    
                elif caching_policy == "Second-Hit-LRU":
                    find_result = self.build_network.level_CDN_1_host[selected_level_CDN_1_id].redis_cache.find(picture_hash=post_id, user_host=self.build_network.user_host[0], current_timestamp=current_timestamp, need_update_cache=need_update_cache, ignore_cache=True, request_delay=util.distance_to_delay(1/nearest_distance), request_bandwidth=util.distance_to_bandwidth(1/nearest_distance))
                    
                elif caching_policy == "OPT":
                    find_result = self.build_network.level_CDN_1_host[selected_level_CDN_1_id].redis_cache.find(picture_hash=post_id, user_host=self.build_network.user_host[0], current_timestamp=current_timestamp, need_update_cache=need_update_cache, request_delay=util.distance_to_delay(1/nearest_distance), request_bandwidth=util.distance_to_bandwidth(1/nearest_distance), use_OPT=True)
                    
                else:
                    find_result = self.build_network.level_CDN_1_host[selected_level_CDN_1_id].redis_cache.find(picture_hash=post_id, user_host=self.build_network.user_host[0], current_timestamp=current_timestamp, need_update_cache=need_update_cache, request_delay=util.distance_to_delay(1/nearest_distance), request_bandwidth=util.distance_to_bandwidth(1/nearest_distance))
                    
                result_level = find_result[0]
                
                if self.if_debug:
                    print(result_level)

                if result_level == 0:
                    '''所有level的cache都没有找到'''
                    print("!!!! ", cnt_line)
                    continue
                
                # curr_view_end_time = time.time()

                print(cnt_line, selected_level_CDN_1_id, result_level, find_result[1], file=f_out_find)
                print(cnt_line, find_result[2], file=f_out_latency)
                
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
        f_out_latency.close()

        if self.use_http_server == True:
            for level_CDN_1_host_id in range(self.build_network.level_CDN_1_host_number):
                for eth_port in range(self.build_network.level_CDN_2_host_number): # 对应第二层的每一个节点
                    util.calculate_flow(host=self.build_network.level_CDN_1_host[level_CDN_1_host_id], eth_name='c%s-eth%s'%(str(level_CDN_1_host_id), str(eth_port)), flow_direction='TX', result_path=self.result_path+'flow/'+self.build_network.level_CDN_1_host_ip[level_CDN_1_host_id])

            for level_CDN_2_host_id in range(self.build_network.level_CDN_2_host_number):
                for eth_port in range(self.build_network.level_data_center_host_number): # 对应第一层的每一个节点，以及自己的switch
                    util.calculate_flow(host=self.build_network.level_CDN_2_host[level_CDN_2_host_id], eth_name='b%s-eth%s'%(str(level_CDN_2_host_id), str(eth_port)), flow_direction='TX', result_path=self.result_path+'flow/'+self.build_network.level_CDN_2_host_ip[level_CDN_2_host_id])

            for level_data_center_host_id in range(self.build_network.level_data_center_host_number):
                for eth_port in range(1): # 对应自己的switch
                    util.calculate_flow(host=self.build_network.level_data_center_host[level_data_center_host_id], eth_name='a%s-eth%s'%(str(level_data_center_host_id), str(eth_port)), flow_direction='TX', result_path=self.result_path+'flow/'+self.build_network.level_data_center_host_ip[level_data_center_host_id])


    def run(self, caching_policy):
        self.main(caching_policy=caching_policy)

if __name__ == '__main__':
    CONFIG = json.load(open('./code/main/config.json', 'r'))
    main_program = Main(trace_dir=CONFIG['trace_dir'], use_http_server=CONFIG['use_http_server'], if_debug=CONFIG['mode']=='debug')
    main_program.run(caching_policy=CONFIG['caching_policy'])
