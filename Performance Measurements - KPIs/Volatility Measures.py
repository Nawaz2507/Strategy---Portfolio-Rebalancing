
# =============================================================================
# Standard Deviation of Returns captures variability of returns w.r.t mean return
# 
# For Annualizing Volatility:
#     For Daily Volatility - Daily Vol * sqrt(252)
#     For Weekly Volatility - Weekly Vol * sqrt(52)
#     For Montly Volatiltiy - Monthly Vol * sqrt(12)
# 
# =============================================================================
# Assumes Normal Distribution of returns which isn't true!
# Standard Deviation doesn't capture Tail Risk!

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

def volatility(DF):
    df = DF.copy()
    df["Daily Returns"] = DF["Adj Close"].pct_change()
    vol = df["Daily Returns"].std() * np.sqrt(252)
    return vol    