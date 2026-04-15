from pathlib import Path
import pandas as pd


def read_csv_file(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(file_path)