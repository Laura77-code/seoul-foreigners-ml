# Machine Learning Analysis of Life Satisfaction Among Foreign Residents in Seoul

**Course:** Machine Learning — Team Final Project
**Dataset:** 2025 Seoul Survey, foreign-resident questionnaire (2,500 respondents)
**Status:** Reproducible corrected benchmark; team contribution statements and instructor dataset approval pending
**Prepared:** November 2026

## Abstract

This study investigates sample-level associations between overall life satisfaction and linguistic integration, socioeconomic and living conditions, and health/discrimination among foreign residents in Seoul. The outcome is the `Q11` survey score (0–10), modeled both as a continuous outcome and as a binary high-satisfaction indicator (`Q11 >= 8`). We use 2,500 respondents from the 2025 Seoul Survey, with a common stratified 2,000/500 train/test partition and five-fold cross-validation for model selection. Four fixed-parameter families are compared for each task: dummy, linear, kernel support vector machine, and random forest. Data preparation corrects special non-applicable survey codes and preserves missingness information within cross-validation pipelines. Among thematic models, linguistic/integration features provide the lowest test regression error and strongest ROC-AUC. The integrated model improves cross-validated RMSE and macro-F1, though the test regression score is similar to language alone. All results are observational and exploratory; independent replication, sampling-weight sensitivity, and minority-class detection are recommended next steps.

## 1. Introduction and Task Definition

Subjective well-being is a key aspect of quality of life, and understanding its associations in immigrant communities may guide future descriptive research and survey design. This project asks whether individual survey responses predict the self-reported overall life satisfaction score (`Q11`) among foreign residents of Seoul, and whether thematic feature groups differ in predictive usefulness. It does not estimate a causal effect of language study, income or discrimination on well-being.

**Questions:** (1) Which thematic feature family performs best under consistent cross-validation? (2) Does combining families improve performance? (3) What are the trade-offs between model complexity, interpretability, minority-class recall and generalization?

## 2. Prior Research and Conceptual Background

The OECD (2013) guidelines explain the relevance and measurement challenges of subjective well-being across economic and social domains. Diener et al. (1985) describe a psychological measure of global life satisfaction; their Satisfaction With Life Scale is a distinct instrument and must not be conflated with the Seoul Survey's single `Q11` item. The official Seoul Survey documentation describes the 2025 foreign-resident sample, questionnaire and sampling context. The study uses scikit-learn's standardized implementations of estimators (Pedregosa et al., 2011). These sources motivate a predictive cross-sectional benchmark; they do not independently validate its numerical findings.

## 3. Dataset and Preprocessing

The input workbook (`seoul_survey_foreigners_2025.xlsx`) includes 2,500 observations and 157 original columns plus an embedded Korean `코드북`. The project does not redistribute respondent-level microdata. Data understanding (`00`) established unique respondent IDs and a complete target. The target distribution is concentrated at high satisfaction: 1,638/2,500 (65.52%) score at least 8, while 862/2,500 (34.48%) score below 8. The original target is retained for regression, and the binary threshold of 8 is an explicit operational choice rather than a validated medical/social-risk cut-off.

Feature engineering includes age (2025 minus reported birth year), total months in Korea, an aggregate Korean proficiency score, and optional `log1p` variants of positive-skew numeric housing/residence fields. Redundant original and derived representations are not both inserted automatically in one model. Survey-category semantics come from the official codebook, not storage dtype.

### 3.1 Methodological audit and corrections

The initial benchmark revealed that code `9` had been interpreted as a valid high numeric value in some discrimination questions; the codebook instead identifies it as non-applicable/non-use. The corrected `01` preprocessing recodes applicable `Q24_*` `9` values to missing, consistent with special codes in selected `Q6_*` difficulty items. Other corrections treat `DQ3` as income brackets (not continuous KRW) and distinguish education level (`DQ4_1`) from education status (`DQ4_2`). The shared modeling pipeline represents nominal absence as a separate sentinel category and numeric absence via median imputation with missing indicators. All learned preprocessing transformations are fitted only to training folds. Permutation importance is now assessed on a holdout carved from the 2,000 training cases rather than using test-set feedback for feature selection. Full traceability appears in `findings/METHODOLOGY_CHANGELOG.md`.

### 3.2 Data split and leakage controls

Notebook 01 creates one stratified 80/20 split with random state 42: 2,000 train and 500 test respondent IDs; no duplicates or overlap. Regression target `Q11`, classification target `high_satisfaction`, respondent identifier and highly target-proximal happiness/satisfaction questions are excluded from model predictors. Survey weights are not model predictors; because sample weights are not used to estimate population quantities, our findings are not claims about population-representative effect sizes.

