# particle swarm optimization
import json
import random
import sys
import os
import subprocess
import copy
import numpy as np
import pandas as pd

CONFIG_FILE_PATH="./code/main/config.json"
SIMULATION_CMD="sudo python3 -m code.main.main"
ANALYZE_CMD="python3 -m code.analyze.get_media_size -n 0"
debug = True

def run_simulator(params, debug=False):
    if True:
        return 0.01*params[0]**2 - 4*params[0]
    
    # write config to file
    with open(CONFIG_FILE_PATH, "w") as config_fd:
        config = json.load(config_fd)
        config['params'] = params
        config_fd.write(json.dumps(config))
    
    print("******* running simulation with params :", params)
    # run simulation
    os.system(SIMULATION_CMD)

    # run analyzation
    res = float(subprocess.getoutput(ANALYZE_CMD))
    print("******* simulator result ", res)

    return res

class particle():
    def __init__(self, position, speed, max_speed, min_speed, omega, c1, c2) -> None:
        self.fitness    = sys.maxsize
        self.position   = position
        self.speed      = speed

        self.max_speed = max_speed
        self.min_speed = min_speed
        self.omega  = omega
        self.c1     = c1
        self.c2     = c2

        self.best_fitness   = sys.maxsize
        self.best_position  = self.position
        print("generate one particle, position: ", self.position)

    def get_fitness(self, debug=False):
        """
        Get current fitness of the particle
        """ 
        self.fitness = run_simulator(self.position.tolist())

        if self.fitness < self.best_fitness:
            self.best_fitness   = self.fitness
            self.best_position  = self.position

        return self.best_fitness, self.best_position
    
    def update_position(self, gbest_position):
        # update speed
        self.speed = self.omega * self.speed + \
                     self.c1 * np.random.rand() * (self.best_position - self.position) + \
                     self.c2 * np.random.rand() * (gbest_position - self.position)
        
        # speed filter
        for i in range(len(self.speed)):
            self.speed[i] = np.clip(self.speed[i], self.min_speed[i], self.max_speed[i])

        # update position
        self.position += self.speed
    
    def get_status(self):
        return dict(fitness  = round(self.fitness, 4), \
                    position = np.round(self.position, 4), \
                    speed    = np.round(self.speed, 4))

class pso_optimzer():
    def __init__(self, pop_size, bounds, speed, max_speed, min_speed, max_iteration, omega=1, c1=1.33, c2=1.33) -> None:

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

        self.best_fitness  = sys.maxsize
        self.best_position = None

    def generate_particles(self):
        # randomly generate initial position for population
        init_positions = np.array([np.random.randint(b[0], b[1], self.pop_size) for b in self.init_bounds], dtype=np.float64)

        self.particles_list = []
        for i in range(self.pop_size):
            # generate one instance
            particle_instance = particle(init_positions[:, i], \
                                        self.init_speed, \
                                        self.max_speed, \
                                        self.min_speed, \
                                        self.omega, \
                                        self.c1, \
                                        self.c2)

            # save instance
            self.particles_list.append(particle_instance)

    def launch(self):
        # init particles
        self.generate_particles()

        # start iteration
        for i in range(self.max_iteration):
            print("--- iteration : %d" %i)
            # log dataframe
            log_df = pd.DataFrame(columns=['fitness', 'position', 'speed'])

            # recompute fitness
            i = 0
            for particle in self.particles_list:
                fitness, position = particle.get_fitness()

                if fitness < self.best_fitness:
                    print("find better result")
                    self.best_fitness  = copy.deepcopy(fitness)
                    self.best_position = copy.deepcopy(position)

                log_df.loc['p%d' %i] = particle.get_status()
                i += 1
            
            # update position
            for particle in self.particles_list:
                particle.update_position(self.best_position)
            
            print(log_df)
            print("best fitness :", self.best_fitness)
            print("best position:", self.best_position)

if __name__ == "__main__":
    print("====== Particle Swarm Optimization =======")
    print("# run as main.")
    with open("config.json") as conf_fd:
        config_json = json.load(conf_fd)
        init_bounds = [tuple(item) for item in config_json['init_bounds']]
        
        optim = pso_optimzer(config_json['pop_size'], \
                            init_bounds, \
                            np.array(config_json['init_speed'], dtype=np.float64), \
                            np.array(config_json['max_speed'], dtype=np.float64), \
                            np.array(config_json['min_speed'], dtype=np.float64), \
                            config_json['max_iteration'], \
                            config_json['omega'], \
                            config_json['c1'], \
                            config_json['c2'])
        optim.launch()
