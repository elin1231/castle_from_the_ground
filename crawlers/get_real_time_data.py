#%%
from yahoo_fin import stock_info as si
import pandas as pd


def yahoo_finance_functions():
    si.get_data("AAPL")
    si.get_day_gainers()
    si.get_day_losers()
    si.get_day_most_active()
    si.get_analysts_info("AAPL")
    stock = si.get_live_price("AAPL")


#%%
if __name__ == "__main__":
    tickers_df = pd.read_csv("./output/tickerList.csv", header=0)
    for tickers in tickers_df:
        print("test")

# %%
