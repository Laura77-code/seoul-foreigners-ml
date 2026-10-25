# Seoul Foreigners ML

Open-source machine learning project for analyzing and predicting life satisfaction among foreign residents in Seoul using the 2025 Seoul Survey.

## Main Objective

To analyze and predict overall life satisfaction among foreign residents in Seoul using demographic, socioeconomic, linguistic, health, and social-integration factors.

## Research Areas

1. Language & Integration
2. Economic & Living Conditions
3. Health, Difficulties & Discrimination
4. Integrated Machine Learning Model

## Repository Structure

```text
seoul-foreigners-ml/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/seoul_foreigners_ml/
├── tests/
├── scripts/
├── figures/
├── results/
├── report/
├── docs/
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Dataset

This repository does not redistribute the original 2025 Seoul Survey dataset.

Place the foreign-resident workbook at:

```text
data/raw/seoul_survey_foreigners_2025.xlsx
```

The raw dataset is excluded from Git tracking.

## Setup

### Windows with Git Bash

```bash
git clone <repository-url>
cd seoul-foreigners-ml
bash scripts/setup.sh
source .venv/Scripts/activate
```

Then place the dataset in `data/raw/`.

Verify the project:

```bash
bash scripts/check.sh
```

## Manual Setup

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

## Testing

```bash
pytest
```

Tests do not require the raw dataset. If the dataset is present locally, an additional dataset validation test is enabled.

## Open-Source Dependencies

This project uses:

- pandas
- NumPy
- Matplotlib
- scikit-learn
- openpyxl
- Jupyter
- pytest

Project-specific analysis, feature engineering, model selection, evaluation, and reusable code are implemented by the project team.

## Team Workflow

Do not work directly on `main`. Use feature branches and pull requests.

See `CONTRIBUTING.md` and `docs/team_workflow.md`.

## License

The source code is licensed under the MIT License.

The Seoul Survey dataset is not covered by this software license and remains subject to the terms of the official data provider.