## 4. Methods and Tools

Code runs in Python, pandas, NumPy, Matplotlib and scikit-learn. The same four candidate estimators are used within each thematic and integrated pipeline. Regression: Dummy mean, ordinary least squares, RBF-SVR (C=1.0, epsilon=0.1), and random forest (200 trees, depth 8, minimum leaf 3). Classification: Dummy majority, logistic regression (C=1, max_iter=2000), RBF-SVC (C=1), and random forest with the same forest complexity constraints. Models are deliberately fixed for a fair first benchmark; no per-theme tuning is performed.

A shuffled five-fold training CV uses `KFold` for regression and `StratifiedKFold` for classification. The preferred regressor minimizes mean CV RMSE, and the preferred classifier maximizes mean CV macro-F1. The latter gives equal emphasis to high- and low-satisfaction groups. Continuous decision scores or probabilities are used for ROC-AUC where supported. Preprocessing and imputation live *inside* each cross-validation pipeline. We use training-only permutation importance for exploratory model interpretation, not as causal analysis.

## 5. Experimental Results

### 5.1 Common train/test protocol and aggregate metrics

All results below were generated from the corrected code and the same 2,000/500 respondent split. Final held-out test scores were inspected during earlier team iteration, therefore the integrated test is not a fully blinded external confirmation. The strongest evidence for integrated design comparison is the uniform training CV; external replication is needed for confirmation.

| Analysis                | Regressor    |   CV_RMSE |   Test_RMSE |   Test_MAE |   Test_R2 | Classifier         |   CV_MacroF1 |   Test_Accuracy |   Test_MacroF1 |   Test_ROCAUC |
|:------------------------|:-------------|----------:|------------:|-----------:|----------:|:-------------------|-------------:|----------------:|---------------:|--------------:|
| Language & integration  | SVR_RBF      |     1.002 |       0.994 |      0.706 |     0.238 | RandomForest       |        0.623 |           0.736 |          0.65  |         0.747 |
| Economic & living       | SVR_RBF      |     1.035 |       1.061 |      0.758 |     0.131 | LogisticRegression |        0.603 |           0.646 |          0.55  |         0.648 |
| Health & discrimination | RandomForest |     1.004 |       1.065 |      0.772 |     0.126 | SVC_RBF            |        0.616 |           0.696 |          0.599 |         0.717 |
| Integrated model        | SVR_RBF      |     0.95  |       0.996 |      0.706 |     0.235 | SVC_RBF            |        0.659 |           0.736 |          0.678 |         0.751 |

### 5.2 Comparative reading

The language/integration model yields regression test RMSE approximately **0.994** and test R² approximately **0.238**. Its classifier achieves test ROC-AUC approximately **0.747**, but identifies only 60 of 172 lower-satisfaction test respondents correctly. Economic/living features produce weaker test regression fit (RMSE approximately **1.061**) and a classifier accuracy of **0.646**, below the simple test-set majority proportion of **0.656**; accuracy is therefore an insufficient measure of its performance. Health/discrimination models obtain regression test RMSE approximately **1.064** and ROC-AUC approximately **0.717**. Importances highlight self-rated health `Q15`, but cannot establish causes.

The integrated model achieves the best cross-validated regression RMSE (**0.950**) and cross-validated classification macro-F1 (**0.659**) of the four feature groups. On the repeatedly inspected test set, its regression RMSE (**0.996**) is almost identical to language-only (**0.994**); integrated classification macro-F1 (**0.678**) is higher than the three thematic classifiers (**0.650**, **0.550**, **0.599**). This pattern supports testing integration in a separate study, not declaring it universally superior.

### 5.3 Failure modes, class imbalance, and uncertainty

The majority class accounts for 328 of 500 test cases; a constant high-satisfaction predictor achieves 65.6% test accuracy. Each thematic classifier favors the positive/high-satisfaction class. Lower-satisfaction recall is comparatively low; macro-F1 and balanced accuracy are more appropriate than overall accuracy for evaluating both groups. Five-fold CV uncertainty, represented by fold-to-fold score standard deviations, should be considered when comparing small model-score gaps. A non-significant numeric difference must not be described as meaningful superiority without further resampling or independent data.

## 6. Discussion, Strengths, and Weaknesses

**Strengths:** explicit survey-code audit; shared train/test respondent IDs; identical models and parameters across thematic benchmarks; appropriate dummy baselines; fold-wise train-only preprocessing; regularized and nonlinear comparisons; CV-first model choice; separate regression and classification objectives; clear open-source reproducibility and privacy rules.

