import pandas as pd 

tmp = pd.read_csv("stocks.csv",sep=";")
tmp = tmp.sort_values("Ticker")
tmp = tmp.dropna(subset=["Country","Name","Exchange"])
tmp.to_csv("stocks.csv",sep=";",index=False)

print(tmp)