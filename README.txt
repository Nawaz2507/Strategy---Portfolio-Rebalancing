This repo contains the scripts for the core protfolio rebalancing strategy alongside the various KPI function definitions like Sharpe, Sortino, CAGR, Max Drawdown

The strategy is implemented on the NIFTY 50 Stock Universe & the Dow Jones Industrial Average Stock Unvierse. 

This is a long only strategy in which we pick 'n' stocks with fixed position sizes based on monthly returns.
The portfolio is rebalanced at the end of each month by removing 'x' worst performing stocks and replacing them with the top 'x' best performing stocks from our selected universe of stocks.
We can double down on the same stock if it continues to be a top performer for the next month also.

The returns are then compared with a simple BUY & HOLD strategy of the Index
Selected Universe of Stocks -> Dow Jones Industrial Average (DJIA) & NIFTY50 constituents as on Feb 1st, 2016

The backtesting is done from Feb 1st 2016 to Oct 1st, 2021. The KPIs are lower than index KPIs when run for NIFTY (strategy underperforms undex) 
& higher than index KPIs when run for DJIA (strategy outperforms index).

Strategy Performance:

1) NIFTY50 (n=40, x=2):
Index Performance -> CAGR = 18.02%, Sharpe = 0.66, Sortino = 0.75, Max Drawdown = 29.34%,
Strategy Performace -> CAGR = 22.19%, Sharpe = 0.88, Sortino = 1.16, Max Drawdown = 33.46%,

2) DJIA (n=6, x=3):
Index Performance -> CAGR = 13.49%, Sharpe = 0.73, Sortino = 0.84, Max Drawdown = 23.20%,
Strategy Performace -> CAGR = 16.82%, Sharpe = 0.89, Sortino = 1.63, Max Drawdown = 17.07%,