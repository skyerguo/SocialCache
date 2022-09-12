import os
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
import numpy as np
import matplotlib as mpl
result_path = 'figures/parameter_fine_tune.eps'

optimize_log_name = {
    "Degree": "optimize.log2022-09-08 22:04:57",
    "Pagerank": "optimize.log2022-09-09 10:26:24",
    "LaplacianCentrality": "optimize.log2022-09-09 11:29:30",
    "BetweennessCentrality": "optimize.log2022-09-09 12:48:51",
    "EffectiveSize": "optimize.log2022-09-09 13:44:49"
}

def fetch_data(max_len=0):
    df = pd.DataFrame()
    df_dict = {}
    for social_metric in optimize_log_name.keys():
        temp_iteration = []
        with open(optimize_log_name[social_metric], 'r') as f_in:
            for line in f_in:
                if "round" in line:
                    now = -1
                if "step" in line:
                    now += 1
                if "traffic" in line and "optimize" not in line:
                    curr_media_size = float(line.split(":")[1].strip())
                    if now >= len(temp_iteration):
                        temp_iteration.append(curr_media_size)
                        if now > 0:
                            temp_iteration[now] = min(temp_iteration[now], temp_iteration[now-1])
                    else:
                        temp_iteration[now] = min(temp_iteration[now], curr_media_size)
        if max_len > 0 and len(temp_iteration) > max_len:
            temp_iteration = temp_iteration[:max_len]
        df_dict[social_metric] = temp_iteration
        
    df = pd.DataFrame.from_dict(dict([(k,pd.Series(v)) for k,v in df_dict.items()]))
    df = df.fillna(method = 'ffill') # 使用前一列填充NAN
    # print(df)
    return df
    

# data_path = 'code/optimize/optimize_trace.csv'
# df = pd.read_csv(data_path)
# df = df.fillna(method = 'ffill') # 使用前一列填充NAN
# df = df.drop(['Unnamed: 0'], axis=1)  #删除a列

if __name__ == '__main__':
    df = fetch_data(161)
    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14
    g = sns.lineplot(data=df)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    g.legend(loc='upper right', frameon=False, title=None)
    plt.savefig(result_path, dpi=600, bbox_inches='tight', format='eps')