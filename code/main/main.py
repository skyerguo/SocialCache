from code.build.build_main import Build_network
from code.trace.make_trace import Make_trace
from code.cache.redis_cache.redis_cache import Redis_cache

trace_dir = 'naive'
m = Make_trace(trace_dir)
m.run()

## read_trace
f_in = open("data/traces/" + trace_dir + "/all_timeline.txt", "r")
for line in f_in:
    current_type = line.split("+")[-1].strip()
    current_location = eval(line.split("+")[2])
f_in.close()

b = Build_network()
b.run()