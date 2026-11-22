# Shared Project Contract

**Project:** Machine Learning Analysis of Life Satisfaction Among Foreign Residents in Seoul.

This is the single methodological source of truth for notebooks 02–05. Read alongside `MODEL_CONFIG.md` and the official codebook sheet (`코드북`).

| Rule | Decision |
|---|---|
| Main target | `Q11`, overall life satisfaction, 0–10 |
| Secondary target | `high_satisfaction = 1(Q11 >= 8)`; positive label 1 |
| Data basis | 2025 Seoul Survey foreign-resident sample, 2,500 rows |
| Train/test | Fixed respondent IDs from notebook 01: 2,000/500, stratified by binary target |
| Random state | 42 |
| CV | 5 folds on **training only**, `KFold` (regression) / `StratifiedKFold` (classification) |
| Core model families | Dummy, Linear/Logistic, SVR/SVC (RBF), Random Forest |
| Model choice | Lowest training CV RMSE for regression; highest training CV macro-F1 for classification |
| Missing data | Codebook recoding first, then imputation inside folds; nominal missing sentinel and numeric missing indicators |
| Scaling | StandardScaler inside preprocessing pipeline; only fitted on training fold |
| Scoring | Regression MAE/RMSE/R²; classification accuracy/precision/recall/F1/macro-F1/balanced accuracy/ROC-AUC/confusion matrix |
| Feature exclusions | `ID`, `Q11`, `high_satisfaction`, weighting columns, `Q4_*`, `Q10_*`, `Q14` (target-proximal) |
| Derived features | Choose one representation per concept (birth year/age, duration/original components, skills/composite, monetary/log version) |
| Feature importance | Separate, training-only 80/20 holdout; **never** select for 05 using test-based importances |
| Reporting | Each notebook has `findings/NN_*.md`; publish aggregated metrics and evidence, not respondent-level microdata |

**Known corrections:** Code 9 for `Q6_*` and `Q24_*` special non-applicability is not part of their 1–5 scales. `DQ3` is a category of employment-income brackets, `DQ4_1` is educational attainment (ordinal), `DQ4_2` is completion/status (nominal), and `Q31=8` means no housing problem. Refer to `findings/METHODOLOGY_CHANGELOG.md`.

**Test-set caveat:** earlier team experiments used the same 500 test records for score inspection, so the comparison in Notebook 05 should not be described as an untouched final blind evaluation.

**Survey weighting caveat:** survey weights are excluded as features; population-level representativeness is not established by this ML benchmark.
