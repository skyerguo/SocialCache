import seaborn as sns
import matplotlib.pyplot as plt
import os
import json
import pandas as pd
import numpy as np
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
    'Media File Size (Bytes)': [
        4156979, 2445467, 2638787, 2613263, 2201197, 
        17310542, 13683042, 9479182, 16517546, 8456018,
        489575848, 415480796, 397356592, 481480978, 394841358 
    ]
}
result_path = './figures/results/result_fig_dataset_mediasize.pdf'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14

    g = sns.barplot(x='Dataset', y='Media File Size (Bytes)', hue="Method", data=df)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.set_yscale("log")
    g.set_ylim(1)

    hatches = ['--', 'xx', '**', '\\\\', 'oo']
    for i,thisbar in enumerate(g.patches):
        thisbar.set_hatch(hatches[math.floor(i/3)])
    g.legend(loc='upper left', frameon=False, title=None, ncol=2)

    plt.savefig(result_path, dpi=600, bbox_inches='tight')