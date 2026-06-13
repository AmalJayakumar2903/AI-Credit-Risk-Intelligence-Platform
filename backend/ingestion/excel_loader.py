import pandas as pd


def load_file(file_path, nrows=None):
    """
    Load CSV or Excel files into a Pandas DataFrame.
    """

    file_path = str(file_path)

    if file_path.lower().endswith(".csv"):
        return pd.read_csv(
            file_path,
            nrows=nrows,
            low_memory=False
        )

    elif file_path.lower().endswith(".xlsx"):
        return pd.read_excel(
            file_path,
            nrows=nrows
        )

    else:
        raise ValueError(
            f"Unsupported file type: {file_path}"
        )