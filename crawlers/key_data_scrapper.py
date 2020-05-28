import os
<< << << < HEAD
== == == =
import csv
>> >> >> > master
import datetime
from pandas_datareader import data as pdr
from datetime import date
import yfinance as yf
import pandas as pd


class Yahoo_Data_Scrapper:
    def __init__(self, ticker_list):
        self.ticker_list = ticker_list
        self.date = date.today()
        self.dir = os.getcwd()

    def update_data(self):
        for ticker in self.ticker_list:
            print(ticker)
            yf_ticker = yf.Ticker(ticker)
            # finding index for dates that need to be updated

<< << << < HEAD
ticker_news_df = pd.read_csv("./output/sentiment_processed/" + ticker + ".csv", header=0)
ticker_news_df = ticker_news_df.rename(columns={'Unnamed: 0': 'DATE'})
update_list = ticker_news_df[
    ticker_news_df["UPDATED"] == "F"
    ].index.tolist()
ticker_news_df.iloc[update_list, 3] = 'T'
ticker_news_df.to_csv("./output/sentiment_processed/" + ticker + ".csv", header=True, index=False)

# getting historical data date/open/high/low/close/adj_close/volume
yf.pdr_override()
ticker_historical_df = pdr.get_data_yahoo(ticker, start=ticker_news_df.iloc[update_list[len(update_list) - 1], 0],
                                          end=ticker_news_df.iloc[update_list[0], 0])
ticker_historical_df = ticker_historical_df.reindex(index=ticker_historical_df.index[::-1])
s = pd.Series(range(len(ticker_historical_df)))

# getting info data from yf
if 'T' not in ticker_news_df.iloc[:, 3]:  # if ticker has been run before
    try:
        # getting ticker info
        ticker_info_dict = yf_ticker.info
        ticker_info_df = pd.DataFrame.from_dict(ticker_info_dict, orient="index").T
        pd.concat([ticker_info_df] * len(update_list))
        ### add other df
        ticker_training_set = pd.concat([ticker_news_df, ticker_historical_df, ticker_info_df], axis=1)
        ticker_training_set.to_csv("./output/training_set/" + ticker + ".csv", header=True, index=False)
    except Exception:
        print("Failed on {}".format(ticker))

    # else: # if ticker hasn't been run before
    ### add df except for info
    ticker_training_set = pd.concat([ticker_news_df, ticker_info_df], axis=1)
== == == =
ticker_news_df = None
for filename in os.listdir("./output/sentiment_processed"):
    if filename.split(".")[0] == ticker:
        ticker_news_df = pd.read_csv(
            "./output/sentiment_processed/{}.csv".format(ticker)
        )
        ticker_news_df = ticker_news_df.rename(
            columns={"Unnamed: 0": "DATE"}
        )
        update_list = ticker_news_df[
            ticker_news_df["UPDATED"] == "F"
            ].index.tolist()
        ticker_end_date = datetime.datetime.strptime(
            ticker_news_df.iloc[update_list[0], 0], "%Y-%m-%d"
        )
        ticker_start_date = datetime.datetime.strptime(
            ticker_news_df.iloc[update_list[-1], 0], "%Y-%m-%d"
        )
# getting data from yf
try:
    ticker_info_dict = yf_ticker.info
    ticker_info_df = pd.DataFrame.from_dict(
        ticker_info_dict, orient="index"
    ).T
    ticker_training_set = pd.concat(
        [ticker_news_df, ticker_info_df], axis=1
    )
    ticker_training_set.to_csv("./output/training_set/" + ticker + ".csv")
except Exception:
    print("Failed on {}".format(ticker))
>> >> >> > master


def create_ticker_list():
    ticker_list = []
    output_dir = "./output/headline_sentiment"
    for file_name in os.listdir(output_dir):
        if not file_name.startswith("."):
            ticker = file_name.split("_")[2]
            ticker = ticker.split(".")[0]
        ticker_list.append(ticker)
    return ticker_list

<< << << < HEAD

# 2) fix index for concat
# 3) fetch historical data


== == == =
# 2) fix index for concat
# 3) fetch historical data

>> >> >> > master
if __name__ == "__main__":
    ticker_list = create_ticker_list()
    yahoo_data_scrapper = Yahoo_Data_Scrapper(ticker_list)
    yahoo_data_scrapper.update_data()
