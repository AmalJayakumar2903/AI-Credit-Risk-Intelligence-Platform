import pandas as pd

from backend.profiler import profile_dataset

FILE_PATH = r"data/raw/accepted_2007_to_2018Q4.csv"

df = pd.read_csv(
    FILE_PATH,
    nrows=2000
)

print(profile_dataset(df))