import random
import argparse
import code.util.media_size_sample.media_size_sample as sp
import numpy as np
import pandas as pd
import easygraph as eg
import matplotlib.pyplot as plt
import pickle
import math
import code.trace.trace_utils as trace_utils

class gen_trace_data:
    def __init__(self, edge_file="edges.dat", loc_file="loc.dat", res_path="./", zipf_size=2000):
        # The number of clusters that users are divided into using the K-means algorithm
        # self.cluster    = 7

        # Parameters of zipf distribution of user activities, zipf(x) = zipf_B * pow(x, -zipf_A)
        self.zipf_A     = 1.765
        self.zipf_B     = 4.888
        self.zipf_size  = zipf_size
        self.zipf_start_point = 10

        print("zipf_size: ", self.zipf_size)
        
        # Inter-activity time distribution
        self.lognormal_mu       = 1.789
        self.lognormal_theta    = 2.366

        self.pub_ratio  = 0.05
        self.near_ratio = 5
        self.edge_file  = edge_file
        self.loc_file   = loc_file
        self.res_path   = res_path

        self.media_size = sp.media_size_sample()
    
    def load_network(self, filename):
        self.G = eg.DiGraph()
        self.G.add_edges_from_file(filename)
    
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
        # print(self.locations)

    def build_user_df(self):
        # calculate degree of user
        social_dict = self.G.in_degree()
        # social_dict = pickle.load(open('./data/social_metric_dict/gtc_long_trace/PageRank.pkl', "rb"))
        
        self.user_df = pd.DataFrame(dict(user_id=list(social_dict.keys()), user_influence=list(social_dict.values())))
        rank_degree = {}
        temp_rank_degree = sorted(np.unique(list(social_dict.values())), reverse=True)
        for i in range(len(temp_rank_degree)):
            rank_degree[temp_rank_degree[i]] = i + self.zipf_start_point
        
        # min_zipf_number = self.zipf_B * pow(len(temp_rank_degree), -self.zipf_A)
        max_zipf_number = self.zipf_B * pow(self.zipf_start_point, -self.zipf_A)
        # print(min_zipf_number)

        self.user_df["activity_number"] = [int(self.zipf_B * pow(rank_degree[social_dict[x]], -self.zipf_A) / max_zipf_number * (self.zipf_size)) for x in self.user_df['user_id']]

        # print(self.user_df)
        # print([int(self.zipf_B * pow(rank_degree[social_dict[x]], -self.zipf_A) / max_zipf_number * (self.zipf_size)) for x in self.user_df['user_id']])
        # exit(0)
    
    def gen_activity_df(self, activity_num):
        time_list       = []
        loc_list        = [] 
        media_size_list = []
        kind_list = np.random.binomial(1, self.pub_ratio, activity_num)
        media_size_list = self.media_size.sample(activity_num)
        activity_interval = np.random.lognormal(self.lognormal_mu, self.lognormal_theta, self.zipf_size)
        time = 0
        curr_mod = math.floor(self.zipf_size / activity_num)
        start_point = random.randint(0, curr_mod)
        cnt = start_point
        for interval in activity_interval:
            time += int(interval * 10)
            if (cnt - start_point) % curr_mod == 0:
                time_list.append(time)
                loc_list.append(random.choice(self.location_list))
            if len(time_list) == activity_num:
                break
            cnt += 1
        # print(len(time_list), len(kind_list), len(media_size_list), len(loc_list), activity_num)
        return pd.DataFrame(dict(timestamp=time_list, publish=kind_list, media_size=media_size_list, location=loc_list)), time

    def build_user_activity(self):
        user_act_dict = {}
        self.user_postline_dict = {}
        max_duration = 0
        self.df_trace = pd.DataFrame(columns=["timestamp", "publish", "media_size", "location", "user_id"])
        for rowidx, row in self.user_df.iterrows():
            if rowidx % 100 == 0:
                print("rowidx: ", rowidx)

            user_id = row["user_id"]
            df, duration = self.gen_activity_df(int(row["activity_number"]))
            df["user_id"] = user_id
            #print(df)
            user_act_dict[user_id] = df
            max_duration = max(max_duration, duration)
            self.df_trace = pd.concat([self.df_trace, df])
        
        # shift timestamp of users' activity sequence 
        self.df_trace = self.df_trace.sort_values(by="timestamp").reset_index(drop=True)
    
    def trans_trace2timeline(self):
        # init data
        print("trans trace data to all_timeline")
        user_postline_dict  = {}
        position_post_dict  = {}
        
        user_viewed_post_list_dict = {}
        user_adj_post_list_dict = {}

        for user in self.G.nodes:
            user_postline_dict[user] = []
            user_viewed_post_list_dict[user] = []
            user_adj_post_list_dict[user] = []

        for loc in self.locations:
            position_post_dict[loc] = []

        fd = open(self.res_path + "all_timeline.txt", "w+")
        post_seq_num = -1
        last_view_id = -1
        last_user_id = -1

        line_number = 0

        for rowidx, row in self.df_trace.iterrows():
            item_line = str(row["timestamp"])
            curr_user_id = str(row["user_id"])

            if row["publish"] == 1:
                # get a post item
                post_seq_num += 1

                user_postline_dict[curr_user_id].append(post_seq_num)
                
                position_post_dict[row["location"]].append(post_seq_num)
                item_line += "+%s+{'lat': '%.2f', 'lon': '%.2f'}+%s+%d+post"\
                            %(str(row["media_size"] / 1024),\
                            row["location"][0], row["location"][1],\
                            curr_user_id,\
                            post_seq_num)
                for adj_user in list(self.G.predecessors(curr_user_id)): # 对当前节点的predecessors（存在入边的节点）进行更新
                    user_adj_post_list_dict[adj_user].append(post_seq_num)
            else:
                # get a view item
                viewid  = -1

                coin = random.randint(1, 100)
                if coin <= self.near_ratio:
                    # nearby view
                    loc_post_list = position_post_dict[row["location"]]
                    if loc_post_list:
                        viewid = loc_post_list[-1]
                else:
                    # friend view
                    viewed_post_id = trace_utils.get_neareast_friend_post(curr_user_id, user_adj_post_list_dict[curr_user_id], user_viewed_post_list_dict[curr_user_id])
                    if viewed_post_id:
                        user_viewed_post_list_dict[curr_user_id].append(viewed_post_id)
                        viewid = viewed_post_id

                if viewid != -1:
                    # valid view
                    item_line += "+%d+{'lat': '%.2f', 'lon': '%.2f'}+%s+view"\
                            %(viewid, \
                            row["location"][0], row["location"][1], \
                            curr_user_id)
                else:
                    # ignore invalid view
                    continue
            fd.write(item_line + '\n')
            line_number += 1
            # if line_number % 1000 == 0:
                # print("line_number: ", line_number)
        fd.close()
        print("line_number: ", line_number)

    def launch(self):
        self.load_network(self.res_path + "relations.txt")
        self.load_location(self.loc_file)
        self.build_user_df()
        self.build_user_activity()
        self.trans_trace2timeline()
    
if __name__ == "__main__":
    argpar = argparse.ArgumentParser(description="Make trace data for the system.")
    argpar.add_argument('-G', help="add 'big' to use full usernet")
    args = argpar.parse_args()
    # print(type(args.G))
    if args.G == 'big':
        print("use big net")
        usernet_filename = "./data/static/twitter_combined.txt"
        res_path = "./data/traces/TwitterFull/"
        zipf_size = 5000
    else:
        print("use litte net")
        usernet_filename = "./data/static/twitter_single.txt"
        res_path = "./data/traces/TwitterEgo/"
        zipf_size = 2000
    trace_data = gen_trace_data(usernet_filename, "./data/static/user_country.csv", res_path, zipf_size)
    trace_data.launch()
