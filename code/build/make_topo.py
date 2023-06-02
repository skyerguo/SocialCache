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
area_ignore = ['asia-southeast1', 'us-central1']

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
    if area in area_ignore:
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

delay_topo = [[0 for _ in range(len(area_all))] for _ in range(len(area_all))]
bandwidth_topo = [[0 for _ in range(len(area_all))] for _ in range(len(area_all))]

for line in lines:
    if (line[0][:-2] in area_ignore) or (line[1][7:-2] in area_ignore):
        continue

    src = map_area2id[line[0][:-2]] 
    des = map_area2id[line[1][7:-2]]

    delay_topo[src][des] = float(line[2]) / 2 ## delay是RTT的一半
    delay_topo[des][src] = float(line[2]) / 2

    bandwidth_topo[src][des] = line[3]
    bandwidth_topo[des][src] = line[3]

# print(delay_topo)
# print(bandwidth_topo)
'''定义每层节点地理位置'''
user_area = ['us-west4']
user_id = [map_area2id[x] for x in user_area]
level_CDN_1_area = ['asia-east2','asia-northeast1','asia-northeast2','asia-northeast3','asia-south1','asia-south2','asia-southeast2','australia-southeast1','australia-southeast2','europe-central2','europe-north1','europe-west1','europe-west2','europe-west3','europe-west4','europe-west6','northamerica-northeast1','northamerica-northeast2','southamerica-east1','southamerica-west1','us-east1','us-east4','us-west1','us-west3','us-west4']
level_CDN_1_id = [map_area2id[x] for x in level_CDN_1_area]
level_CDN_2_area = ['asia-east1', 'australia-southeast2', 'europe-central2', 'northamerica-northeast1', 'southamerica-east1']
level_CDN_2_id = [map_area2id[x] for x in level_CDN_2_area]
level_data_center_area = ['us-west2']
level_data_center_id = [map_area2id[x] for x in level_data_center_area]

'''定义层级向上绑定关系'''
up_bind_3_2 = []
for temp_3_area in level_CDN_1_area:
    temp_delay_min = 10000
    temp_delay_best_area_index = -1
    for j in range(len(level_CDN_2_area)):
        if delay_topo[map_area2id[temp_3_area]][level_CDN_2_id[j]] < temp_delay_min:
            temp_delay_min = delay_topo[map_area2id[temp_3_area]][level_CDN_2_id[j]]
            temp_delay_best_area_index = j
    up_bind_3_2.append(temp_delay_best_area_index)

up_bind_2_1 = [0 for _ in range(len(level_CDN_2_area))]

'''获得经纬度'''
areaid2position = {}
position_path_name = 'data/static/position-gcp-list.csv'  
with open(position_path_name, 'r') as csv_file:
    cnt_line = -1
    for line in csv_file:
        if cnt_line == -1:
            cnt_line += 1
            continue
        curr_area = line.split(',')[0]
        if curr_area in area_ignore:
            continue
        latitude = line.split(',')[1]
        longitude = line.split(',')[2].strip()
        areaid2position[map_area2id[curr_area]] = {'lon': longitude, 'lat': latitude}

result = {}
result['level_CDN_1_id'] = level_CDN_1_id
result['level_CDN_2_id'] = level_CDN_2_id
result['level_data_center_id'] = level_data_center_id
result['user_id'] = user_id
result['up_bind_3_2'] = up_bind_3_2
result['up_bind_2_1'] = up_bind_2_1
result['delay_topo'] = delay_topo
result['bandwidth_topo'] = bandwidth_topo
result['areaid2position'] = areaid2position
result['cpu_level_CDN_1'] = 0.3
result['cpu_level_CDN_2'] = 0.3
result['cpu_level_data_center'] = 0.3
result['cpu_user'] = 1

json_file = 'code/build/topo.json'
f_out = open(json_file, 'w')
json.dump(result, f_out)
f_out.close()