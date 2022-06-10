from code.build.build_main import Build_network
from code.trace.make_trace import Make_trace
from code.cache.redis_cache.redis_cache import Redis_cache
import code.util.util as util

b = Build_network()
b.run()

level_3_area_id = b.topo['level_3_id']
level_3_area_location = []
for area_id in level_3_area_id:
    level_3_area_location.append(b.topo["areaid2position"][str(area_id)])

trace_dir = 'naive'
m = Make_trace(trace_dir)
m.run()

## read_trace
f_in = open("data/traces/" + trace_dir + "/all_timeline.txt", "r")
for line in f_in:
    current_type = line.split("+")[-1].strip()
    current_location = eval(line.split("+")[2])

    # print(current_location, level_3_area_location)
    selected_level_3_id = util.find_nearest_location(current_location, level_3_area_location)
    # print(selected_level_3_id) 

    break
    # print()
f_in.close()
