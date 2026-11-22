# 02 — Language & Integration: Verified Findings

**Data source:** 2025 Seoul Survey, foreign-resident sample. **Observations:** 2,500; training: 2,000; test: 500. **Version:** corrected codebook-based preprocessing and common experiment module. **Targets:** regression `Q11`; classification `1(Q11 >= 8)`. This is a sample-level predictive study, not causal inference.

## 1. Research question

How strongly can the language & integration feature family predict overall life satisfaction, and how does it compare with common dummy, linear, kernel, and forest benchmarks under the same training-only CV protocol?

## 2. Features and missingness

See `results/02_language_feature_audit.csv` (generated locally) for the exact feature list, observed missing percentages, and data types. All categorical codes are interpreted against the official workbook codebook; non-applicable responses are not interpreted as higher scale values. Missingness treatment is fitted inside training CV folds.

## 3. Model selection (training only)

- **Regression selected:** `SVR_RBF`; mean 5-fold CV RMSE **1.002 ± 0.040**; mean CV R² **0.210**.
- **Classification selected:** `RandomForest`; mean 5-fold CV macro-F1 **0.623 ± 0.021**; mean CV ROC-AUC **0.722**.
- All four candidate models per task, including a Dummy baseline, were compared by five training folds with fixed settings (`MODEL_CONFIG.md`).

## 4. Test-set results (descriptive; reused across team analyses)

| Task | Selected model | Metric | Value |
|---|---|---|---:|
| Regression | SVR_RBF | MAE | 0.706 |
| Regression | SVR_RBF | RMSE | 0.994 |
| Regression | SVR_RBF | R² | 0.238 |
| Classification | RandomForest | Accuracy | 0.736 |
| Classification | RandomForest | Macro-F1 | 0.650 |
| Classification | RandomForest | Balanced accuracy | 0.644 |
| Classification | RandomForest | ROC-AUC | 0.747 |

**Confusion matrix:** actual 0 → predicted 0: 60; actual 0 → predicted 1: 112; actual 1 → predicted 0: 20; actual 1 → predicted 1: 308. The test set has 172 lower-satisfaction and 328 high-satisfaction respondents. Majority-class test accuracy is 328/500 = 0.656. Always interpret accuracy in relation to this baseline.

## 5. Feature interpretation (training-only permutation)

- **Regression's highest measured reliance:** `Q20_3`, `korean_proficiency_10`, `SQ1`, `months_in_korea_log1p`, `age`.
- **Classifier's highest measured reliance:** `Q20_2`, `SQ2`, `korean_proficiency_10`, `Q20_3`, `Q20_1`.

Permutation scores measure model reliance in a separate validation subset of training. They are affected by predictor correlation and are **not causal effects**. Do not treat the ranking as a statement about the intrinsic importance of social or policy factors.

## 6. Strengths and weaknesses

**Strengths:** shared sample split, training-only cross-validation, fold-wise imputation/encoding/scaling, dummy baselines, and consistent metrics for comparing regression and classification.

**Weaknesses:** survey answers are self-reported and cross-sectional; conditional skips and imputation can influence models; the positive class is more prevalent; high accuracy can coincide with weak identification of the minority class. The data are not independently revalidated outside the 2025 survey sample. Population representativeness is unproven without weight-aware methods.

## 7. Directions for the modeling strategy

Use performance measured in **training CV** and a theory-informed feature inventory to design further experiments. Evaluate class weighting, missingness sensitivity, and simpler models *within CV*, rather than repeatedly selecting changes from test performance. A future survey year or other external sample should provide independent final confirmation.

## 8. Individual contribution

**To be completed and approved by the responsible team member:** identify which portions of code, EDA, analysis, tests, peer review, and report writing were performed and linked PRs/commits. Do not assign unverified contribution claims.

## 9. Language and community integration caveat

`Q19_*` concerns community connections/participation and `Q20_*` concerns place-related belonging, with higher valid ratings generally indicating stronger agreement/belonging. We use the combined Korean language proficiency score rather than its four source variables in the same benchmark.
