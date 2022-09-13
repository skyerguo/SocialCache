import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import matplotlib as mpl
import math

raw_data = {
    'Dataset': [
        'Data-Alpha', 'Data-Alpha', 'Data-Alpha', 'Data-Alpha', 'Data-Alpha',
        'Data-Beta', 'Data-Beta', 'Data-Beta', 'Data-Beta', 'Data-Beta', 
        'Data-Gamma', 'Data-Gamma', 'Data-Gamma', 'Data-Gamma', 'Data-Gamma'
    ],
    'Method': [
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache', 
    ],
    'Media File Size (KB)': [
        3970424, 2214202, 2364660, 2363142, 1920556, 
        12015569, 8445286, 6949517, 6951902, 5966313,
        135219910, 124954591, 124214721, 124075570, 115831643,
    ]
}
result_path = './figures/results/result_fig_dataset_mediasize.eps'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14
    edgecolor_list = ["#cb364a", "#509a80", "#a05d46", "#5091c0", "#684e94"]
    
    g = sns.barplot(x='Dataset', y='Media File Size (KB)', hue='Method', data=df, facecolor=(0, 0, 0, 0))
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    hatches = ['--', '**', 'xx', 'oo', '\\\\']
    for i,thisbar in enumerate(g.patches):
        thisbar.set_hatch(hatches[math.floor(i/4)])
        thisbar.set_edgecolor(edgecolor_list[math.floor(i/4)])
    g.legend(loc='upper left', frameon=False, title=None)

    plt.savefig(result_path, dpi=600, bbox_inches='tight', format='eps')
