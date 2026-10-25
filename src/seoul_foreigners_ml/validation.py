import pandas as pd

def validate_target(df: pd.DataFrame, target: str = "Q11") -> dict:
    if target not in df.columns:
        raise KeyError(f"Target variable '{target}' was not found.")
    series = df[target]
    return {
        "target": target,
        "rows": int(len(df)),
        "non_missing": int(series.notna().sum()),
        "missing": int(series.isna().sum()),
        "unique_values": int(series.nunique(dropna=True)),
        "dtype": str(series.dtype),
    }

def validate_required_columns(df: pd.DataFrame, columns: list[str]) -> list[str]:
    return [column for column in columns if column not in df.columns]
