import os
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
import numpy as np
result_path = 'figures/meidasize_distribution.pdf'

data_path = 'code/trace/media_size_sample/population'
test_data = np.loadtxt(data_path, dtype='int') 
df = pd.DataFrame(test_data, columns=['Media Size (Bytes)'])

if __name__ == '__main__':
    plt.rcParams["font.family"] = "Times New Roman"
    # print(df)
    # g = sns.lineplot(x='Level 1 Cache Size', y='Media File Size', hue='Method', style='Method', data=df)
    g = sns.histplot(data=df, x="Media Size (Bytes)", log_scale=True)
    g.set_xlim(1)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    plt.savefig(result_path, dpi=600, bbox_inches='tight')