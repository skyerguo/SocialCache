import pandas as pd

df = pd.read_csv('raw.dat')

print(df.head())

df_transposed = df.transpose()

print(df_transposed.head())