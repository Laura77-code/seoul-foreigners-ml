import pytest

from seoul_foreigners_ml.data import load_survey_data
from seoul_foreigners_ml.paths import RAW_DATA_FILE
from seoul_foreigners_ml.validation import validate_target

@pytest.mark.skipif(not RAW_DATA_FILE.exists(), reason="Local raw dataset is not available.")
def test_local_dataset_contains_q11():
    df = load_survey_data()
    summary = validate_target(df, "Q11")
    assert summary["rows"] > 0
    assert summary["non_missing"] > 0
