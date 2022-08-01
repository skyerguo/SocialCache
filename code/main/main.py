from code.build.build_main import Build_network
from code.trace.make_trace import Make_trace
from code.cache.redis_cache.redis_cache import Redis_cache
import easygraph as eg
import code.util.util as util
from mininet.cli import CLI
import json
import os
import time
import random

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
        self.make_trace = Make_trace(self.trace_dir)
        self.make_trace.run()

        self.use_http_server = use_http_server
        

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
        
        time.sleep(5) ## 等待5秒，让HTTP server启动


    def main(self, caching_policy):
        '''read_trace'''
        if caching_policy == "LRU":
            self.reflush_cache(use_LRU_cache=True)
        else:
            self.reflush_cache(use_LRU_cache=False)
        
        if caching_policy == 'PageRank':
            page_rank_metrics = eg.functions.not_sorted.pagerank(self.make_trace.G)

        f_in = open("data/traces/" + self.trace_dir + "/all_timeline.txt", "r")
        f_out = open(self.result_path + 'find_result.txt', 'w')
        cnt_line = 0 
        for line in f_in:
            cnt_line += 1
            if CONFIG['max_trace_len'] and cnt_line > CONFIG['max_trace_len']:
               break 
            current_type = line.split('+')[-1].strip()
            current_location = eval(line.split('+')[2])
            current_timestamp = int(line.split('+')[0])

            selected_level_3_id = util.find_nearest_location(current_location, self.level_3_area_location)

            if current_type == "post":
                post_id = int(line.split('+')[4])
                user_id = int(line.split('+')[3])

                if caching_policy == 'RAND':
                    sort_value = random.randint()
                elif caching_policy == 'FIFO' or caching_policy == 'LRU':
                    sort_value = int(current_timestamp)
                elif caching_policy == 'PageRank':
                    sort_value = page_rank_metrics[str(user_id)]
                    
                '''记录redis_object，使用json形式保存'''
                temp_redis_object = {
                    'sort_value': sort_value,
                    'media_size': int(float(line.split('+')[1]))
                }

                if self.if_debug:
                    print("post_id: ", post_id)
                    print("user_id: ", user_id)
                    print("selected_level_3_id: ", selected_level_3_id)
                    print("temp_redis_object: ", temp_redis_object)
                
                '''往第三层级插入，后续的调整都由redis内部完成'''
                self.build_network.level_3_host[selected_level_3_id].redis_cache.insert(picture_hash=post_id, redis_object=temp_redis_object, need_uplift=True)

            elif current_type == "view":
                post_id = int(line.split('+')[1])
                '''往第三层级查询，后续的调整都由redis内部完成，这里先假设只有一个user'''
                find_result = self.build_network.level_3_host[selected_level_3_id].redis_cache.find(picture_hash=post_id, user_host=self.build_network.user_host[0])
                result_level = find_result[0]

                if result_level == 0:
                    '''所有level的cache都没有找到'''
                    continue

                print(cnt_line, result_level, file=f_out)
                
                for temp_level in range(3, result_level, -1):
                    self.find_fail_number[temp_level] += 1
                self.find_success_number[result_level] += 1
            else:
                print("ERROR!")
        f_in.close()

        # CLI(self.build_network.net)

        if self.use_http_server == True:
            for level_3_host_id in range(self.build_network.level_3_host_number):
                for eth_port in range(self.build_network.level_2_host_number):
                    util.calculate_flow(host=self.build_network.level_3_host[level_3_host_id], eth_name='c%s-eth%s'%(str(level_3_host_id), str(eth_port)), flow_direction='TX', result_path=self.result_path+'flow/'+self.build_network.level_3_host_ip[level_3_host_id])

        '''分析'''
        print('缓存策略： *** %s ***'%(caching_policy))
        if self.find_success_number[3] + self.find_fail_number[3] > 0:
            print('三级CDN缓存命中率：', self.find_success_number[3] / (self.find_success_number[3] + self.find_fail_number[3]))
        else:
            print('未经过三级CDN缓存')

        if self.find_success_number[2] + self.find_fail_number[2] > 0:
            print('二级CDN缓存命中率：', self.find_success_number[2] / (self.find_success_number[2] + self.find_fail_number[2]))
        else:
            print('未经过二级CDN缓存')
            
        if self.find_success_number[1] + self.find_fail_number[1] > 0:
            print('一级CDN缓存命中率：', self.find_success_number[1] / (self.find_success_number[1] + self.find_fail_number[1]))
        else:
            print('未经过一级CDN缓存')

    def run(self, caching_policy):
        self.main(caching_policy=caching_policy)

if __name__ == '__main__':
    CONFIG = json.load(open('./code/main/config.json', 'r'))
    main_program = Main(trace_dir=CONFIG['trace_dir'], use_http_server=CONFIG['use_http_server'], if_debug=CONFIG['mode']=='debug')
    main_program.run(caching_policy=CONFIG['caching_policy'])
