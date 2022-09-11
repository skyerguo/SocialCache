import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import matplotlib as mpl
import math

result_path = 'figures/mediasize_distribution.png'

def calc_mediasize(data_path):
    f_out = open(data_path, 'w')
    with open('data/traces/gtc_long_trace/all_timeline.txt', 'r') as f_in:
        for line in f_in:
            current_type = line.split('+')[-1].strip()
            if current_type == "post":
                media_size = int(float(line.split('+')[1]))
                print(media_size, file=f_out)
    f_out.close()

if __name__ == '__main__':
    trace_data_path = "data/traces/gtc_long_trace/mediasize.txt"
    if not os.path.exists(trace_data_path):
        calc_mediasize(trace_data_path)
    trace_data = np.loadtxt(trace_data_path, dtype='int')
    trace_data_dict = {'Media File Size (KB)': trace_data, 'Kind': ['Trace' for _ in range(len(trace_data))]}

    origin_data_path = 'code/util/media_size_sample/population'
    origin_data = np.loadtxt(origin_data_path, dtype='int') / 1024
    origin_data_dict = {'Media File Size (KB)': origin_data, 'Kind': ['Origin' for _ in range(len(origin_data))]}

    df1 = pd.DataFrame(origin_data_dict)
    df2 = pd.DataFrame(trace_data_dict)
    df = pd.concat([df1, df2])
    ## 弄成两列，一列是Size，另一列是对等长度的Kind

    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14

    g = sns.displot(data=df, x="Media File Size (KB)", hue="Kind", col="Kind", kind="kde")

    # g.set_xscale("log")
    # g.set_xlim(1)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    plt.savefig(result_path, dpi=600, bbox_inches='tight')