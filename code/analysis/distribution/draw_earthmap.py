from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import pandas as pd
import matplotlib.pyplot as plt
import json
import csv
# from usage.get_geoip import area_pos as area_pos
from usage.get_region_position import region2position as region2position


def draw_server():
    path_name = ['machine_0522_us.json', 'machine_0522_europe.json', 'machine_0522_world.json']
    color_name = ['red', 'red', 'red']
    alpha = [1, 1, 1]
    for i in range(1, 2):
        data_root_path = 'machine_data/'
        machine_path = data_root_path + path_name[i]
        position_list = 'position-gcp-list.csv'

        machine_dict = json.load(open(machine_path, 'r'))

        with open(data_root_path + "tmp_position.csv", "w") as csv_writer:
            f_csv = csv.writer(csv_writer)
            f_csv.writerow(['Longitude', 'Latitude'])
            for index in machine_dict.keys():
                try:
                    region_name = machine_dict[index]['zone'].replace('-c', '')
                    print(region2position(region_name,position_list))
                    f_csv.writerow(region2position(region_name, position_list))
                except:
                    pass

        df = pd.read_csv(data_root_path + "tmp_position.csv", delimiter=',', skiprows=0, low_memory=False)

        geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
        gdf = GeoDataFrame(df, geometry=geometry)

        # this is a simple map that goes with geopandas
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        if i != 1:
            last = gdf.plot(ax=last, marker='o', color=color_name[i], markersize=35, alpha=alpha[i])
        else:
            last = gdf.plot(ax=world.plot(figsize=(10, 6)), marker='o', color=color_name[i], markersize=35, alpha=alpha[i])

    plt.xlabel('Longitude', fontsize=20)
    plt.ylabel('Latitude', fontsize=20)
    plt.title('Server Distribution', fontsize=32)
    plt.savefig('analysis/figure/position/server_all.svg', dpi=600, format='svg')
    plt.show()


def draw_client():
    path_name = ['client_gcp.txt', 'client_aws_hosts.json']
    color_name = ['red', 'orange']
    position_name = ['position-gcp-list.csv', 'position-aws-list.csv']
    alpha = [1, 0.6]
    for i in range(1, 2):
        data_root_path = 'machine_data/'
        machine_path = data_root_path + path_name[i]
        position_list = position_name[i]

        machine_dict = json.load(open(machine_path, 'r'))

        # client
        with open(data_root_path + "tmp_position.csv", "w") as csv_writer:
            f_csv = csv.writer(csv_writer)
            f_csv.writerow(['Longitude', 'Latitude'])
            for item in machine_dict:
                try:
                    if i == 0:
                        region_name = item.replace('-c', '')
                    elif i == 1:
                        region_name = item['region']
                    f_csv.writerow(region2position(region_name, position_list))
                except:
                    pass

        df = pd.read_csv(data_root_path + "tmp_position.csv", delimiter=',', skiprows=0, low_memory=False)

        geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
        gdf = GeoDataFrame(df, geometry=geometry)

        # this is a simple map that goes with geopandas
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        if i != 0:
            last = gdf.plot(ax=last, marker='o', color=color_name[i], markersize=35, alpha=alpha[i])
        else:
            last = gdf.plot(ax=world.plot(figsize=(10, 6)), marker='o', color=color_name[i], markersize=35,
                            alpha=alpha[i])

    plt.xlabel('Longitude', fontsize=20)
    plt.ylabel('Latitude', fontsize=20)
    plt.title('Client Distribution', fontsize=32)
    plt.savefig('analysis/figure/position/client_all.svg', dpi=600, format='svg')
    plt.show()


if __name__ == '__main__':
    draw_server()
    # draw_client()
