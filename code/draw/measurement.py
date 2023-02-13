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
    'Latency': [
        
    ],
    'Bandwidth': [
        
    ],
    'Classification': [
        
    ]
}

def plot_distance_latency_linear():
    result_path = './figures/implementation_distance_latency_linear.pdf'
    df = pd.DataFrame.from_dict(distance_latency)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.size"] = 18
    
    y, X = dmatrices('Latency ~ Distance', data=df, return_type='dataframe')
    rlm_model = sm.RLM(y, X) #Robust linear regression model
    rlm_results = rlm_model.fit() 

    df.rename(columns = {'Latency' : 'Latency(ms)', 'Distance' : 'Geolocation Distance(km)'}, inplace = True)
    g = sns.regplot(x='Geolocation Distance(km)', y='Latency(ms)', marker='.', color='b', robust=True, line_kws={'label':"y={0:.3f}x+{1:.3f}".format(rlm_results.params[1],rlm_results.params[0]), 'color':'red'}, data=df)
    
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.legend(loc='upper right', frameon=False, title=None, fontsize=18)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')
    
    
def plot_distance_latency_log_log():
    result_path = './figures/implementation_distance_latency_log_log.pdf'
    df = pd.DataFrame.from_dict(distance_latency)
    df['Distance'] = np.log(df['Distance'])
    df['Latency'] = np.log(df['Latency'])
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.size"] = 18
    
    y, X = dmatrices('Latency ~ Distance', data=df, return_type='dataframe')
    rlm_model = sm.RLM(y, X) #Robust linear regression model
    rlm_results = rlm_model.fit() 

    df.rename(columns = {'Latency' : 'Latency(ms) - Log Scale', 'Distance' : 'Geolocation Distance(km) - Log Scale'}, inplace = True)
    g = sns.regplot(x='Geolocation Distance(km) - Log Scale', y='Latency(ms) - Log Scale', marker='.', color='b', robust=True, line_kws={'label':"y={0:.3f}x{1:.3f}".format(rlm_results.params[1],rlm_results.params[0]), 'color':'red'}, data=df)
    
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.legend(loc='upper right', frameon=False, title=None, fontsize=18)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')
    
def plot_distance_latency_pow():
    result_path = './figures/implementation_distance_latency_pow.pdf'
    df = pd.DataFrame.from_dict(distance_latency)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.size"] = 18
    
    a = 0.024
    b = 0.889
    x = np.linspace(0, 20000, 1000)
    y = a * pow(x, b)

    df.rename(columns = {'Latency' : 'Latency(ms)', 'Distance' : 'Geolocation Distance(km)'}, inplace = True)
    g = sns.scatterplot(x='Geolocation Distance(km)', y='Latency(ms)', marker='o', color='b', data=df)
    
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    plt.plot(x, y, color='red',label='$y=%.3fx^{%.3f}$'%(a,b),linewidth=1)
    plt.legend(loc='upper right', frameon=False, title=None, fontsize=18)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')
    
    
def plot_distance_bandwidth_linear():
    result_path = './figures/implementation_distance_bandwidth_linear.pdf'
    df = pd.DataFrame.from_dict(distance_bandwidth)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.size"] = 18
    
    y, X = dmatrices('Bandwidth ~ Distance', data=df, return_type='dataframe')
    rlm_model = sm.RLM(y, X) #Robust linear regression model
    rlm_results = rlm_model.fit() 

    df.rename(columns = {'Bandwidth' : 'Bandwidth(Mbps)', 'Distance' : 'Geolocation Distance(km)'}, inplace = True)
    g = sns.regplot(x='Geolocation Distance(km)', y='Bandwidth(Mbps)', marker='.', color='b', robust=True, line_kws={'label':"y={0:.3f}x+{1:.3f}".format(rlm_results.params[1],rlm_results.params[0]), 'color':'red'}, data=df)
    
    g.set_ylim(0)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.legend(loc='upper right', frameon=False, title=None, fontsize=18)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')
    

def plot_distance_bandwidth_log_log():
    result_path = './figures/implementation_distance_bandwidth_log_log.pdf'
    df = pd.DataFrame.from_dict(distance_bandwidth)
    df['Distance'] = np.log(df['Distance'])
    df['Bandwidth'] = np.log(df['Bandwidth'])
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.size"] = 18
    
    y, X = dmatrices('Bandwidth ~ Distance', data=df, return_type='dataframe')
    rlm_model = sm.RLM(y, X) #Robust linear regression model
    rlm_results = rlm_model.fit() 

    df.rename(columns = {'Bandwidth' : 'Bandwidth(Mbps) - Log Scale', 'Distance' : 'Geolocation Distance(km) - Log Scale'}, inplace = True)
    g = sns.regplot(x='Geolocation Distance(km) - Log Scale', y='Bandwidth(Mbps) - Log Scale', marker='.', color='b', robust=True, line_kws={'label':"y={0:.3f}x+{1:.3f}".format(rlm_results.params[1],rlm_results.params[0]), 'color':'red'}, data=df)
    
    g.set_ylim(0)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.legend(loc='upper right', frameon=False, title=None, fontsize=18)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')
    
    
def plot_distance_bandwidth_pow():
    result_path = './figures/implementation_distance_bandwidth_pow.pdf'
    df = pd.DataFrame.from_dict(distance_bandwidth)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.size"] = 18
    
    a = 228433.404
    b = -0.819
    x = np.linspace(60, 20000, 1000)
    y = a * pow(x, b)

    df.rename(columns = {'Bandwidth' : 'Bandwidth(Mbps)', 'Distance' : 'Geolocation Distance(km)'}, inplace = True)
    g = sns.scatterplot(x='Geolocation Distance(km)', y='Bandwidth(Mbps)', marker='o', color='b', data=df)
    
    g.set_ylim(0)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    plt.plot(x, y, color='red',label='$y=%.3fx^{%.3f}$'%(a,b),linewidth=3)
    plt.legend(loc='upper right', frameon=False, title=None, fontsize=18)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')
    
    
