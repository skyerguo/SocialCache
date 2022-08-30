import os
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
import numpy as np
result_path = 'figures/parameter_fine_tune.pdf'

data_path = 'code/optimize/optimize_trace.csv'
df = pd.read_csv(data_path)
df = df.fillna(method = 'ffill') # 使用前一列填充NAN
df = df.drop(['Unnamed: 0'], axis=1)  #删除a列

if __name__ == '__main__':
    plt.rcParams["font.family"] = "Times New Roman"
    g = sns.lineplot(data=df)
    # g.set_ylim(0) # 加了图有点丑
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    plt.savefig(result_path, dpi=600, bbox_inches='tight')