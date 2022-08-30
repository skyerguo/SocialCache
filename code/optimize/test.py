import pandas as pd
import re

policy_list = ["Degree", "PageRank", "LaplacianCentrality", "BetweennessCentrality", "EffectiveSize"]

df = pd.DataFrame()
for policy in policy_list:
    with open(policy + ".log", "r") as fd:
        optimize_trace = []
        lines = fd.readlines()
        for line in lines:
            if re.match("traffic", line):
                optimize_trace.append(int(line.split(":")[1]))
        
        print(optimize_trace)
    se = pd.Series(optimize_trace, dtype=int, name=policy)
    print(se)
    df = pd.concat([df, se], axis=1, ignore_index=True)
    #df[policy] = optimize_trace
    print(df)

print(df)
df.columns = policy_list
print(df)
df.to_csv("optimize_trace.csv")