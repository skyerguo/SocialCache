from asyncio import FastChildWatcher
import json
import shlex
import subprocess
import random
import os
import time
import pandas as pd
import matplotlib.pyplot as plt

CONFIG_FILE_PATH="./code/main/config.json"
SIMULATION_CMD="sudo python3 -m code.main.main"
ANALYZE_CMD="python3 -m code.analyze.get_media_size -n 0"
LOG_FILENAME="./optimize.log"

init_list = {
    "PageRank": [[10000, 64.5, 310000]],
    "HITS": [[15000, 64.5, 310000]],
    "ClusteringCoefficient": [[15000, 64.5, 310]],
    "DegreeCentrality": [[15000, 64.5, 310]],
    "BetweennessCentrality": [[15000, 57.5, 54000]],
    "ClosenessCentrality": [[15000, 54.0, 52000]],
    "EigenvectorCentrality": [[15000, 54.0, 52000]],
    "LaplacianCentrality": [[15000, 54.0, 52000]],
    "EgoBetweennessCentrality": [[15000, 57.5, 54000]],
    "EffectiveSize": [[15000, 64.5, 10]],
}

step_social = {
    "PageRank": 50000,
    "HITS": 50000,
    "ClusteringCoefficient": 30,
    "DegreeCentrality": 30,
    "ClosenessCentrality": 5000,
    "BetweennessCentrality": 5000,
    "EigenvectorCentrality": 5000,
    "LaplacianCentrality": 5000,
    "EgoBetweennessCentrality": 7000,
    "EffectiveSize": 1,
}

class hill_climb_optimize():
    def __init__(self) -> None:
        self.json_config    = json.load(open(CONFIG_FILE_PATH, "r"))
        self.visited        = set()
        self.init_config    = self.json_config
        self.init_altitude  = 0

        self.optimal_config     = self.init_config
        self.optimal_altitude   = self.init_altitude

        self.iteration_time = 0

        # define step length
        self.step_len0 = 3000       # location
        self.step_len1 = 1      # media_size
        self.step_len2 = step_social[self.init_config['caching_policy']]      # social_metric
        self.step_list = [self.step_len0, self.step_len1, self.step_len2]

        # debug switch
        self.debug = False

        # init logfile
        self.start_timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.log_filename = LOG_FILENAME + "%s" %(self.start_timestamp)
        with open(self.log_filename, "w") as log_fd:
            log_fd.write("\n")
        
        # init log dataframe
        self.log_df = pd.DataFrame()


    def run_simulator(self, config):
        if self.debug:
            return random.randint(1, 1000)

        print("******* run simulator with config:\n", config)
        # wrtie config to file
        with open(CONFIG_FILE_PATH, "w") as config_fd:
            config_fd.write(json.dumps(config))

        # run simulation
        os.system(SIMULATION_CMD)

        # run analyzation
        res = float(subprocess.getoutput(ANALYZE_CMD))
        
        print("******* simulator done, get res ", res)
        return res

    def get_near_ways(self, params):
        near_params = []

        # method1
        #for p0 in [self.step_len0, -self.step_len0, self.step_len0/2, -self.step_len0/2]:
        #    for p1 in [self.step_len1, -self.step_len1, self.step_len1/2, -self.step_len1/2]:
        #        for p2 in [self.step_len2, -self.step_len2, self.step_len2/2, -self.step_len2/2]:
        #            near_params.append((params[0] + p0, params[1] + p1, params[2] + p2))
        #

        # method2
        for i in range(3):
            new_params = params
            new_params[i] += self.step_list[i]
            near_params.append(tuple(new_params))
            new_params = params
            new_params[i] -= self.step_list[i]
            near_params.append(tuple(new_params))
        
        print("near ways: ", near_params)
        return near_params

    def start_climb(self):
        print("start find way up, current altitude : ", self.optimal_altitude)
        self.climb_path.append(dict(params=self.optimal_config["params"], traffic=self.optimal_altitude))

        near_list = self.get_near_ways(self.optimal_config["params"])

        for way in near_list:
            if way in self.visited:
                continue
            self.visited.add(way)
            
            new_config = self.optimal_config
            new_config["params"] = list(way)
            new_altitude = self.run_simulator(new_config)
            print("find altitude : ", new_altitude)

            # if find a higher altitude, then refresh the optimal params,
            # here higher altitude means lower traffic
            if self.optimal_altitude > new_altitude:
                self.search_depth += 1
                print("*** Find better config, current depth %d" %self.search_depth)
                self.optimal_altitude   = new_altitude
                self.optimal_config     = new_config
                self.start_climb()
            

    def reset(self, params=None):
        # clear cache  werwer
        self.climb_path = []
        self.visited.clear()
        self.search_depth = 0

        if not params:
            # randomly init status
            param0 = round(random.uniform(0, 200), 1)
            param1 = round(random.uniform(0, 100), 1)
            param2 = round(random.uniform(0, 500000), 1)

            self.init_config["params"]  = [param0, param1, param2]
        else:
            self.init_config["params"]  = params

        self.init_altitude          = self.run_simulator(self.init_config)
        self.optimal_config     = self.init_config
        self.optimal_altitude   = self.init_altitude

        self.iteration_time += 1


    def record(self):
        # save to log file
        log_str = "\n"*2
        log_str += "="*21 + " round " + "="*21 + "\n"
        log_str += "start :" + self.start_time + "\n"
        log_str += "end   :" + self.end_time   + "\n"
        log_str += "cache policy     :" + str(self.json_config["caching_policy"]) + "\n"
        log_str += "optimize traffic : " + str(self.optimal_altitude) + "\n"
        log_str += "optimize params  : " + str([round(x, 2) for x in self.optimal_config["params"]]) + "\n"

        step = 0
        for footprint in self.climb_path:
            step+=1
            log_str += "\n------ [step%d] ------\n" %step
            log_str += "params  :" + str([round(x, 2) for x in footprint["params"]]) + "\n"
            log_str += "traffic :" + str(footprint["traffic"]) + "\n"
        
        with open(self.log_filename, "a") as log_fd:
            log_fd.write(log_str)

        # save to dataframe
        self.log_df = pd.concat([self.log_df, pd.Series([x['traffic'] for x in self.climb_path], name="iter%d" %self.iteration_time)], axis=1)

    def hill_climb(self, seed_num=10):
        for i in range(seed_num):
            # reset status
            self.reset()

            # start time
            self.start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

            # start hill climbing
            self.start_climb()

            # end time
            self.end_time   = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

            # record
            self.record()

    def hill_climb_specific_point(self, params_list):
        for params in params_list:
            # reset status
            self.reset(params)

            # start time
            self.start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

            # start hill climbing
            self.start_climb()

            # end time
            self.end_time   = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

            # record
            self.record()
    
    def savelog(self):
        self.log_df.to_csv("./optimze_%s.csv"%(self.start_timestamp))

    def visualize(self):
        print(self.log_df)
        #fig_df = log_df
        print("ploting result")
        plt.figure()
        self.log_df.plot.line(xlabel="iterations", ylabel="traffic",title="hill-climbing optimization", grid=True)
        plt.savefig("./code/figures/hil_climbing/opt_%s.png" %self.end_time)

if __name__ == "__main__":
    optimize = hill_climb_optimize()
    optimize.hill_climb_specific_point(init_list[optimize.init_config['caching_policy']])
    optimize.hill_climb(0)
    # optimize.visualize()
    # optimize.savelog()
