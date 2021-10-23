#%% CAGR Computation 


import pandas as pd
import datetime 
import yfinance as yf
import matplotlib.pyplot as plt

ticker = '^GSPC' # Ticker for SnP 500 Stocks
#start = dt.datetime.today()-datetime.timedelta(1825)
#end = dt.datetime.today()
SnP = yf.download(ticker, datetime.date.today()-datetime.timedelta(1825), datetime.date.today())
SnP["Adj Close"].plot()



def CAGR(DF):
    df = DF.copy()
    df["Daily Returns"] = DF["Adj Close"].pct_change() # Daily Returns aren't very useful
    df["Cumulative Returns"] = (1+df["Daily Returns"]).cumprod()
    n = len(df)/252 
    # len(df) gives no. of trading days in our time horizon
    # 252 is no. of trading days in a year
    cagr = (df["Cumulative Returns"][-1])**(1/n) - 1
    # Computed CAGR is for daily returns, if you use weekly/intraday data, change n
    return cagr

#%%

CAGR(SnP)