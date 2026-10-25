from pathlib import Path
import pandas as pd
from .paths import RAW_DATA_FILE

def list_excel_sheets(path: str | Path = RAW_DATA_FILE) -> list[str]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Place the workbook in data/raw/."
        )
    return pd.ExcelFile(path).sheet_names

def load_survey_data(path: str | Path = RAW_DATA_FILE, sheet_name: int | str = 0) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Place the workbook in data/raw/."
        )
    return pd.read_excel(path, sheet_name=sheet_name)

def load_codebook(path: str | Path = RAW_DATA_FILE) -> pd.DataFrame:
    path = Path(path)
    sheets = list_excel_sheets(path)
    candidates = [sheet for sheet in sheets if "코드북" in str(sheet)]
    if not candidates:
        raise ValueError("No codebook sheet containing '코드북' was found.")
    return pd.read_excel(path, sheet_name=candidates[0])
