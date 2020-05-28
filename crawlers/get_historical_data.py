from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd




tickers_df = pd.read_csv('./output/tickerList.csv', header=0)
for i in range(len(tickers_df)):
    print(tickers_df.iloc[i, 0], i)
    yf.pdr_override()
    print("getting historical data")
    ticker_historical_df = pdr.get_data_yahoo(tickers_df.iloc[i, 0], period='Max')
    ticker_historical_df.to_csv("./output/historical_data/" + tickers_df.iloc[i, 0] + ".csv", header=True)
print('finished download')
