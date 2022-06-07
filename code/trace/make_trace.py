import os
import numpy as np
import pandas as pd
import easygraph as eg
import random

class Make_trace:
    def __init__(self, user_number=100, edge_create_probability=0.3):
        ## 100个用户，随机连边
        self.user_number = user_number
        self.edge_create_probability = edge_create_probability
        self.start_time = 1000000000
        self.end_time = 1000010000
    
    def make_friend_relations(self, dir_name):
        '''建立好友关系连边'''
        file_path = "data/traces/" + dir_name + "/relations.txt"
        eg.fast_erdos_renyi_P(self.user_number, self.edge_create_probability, directed=True, FilePath=file_path)

        G = eg.DiGraph()
        G.add_edges_from_file(file_path)
        self.in_degree_dict = G.in_degree()
        # print(in_degree_dict)

    def make_posts_trace(self, dir_name):
        '''建立发布的轨迹，时间+地点+图片大小'''
        dir_path = "data/traces/" + dir_name + "/tweet_posts/"
        os.system("mkdir -p " + dir_path)

        locations = [{'lat': '23.5', 'log': '90.0'}, {'lat': '-23.5', 'log': '-60.0'}, {'lat': '66.75', 'log': '30.0'}, {'lat': '50.34', 'log': '2.05'}]
        for user_id in range(self.user_number):
            filename = dir_path + str(user_id) + ".txt"
            f_out = open(filename, "w")
            now_time = self.start_time + random.randint(0, 1000)
            while now_time < self.end_time:
                media_size = random.randint(0, 2)  * random.uniform(10.0, 60.0)
                time_interval = random.randint(100, 50 * int(self.in_degree_dict[str(user_id)])) # 发帖间隔
                curr_location = random.choice(locations)
                
                print(str(now_time) + '+' + str(media_size) + '+' + str(curr_location), file=f_out)
                now_time += time_interval

    def make_checkins(self, dir_name):
        '''建立登陆的轨迹，check_in时间+随机浏览最近发帖的好友/附近的图片'''
        dir_path = "data/traces/" + dir_name + "/checkins/"
        os.system("mkdir -p " + dir_path)

        for user_id in range(self.user_number):
            filename = dir_path + str(user_id) + ".txt"
            f_out = open(filename, "w")
            now_time = self.start_time + random.randint(0, 1000)
            while now_time < self.end_time:
                time_interval = random.randint(10, 50 * int(self.in_degree_dict[str(user_id)])) # 登陆间隔
                friends_read = random.randint(10, 50)
                nearby_read = random.randint(2, 10)
                
                print(str(now_time) + '+' + str(friends_read) + '+' + str(nearby_read), file=f_out)
                now_time += time_interval


    def run(self, dir_name):
        os.system("mkdir -p data/traces/" + dir_name)
        self.make_friend_relations(dir_name)
        self.make_posts_trace(dir_name)
        self.make_checkins(dir_name)

 
if __name__ == '__main__':
    m = Make_trace()
    m.run('naive')
