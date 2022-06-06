from PyMimircache import Cachecow
c = Cachecow()
# c.csv("/users/gtc/PyMimircache/data/trace.csv", init_params={'label': 0})
c.vscsi("/users/gtc/PyMimircache/data/trace.vscsi")

# cnt = 0
# for curr_req in c:
#     print(curr_req)
#     cnt += 1
#     if cnt > 10:
#         break

# print(c.stat())
# print(c.get_reuse_distance())
# print(c.get_hit_ratio_dict("LRU", cache_size=20))
# c.plotHRCs(["LRU", "LFU", "Optimal"])