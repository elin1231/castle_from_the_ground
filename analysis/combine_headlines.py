import os
import csv
import pandas as pd


headline_sentiment_path = "./output/headline_sentiment"


def parse_file(company_sentimenet_file):
    # 0 for ticker, 1 for date, 2 for time, 3 for headlines, 7 compound
    data_list = list(csv.reader(company_sentimenet_file))
    data_list.pop(0)
    parsed_dictionary = {}

    for row in data_list:
        date = row[1]
        if date in parsed_dictionary:
            parsed_dictionary[date][1].append(float(row[7]))
        else:
            parsed_dictionary[date] = [
                row[0],
                [float(row[7])],
                "F",
            ]
    for date in parsed_dictionary:
        parsed_dictionary[date][1] = sum(parsed_dictionary[date][1]) / len(
            parsed_dictionary[date][1]
        )
    df = pd.DataFrame.from_dict(parsed_dictionary, orient="index")
    df.columns = ("TICKER", "COMPOUND", "UPDATED")
    df.to_csv(
        "./output/sentiment_processed/{}.csv".format(data_list[0][0]), header=True
    )


if __name__ == "__main__":
    for sentiment_file in os.listdir(headline_sentiment_path):
        if not sentiment_file.startswith(".") and os.path.isfile(
            os.path.join(headline_sentiment_path, sentiment_file)
        ):
            with open(
                os.path.join(headline_sentiment_path, sentiment_file), "r"
            ) as company_sentimenet_file:
                parse_file(company_sentimenet_file)
