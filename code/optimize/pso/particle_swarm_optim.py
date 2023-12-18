# particle swarm optimization
import json
import random
import sys
import os
import subprocess
import threading
import copy
import numpy as np
import pandas as pd
import logging

# Be clear that what you want to optimize
# if you want to optimize the cache hit rate, then the larger fitness is better
# if you want to optimize the traffic volume, then the smaller fitness is better
# you must change the code before you run it


#CONFIG_FILE_PATH="./code/main/basic_config.json"
CONFIG_FILE_PATH="./code/optimize/pso/emu_config.json"

class particle():
    def __init__(self, name, optim_target, init_config, position, speed, max_speed, min_speed, omega, c1, c2) -> None:
        self.name = name
        self.fitness    = sys.maxsize
        self.position   = position
        self.speed      = speed

        self.config_json = init_config
        self.config_json['params'] = self.position.tolist()

        self.max_speed = max_speed
        self.min_speed = min_speed
        self.omega  = omega
        self.c1     = c1
        self.c2     = c2

        self.best_fitness   = 0
        self.best_position  = self.position

        self.optim_target = optim_target

        # create working directory and write config
        if not os.path.exists("./particles/%s" %self.name):
            os.mkdir("./particles/%s" %self.name)
        with open("./particles/%s/config.json" %self.name, "w+") as config_fd:
            config_fd.write(json.dumps(self.config_json))
        
        self.log_file = "./particles/%s/log.txt" %self.name
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        # create log file
        self.log_fd = open(self.log_file, "w+")

        print("init particle %s with init config %s" %(self.name, self.config_json))


    def get_fitness(self, debug=False):
        """
        Get current fitness of the particle
        """
        self.log_fd.write("------ iteration ------\n")

        # write config to file
        self.config_json['params'] = self.position.tolist()
        with open("./particles/%s/config.json" %self.name, "w+") as config_fd:
            config_fd.write(json.dumps(self.config_json))
            self.log_fd.write("config file: %s\n" %json.dumps(self.config_json))

        # run docker image
        cmd = 'sudo docker run --rm --privileged -v /users/gtc/SocialCache/particles/%s/config.json:/root/config.json mayuke/social-cdn:tpds /bin/bash -c "cp /root/config.json /root/socialcache/code/main/config.json && cd /root/socialcache && sudo python3 -m code.main.main && sudo python3 -m code.analyze.main -ecpdlmy"' %self.name

        self.log_fd.write("run docker image cmd: %s\n" %cmd)
        docker_res = None
        try:
            # get result
            docker_res = subprocess.check_output(cmd, shell=True)
            self.log_fd.write("docker result: %s\n" %docker_res.decode('utf-8'))
            print(docker_res.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            print("run cmd error", e.output.decode('utf-8'))
            sys.exit(-1)

        # get fitness
        fitness = 0
        # split result by line
        docker_res = docker_res.decode('utf-8').split("\n")
        if self.optim_target == "traffic_volume":
            for line in docker_res:
                if "total_media_size" in line:
                    fitness = float(line.split(":")[-1])
                    break
        elif self.optim_target == "cache_hit_rate":
            for line in docker_res:
                if "总缓存命中率" in line:
                    fitness = float(line.split(":")[-1])
                    break
    
        self.log_fd.write("particle %s fitness : %f\n" %(self.name, fitness))
        self.fitness = fitness

        if self.optim_target == "traffic_volume":
            if self.fitness < self.best_fitness:
                self.best_fitness   = self.fitness
                self.best_position  = self.position
                self.log_fd.write("find better result : %f, %s\n" %(self.best_fitness, self.best_position))
        elif self.optim_target == "cache_hit_rate":
            if self.fitness > self.best_fitness:
                self.best_fitness   = self.fitness
                self.best_position  = self.position
                self.log_fd.write("find better result : %f, %s\n" %(self.best_fitness, self.best_position))
            
        # write log
        self.log_fd.write(" fitness : %f\n" %self.fitness)
        self.log_fd.write(" position: %s\n" %self.position)
        self.log_fd.write(" speed   : %s\n" %self.speed)
        self.log_fd.write("------ iteration end ------\n\n")

        return self.fitness, self.position
    
    def update_position(self, gbest_position):
        self.log_fd.write("------ update position ------\n")
        # update speed
        self.speed = self.omega * self.speed + \
                     self.c1 * np.random.rand() * (self.best_position - self.position) + \
                     self.c2 * np.random.rand() * (gbest_position - self.position)
        
        # speed filter
        for i in range(len(self.speed)):
            self.speed[i] = np.clip(self.speed[i], self.min_speed[i], self.max_speed[i])

        self.log_fd.write("speed: %s\n" %self.speed)
        # update position
        self.position += self.speed
        self.log_fd.write("position: %s\n" %self.position)

        # write config to file
        #self.config_json['params'] = self.position.tolist()
        #with open("./particles/%s/config.json" %self.name, "w+") as config_fd:
        #    config_fd.write(json.dumps(self.config_json))
    
    def get_status(self):
        return dict(fitness = self.fitness, position = self.position, speed = self.speed)

class pso_optimzer():
    def __init__(self, optim_target, early_stop_val, pop_size, bounds, speed, max_speed, min_speed, max_iteration, omega=1, c1=1.33, c2=1.33) -> None:
        # optimization target
        self.optim_target = optim_target
        self.early_stop_val = early_stop_val

        # swarm params
        self.pop_size = pop_size
        self.init_bounds   = bounds
        self.init_speed    = speed
        self.max_iteration = max_iteration
        
        # speed update params
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.omega  = omega
        self.c1     = c1
        self.c2     = c2

        if self.optim_target == "cache_hit_rate":
            self.best_fitness  = 0
            self.best_position = None
        elif self.optim_target == "traffic_volume":
            self.best_fitness  = sys.maxsize
            self.best_position = None

        # create log file
        self.log_file_name = "./particles/log.txt"
        if os.path.exists(self.log_file_name):
            os.remove(self.log_file_name)
        os.mknod(self.log_file_name)

        self.logger = logging.getLogger("pso")
        self.logger.setLevel(logging.INFO)

        self.log_file_handler = logging.FileHandler(self.log_file_name, mode="w+", encoding="utf-8")
        self.log_file_handler.setLevel(logging.INFO)

        self.log_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(self.log_file_handler)

        # print info
        self.logger.info("====== Particle Swarm Optimization ======")
        self.logger.info("optim target: %s" %self.optim_target)
        self.logger.info("early stop val: %f" %self.early_stop_val)
        self.logger.info("max iteration: %d" %self.max_iteration)
        self.logger.info("pop size: %d" %self.pop_size)
        self.logger.info("init speed: %s" %self.init_speed)


    def generate_particles(self):
        # randomly generate initial position for population
        print(self.init_bounds)
        init_positions = np.array([np.random.uniform(b[0], b[1], self.pop_size) for b in self.init_bounds], dtype=np.float64)

        self.particles_list = []
        init_config = None
        with open(CONFIG_FILE_PATH, "r+") as config_fd:
            init_config = json.load(config_fd)

        for i in range(self.pop_size):
            # generate one instance
            particle_name = "particle_%d" %i
            particle_instance = particle(particle_name, \
                                         self.optim_target, \
                                        init_config, \
                                        init_positions[:, i], \
                                        self.init_speed, \
                                        self.max_speed, \
                                        self.min_speed, \
                                        self.omega, \
                                        self.c1, \
                                        self.c2)

            # save instance
            self.particles_list.append(particle_instance)

    def launch(self):
        # create particle working directory
        if not os.path.exists("./particles"):
            os.mkdir("./particles")

        # init particles
        self.generate_particles()

        # start iteration
        for i in range(self.max_iteration):
            print("--- iteration : %d" %i)
            # log dataframe
            log_df = pd.DataFrame(columns=['fitness', 'position', 'speed'])

            # recompute fitness
            threads = []
            for particle in self.particles_list:
                # use multi-thread to compute fitness
                thread = threading.Thread(target=particle.get_fitness)
                thread.start()

                threads.append(thread)
            
            for thread in threads:
                thread.join()
            
            # update global best fitness and position
            particle_num = 0
            for particle in self.particles_list:
                fitness, position = particle.get_status()['fitness'], particle.get_status()['position']

                if self.optim_target == "cache_hit_rate":
                    if fitness > self.best_fitness:
                        print("find better result")
                        self.best_fitness  = copy.deepcopy(fitness)
                        self.best_position = copy.deepcopy(position)
                elif self.optim_target == "traffic_volume":
                    if fitness < self.best_fitness:
                        print("find better result")
                        self.best_fitness  = copy.deepcopy(fitness)
                        self.best_position = copy.deepcopy(position)

                log_df.loc['p%d' %particle_num] = particle.get_status()
                particle_num += 1
            
            # update position
            for particle in self.particles_list:
                particle.update_position(self.best_position)

            # print log
            self.logger.info("------ iteration %d ------" %i)
            self.logger.info(log_df.to_string())
            self.logger.info("best fitness: %f, best position: %s" %(self.best_fitness, self.best_position))
            
            print(log_df)
            print("best fitness :", self.best_fitness)
            print("best position:", self.best_position)

if __name__ == "__main__":
    print("====== Particle Swarm Optimization =======")

    with open("./code/optimize/pso/config.json") as conf_fd:
        config_json = json.load(conf_fd)
        init_bounds = [tuple(item) for item in config_json['init_bounds']]
        
        optim = pso_optimzer(config_json['optim_target'], \
                            config_json['early_stop_value'], \
                            config_json['pop_size'], \
                            init_bounds, \
                            np.array(config_json['init_speed'], dtype=np.float64), \
                            np.array(config_json['max_speed'], dtype=np.float64), \
                            np.array(config_json['min_speed'], dtype=np.float64), \
                            config_json['max_iteration'], \
                            config_json['omega'], \
                            config_json['c1'], \
                            config_json['c2'],
                            )
        optim.launch()
