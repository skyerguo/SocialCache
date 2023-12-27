import pandas as pd
from ast import literal_eval
# csv file name
csv_file = 'traffic_volume.csv'

def main():
    # read dataframe from csv file
    df = pd.read_csv(csv_file, index_col=0)

    print(df)

    # for each tuple element in the dataframe, add the values
    all_df = df.applymap(lambda x: sum(literal_eval(x)))

    print(all_df)

    # export to csv file
    all_df.to_csv('traffic_volume_all.csv')
    # export to txt file
    all_df.to_string('traffic_volume_all.txt')


main()