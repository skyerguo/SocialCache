import seaborn as sns
import matplotlib.pyplot as plt
import os
import json
import pandas as pd
import numpy as np

raw_data = {
    'Method': [
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache'
    ],
    'Timestamp': [
        1756.533695, 1448.979625, 1215.642967, 1889.90346, 1800.42668
    ]
}
result_path = './figures/results/result_fig_method_timestamp.pdf'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    # print(df)
    plt.rcParams["font.family"] = "Times New Roman"
    
    g = sns.barplot(x='Timestamp', y='Method', data=df)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    plt.savefig(result_path, dpi=600, bbox_inches='tight')