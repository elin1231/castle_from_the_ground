# %%
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


def web_scrap(tickers):
    for ticker in tickers:
        url = finviz_url + ticker
        if DEBUG_FLAG:
            print("URL: {}".format(url))
        try:
            req = Request(url=url, headers={"user-agent": "my-app/0.0.1"})
            response = urlopen(req, timeout=15)
            # Read the contents of the file into 'html'
            html = BeautifulSoup(response, features="lxml")
        except Exception:
            continue

        # Find 'news-table' in the Soup and load it into 'news_table'
        news_table = html.find(id="news-table")
        # Add the table to our dictionary
        news_tables[ticker] = news_table


def parse(tickers):
    # if DEBUG_FLAG:
    #     print("Scrapping ticker: {}".format(ticker))
    # print(news_table)
    # %%
    for ticker in tickers:
        try:
            current_company = news_tables[ticker]
            current_company_tr = current_company.findAll("tr")
        except Exception:
            break

        for i, table_row in enumerate(current_company_tr):
            # Read the text of the element 'a' into 'link_text'
            a_text = table_row.a.text
            # Read the text of the element 'td' into 'data_text'
            td_text = table_row.td.text
            # Print the contents of 'link_text' and 'data_text'
            print(a_text)
            print(td_text)
            # Exit after printing 4 rows of data
            if i == 3:
                break

        parsed_news = []

        # Iterate through the news
        for file_name, news_table in news_tables.items():
            # Iterate through all tr tags in 'news_table'
            for x in news_table.findAll("tr"):
                # read the text from each tr tag into text
                # get text from a only
                text = x.a.get_text()
                # splite text in the td tag into a list
                date_scrape = x.td.text.split()
                # if the length of 'date_scrape' is 1, load 'time' as the only element

                if len(date_scrape) == 1:
                    time = date_scrape[0]

                # else load 'date' as the 1st element and 'time' as the second
                else:
                    date = date_scrape[0]
                    time = date_scrape[1]
                # Extract the ticker from the file name, get the string up to the 1st '_'
                ticker = file_name.split("_")[0]

                # Append ticker, date, time and headline as a list to the 'parsed_news' list
                parsed_news.append([ticker, date, time, text])


# %%
def sentiment_analyze():
    for ticker in tickers:
        vader = SentimentIntensityAnalyzer()
        # Set column names
        columns = ["ticker", "date", "time", "headline"]

        # Convert the parsed_news list into a DataFrame called 'parsed_and_scored_news'
        parsed_and_scored_news = pd.DataFrame(parsed_news, columns=columns)

        # Iterate through the headlines and get the polarity scores using vader
        scores = (
            parsed_and_scored_news["headline"].apply(vader.polarity_scores).tolist()
        )

        # Convert the 'scores' list of dicts into a DataFrame
        scores_df = pd.DataFrame(scores)

        # Join the DataFrames of the news and the list of dicts
        parsed_and_scored_news = parsed_and_scored_news.join(
            scores_df, rsuffix="_right"
        )

        # Convert the date column from string to datetime
        parsed_and_scored_news["date"] = pd.to_datetime(
            parsed_and_scored_news.date
        ).dt.date

        parsed_and_scored_news.head()

        # This needs to be changed later
        parsed_and_scored_news.to_csv(
            "../output/sentiment_scored_{}.csv".format(ticker), index=False, header=True
        )


# %%
# work in progress have to rewrite so that the function returns records, and could be pieced together
company_info = pd.read_csv("../output/tickerList.csv")
tickers = company_info["TICKER"].tolist()

manager = Manager()
news_tables = manager.dict()
finviz_url = "https://finviz.com/quote.ashx?t="

with Pool(12) as p:
    p.map(web_scrap, tickers)

print(news_tables)
# with Pool(12) as p:
#     p.sentiment_analyze(tickers)
