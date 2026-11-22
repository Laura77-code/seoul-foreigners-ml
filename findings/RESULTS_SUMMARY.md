# Corrected Benchmark Results — Reproduced Locally

This file reports **corrected** metrics from the re-executed `01`–`05` notebooks. All three thematic areas and the combined model used the same shared 2,000/500 respondent partition. Model selection was based on five-fold training CV, not the test set. Source metric files are generated in `results/` (ignored by Git), while `report/AGGREGATED_MODEL_RESULTS.csv` is a de-identified aggregate snapshot.

## Side-by-side comparison

| Analysis                | Regressor    |   CV_RMSE |   Test_RMSE |   Test_MAE |   Test_R2 | Classifier         |   CV_MacroF1 |   Test_Accuracy |   Test_MacroF1 |   Test_ROCAUC |
|:------------------------|:-------------|----------:|------------:|-----------:|----------:|:-------------------|-------------:|----------------:|---------------:|--------------:|
| Language & integration  | SVR_RBF      |     1.002 |       0.994 |      0.706 |     0.238 | RandomForest       |        0.623 |           0.736 |          0.65  |         0.747 |
| Economic & living       | SVR_RBF      |     1.035 |       1.061 |      0.758 |     0.131 | LogisticRegression |        0.603 |           0.646 |          0.55  |         0.648 |
| Health & discrimination | RandomForest |     1.004 |       1.065 |      0.772 |     0.126 | SVC_RBF            |        0.616 |           0.696 |          0.599 |         0.717 |
| Integrated model        | SVR_RBF      |     0.95  |       0.996 |      0.706 |     0.235 | SVC_RBF            |        0.659 |           0.736 |          0.678 |         0.751 |

### Interpretation

- **Language & integration** has the lowest thematic test RMSE and the strongest thematic ROC-AUC; the regression model nevertheless explains only about 24% of test-set variation.
- **Economic & living** contains useful associations but has weaker test performance, with classification accuracy below the majority-class baseline of 0.656. Its cross-validated macro-F1 still indicates some discrimination beyond naive prediction; inspect the confusion matrix.
- **Health & discrimination** has relevant self-rated-health and difficulty predictors, but the test minority-class recall remains limited. The corrected Q24 non-applicable codes mean earlier uncorrected metrics should not be reused.
- The **integrated model** shows better CV RMSE and CV macro-F1 than each thematic model, but its *test* regression R² is similar to language-only; the integrated classifier improves test macro-F1 relative to the thematic classifiers in this run. This is **exploratory** evidence, not proof of universal superiority.
- **Selection caution:** the 500-case test set was viewed during earlier team work; it is not an untouched confirmatory sample for Notebook 05.
- **Ethical and inference caution:** scores are conditional statistical predictions on one observational survey. Correlation, model reliance and feature importance do not establish causal impact, and no population-weighted estimates were computed.

### Evidence locations

- `findings/02_language_integration.md`
- `findings/03_economic_living.md`
- `findings/04_health_discrimination.md`
- `findings/05_global_ml_model.md`
- `findings/METHODOLOGY_CHANGELOG.md`
- `report/AGGREGATED_MODEL_RESULTS.csv`

**Modeling direction:** Evaluate missingness sensitivity, class weighting (within training CV only), ordinal-versus-nominal income encoding, and time/external validation if available. Preserve interpretability and evaluate whether complexity yields meaningful improvements over simpler baselines. Include a transparent report of the prior reuse of the test set.
