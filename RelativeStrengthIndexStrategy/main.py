import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (18, 12)

import requests
import datetime as dt
import json
import time


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
    data['Low'] = data['Low'].astype('float')
    data['Close'] = data['Close'].astype('float')
    return data


df = get_klines('ethusdt', '15m', 1500)


# Calculate the RSI
def get_rsi(close, lookback):
    ret = close.diff()
    up = []
    down = []
    for i in range(len(ret)):
        if ret[i] < 0:
            up.append(0)
            down.append(ret[i])
        else:
            up.append(ret[i])
            down.append(0)
    up_series = pd.Series(up)
    down_series = pd.Series(down).abs()
    up_ewm = up_series.ewm(com=lookback - 1, adjust=False).mean()
    down_ewm = down_series.ewm(com=lookback - 1, adjust=False).mean()
    rs = up_ewm / down_ewm
    rsi = 100 - (100 / (1 + rs))
    rsi_df = pd.DataFrame(rsi).rename(columns={0:'rsi'}).set_index(close.index)
    rsi_df = rsi_df.dropna()
    return rsi_df[3:]


df['rsi_14'] = get_rsi(df['Close'], 14)
df = df.dropna()


# Plot the RSI
# ax1 = plt.subplot2grid((10,1), (0,0), rowspan=4, colspan=1)
# ax2 = plt.subplot2grid((10,1), (5,0), rowspan=4, colspan=1)
# ax1.plot(df['Close'], linewidth=2.5)
# ax1.set_title('BTC Close Price')
# ax2.plot(df['rsi_14'], color='#6c5ce7', linewidth=2.5)
# ax2.axhline(30, linestyle='--', linewidth=1.5, color='#636e72')
# ax2.axhline(70, linestyle='--', linewidth=1.5, color='#636e72')
# ax2.set_title('BTC RELATIVE STRENGTH INDEX')
# plt.show()


# Create the strategy
def implement_rsi_strategy(prices, rsi):
    buy_price = []
    sell_price = []
    rsi_signal = []
    signal = 0

    for i in range(len(rsi)):
        if rsi.iloc[i-1] > 30 and rsi.iloc[i] < 30:
            if signal != 1:
                buy_price.append(prices.iloc[i])
                sell_price.append(np.nan)
                signal = 1
                rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)
        elif rsi.iloc[i-1] < 70 and rsi.iloc[i] > 70:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices.iloc[i])
                signal = -1
                rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            rsi_signal.append(0)

    return buy_price, sell_price, rsi_signal


buy_price, sell_price, rsi_signal = implement_rsi_strategy(df['Close'], df['rsi_14'])
print(f'Long signals: {rsi_signal.count(1)} | Short signals: {rsi_signal.count(-1)}')


# Plot the signals
ax1 = plt.subplot2grid((10,1), (0,0), rowspan=4, colspan=1)
ax2 = plt.subplot2grid((10,1), (5,0), rowspan=4, colspan=1)
ax1.plot(df['Close'], linewidth=1.5, color='#2f3542', label='BTC')
ax1.plot(df.index, buy_price, marker='^', color='#2ed573', markersize=10, label='Buy Signal')
ax1.plot(df.index, sell_price, marker='v', color='#ff4757', markersize=10, label='Sell Signal')
ax1.set_title('BTC Price')
ax2.plot(df['rsi_14'], color='#1e90ff', linewidth=1.2)
ax2.axhline(30, linestyle='--', linewidth=1.5, color='#2f3542')
ax2.axhline(70, linestyle='--', linewidth=1.5, color='#2f3542')
plt.show()

