# import pandas as pd
#
# data = pd.read_csv("listing_status.csv")
# print(data.columns)

import pandas as pd 
import requests 
import os
from datetime import datetime
from bs4 import BeautifulSoup as Soup 
import re
import ast

with open("alpha_vantage_api.txt","r") as f:
    key = f.read().split("\n")[0]

nasdaq = pd.read_csv("nasdaq.csv",sep=",")
nasdaq_list = nasdaq["Symbol"].to_list()
for i in nasdaq_list:
    print(i)
    for year in [1,2]:
        for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=30min&adjusted=false&slice=year{year}month{month}&apikey={key}'
            tmp = requests.get(url)
            with open("tmp.csv","wb") as tmpfile:
                tmpfile.write(tmp.content)
            tmp_df = pd.read_csv("tmp.csv",sep=",")
            if year == 1 and month == 1:
                tmp_df.to_csv(f"./stock_data/{i}_data.csv",index=False)
            else:
                tmp_df.to_csv(f"./stock_data/{i}_data.csv",index=False,mode="a")
            # with open(f"./stock_data/{i}_data.csv","wb") as outfile:
            #     outfile.write(tmp.content)
