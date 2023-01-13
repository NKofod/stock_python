
import pandas as pd
import json 
import pandas_datareader.data as web 
import datetime 
import time 

with open('env.json', "r") as infile:
    env_json = json.load(infile)
    
with open('stocks.json','r') as infile:
    stocks_dict = json.load(infile)
    
stock_list = stocks_dict[str(env_json['Current_day'])]

day = datetime.date.today().day 
month = datetime.date.today().month 
year = datetime.date.today().year
for i in stock_list: 
    try: 
        tmp = web.DataReader(i , 'av-intraday', start=datetime.datetime(2022,1,1),end=datetime.date.today(),api_key='QVEGLYRJUK0ABVMT')
        ticker_list = [i] * len(tmp)
        tmp['Ticker'] = ticker_list 
        tmp.to_csv(f'./data/{i}_{year}_{month}_{day}.csv')
    except ValueError:
        pass 
    time.sleep(20)

with open('env.json', "w") as outfile:
    env_json_out = env_json
    env_json_out['Current_day'] += 1 
    json.dump(env_json_out,outfile)
