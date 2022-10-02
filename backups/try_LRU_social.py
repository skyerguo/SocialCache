from asyncio import FastChildWatcher
import json
import shlex
import subprocess
import random
import os
import time
import pandas as pd
import matplotlib.pyplot as plt

SIMULATION_CMD="sudo python3 -m code.main.main"
ANALYZE_CMD="python3 -m code.analyze.get_media_size -n 0"
BETTER_NUMBER = 5

for i in range(BETTER_NUMBER):
    res = 1e18
    while res > 131342355.81542969:
        os.system(SIMULATION_CMD)

        # run analyzation
        res = float(subprocess.getoutput(ANALYZE_CMD))

        print("!!!!", 131342355.81542969-res)

        if res < 131342355.81542969:
            os.system("sudo cp data/social_metric_dict/gtc_long_trace/LRUSocial.pkl data/social_metric_dict/gtc_long_trace/LRUSocial_%s.pkl"%i)