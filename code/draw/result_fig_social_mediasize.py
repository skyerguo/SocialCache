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
    'CDN Level': [
        'L1 CDN', 'L1 CDN', 'L1 CDN', 'L1 CDN', 'L1 CDN',
        'L2 CDN', 'L2 CDN', 'L2 CDN', 'L2 CDN', 'L2 CDN', 
        'L3 CDN', 'L3 CDN', 'L3 CDN', 'L3 CDN', 'L3 CDN',
        'All', 'All', 'All', 'All', 'All'
    ],
    'OSN Connectivity Metric': [
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size', 
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size', 
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size', 
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size'
    ],
    'Network Traffic Volume (GB)': [
        33.324505, 33.437381, 33.474719, 33.429438, 33.296113,
        57.415569, 57.638458, 57.822382, 57.781147, 56.935121,
        26.052466, 26.162479, 26.309065, 26.313111, 25.600410, 
        116.792540, 117.238317, 117.606166, 117.523695, 115.831643, 
    ]
}
result_path = './figures/result_fig_social_mediasize.eps'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)

    mpl.rcParams['figure.figsize'] = (6, 5)
    # plt.  ["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 16
    # edgecolor_list = ["#cb364a", "#509a80", "#a05d46", "#5091c0", "#684e94"]
    edgecolor_list = ["#684e94", "#5091c0", "#a05d46", "#509a80", "#cb364a"]
    
    g = sns.barplot(x='CDN Level', y='Network Traffic Volume (GB)', hue='OSN Connectivity Metric', data=df, facecolor=(0, 0, 0, 0))
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    hatches = ['--', '**', 'xx', 'oo', '\\\\']
    for i,thisbar in enumerate(g.patches):
        thisbar.set_hatch(hatches[math.floor(i/4)])
        thisbar.set_edgecolor(edgecolor_list[math.floor(i/4)])
    g.legend(loc='upper left', frameon=False, title=None)

    plt.savefig(result_path, dpi=600, bbox_inches='tight', format='eps')