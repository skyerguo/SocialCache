from . import model_idenpendent_cascade as ic
import easygraph as eg
import pandas as pd
import random

class make_twitter_trace:
    def __init__(self, output_path="./output.txt"):
        print("init make_twitter_trace")
        self.output_path = output_path
        self.unordered_trace = []

        self.propagation_interval = 600
        self.max_iteration = 16
        self.activate_prob = 0.5


    def load_graph(self, graph_path):
        print("load graph")
        self.G = eg.DiGraph()
        self.G.add_edges_from_file(graph_path)
    
    def load_location(self, location_path):
        print("load location")
        self.country_location = pd.read_csv(location_path)
        choice_list = []

        for rowidx, row in self.country_location.iterrows():
            longtitude  = float(row["longtitude"])
            latitude    = float(row["latitude"])
            w_repeat    = [(longtitude, latitude)]*int(row["count"])
            choice_list.extend(w_repeat)

        #print(self.G.nodes)
        for node in self.G.nodes:
            self.G.nodes[node]['location'] = random.choice(choice_list)

    def load_post(self, post_path):
        print("load post")
        with open(post_path, 'r') as post_fd:
            self.post_line = post_fd.readlines()
    
    def gen_trace(self):
        # generate trace for each post
        print("gen trace")
        log_count = 0
        for post in self.post_line:
            if 'post' not in post:
                continue
            
            onepost = post

            onepost.strip()
            line_items = onepost.split('+')
        
            post_id, user_id, post_time = line_items[-2], line_items[-3], float(line_items[0])

            self.unordered_trace.append((post_time, post))
            # generate view trace
            view_trace = ic.propagation(self.G, user_id, self.propagation_interval, self.activate_prob, self.max_iteration)
            #print(view_trace)

            for view in view_trace:
                # view_time, viewer_id, post_id 
                self.unordered_trace.append((view[0] + post_time, view[1], post_id))
            
            log_count += 1
            if log_count % 100 == 0:
                print("log_count: %d" %(log_count))
    
    def export_trace(self):
        # sort by time
        sorted_trace = sorted(self.unordered_trace, key=lambda x: x[0])

        # export trace
        with open(self.output_path, 'w+') as output_fd:
            log_count = 0
            for trace in sorted_trace:
                if (log_count % 100000) == 0:
                    print("log_count: %d" %(log_count))
                if 'post' in trace[1]:
                    # get post trace
                    output_fd.write(trace[1])
                else:
                    # get view trace
                    view_time, viewer_id, post_id = trace
                    location = self.G.nodes[viewer_id]['location']

                    item_line = "%s+%s+{'lat': '%.2f', 'lon': '%.2f'}+%s+view\n"\
                            %(str(view_time), \
                            post_id, \
                            location[0], location[1], \
                            viewer_id)
                    output_fd.write(item_line)
            
                log_count += 1
        
        print("output file: %s" %(self.output_path))

if __name__ == "__main__":
    print("make twitter trace")
    twitter_file = "TwitterEgo"
    mtt = make_twitter_trace("./data/traces/" + twitter_file +"/all_timeline.txt")
    mtt.load_graph("./data/traces/" + twitter_file + "/relations.txt")
    mtt.load_location("./data/static/user_country.csv")
    mtt.load_post("./data/traces/" + twitter_file + "/all_timeline.txt")
    mtt.gen_trace()
    mtt.export_trace()


            
