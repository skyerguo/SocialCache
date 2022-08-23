import seaborn as sns
import matplotlib.pyplot as plt
import os
import json
import pandas as pd
import numpy as np

raw_data = {
    'Cache Level': [
        'Total', 'Total', 'Total', 'Total', 'Total', 
        'Level 1', 'Level 1', 'Level 1', 'Level 1', 'Level 1', 
        'Level 2', 'Level 2', 'Level 2', 'Level 2', 'Level 2', 
        'Level 3', 'Level 3', 'Level 3', 'Level 3', 'Level 3'
    ],
    'Social Metric': [
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size', 
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size', 
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size', 
        'Degree', 'PageRank', 'Laplacian Centrality', 'Betweenness Centrality', 'Effective Size'
    ],
    'Media File Size': [
        6604517, 4028162, 4021697, 4358568, 6604460, 
        399694, 399694, 399694, 399694, 399694, 
        3901250, 2936652, 2972601, 3256040, 3883529, 
        2303573, 691816, 649402, 702834, 2321237
    ]
}
result_path = './figures/results/result_fig_social_mediasize.pdf'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    print(df)
    sns.catplot(x='Cache Level', y='Media File Size', hue='Social Metric', kind='bar', data=df)
    plt.savefig(result_path, dpi=600, bbox_inches='tight')