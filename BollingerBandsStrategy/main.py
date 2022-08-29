# Import all packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests
import json
import datetime as dt

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (14, 9)
plt.rcParams['axes.facecolor'] = '#2d3436'

# Extracting the data from Binance
def get_klines(symbol, interval, limit=500):
    url = 'https://fapi.binance.com/fapi/v1/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    data = pd.DataFrame(json.loads(requests.get(url, params=params).text))
    data = data.iloc[:,0:6]
    data.columns = [
        'Open Time',
        'Open',
        'High',
        'Low',
        'Close',
        'Volume'
    ]
    data['Open Time'] = [dt.datetime.fromtimestamp(x / 1000) for x in data['Open Time']]
    data['Open'] = data['Open'].astype('float')
    data['High'] = data['High'].astype('float')
    data['Low'] = data['Low'].astype(float)
    data['Close'] = data['Close'].astype('float')
    return data


df = get_klines('ethusdt', '1h', 1500)


# Bollinger Bands calculation
# Step One -> Calculate the SMA
def sma(data, window):
    data = data.rolling(window=window).mean()
    return data


df['sma_20'] = sma(df['Close'], 20)

# Step Two -> Calculating Bollinger Bands
def bb(data, sma, window):
    std = data.rolling(window=window).std()
    upper_bb = sma + std * 1.5
    lower_bb = sma - std * 1.5
    return upper_bb, lower_bb


df['upper_bb'], df['lower_bb'] = bb(df['Close'], df['sma_20'], 20)


# Plotting Bollinger Bands values
# df['Close'].plot(label='Close Price', color='#f1f1f1', linewidth=1.3)
# df['upper_bb'].plot(label='Upper BB 20', linewidth=1.3, color='#e84393')
# df['sma_20'].plot(label='Middle BB 20', linewidth=1, color='#ffeaa7')
# df['lower_bb'].plot(label='Lower BB 20', linewidth=1.3, color='#6c5ce7')
# plt.legend(loc='upper left')
# plt.title('BTC BOLLINGER BANDS')
# plt.show()


# Creating the Trading Strategy
def implement_bb_strategy(data, lower_bb, upper_bb):
    buy_price = []
    sell_price = []
    bb_signal = []
    signal = 0

    for i in range(len(data)):
        if data.iloc[i-1] > lower_bb.iloc[i-1] and data.iloc[i] < lower_bb.iloc[i]:
            if signal != 1:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal = 1
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        elif data.iloc[i - 1] < upper_bb.iloc[i - 1] and data.iloc[i] > upper_bb.iloc[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -1
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_signal.append(0)

    return buy_price, sell_price, bb_signal


buy_price, sell_price, bb_signal = implement_bb_strategy(df['Close'], df['lower_bb'], df['upper_bb'])

def backtest(prices, signal):
    long_trades = []
    short_trades = []

    for i in range(len(signal)):
        if signal[i] == 1:
            target = prices[i] + (prices[i] * 0.02)
            stop = prices[i] - (prices[i] * 0.8)

            for j in prices:
                if target <= j:
                    long_trades.append(1)
                    break
                elif stop <= j:
                    long_trades.append(-1)
                    break
        elif signal[i] == -1:
            pass
    return long_trades

l_trade = backtest(df['Close'], bb_signal)
print(f'Total Signals: {bb_signal.count(1)} | Good Trades: {l_trade.count(1)} | Bad Trades: {l_trade.count(-1)}')

# Ploting the data with signals
# df['Close'].plot(label='Close Price', color='#f1f1f1', linewidth=1.3)
# df['upper_bb'].plot(label='Upper BB', color='#e84393', linewidth=1.3)
# df['sma_20'].plot(label='Middle BB', color='#fff200', linewidth=1)
# df['lower_bb'].plot(label='Lower BB', color='#6c5ce7', linewidth=1.3)
# plt.scatter(df.index, buy_price, marker='^', color='#32ff7e', label='Buy', s=200)
# plt.scatter(df.index, sell_price, marker='v', color='#ff3838', label='Sell', s=200)
# plt.title('BTC BB STRATEGY TRADING SIGNALS')
# plt.legend(loc='upper left')
# plt.show()

ff8ddb0d2