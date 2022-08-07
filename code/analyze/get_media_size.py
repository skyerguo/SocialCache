import argparse
import os
import json

p = argparse.ArgumentParser(description='Analyze the result')
p.add_argument('-t', '--timestamp', type=str, default="", dest="timestamp", action="store", help="the timestamp of data file")
p.add_argument('-n', '--nearnumber', type=int, default=0, dest="nearNumber", action="store", help="the number of nearest timestamp")
args = p.parse_args()

data_root = '/proj/socnet-PG0/data/'
if args.timestamp:
    media_size_path = data_root + args.timestamp + '/mediaSize/'
else:
    files = os.listdir(data_root)
    files = sorted(files, reverse=True)
    media_size_path = data_root + files[args.nearNumber] + '/mediaSize/'

total_media_size = 0
for ip_address in os.listdir(media_size_path):
    curr_path = media_size_path + ip_address + '/'
    for file_name in os.listdir(curr_path):
        for line in open(curr_path + file_name, 'r'):
            if line.strip():
                total_media_size += int(line.strip())
print(total_media_size)