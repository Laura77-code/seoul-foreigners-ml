# 00 - Data Understanding: Conclusions

## Dataset Overview

The 2025 Seoul Survey foreign-resident dataset contains **2,500 respondents and 157 variables**. Respondent IDs are unique and no exact duplicate rows were detected.

Although all survey variables are stored numerically, many columns represent categorical or ordinal survey codes rather than continuous quantitative measurements. Therefore, storage dtype alone must not determine preprocessing decisions.

## Target Variable: Q11

`Q11` represents overall life satisfaction and contains no missing values.

Observed distribution:

| Q11 | Count | Percent |
|---:|---:|---:|
| 0 | 1 | 0.04% |
| 2 | 1 | 0.04% |
| 3 | 4 | 0.16% |
| 4 | 11 | 0.44% |
| 5 | 78 | 3.12% |
| 6 | 198 | 7.92% |
| 7 | 569 | 22.76% |
| 8 | 1,036 | 41.44% |
| 9 | 506 | 20.24% |
| 10 | 96 | 3.84% |

The distribution is concentrated toward high satisfaction scores, especially 7–9. This should be considered when defining a classification target.

## Missing Values

Missingness varies substantially across variables. Several columns contain very high missing rates, including variables above 90% and one variable with 100% missing observations.

These missing values must not automatically be treated as data-quality failures. Many survey questions are conditional or not applicable to all respondents. Each variable must therefore be interpreted using the codebook before deciding whether to:

- retain missing values;
- recode special survey values;
- impute values;
- or exclude the feature from a specific model.

## Preliminary Associations with Q11

The strongest numeric correlations with `Q11` include:

- `Q17_3`: 0.7447
- `Q10_5`: 0.5870
- `Q10_1`: 0.5790
- `Q10_3`: 0.5685
- `Q10_2`: 0.5655
- `Q10_4`: 0.5586

These values are exploratory only. High correlation does not automatically mean that a variable should be used as a predictor. Some of these variables may measure concepts very close to overall life satisfaction and can create target leakage or overly optimistic models.

## Main Conclusions

1. The dataset is sufficiently large for the planned machine-learning experiments.
2. `Q11` is complete and suitable as the main regression target.
3. Survey codes require semantic interpretation before preprocessing.
4. Missingness is strongly influenced by questionnaire logic.
5. Life satisfaction is skewed toward relatively high values.
6. Correlation analysis is useful for exploration but cannot replace codebook-based feature selection.
7. Target-proximal variables require a leakage audit before modeling.
8. A shared preprocessing strategy is necessary before the team divides into separate modeling tasks.
