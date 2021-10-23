
# =============================================================================
# Sharpe Ratio = Avg Return earned in excess of risk free rate per unit of risk
# Sharpe = (Rp - Rf)/StdDev
# Rp = Expected Returns
# Rf = Risk Free Rate
# StdDev = Standard Deviation of returns for the time period
# =============================================================================


# =============================================================================
# Sortino Ratio = Variation of Sharpe, considers std dev of only Negative Returns
# Sortino makes distinction b/w upside & downside vol,considers only harmful vol
# =============================================================================

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

# =============================================================================
# Annualized Standard Deviation
# =============================================================================

def volatility(DF):
    df = DF.copy()
    df["Daily Returns"] = DF["Adj Close"].pct_change()
    vol = df["Daily Returns"].std() * np.sqrt(252)
    return vol    

rf = 0.022

#%%
# =============================================================================
# Sharpe Ratio Computation
# =============================================================================

def Sharpe(DF, rf):
    df = DF.copy()
    sharpe = (CAGR(DF) - rf)/volatility(DF)
    return sharpe

#%%
# =============================================================================
# Sortino Ratio Computation 
# =============================================================================

def Sortino(DF, rf):
    df = DF.copy()
    df["Daily Returns"] = DF["Adj Close"].pct_change()
    neg_vol = df[df["Daily Returns"] < 0]["Daily Returns"].std() * np.sqrt(252)
    sortino = (CAGR(DF) - rf)/neg_vol
    return sortino

Sharpe(SnP, 0.022)
Sortino(SnP, 0.022)