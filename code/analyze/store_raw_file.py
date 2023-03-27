import os

raw_file_path = '/proj/socnet-PG0/data/'
analyze_file_path = '/users/gtc/SocialCache/data/results/analyse_data/'
useful_raw_data_path = '/users/gtc/useful_raw_data/'

os.system('mkdir -p %s'%(useful_raw_data_path))

for file_name in os.listdir(analyze_file_path):
    if os.path.exists(raw_file_path + file_name):
        os.system('sudo cp -r %s %s'%(raw_file_path + file_name, useful_raw_data_path))
