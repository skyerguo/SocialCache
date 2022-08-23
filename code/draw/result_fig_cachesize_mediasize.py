import seaborn as sns
import matplotlib.pyplot as plt
import os
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
    'Media File Size': [
        1, 1, 1, 1, 1,
        239039783, 201837418, 192775316, 232529916, 191517699, 
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1,
        232527771, 184766619, 133772036, 210210454, 130388305
    ]
}
result_path = './figures/results/result_fig_cachesize_mediasize.pdf'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    # print(df)
    sns.lineplot(x='Level 1 Cache Size', y='Media File Size', hue='Method', style='Method', data=df)
    plt.savefig(result_path, dpi=600, bbox_inches='tight')