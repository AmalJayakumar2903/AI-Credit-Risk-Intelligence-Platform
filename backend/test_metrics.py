import pandas as pd

from backend.analytics.portfolio import portfolio_summary


FILE_PATH = r"data/raw/accepted_2007_to_2018Q4.csv"

df = pd.read_csv(
    FILE_PATH,
    nrows=2000
)

result = portfolio_summary(df)

print(result)