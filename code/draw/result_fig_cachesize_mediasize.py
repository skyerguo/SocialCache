import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import matplotlib as mpl
import math
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

raw_data = {
    'L1 CDN Cache Size': [
        5, 5, 5, 5, 5,
        10, 10, 10, 10, 10,
        15, 15, 15, 15, 15,
        20, 20, 20, 20, 20,
        25, 25, 25, 25, 25,
        50, 50, 50, 50, 50,
        75, 75, 75, 75, 75,
        100, 100, 100, 100, 100
    ],
    'Method': [
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache',
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache',
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache',
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache',
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache',
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache',
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache',
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache'
    ],
    'Network Traffic Volume (GB)': [
        136.898589, 129.580451, 131.342356, 131.635447, 125.001941,
        135.938238, 126.947334, 127.377876, 127.647782, 119.575117, 
        135.219910, 124.954591, 124.214721, 124.075570, 115.831643,
        134.083708, 123.257532, 121.431983, 121.566200, 112.971637,
        133.673496, 121.799502, 119.067295, 119.203876, 110.657800,
        129.778995, 115.897593, 109.840942, 110.220227, 102.244003,
        126.830329, 111.121490, 103.048312, 103.268061, 96.141512,
        124.006822, 107.198527, 97.511786, 97.726852, 90.978330
    ]
}
result_path = './figures/result_fig_cachesize_mediasize.eps'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    mpl.rcParams['figure.figsize'] = (6, 5)
    # plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 16
    color_list = ["#684e94", "#5091c0", "#a05d46", "#509a80", "#cb364a"]
    
    g = sns.lineplot(x='L1 CDN Cache Size', y='Network Traffic Volume (GB)', hue='Method', style='Method', palette=color_list, data=df)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.set_ylim(0)
    g.legend(loc='lower left', frameon=False, title=None)

    plt.savefig(result_path, dpi=600, bbox_inches='tight', format='eps')