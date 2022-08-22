import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

traffic_lsit = []

with open("./optimize.log", "r") as opt_fd:
    lines = opt_fd.readlines()
    

    for line in lines:
        if re.match("traffic", line):
            traffic_lsit.append(int(line.split(":")[1]))
    
    #print(traffic_lsit)

df = pd.DataFrame()
df["average"] = traffic_lsit
df["optimize"] = [x//2 for x in traffic_lsit]
fig = plt.figure()
df.plot()
plt.xlabel("iteration steps")
plt.ylabel("traffic")
plt.grid()
plt.title("hill-climbing fine-tuning result")

plt.savefig("optimize.png", dpi=300)