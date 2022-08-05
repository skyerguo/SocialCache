import argparse
import os
import json

data_root = '/proj/socnet-PG0/data/'

p = argparse.ArgumentParser(description='Analyze the result')
p.add_argument('-t', '--timestamp', type=str, default="", dest="timestamp", action="store", help="the timestamp of data file")
p.add_argument('-n', '--nearnumber', type=int, default=0, dest="nearNumber", action="store", help="the number of nearest timestamp")
args = p.parse_args()

data_root = '/proj/socnet-PG0/data/'
if args.timestamp:
    flow_path = data_root + args.timestamp + '/flow/'
else:
    files = os.listdir(data_root)
    files = sorted(files, reverse=True)
    flow_path = data_root + files[args.nearNumber] + '/flow/'
    
total_flow = 0
for ip_address in os.listdir(flow_path):
    curr_path = flow_path + ip_address + '/'
    for file_name in os.listdir(curr_path):
        for line in open(curr_path + file_name, 'r'):
            total_flow += int(line)
print(total_flow)