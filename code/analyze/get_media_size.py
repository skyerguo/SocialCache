import argparse
import os
import json
import math

p = argparse.ArgumentParser(description='Analyze the result')
p.add_argument('-t', '--timestamp', type=str, default="", dest="timestamp", action="store", help="the timestamp of data file")
p.add_argument('-n', '--nearnumber', type=int, default=0, dest="nearNumber", action="store", help="the number of nearest timestamp")
p.add_argument('-d', '--detailoutput', default=False, dest="detailOutput", action="store_true", help="give more detail outputs")
args = p.parse_args()

data_root = '/proj/socnet-PG0/data/'
if args.timestamp:
    experiment_path = data_root + args.timestamp
else:
    files = os.listdir(data_root)
    files = sorted(files, reverse=True)
    experiment_path = data_root + files[args.nearNumber]

media_size_path = experiment_path + '/mediaSize/'
config_path = experiment_path + '/config.json'
caching_policy = json.load(open(config_path, 'r'))['caching_policy']

total_media_size = 0
media_size_each_level = [0 for _ in range(3)]
for ip_address in os.listdir(media_size_path):
    curr_path = media_size_path + ip_address + '/'
    curr_level = math.floor(int(ip_address.split('.')[-1]) / 2)
    for file_name in os.listdir(curr_path):
        for line in open(curr_path + file_name, 'r'):
            curr_media_size = line.strip()
            if curr_media_size:
                total_media_size += int(curr_media_size)
                media_size_each_level[curr_level] += int(curr_media_size)
print(total_media_size)

if args.detailOutput:
    print("caching_policy: ", caching_policy)
    for i in range(3):
        print("level %s flow %s"%(str(i), media_size_each_level[i]))