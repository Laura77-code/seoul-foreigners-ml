# Methodology Corrections and Rationale — Notebooks 01–04

**Project:** Machine Learning Analysis of Life Satisfaction Among Foreign Residents in Seoul
**Review date:** 2026-11-02
**Evidence reviewed:** official codebook embedded in `seoul_survey_foreigners_2025.xlsx`, notebooks 00–01, existing modeling master, shared training module, and the previously executed 02–04 results.

## 1. Why this revision was necessary

The first reproducible benchmark successfully used the same 2,000/500 respondent split and consistent model settings across three thematic analyses. A codebook-level review, however, identified special survey response codes and feature-type mismatches that could change how models interpret discrimination and economic circumstances. An additional audit found that the shared module provided test-based feature permutation, while notebooks separately calculated in-sample training permutation scores. Neither method should guide the selection of global-model features: test-based rankings can introduce test-driven selection, and in-sample rankings can overstate predictive usefulness. The revision addresses these issues before building Notebook 05.

## 2. Documented corrections

| ID | File and section | Before | After | Rationale |
|---|---|---|---|---|
| C01 | `notebooks/01_preprocessing.ipynb`, Section 8 | Q6 code 9 recoded, but Q24 code 9 left as numeric 9 | Also recode `Q24_1`–`Q24_5` code 9 to missing (when present) | Official codebook defines Q24 1–5 as discrimination degree and 9 as not applicable/non-use. 9 must not be interpreted as extreme discrimination. |
| C02 | `notebooks/03_economic_living.ipynb`, Section 3 | `DQ3` used as continuous numeric | `DQ3` treated as nominal categorical in the common benchmark | Codebook defines DQ3 as *ordered employment-income brackets*, not continuous monetary amounts; one-hot encoding avoids assuming equal numeric distances between brackets. An explicitly documented ordinal sensitivity analysis can be performed later. |
| C03 | `notebooks/03_economic_living.ipynb`, Section 3 | `DQ4_1` nominal, `DQ4_2` ordinal | `DQ4_1` ordinal (education level), `DQ4_2` nominal (graduation/completion status) | Education levels have an order, while graduation, ongoing study, leave, and withdrawal are statuses without a single defensible numerical order. |
| C04 | `src/seoul_foreigners_ml/team_experiments.py`, `preprocessing()` | Mode imputation for nominal variables | Explicit `-1` sentinel category for missing nominal data | Prevents imputing a fabricated employment/income/housing category when a question is conditional. The -1 sentinel is outside the original positive-valued survey codes and is a neutral missingness flag, *not* proof that the respondent is unemployed or the question is non-applicable. |
| C05 | Same module, `preprocessing()` | Median imputation for numeric and ordinal predictors | Median imputation with missing-value indicators | Retains information about whether a value was missing. This is especially relevant to housing deposit/rent and conditional survey questions. The numerical value itself is still imputed only within the training fold. |
| C06 | Same module, `feature_permutation()` | Permutation importance calculated on supplied test data | Refits a clone on 80% of shared training, evaluates permutation importance on the remaining 20% of training | Protects the fixed test set from feature-ranking decisions. The new training holdout is separate from the final 500 respondents and is not used to report final generalization. |
| C07 | Notebooks `02`, `03`, `04`, Section 9 | In-sample permutation importance using the already fitted pipeline on its own training records | Shared held-out-training permutation importance | Avoids over-optimistic in-sample importance and aligns feature interpretation methodology across all roles. |
| C08 | Notebook `04`, interpretation note | Generic caution about Q24 | Explicit codebook definitions of Q15, Q6 and Q24 | Health: Q15 1=very poor, 5=very good. Difficulty: Q6 1=not difficult, 5=very difficult. Discrimination: Q24 1=no discrimination, 5=severe discrimination, 9=not applicable. Interpretation direction matters. |
| C09 | Notebook `02`, interpretation note | Generic descriptions | Precise meanings of Q19 and Q20 | Q19 concerns local-community contacts, mutual assistance and participation; Q20 measures belonging to Korea, Seoul, neighborhood and origin country. Higher values indicate greater reported belonging. |
| C10 | Notebook `03`, interpretation note | Unresolved meanings of some codes | Clarifies `SQ6_1`, `SQ6_2` units, `Q31=8`, and DQ feature types | Housing deposit and rent are recorded in units of 10,000 KRW; Q31=8 means no housing problem. These definitions prevent false substantive conclusions. |

