import pandas as pd
import pytest

from seoul_foreigners_ml.validation import validate_required_columns, validate_target

def test_validate_target_returns_expected_summary():
    df = pd.DataFrame({"Q11": [5, 7, None, 8]})
    summary = validate_target(df)
    assert summary["rows"] == 4
    assert summary["non_missing"] == 3
    assert summary["missing"] == 1
    assert summary["unique_values"] == 3

def test_validate_target_rejects_missing_target():
    df = pd.DataFrame({"Q10": [1, 2]})
    with pytest.raises(KeyError):
        validate_target(df)

def test_validate_required_columns():
    df = pd.DataFrame({"Q11": [7], "SQ1": [1]})
    assert validate_required_columns(df, ["Q11", "SQ1", "SQ2"]) == ["SQ2"]
