# Relative Strength Index
An oscillator is a technical tool that constructs a trend-based indicator whose values are bound between a high and low band. Traders use these bands along with the constructed trend-based indicator to identify the market state and make potential buy and sell trades.

Relative Strength Index is a momentum oscillator that is used by traders to identify whether the market is in the state of overbought or oversold.  

**overbought:** A market is considered to be in the state of overbought when an asset isconstantly bought by traders moving it to an extremely bullish trend and bound to consolidate.  

**oversold:** Similarly, a market is considered to be in the state of oversold when an asset is constantly sold by traders moving it to a bearish trend and tends to bounce back.

***There are three steps involved in the calculation of RSI.***  
- ***Calculating the Exponential Moving Average (EMA) of the gain and loss of an asset:*** In this step, we will first calculate the returns of the asset and separate the gains from losses. Using these separated values, the two EMAs for a specified number of periods are calculated.


- ***Calculating the Relative Strength of an asset:*** The Relative Strength of an asset is determined by dividing the Exponential Moving Average of the gain of an asset from the Exponential Moving Average of the loss of an asset for a specified number of periods. It can be mathematically represented as follows:  
***RS = GAIN EMA / LOSS EMA***  
where,  
RS = Relative Strength  
GAIN EMA = Exponential Moving Average of the gains  
LOSS EMA = Exponential Moving Average of the losses


- ***Calculating the RSI values:*** In this step, we will calculate the RSI itself by making use of the Relative Strength values we calculated in the previous step. To calculate the values of RSI of a given asset for a specified number of periods, there is a formula that we need to follow:  
***RSI = 100.0 - (100.0 / (1.0 + RS))***
where,
RSI = Relative Strength Index
RS = Relative Strength


### ***RSI Trading Strategy***
IF PREVIOUS RSI > 30 AND CURRENT RSI < 30 ==> BUY SIGNAL  
IF PREVIOUS RSI < 70 AND CURRENT RSI > 70 ==> SELL SIGNAL