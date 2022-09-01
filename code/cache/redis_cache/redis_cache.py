import logging
import json
import queue
import subprocess
from collections import OrderedDict, defaultdict
import os
import code.util.util as util
import copy

class Redis_cache:
    def __init__(self, db, host, cache_size=5, use_priority_queue=True, use_LRU_cache=False, result_path='~/', host_ip='', host_port='', cache_level=0):
        """初始化

        Args:
            db (int): 数据库表单
            use_priority_queue (bool, optional): 是否使用优先队列维护权值最小的点. Defaults to True.
        """
        logging.info("initing redis cache...")

        self.cache_size = int(cache_size)

        '''获得本机的IP地址，作为redis IP'''
        # self.redis_ip = "128.105.145.13"
        ret = subprocess.Popen("ifconfig eno1 | grep inet | awk '{print $2}' | cut -f 2 -d ':'",shell=True,stdout=subprocess.PIPE)
        self.redis_ip = ret.stdout.read().decode("utf-8").strip('\n')
        ret.stdout.close()

        '''记录db数据'''
        self.db=db

        '''连接池'''
        self.redis_fake = {}

        '''设置优先队列'''
        self.use_priority_queue = use_priority_queue
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

        '''设置当前cache对应的mininet_host'''
        self.host = host
        
        '''设置当前cache的IP地址和HTTP端口'''
        self.host_ip = host_ip
        self.host_port = host_port

        self.hash_table = {}

        '''设置结果存的根目录'''
        self.result_path = result_path
        os.system('mkdir -p ' + self.result_path + 'mediaSize/' + self.host_ip)
        self.file_insert_media_size = open(self.result_path + 'mediaSize/' + self.host_ip + '/insert_all.txt', 'a')
        self.file_receive_media_size = open(self.result_path + 'mediaSize/' + self.host_ip + '/receive_all.txt', 'a')

    def remove_cache_node(self, given_key=''):
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
                    # print(curr_value)
                    if curr_value < min_value:
                        min_value = curr_value
                        remove_key = curr_key
        del self.redis_fake[remove_key]

        if self.picture_root_path != '/dev/null': ## 启用HTTP了
            util.delete_picture(host=self.host, picture_path=self.picture_root_path+str(remove_key)) #在硬盘中删除当前文件，保证硬盘不会存太多垃圾文件

    def modify_cache_node(self, picture_hash, redis_object):
        '''修改cache里面的节点，一般为插入或者调整'''

        '''如果是LRU，特殊处理'''
        if self.use_LRU_cache: 
            '''若数据已存在，表示命中一次，需要把数据移到缓存队列末端'''
            if picture_hash in self.LRUcache:
                self.LRUcache.move_to_end(picture_hash)
            elif len(self.redis_fake) >= self.cache_size:
                '''若缓存已满，则需要淘汰最早没有使用的数据'''
                self.remove_cache_node(given_key=next(iter(self.LRUcache)))
                self.LRUcache.popitem(last=False)
            self.LRUcache[picture_hash] = redis_object['sort_value']

        else:
            '''如果当前cache的空间使用完了，且不是LRU，则按照内在的权值替换'''
            if len(self.redis_fake) >= self.cache_size:
                if picture_hash not in self.redis_fake.keys() and len(self.redis_fake) == self.cache_size:
                    self.remove_cache_node()
        
        '''插入redis数据库'''
        self.redis_fake[picture_hash] = redis_object
        '''留个检测，以防出现bug'''
        if len(self.redis_fake) > self.cache_size:
            print("Error to check!!!", picture_hash, self.redis_fake[picture_hash])
            exit(0)

        '''如有有使用优先队列，每次插入时需要维护优先队列。使用第一关键字为sort_value，第二关键字为timestamp。保证timestamp互不相同，从而保证了key的唯一'''
        if self.use_priority_queue:
            self.hash_table[picture_hash] = (redis_object['sort_value'], redis_object['timestamp'])
            self.priority_queue.put(((redis_object['sort_value'], redis_object['timestamp']), picture_hash))  
        
    def get_lru_social_parameter_s(self) -> int:
        res = 0
        for curr_key in self.redis_fake.keys():
            curr_value = self.redis_fake[curr_key]['sort_value']
            if curr_value > self.cache_size:
                res += 1
        return res

    def decrement_lru_social(self, lowerest_threshold=0):
        for curr_key in self.redis_fake.keys():
            temp_redis_object = self.redis_fake[curr_key]
            curr_value = int(temp_redis_object['sort_value'])
            if curr_value > lowerest_threshold:
                temp_redis_object['sort_value'] = curr_value - 1
                self.redis_fake[curr_key] = temp_redis_object
                '''lru-social就不要管priority_queue了'''
                # if self.use_priority_queue:
                    # self.priority_queue.put((temp_redis_object['sort_value'], int.from_bytes(curr_key, byteorder='big'))) 

    def insert(self, picture_hash, redis_object, need_uplift=True, use_LRU_social=False, first_insert=False, lru_social_parameter_sp=0):
        '''
            need_uplift: True表示向上传播，False表示向下传播
        '''

        print(redis_object['media_size'], file=self.file_receive_media_size)
        
        if use_LRU_social:
            lru_social_parameter_c = self.cache_size
            lru_social_parameter_s = self.get_lru_social_parameter_s()
            if first_insert:
                '''set the sort_value as SPu * C'''
                # print("lru_social_parameter_sp: ", lru_social_parameter_sp)
                # print("lru_social_parameter_c: ", lru_social_parameter_c)
                redis_object['sort_value'] = lru_social_parameter_sp * lru_social_parameter_c + redis_object['timestamp']
                # print("redis_object['sort_value']: ", redis_object['sort_value'])
            else:
                '''set label as C-S'''
                if lru_social_parameter_c - lru_social_parameter_s > 0:
                    redis_object['sort_value'] = lru_social_parameter_c - lru_social_parameter_s + redis_object['timestamp']
                else:
                    redis_object['sort_value'] = redis_object['timestamp']

        self.modify_cache_node(picture_hash=picture_hash, redis_object=redis_object)

        if need_uplift:
            '''需要逐层递归向上传播'''
            if self.picture_root_path != '/dev/null': 
                '''使用HTTP，相关的数据传输和存储'''
                if self.cache_level == 3: 
                    '''如果需要创建图片，则在最后一层路径中创建一个文件'''
                    util.create_picture(host=self.host, picture_size=redis_object['media_size'], picture_path=self.picture_root_path+str(picture_hash))

                if self.cache_level > 1:
                    '''如果有上层cache的需要，使用HTTP_POST向上传播'''
                    util.HTTP_POST(host=self.host, picture_path=self.picture_root_path+str(picture_hash), IP_address=self.higher_cache_redis.host_ip, port_number=self.higher_cache_redis.host_port, use_TLS=False, result_path=self.result_path+'curl/'+self.host_ip)

            if self.cache_level > 1:
                '''递归调用，一层层上传'''
                print(redis_object['media_size'], file=self.file_insert_media_size)
                self.higher_cache_redis.insert(picture_hash=picture_hash, redis_object=redis_object, need_uplift=need_uplift, use_LRU_social=use_LRU_social, first_insert=first_insert, lru_social_parameter_sp=lru_social_parameter_sp) 

        elif self.cache_level > 1: 
            '''如果不是最后一层，而且需要从上层获取数据传播'''
            if self.picture_root_path != '/dev/null': 
                '''从该节点对上一层进行HTTP_GET操作。这里保证上层有需要的数据'''
                util.HTTP_GET(host=self.host, picture_hash=picture_hash, IP_address=self.higher_cache_redis.host_ip, port_number=self.higher_cache_redis.host_port, use_TLS=False, result_path=self.higher_cache_redis.result_path+'wget/'+self.host_ip, picture_path=self.picture_root_path+str(picture_hash))
            print(redis_object['media_size'], file=self.higher_cache_redis.file_insert_media_size)

    def find(self, picture_hash, user_host, current_timestamp, need_update_cache=False, config_timestamp=1, use_LRU_social=False):
        
        if picture_hash in self.redis_fake.keys():
            '''如果找到了'''
            redis_object = self.redis_fake[picture_hash]
            result_level = self.cache_level
            new_redis_object= copy.deepcopy(redis_object)

            '''查询需要更新cache'''
            if need_update_cache:
                if use_LRU_social:
                    lru_social_parameter_c = self.cache_size
                    lru_social_parameter_s = self.get_lru_social_parameter_s()
                    result_label = redis_object['sort_value']
                    if result_label > lru_social_parameter_c:
                        self.decrement_lru_social(lowerest_threshold=lru_social_parameter_c)
                    else:
                        self.decrement_lru_social(lowerest_threshold=result_label)
                    
                    if lru_social_parameter_c - lru_social_parameter_s > 0:
                        new_sort_value = lru_social_parameter_c - lru_social_parameter_s + current_timestamp
                    else:
                        new_sort_value = current_timestamp
                    new_redis_object['timestamp'] = current_timestamp
                    new_redis_object['sort_value'] = new_sort_value 
                else:
                    last_timestamp = redis_object['timestamp']
                    new_sort_value = redis_object['sort_value'] + (current_timestamp - last_timestamp) * config_timestamp
                    new_redis_object['timestamp'] = current_timestamp
                    new_redis_object['sort_value'] = new_sort_value
                
                # print("redis_object: ", redis_object)
                # print("new_redis_object: ", new_redis_object)
                self.modify_cache_node(picture_hash=picture_hash, redis_object=new_redis_object)

            '''启用HTTP，从user_host对当前节点进行HTTP_GET操作'''
            if self.picture_root_path != '/dev/null': 
                util.HTTP_GET(host=user_host, picture_hash=picture_hash, IP_address=self.host_ip, port_number=self.host_port, use_TLS=False, result_path=self.result_path+'wget/'+self.host_ip, picture_path='/dev/null')            

            '''返回一个list，分别表示[第几层命中的, 查到的redis_object]'''
            return [result_level, new_redis_object]

        else:
            result_level = 0
            redis_object = {}

            '''如果当前层没找到，有更高层，向上查询'''
            if self.cache_level > 1:
                find_result = self.higher_cache_redis.find(picture_hash=picture_hash, user_host=user_host, current_timestamp=current_timestamp, need_update_cache=need_update_cache, config_timestamp=config_timestamp, use_LRU_social=use_LRU_social)
                result_level = find_result[0]
                redis_object = find_result[1]

                '''上层已经操作完毕。根据上层的结果，当前层获取图片cache'''
                if result_level != 0: 
                    '''有命中数据'''
                    self.insert(picture_hash=picture_hash, redis_object=redis_object, need_uplift=False, use_LRU_social=use_LRU_social, first_insert=False, lru_social_parameter_sp=0)
            
            '''返回一个list，分别表示[第几层命中的, 查到的redis_object]'''
            return [result_level, redis_object]

