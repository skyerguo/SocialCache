import os
import numpy as np
import pandas as pd
import easygraph as eg
import random
import code.util.util as util

class Make_trace:
    def __init__(self, dir_name, user_number=1000, edge_create_probability=0.3,):
        ## 100个用户，随机连边
        self.user_number = user_number
        self.edge_create_probability = edge_create_probability
        self.start_time = 1000000000
        self.end_time = 1000010000
        self.dir_name = dir_name
        self.G = eg.DiGraph()
    
    def make_friend_relations(self):
        '''建立好友关系连边'''
        file_path = "data/traces/" + self.dir_name + "/relations.txt"
        eg.fast_erdos_renyi_P(self.user_number, self.edge_create_probability, directed=True, FilePath=file_path)

        self.G.add_edges_from_file(file_path)
        self.in_degree_dict = self.G.in_degree()
        print(self.in_degree_dict)

    def make_posts(self):
        '''建立发布的轨迹，时间+地点+图片大小'''
        dir_path = "data/traces/" + self.dir_name + "/tweet_posts/"
        os.system("mkdir -p " + dir_path)

        locations = [{'lat': '23.5', 'lon': '90.0'}, {'lat': '-23.5', 'lon': '-60.0'}, {'lat': '66.75', 'lon': '30.0'}, {'lat': '50.34', 'lon': '2.05'}]
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
            f_out.close()

    def make_checkins(self):
        '''建立登陆的轨迹，check_in时间+随机浏览最近发帖的好友/附近的图片'''
        dir_path = "data/traces/" + self.dir_name + "/checkins/"
        os.system("mkdir -p " + dir_path)

        locations = [{'lat': '23.5', 'lon': '90.0'}, {'lat': '-23.5', 'lon': '-60.0'}, {'lat': '66.75', 'lon': '30.0'}, {'lat': '50.34', 'lon': '2.05'}]

        for user_id in range(self.user_number):
            filename = dir_path + str(user_id) + ".txt"
            f_out = open(filename, "w")
            now_time = self.start_time + random.randint(0, 1000)
            while now_time < self.end_time:
                time_interval = random.randint(200, 50 * int(self.in_degree_dict[str(user_id)])) # 登陆间隔
                friends_read = random.randint(5, 30)
                nearby_read = random.randint(2, 5)
                curr_location = random.choice(locations)
                
                print(str(now_time) + '+' + str(curr_location) + '+' + str(friends_read) + '+' + str(nearby_read), file=f_out)
                now_time += time_interval
            f_out.close()

    def binary_search_latest(self, timestamp):
        '''找到timestamp之前的最后一个post的id'''
        low_id = 0; high_id = len(self.posts_timeline); 
        while low_id < high_id:
            mid_id = int((low_id+high_id+1)/2)
            if int(self.posts_timeline[mid_id].split("+")[0]) < timestamp:
                low_id = mid_id
            else:
                high_id = mid_id - 1
        return low_id

    def get_friend_latest_posts(self, current_time, number, user_id):
        '''获得从某个时间开始，最长为number的朋友的post'''
        views_friend = []
        latest_id = self.binary_search_latest(current_time)
        for post_id in range(latest_id, 0, -1):
            current_post = self.posts_timeline[post_id]
            current_post_user_id = int(current_post.split("+")[3])
            if self.G.has_edge(str(user_id), str(current_post_user_id)): ## 如果这个帖子是由你关注的人发布的
                views_friend.append(post_id)
                if len(views_friend) >= number:
                    return views_friend
        return views_friend

    def get_nearby_latest_posts(self, current_time, number, user_location):
        views_nearby = []
        latest_id = self.binary_search_latest(current_time)
        for post_id in range(latest_id, 0, -1):
            current_post = self.posts_timeline[post_id]
            current_post_user_location = eval(current_post.split("+")[2])
            '''只看附近10km内的'''
            if util.calc_geolocation_distance(user_location, current_post_user_location) <= 10:
                views_nearby.append(post_id)
                if len(views_nearby) >= number:
                    return views_nearby
        return views_nearby


    def get_posts_timeline(self):
        '''将posts合成一个序列，返回一个list'''
        posts_all = []
        posts_dir_path = "data/traces/" + self.dir_name + "/tweet_posts/"
        files = os.listdir(posts_dir_path)
        for file_name in files:
            f_in = open(posts_dir_path + file_name, "r")
            for line in f_in:
                posts_all.append(line.strip()+'+'+file_name.split(".")[0])
            f_in.close()

        '''每条信息为a+b+c+d+e+f，a为时间戳，b为媒体文件大小，c为发布地理位置，d为用户id，e为post_id, f为post标记'''
        posts_all.sort(key=lambda x:x.split("+")[0])
        for post_id in range(len(posts_all)):
            posts_all[post_id] = posts_all[post_id] + '+' + str(post_id) + '+' + 'post'
        return posts_all


    def get_views_timeline(self):
        '''将check_in数据生成合理的浏览序列，返回一个lists'''
        views_all = []
        checkins_dir_path = "data/traces/" + self.dir_name + "/checkins/"
        files = os.listdir(checkins_dir_path)
        for file_name in files:
            f_in = open(checkins_dir_path + file_name, "r")
            user_id = int(file_name.split(".")[0])
            for line in f_in:
                checkin_time = int(line.split("+")[0])
                user_location = eval(line.split("+")[1]) ## 登陆的地理位置
                friend_view_number = int(line.split("+")[2]) ## 访问好友的posts数量
                nearby_view_number = int(line.split("+")[3]) ## 访问附近地理位置的posts数量
                
                views_friend = self.get_friend_latest_posts(checkin_time, friend_view_number, user_id)
                views_nearby = self.get_nearby_latest_posts(checkin_time, nearby_view_number, user_location)

                '''如果没那么多posts，相当于一个取min操作'''
                friend_view_number = len(views_friend) 
                nearby_view_number = len(views_nearby) 

                '''随机访问friend和nearby'''
                views_order = [x for x in range(friend_view_number+nearby_view_number)] 
                random.shuffle(views_order)

                '''登陆后，每5秒看一个post''' 
                current_view_time = checkin_time
                for view_step in range(len(views_order)):
                    current_view_time += 5
                    if views_order[view_step] >= friend_view_number: 
                        views_all.append(str(current_view_time) + '+' + str(views_nearby[views_order[view_step] - friend_view_number]) + '+' + str(user_location) + '+' + str(user_id) + '+' + 'view')
                    else:
                        views_all.append(str(current_view_time) + '+' + str(views_friend[views_order[view_step]]) + '+' + str(user_location) + '+' + str(user_id) + '+' + 'view')
            f_in.close()
        '''每条信息为a+b+c+d+e，a为时间戳，b为post_id，c为checkin的地理位置, d为用户id，e为view标记'''
        views_all.sort(key=lambda x:x.split("+")[0])
        return views_all

    
    def synthesis_timeline(self):
        '''按照时间顺序，合成一个序列'''

        self.posts_timeline = self.get_posts_timeline()
        self.views_timeline = self.get_views_timeline()

        '''输出posts按时间排序'''
        f_out = open("data/traces/" + self.dir_name + "/posts_timeline.txt", "w")
        for post_line in self.posts_timeline:
            print(post_line, file=f_out)
        f_out.close()

        '''输出views按时间排序'''
        f_out = open("data/traces/" + self.dir_name + "/views_timeline.txt", "w")
        for view_line in self.views_timeline:
            print(view_line, file=f_out)
        f_out.close()

        '''输出所有的按时间排序'''
        all_timeline = self.posts_timeline + self.views_timeline
        all_timeline.sort(key=lambda x:x.split("+")[0])
        f_out = open("data/traces/" + self.dir_name + "/all_timeline.txt", "w")
        for line in all_timeline:
            print(line, file=f_out)
        f_out.close()

    def run(self):
        os.system("mkdir -p data/traces/" + self.dir_name)
        
        # self.make_friend_relations()
        # self.make_posts()
        # self.make_checkins()
        self.G.add_edges_from_file("data/traces/" + self.dir_name + "/relations.txt")
        self.synthesis_timeline()

# if __name__ == '__main__':
#     m = Make_trace('naive')
#     m.run()
