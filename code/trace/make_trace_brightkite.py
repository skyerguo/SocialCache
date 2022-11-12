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
    def __init__(self, location_filename, relation_filename, output_filename):
        # Inter-activity time distribution
        self.lognormal_mu       = 1.789
        self.lognormal_theta    = 2.366
        
        self.near_ratio = 5 # 5%看附近，95%看朋友
        self.location_filename   = location_filename
        self.relation_filename   = relation_filename
        self.output_filename = output_filename

        self.media_size = sp.media_size_sample()
    
    
    def load_network(self, filename, use_community, new_filename):
        # self.G = eg.Graph()
        # self.G.add_edges([(1,2),(2,3),(3,4),(1,5),(5,6),(5,7),(6,7)])
        self.G = eg.DiGraph()
        self.G.add_edges_from_file(filename)
        if use_community:
            communities = eg.greedy_modularity_communities(self.G)
            largest_community = communities[0]
            self.G = self.G.nodes_subgraph(largest_community)
            with open(new_filename, "w") as f_out: ## 更新relations
                for temp_edge in self.G.edges:
                    print(temp_edge[0], temp_edge[1], file=f_out)
        print("nodes number: ", self.G.number_of_nodes())
        
    def load_checkins(self, filename, use_community):
        self.checkins = []
        temp_timeline = []
        
        self.start_time = 1262275200 #2010-1-1
        self.end_time = 1264953600 #2010-2-1
        
        # cnt = 240
        with open(filename, "r") as f_in:
            for line in f_in:
                line_list = line.strip().split('\t')
                if len(line_list) < 4: # 清洗错误数据
                    continue
                user_id = int(line_list[0])
                timestamp = int(datetime.datetime.timestamp(datetime.datetime.strptime(line_list[1], '%Y-%m-%dT%H:%M:%SZ')))
                latitude = line_list[2]
                longtitude = line_list[3]
                if timestamp > self.end_time or timestamp < self.start_time:
                    continue
                if use_community and user_id not in self.G.nodes:
                    continue
                self.checkins.append([user_id, timestamp, {'lat': latitude, 'lon': longtitude}])
                # temp_timeline.append(timestamp)
                # cnt -= 1
                # if cnt < 0:
                #     break
                
        self.checkins = sorted(self.checkins, key=lambda x: (x[0], x[1])) # sorted by first user, second timestamp
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
        
        self.posts = sorted(self.posts, key=lambda x: x[0]) # sorted by timestamp
        for i in range(len(self.posts)): # 重新赋值post_id
            self.posts[i][4] = i
        self.views = sorted(self.views, key=lambda x: x[0]) # sorted by timestamp
        
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
        
        
    def output_requests(self):
        point_post = 0
        point_view = 0
        post_number = len(self.posts)
        view_number = len(self.views)
        
        with open(self.output_filename, "w") as f_out:
            while point_post < post_number and point_view < view_number:
                if self.posts[point_post][0] < self.views[point_view][0]:
                    '''每条POST信息为0+1+2+3+4+5，0为时间戳，1为媒体文件大小，2为发布地理位置，3为用户id，4为post_id, 5为post标记'''
                    item = self.posts[point_post]
                    f_out.write(str(item[0]) + '+' + str(item[1]) + '+' + str(item[2]) + '+' + str(item[3]) + '+' + str(item[4]) + '+' + 'post\n')
                    point_post += 1
                else:
                    '''每条VIEW信息为0+1+2+3+4，0为时间戳，1为post_id，2为checkin的地理位置, 3为用户id，4为view标记'''
                    item = self.views[point_view]
                    if item[1] != -1: # 有对应post_id的view，才生效
                        f_out.write(str(item[0]) + '+' + str(item[1]) + '+' + str(item[2]) + '+' + str(item[3]) + '+' + 'view\n')
                    point_view += 1
                    
            while point_post < post_number:
                '''每条POST信息为0+1+2+3+4+5，0为时间戳，1为媒体文件大小，2为发布地理位置，3为用户id，4为post_id, 5为post标记'''
                item = self.posts[point_post]
                f_out.write(str(item[0]) + '+' + str(item[1]) + '+' + str(item[2]) + '+' + str(item[3]) + '+' + str(item[4]) + '+' + 'post\n')
                point_post += 1
                
            while point_view < view_number:
                '''每条VIEW信息为0+1+2+3+4，0为时间戳，1为post_id，2为checkin的地理位置, 3为用户id，4为view标记'''
                item = self.views[point_view]
                if item[1] != -1: # 有对应post_id的view，才生效
                    f_out.write(str(item[0]) + '+' + str(item[1]) + '+' + str(item[2]) + '+' + str(item[3]) + '+' + 'view\n')
                point_view += 1
                
        print("output_requests done!")
            
            
    def launch(self, use_community, new_filename):
        self.load_network(self.relation_filename, use_community=use_community, new_filename=new_filename)
        self.load_checkins(self.location_filename, use_community=use_community)
        self.generate_initials()
        self.finish_views()
        self.output_requests()
        
    
if __name__ == "__main__":
    argpar = argparse.ArgumentParser(description="Make trace data for the system.")
    argpar.add_argument('-G', help="add 'big' to use full usernet, generate to generate a community")
    args = argpar.parse_args()
    if args.G == 'big':
        location_filename = "/proj/socnet-PG0/rawdata/LBSN-Brightkite/loc-brightkite_totalCheckins.txt"
        relation_filename = "./data/traces/LBSN_Brightkite_Bigraph/relations.txt"
        output_filename = "./data/traces/LBSN_Brightkite_Bigraph/all_timeline.txt"
        trace_data = gen_trace_data(location_filename, relation_filename, output_filename)
        trace_data.launch(use_community=False, new_filename="")
        
    elif args.G == "small":
        location_filename = "/proj/socnet-PG0/rawdata/LBSN-Brightkite/loc-brightkite_totalCheckins.txt"
        relation_filename = "./data/traces/LBSN_Brightkite_Bigraph_Community/relations.txt"
        output_filename = "./data/traces/LBSN_Brightkite_Bigraph_Community/all_timeline.txt"
        trace_data = gen_trace_data(location_filename, relation_filename, output_filename)
        trace_data.launch(use_community=False, new_filename="")
        
    elif args.G == "generate":
        location_filename = "/proj/socnet-PG0/rawdata/LBSN-Brightkite/loc-brightkite_totalCheckins.txt"
        relation_old_filename = "./data/traces/LBSN_Brightkite_Bigraph/relations.txt"
        relation_new_filename = "./data/traces/LBSN_Brightkite_Bigraph_Community/relations.txt"
        output_filename = "./data/traces/LBSN_Brightkite_Bigraph_Community/all_timeline.txt"
        trace_data = gen_trace_data(location_filename, relation_old_filename, output_filename)
        trace_data.launch(use_community=True, new_filename=relation_new_filename)
