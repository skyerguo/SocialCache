import argparse
import os
import json
import math

data_root = '/proj/socnet-PG0/data/'

p = argparse.ArgumentParser(description='Analyze the result')
p.add_argument('-t', '--timestamp', type=str, default="", dest="timestamp", action="store", help="the timestamp of data file")
p.add_argument('-n', '--nearnumber', type=int, default=0, dest="nearNumber", action="store", help="the number of nearest timestamp")
p.add_argument('-d', '--detailoutput', default=False, dest="detailOutput", action="store_true", help="give more detail outputs")
args = p.parse_args()

data_root = '/proj/socnet-PG0/data/'
if args.timestamp:
    flow_path = data_root + args.timestamp + '/flow/'
else:
    files = os.listdir(data_root)
    files = sorted(files, reverse=True)
    flow_path = data_root + files[args.nearNumber] + '/flow/'
    
total_flow = 0
flow_each_level = [0 for _ in range(3)]
for ip_address in os.listdir(flow_path):
    curr_path = flow_path + ip_address + '/'
    curr_level = math.floor(int(ip_address.split('.')[-1]) / 2)
    for file_name in os.listdir(curr_path):
        for line in open(curr_path + file_name, 'r'):
            total_flow += int(line)
            flow_each_level[curr_level] += int(line)
print(total_flow)

if args.detailOutput:
    for i in range(3):
        print("level %s flow %s"%(str(i), flow_each_level[i]))