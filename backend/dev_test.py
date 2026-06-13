import pandas as pd
from backend.pipeline import run_analysis

FILE_PATH = r"data/raw/accepted_2007_to_2018Q4.csv"
df = pd.read_csv(
    FILE_PATH,
    nrows=2000
)

result = run_analysis(df)

print(result)