import os
import pickle
import sys
import copy
import code.util.util as util

class Opt_eviction:
    def __init__(self, trace_dir, level_3_area_location, cache_id):
        self.level_3_area_location = level_3_area_location
        self.cache_id = cache_id
        
        self.viewlog_dict = {}
        if not os.path.isfile(trace_dir + "viewlog_" + str(cache_id) + ".pkl"):
            self.viewlog_dict = self.build_viewlog_dict(trace_dir + "all_timeline.txt", trace_dir + "viewlog_" + str(cache_id) + ".pkl")
        else:
            with open(trace_dir + "viewlog_" + str(cache_id) + ".pkl", "rb") as tf:
                self.viewlog_dict = pickle.load(tf)
        # print("2333", self.level_3_area_location)
        # print("????", self.viewlog_dict[2][13])

    def build_viewlog_dict(self, rd_filename, wr_filename):
        post_viewlog_dict = {}
        with open(rd_filename, "r") as fd_in:
            lines = fd_in.readlines()
            for line in lines:
                # skip post item
                if line.find("view") == -1:
                    continue

                line_elems = line.split("+")
                timestamp = int(line_elems[0])
                post_id = int(line_elems[1])
                current_location = eval(line_elems[2])
                selected_level_3_id = util.find_nearest_location(current_location, self.level_3_area_location)[0]
                
                '''只考虑会到当前CDN节点的view请求'''
                if selected_level_3_id != self.cache_id:
                    continue
                
                # if self.cache_id == 2 and post_id == 13 and timestamp < 15000:
                #     print(line, timestamp)

                if not post_viewlog_dict.__contains__(post_id):
                    post_viewlog_dict[post_id] = []

                post_viewlog_dict[post_id].append(timestamp)

        '''save result to file'''
        with open(wr_filename, "wb") as tf:
            pickle.dump(post_viewlog_dict, tf)
        
        return post_viewlog_dict

    def request_all(self, id_list, current_time):
        opt_rank_list = []        
        for post_id in id_list:
            view_sequence = self.viewlog_dict[post_id]
            next_view_time = self.binary_search(view_sequence, current_time)
            # print("Post ID: ", post_id, "Next View: ", next_view_time)
            opt_rank_list.append((post_id, next_view_time))

        opt_rank_list.sort(key=lambda elem:elem[1], reverse=True)

        return opt_rank_list

    def request_latest(self, id_list, current_time):
        latest_next_view_time = 0
        res_post_id = 0
        for post_id in id_list:
            if post_id not in self.viewlog_dict:
                next_view_time = sys.maxsize
            else:
                view_sequence = self.viewlog_dict[post_id]
                next_view_time = self.binary_search(view_sequence, current_time)
            
            if next_view_time > latest_next_view_time:
                latest_next_view_time = copy.deepcopy(next_view_time)
                res_post_id = copy.deepcopy(post_id)

        return (res_post_id, latest_next_view_time)

    def binary_search(self, view_sequence, current_time):
        view_sequence.append(sys.maxsize)
        for item in view_sequence:
            if item > current_time:
                return item
            
        left, right = 0, len(view_sequence) - 1
        
        while left < right:
            mid = (left + right) >> 1
            if view_sequence[mid] < current_time:
                left = mid + 1
            else:
                right = mid
        
        return view_sequence[left]

if __name__ == "__main__":
    print("Run as single process.")
    opt = Opt_eviction("data/traces/TwitterSmall/")
    # print(opt.viewlog_dict[174])
    # print(opt.viewlog_dict[45])
    # print(opt.viewlog_dict[118])
    test_res = opt.request_all([174, 45, 118], 10000)
    print(test_res)


'''
def unit_test():
    li = [2, 4, 6, 8, 10, sys.maxsize]
    tar = 4

    left , right = 0, len(li)
    while left < right:
        mid = (left + right) >> 1
        if li[mid] < tar:
            left = mid + 1
        else:
            right = mid
    
    print("left ", li[right])

unit_test()
def uint_test2():
    li = [(1,10), (2, 9), (3, 8)]
    li.sort(key=lambda elem:elem[1], reverse=True)

    print(li)

uint_test2()
'''