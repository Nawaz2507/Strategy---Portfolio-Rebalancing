#%% Monthly Portfolio Rebalancing Strategy - Details

# This is a long only strategy in which we pick 'n' stocks with fixed position sizes based on monthly returns
# The portfolio is rebalanced at the end of each month by removing 'x' worst performing stocks and replacing them with the top 'x' best performing stocks 
# from our selected universe of stocks.
# We can double down on the same stock if it continues to be a top performer for the next month also


# Selected Universe of Stocks -> NIFTY50 constituents as on Feb 1st, 2016

#%% Importing Libraries

import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import copy


#%% KPIs 

def CAGR(DF):
    df = DF.copy()
    df["Cumulative Returns"] = (1+df["Monthly Returns"]).cumprod()
    n = len(df)/12 
    # len(df) gives no. of trading months in our time horizon 
    cagr = (df["Cumulative Returns"].tolist()[-1])**(1/n) - 1
    # Computed CAGR is for daily returns, if you use weekly/intraday data, change n
    return cagr


def volatility(DF):
    df = DF.copy()
    vol = df["Monthly Returns"].std() * np.sqrt(12)
    return vol    


def Sharpe(DF,rf):
    sharpe = (CAGR(DF) - rf)/volatility(DF)
    return sharpe


def MaxDD(DF):
    df = DF.copy()
    df["Cumulative Returns"] = (1+df["Monthly Returns"]).cumprod()
    df["Cum_Rolling_Max"] = df["Cumulative Returns"].cummax()
    df["Drawdown"] = df["Cum_Rolling_Max"] - df["Cumulative Returns"]
    df["Drawdown_pct"] = df["Drawdown"] / df["Cum_Rolling_Max"]
    maxDD = df["Drawdown_pct"].max()
    return maxDD


def Sortino(DF, rf):
    df = DF.copy()
    neg_vol = df[df["Monthly Returns"] < 0]["Monthly Returns"].std() * np.sqrt(12)
    sortino = (CAGR(DF) - rf)/neg_vol
    return sortino

#%% Importing Monthly Data 

tickers = ["ACC.BO", "ADANIPORTS.NS", "AMBUJACEM.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BANKBARODA.NS", "BHARTIARTL.NS", "BHEL.NS", "BOSCHLTD.NS", 
           "BPCL.NS", "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "GAIL.NS", "GRASIM.NS", "HCLTECH.NS",
           "HDFC.NS", "HDFCBANK.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "IDEA.NS", 
           "INDUSINDBK.NS", "INFY.NS", "ITC.NS", "KOTAKBANK.NS", "LT.NS", "LUPIN.NS", "M&M.NS", "MARUTI.NS", 
           "NTPC.NS", "ONGC.NS", "PNB.NS", "POWERGRID.NS", "RELIANCE.NS", "SBIN.NS", "SUNPHARMA.NS", "TATAMOTORS.NS", "TATAPOWER.NS", 
           "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "ULTRACEMCO.NS", "VEDL.NS", "WIPRO.NS", "YESBANK.NS", "ZEEL.NS"]   

ohlc_data = {}

start = dt.date.fromisoformat('2016-02-01')
end = dt.date.fromisoformat('2021-10-01')                     


for ticker in tickers:
    print("Downloading data for ", ticker + '\n')
    ohlc_data[ticker] = yf.download(ticker, start, end, interval="1mo")
    ohlc_data[ticker].bfill(inplace=True)
    
#dropna(inplace=True, how="all")

tickers = ohlc_data.keys()


#%% Computing Monthly Returns 

ohlc_copy = copy.deepcopy(ohlc_data)
returns_DF = pd.DataFrame()

for ticker in tickers:
    print("Computing Monthly Returns of ", ticker + '\n')
    ohlc_copy[ticker]["Monthly Returns"] = ohlc_copy[ticker]["Adj Close"].pct_change()
    returns_DF[ticker] = ohlc_copy[ticker]["Monthly Returns"]

returns_DF.dropna(inplace=True)

#%% Computing Performance of a simple BUY & HOLD strategy of the Index (NIFTY50) for the same period

index_ticker = "^NSEI"
NIFTY = yf.download(index_ticker, start, end, interval="1mo")
NIFTY["Monthly Returns"] = NIFTY["Adj Close"].pct_change()

rf = 0.06 # Assumed Risk-Free rate for this period

CAGR(NIFTY)
Sharpe(NIFTY, rf)
Sortino(NIFTY, rf)
MaxDD(NIFTY)


#%% Defining Proposed Portfolio Rebalancing Strategy 

""" 
    DF = DataFrame containing Monthly Returns of all tickers
    n = No. of stocks to be held in the portfolio
    x = No. of stocks to be removed each month
"""

def stratRebalancing(DF, n, x):
    df = DF.copy()
    portfolio = df.iloc[0, :n].index.values.tolist()
    monthly_ret_strat = [0]
    
    for i in range(len(df)):
        if(len(portfolio)>0):
            monthly_ret_strat.append(df[portfolio].iloc[i, :].mean())
            bad_stocks = df[portfolio].iloc[i, :].sort_values(ascending=True)[:x].index.values.tolist()
            portfolio = [t for t in portfolio if t not in bad_stocks]
            
        to_add = n - len(portfolio)
        new_picks = df.iloc[i, :].sort_values(ascending=False)[:to_add].index.values.tolist()
        portfolio = portfolio + new_picks
        
    strat_ret_DF = pd.DataFrame(np.array(monthly_ret_strat), columns=["Monthly Returns"])
    return strat_ret_DF
    

#%% Computing Strategy Performance 
n = 30
x = 20
strat_DF = pd.DataFrame()
strat_DF = stratRebalancing(returns_DF, n, x)
CAGR(strat_DF)
Sharpe(strat_DF, rf)
Sortino(strat_DF, rf)
MaxDD(strat_DF)

#%% Plotting Results

fig, ax = plt.subplots()
plt.plot((1+strat_DF).cumprod())
plt.plot((1+NIFTY["Monthly Returns"].reset_index(drop=True)).cumprod())
plt.title("Index Return vs Strategy Return")
plt.ylabel("cumulative return")
plt.xlabel("months")
ax.legend(["Strategy Return","Index Return"])