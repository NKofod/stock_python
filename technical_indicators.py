
def get_SMA(prices,period):
    import statistics as stats 
    history = []
    sma_values = []
    for close_price in prices:
        history.append(close_price)
        if len(history) > period:
            del history[0]
        sma_values.append(stats.mean(history))

    return sma_values

def get_EMA(prices,period,smoothing=2):
    K = smoothing / (period + 1)
    ema_p = 0 
    ema_values = []

    for close_price in prices:
        if ema_p == 0: 
            ema_p = close_price
        else:
            ema_p = (close_price - ema_p) * K + ema_p
        ema_values.append(ema_p)
    return ema_values

def get_apo(prices,fast_period=10,slow_period=40,smoothing=2):
    K_fast = smoothing / (fast_period + 1)
    ema_fast = 0 

    K_slow = smoothing / (slow_period + 1)
    ema_slow = 0 

    ema_fast_values = []
    ema_slow_values = []
    apo_values = []

    for close_price in prices:
        if ema_fast == 0:
            ema_fast = close_price
            ema_slow = close_price
        else:
            ema_fast = (close_price - ema_fast) * K_fast + ema_fast
            ema_slow = (close_price - ema_slow) * K_slow + ema_slow
        ema_fast_values.append(ema_fast)
        ema_slow_values.append(ema_slow)
        apo_values.append(ema_fast-ema_slow)
    return ema_slow_values, ema_fast_values, apo_values

def get_macd(data, fast_period=10, macd_period = 20, slow_period=40, smoothing=2): 
    from matplotlib import pyplot as plt
    prices = data['Close']
    
    K_fast = smoothing / (fast_period + 1)
    K_slow = smoothing / (slow_period + 1)
    K_macd = smoothing / (macd_period + 1)
    ema_fast = 0
    ema_slow = 0 
    ema_macd = 0 
    ema_fast_values = []
    ema_slow_values = []
    macd_values = []
    macd_signal_values = []
    macd_histogram_values = []

    for close_price in prices:
        if ema_fast == 0:
            ema_fast = close_price
            ema_slow = close_price
        else: 
            ema_fast = (close_price - ema_fast) * K_fast + ema_fast
            ema_slow = (close_price - ema_slow) * K_slow + ema_slow

        ema_fast_values.append(ema_fast)
        ema_slow_values.append(ema_slow)
        macd = ema_fast - ema_slow

        if ema_macd == 0:
            ema_macd = macd
        else:
            ema_macd = (macd - ema_macd) * K_macd + ema_macd
        macd_values.append(macd)
        macd_signal_values.append(ema_macd)
        macd_histogram_values.append(macd - ema_macd)
    data['FastExponential10DayMovingAverage'] = ema_fast_values
    data['SlowExponential40DayMovingAverage'] = ema_slow_values
    data['MovingAverageConvergenceDivergence'] = macd_values
    data['Exponential20DayMovingAverageOfMACD'] = macd_signal_values
    data['MACDHistogram'] = macd_histogram_values
    
    ema_f = data['FastExponential10DayMovingAverage']
    ema_s = data['SlowExponential40DayMovingAverage']
    macd = data['MovingAverageConvergenceDivergence']
    ema_macd = data['Exponential20DayMovingAverageOfMACD']
    macd_histogram = data['MACDHistogram']

    fig = plt.figure()
    ax1 = fig.add_subplot(311,ylabel="Price in $")
    prices.plot(ax = ax1, color = "g", lw=2., legend=True)
    ema_f.plot(ax = ax1, color = "b", lw=2., legend=True)
    ema_s.plot(ax = ax1, color = "r", lw=2., legend=True)
    ax2 = fig.add_subplot(312,ylabel = "MACD")
    macd.plot(ax = ax2, color = "black", lw=2., legend=True)
    ema_macd.plot(ax = ax2, color = "g", lw=2., legend=True)
    ax3 = fig.add_subplot(313,ylabel="MACD")
    macd_histogram.plot(ax = ax3, color = "r", kind="bar", legend=True)
    fig.set_size_inches(15,10)
    plt.savefig("AA.png", dpi=600,format="png")

    return




def trading_support_resistance(data,bin_width=20):
    data['sup_tolerance'] = pd.Series(np.zeros(len(data)))
    data['res_tolerance'] = pd.Series(np.zeros(len(data)))
    data['sup_count'] = pd.Series(np.zeros(len(data)))
    data['res_count'] = pd.Series(np.zeros(len(data)))
    data['sup'] = pd.Series(np.zeros(len(data)))
    data['res'] = pd.Series(np.zeros(len(data)))
    data['positions'] = pd.Series(np.zeros(len(data)))
    data['signal'] = pd.Series(np.zeros(len(data)))
    in_support = 0 
    in_resistance = 0
    for x in range((bin_width - 1) + bin_width, len(data)):
        data_section = data[x-bin_width:x + 1]
        support_level = min(data_section["price"])
        resistance_level = max(data_section['price'])
        range_level = resistance_level - support_level
        data['res'][x] = resistance_level
        data['sup'][x] = support_level
        data['sup_tolerance'][x] = support_level + 0.2 * range_level
        data['res_tolerance'][x] = resistance_level + 0.2 * range_level
    return 

import pandas as pd 
in_df = pd.read_csv("./data/stock_data_1d/AA_data.csv",sep=";")
# print(in_df['Close'])
get_macd(in_df)