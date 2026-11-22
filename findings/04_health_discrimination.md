# 04 — Health & Discrimination: Verified Findings

**Data source:** 2025 Seoul Survey, foreign-resident sample. **Observations:** 2,500; training: 2,000; test: 500. **Version:** corrected codebook-based preprocessing and common experiment module. **Targets:** regression `Q11`; classification `1(Q11 >= 8)`. This is a sample-level predictive study, not causal inference.

## 1. Research question

How strongly can the health & discrimination feature family predict overall life satisfaction, and how does it compare with common dummy, linear, kernel, and forest benchmarks under the same training-only CV protocol?

## 2. Features and missingness

See `results/04_health_feature_audit.csv` (generated locally) for the exact feature list, observed missing percentages, and data types. All categorical codes are interpreted against the official workbook codebook; non-applicable responses are not interpreted as higher scale values. Missingness treatment is fitted inside training CV folds.

## 3. Model selection (training only)

- **Regression selected:** `RandomForest`; mean 5-fold CV RMSE **1.004 ± 0.032**; mean CV R² **0.207**.
- **Classification selected:** `SVC_RBF`; mean 5-fold CV macro-F1 **0.616 ± 0.013**; mean CV ROC-AUC **0.728**.
- All four candidate models per task, including a Dummy baseline, were compared by five training folds with fixed settings (`MODEL_CONFIG.md`).

## 4. Test-set results (descriptive; reused across team analyses)

| Task | Selected model | Metric | Value |
|---|---|---|---:|
| Regression | RandomForest | MAE | 0.772 |
| Regression | RandomForest | RMSE | 1.065 |
| Regression | RandomForest | R² | 0.126 |
| Classification | SVC_RBF | Accuracy | 0.696 |
| Classification | SVC_RBF | Macro-F1 | 0.599 |
| Classification | SVC_RBF | Balanced accuracy | 0.601 |
| Classification | SVC_RBF | ROC-AUC | 0.717 |

**Confusion matrix:** actual 0 → predicted 0: 51; actual 0 → predicted 1: 121; actual 1 → predicted 0: 31; actual 1 → predicted 1: 297. The test set has 172 lower-satisfaction and 328 high-satisfaction respondents. Majority-class test accuracy is 328/500 = 0.656. Always interpret accuracy in relation to this baseline.

## 5. Feature interpretation (training-only permutation)

- **Regression's highest measured reliance:** `Q15`, `Q6_1`, `months_in_korea_log1p`, `Q6_2`, `Q24_1`.
- **Classifier's highest measured reliance:** `Q15`, `Q24_5`, `Q6_2`, `SQ2`, `months_in_korea_log1p`.

Permutation scores measure model reliance in a separate validation subset of training. They are affected by predictor correlation and are **not causal effects**. Do not treat the ranking as a statement about the intrinsic importance of social or policy factors.

## 6. Strengths and weaknesses

**Strengths:** shared sample split, training-only cross-validation, fold-wise imputation/encoding/scaling, dummy baselines, and consistent metrics for comparing regression and classification.

**Weaknesses:** survey answers are self-reported and cross-sectional; conditional skips and imputation can influence models; the positive class is more prevalent; high accuracy can coincide with weak identification of the minority class. The data are not independently revalidated outside the 2025 survey sample. Population representativeness is unproven without weight-aware methods.

## 7. Directions for the modeling strategy

Use performance measured in **training CV** and a theory-informed feature inventory to design further experiments. Evaluate class weighting, missingness sensitivity, and simpler models *within CV*, rather than repeatedly selecting changes from test performance. A future survey year or other external sample should provide independent final confirmation.

## 8. Individual contribution

**To be completed and approved by the responsible team member:** identify which portions of code, EDA, analysis, tests, peer review, and report writing were performed and linked PRs/commits. Do not assign unverified contribution claims.

## 9. Special health/discrimination caveat

The codebook defines `Q15` higher values as better self-rated health, `Q6_*` higher values as greater reported difficulty, and `Q24_*` higher values as more reported discrimination among valid 1–5 responses. Special `9` values in `Q24_3`–`Q24_5` denote nonuse/non-applicability, not greater discrimination, and are recoded in Notebook 01. `Q6_2` has substantial non-applicability; median imputation + missing indicator must not be interpreted as a true answer.
