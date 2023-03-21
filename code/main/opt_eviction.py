import os
import pickle
import sys

class opt_eviction:
    def __init__(self, trace_dir):
        self.viewlog_dict = {}
        if not os.path.isfile(trace_dir + "viewlog.pkl"):
            self.viewlog_dict = self.build_viewlog_dict(trace_dir + "all_timeline.txt", trace_dir + "viewlog.pkl")
        else:
            with open(trace_dir + "viewlog.pkl", "rb") as tf:
                self.viewlog_dict = pickle.load(tf)

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
                post_id = int(line_elems[-2])

                if not post_viewlog_dict.__contains__(post_id):
                    post_viewlog_dict[post_id] = []

                post_viewlog_dict[post_id].append(timestamp)
            
            # append a infinite number in the end for critical case
            for key, val in post_viewlog_dict.items():
                val.append(sys.maxsize)

        # save result to file
        with open(wr_filename, "wb") as tf:
            pickle.dump(post_viewlog_dict, tf)
        
        return post_viewlog_dict

    def request(self, id_list, current_time):
        opt_rank_list = []        
        for post_id in id_list:
            view_sequence = self.viewlog_dict[post_id]
            next_view_time = self.binary_search(view_sequence, current_time)
            print("Post ID: ", post_id, "Next View: ", next_view_time)
            opt_rank_list.append((post_id, next_view_time))

        opt_rank_list.sort(key=lambda elem:elem[1], reverse=True)

        return opt_rank_list

    def binary_search(self, view_sequence, current_time):
        left, right = 0, len(view_sequence)
        
        while left < right:
            mid = (left + right) >> 1
            if view_sequence[mid] < current_time:
                left = mid + 1
            else:
                right = mid
        
        return view_sequence[right]

if __name__ == "__main__":
    print("Run as single process.")
    opt = opt_eviction("../../data/traces/TwitterSmall/")
    print(opt.viewlog_dict[174])
    print(opt.viewlog_dict[45])
    print(opt.viewlog_dict[118])
    test_res = opt.request([174, 45, 118], 10000)
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