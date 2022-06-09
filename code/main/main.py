from code.build.build_main import Build_network
from code.trace.make_trace import Make_trace
from code.cache.redis_cache.redis_cache import Redis_cache

trace_dir = 'naive'
m = Make_trace(trace_dir)
m.run()

b = Build_network()
b.run()

## read_trace
f_posts_in = open("data/traces/" + trace_dir + "/posts_timeline.txt", "r")
f_views_in = open("data/traces/" + trace_dir + "/views_timeline.txt", "r")



f_posts_in.close()
f_views_in.close()
