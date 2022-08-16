import pandas as pd

log_df = pd.DataFrame(columns=["optimal", "average"])
print(log_df)

log_df = log_df.append(dict(optimal=1366600, average=1489999), ignore_index=True)

print(log_df)