# 05 - Integrated Model Plan

## Purpose

Notebook `05_global_ml_model.ipynb` combines evidence from notebooks 02–04.

It should not simply concatenate every variable.

Each role should recommend a small set of validated features based on:

- research relevance;
- missingness;
- predictive contribution;
- redundancy;
- leakage risk;
- interpretability.

## Inputs from Team Members

Each findings file must end with:

```text
Recommended features for Notebook 05
```

The integrated model will then compare:

### Classification

- Logistic Regression
- SVM
- Decision Tree
- Random Forest
- optional ensemble comparison

### Regression

- Linear Regression
- SVR
- Decision Tree Regressor
- Random Forest Regressor

## Optional Advanced Experiment

PCA may be tested as an additional experiment for scale-sensitive models.

It must be compared against the interpretable non-PCA model.

## Final Goal

Answer:

**Which combination of linguistic, integration, economic, living-condition, health, and vulnerability factors best predicts life satisfaction among foreign residents in Seoul?**
