import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import matplotlib as mpl
import math
import code.util.util as util
import statsmodels.api as sm
from patsy import dmatrices

mpl.rcParams['font.family'] = 'Times New Roman'
# mpl.rcParams['pdf.fonttype'] = 42
# mpl.rcParams['ps.fonttype'] = 42

area_all = ['asia-east1','asia-east2','asia-northeast1','asia-northeast2','asia-northeast3','asia-south1','asia-south2','asia-southeast2','australia-southeast1','australia-southeast2','europe-central2','europe-north1','europe-west1','europe-west2','europe-west3','europe-west4','europe-west6','northamerica-northeast1','northamerica-northeast2','southamerica-east1','southamerica-west1','us-east1','us-east4','us-west1','us-west2','us-west3','us-west4']

measure_path_name = 'data/static/measure.csv'
position_path_name = 'data/static/position-gcp-list.csv'  

distance_latency = {
    'Distance': [
        
    ],
    'Latency': [
        
    ]
}

distance_bandwidth = {
    'Distance': [
        
    ],
    'Bandwidth': [
        
    ]
}

latency_bandwidth = {
    'Latency(ms)': [
        
    ],
    'Bandwidth(Mbps)': [
        
    ],
    'Geolocation Classification': [
        
    ]
}

def plot_distance_latency():
    result_path = './figures/implementation_distance_latency.pdf'
    df = pd.DataFrame.from_dict(distance_latency)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.size"] = 14
    
    y, X = dmatrices('Latency ~ Distance', data=df, return_type='dataframe')
    rlm_model = sm.RLM(y, X) #Robust linear regression model
    rlm_results = rlm_model.fit() 

    df.rename(columns = {'Latency' : 'Latency(ms)', 'Distance' : 'Geolocation Distance(km)'}, inplace = True)
    g = sns.regplot(x='Geolocation Distance(km)', y='Latency(ms)', marker='.', color='b', robust=True, line_kws={'label':"y={0:.3f}x+{1:.3f}".format(rlm_results.params[1],rlm_results.params[0])}, data=df)
    
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.legend(loc='upper right', frameon=False, title=None, fontsize=14)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')
    
def plot_distance_bandwidth():
    result_path = './figures/implementation_distance_bandwidth.pdf'
    df = pd.DataFrame.from_dict(distance_bandwidth)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.size"] = 14
    
    y, X = dmatrices('Bandwidth ~ Distance', data=df, return_type='dataframe')
    rlm_model = sm.RLM(y, X) #Robust linear regression model
    rlm_results = rlm_model.fit() 

    df.rename(columns = {'Bandwidth' : 'Bandwidth(Mbps)', 'Distance' : 'Geolocation Distance(km)'}, inplace = True)
    g = sns.regplot(x='Geolocation Distance(km)', y='Bandwidth(Mbps)', marker='.', color='b', robust=True, line_kws={'label':"y={0:.3f}x+{1:.3f}".format(rlm_results.params[1],rlm_results.params[0])}, data=df)
    
    g.set_ylim(0)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.legend(loc='upper right', frameon=False, title=None, fontsize=14)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')

if __name__ == '__main__':
    region2position = {}
    with open(position_path_name, 'r') as csv_file:
        cnt_line = -1
        for line in csv_file:
            if cnt_line == -1:
                cnt_line += 1
                continue
            region = line.split(',')[0]
            latitude = line.split(',')[1]
            longitude = line.split(',')[2].strip()
            region2position[region] = {'lon': longitude, 'lat': latitude}
    # print(region2position.keys())

    with open(measure_path_name, 'r') as f_in:
        for line in f_in:
            # print(line)
            area1 = line.split(',')[0][:-2]
            area2 = line.split(',')[1][7:-2]
            if area1.split('-')[0] == area2.split('-')[0] or \
            (area1.split('-')[0] == 'us' and area2.split('-')[0] == 'northamerica') or \
            (area1.split('-')[0] == 'northamerica' and area2.split('-')[0] == 'us'):
                curr_type = "Same Continent"
            else:
                curr_type = "Different Continent"
            curr_distance = util.calc_geolocation_distance(region2position[area1],region2position[area2])
            curr_latency = float(line.split(',')[2]) / 2
            
            distance_latency['Distance'].append(curr_distance)
            distance_latency['Latency'].append(curr_latency)
            
            curr_bandwidth = line.split(',')[3].strip()
            if not curr_bandwidth:
                continue
            elif 'Mb' in curr_bandwidth:
                curr_bandwidth = float(curr_bandwidth.split('_')[0])
            elif 'Gb' in curr_bandwidth:
                line[3] = float(curr_bandwidth.split('_')[0]) * 1000
            elif 'Kb' in curr_bandwidth:
                line[3] = float(curr_bandwidth.split('_')[0]) / 1000
                
            distance_bandwidth['Distance'].append(curr_distance)
            distance_bandwidth['Bandwidth'].append(curr_bandwidth)
            
    # plot_distance_latency()
    plot_distance_bandwidth()
    
