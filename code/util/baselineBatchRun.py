#!/bin/python3
# This script is used to run all the configurations in a batch
# Each Docker as a configuration

import os
import sys
import json
import threading
import subprocess
import pandas as pd
import argparse

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Basic configure json
'''
basic_configure = {
  "trace_dir": "TwitterEgo",
  "caching_policy": "EffectiveSize",
  "use_http_server": false,
  "use_priority_queue": true,
  "cache_size_level_3": 15,
  "cache_size_level_2": 150,
  "cache_size_level_1": 1000000,
  "max_trace_len": null,
  "mode": "normal",
  "params": [
    0,
    0,
    0
  ]
}
'''
basic_config_filepath = "./code/main/basic_config.json"


# Datasets BrightkiteBigraphCommunity  GooglePlus  GowallaBigraphCommunity   TwitterEgo  TwitterFull
datasets = ["BrightkiteBigraphCommunity", "GooglePlus", "GowallaBigraphCommunity", "TwitterEgo", "TwitterFull"]

# Caching policies RAND FIFO LRU LRU-Social SecondHit
caching_policies = ["RAND", "FIFO", "LRU", "LRU-Social", "Second-Hit-LRU"]

# Working directory
working_dir = "/tmp/socialcdn/batchRun"
result_dir = "/tmp/socialcdn/batchRun/result"
reduce_dir = "/tmp/socialcdn/batchRun/reduce"

################################################################################
#                               Run the docker
################################################################################

def run_docker(configure):
  # Create the /tmp/socialcdn/batchRun path and get thread id
  thread_id = threading.current_thread().ident

  # Create the configure file
  configure_file = open("%s/config_%d.json" %(working_dir, thread_id), "w+")
  configure_file.write(json.dumps(configure))
  configure_file.close()

  # Run the docker
  cmd = 'sudo docker run --rm --privileged -v %s:/root/config.json mayuke/social-cdn:tpds /bin/bash -c "cp /root/config.json /root/socialcache/code/main/config.json && cd /root/socialcache && sudo python3 -m code.main.main && sudo python3 -m code.analyze.main -ecpdlmy "' %(configure_file.name)

  # Run the docker
  print("Run the docker: %s" %cmd)
  docker_res = None
  try:
    # get result
    docker_res = subprocess.check_output(cmd, shell=True)
    print("Docker result: %s" %docker_res)
  except subprocess.CalledProcessError as e:
    print("Run cmd error", e.output.decode('utf-8'))
    sys.exit(-1)

  # Write the result to the log file
  log_file = open("%s/log_%d.txt" %(result_dir, thread_id), "w+")
  log_file.write("TraceDir: %s\n" %configure["trace_dir"])
  log_file.write("CachingPolicy: %s\n" %configure["caching_policy"])
  log_file.write(docker_res.decode('utf-8'))
  
  # Clean the configure file
  os.system("rm %s" %configure_file.name)

