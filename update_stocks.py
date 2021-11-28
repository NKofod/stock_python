import pandas as pd
import yfinance as yf
import datetime
from joblib import Parallel, delayed
import multiprocessing


def update_stock(stock,start_date,end_date):
    import os
    try:
        tmp = pd.read_csv(f"./data/stock_data_1m/{stock}_data.csv",sep=";")
        
        ticker_download = yf.download(tickers=f"{stock}", start=f"{start_date}",end=f"{end_date}",interval="1m",auto_adjust=True,threads=True)
        ticker_download.to_csv(f"tmp_{stock}.csv",sep=";")
        ticker_download = pd.read_csv(f"tmp.csv",sep=";")
        # try: 
        ticker_download["Time"] = ticker_download['Unnamed: 0']
        ticker_download = ticker_download.drop(['Unnamed: 0'],axis=1)
            # print(tmp)
        # except KeyError:
        #     pass 
        tmp = tmp.append(ticker_download).drop_duplicates()
        tmp.to_csv(f"./data/stock_data_{i}/{stock}_data.csv",sep=";",index=False)
        os.remove(f"tmp_{stock}.csv")
    except ValueError:
        return 
    except KeyError:
        os.remove(f"./data/stock_data_1m/{stock}_data.csv")
    except FileNotFoundError:
        return 
    # except FileNotFoundError:
    #     return
    # except pd.errors.EmptyDataError:
    #     return

def processInput(stock,start_date,end_date):
    if stock != "":
        print(stock)
        update_stock(stock,start_date,end_date)

def update(stockfile):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    with open(stockfile,"r") as infile:
        stock_list = infile.read().split("\n")
    Parallel(n_jobs=8)(delayed(processInput)(i,"2021-07-21","2021-07-22") for i in stock_list)

update("stocks.txt")
today = datetime.date.today()
with open("logs.txt","a") as logfile:
    logfile.write(f"{today} - Updated stocks.")