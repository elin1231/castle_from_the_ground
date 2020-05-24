import os
import csv
from pandas_datareader import data as pdr
import datetime
from datetime import date
import yfinance as yf
import pandas as pd


class yahoo_data_scrapper:
    def __init__(self, ticker):
        self.ticker = yf.Ticker(ticker)
        self.name = ticker
        self.date = date.today()
        self.dir = os.getcwd()

    def update_data(self):
        # finding index for dates that need to be updated
        for filename in os.listdir(
            os.path.join(os.getcwd(), "./output/headline_sentiment/sentiment_processed")
        ):
            if filename.split(".")[0] == self.name:
                cols = ["TICKER", "DATE", "COMPOUND", "UPDATED"]
                ticker_news_df = pd.read_csv(
                    os.path.join(
                        os.getcwd(),
                        "./output/headline_sentiment/sentiment_processed",
                        self.name + ".csv",
                    )
                )
                update_list = ticker_news_df[
                    ticker_news_df["UPDATED"] == "T"
                ].index.tolist()
                ticker_end_date = datetime.datetime.strptime(
                    ticker_news_df.iloc[update_list[0], 1], "%m/%d/%y"
                )
                ticker_start_date = datetime.datetime.strptime(
                    ticker_news_df.iloc[update_list[-1], 1], "%m/%d/%y"
                )
        # getting data from yf
        ticker_info_dict = self.ticker.info
        ticker_info_df = pd.DataFrame.from_dict(ticker_info_dict, orient="index").T
        ticker_training_set = pd.concat([ticker_news_df, ticker_info_df], axis=1)
        ticker_training_set.to_csv("./output/training_set/" + self.name + ".csv")


def create_ticker_list():
    ticker_list = []
    output_dir = os.path.join(
        os.getcwd(), "./output/headline_sentiment/sentiment_collection"
    )
    for file_name in os.listdir(output_dir):
        if not file_name.startswith("."):
            ticker = file_name.split("_")[2]
            ticker = ticker.split(".")[0]
        ticker_list.append(ticker)