################################################################################
#                               Parse the result
################################################################################
def reduce_traffic_volume():
  # Reduce the traffic volume
  # Create result dataframe
  result_df_L1 = pd.DataFrame(columns=datasets, index=caching_policies)
  result_df_L2 = pd.DataFrame(columns=datasets, index=caching_policies)
  result_df_L3 = pd.DataFrame(columns=datasets, index=caching_policies)
  # read the result file
  result_files = os.listdir(result_dir)
  for result_file in result_files:
    # Read the result file
    result_file = "%s/%s" %(result_dir, result_file)
    result_fd = open(result_file, "r")
    result_lines = result_fd.readlines()
    result_fd.close()

    # Get the trace dir and caching policy
    trace_dir = result_lines[0].split(":")[1].strip()
    caching_policy = result_lines[1].split(":")[1].strip()

    # Get the traffic volume
    L1_traffic_volume = 0
    L2_traffic_volume = 0
    L3_traffic_volume = 0
    for line in result_lines:
      if line.startswith("level 1; media size:"):
        L1_traffic_volume = float(line.split(":")[1].strip())
      elif line.startswith("level 2; media size:"):
        L2_traffic_volume = float(line.split(":")[1].strip())
      elif line.startswith("level 3; media size:"):
        L3_traffic_volume = float(line.split(":")[1].strip())
    
    # Write the result to the dataframe
    #result_df.loc[caching_policy, trace_dir] = dict(L1=L1_traffic_volume, L2=L2_traffic_volume, L3=L3_traffic_volume)
    result_df_L1.loc[caching_policy, trace_dir] = L1_traffic_volume
    result_df_L2.loc[caching_policy, trace_dir] = L2_traffic_volume
    result_df_L3.loc[caching_policy, trace_dir] = L3_traffic_volume


  # Write the result to the file
  #result_df.to_csv("%s/traffic_volume.csv" %reduce_dir)
  result_df_L1.to_csv("%s/traffic_volume_L1.csv" %reduce_dir)
  result_df_L2.to_csv("%s/traffic_volume_L2.csv" %reduce_dir)
  result_df_L3.to_csv("%s/traffic_volume_L3.csv" %reduce_dir)

  # Write the result to the file
  result_df_L1.to_string("%s/traffic_volume_L1.txt" %reduce_dir)
  result_df_L2.to_string("%s/traffic_volume_L2.txt" %reduce_dir)
  result_df_L3.to_string("%s/traffic_volume_L3.txt" %reduce_dir)

def reduce_request_latency():
  # Reduce the request latency
  # Create result dataframe
  result_df = pd.DataFrame(columns=datasets, index=caching_policies)
  # read the result file
  result_files = os.listdir(result_dir)
  for result_file in result_files:
    # Read the result file
    result_file = "%s/%s" %(result_dir, result_file)
    result_fd = open(result_file, "r")
    result_lines = result_fd.readlines()
    result_fd.close()

    # Get the trace dir and caching policy
    trace_dir = result_lines[0].split(":")[1].strip()
    caching_policy = result_lines[1].split(":")[1].strip()

    # Get the request latency
    latency = 0
    for line in result_lines:
      if line.startswith("latency_average:"):
        latency = float(line.split(":")[1].strip())
    
    # Write the result to the dataframe
    result_df.loc[caching_policy, trace_dir] = latency

  # Write the result to the file
  result_df.to_csv("%s/request_latency.csv" %reduce_dir)

  result_df.to_string("%s/request_latency.txt" %reduce_dir)

def reduce_runtime():
  # Reduce the runtime
  # Create result dataframe
  result_df = pd.DataFrame(columns=datasets, index=caching_policies)
  # read the result file
  result_files = os.listdir(result_dir)
  for result_file in result_files:
    # Read the result file
    result_file = "%s/%s" %(result_dir, result_file)
    result_fd = open(result_file, "r")
    result_lines = result_fd.readlines()
    result_fd.close()

    # Get the trace dir and caching policy
    trace_dir = result_lines[0].split(":")[1].strip()
    caching_policy = result_lines[1].split(":")[1].strip()

    # Get the runtime
    runtime = 0
    for line in result_lines:
      if line.startswith("time_duration:"):
        runtime = float(line.split(":")[1].strip())
    
    # Write the result to the dataframe
    result_df.loc[caching_policy, trace_dir] = runtime

  # Write the result to the file
  result_df.to_csv("%s/runtime.csv" %reduce_dir)

  result_df.to_string("%s/runtime.txt" %reduce_dir)

