import random
import argparse
import code.util.media_size_sample.media_size_sample as sp
import numpy as np
import pandas as pd
import easygraph as eg
import matplotlib.pyplot as plt
import pickle
import math
import datetime
import copy
import seaborn
import code.util.util as util

class gen_trace_data:
    def __init__(self, loc_file, relation_file):
        # Parameters of zipf distribution of user activities, zipf(x) = zipf_B * pow(x, -zipf_A)
        self.zipf_A     = 1.765
        self.zipf_B     = 4.888
        # self.zipf_size  = zipf_size
        self.zipf_start_point = 10

        # Inter-activity time distribution
        self.lognormal_mu       = 1.789
        self.lognormal_theta    = 2.366

        self.pub_ratio  = 0.05
        self.near_ratio = 5 # 5%看附近，95%看朋友
        self.loc_file   = loc_file
        self.relation_file   = relation_file

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

        for user in self.G.nodes:
            user_postline_dict[user] = []

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
                    viewadj = -1
                    adjlist = list(self.G.neighbors(curr_user_id))
                    
                    while adjlist:
                        adj_idx = random.choice(adjlist)
                        user_post_list = user_postline_dict[adj_idx]

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
                        
                        adjlist.remove(adj_idx)

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
        
    def load_checkins(self, filename):
        self.checkins = []
        temp_timeline = []
        
        self.start_time = 1262275200 #2010-1-1
        self.end_time = 1264953600 #2010-2-1
        
        cnt = 240
        with open(filename, "r") as f_in:
            for line in f_in:
                line_list = line.strip().split('\t')
                user_id = int(line_list[0])
                timestamp = int(datetime.datetime.timestamp(datetime.datetime.strptime(line_list[1], '%Y-%m-%dT%H:%M:%SZ')))
                latitude = line_list[2]
                longtitude = line_list[3]
                if timestamp > self.end_time or timestamp < self.start_time:
                    continue
                self.checkins.append([user_id, timestamp, {'lat': latitude, 'lon': longtitude}])
                # temp_timeline.append(timestamp)
                cnt -= 1
                if cnt < 0:
                    break
                
        sorted(self.checkins, key=lambda x: (x[0], x[1])) # sorted by first user, second timestamp
        print("load_checkin done!")
        # util.display_timeline(temp_timeline)
        
        
    
    def generate_initials(self):
        '''
            获取post列表，和view的时间戳以及地点
            假设每次登陆，发布1次帖子，浏览19次帖子
        '''
        media_size_list = self.media_size.sample(len(self.checkins)) ## 根据post个数，生成分布()
        self.posts = []
        self.views = []
        for i in range(len(self.checkins)): 
            post_location = random.randint(0, 19) # post的位置
            
            time_intervals = np.random.lognormal(self.lognormal_mu, self.lognormal_theta, 20)
            temp_delta = [0 for _ in range(20)]
            temp_delta[0] = time_intervals[0] * 10
            for t in range(1, 20):
                temp_delta[t] = temp_delta[t-1] + time_intervals[t] * 10
            
            self.posts.append([self.checkins[i][1] + temp_delta[post_location], media_size_list[i], self.checkins[i][2], self.checkins[i][0], i]) # timestamp, media_size, location, user_id, post_id
            
            for j in range(20):
                if j == post_location:
                    continue
                self.views.append([self.checkins[i][1] + temp_delta[j], -1, self.checkins[i][2], self.checkins[i][0], i]) # timestamp, post_id, location, user_id, checkin_id。需要生成所有post后再通过self.finish_views()完成。此处使用-1暂时填补
        
        sorted(self.posts, key=lambda x: x[0]) # sorted by timestamp
        for i in range(len(self.posts)): # 重新赋值post_id
            self.posts[i][4] = i
        sorted(self.views, key=lambda x: x[0]) # sorted by timestamp
        
        print("generate_initials done!")
        
    def find_location_post(self, start_point, viewed_list, user_id, location, sequence_span=50):
        min_dis = 1e9
        res_post_id = -1
        
        for i in range(start_point, max(start_point - sequence_span, 0), -1):
            if i in viewed_list: # 第i个post被同一次checkin 访问过
                continue
            if self.posts[i][3] == user_id: # 自己不看自己的
                continue
            
            temp_dis = util.calc_geolocation_distance(location, self.posts[i][2])
            if temp_dis < min_dis:
                min_dis = temp_dis
                res_post_id = i
                
        return res_post_id
    
    def find_friend_post(self, start_point, viewed_list, user_id, sequence_span=50):
        for i in range(start_point, max(start_point - sequence_span, 0), -1):
            if i in viewed_list: # 第i个post被同一次checkin 访问过
                continue
            if self.posts[i][3] == user_id: # 自己不看自己的
                continue
            
            if self.G.has_edge(str(user_id), str(self.posts[i][3])):
                return i
            
        return -1
            
           
    def finish_views(self):
        recent_post_id = -1 ## 比当前时间小的，时间最大的的post_id
        posts_number = len(self.posts)
        checkin_viewed = [[] for _ in range(len(self.checkins))] ## 每次checkin，看过哪些post，避免重复看
        
        for i in range(len(self.views)):
            while recent_post_id+1 < posts_number and self.views[i][0] > self.posts[recent_post_id+1][0]:
                recent_post_id += 1
            if recent_post_id == -1:
                continue
            
            if util.random_percentage(5):
                curr_post_id = self.find_location_post(recent_post_id, checkin_viewed[self.views[i][4]], self.views[i][3], self.views[i][2], 50)
            else:
                curr_post_id = self.find_friend_post(recent_post_id, checkin_viewed[self.views[i][4]], self.views[i][3], 50)
                
            if curr_post_id != -1:
                checkin_viewed[self.views[i][4]].append(curr_post_id)
                self.views[i][1] = curr_post_id
        
        print("finish_views done!")

    def launch(self):
        self.load_network(self.relation_file)
        self.load_checkins(self.loc_file)
        self.generate_initials()
        self.finish_views()
        
    
if __name__ == "__main__":
    location_filename = "/proj/socnet-PG0/rawdata/LBSN-Brightkite/loc-brightkite_totalCheckins.txt"
    relation_file = "./data/traces/LBSN_Brightkite_Bigraph/relations.txt"
    trace_data = gen_trace_data(location_filename, relation_file)
    trace_data.launch()
