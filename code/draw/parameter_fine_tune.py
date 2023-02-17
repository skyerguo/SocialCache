import os
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
import numpy as np
import matplotlib as mpl
optimize_log_root_path = 'data/optimize/'
result_path = 'figures/parameter_fine_tune.pdf'
# mpl.rcParams['font.family'] = 'Times New Roman'
# mpl.rcParams['pdf.fonttype'] = 42
# mpl.rcParams['ps.fonttype'] = 42

optimize_log_name = {
    "PageRank": "optimize.log2023-02-13 18:30:09",
    "Authority": "optimize.log2023-02-13 18:41:20",
    "Clustering coefficient": "optimize.log2023-02-13 15:19:13",
    "Degree centrality": "optimize.log2023-02-13 15:22:09",
    "Betweenness centrality": "optimize.log2023-02-13 15:24:33",
    "Closeness centrality": "optimize.log2023-02-13 15:28:00",
    "Eigenvector centrality": "optimize.log2023-02-13 16:11:06",
    "Laplacian centrality": "optimize.log2023-02-13 19:00:25",
    "Ego betweenness centrality": "optimize.log2023-02-13 21:38:34",
    "Effective size": "optimize.log2023-02-13 16:19:33"
}

def fetch_data(max_len=0):
    df = pd.DataFrame()
    df_dict = {}
    for social_metric in optimize_log_name.keys():
        temp_iteration = []
        with open(optimize_log_root_path + optimize_log_name[social_metric], 'r') as f_in:
            for line in f_in:
                if "round" in line:
                    now = -1
                if "step" in line:
                    now += 1
                if "traffic" in line and "optimize" not in line:
                    curr_media_size = float(line.split(":")[1].strip()) / 1000000 # 转换为GB
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
    
    return df

if __name__ == '__main__':
    df = fetch_data(31)
    mpl.rcParams['figure.figsize'] = (16, 9)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 20
    # color_list = ["#684e94", "#5091c0", "#a05d46", "#509a80", "#cb364a"]

    # g = sns.lineplot(data=df, palette=color_list)
    g = sns.lineplot(data=df)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    plt.xlabel('Iterations', fontsize=20)
    plt.ylabel('Network Traffic Volume (GB)', fontsize=20)
    g.legend(loc='best', frameon=False, title=None, fontsize=10)
    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')