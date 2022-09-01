import seaborn as sns
import matplotlib.pyplot as plt
import os
import json
import pandas as pd
import numpy as np
import math

raw_data = {
    'Cache Level': [
        'Total', 'Total', 'Total', 'Total', 'Total', 
        'Level 1', 'Level 1', 'Level 1', 'Level 1', 'Level 1', 
        'Level 2', 'Level 2', 'Level 2', 'Level 2', 'Level 2', 
        'Level 3', 'Level 3', 'Level 3', 'Level 3', 'Level 3'
    ],
    'OSN Graph Metric': [
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size', 
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size', 
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size', 
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size'
    ],
    'Media File Size (Bytes)': [
        451628224, 394841358, 398426694, 407055872, 449130290, 
        128287235, 121094999, 121978632, 126173682, 128059524, 
        219911132, 191517699, 193310367, 197624956, 218662165, 
        103429857, 82228660, 83137695, 83257234, 102408601
    ]
}
result_path = './figures/results/result_fig_social_mediasize.pdf'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14

    g = sns.barplot(x='Cache Level', y='Media File Size (Bytes)', hue='OSN Graph Metric', data=df)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)

    hatches = ['--', 'xx', '**', '\\\\', 'oo']
    for i,thisbar in enumerate(g.patches):
        thisbar.set_hatch(hatches[math.floor(i/4)])
    g.legend(loc='upper right', frameon=False, title=None)

    plt.savefig(result_path, dpi=600, bbox_inches='tight')