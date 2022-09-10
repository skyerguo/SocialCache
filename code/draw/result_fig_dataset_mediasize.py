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
        13072837, 10834993, 10019583, 10007388, 8491286,
        136898589, 129580451, 131342355, 131635447, 125001941 
    ]
}
result_path = './figures/results/result_fig_dataset_mediasize.pdf'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14
    edgecolor_list = ["#cb364a", "#509a80", "#a05d46", "#5091c0", "#684e94"]
    # print(df)
    g = sns.barplot(x='Dataset', y='Media File Size (KB)', hue='Method', data=df, facecolor=(0, 0, 0, 0))
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    hatches = ['--', '**', 'xx', 'oo', '\\\\']
    for i,thisbar in enumerate(g.patches):
        thisbar.set_hatch(hatches[math.floor(i/4)])
        thisbar.set_edgecolor(edgecolor_list[math.floor(i/4)])
    g.legend(loc='upper right', frameon=False, title=None)

    plt.savefig(result_path, dpi=600, bbox_inches='tight', format='eps')
