import os
import csv
import random
import json
import copy

# SET_MAX_BW = 10 ## 假设最大的带宽为10MB/s

area_all = ['asia-east1','asia-east2','asia-northeast1','asia-northeast2','asia-northeast3','asia-south1','asia-south2','asia-southeast2','australia-southeast1','australia-southeast2','europe-central2','europe-north1','europe-west1','europe-west2','europe-west3','europe-west4','europe-west6','northamerica-northeast1','northamerica-northeast2','southamerica-east1','southamerica-west1','us-east1','us-east4','us-west1','us-west2','us-west3','us-west4']
area_zone = {
    '0': ['asia-east1','asia-east2','asia-northeast1','asia-northeast2','asia-northeast3','asia-south1','asia-south2','asia-southeast2'], 
    '1': ['australia-southeast1','australia-southeast2'], 
    '2': ['europe-central2','europe-north1','europe-west1','europe-west2','europe-west3','europe-west4','europe-west6'],
    '3': ['northamerica-northeast1','northamerica-northeast2'],
    '4': ['southamerica-east1','southamerica-west1'],
    '5': ['us-east1','us-east4','us-west1','us-west2','us-west3','us-west4'],
}
zone_ignore = ['asia-southeast1', 'us-central1']

max_bw = 0
csv_file_path = 'data/static/measure.csv'
f_in = open(csv_file_path, 'r')
csv_reader = csv.reader(f_in)

'''获得两种反向查找方式'''
map_area2id = {}
map_area2zone = {}
for i in range(len(area_all)):
    map_area2id[area_all[i]] = i
for curr_zone in area_zone.keys():
    for i in range(len(area_zone[curr_zone])):
        map_area2zone[area_zone[curr_zone][i]] = int(curr_zone)

'''处理数据中的Gb,Mb,Kb'''
lines = []
for line in csv_reader:
    lines.append(line)

    area = line[0][:-2]
    if area in zone_ignore:
        continue
    if not line[3]:
        continue
    elif 'Mb' in line[3].split('_')[1]:
        line[3] = float(line[3].split('_')[0])
        max_bw = max(max_bw, line[3])
    elif 'Gb' in line[3].split('_')[1]:
        line[3] = float(line[3].split('_')[0]) * 1000
        max_bw = max(max_bw, line[3])
    elif 'Kb' in line[3].split('_')[1]:
        line[3] = float(line[3].split('_')[0]) / 1000
        max_bw = max(max_bw, line[3])

latency_topo = [[0 for _ in range(len(area_all))] for _ in range(len(area_all))]
bandwidth_topo = [[0 for _ in range(len(area_all))] for _ in range(len(area_all))]

for line in lines:
    if (line[0][:-2] in zone_ignore) or (line[1][7:-2] in zone_ignore):
        continue

    src = map_area2id[line[0][:-2]] 
    des = map_area2id[line[1][7:-2]]

    latency_topo[src][des] = float(line[2])
    latency_topo[des][src] = float(line[2])

    bandwidth_topo[src][des] = line[3]
    bandwidth_topo[des][src] = line[3]

# print(latency_topo)
# print(bandwidth_topo)

level_3_area = ['asia-east1', 'australia-southeast2', 'europe-central2', 'northamerica-northeast1', 'southamerica-east1']
level_3_id = [map_area2id[x] for x in level_3_area]
level_2_area = ['us-east1', 'asia-northeast1', 'southamerica-west1']
level_2_id = [map_area2id[x] for x in level_2_area]
level_1_area = ['us-west2']
level_1_id = [map_area2id[x] for x in level_1_area]

result = {}
result['level_3_id'] = level_3_id
result['level_2_id'] = level_2_id
result['level_1_id'] = level_1_id
result['latency_topo'] = latency_topo
result['bandwidth_topo'] = bandwidth_topo

json_file = 'code/build/topo.json'
f_out = open(json_file, 'w')
json.dump(result, f_out)
f_out.close()
exit()

# print(latency_topo)
# print(bandwidth_topo[0])

