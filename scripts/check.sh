#!/usr/bin/env bash
set -e

echo "== Project checks =="

python -c "import pandas, numpy, sklearn, openpyxl, matplotlib; print('Core dependencies: OK')"
python -c "import seoul_foreigners_ml; print('Project package:', seoul_foreigners_ml.__version__)"

pytest

if [ -f "data/raw/seoul_survey_foreigners_2025.xlsx" ]; then
  python - <<'PY'
from seoul_foreigners_ml.data import load_survey_data
from seoul_foreigners_ml.validation import validate_target

df = load_survey_data()
print("Local dataset:", validate_target(df, "Q11"))
PY
else
  echo "Local dataset not found: dataset-specific check skipped."
fi

echo "All available checks passed."
