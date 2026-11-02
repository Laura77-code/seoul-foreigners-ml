# 03_economic_living — Findings

## 1. Research Question

How are work, income, education, and housing characteristics associated with overall life satisfaction?

The analysis uses the shared Seoul Foreign Residents Survey modeling dataset. The notebook examines the selected survey features as predictors of overall life satisfaction (`Q11`). Because this is observational survey data, the results describe associations and predictive patterns; they do **not** establish causal effects.

## 2. Dataset and Shared Split

- Shared master dataset: **2,500 respondents** and 165 columns.
- Training set: **2,000 respondents**.
- Test set: **500 respondents**.
- Random state: **42**.
- Regression target: `Q11` (overall life satisfaction).
- Classification target: `high_satisfaction` (`Q11 >= 8`).
- In the full dataset, the high-satisfaction class accounts for **65.52%** and the lower-satisfaction class for **34.48%**.
- `Q11` has a mean of **7.768**, standard deviation of **1.131**, median of **8**, and observed range of **0–10**.

## 3. Codebook-verified Features

The notebook uses the following 14 predictor columns:

| Feature | Notebook data type | Missing (%) | Unique non-missing values |
|---|---|---:|---:|
| `SQ1` | Nominal | 0.00 | 10 |
| `SQ2` | Nominal | 0.00 | 9 |
| `SQ5` | Nominal | 0.00 | 6 |
| `SQ6` | Nominal | 0.00 | 5 |
| `SQ7` | Nominal | 0.00 | 2 |
| `DQ1` | Nominal | 0.00 | 12 |
| `DQ2` | Nominal | 31.56 | 7 |
| `DQ4_1` | Nominal | 0.00 | 7 |
| `DQ4_2` | Ordinal | 0.00 | 5 |
| `age` | Numeric | 0.00 | 53 |
| `months_in_korea_log1p` | Numeric | 0.00 | 196 |
| `SQ6_1_log1p` | Numeric | 31.32 | 85 |
| `SQ6_2_log1p` | Numeric | 32.72 | 66 |
| `DQ3` | Numeric | 31.56 | 19 |

**Codebook limitation:** The supplied notebook contains variable codes and modeling types, but it does not include the official question wording, response labels, or category coding direction. Therefore, the substantive meanings of `SQ1`, `SQ2`, `SQ5`, `SQ6`, `SQ7`, `DQ1`, `DQ2`, `DQ3`, `DQ4_1`, and `DQ4_2` cannot be verified from the supplied files alone. Do not describe these codes as employment, income, education, or housing variables until they have been checked against the official survey codebook. The `_log1p` columns are transformed numeric variables, but their original question meanings also need codebook confirmation.

The notebook treats the listed nominal variables as categories, `DQ4_2` as ordinal, and the remaining listed numeric variables as numeric. It notes that treating ordinal scores numerically is an approximation and that `DQ3` may need categorical treatment depending on its official coding.

## 4. Data Quality and Missingness

Four predictors have substantial missingness:

- `SQ6_2_log1p`: **32.72%**
- `DQ2`: **31.56%**
- `DQ3`: **31.56%**
- `SQ6_1_log1p`: **31.32%**

The other ten selected predictors have no missing values in the feature audit.

The notebook warns that missingness in `DQ2`, `DQ3`, `SQ6_1`, and `SQ6_2` may be caused by survey skip logic or subgroup-specific questions. Such values may mean “not applicable” rather than an ordinary unanswered response. They should not automatically be assumed to be missing at random. The modeling pipeline handles imputation, but imputation does not remove the need to explain the survey's conditional-question structure.

Before giving these variables substantive interpretations, check their original question wording, units, and category labels in the official codebook.

## 5. Training EDA Observations

All association summaries below use the **training split only**. The training-set mean of `Q11` is **7.772**.

For nominal variables, the notebook reports the range between category-level mean `Q11` values, considering groups with at least 15 observations. These are descriptive ranges, not effect sizes or causal estimates.

| Feature | Training-only summary | Value |
|---|---|---:|
| `DQ1` | Range of group mean `Q11` | 1.153 |
| `DQ2` | Range of group mean `Q11` | 1.050 |
| `SQ6` | Range of group mean `Q11` | 0.801 |
| `SQ1` | Range of group mean `Q11` | 0.670 |
| `DQ4_1` | Range of group mean `Q11` | 0.670 |
| `SQ5` | Range of group mean `Q11` | 0.574 |
| `SQ2` | Range of group mean `Q11` | 0.512 |
| `SQ7` | Range of group mean `Q11` | 0.021 |

For numeric and ordinal variables, the notebook reports Spearman correlations with `Q11`:

| Feature | Spearman's rho |
|---|---:|
| `DQ3` | 0.241 |
| `SQ6_1_log1p` | 0.140 |
| `SQ6_2_log1p` | -0.078 |
| `months_in_korea_log1p` | 0.058 |
| `age` | -0.003 |
| `DQ4_2` | 0.001 |

Within this set, `DQ3` has the largest positive Spearman association with `Q11`, followed by `SQ6_1_log1p`. These are correlations only. The category-level differences and correlations should not be interpreted until the variable meanings and coding directions are verified.

## 6. Cross-Validation Comparison

The notebook compares common baseline models using **5-fold cross-validation on the training set**, with fixed shared settings and no hyperparameter tuning.

### Regression

