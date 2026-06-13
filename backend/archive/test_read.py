import pandas as pd

FILE_PATH = r"data/raw/accepted_2007_to_2018Q4.csv"

df = pd.read_csv(
    FILE_PATH,
    nrows=2000
)

print("\nFIRST 5 ROWS:")
print(df.head())

print("\nROWS:", len(df))
print("COLUMNS:", len(df.columns))

print("\nCOLUMN NAMES:")
print(df.columns.tolist())