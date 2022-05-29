import os
import csv
import random
import json
import copy

SET_MAX_BW = 5 ## 假设最大的带宽为5MB/s
CLIENT_NUMBER = 100
DISPATCHER_NUMBER = 5 # 最多10个
SERVER_NUMBER = 15
THREAD_NUMBER = 5 # 每个CLIENT的线程数，请算一下14433+CLIENT_NUMBER*THREAD_NUMBER，是否可能造成冲突**

csv_file_path = '../data-prepare/measure.csv'
f_in = open(csv_file_path, 'r')
csv_reader = csv.reader(f_in)

area_all = ['asia-east1','asia-east2','asia-northeast1','asia-northeast2','asia-northeast3','asia-south1','asia-south2','asia-southeast2','australia-southeast1','australia-southeast2','europe-central2','europe-north1','europe-west1','europe-west2','europe-west3','europe-west4','europe-west6','northamerica-northeast1','northamerica-northeast2','southamerica-east1','southamerica-west1','us-east1','us-east4','us-west1','us-west2','us-west3','us-west4']
area_zone = [
    ['asia-east1','asia-east2','asia-northeast1','asia-northeast2','asia-northeast3','asia-south1','asia-south2','asia-southeast2'], 
    ['australia-southeast1','australia-southeast2'], 
    ['europe-central2','europe-north1','europe-west1','europe-west2','europe-west3','europe-west4','europe-west6'],
    ['northamerica-northeast1','northamerica-northeast2'],
    ['southamerica-east1','southamerica-west1'],
    ['us-east1','us-east4','us-west1','us-west2','us-west3','us-west4'],
]
zone_ignore = ['asia-southeast1', 'us-central1']

zone_dispatcher = ['asia-southeast2', 'australia-southeast1', 'europe-west3', 'northamerica-northeast1', 'southamerica-west1', 'us-west2']
zone_server = [
    ['asia-east1','asia-northeast3','asia-south2','asia-southeast2'], 
    ['australia-southeast1'],
    ['europe-central2','europe-north1','europe-west1'],
    ['northamerica-northeast1','northamerica-northeast2'],
    ['southamerica-east1'],
    ['us-east1','us-east4','us-west3','us-west4'], 
]
zone_ratio = [4, 1, 3, 2, 1, 4] # 保证相加 = SERVER_NUMBER

## 4 1 3 2 1 4  server分布 Polygon+Anycast
## client按照server的zone分布来
## FastRoute
## 2 1 1 1 1 2  外层      
## 1 0 1 0 0 1  内层
## 1 0 1 1 0 1  中层 
## 映射关系
## aus->asia，southamerica->us, northamerica->us
## 0->2, 1->2, 2->3
## 4->2
## 5->6, 6->7
## 8->9, 9->14
## 10->13
## 11->13, 12->13, 13->14
dns_links = [[0,2], [1,2], [2,3], [4,2], [5,6], [6,7], [8,9], [9,14], [10,13], [11,13], [12,13], [13,14]]
dns_outers = [[0,1], [4], [5], [8], [10], [11,12]] 

zone_dispatcher = zone_dispatcher[:DISPATCHER_NUMBER]
client2dispatcher = [0 for _ in range(len(area_all))]
client2dispatcher[0] = client2dispatcher[1] = client2dispatcher[2] = client2dispatcher[3] =  client2dispatcher[4] = client2dispatcher[5] = client2dispatcher[6] =  client2dispatcher[7] = 0
client2dispatcher[8] = client2dispatcher[9] = 1
client2dispatcher[10] = client2dispatcher[11] = client2dispatcher[12] = client2dispatcher[13] = client2dispatcher[14] = client2dispatcher[15] =  client2dispatcher[16] =  2
client2dispatcher[17] = client2dispatcher[18] = 3
client2dispatcher[19] = client2dispatcher[20] = 4
client2dispatcher[21] = client2dispatcher[22] = client2dispatcher[23] = client2dispatcher[24] = client2dispatcher[25] = client2dispatcher[26] = 5

client_zone = []
dispatcher_zone = copy.deepcopy(zone_dispatcher)
server_zone = [y for x in zone_server for y in x]

zone_number = 0
zone_map = {}

max_bw = 0

lines = []

for line in csv_reader:
    lines.append(line)

    area = line[0][:-2]
    if area in zone_ignore:
        continue
    if area not in zone_map:    
        zone_map[area] = zone_number
        zone_number += 1

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

latency_topo = [[0 for _ in range(zone_number)] for _ in range(zone_number)]
bandwidth_topo = [[0 for _ in range(zone_number)] for _ in range(zone_number)]

print("max bandwidth: ", max_bw)
# exit(0)
# print("zone_number:", zone_number)

for line in lines:
    if (line[0][:-2] in zone_ignore) or (line[1][7:-2] in zone_ignore):
        continue

    src = zone_map[line[0][:-2]] 
    des = zone_map[line[1][7:-2]]

    latency_topo[src][des] = float(line[2])
    latency_topo[des][src] = float(line[2])

    bandwidth_topo[src][des] = (line[3] / max_bw) * SET_MAX_BW
    bandwidth_topo[des][src] = (line[3] / max_bw) * SET_MAX_BW

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
