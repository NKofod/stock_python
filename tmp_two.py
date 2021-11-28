import os 

os.system("ls ./data/stock_data_1d > stock_day.txt")
os.system("ls ./data/stock_data_1h > stock_hour.txt")
os.system("ls ./data/stock_data_1m > stock_minute.txt")

with open("stock_day.txt","r") as day_file:
    day_stocks = day_file.read().split("\n")

with open("stock_hour.txt","r") as hour_file:
    hour_stocks = hour_file.read().split("\n")

with open("stock_minute.txt","r") as minute_file:
    minute_stocks = minute_file.read().split("\n")


for i in minute_stocks:
    if os.path.getsize(f"./data/stock_data_1m/{i}") <= 1000:
        os.remove(f"./data/stock_data_1m/{i}")
for i in hour_stocks:
    if os.path.getsize(f"./data/stock_data_1h/{i}") <= 1000:
        os.remove(f"./data/stock_data_1h/{i}")
for i in day_stocks:
    if os.path.getsize(f"./data/stock_data_1d/{i}") <= 100000:
        os.remove(f"./data/stock_data_1d/{i}")

os.system("ls ./data/stock_data_1d > stock_day.txt")
os.system("ls ./data/stock_data_1h > stock_hour.txt")
os.system("ls ./data/stock_data_1m > stock_minute.txt")

with open("stock_day.txt","r") as day_file:
    day_stocks = day_file.read().split("\n")

with open("stock_hour.txt","r") as hour_file:
    hour_stocks = hour_file.read().split("\n")

with open("stock_minute.txt","r") as minute_file:
    minute_stocks = minute_file.read().split("\n")


common_stocks = []
for i in day_stocks:
    if i in hour_stocks and i in minute_stocks:
        print(i)
        common_stocks.append(i)
    else:
        # os.remove(f"./stock_data_1d/{i}")
        pass 

for i in day_stocks:
    if i not in common_stocks:
        os.remove(f"./data/stock_data_1d/{i}")
for i in hour_stocks:
    if i not in common_stocks:
        os.remove(f"./data/stock_data_1h/{i}")
for i in minute_stocks:
    if i not in common_stocks:
        os.remove(f"./data/stock_data_1m/{i}")

with open("stocks.txt","w") as stockfile:
    for stock in common_stocks:
        stockfile.write(f"{stock}\n")