**Limitations:** a single cross-sectional self-report sample; possible measurement error and response bias; selection/missingness associated with questionnaire routing; no causal identification; no model fairness audit by subgroup; no population-weighted ML evaluation; high-scoring target and class imbalance; moderate predictive power; possible instability of permutation importance with correlated features. Critically, preliminary test results were viewed before integrated model design, so test-set results are exploratory rather than a truly untouched final evaluation.

## 7. Proposed Modeling Strategies

The evidence supports retaining interpretable linear/logistic models and RBF-SVMs as transparent baselines, while comparing random forests for nonlinear effects. Integrated feature families should be assessed by cross-validation and subject-matter rationale rather than cherry-picked test importances. Future work could examine class-weighted classification and calibrated thresholds for better detection of lower satisfaction, different principled encodings of income categories, sensitivity to missingness mechanisms, survey-weighted evaluation and explainability stability. Model selection/tuning should occur inside nested CV when feasible. If a new survey year or independent dataset becomes available, reserve it for genuine external validation.

## 8. Conclusion

The project demonstrates a reproducible approach to questionnaire-driven ML: semantics-aware preprocessing, shared folds and models, honest handling of naive baselines, and separate thematic and integrated analysis. Language/integration variables are most predictive individually in this sample, and integration improves CV summary scores for both tasks. Nevertheless, the integrated regression test score remains similar to language alone, and none of these findings establishes causal effects or generalizes automatically beyond the 2025 respondent sample.

## 9. Individual Member Contributions — REQUIRED BEFORE SUBMISSION

**Replace these placeholders with four team-approved statements and corresponding commit/PR references. Do not invent contributions.**

- **Member A — Language & Integration:** [Name], [EDA], [models], [findings], [PR(s) / commits].
- **Member B — Economic & Living:** [Name], [survey codebook review], [EDA], [models], [findings], [PR(s) / commits].
- **Member C — Health & Discrimination:** [Name], [Q6/Q24 review], [models], [interpretation], [PR(s) / commits].
- **Member D — Integration, QA, and Report:** [Name], [preprocessing audit], [global model], [CI/test/docs], [PR(s) / commits].

## References

1. Seoul Metropolitan Government (2025). *Seoul Survey Urban Policy Indicator Data*, 2025 edition. https://data.seoul.go.kr/dataList/OA-15564/F/1/datasetView.do
2. OECD (2013). *OECD Guidelines on Measuring Subjective Well-being*. OECD Publishing. https://doi.org/10.1787/9789264191655-en
3. Diener, E., Emmons, R. A., Larsen, R. J., & Griffin, S. (1985). The Satisfaction With Life Scale. *Journal of Personality Assessment*, 49(1), 71–75. https://doi.org/10.1207/s15327752jpa4901_13
4. Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html

## Appendix A. Reproducibility and Commented Code

The complete implementation is available in `notebooks/00_*.ipynb` through `notebooks/05_*.ipynb` and `src/seoul_foreigners_ml/team_experiments.py`. The reproducibility audit can be run with `python -m pytest -q` and `python scripts/verify_release.py --with-data` after locally generating the processed dataset. See `report/evidence/verification_log.txt` for the verification output from this release.

```python
# Shared split: use the same respondent IDs for every thematic benchmark.
root, all_rows, train, test = load_shared_data()

# Cross-validation trains an entire preprocessing + estimator pipeline per fold.
regression_scores = cv_compare(train, nominal, ordinal, numeric, 'regression')
classification_scores = cv_compare(train, nominal, ordinal, numeric, 'classification')

# The best estimator is chosen using training CV, not test-set accuracy.
regressor_name = regression_scores.iloc[0]['model']
```

## Appendix B. Figures and Output Evidence

- `report/evidence/cv_regression_rmse.png`: original chart generated from corrected CV metrics.
- `report/evidence/cv_classification_macro_f1.png`: corrected CV classification comparison.
- `report/evidence/test_roc_auc.png`: exploratory test ROC-AUC with repeat-test caveat.
- `report/AGGREGATED_MODEL_RESULTS.csv`: table of model performance.

**Submission evidence requirement:** capture VS Code/Jupyter screenshots of the final executed notebooks and model output cells **without respondent-level microdata**. Include at least one screenshot of an executed EDA chart, preprocessing code/output, CV model table and final confusion matrix. Capture these from your machine after `Run All`, then insert the images in the Word/PDF report. The figures above are directly generated aggregate results; they are not screenshots of the VS Code interface.

## Appendix C. Dataset Eligibility Check

The assignment says the chosen dataset should come from the course-provided options; the pasted course instructions mention WESAD as an example. **The team must confirm that the instructor accepts the Seoul Survey dataset** as an approved choice. This report assumes permission but does not assert it was granted.
