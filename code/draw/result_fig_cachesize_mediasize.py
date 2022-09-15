import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import matplotlib as mpl
import math

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
    'Network Traffic (KB)': [
        136898589, 129580451, 131342356, 131635447, 125001941,
        135938238, 126947334, 127377876, 127647782, 119575117, 
        135219910, 124954591, 124214721, 124075570, 115831643,
        134083708, 123257532, 121431983, 121566200, 112971637,
        133673496, 121799502, 119067295, 119203876, 110657800,
        129778995, 115897593, 109840942, 110220227, 102244003,
        126830329, 111121490, 103048312, 103268061, 96141512,
        124006822, 107198527, 97511786, 97726852, 90978330
    ]
}
result_path = './figures/results/result_fig_cachesize_mediasize.eps'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14

    g = sns.lineplot(x='L1 CDN Cache Size', y='Network Traffic (KB)', hue='Method', style='Method', data=df)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.set_ylim(0)
    g.legend(loc='lower left', frameon=False, title=None)

    plt.savefig(result_path, dpi=600, bbox_inches='tight', format='eps')