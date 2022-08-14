import argparse
import os
import json

data_root = '/proj/socnet-PG0/data/'
files = os.listdir(data_root)
files = sorted(files, reverse=True)
print(files[0])

# if __name__ == '__main__':
#     p = argparse.ArgumentParser(description='Analyze the result')
#     p.add_argument('-p', '--port', type=int, default=8000, dest="port", action="store", help="the port for the http service to listen on")
#     p.add_argument('-l', '--listen', type=str, default="0.0.0.0", dest="listen", action="store", help="the interface to bind to")
#     p.add_argument('-n', '--no-ssl', action="store_true", default=False, dest="nossl", help="do not serve https / ssl")
#     p.add_argument('-d', '--debug', action="store_true", default=False, help="use debug model to print some more logs")
#     args = p.parse_args()