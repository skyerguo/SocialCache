import os

data_root_path = '/proj/socnet-PG0/data/'

for file_name in os.listdir('./data/results/analyse_data/'):
    # print(file_name)
    os.system("cp -r %s %s"%(data_root_path+file_name, './data/results/origin_data/'+file_name))