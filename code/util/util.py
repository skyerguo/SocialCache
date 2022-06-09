import math

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