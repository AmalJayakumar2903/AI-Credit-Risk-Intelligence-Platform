from backend.ingestion.excel_loader import load_file
from backend.pipeline import run_analysis


FILE_PATH = r"data/raw/accepted_2007_to_2018Q4.csv"

df = load_file(
    FILE_PATH,
    nrows=2000
)

result = run_analysis(df)

# print(result["validation"])

print(result["cleaning_report"])