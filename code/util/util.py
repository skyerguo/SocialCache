import math
import os
import shutil
import time
from timeit import repeat
import numpy as np

def calc_geolocation_distance(loc1, loc2): 
    '''计算两个地理位置的地表距离，返回单位为公里'''

    from math import radians, cos, sin, asin, sqrt
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [float(loc1['lon']), float(loc1['lat']), float(loc2['lon']), float(loc2['lat'])])
 
    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # 地球平均半径，单位为公里
    return c * r

def find_nearest_location(loc1, loc_list) -> list:
    nearest_distance = 6371 * 2
    nearest_id = -1
    for loc_id in range(len(loc_list)):
        if calc_geolocation_distance(loc1, loc_list[loc_id]) < nearest_distance:
            nearest_distance = calc_geolocation_distance(loc1, loc_list[loc_id])
            nearest_id = loc_id
    return [nearest_id, nearest_distance]

def reflush_path(path):
    if os.path.exists(path):
        if 'temp' in path:
            os.system('rm -rf ' + path)
    os.system('mkdir -p ' + path)

def create_picture(host, picture_size, picture_path):
    host.cmdPrint('head -c %s /dev/zero > %s'%(str(picture_size), picture_path))
    for _ in range(5):
        if not os.path.exists(picture_path):
            print('文件' + picture_path + '未创建成功，等待一秒')
            time.sleep(1)
        else:
            break

def delete_picture(host, picture_path):
    host.cmd('rm %s'%(str(picture_path)))

def HTTP_GET(host, picture_hash, IP_address, port_number, use_TLS=False, result_path='', picture_path='/dev/null'):
    '''如果是user端调用，不需要存储，只需要跑流量，所以把数据结果存到/dev/null即可'''
    '''A wget B, 日志存储到B的对应文件夹中'''
    host.cmdPrint('wget http%s://%s:%s/%s -O %s -a %s/wget_log1.txt'%('s' if use_TLS==True else '', IP_address, port_number, picture_hash, picture_path, result_path))

def HTTP_POST(host, picture_path, IP_address, port_number, use_TLS=False, result_path=''):
    '''A curl B, 日志存储到A对应的文件夹中'''
    host.cmdPrint('curl -k -i -X POST -F filename=@"%s" -F name=file "http%s://%s:%s" 1>> %s/curl_log1.txt 2>> %s/curl_log2.txt '%(picture_path, 's' if use_TLS==True else '', IP_address, port_number, result_path, result_path))

def calculate_flow(host, eth_name, flow_direction, result_path=''):
    '''
        flow_direction 只能为 RX或者TX
    '''
    # print("flow_direction: ", flow_direction)
    if flow_direction != 'RX' and flow_direction != 'TX':
        return -1
    export_path = result_path + '/%s_%s.log' % (str(flow_direction), str(eth_name))
    host.cmd("ifconfig %s | grep %s | grep bytes | awk '{print $5}' > %s"%(str(eth_name), str(flow_direction), str(export_path)))

'''生成接表'''
def generate_adj_matrix_graph(relation_file_path, nodes_number):
    import re
    A = np.zeros((nodes_number, nodes_number), int)
    f_in = open(relation_file_path, "r")
    for line in f_in:
        user_list = re.split(' |\t',line.strip())
        A[int(user_list[1])][int(user_list[0])] = 1 ## 原图是关注，为了SIR传播，需要改为反向图，发送关系。
    f_in.close()

    return A


def random_percentage(ratio):
    import random
    coin = random.randint(1, 100)
    return coin <= ratio


def display_timeline(time_list):
    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt
    temp_df = pd.DataFrame(time_list)
    # print(temp_df)
    sns.displot(temp_df, kind="kde")
    result_path = './figures/timeline.png'
    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='png')

def hash_relations(filename):
    import re
    import os
    os.system("mv %s %s"%(filename, filename+'.bak'))
    hash_user = {}
    hash_number = 0
    with open(filename, 'w') as f_out:
        with open(filename+'.bak', 'r') as f_in:
            for line in f_in:
                user_list = re.split(' |\t',line.strip())
                if int(user_list[0]) not in hash_user:
                    hash_user[int(user_list[0])] = hash_number
                    hash_number += 1
                if int(user_list[1]) not in hash_user:
                    hash_user[int(user_list[1])] = hash_number
                    hash_number += 1
                print(hash_user[int(user_list[0])], hash_user[int(user_list[1])], file=f_out)
    return hash_user

def distance_to_delay(distance):
    # return 0.007 * distance + 7.774
    return 0.02 * (distance ** 0.89) ## ms

def distance_to_bandwidth(distance):
    return 228433.40 * (distance ** -0.82) ## Mbps

# # 对于user而言传一个文件所需时间
# def latency_user(distance, media_size):
#     return 2 * distance_to_delay(1/distance) + distance_to_bandwidth(distance) / media_size * 1024 * 1000 ## 转换单位，Mbps/kb

## 传一个文件所需时间，从高层CDN节点往下传时做计算
def latency_CDN(delay, bandwidth, media_size): ## ms
    return 2 * delay + media_size / (bandwidth * 1024) * 1000 ## 转换单位，kb/Mbps ==> ms