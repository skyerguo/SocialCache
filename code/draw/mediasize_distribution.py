import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import matplotlib as mpl
import math

result_path = 'figures/mediasize_distribution.pdf'

def calc_mediasize(data_path):
    f_out = open(data_path, 'w')
    with open('data/traces/TwitterLarge/all_timeline.txt', 'r') as f_in:
        for line in f_in:
            current_type = line.split('+')[-1].strip()
            if current_type == "post":
                media_size = int(float(line.split('+')[1]))
                print(media_size, file=f_out)
    f_out.close()

def old():
    trace_data_path = "data/traces/TwitterLarge/mediasize.txt"
    if not os.path.exists(trace_data_path):
        calc_mediasize(trace_data_path)
    trace_data = np.loadtxt(trace_data_path, dtype='int')
    trace_data_dict = {'Media File Size (KB)': trace_data, 'Kind': ['Trace' for _ in range(len(trace_data))]}

    origin_data_path = 'code/util/media_size_sample/population'
    origin_data = np.loadtxt(origin_data_path, dtype='int') / 1024
    origin_data_dict = {'Media File Size (KB)': origin_data, 'Kind': ['Origin' for _ in range(len(origin_data))]}

    df1 = pd.DataFrame(origin_data_dict)
    df2 = pd.DataFrame(trace_data_dict)
    df = pd.concat([df1, df2]).reset_index()
    ## 弄成两列，一列是Size，另一列是对等长度的Kind

    mpl.rcParams['figure.figsize'] = (6, 5)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14

    g = sns.displot(data=df1, x="Media File Size (KB)", kind="kde", aspect=1.2)
    plt.xlim(0, 1000)
    # g.set(xticks=range(0,1000,100))
    plt.legend(["Origin Data"], loc='upper right', frameon=False, title=None)
    
    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')
    
def new():
    origin_data_path = 'code/util/media_size_sample/population'
    origin_data = np.loadtxt(origin_data_path, dtype='int') / 1024
    origin_data_dict = {'Media File Size (KB)': origin_data}
    df = pd.DataFrame(origin_data_dict)

    mpl.rcParams['figure.figsize'] = (16, 9)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 14

    ax = sns.kdeplot(data=df, x="Media File Size (KB)", shade=False, color='grey', cumulative=True, log_scale=True)
    kdeline = ax.lines[0]
    left, middle, right = np.percentile(origin_data, [10, 50, 90])
    xs = kdeline.get_xdata()
    ys = kdeline.get_ydata()
    y_left = np.interp(left, xs, ys)
    y_middle = np.interp(middle, xs, ys)
    y_right = np.interp(right, xs, ys)
    
    ax.vlines(middle, 0, np.interp(middle, xs, ys), color='crimson', ls=':', linewidth=2.5)
    ax.vlines(left, 0, np.interp(left, xs, ys), color='darkblue', ls=':', linewidth=1.5)
    ax.vlines(right, 0, np.interp(right, xs, ys), color='darkblue', ls=':', linewidth=1.5)
    ax.hlines(np.interp(middle, xs, ys), 0, middle, color='crimson', ls=':', linewidth=2.5)
    ax.hlines(np.interp(left, xs, ys), 0, left, color='darkblue', ls=':', linewidth=1.5)
    ax.hlines(np.interp(right, xs, ys), 0, right, color='darkblue', ls=':', linewidth=1.5)
    ax.fill_between(xs, 0, ys, facecolor='darkblue', alpha=0.2)
    ax.fill_between(xs, 0, ys, where=(left <= xs) & (xs <= right) & (y_left <= ys) & (ys <= y_right), interpolate=True, facecolor='crimson', alpha=0.2)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')

if __name__ == '__main__':
    # old()
    new()