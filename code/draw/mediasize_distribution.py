import os
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
import numpy as np
result_path = 'figures/mediasize_distribution.pdf'

data_path = 'code/trace/media_size_sample/population'
test_data = np.loadtxt(data_path, dtype='int') 
df = pd.DataFrame(test_data, columns=['Media Size (Bytes)'])

if __name__ == '__main__':
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14 
    plt.figure(figsize=(10, 6))
    g = sns.histplot(data=df, x="Media Size (Bytes)", element="step", log_scale=True)
    # g.set_xlim(1)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    plt.savefig(result_path, dpi=600, bbox_inches='tight')