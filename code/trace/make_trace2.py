import random
import argparse
import code.util.media_size_sample.media_size_sample as sp
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

class gen_trace_data:
    def __init__(self, edge_file="edges.dat", loc_file="loc.dat", res_path="./"):
        # The number of clusters that users are divided into using the K-means algorithm
        self.cluster    = 7

        # Parameters of zipf distribution of user activities
        self.zipf_A     = 1.765
        self.zipf_size  = 10000
        
        # Inter-activity time distribution
        self.lognormal_mu       = 1.789
        self.lognormal_theta    = 2.366

        self.pub_ratio  = 0.05
        self.edge_file  = edge_file
        self.loc_file   = loc_file
        self.res_path   = res_path

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
        self.locations     = []

        for rowidx, row in self.country_location.iterrows():
            longtitude  = float(row["longtitude"])
            latitude    = float(row["latitude"])
            repeat = [(longtitude, latitude)]*int(row["count"])
            self.location_list.extend(repeat)
            self.locations.append((longtitude, latitude))
        #print(self.location_list)
        print(self.locations)

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
        
        return pd.DataFrame(dict(timestamp=time_list, publish=kind_list, media_size=media_size_list, location=loc_list)), time

    def build_user_activity(self):
        user_act_dict = {}
        self.user_postline_dict = {}
        max_duration = 0
        self.df_trace = pd.DataFrame(columns=["timestamp", "publish", "media_size", "location", "user_id"])
        for rowidx, row in self.user_df.iterrows():
            user_id = int(row["user_id"])
            df, duration = self.gen_activity_df(int(row["activity_number"]))
            df["user_id"] = user_id
            #print(df)
            user_act_dict[user_id] = df
            max_duration = max(max_duration, duration)
            self.df_trace = pd.concat([self.df_trace, df])
        
        # shift timestamp of users' activity sequence 
        self.df_trace = self.df_trace.sort_values(by="timestamp").reset_index(drop=True)
        #self.df_trace.to_csv("trace.csv")
    
    def trans_trace2timeline(self):
        # init data
        print("trans trace data to all_timeline")
        user_postline_dict  = {}
        position_post_dict  = {}
        user_adjlist_dict   = {}

        for user in self.user_net.nodes:
            user_postline_dict[user] = []
            adjlist = []
            [adjlist.append(adj) for adj in self.user_net[user]]
            user_adjlist_dict[user] = adjlist
            #print("user %d adjcent :" %user , adjlist)

        for loc in self.locations:
            position_post_dict[loc] = []

        fd = open(self.res_path + "all_timeline.txt", "w+")
        post_seq_num = -1
        last_view_id = -1
        last_user_id = -1

        for rowidx, row in self.df_trace.iterrows():
            item_line = str(row["timestamp"])
            curr_user_id = row["user_id"]
            #line = str(row["timestamp"]) + "+" + str(row["media_size"]) + "+{'lat': '%.2f', 'lon': '%.2f'}" %(row["location"][0], row["location"][1]) + "+" + str(row["user_id"])

            if row["publish"] == 1:
                # get a post item
                print("Get a post item")
                post_seq_num += 1

                user_postline_dict[curr_user_id].append(post_seq_num)
                position_post_dict[row["location"]].append(post_seq_num)
                item_line += "+%s+{'lat': '%.2f', 'lon': '%.2f'}+%d+%d+post"\
                            %(str(row["media_size"] / 1024),\
                            row["location"][0], row["location"][1],\
                            curr_user_id,\
                            post_seq_num)

                #print("user %d current postline : " %curr_user_id, user_postline_dict[curr_user_id])
            else:
                # get a view item
                print("Get a view item")
                viewid  = -1

                coin = random.randint(1, 10)
                if coin == 1:
                    # nearby view
                    # item_line += "+nearby"
                    loc_post_list = position_post_dict[row["location"]]
                    #print("loc", row["location"], "post line:", loc_post_list)
                    if loc_post_list:
                        viewid = loc_post_list[-1]
                else:
                    # friend view
                    # item_line += "+friend"
                    viewadj = -1
                    adjlist = user_adjlist_dict[curr_user_id]
                    while adjlist:
                        # random pick an adjcent
                        #print("current adjlist : ", adjlist)
                        adj_idx = random.choice(adjlist)
                        user_post_list = user_postline_dict[adj_idx]

                        #print("choose adj%d, postline :" %adj_idx, user_post_list)
                        if user_post_list:
                            viewadj = adj_idx

                            # to prevent the situation that the same user always views the same post
                            for i in range(len(user_post_list)):
                                viewid = user_post_list[-(i+1)]
                                if not (viewid == last_view_id and curr_user_id == last_user_id):
                                    break
                            last_view_id = viewid
                            last_user_id = curr_user_id
                            break
                        
                        #print("user %d adj%d's postline is empty ")
                        adjlist.remove(adj_idx)

                if viewid != -1:
                    # valid view
                    item_line += "+%d+{'lat': '%.2f', 'lon': '%.2f'}+%d+view"\
                            %(viewid, \
                            row["location"][0], row["location"][1], \
                            curr_user_id)
                else:
                    # ignore invalid view
                    continue
            fd.write(item_line + '\n')
        fd.close()

    def launch(self):
        self.load_network(self.edge_file, output_edge_filename = self.res_path + "relations.txt", draw=False)
        self.load_location(self.loc_file)
        self.build_user_df()
        self.build_user_activity()
        self.trans_trace2timeline()
    
if __name__ == "__main__":
    argpar = argparse.ArgumentParser(description="Make trace data for the system.")
    argpar.add_argument('-G', help="add 'big' to use full usernet")
    args = argpar.parse_args()
    print(type(args.G))
    if args.G == 'big':
        print("use big net")
        usernet_filename = "./data/static/twitter_combined.txt"
        res_path = "./data/traces/long_trace/"
    else:
        print("use litte net")
        usernet_filename = "./data/static/twitter_single.txt"
        res_path = "./data/traces/short_trace/"
    trace_data = gen_trace_data(usernet_filename, "./data/static/user_country.csv", res_path)
    trace_data.launch()
