import logging
import json
import queue
import subprocess
from collections import OrderedDict, defaultdict
import os
import code.util.util as util
from code.trace.opt_eviction import Opt_eviction
import copy

class Redis_cache:
    def __init__(self, db, host, cache_size=5, use_priority_queue=True, use_LRU_cache=False, result_path='~/', host_ip='', host_port='', cache_level=0, use_OPT=False, trace_dir='', cache_id='', level_3_area_location=''):
        """初始化

        Args:
            db (int): 数据库表单
            use_priority_queue (bool, optional): 是否使用优先队列维护权值最小的点. Defaults to True.
        """
        logging.info("initing redis cache...")

        self.cache_size = int(cache_size)

        '''连接池'''
        self.redis_fake = {}

        '''设置优先队列'''
        self.use_priority_queue = use_priority_queue
        # if self.cache_size == 1000000 or self.cache_size == 15:
            # self.use_priority_queue = False
        if self.use_priority_queue:
            self.priority_queue = queue.PriorityQueue()

        '''设置LRU的字典'''
        self.use_LRU_cache = use_LRU_cache
        if self.use_LRU_cache:
            self.LRUcache = OrderedDict() # 用有序字典来实现LRU

        '''设置实际数据文件存储路径'''
        self.picture_root_path = '/dev/null'

        '''设置当前层的redis_cache'''
        self.cache_level = cache_level
        self.cache_id = int(cache_id)
        self.lru_social_parameter_s = 0
        
        '''设置节点层级之间的关系'''
        self.higher_CDN_delay = 0
        self.higher_CDN_bandwidth = 0

        '''设置当前cache对应的mininet_host'''
        self.host = host
        
        '''设置当前cache的IP地址和HTTP端口'''
        self.host_ip = host_ip
        self.host_port = host_port

        self.hash_table = {}
        
        '''如果是最底层的CDN，设置second-hit的hash表'''
        if self.cache_level == 3:
            self.second_view_hash = []
        
        '''如果是最底层的CDN，且使用了OPT，记录opt表格'''
        if use_OPT and self.cache_level == 3:    
            self.opt = Opt_eviction("data/traces/" + trace_dir + '/', level_3_area_location, self.cache_id)
            # self.picture_hash_list = []

        '''设置结果存的根目录'''
        self.result_path = result_path
        os.system('mkdir -p ' + self.result_path + 'mediaSize/' + self.host_ip)
        self.file_insert_media_size = open(self.result_path + 'mediaSize/' + self.host_ip + '/insert_all.txt', 'a')
        self.file_receive_media_size = open(self.result_path + 'mediaSize/' + self.host_ip + '/receive_all.txt', 'a')

    def remove_cache_node(self, given_key='', use_LRU_social=False):
        '''删掉权值最小的cache数据'''

        '''如果有指定的key，直接删除'''
        if given_key != '':
            remove_key = given_key
        else:
            '''否则寻找权值最小的key'''
            if self.use_priority_queue:
                '''在优先队列中找到值最小的元素删除，同时要保证这个元素是有效的'''
                a = self.priority_queue.get() ## 取出并在priority_queue中去掉该元素
                remove_key = a[1]
                
                while not self.priority_queue.empty() and (not remove_key in self.redis_fake.keys() or self.hash_table[remove_key] != a[0]):
                    a = self.priority_queue.get() ## 取出并在priority_queue中去掉该元素
                    remove_key = a[1]
            else:
                min_value = 1e18
                remove_key = -1
                for curr_key in self.redis_fake.keys():
                    curr_value = self.redis_fake[curr_key]['sort_value']
                    if curr_value < min_value:
                        min_value = curr_value
                        remove_key = curr_key
        if remove_key == -1:
            print("Error Delete")
            exit(0)
        if use_LRU_social:
            min_value = self.redis_fake[remove_key]['sort_value']
            if min_value > self.cache_size:
                self.lru_social_parameter_s -= 1
        del self.redis_fake[remove_key]

        if self.picture_root_path != '/dev/null': ## 启用HTTP了
            util.delete_picture(host=self.host, picture_path=self.picture_root_path+str(remove_key)) #在硬盘中删除当前文件，保证硬盘不会存太多垃圾文件

    def get_lru_social_parameter_s(self) -> int:
        res = 0
        for curr_key in self.redis_fake.keys():
            curr_value = self.redis_fake[curr_key]['sort_value']
            if curr_value > self.cache_size:
                res += 1
        return res

    def decrement_lru_label(self, lowerest_threshold=0, use_LRU_social=False):
        # print("self.cache_level: ", self.cache_level)
        # print(self.redis_fake)
        # print(lowerest_threshold)
        
        for curr_key in self.redis_fake.keys():
            if self.redis_fake[curr_key]['sort_value'] > lowerest_threshold:
                self.redis_fake[curr_key]['sort_value'] -= 1
                if use_LRU_social:
                    if self.redis_fake[curr_key]['sort_value'] == self.cache_size: ## 原来大于C，更新S
                        self.lru_social_parameter_s -= 1
        # print(self.redis_fake)
        # print("-------")

    def modify_cache_node(self, picture_hash, redis_object, use_LRU_label, use_LRU_social, use_OPT):
        '''修改cache里面的节点，一般为插入或者调整'''

        whether_insert_flag = True
        if use_OPT and self.cache_level == 3: 
            if len(self.redis_fake.keys()) >= self.cache_size and picture_hash not in self.redis_fake.keys(): ## 如果缓存已满，替换最后被访问的那个文件
                latest_next = self.opt.request_latest(self.redis_fake.keys(), redis_object['timestamp'])
                now_next = self.opt.request_latest([picture_hash], redis_object['timestamp'])
                if now_next[1] < latest_next[1]:
                    self.redis_fake.pop(latest_next[0])
                else:
                    # print(self.redis_fake, redis_object['timestamp'], self.cache_id)
                    # print(latest_next)
                    # print(picture_hash, now_next)
                    # exit(0)
                    whether_insert_flag = False
                
        elif self.use_LRU_cache: 
            '''如果是LRU，特殊处理'''
            if picture_hash in self.LRUcache:
                '''若数据已存在，表示命中一次，需要把数据移到缓存队列末端'''
                self.LRUcache.move_to_end(picture_hash)
            elif len(self.redis_fake) >= self.cache_size:
                '''若缓存已满，则需要淘汰最早没有使用的数据'''
                self.remove_cache_node(given_key=next(iter(self.LRUcache)))
                self.LRUcache.popitem(last=False)
            self.LRUcache[picture_hash] = redis_object['sort_value']

        elif use_LRU_label:
            if picture_hash in self.redis_fake.keys(): 
                '''Cache Hit'''
                self.decrement_lru_label(lowerest_threshold=self.redis_fake[picture_hash]['sort_value'])
            else:
                if len(self.redis_fake) >= self.cache_size:
                    '''Cache Miss and Cahce is Full'''
                    self.remove_cache_node()
                '''Cache Miss'''
                self.decrement_lru_label(lowerest_threshold=0)

        elif use_LRU_social:
            if picture_hash in self.redis_fake.keys(): 
                '''Cache Hit'''
                if self.redis_fake[picture_hash]['sort_value'] > self.cache_size:
                    self.decrement_lru_label(lowerest_threshold=self.cache_size, use_LRU_social=True)
                else:
                    self.decrement_lru_label(lowerest_threshold=self.redis_fake[picture_hash]['sort_value'], use_LRU_social=True)
                    redis_object['sort_value'] = self.cache_size - self.lru_social_parameter_s
                    self.redis_fake[picture_hash] = redis_object
            else:
                if len(self.redis_fake) >= self.cache_size:
                    '''Cache Miss and Cahce is Full'''
                    self.remove_cache_node(given_key='', use_LRU_social=True)
                '''Cache Miss'''
                self.decrement_lru_label(lowerest_threshold=0, use_LRU_social=True)
                self.redis_fake[picture_hash] = redis_object
                if redis_object['sort_value'] > self.cache_size:
                    self.lru_social_parameter_s += 1
                    
        else:
            '''如果当前cache的空间使用完了，且不是LRU，则按照内在的权值替换'''
            if len(self.redis_fake) >= self.cache_size:
                if picture_hash not in self.redis_fake.keys() and len(self.redis_fake) == self.cache_size:
                    self.remove_cache_node()
        
        '''插入redis数据库, LRU_social单独处理'''
        if use_LRU_social == False and whether_insert_flag == True:
            self.redis_fake[picture_hash] = redis_object

        '''留个检测，以防出现bug'''
        if len(self.redis_fake) > self.cache_size:
            print("Error to check!!!", picture_hash, self.redis_fake[picture_hash])
            exit(0)

        '''如有有使用优先队列，每次插入时需要维护优先队列。使用第一关键字为sort_value，第二关键字为timestamp。保证timestamp互不相同，从而保证了key的唯一'''
        if self.use_priority_queue:
            self.hash_table[picture_hash] = (redis_object['sort_value'], redis_object['timestamp'])
            self.priority_queue.put(((redis_object['sort_value'], redis_object['timestamp']), picture_hash))  

    def insert(self, picture_hash, redis_object, need_uplift=True, use_LRU_label=False, use_LRU_social=False, first_insert=False, lru_social_parameter_sp=0, ignore_cache=False, use_OPT=False):
        '''
            need_uplift: True表示向上传播，False表示向下传播
        '''

        print(redis_object['media_size'], file=self.file_receive_media_size)
        
        if use_LRU_label:
            redis_object['sort_value'] = self.cache_size

        elif use_LRU_social:       
            # if self.lru_social_parameter_s != self.get_lru_social_parameter_s():
            #     print("!!!!!!!", self.lru_social_parameter_s, self.get_lru_social_parameter_s(), self.cache_size)
            #     print(self.redis_fake)
            #     exit(0)
            if first_insert:
                '''set the sort_value as SPu * C'''
                redis_object['sort_value'] = lru_social_parameter_sp * self.cache_size
                # redis_object['sort_value'] = ((lru_social_parameter_sp - 1) / self.cache_size + 1) * self.cache_size
                # print(lru_social_parameter_sp, self.cache_size, redis_object['sort_value'])
            else:
                '''set label as C-S'''
                redis_object['sort_value'] = self.cache_size - self.lru_social_parameter_s
                
        # print("post!!!", self.host_ip, picture_hash, self.cache_level, redis_object)
        # print(self.redis_fake)
        '''如果是second-hit，只有data center才将插入的内容放入缓存'''
        if (ignore_cache == False or (ignore_cache == True and self.cache_level == 1)):
            self.modify_cache_node(picture_hash=picture_hash, redis_object=copy.deepcopy(redis_object), use_LRU_label=use_LRU_label, use_LRU_social=use_LRU_social, use_OPT=use_OPT)
        # print(self.redis_fake)
        # print("---------")

        if need_uplift:
            '''需要逐层递归向上传播'''
            if self.picture_root_path != '/dev/null': 
                '''使用HTTP，相关的数据传输和存储'''
                if self.cache_level == 3: 
                    '''如果需要创建图片，则在最后一层路径中创建一个文件'''
                    util.create_picture(host=self.host, picture_size=redis_object['media_size'], picture_path=self.picture_root_path+str(picture_hash))

                if self.cache_level > 1:
                    '''如果有上层cache的需要，使用HTTP_POST向上传播'''
                    util.HTTP_POST(host=self.host, picture_path=self.picture_root_path+str(picture_hash), IP_address=self.higher_CDN_redis.host_ip, port_number=self.higher_CDN_redis.host_port, use_TLS=False, result_path=self.result_path+'curl/'+self.host_ip)

            if self.cache_level > 1:
                '''递归调用，一层层上传'''
                print(redis_object['media_size'], file=self.file_insert_media_size)
                self.higher_CDN_redis.insert(picture_hash=picture_hash, redis_object=copy.deepcopy(redis_object), need_uplift=need_uplift, use_LRU_label=use_LRU_label, use_LRU_social=use_LRU_social, first_insert=first_insert, lru_social_parameter_sp=lru_social_parameter_sp) 
                # print("???", self.redis_fake)

        elif self.cache_level > 1: 
            '''如果不是第一层，需要从上层获取数据传播'''
            if self.picture_root_path != '/dev/null': 
                '''从该节点对上一层进行HTTP_GET操作。这里保证上层有需要的数据'''
                util.HTTP_GET(host=self.host, picture_hash=picture_hash, IP_address=self.higher_CDN_redis.host_ip, port_number=self.higher_CDN_redis.host_port, use_TLS=False, result_path=self.higher_CDN_redis.result_path+'wget/'+self.host_ip, picture_path=self.picture_root_path+str(picture_hash))
            print(redis_object['media_size'], file=self.higher_CDN_redis.file_insert_media_size)

    def find(self, picture_hash, user_host, current_timestamp, need_update_cache=False, config_timestamp=1, use_LRU_label=False, use_LRU_social=False, ignore_cache=False, request_delay=0, request_bandwidth=0, use_OPT=False):
        if picture_hash in self.redis_fake.keys(): 
            '''如果找到了'''
            redis_object = copy.deepcopy(self.redis_fake[picture_hash])
            result_level = self.cache_level
            new_redis_object = copy.deepcopy(redis_object)

            '''查询需要更新cache'''
            if need_update_cache:
                if use_LRU_label:
                    new_redis_object['sort_value'] = self.cache_size 

                elif use_LRU_social:
                    new_redis_object['sort_value'] = 0 ## 会在modify_cache_node自动处理
                    
                else:
                    last_timestamp = redis_object['timestamp']
                    new_sort_value = redis_object['sort_value'] + (current_timestamp - last_timestamp) * config_timestamp
                    new_redis_object['timestamp'] = current_timestamp
                    new_redis_object['sort_value'] = new_sort_value
                
                # print("view hit!!!", self.host_ip, picture_hash, self.cache_level, result_level, redis_object, new_redis_object)
                # print(self.redis_fake)
                self.modify_cache_node(picture_hash=picture_hash, redis_object=copy.deepcopy(new_redis_object), use_LRU_label=use_LRU_label, use_LRU_social=use_LRU_social, use_OPT=use_OPT)
                # print(self.redis_fake)
                # print("------")

            '''启用HTTP，从user_host对当前节点进行HTTP_GET操作'''
            if self.picture_root_path != '/dev/null': 
                util.HTTP_GET(host=user_host, picture_hash=picture_hash, IP_address=self.host_ip, port_number=self.host_port, use_TLS=False, result_path=self.result_path+'wget/'+self.host_ip, picture_path='/dev/null')            

            '''返回一个list，分别表示[第几层命中的, 查到的redis_object]'''
            return [result_level, new_redis_object, util.latency_CDN(delay=request_delay, bandwidth=request_bandwidth, media_size=new_redis_object['media_size'])]

        else:
            # if self.cache_level == 3:
            #     print(self.cache_id, picture_hash, current_timestamp)
            #     exit(0)
            result_level = 0
            redis_object = {}

            '''如果当前层没找到，有更高层，向上查询'''
            if self.cache_level > 1:
                if ignore_cache == True and self.cache_level == 3:
                    if picture_hash in self.second_view_hash:
                        ignore_cache = False ## 和常规LRU一样操作即可
                    else:
                        self.second_view_hash.append(picture_hash)
                    
                find_result = self.higher_CDN_redis.find(picture_hash=picture_hash, user_host=user_host, current_timestamp=current_timestamp, need_update_cache=need_update_cache, config_timestamp=config_timestamp, use_LRU_label=use_LRU_label, use_LRU_social=use_LRU_social, ignore_cache=ignore_cache, request_delay=self.higher_CDN_delay, request_bandwidth=self.higher_CDN_bandwidth, use_OPT=use_OPT)
                result_level = copy.deepcopy(find_result[0])
                redis_object = copy.deepcopy(find_result[1])
                latency_CDN = copy.deepcopy(find_result[2])

                '''上层已经操作完毕。根据上层的结果，当前层获取图片cache'''
                if result_level != 0: 
                    '''有命中数据'''
                    # print("view miss!!!", self.host_ip, picture_hash, self.cache_level, result_level, redis_object)
                    # print(self.redis_fake)
                    self.insert(picture_hash=picture_hash, redis_object=copy.deepcopy(redis_object), need_uplift=False, use_LRU_label=use_LRU_label, use_LRU_social=use_LRU_social, first_insert=False, lru_social_parameter_sp=0, ignore_cache=ignore_cache, use_OPT=use_OPT)
                    # print(self.redis_fake)
                    # print("------")
            
            '''返回一个list，分别表示[第几层命中的, 查到的redis_object]'''
            return [result_level, redis_object, latency_CDN + util.latency_CDN(delay=request_delay, bandwidth=request_bandwidth, media_size=redis_object['media_size'])]

