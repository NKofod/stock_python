import pandas as pd 
import os 
import datetime 
day = datetime.date.today().day 
month = datetime.date.today().month 
year = datetime.date.today().year
filelist = sorted(list(os.walk("./data/"))[0][2])
for i in [15,16,17,18,19,20,21,22]: 
    tmp_filelist = [j for j in filelist if f"2023_1_{i}" in j]

    tmp_df = pd.read_csv(f"./data/{tmp_filelist[0]}",index_col=False)


    for j in tmp_filelist[1:]:
        tmp_df = pd.concat([tmp_df,pd.read_csv(f"./data/{j}",index_col=False)])

        print(f"{j} - {len(tmp_df)}")
    tmp_df.to_csv(f"./collated/collated_2023_1_{i}.csv",index=False)