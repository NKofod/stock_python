import pandas as pd 
import os 

filelist = list(os.walk("./data/"))[0][2]

tmp_df = pd.read_csv(f"./data/{filelist[0]}",index_col=False)

for i in filelist[1:]:
    
    tmp_df = pd.concat([tmp_df,pd.read_csv(f"./data/{i}",index_col=False)])

    print(f"{i} - {len(tmp_df)}")
tmp_df.to_csv("./collated/collated.csv",index=False)
