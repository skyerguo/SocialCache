import pymongo
import random

client = pymongo.MongoClient('localhost', 27117)
db = client['shuffle_index']
db_size = 100000
collection = db['shuffle_%s'%(db_size)]

obj = {}
a = [x for x in range(db_size)]
random.shuffle(a)

for i in range(db_size):
    collection.insert_one({'index': i, 'value': a[i]})
# print(obj)