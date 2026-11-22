# Life Satisfaction Among Foreign Residents in Seoul

[![CI](https://github.com/OWNER/REPOSITORY/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPOSITORY/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

**Reproducible educational ML benchmark | 2025 Seoul Survey (foreign-resident sample) | English documentation**

> The CI badge contains placeholders `OWNER/REPOSITORY`. Replace both after creating the public GitHub repository. The repository is not published by this package.

## Executive summary

This open-source project studies factors **associated with** overall life satisfaction among foreign residents in Seoul. It compares interpretable linear models, kernel SVMs, ensemble models, and simple dummy baselines. We tackle both (a) **regression** of a 0–10 satisfaction score, and (b) **binary classification** of high satisfaction (`Q11 >= 8`). The four project workstreams are initial data understanding (`00`), shared preprocessing (`01`), three distinct thematic benchmarks (`02`–`04`), and an integrated comparison (`05`).

The 2025 foreign-resident survey contains **2,500 respondents and 157 original variables**. The processed modeling table adds derived features (165 columns in the original baseline design). Across 2,500 responses, 1,638 (65.52%) have `Q11 >= 8` and 862 (34.48%) have scores below 8. A majority-class prediction already achieves about **65.6% accuracy on the fixed test set**; macro-F1 and balanced accuracy are therefore essential.

### Research questions

1. How do Korean-language proficiency and perceived belonging relate to life satisfaction?
2. How do economic position, housing, and living conditions relate to life satisfaction?
3. How do self-rated health, social difficulties, and reported discrimination relate to life satisfaction?
4. Does an integrated set of conceptually distinct predictors improve cross-validated performance over individual thematic models?

**Scope:** predictive associations in cross-sectional self-reports; **not** causal inference, diagnosis, individual eligibility screening, or policy impact evaluation.

**Course dataset approval required:** The supplied assignment instructions say to select a dataset from provided options and mention WESAD. Confirm that the instructor accepts this Seoul Survey dataset before final submission.

## Dataset, provenance, and responsible reuse

- Source: Seoul Metropolitan Government, [Seoul Survey Urban Policy Indicators](https://data.seoul.go.kr/dataList/OA-15564/F/1/datasetView.do), 2025 edition.
- The survey covers registered foreign residents in Seoul aged 20+ with more than 90 days of residence; 2025 official survey notice specifies 2,500 foreign-resident respondents.
- Required local file: `data/raw/seoul_survey_foreigners_2025.xlsx` (survey data and Korean-language `코드북` worksheet).
- **The microdata are not included in this repository.** Review the data provider's current redistribution/use conditions independently; an MIT code license does **not** license the survey data.
- Keep `data/raw/` and `data/processed/` out of Git. Do not publish respondent-level records, IDs, or row-level predictions. Aggregated scores and codebook-derived variable descriptions are suitable for project documentation where allowed.
- Sampling weights are excluded from core ML predictors. These results do not claim population-weighted representativeness.

## Setup (Windows / Git Bash / macOS / Linux)

```bash
git clone https://github.com/OWNER/REPOSITORY.git
cd REPOSITORY
python -m venv .venv
# Windows Git Bash:
source .venv/Scripts/activate
# macOS / Linux:
# source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pip install -e .
```

Place the locally obtained Excel workbook at:

```text
data/raw/seoul_survey_foreigners_2025.xlsx
```

**Notebook run order (VS Code / Jupyter):**

```text
00_data_understanding.ipynb          --> descriptive audit of raw data
01_preprocessing.ipynb               --> cleaned master, train/test IDs
02_language_integration.ipynb        --> thematic benchmark
03_economic_living.ipynb             --> thematic benchmark
04_health_discrimination.ipynb       --> thematic benchmark
05_global_ml_model.ipynb             --> integrated benchmark
```

Select your `.venv` Python kernel. Run `00`, then `01`, then the later notebooks. Save the notebook outputs after `Run All`. **Do not recreate a different train/test split in each notebook.** The common source of truth is:

```text
data/processed/seoul_foreigners_modeling_master.csv
data/processed/train_ids.csv
data/processed/test_ids.csv
```

## Repository map

```text
.
├── .github/workflows/ci.yml      # Lint/test build (no private data)
├── src/seoul_foreigners_ml/      # Shared preprocessing, validation, experiment code
├── notebooks/                   # Numbered reproducible analyses, 00–05
├── tests/                       # Dataset-independent and optional local-data tests
├── findings/                    # Human-reviewed interpretation and change log
├── results/                     # Local/generated metric CSVs (ignored by Git)
├── figures/                     # Local/generated figures
├── report/                      # Assignment-ready report drafts, evidence guidance
├── PROJECT_CONTRACT.md          # Required shared scientific rules
├── MODEL_CONFIG.md              # Shared hyperparameters
├── CONTRIBUTING.md              # Pull-request workflow
└── LICENSE                      # MIT license for source code only
```

## Methods and reproducibility

1. **Survey-code audit:** interpret numeric codes using the official Korean codebook, not pandas dtype. Special `9` responses in relevant `Q6_*` / `Q24_*` questions mean non-applicable and are represented by missing values. `DQ3` is an income bracket, not a salary amount. See the [Methodology Change Log](findings/METHODOLOGY_CHANGELOG.md).
2. **Feature engineering:** `age = 2025 - SQ3`; `months_in_korea = 12 * SQ4_1 + SQ4_2`; Korean-proficiency mean and normalized score; optional `log1p` for right-skewed nonnegative numerical variables.
3. **Fixed split:** 2,000 training and 500 test IDs, stratified by `high_satisfaction` with seed 42; the test set is held out from fold-wise fitting. Every team member uses the same 500 test respondents.
4. **Fold-wise preprocessing:** nominal missingness becomes a distinct sentinel then one-hot categories; ordinal/continuous features use median imputation with missingness indicators and StandardScaler, all fitted in the training folds.
5. **Benchmark:** for each theme, Dummy/Linear Regression/SVR/Random Forest for regression; Dummy/Logistic Regression/SVC/Random Forest for classification. The same fixed model parameters are used for all comparisons.
6. **Model selection:** training 5-fold CV: minimize RMSE for regression; maximize macro-F1 for classification. Inspect the test set **after selection**. ROC-AUC uses continuous prediction scores.
7. **Interpretation:** Spearman/group differences for exploratory EDA; held-out-training permutation importance for model reliance, not causal inference.
8. **Integrated model:** predeclared union of thematic feature families; report the test-use caveat in the integrated findings and final report.

For exact hyperparameters see [`MODEL_CONFIG.md`](MODEL_CONFIG.md). For methodological obligations see [`PROJECT_CONTRACT.md`](PROJECT_CONTRACT.md).

## Results and interpretation

The corrected, executed notebooks produce aggregated results in `results/`, with a human-readable summary in [`findings/RESULTS_SUMMARY.md`](findings/RESULTS_SUMMARY.md) and individual files `findings/02_*.md`, `03_*.md`, `04_*.md`, and `05_*.md`. **Metrics in generated files are only valid for the exact data transformation and code version that produced them.** Rerun after modifying preprocessing.

**Known evaluation limitation:** preliminary thematic test metrics were inspected before integrated modeling decisions. Therefore, the existing 500-person test set should not be characterized as an entirely blind final confirmation for Notebook 05. Independent replication or a fresh survey year would improve confidence.

## How to verify locally

```bash
python -m pytest -q
python scripts/verify_release.py
python scripts/verify_release.py --with-data
```

The last command checks private local processed data and generated results, without uploading or committing respondents' records. A project run can be considered reproducible when no notebook reports exceptions, all shared IDs align, feature/target exclusions hold, and all required CSVs exist.

## Open-source collaboration

We use GitHub issues for reproducible bugs and research tasks; short feature branches for parallel work; Pull Requests for peer review; and a reproducibility checklist in [`CONTRIBUTING.md`](CONTRIBUTING.md). Open issues should describe expected behavior, reproduction steps, error logs, and affected files, avoiding respondent-level data.

Suggested division: 02 language/integration, 03 economic/living, 04 health/discrimination, and a joint 05 integration/review. The actual individual contributions must be completed by the team in the final report; do **not** attribute work to someone without their approval.

## Assignment deliverables

The written report outline in `report/FINAL_REPORT_DRAFT.md` explicitly covers: introduction, related studies, methods/tools, experiment settings, results, discussion/conclusions, references, **individual member contributions**, and appendices with commented code and screenshots/output logs. A Word report can be made from this outline after the team verifies all final results.

## References

- Seoul Metropolitan Government, *Seoul Survey Urban Policy Indicators*, 2025 dataset: https://data.seoul.go.kr/dataList/OA-15564/F/1/datasetView.do
- OECD (2013), *OECD Guidelines on Measuring Subjective Well-being*: https://doi.org/10.1787/9789264191655-en
- Diener, E. et al. (1985), *The Satisfaction With Life Scale*, *Journal of Personality Assessment*, 49(1), 71–75: https://doi.org/10.1207/s15327752jpa4901_13
- Pedregosa, F. et al. (2011), *Scikit-learn: Machine Learning in Python*, *JMLR* 12, 2825–2830: https://jmlr.org/papers/v12/pedregosa11a.html

## License

Code is licensed under [MIT](LICENSE). Survey data and third-party materials retain their own separate terms. See `CONTRIBUTING.md` for responsible contribution and data handling.
