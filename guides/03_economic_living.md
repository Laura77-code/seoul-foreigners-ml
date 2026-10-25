# 03 - Economic & Living Conditions Guide

## Notebook

```text
notebooks/03_economic_living.ipynb
```

## Findings

```text
findings/03_economic_living.md
```

## Research Question

**How are employment, income, housing, and living conditions associated with life satisfaction among foreign residents in Seoul, and how well can these factors predict life satisfaction?**

## Core Dimension

Economic and living conditions.

## Shared Inputs

Use:

```text
data/processed/seoul_foreigners_modeling_master.csv
data/processed/train_ids.csv
data/processed/test_ids.csv
```

Do not create another split.

## Candidate Feature Families

Use the codebook to identify and document variables related to:

- employment status;
- occupation;
- employment type;
- income;
- education;
- housing type;
- housing tenure;
- housing deposit;
- monthly rent;
- economic difficulties;
- urban living conditions.

Known derived/transformed candidates include:

```text
SQ6_1
SQ6_2
SQ6_1_log1p
SQ6_2_log1p
```

For highly skewed monetary variables, compare raw and log-transformed representations.

### Shared demographic controls

Possible:

```text
age
SQ1
SQ2
SQ7
months_in_korea
```

Keep the notebook focused on economic/living conditions.

## Target-Proximal Warning

Some `Q4_*` variables may represent direct satisfaction with living-environment dimensions.

They may be useful descriptively but are flagged as target-proximal.

Core predictive model:

```text
Exclude Q4_*
```

Optional explanatory model:

```text
Include selected Q4_* variables
```

If this optional model is used, report it separately and explain why it is expected to perform better.

## EDA

Show:

- income distribution;
- employment distribution;
- housing distribution;
- rent/deposit distributions;
- life satisfaction across important economic groups;
- effects of log transformation where relevant.

## Regression

Baseline:

```text
Linear Regression
```

Recommended nonlinear comparison:

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

## Classification

Baseline:

```text
Logistic Regression
```

Recommended:

```text
Decision Tree
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

## Feature Interpretation

Answer:

- Does employment status matter?
- Does income improve prediction?
- Are housing conditions important?
- Are monetary variables better modeled after log transformation?
- Which economic variables contribute most?

## Required Exports

```text
results/03_economic_regression_metrics.csv
results/03_economic_classification_metrics.csv
results/03_economic_feature_summary.csv
```

## Findings File

Include:

1. Research question
2. Feature list
3. Main EDA results
4. Raw vs. transformed variable observations
5. Regression comparison
6. Classification comparison
7. Important economic/living features
8. Limitations
9. Features recommended for Notebook 05
