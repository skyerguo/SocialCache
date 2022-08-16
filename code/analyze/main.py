import argparse
import os
import json
import math

p = argparse.ArgumentParser(description='Analyze the result')
p.add_argument('-t', '--timestamp', type=str, default="", dest="timestamp", action="store", help="the timestamp of data file")
p.add_argument('-n', '--nearnumber', type=int, default=0, dest="nearNumber", action="store", help="the number of nearest timestamp")
p.add_argument('-d', '--detailoutput', default=False, dest="detailOutput", action="store_true", help="give more detail outputs")
p.add_argument('-m', '--mediasize', default=False, dest="mediaSize", action="store_true", help="whether output media size")
p.add_argument('-e', '--executiontime', default=False, dest="executionTime", action="store_true", help="whether output execution time")
p.add_argument('-f', '--flow', default=False, dest="flow", action="store_true", help="whether output flow")
args = p.parse_args()

data_root = '/proj/socnet-PG0/data/'
if args.timestamp:
    experiment_path = data_root + args.timestamp
else:
    files = os.listdir(data_root)
    files = sorted(files, reverse=True)
    experiment_path = data_root + files[args.nearNumber]

media_size_path = experiment_path + '/mediaSize/'
execution_time_path = experiment_path + '/time_log.txt'
flow_path = experiment_path + '/flow/'
config_path = experiment_path + '/config.json'
caching_policy = json.load(open(config_path, 'r'))['caching_policy']

def get_media_size():
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
    print("total_media_size: ", total_media_size)
    if args.detailOutput:
        for i in range(3):
            print("level %i; media szie: %s"%(i + 1, media_size_each_level[i]))


def get_execution_time():
    f_in = open(execution_time_path, 'r')
    time_duration = -1
    for line in f_in:
        if 'time_duration' in line:
            time_duration = float(line.split(" ")[-1].strip())
    print("time_duration: ", time_duration)

def get_flow():
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

if __name__ == '__main__':
    print("caching_policy: ", caching_policy)
    print("------")

    if args.mediaSize:
        get_media_size()
        print("------")

    if args.executionTime:
        get_execution_time()
        print("------")

    if args.flow:
        get_flow()
        print("------")