def plot_latency_bandwidth_linear():
    result_path = './figures/implementation_latency_bandwidth_linear.pdf'
    df = pd.DataFrame.from_dict(latency_bandwidth)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.size"] = 18
    
    y1, X1 = dmatrices('Bandwidth ~ Latency', data=df[df['Classification'] == 'Same Continent'], return_type='dataframe')
    rlm_model1 = sm.RLM(y1, X1) #Robust linear regression model
    rlm_results1 = rlm_model1.fit() 
    
    y2, X2 = dmatrices('Bandwidth ~ Latency', data=df[df['Classification'] == 'Different Continent'], return_type='dataframe')
    rlm_model2 = sm.RLM(y2, X2) #Robust linear regression model
    rlm_results2 = rlm_model2.fit() 

    df.rename(columns = {'Bandwidth' : 'Bandwidth(Mbps)', 'Latency' : 'Latency(ms)', 'Classification': 'Geolocation Classification'}, inplace = True)
    g = sns.lmplot(x='Latency(ms)', y='Bandwidth(Mbps)', hue='Geolocation Classification', markers=['.','+'], robust=True, data=df, legend=False)
    
    ax = g.axes[0, 0]
    ax.set_ylim(0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(loc='upper right', labels=["y={0:.3f}x+{1:.3f}".format(rlm_results1.params[1],rlm_results1.params[0]), "y={0:.3f}x+{1:.3f}".format(rlm_results2.params[1],rlm_results2.params[0])], frameon=False, title=None, fontsize=16)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')
    
def plot_latency_bandwidth_log_log():
    result_path = './figures/implementation_latency_bandwidth_log_log.pdf'
    df = pd.DataFrame.from_dict(latency_bandwidth)
    df['Latency'] = np.log(df['Latency'])
    df['Bandwidth'] = np.log(df['Bandwidth'])
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.size"] = 18
    
    y1, X1 = dmatrices('Bandwidth ~ Latency', data=df[df['Classification'] == 'Same Continent'], return_type='dataframe')
    rlm_model1 = sm.RLM(y1, X1) #Robust linear regression model
    rlm_results1 = rlm_model1.fit() 
    
    y2, X2 = dmatrices('Bandwidth ~ Latency', data=df[df['Classification'] == 'Different Continent'], return_type='dataframe')
    rlm_model2 = sm.RLM(y2, X2) #Robust linear regression model
    rlm_results2 = rlm_model2.fit() 

    df.rename(columns = {'Bandwidth' : 'Bandwidth(Mbps) - Log Scale', 'Latency' : 'Latency(ms) - Log Scale', 'Classification': 'Geolocation Classification'}, inplace = True)
    g = sns.lmplot(x='Latency(ms) - Log Scale', y='Bandwidth(Mbps) - Log Scale', hue='Geolocation Classification', markers=['.','+'], robust=True, data=df, legend=False)
    
    ax = g.axes[0, 0]
    ax.set_ylim(0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(loc='upper right', labels=["y={0:.3f}x+{1:.3f}".format(rlm_results1.params[1],rlm_results1.params[0]), "y={0:.3f}x+{1:.3f}".format(rlm_results2.params[1],rlm_results2.params[0])], frameon=False, title=None, fontsize=16)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')
    
def plot_latency_bandwidth_pow():
    result_path = './figures/implementation_latency_bandwidth_pow.pdf'
    df = pd.DataFrame.from_dict(latency_bandwidth)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.size"] = 18
    
    a1 = 21633.536
    b1 = -1.162
    x1 = np.linspace(1, 200, 200)
    y1 = a1 * pow(x1, b1)   
    
    a2 = 1155.167
    b2 = -0.287
    x2 = np.linspace(1, 200, 200)
    y2 = a2 * pow(x2, b2)   

    df.rename(columns = {'Bandwidth' : 'Bandwidth(Mbps)', 'Latency' : 'Latency(ms)', 'Classification': 'Geolocation Classification'}, inplace = True)
    g = sns.scatterplot(x='Latency(ms)', y='Bandwidth(Mbps)', hue='Geolocation Classification', markers=['o','+'], data=df, legend=False)
    
    g.set_ylim(0)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    plt.plot(x1, y1)
    plt.plot(x2, y2)
    plt.legend(loc='upper right', labels=['$y=%.3fx^{%.3f}$'%(a1,b1),'$y=%.3fx^{%.3f}$'%(a2,b2)], frameon=False, title=None, fontsize=16)

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
            
            if curr_distance > 0.001: #防止出现0
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
            
            if curr_distance > 0.001: #防止出现0
                distance_bandwidth['Distance'].append(curr_distance)
                distance_bandwidth['Bandwidth'].append(curr_bandwidth)
            
            latency_bandwidth['Latency'].append(curr_latency)
            latency_bandwidth['Bandwidth'].append(curr_bandwidth)
            latency_bandwidth['Classification'].append(curr_type)
            
    # plot_distance_latency_linear()
    # plot_distance_bandwidth_linear()
    # plot_distance_latency_log_log()
    # plot_distance_bandwidth_log_log()
    # plot_distance_latency_pow()
    # plot_distance_bandwidth_pow()
    
    # plot_latency_bandwidth_linear()
    # plot_latency_bandwidth_log_log()
    plot_latency_bandwidth_pow()