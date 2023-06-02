import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import matplotlib.cm as cm
import math
import csv
import groupstackbar
import random
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
temp_file_path = './figures/temp_data/experiment_service_network_traffic.csv'

def generate_dummy_data():
    with open(temp_file_path,'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(['Dataset', 'Method', 'CDN_Layer', 'Value'])
        for i in ['TwitterEgo', 'TwitterFull', 'Brightkite', 'Gowalla']: # 4 datasets
            for j in ['RAND', 'FIFO', 'LRU', 'LRU-Social', 'SocialCDN']: # 5 methods
                for k in ['L1 CDN Layer', 'L2 CDN Layer', 'Data Center Layer']:
                    csvwriter.writerow([i,j,k, int(random.random()*100)])


if __name__ == '__main__':
    df = pd.DataFrame.from_dict(raw_data)
    # df1 = df[df['Method'] == 'RAND']
    # df2 = df[df['Method'] == 'FIFO']
    # df3 = df[df['Method'] == 'LRU']
    # mpl.rcParams['figure.figsize'] = (16, 9)
    plt.rcParams["font.family"] = "Times New Roman"
    # plt.rcParams["font.size"] = 28
    color_list = ["#684e94", "#5091c0", "#a05d46", "#509a80", "#cb364a"]
    


    generate_dummy_data()

    f = groupstackbar.plot_grouped_stacks(temp_file_path, BGV=['Method', 'Dataset', 'CDN_Layer'], extra_space_on_top = 30)


    plt.savefig("./figures/output.png",dpi=500)
        

    # g.spines['top'].set_visible(False)
    # g.spines['right'].set_visible(False)
    # g.set_ylim(0)
    # g.legend(loc='lower left', frameon=False, title=None, fontsize=24)

    # plt.savefig(result_path, dpi=300, bbox_inches='tight', format='pdf')