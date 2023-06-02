import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import matplotlib.cm as cm
import math
import copy
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

def cumulate_raw():
    res = copy.deepcopy(raw_data)
    for i in range(len(raw_data['Network Traffic Volume (GB)'])):
        if i % 3 == 1 or i % 3 == 2:
            res['Network Traffic Volume (GB)'][i] = res['Network Traffic Volume (GB)'][i] + res['Network Traffic Volume (GB)'][i - 1]
    return res

if __name__ == '__main__':
    # mpl.rcParams['figure.figsize'] = (20, 9)
    plt.rcParams["font.family"] = "Times New Roman"
    # plt.rcParams["font.size"] = 28
    
    color_list = ["#684e94", "#5091c0", "#a05d46", "#509a80", "#cb364a"]
    
    # cumulated_raw_data = cumulate_raw()
    # df = pd.DataFrame.from_dict(cumulated_raw_data)
    
    # g = sns.FacetGrid(df, col="Dataset", hue='CDN Layer', palette=color_list, col_wrap=4)
    # g = (g.map(sns.barplot, 'Method', 'Network Traffic Volume (GB)', ci = None).add_legend())
    # for axes in g.axes.flat:
    #     axes.set_xticklabels(axes.get_xticklabels(), rotation=65)
    
    data = pd.DataFrame.from_dict(raw_data)
    
    number_columns = len(data['Dataset'].unique())
    fig, axes = plt.subplots(nrows=1, ncols=number_columns, figsize=(15,6))
    
    for curr_dataset_name,ax in zip(data['Dataset'].unique(), axes):
        df = data[data.Dataset==curr_dataset_name].groupby(['Method','CDN Layer'])['Network Traffic Volume (GB)'].sum()
        df.unstack().plot.bar(ax=ax, stacked=True)
    # ax_position = 0
    # for dataset in df['Dataset'].unique():
    #     idx = pd.IndexSlice
        
        
    #     # subset = df[df['Dataset'] == dataset]
    #     # ax = sns.barplot(data=subset, x='Method', y='Network Traffic Volume (GB)', hue='CDN Layer', ci=None, ax=axes[ax_position])
        
    #     subset = df[df['Dataset'] == dataset]
    #     subdf = pd.DataFrame({'Method': subset['Method'].unique()})
    #     subdf.set_index('Method')
    #     for CDN_layer_name in subset['CDN Layer'].unique():
    #         traffic = []
    #         for method_name in subset['Method'].unique():
    #             traffic.append(subset[(subset["CDN Layer"] == CDN_layer_name) & (subset["Method"] == method_name)]['Network Traffic Volume (GB)'])
    #         subdf.loc[:,CDN_layer_name] = traffic
    #     ax = subdf.plot(kind="bar", stacked=True, ax=axes[ax_position])
        
    #     ax.set_title(dataset, fontsize=30, alpha=1.0)
    #     ax.set_ylim(0, 600)
    #     ax.set_ylabel('Network Traffic Volume (GB)', fontsize=18),
    #     ax.set_xlabel('Method', fontsize=30, alpha=0.0),
    #     ax.set_yticklabels(ax.get_yticklabels(), rotation=0, minor=False, fontsize=18)
    #     ax.set_xticklabels(ax.get_xticklabels(), rotation=65, fontsize=18)
    #     ax_position += 1
        
    # # plt.tight_layout(pad=0., w_pad=-16.5, h_pad=0.0)
    # for i in range(number_columns - 1):
    #     axes[i].legend().set_visible(False)
    # for i in range(1, number_columns):
    #     axes[i].set_ylabel("")
    #     axes[i].set_yticklabels("")
    plt.savefig('./figures/output.png', dpi=300, bbox_inches='tight')
    exit(0)

    

    # g.spines['top'].set_visible(False)
    # g.spines['right'].set_visible(False)
    # g.set_ylim(0)
    # g.legend(loc='lower left', frameon=False, title=None, fontsize=24)

    plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')