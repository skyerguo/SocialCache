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

class hill_climb_optimize():
    def __init__(self) -> None:
        self.json_config    = json.load(open(CONFIG_FILE_PATH, "r"))
        self.visited        = set()
        self.init_config    = self.json_config
        self.init_altitude  = 0

        self.optimal_config     = self.init_config
        self.optimal_altitude   = self.init_altitude

        # define step length
        self.step_len0 = 0.1        # timestamp
        self.step_len1 = 5          # pagerank * media_size
        self.step_len2 = 0.1        # nearest

        # debug switch
        self.debug = False

        # init logfile
        with open(LOG_FILENAME, "w") as logfd:
            logfd.write("\n")
        
        # init log dataframe
        self.log_df = pd.DataFrame(columns=["optimal", "average"])


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
        res = int(subprocess.getoutput(ANALYZE_CMD))
        
        print("******* simulator done, get res ", res)
        return res

    def get_near_ways(self, params):
        near_params = []

        for p0 in [self.step_len0, -self.step_len0]:
            for p1 in [self.step_len1, -self.step_len1]:
                for p2 in [self.step_len2, -self.step_len2]:
                    near_params.append((params[0] + p0, params[1] + p1, params[2] + p2))
        
        print("near ways: ", near_params)
        return near_params

    def start_climb(self):
        print("start find way up, current altitude : ", self.optimal_altitude)
        self.climb_path.append(dict(params=self.optimal_config["params"], traffic=self.optimal_altitude))

        near_list = self.get_near_ways(self.optimal_config["params"])
        move = False

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
                self.optimal_altitude   = new_altitude
                self.optimal_config     = new_config
                move = True
        
        if move:
            self.start_climb()

    def reset(self):
        # clear cache
        self.climb_path = []
        self.visited.clear()

        # init status
        param0 = round(random.uniform(0, 2), 1)
        param1 = random.randint(0, 100)
        param2 = round(random.uniform(-2, 2), 1)

        self.init_config["params"]  = [param0, param1, param2]
        self.init_altitude          = self.run_simulator(self.init_config)

        self.optimal_config     = self.init_config
        self.optimal_altitude   = self.init_altitude

    def record(self):
        # save to log file
        log_str = "\n"*2
        log_str += "="*21 + " round " + "="*21 + "\n"
        log_str += "start :" + self.start_time + "\n"
        log_str += "end   :" + self.end_time   + "\n"
        log_str += "optimize traffic : " + str(self.optimal_altitude) + "\n"
        log_str += "optimize params  : " + str([round(x, 2) for x in self.optimal_config["params"]]) + "\n"

        step = 0
        sum_altitude = 0
        for footprint in self.climb_path:
            step+=1
            log_str += "\n------ [step%d] ------\n" %step
            log_str += "params  :" + str([round(x, 2) for x in footprint["params"]]) + "\n"
            log_str += "traffic :" + str(footprint["traffic"]) + "\n"

            sum_altitude += footprint["traffic"]
        
        self.average_altitude = sum_altitude // step
        self.log_df = self.log_df.append(dict(optimal=self.optimal_altitude, average=self.average_altitude), ignore_index=True)

        with open(LOG_FILENAME, "a") as log_fd:
            log_fd.write(log_str)

    def hill_climb(self):
        for i in range(10):
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
    
    def visualize(self):
        print("ploting result")
        plt.figure()
        self.log_df.plot.line(xlabel="iterations", ylabel="traffic",title="hill-climbing optimization", grid=True)
        plt.savefig("./figures/hill_climbing/opt_%s.png" %self.end_time)

if __name__ == "__main__":
    optimize = hill_climb_optimize()
    optimize.hill_climb()
    optimize.visualize()