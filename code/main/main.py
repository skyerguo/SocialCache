from code.build.build_main import Build_network
from code.trace.make_trace import Make_trace
from code.cache.redis_cache.redis_cache import Redis_cache
import code.util.util as util
import json

b = Build_network()
b.run()
host_all = []
for level_1_host_id in range(b.level_1_host_number):
    b.level_1_host[level_1_host_id].redis_cache = Redis_cache(db=len(host_all), cache_size=500)
    host_all.append(b.level_1_host[level_1_host_id])
for level_2_host_id in range(b.level_2_host_number):
    b.level_2_host[level_2_host_id].redis_cache = Redis_cache(db=len(host_all), cache_size=50)
    host_all.append(b.level_2_host[level_2_host_id])
for level_3_host_id in range(b.level_3_host_number):
    b.level_3_host[level_3_host_id].redis_cache = Redis_cache(db=len(host_all), cache_size=5)
    host_all.append(b.level_3_host[level_2_host_id])

topo = json.load(open('code/build/topo.json', 'r'))
level_3_area_id = topo['level_3_id']
level_3_area_location = []
for area_id in level_3_area_id:
    level_3_area_location.append(topo["areaid2position"][str(area_id)])

trace_dir = 'naive'
m = Make_trace(trace_dir)
m.run()

find_success_number = [0, 0, 0, 0]
find_fail_number = [0, 0, 0, 0]
'''read_trace'''
f_in = open("data/traces/" + trace_dir + "/all_timeline.txt", "r")
for line in f_in:
    current_type = line.split('+')[-1].strip()
    current_location = eval(line.split('+')[2])
    current_timestamp = int(line.split('+')[0])
    
    selected_level_3_id = util.find_nearest_location(current_location, level_3_area_location)
    bind_level_2_id = topo['up_bind_3_2'][selected_level_3_id]
    bind_level_1_id = topo['up_bind_2_1'][bind_level_2_id]

    if current_type == "post":
        post_id = int(line.split('+')[4])
        # print(current_type, post_id)
        b.level_3_host[selected_level_3_id].redis_cache.insert(post_id, current_timestamp)
        b.level_2_host[bind_level_2_id].redis_cache.insert(post_id, current_timestamp)
        b.level_1_host[bind_level_1_id].redis_cache.insert(post_id, current_timestamp)

    elif current_type == "view":
        post_id = int(line.split('+')[1])
        if b.level_3_host[selected_level_3_id].redis_cache.find(post_id) == -1:
            find_fail_number[3] += 1
            if b.level_2_host[bind_level_2_id].redis_cache.find(post_id) == -1:
                find_fail_number[2] += 1
                if b.level_1_host[bind_level_1_id].redis_cache.find(post_id) == -1:
                    find_fail_number[1] += 1
                else:
                    find_success_number[1] += 1
            else:
                find_success_number[2] += 1
        else:
            find_success_number[3] += 1
    else:
        print("ERROR!")
f_in.close()

'''分析'''
print("三级CDN缓存命中率：", find_success_number[3] / (find_success_number[3] + find_fail_number[3]))
print("二级CDN缓存命中率：", find_success_number[2] / (find_success_number[2] + find_fail_number[2]))
print("一级CDN缓存命中率：", find_success_number[1] / (find_success_number[1] + find_fail_number[1]))
