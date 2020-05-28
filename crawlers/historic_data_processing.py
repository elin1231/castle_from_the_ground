from pandas_datareader import data as pdr
import pandas as pd
import os


historial_data_path = "./output/historical_data"

# For some reason these files are all empty
def remove_empty_files():
    for file in os.listdir(historial_data_path):
        if "^" in file:
            os.remove(os.path.join(historial_data_path, file))


# applied
def add_mean(df):
    if "Average" not in df.columns:
        print("CALCULATING AVERAGE")
        mean = []
        for index, row in df.iterrows():
            mean.append((row["High"] + row["Low"]) / 2)
        df["Average"] = mean


if __name__ == "__main__":
    remove_empty_files()
    for file in os.listdir(historial_data_path):
        if not file.startswith(".") and os.path.isfile(
            os.path.join(historial_data_path, file)
        ):
            print(file)
            with open(os.path.join(historial_data_path, file), "r") as csv_file:
                df = pd.read_csv(csv_file)
                # Add whatever method you want to do for historical data, all should be in their own method
                add_mean(df)
                # add_general_info(df, insert_columns)
                #
                df.to_csv(os.path.join(historial_data_path, file))
