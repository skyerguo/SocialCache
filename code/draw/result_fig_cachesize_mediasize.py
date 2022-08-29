import os
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
import numpy as np

raw_data = {
    'Level 1 Cache Size': [
        5, 5, 5, 5, 5,
        10, 10, 10, 10, 10,
        20, 20, 20, 20, 20,
        50, 50, 50, 50, 50,
        100, 100, 100, 100, 100
    ],
    'Method': [
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocCache',
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocCache',
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocCache',
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocCache',
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocCache'
    ],
    'Media File Size': [ ## Level 1
        107579639, 88030325, 82564049, 104132987, 78867908,
        107349735, 86603630, 74161487, 101827053, 70422700, 
        106538623, 84837176, 64584126, 98767073, 62043814,
        104220906, 80609286, 49250184, 92234825, 48244556,
        101655824, 74832825, 35986053, 84831237, 35701844
    ]
}
result_path = './figures/results/result_fig_cachesize_mediasize.pdf'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    plt.rcParams["font.family"] = "Times New Roman"
    # print(df)
    g = sns.lineplot(x='Level 1 Cache Size', y='Media File Size', hue='Method', style='Method', data=df)

    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.set_ylim(0, 120000000)
    plt.savefig(result_path, dpi=600, bbox_inches='tight')