## 3. Verified codebook findings

- `Q24_3`: 91 respondents used special code 9 in the previously exported modeling master.
- `Q24_4`: 85 respondents used special code 9.
- `Q24_5`: 217 respondents used special code 9.
- `Q24_1`, `Q24_2`: no code 9 observed in the previously exported modeling master.
- `DQ2` and `DQ3`: 789 missing entries each, potentially explained by employment-related questionnaire routing; the meaning of individual missing values cannot be proven solely from the count.
- `Q6_2`: approximately 52.6% are missing after the existing recode of code 9, consistent with substantial non-applicability for childcare/education difficulties.
- `Q31=8` means **no housing problem**, not an unrecognized error.
- `SQ6_1` and `SQ6_2` are deposit and monthly rent amounts in **10,000 Korean won**, not plain KRW amounts.

## 4. What remains unchanged

The revision deliberately keeps all benchmark comparison settings fixed:

- Regression target: `Q11` (0–10 overall life satisfaction).
- Classification target: `high_satisfaction = (Q11 >= 8)`.
- Train/test split: 2,000/500 original respondent IDs; no new split of the full sample.
- Random state: 42; five-fold training cross-validation.
- Regression selection: lowest CV RMSE.
- Classification selection: highest CV macro-F1.
- Same model families and fixed benchmark hyperparameters (Dummy, Linear/Logistic Regression, SVR/SVC, Random Forest).
- Pipeline fitting, including imputation, encoding and scaling, takes place within each training fold.
- No target `Q11`, binary target, identifiers, or flagged target-proximal satisfaction/happiness variables are included in the core predictors.

## 5. Why earlier numeric results must not be reused

The previously recorded test metrics and feature importances for notebooks 02–04 were generated **before** these corrections. The newly recoded Q24 values and different encoding/imputation can change model coefficients, CV scores, selected model, test predictions, confusion matrices and feature rankings. Therefore, prior numbers must be labeled **pre-correction exploratory benchmark**, not silently copied as final results.

**Required reproducibility sequence:**

1. Run the corrected `01_preprocessing.ipynb`, creating a new `seoul_foreigners_modeling_master.csv`, `train_ids.csv` and `test_ids.csv`.
2. Confirm the existing split remains 2,000/500, with no overlap, and that special code 9 is absent from `Q24_*` valid-scale values.
3. Run revised notebooks `02`, `03` and `04` after installing the corrected shared module.
4. Replace their generated files in `results/`, and write final findings from the *new* CSV results.
5. Select candidates for Notebook 05 based on domain rationale and training-only validation. Do not repeatedly use test metrics to choose or adjust features.
6. Complete the final integrated evaluation with the original fixed 500 test respondents, and transparently document any further exploratory iterations.

## 6. Interpretation and limitations

This is observational, self-reported survey data. Correlations and permutation importance describe statistical associations or model reliance, **not causal effects**. High-missingness features can represent survey skip logic; adding missingness indicators preserves information but does not prove the reason for nonresponse. One-hot encoding of ordered income brackets in the benchmark is a conservative representational choice and may be compared with explicitly ordinal approaches using training-only validation. Permutation importance depends on the fitted model, holdout sample and correlated predictors; it is not a definitive ranking of causal or policy importance.

## 7. Suggested paragraph for the final report

> Following an audit of the official 2025 Seoul Survey codebook and our shared modeling pipeline, we revised data preprocessing and model interpretation before integrating thematic analyses. Specifically, the non-applicable code 9 in selected discrimination questions was recoded as missing, employment-income brackets were treated as categorical rather than continuous monetary observations, and educational attainment was distinguished from graduation status. We also modified the common pipeline to retain missingness information and moved permutation-based interpretation to a holdout within the training sample, thereby avoiding feature-selection decisions based on the final test set. All three thematic models were subsequently required to be rerun using the original fixed respondent split and identical cross-validation/model-selection settings. These changes improved semantic validity and methodological consistency; results produced prior to the revision are considered preliminary rather than final.
