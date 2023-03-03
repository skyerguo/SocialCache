import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import matplotlib as mpl
import math
mpl.rcParams['font.family'] = 'Times New Roman'
compare_data = {
    "TwitterFull": ['2023-02-10_17:00:08', '2023-02-10_16:45:13'],
    "Gowalla": ['2023-02-15_13:40:14', '2023-02-11_13:29:47']
}
methods = {
    "TwitterFull": ['SocialCache', 'LRU-Social'],
    "Gowalla": ['SocialCache', 'LRU']
}

def draw_flow(dataset):
    result_path = './figures/experiment_case_flow_%s.pdf'%(dataset)
    raw_data = {
        'Method': [],
        'Network Traffic Volume (GB)': [],
        'CDN Level': [],
    }
    
    for i in range(len(compare_data[dataset])):
        curr_path = './data/results/analyse_data/' + compare_data[dataset][i]
        f_in = open(curr_path, 'r')
        for line in f_in:
            if line[:5] == 'level' and 'media size' in line and 'node' in line:
                curr_level = int(line.split(';')[0].split(' ')[-1])
                curr_node = int(line.split(';')[1].split(' ')[-1])
                curr_media_size = float(line.split(';')[2].split(' ')[-1].strip()) / 1000000.0
                if curr_level == 1 or curr_media_size == 0:
                    continue
                    
                raw_data['Method'].append(methods[dataset][i])
                raw_data['Network Traffic Volume (GB)'].append(curr_media_size)
                raw_data['CDN Level'].append('All L%s CDN'%(4-curr_level))
        f_in.close()

    for i in range(len(compare_data[dataset])):
        curr_path = './data/results/analyse_data/' + compare_data[dataset][i]
        f_in = open(curr_path, 'r')
        for line in f_in:
            if line[:5] == 'level' and 'media size' in line and 'node' in line:
                curr_level = int(line.split(';')[0].split(' ')[-1])
                curr_node = int(line.split(';')[1].split(' ')[-1])
                curr_media_size = float(line.split(';')[2].split(' ')[-1].strip()) / 1000000.0
                if curr_level == 1 or curr_media_size == 0:
                    continue
                if (curr_level == 2 and (curr_node == 1 or curr_node == 3)) or (curr_level == 3 and (curr_node == 4 or curr_node == 3)):
                    curr_zone_type = 'Hot Zone'
                else:
                    curr_zone_type = 'Idle Zone'
                    
                if curr_zone_type == 'Hot Zone':
                    raw_data['Method'].append(methods[dataset][i])
                    raw_data['Network Traffic Volume (GB)'].append(curr_media_size)
                    raw_data['CDN Level'].append('Hot L%s CDN'%(4-curr_level))
        f_in.close()

    df = pd.DataFrame.from_dict(raw_data)
    mpl.rcParams['figure.figsize'] = (16, 9)
    plt.rcParams["font.size"] = 32
    
    g = sns.boxplot(x='CDN Level', y='Network Traffic Volume (GB)', hue='Method', width=0.5, linewidth=0.5, data=df)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.set_ylim(0)
    g.legend(loc='upper right', frameon=False, title=None, fontsize=26)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')
    
def draw_cache(dataset):
    result_path = './figures/experiment_case_cache_%s.pdf'%(dataset)
    raw_data = {
        'Method': [],
        'Cache Hit Ratio (%)': [],
        'CDN Level': [],
    }
    
    for i in range(len(compare_data[dataset])):
        curr_path = './data/results/analyse_data/' + compare_data[dataset][i]
        f_in = open(curr_path, 'r')
        for line in f_in:
            if line[:5] == 'level' and '缓存命中率' in line and 'node' in line:
                curr_level = int(line.split(';')[0].split(' ')[-1])
                curr_node = int(line.split(';')[1].split(' ')[-1])
                curr_cache_hit_ratio = float(line.split(';')[2].split(' ')[-1].strip()) * 100
                if curr_level == 1 or curr_cache_hit_ratio < 0:
                    continue
                    
                raw_data['Method'].append(methods[dataset][i])
                raw_data['Cache Hit Ratio (%)'].append(curr_cache_hit_ratio)
                raw_data['CDN Level'].append('All L%s CDN'%(4-curr_level))
        f_in.close()

    for i in range(len(compare_data[dataset])):
        curr_path = './data/results/analyse_data/' + compare_data[dataset][i]
        f_in = open(curr_path, 'r')
        for line in f_in:
            if line[:5] == 'level' and '缓存命中率' in line and 'node' in line:
                curr_level = int(line.split(';')[0].split(' ')[-1])
                curr_node = int(line.split(';')[1].split(' ')[-1])
                curr_cache_hit_ratio = float(line.split(';')[2].split(' ')[-1].strip()) * 100
                if curr_level == 1 or curr_cache_hit_ratio < 0:
                    continue
                if (curr_level == 2 and (curr_node == 1 or curr_node == 3)) or (curr_level == 3 and (curr_node == 4 or curr_node == 3)):
                    curr_zone_type = 'Hot Zone'
                else:
                    curr_zone_type = 'Idle Zone'
                    
                if curr_zone_type == 'Hot Zone':
                    raw_data['Method'].append(methods[dataset][i])
                    raw_data['Cache Hit Ratio (%)'].append(curr_cache_hit_ratio)
                    raw_data['CDN Level'].append('Hot L%s CDN'%(4-curr_level))
        f_in.close()

    df = pd.DataFrame.from_dict(raw_data)
    mpl.rcParams['figure.figsize'] = (16, 9)
    plt.rcParams["font.size"] = 32
    
    g = sns.boxplot(x='CDN Level', y='Cache Hit Ratio (%)', hue='Method', width=0.5, linewidth=0.5, data=df)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.set_ylim(0, 20, 4)
    # g.set_yscale()
    g.legend(loc='upper right', frameon=False, title=None, fontsize=26)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')

if __name__ == '__main__':
    # draw_flow('TwitterFull')
    # draw_cache('TwitterFull')