# 04 - Health, Difficulties & Discrimination Guide

## Notebook

```text
notebooks/04_health_discrimination.ipynb
```

## Findings

```text
findings/04_health_discrimination.md
```

## Research Question

**How are health, difficulties living in Seoul, discrimination, and social vulnerability associated with life satisfaction among foreign residents in Seoul, and how well can these factors predict life satisfaction?**

## Core Dimension

Health and social vulnerability.

## Shared Inputs

Use:

```text
data/processed/seoul_foreigners_modeling_master.csv
data/processed/train_ids.csv
data/processed/test_ids.csv
```

Do not recreate the split.

## Candidate Feature Families

Use the codebook to identify and document variables related to:

- overall health;
- difficulties living in Seoul;
- discrimination experiences;
- reasons for discrimination;
- access to support;
- social relationships;
- community/social vulnerability.

### Q6 Variables

Notebook 01 already converted verified code `9` to missing for:

```text
Q6_2
Q6_6
Q6_8
Q6_10
```

Do not reverse this preprocessing.

Review missingness carefully because many difficulty questions are conditional.

## Target-Proximal Warning

The `Q10_*` variables are conceptually close to overall happiness/life satisfaction.

Core predictive model:

```text
Exclude Q10_*
```

Optional explanatory analysis:

```text
Analyze Q10_* descriptively or in a separately labeled extended model
```

Do not mix the extended model with the main model results.

## EDA

Show:

- health distribution;
- distribution of key difficulties;
- discrimination prevalence;
- Q11 by health category;
- Q11 by discrimination experience;
- missing-value patterns for conditional variables.

## Regression

Baseline:

```text
Linear Regression
```

Recommended additional model:

```text
SVR
```

Optional:

```text
RandomForestRegressor
```

Metrics:

```text
MAE
RMSE
R²
```

## Classification

Baseline:

```text
Logistic Regression
```

Recommended:

```text
SVM
Random Forest
```

Metrics:

```text
Accuracy
Precision
Recall
F1
ROC-AUC
Confusion Matrix
```

Recall and false negatives should receive special attention when interpreting vulnerability-related classification.

## Feature Interpretation

Answer:

- Is worse health associated with lower life satisfaction?
- Which difficulties living in Seoul matter most?
- Is reported discrimination associated with lower satisfaction?
- Which vulnerability variables remain useful after demographic controls?
- How does conditional missingness affect interpretation?

## Required Exports

```text
results/04_health_regression_metrics.csv
results/04_health_classification_metrics.csv
results/04_health_feature_summary.csv
```

## Findings File

Include:

1. Research question
2. Feature list
3. Missingness/conditional-question notes
4. Main EDA findings
5. Regression results
6. Classification results
7. Important features
8. Interpretation
9. Limitations
10. Features recommended for Notebook 05
