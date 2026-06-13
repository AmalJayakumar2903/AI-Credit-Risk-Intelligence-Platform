# backend/test_status.py

import pandas as pd

FILE_PATH = r"data/raw/accepted_2007_to_2018Q4.csv"

df = pd.read_csv(
    FILE_PATH,
    nrows=2000
)

print(df["loan_status"].value_counts())