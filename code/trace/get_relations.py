usernet_path = "./data/static/gplus_combined.txt"
result_path = "./data/traces/google_plus_trace/relations.txt"

hash_map = {}
f_out = open(result_path, 'w')

cnt = 0
with open(usernet_path, 'r') as f_in:
    for line in f_in:
        u = int(line.split(' ')[0])
        v = int(line.split(' ')[1])
        if u not in hash_map.keys():
            hash_map[u] = cnt
            cnt += 1
        if v not in hash_map.keys():
            hash_map[v] = cnt
            cnt += 1
        print(hash_map[u], hash_map[v], file=f_out)
