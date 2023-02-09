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
        'RAND', 'FIFO', 'LRU', 'LRU-Social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-Social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-Social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-Social', 'SocialCache'
    ],
    'Network Traffic Volume (KB)': [
        135219910, 124954591, 124214721, 124075570, 115831643,
        32807150, 29475154, 28437740, 28417154, 25600410,
        66629254, 61496594, 61126659, 61057084, 56935121, 
        35783506, 33982842, 34650321, 34601332, 33296113
    ]
}
result_path = './figures/result_fig_method_mediasize.eps'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14
    edgecolor_list = ["#cb364a", "#509a80", "#a05d46", "#5091c0", "#684e94"]
    # print(df)
    g = sns.barplot(x='CDN Level', y='Network Traffic Volume (KB)', hue='Method', data=df, facecolor=(0, 0, 0, 0))
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    hatches = ['--', '**', 'xx', 'oo', '\\\\']
    for i,thisbar in enumerate(g.patches):
        thisbar.set_hatch(hatches[math.floor(i/4)])
        thisbar.set_edgecolor(edgecolor_list[math.floor(i/4)])
    g.legend(loc='upper right', frameon=False, title=None)

    plt.savefig(result_path, dpi=600, bbox_inches='tight', format='eps')