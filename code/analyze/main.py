import argparse
import os
import json
import math
import sys
import numpy as np

p = argparse.ArgumentParser(description='Analyze the result')
p.add_argument('-t', '--timestamp', type=str, default="", dest="timestamp", action="store", help="the timestamp of data file")
p.add_argument('-n', '--nearnumber', type=int, default=0, dest="nearNumber", action="store", help="the number of nearest timestamp")
p.add_argument('-l', '--detailoutput', default=False, dest="detailOutput", action="store_true", help="give more detail outputs")
p.add_argument('-m', '--mediasize', default=False, dest="mediaSize", action="store_true", help="whether output media size")
p.add_argument('-e', '--executiontime', default=False, dest="executionTime", action="store_true", help="whether output execution time")
p.add_argument('-f', '--flow', default=False, dest="flow", action="store_true", help="whether output flow")
p.add_argument('-c', '--cachehitratio', default=False, dest="cacheHitRatio", action="store_true", help="whether output cache hit ratio")
p.add_argument('-p', '--parameters', default=False, dest="parameters", action="store_true", help="whether output cache parameters")
p.add_argument('-d', '--dataset', default=False, dest="dataset", action="store_true", help="whether output dataset")
p.add_argument('-q', '--priority_queue', default=False, dest="priority_queue", action="store_true", help="output the setting of using priority_queue")
p.add_argument('-z', '--outputFile', default=False, dest="outputFile", action="store_true", help="whether output the result into files")
p.add_argument('-y', '--latency', default=False, dest="latency", action="store_true", help="whether output latency")

args = p.parse_args()

data_root = '/proj/socnet-PG0/data/'

if args.timestamp:
    result_data_path = args.timestamp
    experiment_path = data_root + args.timestamp
else:
    files = os.listdir(data_root)
    files = sorted(files, reverse=True)
    result_data_path = files[args.nearNumber]
    experiment_path = data_root + files[args.nearNumber]

media_size_path = experiment_path + '/mediaSize/'
execution_time_path = experiment_path + '/time_log.txt'
flow_path = experiment_path + '/flow/'
cache_hit_ratio_path = experiment_path + '/find_log.txt'
latency_path = experiment_path + '/latency_log.txt'
config_path = experiment_path + '/config.json'
config_json = json.load(open(config_path, 'r'))

def get_media_size():
    ## all = insert_all * 2 + insert[level_3];
    total_media_size = 0
    insert_all_media_size = 0
    media_size_each_level = [0 for _ in range(3)]
    for ip_address in os.listdir(media_size_path):
        curr_path = media_size_path + ip_address + '/'
        curr_level = math.floor(int(ip_address.split('.')[-1]) / 2)
        for file_name in os.listdir(curr_path):
            for line in open(curr_path + file_name, 'r'):
                curr_media_size = line.strip()
                if curr_media_size:
                    total_media_size += float(curr_media_size)
                    media_size_each_level[curr_level] += float(curr_media_size)
                    if "insert" in file_name:
                        insert_all_media_size += float(curr_media_size)

    print("total_media_size: ", total_media_size)
    print("insert_all_media_size: ", insert_all_media_size)
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
    f_in.close()
    
def get_latency():
    f_in = open(latency_path, 'r')
    latency_list = []
    for line in f_in:
        latency_list.append(float(line.split(' ')[1].strip()))
    print("latency_average: ", np.mean(latency_list))
    f_in.close()

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

def get_cache_hit_ratio():
    #  print(cnt_line, selected_level_3_id, result_level, find_result[1], file=f_out_find)
    find_success_number = [0, 0, 0, 0]
    find_fail_number = [0, 0, 0, 0]
    f_in = open(cache_hit_ratio_path, 'r')
    for line in f_in:
        result_level = int(line.split(" ")[2].strip())
        for temp_level in range(3, result_level, -1):
            find_fail_number[temp_level] += 1
        find_success_number[result_level] += 1
    f_in.close()

    if find_success_number[3] + find_fail_number[3] > 0:
        print('三级CDN缓存命中率: ', find_success_number[3] / (find_success_number[3] + find_fail_number[3]))
    else:
        print('未经过三级CDN缓存')

    if find_success_number[2] + find_fail_number[2] > 0:
        print('二级CDN缓存命中率: ', find_success_number[2] / (find_success_number[2] + find_fail_number[2]))
    else:
        print('未经过二级CDN缓存')
        
    if find_success_number[1] + find_fail_number[1] > 0:
        print('一级CDN缓存命中率: ', find_success_number[1] / (find_success_number[1] + find_fail_number[1]))
    else:
        print('未经过一级CDN缓存')

    print("总缓存命中率: ", (find_success_number[3] + find_success_number[2] + find_success_number[1]) / (find_success_number[3] + find_success_number[2] + find_success_number[1] + find_fail_number[3] + find_fail_number[2] + find_fail_number[1]))

    print("二三级缓存命中率: ", (find_success_number[3] + find_success_number[2]) / (find_success_number[3] + find_success_number[2] + find_fail_number[3] + find_fail_number[2]))

if __name__ == '__main__':
    if args.outputFile:
        f_out = open('./data/results/analyse_data/' + result_data_path, 'w+')
        sys.stdout = f_out
        pass
    print("caching_policy: ", config_json['caching_policy'])
    if args.parameters:
        print("cache_size_level_3: ", config_json['cache_size_level_3'])
        print("cache_size_level_2: ", config_json['cache_size_level_2'])
        print("cache_size_level_1: ", config_json['cache_size_level_1'])
        print("parameters: ", config_json['params'])
    
    if args.priority_queue:
        print("use_priority_queue: ", config_json['use_priority_queue'])
        print("------")
        
    if args.dataset:
        print("dataset: ", config_json['trace_dir'])
    print("------")

    if args.cacheHitRatio:
        get_cache_hit_ratio()
        print("------")

    if args.mediaSize:
        get_media_size()
        print("------")

    if args.executionTime:
        get_execution_time()
        print("------")
    
    if args.latency:
        get_latency()
        print("------")

    if args.flow:
        get_flow()
        print("------")