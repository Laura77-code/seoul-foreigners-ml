# 01 - Data Preprocessing: Conclusions

## Preprocessing Outcome

The preprocessing stage successfully prepared a common modeling foundation for the 2025 Seoul Survey foreign-resident dataset while preserving the original raw data.

The processed dataset retains **2,500 respondents** and uses a reproducible **80/20 stratified split**:

- Training set: **2,000 respondents**
- Test set: **500 respondents**

The proportion of high-satisfaction respondents is almost identical across the split:

- Train: **65.5%**
- Test: **65.6%**

This confirms that the stratified split preserves the classification-target distribution.

## Regression and Classification Targets

Two supervised-learning targets are retained:

- Regression target: `Q11`
- Classification target: `high_satisfaction`

The binary target is defined as:

- `0`: Q11 < 8
- `1`: Q11 >= 8

Class distribution:

- Lower satisfaction: **862 respondents (34.48%)**
- High satisfaction: **1,638 respondents (65.52%)**

The classification problem is moderately imbalanced, so later classification notebooks should report precision, recall, F1 score, ROC-AUC, and confusion matrices rather than relying only on accuracy.

## Derived Features

Three important feature-construction decisions were made:

- `age` is derived from `SQ3` and should generally replace birth year.
- `months_in_korea` combines `SQ4_1` and `SQ4_2`.
- `korean_proficiency_10` combines `Q1_1`–`Q1_4`.

Later models should avoid using both a derived feature and all of its source variables unless the experiment explicitly compares representations.

## Missing and Special Values

Verified code `9` values were converted to missing values for:

- `Q6_2`: 1,315 records
- `Q6_6`: 80 records
- `Q6_8`: 405 records
- `Q6_10`: 27 records

These values represent non-applicable responses rather than valid points on the original scale.

Other missing values remain untouched until model-specific pipelines. Imputation must be fitted using training data only.

## Outlier Review

IQR-based review flagged:

- `age`: 40 observations
- `months_in_korea`: 96 observations
- `SQ6_1`: 273 observations
- `SQ6_2`: 44 observations

These observations were **not removed automatically** because extreme survey responses can be legitimate.

## Distribution Shape

Strong positive skewness was found in:

- `months_in_korea`: 1.999
- `SQ6_1`: 5.175
- `SQ6_2`: 2.568

Log-transformed candidate features were therefore created for later model comparison:

- `months_in_korea_log1p`
- `SQ6_1_log1p`
- `SQ6_2_log1p`

The original variables are retained so later experiments can compare transformed and untransformed representations.

## Feature Types and Preprocessing

The shared schema separates:

- nominal features → mode imputation + one-hot encoding;
- ordinal features → median imputation + optional scaling;
- continuous/ratio features → median imputation + optional transformation + scaling.

Standardization is the default for scale-sensitive methods such as Logistic Regression and SVM. Min-max normalization remains available as an alternative.

All fitted transformations must use training data only.

## Leakage Control

The following are excluded from predictors:

- `ID`
- `Q11`
- `high_satisfaction`

Target-proximal variables such as `Q4_*`, `Q10_*`, and `Q14` are explicitly flagged. These variables should not automatically be included in the core predictive models because they may measure constructs too similar to overall life satisfaction.

## Final Modeling Decisions

The project will use the following shared rules:

- Keep `Q11` for regression.
- Keep `high_satisfaction` for classification.
- Use the same 80/20 stratified split for every team member.
- Never fit imputers, encoders, or scalers on the complete dataset.
- Preserve the raw survey file unchanged.
- Use codebook semantics to determine variable type.
- Treat highly missing conditional variables carefully rather than automatically imputing them.
- Do not automatically remove IQR outliers.
- Avoid redundant source/derived features in the same model.
- Keep target-proximal variables out of core models unless used in a clearly labeled extended experiment.
- Evaluate optional log transformations during modeling.
- Defer PCA and final feature selection to model-specific experiments.


## Split Validation

The exported train and test identifiers were independently verified.

- Modeling dataset: 2,500 unique respondents
- Training set: 2,000 unique respondents
- Test set: 500 unique respondents
- Train/test ID overlap: 0
- Train + test coverage: 100% of respondents
- High-satisfaction rate:
  - Full dataset: 65.52%
  - Training set: 65.50%
  - Test set: 65.60%
- Mean Q11:
  - Full dataset: 7.768
  - Training set: 7.772
  - Test set: 7.756

The exported split is therefore internally consistent and preserves the target distribution.