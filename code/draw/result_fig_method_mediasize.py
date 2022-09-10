import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import matplotlib as mpl
import math

raw_data = {
    'CDN Level': [
        'Total', 'Total', 'Total', 'Total', 'Total', 
        'Data Center', 'Data Center', 'Data Center', 'Data Center', 'Data Center',
        'L2 CDN', 'L2 CDN', 'L2 CDN', 'L2 CDN', 'L2 CDN', 
        'L1 CDN', 'L1 CDN', 'L1 CDN', 'L1 CDN', 'L1 CDN'
    ],
    'Method': [
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache'
    ],
    'Media File Size (KB)': [
        136898589, 129580451, 131342355, 131635447, 125001941, 
        33570281, 31150702, 31209857, 31385578, 28781628,
        67468594, 63809527, 64690477, 64837023, 61520270, 
        35859714, 34620225, 35442022, 35412846, 34700044
    ]
}
result_path = './figures/results/result_fig_method_mediasize.eps'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14
    edgecolor_list = ["#cb364a", "#509a80", "#a05d46", "#5091c0", "#684e94"]
    # print(df)
    g = sns.barplot(x='CDN Level', y='Media File Size (KB)', hue='Method', data=df, facecolor=(0, 0, 0, 0))
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    hatches = ['--', '**', 'xx', 'oo', '\\\\']
    for i,thisbar in enumerate(g.patches):
        thisbar.set_hatch(hatches[math.floor(i/4)])
        thisbar.set_edgecolor(edgecolor_list[math.floor(i/4)])
    g.legend(loc='upper right', frameon=False, title=None)

    plt.savefig(result_path, dpi=600, bbox_inches='tight', format='eps')