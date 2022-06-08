import os
import numpy as np
import pandas as pd
import easygraph as eg
import random

class Make_trace:
    def __init__(self, dir_name, user_number=100, edge_create_probability=0.3, ):
        ## 100个用户，随机连边
        self.user_number = user_number
        self.edge_create_probability = edge_create_probability
        self.start_time = 1000000000
        self.end_time = 1000010000
        self.dir_name = dir_name
    
    def make_friend_relations(self):
        '''建立好友关系连边'''
        file_path = "data/traces/" + self.dir_name + "/relations.txt"
        eg.fast_erdos_renyi_P(self.user_number, self.edge_create_probability, directed=True, FilePath=file_path)

        G = eg.DiGraph()
        G.add_edges_from_file(file_path)
        self.in_degree_dict = G.in_degree()

    def make_posts_trace(self):
        '''建立发布的轨迹，时间+地点+图片大小'''
        dir_path = "data/traces/" + self.dir_name + "/tweet_posts/"
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

    def make_checkins(self):
        '''建立登陆的轨迹，check_in时间+随机浏览最近发帖的好友/附近的图片'''
        dir_path = "data/traces/" + self.dir_name + "/checkins/"
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


    def get_posts_timeline(self):
        '''将posts合成一个序列，返回一个list'''
        posts_all = []
        posts_dir_path = "data/traces/" + self.dir_name + "/tweet_posts/"
        files = os.listdir(posts_dir_path)
        for file_name in files:
            f_in = open(posts_dir_path + file_name, "r")
            for line in f_in:
                posts_all.append(line.strip()+'+posts')
        posts_all.sort(key=lambda x:x.split("+")[0])
        return posts_all

    def get_views_timeline(self):
        '''将check_in数据生成合理的浏览序列，返回一个lists'''
        views_all = []
        checkins_dir_path = "data/traces/" + self.dir_name + "/checkins/"
        files = os.listdir(checkins_dir_path)
        for file_name in files:
            f_in = open(checkins_dir_path + file_name, "r")
            for line in f_in:
                checkin_time = int(line.split("+")[0])
                friend_view_number = int(line.split("+")[1]) ## 访问好友的posts数量
                nearby_view_number = int(line.split("+")[2]) ## 访问附近地理位置的posts数量
                view_order = [x for x in range(friend_view_number+nearby_view_number)]
                random.shuffle(view_order)
                

    
    def synthesis_timeline(self):
        '''按照时间顺序，合成一个序列'''

        posts_timeline = self.get_posts_timeline()
        views_timeline = self.get_views_timeline()


    def run(self):
        os.system("mkdir -p data/traces/" + self.dir_name)
        
        # self.make_friend_relations()
        # self.make_posts_trace()
        # self.make_checkins()
        self.synthesis_timeline()

 
if __name__ == '__main__':
    m = Make_trace('naive')
    m.run()
