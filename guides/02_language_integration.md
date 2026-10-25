# 02 - Language & Integration Guide

## Notebook

```text
notebooks/02_language_integration.ipynb
```

## Findings

```text
findings/02_language_integration.md
```

## Research Question

**How are Korean-language proficiency and social integration associated with life satisfaction among foreign residents in Seoul, and how well can these factors predict life satisfaction?**

## Core Dimension

Language and social integration.

## Shared Inputs

Use only:

```text
data/processed/seoul_foreigners_modeling_master.csv
data/processed/train_ids.csv
data/processed/test_ids.csv
```

Do not create a new split.

## Candidate Feature Families

### Korean proficiency

```text
Q1_1
Q1_2
Q1_3
Q1_4
```

or the derived:

```text
korean_proficiency_10
```

Do not automatically use both representations in the same model.

### Residence duration

Prefer:

```text
months_in_korea
```

Optional experiment:

```text
months_in_korea_log1p
```

### Integration / belonging variables

Identify relevant variables using the codebook, especially variables measuring:

- belonging to Korea;
- belonging to Seoul;
- neighborhood belonging;
- social/community participation;
- local social relationships;
- intention to continue living in Seoul.

Document every selected variable and its codebook meaning before modeling.

### Shared demographic controls

A small set of controls may be used where appropriate:

```text
age
SQ1
SQ2
SQ7
```

Do not allow demographic controls to become the main topic of the notebook.

## Analysis Requirements

### EDA

Show:

- Korean proficiency distributions;
- life satisfaction by Korean proficiency;
- life satisfaction by residence duration;
- selected belonging/integration distributions;
- relationships between selected integration variables and Q11.

### Regression

Baseline:

```text
Linear Regression
```

Additional model:

```text
SVR
```

Optional:

```text
DecisionTreeRegressor
RandomForestRegressor
```

Metrics:

```text
MAE
RMSE
R²
```

### Classification

Baseline:

```text
Logistic Regression
```

Additional model:

```text
SVM
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

## Feature Interpretation

Answer:

- Is Korean proficiency associated with life satisfaction?
- Does length of stay matter?
- Which integration variables contribute the most?
- Are individual language skills more informative than the combined score?

## Required Exports

Suggested:

```text
results/02_language_regression_metrics.csv
results/02_language_classification_metrics.csv
results/02_language_feature_summary.csv
```

## Findings File

The findings file should contain:

1. Research question
2. Features used
3. Main EDA findings
4. Best regression result
5. Best classification result
6. Most influential features
7. Interpretation
8. Limitations
9. What should be passed to Notebook 05
