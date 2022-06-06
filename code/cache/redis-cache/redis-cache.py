import logging
import json
import redis

class Redis_cache:
    def __init__(self, db):
        logging.info("initing redis cache...")

        '''从config获得参数'''
        config = json.load(open('config.json', 'r'))
        self.cache_size = config['cache-size']

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

    def __del__(self):
        '''程序结束后，自动关闭连接，释放资源'''
        self.redis.connection_pool.disconnect()

    def insert(self, picture_hash, picture_value):
        self.redis.set(name=picture_hash, value=picture_value)
        pass

    def find(self, picture_hash):
        # r = redis.Redis(host=self.redis_ip , port='6379' , db=6 ,decode_responses=True)
        value = self.redis.get(name=picture_hash)
        print(value)
        pass

if __name__ == '__main__':
    r = Redis_cache(0)
    r.insert('123', 456)
