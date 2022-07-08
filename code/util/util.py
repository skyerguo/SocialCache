import math
import os
import shutil
import time
from timeit import repeat

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

def find_nearest_location(loc1, loc_list):
    nearest_distance = 6371 * 2
    nearest_id = -1
    for loc_id in range(len(loc_list)):
        if calc_geolocation_distance(loc1, loc_list[loc_id]) < nearest_distance:
            nearest_distance = calc_geolocation_distance(loc1, loc_list[loc_id])
            nearest_id = loc_id
    return nearest_id

def reflush_path(path):
    if os.path.exists(path):
        if 'temp' in path:
            os.system('rm -rf ' + path)
        # if os.path.isdir(path):
        #     shutil.rmtree(path)
        # elif os.path.isfile(path):
        #     os.remove(path)
        # elif os.path.islink(path):
        #     os.remove(path)
    os.system('mkdir -p ' + path)

def create_picture(host, picture_size, picture_path):
    host.cmd('head -c %s /dev/zero > %s'%(str(picture_size), picture_path))
    for _ in range(5):
        if not os.path.exists(picture_path):
            print('文件' + picture_path + '未创建成功，等待一秒')
            time.sleep(1)
        else:
            break

def delete_picture(host, path):
    host.cmd('rm %s'%(str(path)))

def HTTP_get():
    pass

def HTTP_post(host, picture_path, IP_address, port_number, use_TLS=False, result_path=''):
    host.cmd('curl -k -i -X POST -F filename=@"%s" -F name=file "http%s://%s:%s" 1>> %s/curl_log1.txt 2>> %s/curl_log2.txt '%(picture_path, 's' if use_TLS==True else '', str(IP_address), str(port_number), str(result_path), str(result_path)))

def calculate_flow(host, eth_name, flow_direction, result_path=''):
    '''
        flow_direction 只能为 RX或者TX
    '''
    print("flow_direction: ", flow_direction)
    if flow_direction != 'RX' and flow_direction != 'TX':
        return -1
    export_path = result_path + '/%s_%s.log' % (str(flow_direction), str(eth_name))
    host.cmdPrint("ifconfig %s | grep %s | grep bytes | awk '{print $5}' > %s"%(str(eth_name), str(flow_direction), str(export_path)))
