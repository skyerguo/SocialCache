from shapely.geometry import Point
import geopandas as gpd
# from geopandas import GeoDataFrame
import pandas as pd
import matplotlib.pyplot as plt
# import json
import csv
import os
# from usage.get_region_position import region2position as region2position

area_all = ['asia-east1','asia-east2','asia-northeast1','asia-northeast2','asia-northeast3','asia-south1','asia-south2','asia-southeast2','australia-southeast1','australia-southeast2','europe-central2','europe-north1','europe-west1','europe-west2','europe-west3','europe-west4','europe-west6','northamerica-northeast1','northamerica-northeast2','southamerica-east1','southamerica-west1','us-east1','us-east4','us-west1','us-west2','us-west3','us-west4']

def draw_all():
    region2position = {}
    geometry = []

    measure_path_name = 'data/static/measure.csv'
    position_path_name = 'data/static/position-gcp-list.csv'  

    with open(position_path_name, 'r') as csv_file:
        cnt_line = -1
        for line in csv_file:
            if cnt_line == -1:
                cnt_line += 1
                continue
            region = line.split(',')[0]
            latitude = line.split(',')[1]
            longitude = line.split(',')[2].strip()
            region2position[region] = {'longitude': longitude, 'latitude': latitude}

    with open('data/static/tmp_position.csv', 'w') as csv_writer:
        f_csv = csv.writer(csv_writer)
        f_csv.writerow(['longitude', 'latitude'])
        for area in area_all:
            f_csv.writerow([region2position[area]['longitude'], region2position[area]['latitude']])

    df = pd.read_csv('data/static/tmp_position.csv', delimiter=',', skiprows=0, low_memory=False)
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]

    gdf = gpd.GeoDataFrame(df, geometry=geometry)

    # this is a simple map that goes with geopandas
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    # if i != 0:
    #     last = gdf.plot(ax=last, marker='o', color=color_name[i], markersize=35, alpha=alpha[i])
    # else:
    last = gdf.plot(ax=world.plot(figsize=(10, 6)), marker='*', color='red', markersize=35,
                    alpha=1)

    # last.spines['top'].set_visible(False)
    # last.spines['right'].set_visible(False)
    # last.spines['bottom'].set_visible(False)
    # last.spines['left'].set_visible(False)
    # last.axes.xaxis.set_visible(False)
    # last.axes.yaxis.set_visible(False)
    last.set_xticks([])
    last.set_yticks([])
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    plt.savefig('figures/machine_distribution.pdf', dpi=600, bbox_inches='tight')

if __name__ == '__main__':
    draw_all()