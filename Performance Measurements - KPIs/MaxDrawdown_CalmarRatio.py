
# =============================================================================
# Max Drawdown = Largest Percentage drop in Asset price over a specified time period
# i.e. Distance b/w Peak & Through in line curve of asset returns
# 
# Calmar Ratio = (CAGR / Max Drawdown) 
# It's a measure of risk adjusted return 
# =============================================================================

#%%

import pandas as pd
import datetime 
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

ticker = '^GSPC' # Ticker for SnP 500 Stocks
#start = dt.datetime.today()-datetime.timedelta(1825)
#end = dt.datetime.today()
SnP = yf.download(ticker, datetime.date.today()-datetime.timedelta(1825), datetime.date.today())
SnP["Adj Close"].plot()

DF = SnP.copy()

# =============================================================================
# CAGR Computation
# =============================================================================

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


#%% Computing Max Drawdown 


def max_DrawDown(DF):
    df = DF.copy()
    df["Daily Returns"] = DF["Adj Close"].pct_change()
    df["Cumulative Returns"] = (1+df["Daily Returns"]).cumprod()
    df["Cumulative Rolling Max"] = df["Cumulative Returns"].cummax()
    df["Drawdown"] = df["Cumulative Rolling Max"] - df["Cumulative Returns"] 
    df["Drawdown_pct"] = df["Drawdown"]/df["Cumulative Rolling Max"]     
    max_dd = df["Drawdown_pct"].max()
    return max_dd
    
max_dd = max_DrawDown(SnP) # Max Drawdown is in percentage of the peak value

# Sanity Check by plotting 
SnP['Adj Close'].plot()

#%% Computing Calmar Ratio

def Calmar(DF):
    calmar = CAGR(DF) / max_DrawDown(DF)
    return calmar

Calmar(SnP)
    
    
    
    
    
    
    
    
    
    