## 定义每个client的位置
for i in range(0, CLIENT_NUMBER):
    temp_sum = 0
    for j in range(len(zone_ratio)):
        temp_sum += zone_ratio[j]
        if temp_sum > i%SERVER_NUMBER:
            temp = random.choice(area_zone[j])

            while (client2dispatcher[zone_map[temp]] >= DISPATCHER_NUMBER):
                temp = random.choice(area_zone[j])
            client_zone.append(temp)
            
            break

# ## 定义每个server的位置
# for i in range(DISPATCHER_NUMBER, SERVER_NUMBER):
#     temp = random.choice(area_all)
#     while (client2dispatcher[zone_map[temp]] >= DISPATCHER_NUMBER):
#         temp = random.choice(area_all)
#     server_zone.append(temp)

result = {}
result['client_number'] = CLIENT_NUMBER
result['server_number'] = SERVER_NUMBER
result['dispatcher_number'] = DISPATCHER_NUMBER
result['client_thread'] = THREAD_NUMBER
# result['server_thread'] = THREAD_NUMBER
# result['dispatcher_thread'] = THREAD_NUMBER
result['cpu'] = {}
# result['cpu']['client'] = .2 * CLIENT_NUMBER
# result['cpu']['server'] = .2 * SERVER_NUMBER
# result['cpu']['dispatcher'] = .2 * DISPATCHER_NUMBER
result['cpu']['client'] = .4
result['cpu']['server'] = .3
result['cpu']['dispatcher'] = .3
result['dns_links'] = dns_links
result['dns_outers'] = dns_outers

result['client_zone'] = []
result['server_zone'] = []
result['dispatcher_zone'] = []
for client_area in client_zone:
    result['client_zone'].append(client2dispatcher[zone_map[client_area]])
for server_area in server_zone:
    result['server_zone'].append(client2dispatcher[zone_map[server_area]])
for dispatcher_area in dispatcher_zone:
    result['dispatcher_zone'].append(client2dispatcher[zone_map[dispatcher_area]])


result['bw'] = {}
result['delay'] = {}


result['bw']['client_server'] = [[] for _ in range(CLIENT_NUMBER)]
result['delay']['client_server'] = [[] for _ in range(CLIENT_NUMBER)]
for client_id in range(CLIENT_NUMBER):
    client_pos = zone_map[client_zone[client_id]]
    for server_id in range(SERVER_NUMBER):
        server_pos = zone_map[server_zone[server_id]]
        result['bw']['client_server'][client_id].append(bandwidth_topo[client_pos][server_pos])
        result['delay']['client_server'][client_id].append(latency_topo[client_pos][server_pos])

result['bw']['client_dispatcher'] = [[] for _ in range(CLIENT_NUMBER)]
result['delay']['client_dispatcher'] = [[] for _ in range(CLIENT_NUMBER)]
for client_id in range(CLIENT_NUMBER):
    client_pos = zone_map[client_zone[client_id]]
    for dispatcher_id in range(DISPATCHER_NUMBER):
        dispatcher_pos = zone_map[dispatcher_zone[dispatcher_id]]
        result['bw']['client_dispatcher'][client_id].append(bandwidth_topo[client_pos][dispatcher_pos])
        result['delay']['client_dispatcher'][client_id].append(latency_topo[client_pos][dispatcher_pos])

result['bw']['dispatcher_server'] = [[] for _ in range(DISPATCHER_NUMBER)]
result['delay']['dispatcher_server'] = [[] for _ in range(DISPATCHER_NUMBER)]
for dispatcher_id in range(DISPATCHER_NUMBER):
    dispatcher_pos = zone_map[dispatcher_zone[dispatcher_id]]
    for server_id in range(SERVER_NUMBER):
        server_pos = zone_map[server_zone[server_id]]
        result['bw']['dispatcher_server'][dispatcher_id].append(bandwidth_topo[dispatcher_pos][server_pos])
        result['delay']['dispatcher_server'][dispatcher_id].append(latency_topo[dispatcher_pos][server_pos])
    
json_file = '../json-files/topo.json'
f_out = open(json_file, 'w')
json.dump(result, f_out, indent=1)
f_out.close()
