import os
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
            ticker_news_df = pd.read_csv(
                "./output/sentiment_processed/" + ticker + ".csv", header=0
            )
            ticker_news_df = ticker_news_df.rename(columns={"Unnamed: 0": "DATE"})
            update_list = ticker_news_df[
                ticker_news_df["UPDATED"] == "F"
            ].index.tolist()
            ticker_news_df.iloc[update_list, 3] = "T"
            ticker_news_df.to_csv(
                "./output/sentiment_processed/" + ticker + ".csv",
                header=True,
                index=False,
            )

            # getting info data from yf
            if "T" not in ticker_news_df.iloc[:, 3]:  # if ticker has been run before
                try:
                    # getting ticker info
                    ticker_info_dict = yf_ticker.info
                    ticker_info_df = pd.DataFrame.from_dict(
                        ticker_info_dict, orient="index"
                    ).T
                    pd.concat([ticker_info_df] * len(update_list))
                    ### add other df
                    ticker_training_set = pd.concat(
                        [ticker_news_df, ticker_historical_df, ticker_info_df], axis=1
                    )
                    ticker_training_set.to_csv(
                        "./output/training_set/" + ticker + ".csv",
                        header=True,
                        index=False,
                    )
                except Exception:
                    print("Failed on {}".format(ticker))

                # else: # if ticker hasn't been run before
                ### add df except for info
                ticker_training_set = pd.concat(
                    [ticker_news_df, ticker_info_df], axis=1
                )


def create_ticker_list():
    ticker_list = []
    output_dir = "./output/headline_sentiment"
    for file_name in os.listdir(output_dir):
        if not file_name.startswith("."):
            ticker = file_name.split("_")[2]
            ticker = ticker.split(".")[0]
        ticker_list.append(ticker)
    return ticker_list


# 2) fix index for concat
# 3) fetch historical data


if __name__ == "__main__":
    ticker_list = create_ticker_list()
    yahoo_data_scrapper = Yahoo_Data_Scrapper(ticker_list)
    yahoo_data_scrapper.update_data()
