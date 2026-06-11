import pandas as pd

from backend.analytics.risk import risk_summary

FILE_PATH = r"data/raw/accepted_2007_to_2018Q4.csv"

df = pd.read_csv(
    FILE_PATH,
    nrows=2000
)

print(risk_summary(df))