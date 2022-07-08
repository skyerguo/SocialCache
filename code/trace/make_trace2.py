import random
import media_size_sample.media_size_sample as sp
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

class gen_trace_data:
    def __init__(self, edge_file="edges.dat", loc_file="loc.dat"):
        self.cluster    = 7
        self.zipf_A     = 1.765
        self.zipf_size  = 10000
        self.pub_ratio  = 0.05
        self.lognormal_mu       = 1.789
        self.lognormal_theta    = 2.366
        self.edge_file  = edge_file
        self.loc_file   = loc_file
        self.media_size = sp.media_size_sample()
    
    def load_network(self, filename, output_edge_filename="relations.txt", draw=False):
        self.user_net = nx.DiGraph()
        f_out = open(output_edge_filename, 'w')
        node_max = 0
        with open(filename, encoding='utf-8') as fd:
            newid = 0
            node_dict = {}
            for edge in fd.readlines():
                node1, node2 = int(edge.split()[0]), int(edge.split()[1])
                try:
                    n1 = node_dict[node1]
                except KeyError:
                    node_dict[node1] = newid
                    n1 = newid
                    newid += 1
                try:
                    n2 = node_dict[node2]
                except KeyError:
                    node_dict[node2] = newid
                    n2 = newid
                    newid += 1

                self.user_net.add_edge(n1, n2)
                print("%d %d" %(n1, n2), file=f_out)
                node_max = max(node_max, n1)
                node_max = max(node_max, n2)
                #print("add edge (%d, %d)" %(n1, n2))
        
        print("node_max: ", node_max)
        # dump user network
        if draw:
            nx.draw(self.user_net)
            plt.savefig("user_net.png")
    
    def load_location(self, filename):
        self.country_location = pd.read_csv(filename)
        self.location_list = []

        for rowidx, row in self.country_location.iterrows():
            repeat = [(row["longtitude"], row["latitude"])]*int(row["count"])
            self.location_list.extend(repeat)
        #print(self.location_list)

    def build_user_df(self):
        # calculate pagerank of user
        pr_dict = nx.pagerank(self.user_net)
        self.user_df = pd.DataFrame(dict(user_id=list(pr_dict.keys()), user_influence=list(pr_dict.values())))

        # cluster user influence by k-means
        kmeans = KMeans(n_clusters=self.cluster, random_state=0).fit(np.array(self.user_df["user_influence"]).reshape(-1, 1))
        
        cluster_center  = kmeans.cluster_centers_
        predict_label   = kmeans.labels_

        # label to influence level dict
        cluster_df  = pd.DataFrame(dict(influ=cluster_center.reshape(-1,), label=np.arange(self.cluster)))
        cluster_df  = cluster_df.sort_values(by="influ", axis=0, ascending=False).reset_index(drop=True)
        label_level = dict(zip(cluster_df["label"], cluster_df.index + 1))

        # get influence level for each user
        self.user_df["influence_level"] = [label_level[x] for x in predict_label]

        # zipf distribution
        x = np.random.zipf(a=self.zipf_A, size=self.zipf_size)
        level_nactivity = {}
        for i in range(1, 8):
            level_nactivity[i] = np.count_nonzero(x == i)
        
        self.user_df["activity_number"] = [level_nactivity[x] for x in self.user_df["influence_level"]]
        print(self.user_df)
    
    def gen_activity_df(self, activity_num):
        time_list       = []
        loc_list        = []
        media_size_list = []
        kind_list = np.random.binomial(1, 0.05, activity_num)
        media_size_list = self.media_size.sample(activity_num)
        activity_interval = np.random.lognormal(self.lognormal_mu, self.lognormal_theta, activity_num)
        time = 0
        for interval in activity_interval:
            time += int(interval * 10)
            time_list.append(time)
            loc_list.append(random.choice(self.location_list))


        
        return pd.DataFrame(dict(timestamp=time_list, publish=kind_list, media_size=media_size_list, location=loc_list))

    def build_user_activity(self):
        self.df_trace = pd.DataFrame(columns=["timestamp", "publish", "media_size", "location", "user_id"])
        for rowidx, row in self.user_df.iterrows():
            df = self.gen_activity_df(int(row["activity_number"]))
            df["user_id"] = int(row["user_id"])
            #print(df)
            self.df_trace = pd.concat([self.df_trace, df])
        
        self.df_trace = self.df_trace.sort_values(by="timestamp").reset_index(drop=True)
        print(self.df_trace)
        self.df_trace.to_csv("trace.csv")
    
    def trans_trace2timeline(self):

        fd = open("all_timeline.txt", "w+")
        post_seq_num = 0
        for rowidx, row in self.df_trace.iterrows():
            line = str(row["timestamp"]) + "+" + str(row["media_size"]) + "+{'lat': '%.2f', 'lon': '%.2f'}" %(row["location"][0], row["location"][1]) + "+" + str(row["user_id"])
            if row["publish"] == 1:
                line += "+" + str(post_seq_num) + "+post"
                post_seq_num += 1
            else:
                line += "+view"
            fd.write(line + '\n')

        fd.close()

    def launch(self):
        self.load_network(self.edge_file, draw=True)
        self.load_location(self.loc_file)
        self.build_user_df()
        self.build_user_activity()
        self.trans_trace2timeline()
        
    
if __name__ == "__main__":
    trace_data = gen_trace_data("../../data/traces/myk/edges.dat", "../../data/traces/myk/user_country.csv")
    trace_data.launch()

