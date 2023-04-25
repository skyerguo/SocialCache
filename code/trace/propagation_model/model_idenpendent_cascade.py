import random

def propagation(G, seed, interval=600, p=0.5, max_time=16):
    '''
    G: easygraph.Graph
    seed: list of seed nodes
    p: float(0, 1) activation probability
    max_time: int max time of propagation
    '''
    trace = []
    all_active_nodes = []
    all_active_nodes.append(G.nodes[seed])

    time = 0
    active_nodes = [seed]
    while len(active_nodes) > 0 and time <  max_time * interval :
        new_active_nodes = []

        # traverse all active nodes in last round
        for node in active_nodes:
            # try to active neighbors of each active node
            for neighbor in G.neighbors(node):
                if neighbor in all_active_nodes or neighbor in new_active_nodes:
                    # if neighbor is already active, continue
                    continue
            
                if random.random() < p:
                    # not chosed to be active, continue
                    continue

                new_active_nodes.append(neighbor)
                all_active_nodes.append(neighbor)

                randtime = (time + interval * random.randint(1, 10000)/10000)
                trace.append((randtime, neighbor))

        active_nodes = new_active_nodes
        time += interval

    return trace