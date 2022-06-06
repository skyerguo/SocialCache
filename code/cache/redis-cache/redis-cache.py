import logging
import json
import redis
import pickle

class Redis_cache:
    def __init__(self, db):
        logging.info("initing redis cache...")

        '''从config获得参数'''
        config = json.load(open('config.json', 'r'))
        self.cache_size = int(config['cache-size'])

        '''获得本机的IP地址，作为redis IP'''
        self.redis_ip = "128.105.145.13"
        # ret = subprocess.Popen("ifconfig eno1 | grep inet | awk '{print $2}' | cut -f 2 -d ':'",shell=True,stdout=subprocess.PIPE)
        # self.redis_ip = ret.stdout.read().decode("utf-8").strip('\n')
        # ret.stdout.close()

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

    def __del__(self):
        '''程序结束后，自动关闭连接，释放资源'''
        self.redis.connection_pool.disconnect()

    def remove_cache_node(self):
        '''删掉权值最小的cache数据'''

        '''这里暂时用for循环着最小值，之后改成小根堆'''
        min_value = 1e9
        min_value_related_key = -1
        for curr_key in self.redis.keys():
            # print(curr_key, self.redis.get(name=curr_key))
            curr_value = pickle.loads(self.redis.get(name=curr_key))
            if curr_value < min_value:
                min_value = curr_value
                min_value_related_key = curr_key
        
        self.redis.delete(min_value_related_key)

    def insert(self, picture_hash, picture_value):
        if self.redis.dbsize() >= self.cache_size:
            self.remove_cache_node()
        self.redis.set(name=picture_hash, value=pickle.dumps(picture_value))

    def find(self, picture_hash):
        value = pickle.loads(self.redis.get(name=picture_hash))
        print(value)

if __name__ == '__main__':
    r = Redis_cache(0)
    for i in range(5):
        r.insert(i, i)
    
