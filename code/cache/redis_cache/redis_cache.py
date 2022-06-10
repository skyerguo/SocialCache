import logging
import json
import redis
import pickle
import queue
import subprocess

class Redis_cache:
    def __init__(self, db, cache_size=10, use_priority_queue=True):
        """初始化

        Args:
            db (int): 数据库表单
            use_priority_queue (bool, optional): 是否使用优先队列维护权值最小的点. Defaults to True.
        """
        logging.info("initing redis cache...")

        # '''从config获得参数'''
        # config = json.load(open('code/cache/redis_cache/config.json', 'r'))
        self.cache_size = int(cache_size)

        '''获得本机的IP地址，作为redis IP'''
        # self.redis_ip = "128.105.145.13"
        ret = subprocess.Popen("ifconfig enp1s0f0 | grep inet | awk '{print $2}' | cut -f 2 -d ':'",shell=True,stdout=subprocess.PIPE)
        self.redis_ip = ret.stdout.read().decode("utf-8").strip('\n')
        ret.stdout.close()

        '''连接池'''
        pool = redis.ConnectionPool(
            host=self.redis_ip,
            port=6379,
            db=db,
            password='gtcA4010',
            max_connections=None  # 连接池最大值，默认2**31
        )
        self.redis = redis.Redis(connection_pool=pool)

        '''实验开始，清空该数据库'''
        self.redis.flushdb()

        '''设置优先队列'''
        self.use_priority_queue = use_priority_queue
        if self.use_priority_queue:
            self.priority_queue = queue.PriorityQueue()

    def __del__(self):
        '''程序结束后，自动关闭连接，释放资源'''
        self.redis.connection_pool.disconnect()

    def remove_cache_node(self):
        '''删掉权值最小的cache数据'''

        '''寻找权值最小的key'''
        if self.use_priority_queue:
            a = self.priority_queue.get() ## 取出并在priority_queue中去掉该元素
            min_value = a[0]
            min_value_related_key = a[1]
        else:
            min_value = 1e9
            min_value_related_key = -1
            for curr_key in self.redis.keys():
                curr_value = pickle.loads(self.redis.get(name=curr_key))
                if curr_value < min_value:
                    min_value = curr_value
                    min_value_related_key = curr_key
        
        self.redis.delete(min_value_related_key)

    def insert(self, picture_hash, picture_value):
        '''如果当前cache的空间使用完了，则替换'''
        if self.redis.dbsize() >= self.cache_size:
            self.remove_cache_node()
        
        '''插入redis数据库'''
        self.redis.set(name=picture_hash, value=pickle.dumps(picture_value))

        '''如有有使用优先队列，每次插入时需要维护优先队列'''
        if self.use_priority_queue:
            self.priority_queue.put((picture_value, picture_hash))

    def find(self, picture_hash):
        value = self.redis.get(name=picture_hash)
        if value:
            value = pickle.loads(value)
        else:
            value = -1
        return value

# if __name__ == '__main__':
#     r = Redis_cache(0)
#     for i in range(5):
#         r.insert(i, i)