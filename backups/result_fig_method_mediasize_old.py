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
    'Method': [
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache'
    ],
    'Media File Size': [
        489575848, 415480796, 397356592, 481480978, 394841358, 
        131645946, 115233788, 118613829, 130161149, 121094999,
        238884944, 201837418, 192775316, 234837509, 191517699, 
        119044958, 98409590, 85967447, 116482320, 82228660
    ]
}
result_path = './figures/results/result_fig_method_mediasize.pdf'

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14
    # print(df)
    g = sns.barplot(x='Cache Level', y='Media File Size', hue='Method', data=df)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    hatches = ['--', 'xx', '**', '\\\\', 'oo']
    for i,thisbar in enumerate(g.patches):
        thisbar.set_hatch(hatches[math.floor(i/4)])
    g.legend(loc='upper right', frameon=False, title=None)

    plt.savefig(result_path, dpi=600, bbox_inches='tight')