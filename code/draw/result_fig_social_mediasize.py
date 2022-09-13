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
    'OSN Connectivity Metric': [
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size', 
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size', 
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size', 
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size'
    ],
    'Media File Size (KB)': [
        116792540, 117238317, 117606166, 117523695, 115831643, 
        26052466, 26162479, 26309065, 26313111, 25600410, 
        57415569, 57638458, 57822382, 57781147, 56935121, 
        33324505, 33437381, 33474719, 33429438, 33296113
    ]
}
result_path = './figures/results/result_fig_social_mediasize.eps'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)

    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14
    edgecolor_list = ["#cb364a", "#509a80", "#a05d46", "#5091c0", "#684e94"]
    # print(df)
    g = sns.barplot(x='CDN Level', y='Media File Size (KB)', hue='OSN Connectivity Metric', data=df, facecolor=(0, 0, 0, 0))
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    hatches = ['--', '**', 'xx', 'oo', '\\\\']
    for i,thisbar in enumerate(g.patches):
        thisbar.set_hatch(hatches[math.floor(i/4)])
        thisbar.set_edgecolor(edgecolor_list[math.floor(i/4)])
    g.legend(loc='upper right', frameon=False, title=None)

    plt.savefig(result_path, dpi=600, bbox_inches='tight', format='eps')