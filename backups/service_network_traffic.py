import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import matplotlib.cm as cm
import math
# mpl.rcParams['font.family'] = 'Times New Roman'
# mpl.rcParams['pdf.fonttype'] = 42
# mpl.rcParams['ps.fonttype'] = 42

raw_data = {
    'Dataset': [
        'TwitterEgo', 'TwitterEgo', 'TwitterEgo', #'TwitterEgo',
        'TwitterEgo', 'TwitterEgo', 'TwitterEgo', #'TwitterEgo',
        'TwitterEgo', 'TwitterEgo', 'TwitterEgo', #'TwitterEgo',
        'TwitterEgo', 'TwitterEgo', 'TwitterEgo', #'TwitterEgo',
        'TwitterEgo', 'TwitterEgo', 'TwitterEgo', #'TwitterEgo',
        
        'TwitterFull', 'TwitterFull', 'TwitterFull', #'TwitterFull',
        'TwitterFull', 'TwitterFull', 'TwitterFull', #'TwitterFull',
        'TwitterFull', 'TwitterFull', 'TwitterFull', #'TwitterFull',
        'TwitterFull', 'TwitterFull', 'TwitterFull', #'TwitterFull',
        'TwitterFull', 'TwitterFull', 'TwitterFull', #'TwitterFull',
        
        'Brightkite', 'Brightkite', 'Brightkite', #'Brightkite',
        'Brightkite', 'Brightkite', 'Brightkite', #'Brightkite',
        'Brightkite', 'Brightkite', 'Brightkite', #'Brightkite',
        'Brightkite', 'Brightkite', 'Brightkite', #'Brightkite',
        'Brightkite', 'Brightkite', 'Brightkite', #'Brightkite',
        
        'Gowalla', 'Gowalla', 'Gowalla', #'Gowalla',
        'Gowalla', 'Gowalla', 'Gowalla', #'Gowalla',
        'Gowalla', 'Gowalla', 'Gowalla', #'Gowalla',
        'Gowalla', 'Gowalla', 'Gowalla', #'Gowalla',
        'Gowalla', 'Gowalla', 'Gowalla'#, 'Gowalla'
    ],
    'CDN Layer': [
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer', #'ALL',
        'L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer'#, 'ALL'
    ],
    'Method': [
        'RAND', 'RAND', 'RAND', #'RAND',
        'FIFO', 'FIFO', 'FIFO', #'FIFO',
        'LRU', 'LRU', 'LRU', #'LRU',
        'LRU-Social', 'LRU-Social', 'LRU-Social', #'LRU-Social',
        'SocialCache', 'SocialCache', 'SocialCache', #'SocialCache',
        
        'RAND', 'RAND', 'RAND', #'RAND',
        'FIFO', 'FIFO', 'FIFO', #'FIFO',
        'LRU', 'LRU', 'LRU', #'LRU',
        'LRU-Social', 'LRU-Social', 'LRU-Social', #'LRU-Social',
        'SocialCache', 'SocialCache', 'SocialCache', #'SocialCache',
        
        'RAND', 'RAND', 'RAND', #'RAND',
        'FIFO', 'FIFO', 'FIFO', #'FIFO',
        'LRU', 'LRU', 'LRU', #'LRU',
        'LRU-Social', 'LRU-Social', 'LRU-Social', #'LRU-Social',
        'SocialCache', 'SocialCache', 'SocialCache', #'SocialCache',
        
        'RAND', 'RAND', 'RAND', #'RAND',
        'FIFO', 'FIFO', 'FIFO', #'FIFO',
        'LRU', 'LRU', 'LRU', #'LRU',
        'LRU-Social', 'LRU-Social', 'LRU-Social', #'LRU-Social',
        'SocialCache', 'SocialCache', 'SocialCache'#, 'SocialCache'
        
    ],
    'Network Traffic Volume (GB)': [
        3.50, 5.91, 2.60, #12.02,
        3.01, 4.13, 1.31, #8.45,
        2.94, 3.38, 0.63, #6.95,
        2.94, 3.38, 0.63, #6.95,
        2.46, 2.89, 0.61, #5.97,
        
        35.78, 66.63, 32.81, #135.22,
        33.98, 61.50, 29.48, #124.96,
        34.65, 61.12, 28.43, #124.22,
        34.60, 61.06, 28.42, #124.08,
        33.24, 56.92, 25.64, #115.80,
        
        170.27, 287.85, 143.18, #601.29,
        98.23, 107.23, 34.60, #240.06,
        94.21, 103.21, 34.60, #232.02, 
        126.75, 180.50, 79.35, #386.60,
        91.88, 100.87, 34.59, #227.35,
        
        119.17, 176.98, 88.27, #384.42,
        95.50, 95.72, 30.67, #221.90,
        92.47, 92.69, 30.67, #215.83,
        100.98, 124.95, 54.42, #280.35,
        88.33, 88.55, 30.67#, 207.54
    ]
}
result_path = './figures/experiment_service_network_traffic.pdf'

def plot_clustered_stacked(dfall, labels=None, title="multiple stacked bar plot",  H="/", **kwargs):
    """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot. 
    labels is a list of the names of the dataframe, used for the legend
    title is a string for the title of the plot
    H is the hatch used for identification of the different dataframe"""

    n_df = len(dfall)
    n_col = len(dfall[0]['Dataset'].drop_duplicates()) 
    n_ind = len(dfall[0]['CDN Layer'].drop_duplicates())
    axe = plt.subplot(111)
    

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      x='Dataset',
                      y='Network Traffic Volume (GB)',
                      linewidth=0,
                      stacked=True,
                      ax=axe,
                      legend=False,
                      grid=False,
                      **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                rect.set_hatch(H * int(i / n_col)) #edited part     
                rect.set_width(1 / float(n_df + 1))

    # axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    # axe.set_xticklabels(dfall[0]['Dataset'].drop_duplicates(), rotation = 0)
    # axe.set_title(title)

    # Add invisible data to add another legend
    n=[]        
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

    l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
    if labels is not None:
        l2 = plt.legend(n, labels, loc=[1.01, 0.1]) 
    axe.add_artist(l1)
    return axe

if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    # df1 = df[df['Method'] == 'RAND']
    # df2 = df[df['Method'] == 'FIFO']
    # df3 = df[df['Method'] == 'LRU']
    df1 = pd.DataFrame(np.random.rand(4, 5),
                   index=["A", "B", "C", "D"],
                   columns=["I", "J", "K", "L", "M"])
    df2 = pd.DataFrame(np.random.rand(4, 5),
                    index=["A", "B", "C", "D"],
                    columns=["I", "J", "K", "L", "M"])
    df3 = pd.DataFrame(np.random.rand(4, 5),
                    index=["A", "B", "C", "D"], 
                    columns=["I", "J", "K", "L", "M"])
    mpl.rcParams['figure.figsize'] = (16, 9)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 28
    color_list = ["#684e94", "#5091c0", "#a05d46", "#509a80", "#cb364a"]
    
    plot_clustered_stacked([df1, df2, df3],
                       ["df1", "df2", "df3"],
                       cmap=plt.cm.viridis)
    
    

    # g.spines['top'].set_visible(False)
    # g.spines['right'].set_visible(False)
    # g.set_ylim(0)
    # g.legend(loc='lower left', frameon=False, title=None, fontsize=24)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')