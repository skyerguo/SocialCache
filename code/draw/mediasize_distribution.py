import os
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
import numpy as np
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

trace_data_path = "data/traces/gtc_long_trace/mediasize.txt"
if not os.path.exists(trace_data_path):
    calc_mediasize(trace_data_path)
trace_data = np.loadtxt(trace_data_path, dtype='int')
trace_data_dict = {'Trace Media Size (KB)': trace_data}

origin_data_path = 'code/util/media_size_sample/population'
origin_data = np.loadtxt(origin_data_path, dtype='int') / 1024
origin_data_dict = {'Origin Media Size (KB)': origin_data}

# df1 = pd.DataFrame(origin_data, columns=['Origin Media Size (KB)'])
# df2 = pd.DataFrame(trace_data, columns=['Trace Media Size (KB)'])
df = pd.concat([])

if __name__ == '__main__':
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14 
    plt.figure(figsize=(10, 6))

    # g = sns.distplot(df1)
    # g = sns.distplot(df2)

    # g.set_xscale("log")

    # g = sns.histplot(data=df, x="Media Size (Bytes)", element="step", log_scale=False)
    # g.set_xlim(1)
    g.spines['top'].set_visible(False)
    g.spines['right'].set_visible(False)
    plt.savefig(result_path, dpi=600, bbox_inches='tight')