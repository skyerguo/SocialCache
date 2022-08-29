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
    'Method': [
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocCache'
    ],
    'Media File Size': [
        239039783, 201837418, 192775316, 232529916, 191517699, 
        11805960, 11805960, 11805960, 11805960, 11805960,
        119884088, 103427828, 106807869, 118896903, 109289039, 
        107349735, 86603630, 74161487, 101827053, 70422700
    ]
}
result_path = './figures/results/result_fig_method_mediasize.pdf'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    plt.rcParams["font.family"] = "Times New Roman"
    # print(df)
    g = sns.barplot(x='Cache Level', y='Media File Size', hue='Method', data=df)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    plt.savefig(result_path, dpi=600, bbox_inches='tight')