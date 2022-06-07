from socket import timeout
import urllib.request

def repeat_get_res():
    input_path = './media_url_size.txt'
    output_path = './media_url_size_new.txt'

    f_in = open(input_path, "r")
    f_out = open(output_path, "w")
    for line in f_in:
        curr_url = line.split(" ")[0]
        curr_size = int(line.split(" ")[1])
        if curr_size != 0: ## 如果计算过，就不管了
            print(curr_url, curr_size, file=f_out)
            continue
        
        temp_req = urllib.request.Request(curr_url, method='HEAD') 
        temp_f = urllib.request.urlopen(temp_req, timeout=3)
        curr_size = int(temp_f.headers['Content-Length'])
        print(curr_url, curr_size, file=f_out)

    f_in.close()


def get_from_raw():
    input_path = '../data/Twitter/total_url.txt'
    output_path = './media_url_size.txt'
    
    f_in = open(input_path, "r")
    f_out = open(output_path, "w")
    for line in f_in:
        curr_url = line.split('"')[1]
        curr_size = 0
        temp_req = urllib.request.Request(curr_url, method='HEAD') 
        temp_f = urllib.request.urlopen(temp_req, timeout=3)## 只需要报头，设置3秒的超时
        curr_size = int(temp_f.headers['Content-Length'])
        # try:
        #     temp_req = urllib.request.Request(curr_url, method='HEAD') 
        #     temp_f = urllib.request.urlopen(temp_req, timeout=3)## 只需要报头，设置3秒的超时
        #     curr_size = int(temp_f.headers['Content-Length'])
        # except:
        #     pass
        print(curr_url, curr_size, file=f_out)
        break
        
get_from_raw()