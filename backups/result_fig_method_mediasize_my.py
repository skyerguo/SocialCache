import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import matplotlib as mpl

raw_data = {
    'Cache Level': [
        'Total', 'Total', 'Total', 'Total', 'Total', 
        'Data Center', 'Data Center', 'Data Center', 'Data Center', 'Data Center'
        'L2 CDN', 'L2 CDN', 'L2 CDN', 'L2 CDN', 'L2 CDN', 
        'L1 CDN', 'L1 CDN', 'L1 CDN', 'L1 CDN', 'L1 CDN', 
    ],
    'Method': [
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache', 
        'RAND', 'FIFO', 'LRU', 'LRU-social', 'SocialCache'
    ],
    'Media File Size': [
        136898589, 129580451, 131342355, 131635447, 125001941, 
        33570281, 31150702, 31209857, 31385578, 28781628,
        67468594, 63809527, 64690477, 64837023, 61520270, 
        35859714, 34620225, 35442022, 35412846, 34700044
    ]
}
result_path = './figures/results/result_fig_method_mediasize.png'


mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

mpl.rcParams['figure.figsize'] = (6, 5)
colors = sns.color_palette('Paired')
colors[0] = 'k'
colors[1] = '#1E8449'
colors[2] = (0.2196078431372549, 0.4235294117647059, 0.6901960784313725)
colors[3] = (0.9411764705882353, 0.00784313725490196, 0.4980392156862745)
hatches = ['\\\\', 'xx',  '*']

dns = [7.194,67.96,115.77]
fastroute = [7.917,69.939,138.362]
polygon = [3.738,53.748,67.048]

xlabels = ['Delay', 'Bandwidth', 'CPU']
x = np.arange(len(xlabels))  # the label locations
width = 0.5  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, dns, width/2, 
                label='DNS-based', 
                edgecolor=colors[0], color='w')
rects2 = ax.bar(x, fastroute, width/2, 
                label='FastRoute', 
                edgecolor=colors[2], color='w')
rects3 = ax.bar(x + width/2, polygon, width/2, 
                label='Polygon', 
                edgecolor=colors[3], color='w')

for i, bars in enumerate([rects1, rects2, rects3]):
    labels = [f'{(v.get_height()):.2f}' for v in bars]
#     ax.bar_label(bars, labels=labels, label_type='edge',fontsize=21)
    for thisbar in bars.patches:
        # Set a different hatch for each bar
        thisbar.set_hatch(hatches[i])
    
plt.legend(loc='upper left',fontsize=22,ncol=1, 
#            handletextpad=0.1,columnspacing=0.1,
#            labelspacing=0.3,
#            bbox_to_anchor=(1.04, 1.07),
          frameon=False)
    
plt.yticks(fontsize=20)
plt.ylabel('Job Completion Time (second)',fontsize=23)
ax.set_xticks([0,1,2])
ax.set_xticklabels(xlabels,fontsize=22)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(result_path)
# plt.show()