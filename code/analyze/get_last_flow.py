import argparse
import os
import json

data_root = '/proj/socnet-PG0/data/'
files = os.listdir(data_root)
files = sorted(files, reverse=True)
flow_path = data_root + files[0] + '/flow/'

total_flow = 0
for ip_address in os.listdir(flow_path):
    curr_path = flow_path + ip_address + '/'
    for file_name in os.listdir(curr_path):
        for line in open(curr_path + file_name, 'r'):
            total_flow += int(line)
print(total_flow)