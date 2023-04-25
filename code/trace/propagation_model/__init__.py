import easygraph as eg
import random

class independent_cascade_trace:
    def __init__(self):
        print("init independent_cascade_trace")

    def gen_trace(self, G, seed, p=0.1, max_time=100):
        '''
        G: easygraph.Graph
        seed: list of seed nodes
        p: float(0, 1) activation probability
        max_time: int max time of propagation
        '''
        trace = []
        active_nodes = seed
        time = 0
        while len(active_nodes) > 0 and time < max_time:
            new_active_nodes = []
            for node in active_nodes:
                for neighbor in G.neighbors(node):
                    if neighbor not in active_nodes and neighbor not in new_active_nodes:
                        if random.random() < p:
                            new_active_nodes.append(neighbor)
            trace.append((time, active_nodes))
            active_nodes = new_active_nodes
            time += 1
        return trace