def reduce_hit_rate():
  # Reduce the hit rate
  # Create result dataframe
  result_df_l1 = pd.DataFrame(columns=datasets, index=caching_policies)
  result_df_l2 = pd.DataFrame(columns=datasets, index=caching_policies)
  result_df_l3 = pd.DataFrame(columns=datasets, index=caching_policies)

  # read the result file
  result_files = os.listdir(result_dir)
  for result_file in result_files:
    # Read the result file
    result_file = "%s/%s" %(result_dir, result_file)
    result_fd = open(result_file, "r")
    result_lines = result_fd.readlines()
    result_fd.close()

    # Get the trace dir and caching policy
    trace_dir = result_lines[0].split(":")[1].strip()
    caching_policy = result_lines[1].split(":")[1].strip()

    # Get the hit rate
    L1_hit_rate = 0
    L2_hit_rate = 0
    L3_hit_rate = 0
    for line in result_lines:
      if "(L1 CDN Layer)" in line:
        L1_hit_rate = float(line.split(":")[1].strip())
      elif "(L2 CDN Layer)" in line:
        L2_hit_rate = float(line.split(":")[1].strip())
      elif "(Data Center Layer)" in line:
        L3_hit_rate = float(line.split(":")[1].strip())
    
    # Write the result to the dataframe
    #result_df.loc[caching_policy, trace_dir] = dict(L1=L1_hit_rate, L2=L2_hit_rate, L3=L3_hit_rate)
    result_df_l1.loc[caching_policy, trace_dir] = L1_hit_rate
    result_df_l2.loc[caching_policy, trace_dir] = L2_hit_rate
    result_df_l3.loc[caching_policy, trace_dir] = L3_hit_rate

  # Write the result to the file
  result_df_l1.to_csv("%s/hit_rate_L1.csv" %reduce_dir)
  result_df_l2.to_csv("%s/hit_rate_L2.csv" %reduce_dir)
  result_df_l3.to_csv("%s/hit_rate_L3.csv" %reduce_dir)

  result_df_l1.to_string("%s/hit_rate_L1.txt" %reduce_dir)
  result_df_l2.to_string("%s/hit_rate_L2.txt" %reduce_dir)
  result_df_l3.to_string("%s/hit_rate_L3.txt" %reduce_dir)

def parse_result():
  
  # Network Traffic Volume
  reduce_traffic_volume()

  # Request Latency
  reduce_request_latency()

  # Runtime
  reduce_runtime()

  # Hit Rate
  reduce_hit_rate()


################################################################################
#                               Clean the working directory
################################################################################
def InitDir():
  # Clean the working directory
  if os.path.exists(working_dir):
    os.system("rm -rf %s" %working_dir)
  if os.path.exists(result_dir):
    os.system("rm -rf %s" %result_dir)
  if os.path.exists(reduce_dir):
    os.system("rm -rf %s" %reduce_dir)

  # Create the working directory
  if not os.path.exists(working_dir):
    os.makedirs(working_dir)
  if not os.path.exists(result_dir):
    os.makedirs(result_dir)
  if not os.path.exists(reduce_dir):
    os.makedirs(reduce_dir)

def main():
  print("========== Start Batch Run ==========")

  InitDir()

  # Threads
  threads = []

  for dataset in datasets:
    for caching_policy in caching_policies:

      # Create the configure
      configure = json.loads(open(basic_config_filepath, "r").read())
      configure["trace_dir"] = dataset
      configure["caching_policy"] = caching_policy

      print("Run the configure: %s" %configure)

      thread = threading.Thread(target=run_docker, args=(configure, ))
      thread.start()
      threads.append(thread)
  
  for thread in threads:
    thread.join()

if __name__ == "__main__":
  # commad line arguments parser: 1) map 2) reduce 3) mapreduce
  parser = argparse.ArgumentParser(description='Batch Run')
  parser.add_argument('-m', '--map', action='store_true', help='Run the map')
  parser.add_argument('-r', '--reduce', action='store_true', help='Run the reduce')
  parser.add_argument('-mr', '--mapreduce', action='store_true', help='Run the mapreduce')
  parser.add_argument('-o', '--outputPDF', action='store_true', help='Output the result to PDF')

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  
  args = parser.parse_args()

  if args.map or args.mapreduce:
    main()

  if args.reduce or args.mapreduce:
    parse_result()


