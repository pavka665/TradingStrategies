## Stragegy Info

Bollinger Bands are great to observe the volatility of a given stock over a period of time. The volatility of a stock is observed to be lower when the space or distance between the upper and lower band is less. Similarly, when the space or distance between the upper and lower band is more, the stock has a higher level of volatility  

Calculating the upper and lower bands  
UPPER_BB = STOCK SMA + SMA STANDARD DEVIATION * 2  
LOWER_BB = STOCK SMA - SMA STANDARD DEVIATION * 2  

Trading Strategy  
IF PREV_STOCK > PREV_LOWERBB & CUR_STOCK < CUR_LOWER_BB => BUY  
IF PREV_STOCK < PREV_UPPERBB & CUR_STOCK > CUR_UPPER_BB => SELL  