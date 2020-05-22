from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv
from urllib.error import HTTPError
from multiprocessing import Pool, Manager

DEBUG_FLAG = True


def get_html(ticker):
    url = finviz_url + ticker
    try:
        req = Request(url=url, headers={"user-agent": "my-app/0.0.1"})
        response = urlopen(req, timeout=15)
        # Read the contents of the file into 'html'
        html = BeautifulSoup(response, features="lxml")
    except Exception:
        return None
    print(ticker)


# def web_scrap(ticker):
#     # Find 'news-table' in the Soup and load it into 'news_table'
#     news_table = html.find(id="news-table")
#     # Add the table to our dictionary
#     news_tables[ticker] = news_table
#     # news_tables[ticker] = html.find(id="news-table")


company_info = pd.read_csv("../output/tickerList.csv")
tickers = company_info["TICKER"].tolist()

manager = Manager()
news_tables = manager.dict()
finviz_url = "https://finviz.com/quote.ashx?t="

if __name__ == "__main__":
    with Pool(10) as p:
        p.map(get_html, tickers)
