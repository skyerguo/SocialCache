import math
import os
import shutil

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

def create_picture(mininet_node, picture_size, path):
    mininet_node.cmdPrint('head -c %s /dev/zero > %s'%(str(picture_size), path))

def delete_picture(mininet_node, path):
    mininet_node.cmdPrint('rm %s'%(str(path)))

def HTTP_get():
    pass

def HTTP_post(mininet_node, path, IP_address, port_number, use_TLS=False):
    print('logger: curl -k -i -X POST -F filename=@"%s" -F name=file "http%s://%s:%s"'%(path, 's' if use_TLS==True else '' ,str(IP_address), str(port_number)))
    mininet_node.cmdPrint('curl -k -i -X POST -F filename=@"%s" -F name=file "http%s://%s:%s"'%(path, 's' if use_TLS==True else '', str(IP_address), str(port_number)))
