# Findings Template

# [Notebook Number] - [Research Area]: Findings

## 1. Research Question

Write the exact research question.

## 2. Data Used

- Dataset:
- Train observations:
- Test observations:
- Target:
- Feature families:

Confirm that the shared train/test IDs were used.

## 3. Selected Features

| Variable | Meaning | Type | Preprocessing | Reason for inclusion |
|---|---|---|---|---|

## 4. Data Quality Notes

Document:

- missing values;
- conditional questions;
- special codes;
- outliers;
- transformations;
- excluded features.

## 5. Main EDA Findings

Write evidence-based observations.

Do not simply describe charts.

Example structure:

> Respondents with ___ showed higher/lower Q11 values than ___.

## 6. Regression Results

| Model | CV RMSE | Test RMSE | Test MAE | Test R² |
|---|---:|---:|---:|---:|

### Best Regression Model

Explain the result and trade-offs.

## 7. Classification Results

| Model | CV F1 | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|

### Best Classification Model

Explain the result.

## 8. Feature Interpretation

Describe which features matter most and how.

Avoid causal language unless the analysis supports causality.

Prefer:

> associated with

instead of:

> causes

## 9. Limitations

Discuss:

- observational survey data;
- self-reported variables;
- missingness;
- class imbalance;
- possible measurement overlap;
- limited generalizability;
- model-specific limitations.

## 10. Recommended Features for Notebook 05

| Variable | Why keep it | Evidence |
|---|---|---|

## 11. Final Conclusion

Write 3–6 concise sentences answering the research question.
