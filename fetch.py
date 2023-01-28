
import pandas as pd
import json 
import datetime 
import time 
import alpha_vantage.timeseries
import os 

with open('env.json', "r") as infile:
    env_json = json.load(infile)
    
with open('stocks.json','r') as infile:
    stocks_dict = json.load(infile)
if env_json['Current_day'] > 14: 
    env_json['Current_day'] = 1 
stock_list = stocks_dict[str(env_json['Current_day'])]
    
ts = alpha_vantage.timeseries.TimeSeries(key='QVEGLYRJUK0ABVMT',output_format='pandas')
day = datetime.date.today().day 
month = datetime.date.today().month 
year = datetime.date.today().year
for i in stock_list: 
    
    try: 
        data, meta_data = ts.get_intraday(i,'1min','full')
        ticker_list = [i] * len(data)
        data['Ticker'] = ticker_list 
        print(f'./data/{i}_{year}_{month}_{day}.csv')
        data.to_csv(f'./data/{i}_{year}_{month}_{day}.csv')
    except ValueError as e:
        print(e.__str__())
        pass 
    
    time.sleep(20)

with open('env.json', "w") as outfile:
    env_json_out = env_json
    env_json_out['Current_day'] += 1 
    json.dump(env_json_out,outfile)

filelist = list(os.walk("./data/"))[0][2]
filelist = [i for i in filelist if f"{year}_{month}_{day}" in i]
tmp_df = pd.read_csv(f"./data/{filelist[0]}",index_col=False)

for i in filelist[1:]:
    tmp_df = pd.concat([tmp_df,pd.read_csv(f"./data/{i}",index_col=False)])
    print(f"{i} - {len(tmp_df)}")
tmp_df.to_csv(f"./collated/collated_{year}_{month}_{day}.csv",index=False)