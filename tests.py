import pandas as pd
import yfinance as yf
import datetime
from joblib import Parallel, delayed
import multiprocessing
import json 
import json.decoder
import os 
import requests

# tmp = pd.read_csv("nasdaq.csv",sep=",")

# countries_to_exclude = ["India","China","South Korea", 
                        # "Hong Kong", "Malaysia", "Taiwan", 
                        # "Indonesia", "Thailand", "Singapore",
                        # "Argentina", "Brazil", "Venezuela",
                        # "Israel", "Qatar", "Russia", "Turkey",
                        # "Australia", "New Zealand"]
# for i in countries_to_exclude:
#     tmp = tmp[tmp["Country"] != i]
with open("stocks.txt","r") as infile:
    stock_list = infile.read().split("\n")[:-1]
today = datetime.date.today()
last_week = today - datetime.timedelta(days=7)
two_years = today - datetime.timedelta(days=729)

def processInput(ticker,time):
    print(ticker)
    if os.path.isfile(f"finished_{time}.txt"):
        pass
    else:
        with open(f"finished_{time}.txt","w") as infile:
            infile.write("\n")
    if os.path.isfile(f"./data/stock_data_{time}/{ticker}_data.csv"):
        with open(f"finished_{time}.txt","a") as finished_file:
            finished_file.write(f"{ticker}\n")
    
    with open(f"finished_{time}.txt","r") as infile:
        if ticker in infile.read().split("\n"):
            return
    with open(f"error_file.txt","r") as errorfile:
        if ticker in errorfile.read().split("\n"):
            return 
    
    print(f"{ticker}")
    if time == "1h":
        ticker_download = yf.download(tickers=f"{ticker}", start=f"{two_years}",end=f"{today}",interval=time,auto_adjust=True,threads=True)
    elif time == "1m":
        ticker_download = yf.download(tickers=f"{ticker}", start=f"{last_week}",end=f"{today}",interval=time,auto_adjust=True,threads=True)
    elif time == "1d":
        ticker_download = yf.download(tickers=f"{ticker}", start=f"1970-01-01",end=f"{today}",interval=time,auto_adjust=True,threads=True)
    ticker_download.to_csv(f"./data/stock_data_{time}/{ticker}_data.csv",sep=";")
    with open(f"finished_{time}.txt","a") as finished_file:
        finished_file.write(f"{ticker}\n")
    # except requests.exceptions.ConnectionError:
    #     processInput(ticker)
    # except json.decoder.JSONDecodeError:
    #     with open("error_file.txt","a") as f:
    #         f.write(ticker)
    #     return 
    # except ValueError:
    #     with open("error_file.txt","a") as f:
    #         f.write(ticker)
    #     return 
    # except IndexError:
    #     with open("error_file.txt","a") as f:
    #         f.write(ticker)
    #     return 
    # except ValueError: 
    #     with open("error_file.txt","a") as f:
    #         f.write(ticker)
        return 

# Parallel(n_jobs=12)(delayed(processInput)(i,"1h") for i in stock_list)
Parallel(n_jobs=12)(delayed(processInput)(i,"1m") for i in stock_list)
# Parallel(n_jobs=12)(delayed(processInput)(i,"1d") for i in stock_list)
def check_stocks():
    os.system("ls ./data/stock_data_1h/ > stock_hour.txt")
    with open("stock_hour.txt", "r") as stockfile:
        stocklist = stockfile.read().split("\n")
    for stock in stocklist:
        if stock != "":
            tmp = pd.read_csv(f"./data/stock_data_1h/{stock}",sep=";")
            # tmp = tmp.columns
            try: 
                tmp["Time"] = tmp['Unnamed: 0']
                tmp = tmp.drop(['Unnamed: 0'],axis=1)
                tmp.to_csv(f"./data/stock_data_1h/{stock}",sep=";",index=False)
                # print(tmp)
                print(stock)
            except KeyError:
                try: 
                    print(tmp["Date"])
                    os.remove(f"./data/stock_data_1h/{stock}")
                except KeyError:
                    print(stock)
                    pass 
                    # os.remove(f"./data/stock_data_1h/{stock}")
            # for i in tmp:
            #     print(str(i)[:10])
# check_stocks()
# os.system("ls ./data/stock_data_1h/ > stock_hour.txt")
# with open("./stock_hour.txt","r") as stock_file:
#     tmp = stock_file.read().split("\n")
# stock_list = []
# for i in tmp:
#     if i != "":
#         stock_list.append(i[:-9])
# with open("stocks.txt","w") as outfile:
#     for i in stock_list:
#         outfile.write(f"{i}\n")