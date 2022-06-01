from shapely.geometry import Point
import geopandas as gpd
# from geopandas import GeoDataFrame
import pandas as pd
# import matplotlib.pyplot as plt
# import json
# import csv
import os
# from usage.get_region_position import region2position as region2position

area_all = ['asia-east1','asia-east2','asia-northeast1','asia-northeast2','asia-northeast3','asia-south1','asia-south2','asia-southeast2','australia-southeast1','australia-southeast2','europe-central2','europe-north1','europe-west1','europe-west2','europe-west3','europe-west4','europe-west6','northamerica-northeast1','northamerica-northeast2','southamerica-east1','southamerica-west1','us-east1','us-east4','us-west1','us-west2','us-west3','us-west4']

def draw_all():
    # path_name = ['client_gcp.txt', 'client_aws_hosts.json']
    # color_name = ['red', 'orange']
    # alpha = [1, 0.6]
    region2position = {}
    geometry = []

    measure_path_name = '../../../data/static/measure.csv'
    position_path_name = '../../../data/static/position-gcp-list.csv'  

    with open(position_path_name, 'r') as csv_file:
        cnt_line = -1
        for line in csv_file:
            if cnt_line == -1:
                cnt_line += 1
                continue
            region = line.split(',')[0]
            longitude = line.split(',')[1]
            latitude = line.split(',')[2].strip()
            region2position[region] = {'longitude': longitude, 'latitude': latitude}
            geometry.append(zip(longitude, latitude))

    # with open(measure_path_name, 'r') as csv_file:

    # for i in range(1, 2):
    #     data_root_path = 'machine_data/'
    #     machine_path = data_root_path + path_name[i]
    #     position_list = position_name[i]

    #     machine_dict = json.load(open(machine_path, 'r'))

    #     # client

    # with open(data_root_path + "tmp_position.csv", "w") as csv_writer:
    #     f_csv = csv.writer(csv_writer)
    #     f_csv.writerow(['Longitude', 'Latitude'])
    #     for item in machine_dict:
    #         try:
    #             if i == 0:
    #                 region_name = item.replace('-c', '')
    #             elif i == 1:
    #                 region_name = item['region']
    #             f_csv.writerow(region2position(region_name, position_list))
    #         except:
    #             pass

    # df = pd.read_csv(data_root_path + "tmp_position.csv", delimiter=',', skiprows=0, low_memory=False)

    # geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]

    properties = {}     # 定义 properties
    properties['City'] = ['GD']  # 如果后面要再添加数据，就用properties['City'].append()
    properties['Country'] = ['CN'] 
    df = pd.DataFrame(properties)  
    # df['geometry'] = geometry

    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    exit()

    # this is a simple map that goes with geopandas
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    # if i != 0:
    #     last = gdf.plot(ax=last, marker='o', color=color_name[i], markersize=35, alpha=alpha[i])
    # else:
    last = gdf.plot(ax=world.plot(figsize=(10, 6)), marker='o', color=color_name[i], markersize=35,
                    alpha=alpha[i])

    plt.xlabel('Longitude', fontsize=20)
    plt.ylabel('Latitude', fontsize=20)
    plt.title('Client Distribution', fontsize=32)
    # plt.savefig('analysis/figure/position/client_all.svg', dpi=600, format='svg')
    plt.show()

if __name__ == '__main__':
    # draw_server()
    # draw_client()
    draw_all()