| Model | Mean CV RMSE | Mean CV MAE | Mean CV R² |
|---|---:|---:|---:|
| SVR (RBF) | **1.0281** | **0.7629** | **0.1678** |
| Random Forest | 1.0353 | 0.7666 | 0.1565 |
| Linear Regression | 1.0692 | 0.8071 | 0.0995 |
| Dummy Mean | 1.1281 | 0.8654 | -0.0011 |

**Selected regression model: SVR (RBF).** It has the lowest mean CV RMSE and MAE and the highest mean CV R² among the compared regression models.

### Classification

| Model | Mean CV macro-F1 | Mean CV accuracy | Mean CV ROC-AUC |
|---|---:|---:|---:|
| Logistic Regression | **0.5802** | 0.6670 | 0.6798 |
| SVC (RBF) | 0.5714 | **0.6850** | 0.6825 |
| Random Forest | 0.5217 | 0.6765 | **0.6958** |
| Dummy Most Frequent | 0.3958 | 0.6550 | 0.5000 |

**Selected classification model: Logistic Regression.** The notebook selects the model with the highest mean CV macro-F1, not the highest accuracy or ROC-AUC. Logistic Regression's macro-F1 is 0.5802, higher than SVC and Random Forest in this comparison.

## 7. Final Test Metrics

The selected models were evaluated once on the fixed test set.

### Regression — SVR (RBF)

- MAE: **0.7591**
- RMSE: **1.0509**
- R²: **0.1482**

The test RMSE is slightly higher than the mean cross-validation RMSE (1.0281). The test R² indicates that the model explains a limited proportion of the variation in `Q11`.

### Classification — Logistic Regression

- Accuracy: **0.6420**
- Precision: **0.6877**
- Recall: **0.8323**
- F1: **0.7531**
- Macro-F1: **0.5511**
- Balanced accuracy: **0.5557**
- ROC-AUC: **0.6536**

Confusion matrix (rows = actual class, columns = predicted class):

| | Predicted 0 | Predicted 1 |
|---|---:|---:|
| Actual 0 | 48 | 124 |
| Actual 1 | 55 | 273 |

The test set contains **172 class-0** respondents and **328 class-1** respondents. The classifier correctly identifies 273 of 328 class-1 cases, but correctly identifies only 48 of 172 class-0 cases. Its high class-1 recall therefore coexists with weak performance on the lower-satisfaction class. The accuracy is also below the 65.5% majority-class share in the full dataset, so accuracy alone would give an incomplete picture. Macro-F1 and balanced accuracy make the class-wise performance limitation clearer.

## 8. Interpretation and Limitations

The training-only permutation-importance outputs rank `SQ6`, `SQ2`, `SQ1`, `DQ3`, and `DQ4_1` highly for the regression model. For classification, the leading features are `DQ4_1`, `DQ1`, `SQ6`, `SQ2`, and `DQ3`. The overlap suggests these coded variables may carry useful predictive information in this particular modeling setup.

These rankings are exploratory: the notebook calculates permutation importance on the training data for the fitted selected models. They are not causal effects, and they do not establish that changing a feature would change life satisfaction. Correlated predictors can also share or mask importance. Since the supplied files do not include the official codebook labels, the social meaning of these feature rankings remains unverified.

Other limitations:
- The analysis is observational and cannot establish causation.
- Several variables have substantial conditional missingness.
- Treating ordinal scores numerically may oversimplify their scale.
- `DQ3`'s numeric treatment should be checked against its official coding.
- The classification target is imbalanced (class 1 is the majority), and the selected classifier performs much better on class 1 than class 0.
- The test results are for final reporting and should not be used to retune models or choose features.

Potential social implications should be discussed only after confirming what each survey code represents. Avoid claiming that a particular economic or housing condition improves or reduces life satisfaction based on these model results alone.

## 9. Recommended Features for Notebook 05

The following **five candidates** are supported by the notebook's training-only permutation-importance rankings across the two selected models:

1. **`SQ6`** — among the strongest features for regression and classification.
2. **`DQ4_1`** — the highest-ranked classification feature and also high for regression.
3. **`DQ1`** — highly ranked for classification and among the stronger regression features.
4. **`SQ2`** — consistently high in both regression and classification importance.
5. **`DQ3`** — among the stronger features for both tasks and has the largest numeric/ordinal Spearman correlation with `Q11` (rho = 0.241).

These are candidate predictors, not a final feature-selection decision. Confirm the official codebook meanings and category coding first. Notebook 05 should compare feature sets using training-only cross-validation rather than selecting features based on the fixed test results. In particular, `DQ3` has 31.56% missingness and needs careful handling.

## 10. Conclusion

Using 2,000 training respondents and 5-fold cross-validation, the notebook selected **SVR (RBF)** for regression and **Logistic Regression** for classification. On the 500-person test set, SVR achieved RMSE **1.0509** and R² **0.1482**. Logistic Regression achieved accuracy **0.6420** and macro-F1 **0.5511**, with substantially weaker recognition of the lower-satisfaction class than the high-satisfaction class.

Training-only EDA and permutation importance identify several potentially useful coded predictors, especially `SQ6`, `DQ4_1`, `DQ1`, `SQ2`, and `DQ3`. However, the supplied notebook does not contain the official codebook descriptions, so the meanings and coding directions of these variables must be verified before making claims about work, income, education, or housing. The findings are predictive and descriptive, not causal.
