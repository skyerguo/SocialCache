from code.build.build_main import Build_network
from code.trace.make_trace import Make_trace
from code.cache.redis_cache.redis_cache import Redis_cache
import easygraph as eg
import code.util.util as util
from mininet.cli import CLI
import json
import os

class Main:
    def __init__(self, trace_dir, use_http_server=False):

        self.build_network = Build_network()
        self.build_network.run()

        self.topo = json.load(open('code/build/topo.json', 'r'))
        level_3_area_id = self.topo['level_3_id']
        self.level_3_area_location = []
        for area_id in level_3_area_id:
            self.level_3_area_location.append(self.topo["areaid2position"][str(area_id)])

        self.trace_dir = trace_dir
        self.make_trace = Make_trace(self.trace_dir)
        self.make_trace.run()

        self.use_http_server = use_http_server

        # self.find_success_number = [0, 0, 0, 0]
        # self.find_fail_number = [0, 0, 0, 0]

    def start_http_server(self, host, db, host_ip, temp_save_data_path):
        '''在每个节点启动HTTP server'''
        util.reflush_path(temp_save_data_path)
        host.cmdPrint('cd %s && nohup python3 /users/gtc/SocNet/code/util/simple_httpserver.py -l %s -p %s -n 1>> log1.txt 2>> log2.txt &'%(temp_save_data_path, str(host_ip), str(4433+int(db))))
        

    def reflush_cache(self, use_LRU_cache=False):
        os.system("ps -ef |grep simple_httpserver.py | grep -v grep | awk '{print $2}' | xargs sudo kill -9 > /dev/null 2>&1 && sleep 3")
        host_all = []
        for level_1_host_id in range(self.build_network.level_1_host_number):
            self.build_network.level_1_host[level_1_host_id].redis_cache = Redis_cache(db=len(host_all), cache_size=1000, use_LRU_cache=use_LRU_cache)
            if self.use_http_server:
                self.build_network.level_1_host[level_1_host_id].redis_cache.data_path = '/proj/socnet-PG0/temp_media_data/' + str(len(host_all)) + '/save/'
                self.start_http_server(host=self.build_network.level_1_host[level_1_host_id], db=len(host_all), host_ip=self.build_network.level_1_host_ip[level_1_host_id], temp_save_data_path=self.build_network.level_1_host[level_1_host_id].redis_cache.data_path)
            host_all.append(self.build_network.level_1_host[level_1_host_id])

        for level_2_host_id in range(self.build_network.level_2_host_number):
            self.build_network.level_2_host[level_2_host_id].redis_cache = Redis_cache(db=len(host_all), cache_size=100, use_LRU_cache=use_LRU_cache)
            if self.use_http_server:
                self.build_network.level_2_host[level_2_host_id].redis_cache.data_path = '/proj/socnet-PG0/temp_media_data/' + str(len(host_all)) + '/save/'
                self.start_http_server(host=self.build_network.level_2_host[level_2_host_id], db=len(host_all), host_ip=self.build_network.level_2_host_ip[level_2_host_id], temp_save_data_path=self.build_network.level_2_host[level_2_host_id].redis_cache.data_path)
            host_all.append(self.build_network.level_2_host[level_2_host_id])

        for level_3_host_id in range(self.build_network.level_3_host_number):
            self.build_network.level_3_host[level_3_host_id].redis_cache = Redis_cache(db=len(host_all), cache_size=10, use_LRU_cache=use_LRU_cache)
            if self.use_http_server:
                self.build_network.level_3_host[level_3_host_id].redis_cache.data_path = '/proj/socnet-PG0/temp_media_data/' + str(len(host_all)) + '/save/'
                self.start_http_server(host=self.build_network.level_3_host[level_3_host_id], db=len(host_all), host_ip=self.build_network.level_3_host_ip[level_3_host_id], temp_save_data_path=self.build_network.level_3_host[level_3_host_id].redis_cache.data_path)
            host_all.append(self.build_network.level_3_host[level_3_host_id])

        self.find_success_number = [0, 0, 0, 0]
        self.find_fail_number = [0, 0, 0, 0]

    def Classical(self, specific_type):
        '''read_trace'''
        if specific_type == "LRU":
            self.reflush_cache(use_LRU_cache=True)
        else:
            self.reflush_cache()

        f_in = open("data/traces/" + self.trace_dir + "/all_timeline.txt", "r")
        for line in f_in:
            current_type = line.split('+')[-1].strip()
            current_location = eval(line.split('+')[2])
            current_timestamp = int(line.split('+')[0])
            
            selected_level_3_id = util.find_nearest_location(current_location, self.level_3_area_location)
            bind_level_2_id = self.topo['up_bind_3_2'][selected_level_3_id]
            bind_level_1_id = self.topo['up_bind_2_1'][bind_level_2_id]

            if current_type == "post":
                post_id = int(line.split('+')[4])
                media_size = int(float(line.split('+')[1]) * 1000)
                self.build_network.level_3_host[selected_level_3_id].redis_cache.insert(post_id, current_timestamp, media_size=media_size)
                # self.build_network.level_2_host[bind_level_2_id].redis_cache.insert(post_id, current_timestamp)
                # self.build_network.level_1_host[bind_level_1_id].redis_cache.insert(post_id, current_timestamp)

            elif current_type == "view":
                post_id = int(line.split('+')[1])
                if self.build_network.level_3_host[selected_level_3_id].redis_cache.find(post_id) == -1:
                    self.find_fail_number[3] += 1
                    if self.build_network.level_2_host[bind_level_2_id].redis_cache.find(post_id) == -1:
                        self.find_fail_number[2] += 1
                        if self.build_network.level_1_host[bind_level_1_id].redis_cache.find(post_id) == -1:
                            self.find_fail_number[1] += 1
                        else:
                            self.find_success_number[1] += 1
                    else:
                        self.find_success_number[2] += 1
                else:
                    self.find_success_number[3] += 1
            else:
                print("ERROR!")
        f_in.close()

        '''分析'''
        print("缓存策略： *** %s ***"%(specific_type))
        print("三级CDN缓存命中率：", self.find_success_number[3] / (self.find_success_number[3] + self.find_fail_number[3]))
        print("二级CDN缓存命中率：", self.find_success_number[2] / (self.find_success_number[2] + self.find_fail_number[2]))
        print("一级CDN缓存命中率：", self.find_success_number[1] / (self.find_success_number[1] + self.find_fail_number[1]))
        # print("二级缓存命中数和失效数：", self.find_success_number[2], self.find_fail_number[2])

    def PageRank(self):
        self.reflush_cache()
        '''计算PageRank'''
        page_rank_metrics = eg.functions.not_sorted.pagerank(self.make_trace.G)

        '''read_trace'''
        f_in = open("data/traces/" + self.trace_dir + "/all_timeline.txt", "r")
        for line in f_in:
            current_type = line.split('+')[-1].strip()
            current_location = eval(line.split('+')[2])
            current_timestamp = int(line.split('+')[0])
            
            selected_level_3_id = util.find_nearest_location(current_location, self.level_3_area_location)
            bind_level_2_id = self.topo['up_bind_3_2'][selected_level_3_id]
            bind_level_1_id = self.topo['up_bind_2_1'][bind_level_2_id]

            if current_type == "post":
                post_id = int(line.split('+')[4])
                user_id = int(line.split('+')[3])
                self.build_network.level_3_host[selected_level_3_id].redis_cache.insert(post_id, int(page_rank_metrics[str(user_id)] * 10000) + current_timestamp)
                self.build_network.level_2_host[bind_level_2_id].redis_cache.insert(post_id, int(page_rank_metrics[str(user_id)] * 10000) + current_timestamp)
                self.build_network.level_1_host[bind_level_1_id].redis_cache.insert(post_id, int(page_rank_metrics[str(user_id)] * 10000) + current_timestamp)

            elif current_type == "view":
                post_id = int(line.split('+')[1])
                if self.build_network.level_3_host[selected_level_3_id].redis_cache.find(post_id) == -1:
                    self.find_fail_number[3] += 1
                    if self.build_network.level_2_host[bind_level_2_id].redis_cache.find(post_id) == -1:
                        self.find_fail_number[2] += 1
                        if self.build_network.level_1_host[bind_level_1_id].redis_cache.find(post_id) == -1:
                            self.find_fail_number[1] += 1
                        else:
                            self.find_success_number[1] += 1
                    else:
                        self.find_success_number[2] += 1
                else:
                    self.find_success_number[3] += 1
            else:
                print("ERROR!")
        f_in.close()

        '''分析'''
        print("缓存策略： *** PageRank ***")
        print("三级CDN缓存命中率：", self.find_success_number[3] / (self.find_success_number[3] + self.find_fail_number[3]))
        print("二级CDN缓存命中率：", self.find_success_number[2] / (self.find_success_number[2] + self.find_fail_number[2]))
        print("一级CDN缓存命中率：", self.find_success_number[1] / (self.find_success_number[1] + self.find_fail_number[1]))

    def run(self, caching_policy):
        if caching_policy == 'FIFO':
            self.Classical(specific_type="FIFO")
        elif caching_policy == "LRU":
            self.Classical(specific_type="LRU")
        elif caching_policy == 'PageRank':
            self.PageRank()

if __name__ == '__main__':
    main_program = Main(trace_dir='naive', use_http_server=True)
    main_program.run('FIFO')
    # main_program.run('LRU')
    # main_program.run('PageRank')