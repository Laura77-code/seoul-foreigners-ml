# Shared Modeling Configuration — Frozen for 02, 03, 04

All three notebooks use the shared code in `src/seoul_foreigners_ml/team_experiments.py`.

| Setting | Fixed value | Reason |
|---|---|---|
| Regression target | `Q11` | Original life satisfaction |
| Classification target | `high_satisfaction` (`Q11 >= 8`) | Notebook 01 |
| Split | Existing `train_ids.csv` / `test_ids.csv` | Identical respondents |
| Train/test | 2,000 / 500 | 80/20 stratified by binary target |
| Seed | `42` | Reproducibility |
| Validation | 5 folds, shuffled, seed 42 | Comparable training-only validation |
| CV classification | `StratifiedKFold(5)` | Similar class ratio per fold |
| CV regression | `KFold(5)` | Avoid using classification labels for regression CV folds |
| Selection | Lowest CV RMSE (regression), highest CV macro-F1 (classification) | No test-based tuning |
| Imputation nominal | Most frequent, fit inside each CV fold | No leakage |
| Imputation ordinal/numeric | Median, fit inside each CV fold | No leakage |
| Encoding | `OneHotEncoder(handle_unknown="ignore")` | Nominal categories |
| Scaling | `StandardScaler` numeric & ordinal | SVM / linear comparability |
| Baseline regression | `DummyRegressor(strategy="mean")` | Naive reference |
| Linear regression | `LinearRegression()` | Academic baseline |
| SVR | RBF, `C=1.0`, `epsilon=0.1`, `gamma="scale"` | Common fixed model |
| RandomForestRegressor | `n_estimators=200`, `max_depth=8`, `min_samples_leaf=3`, `random_state=42` | Common fixed complexity |
| Baseline classification | `DummyClassifier(strategy="most_frequent")` | Majority-class reference |
| Logistic Regression | `C=1.0`, `solver="lbfgs"`, `max_iter=2000` | Fixed baseline |
| SVC | RBF, `C=1.0`, `gamma="scale"`, `probability=True`, `random_state=42` | Fixed comparison |
| RandomForestClassifier | `n_estimators=200`, `max_depth=8`, `min_samples_leaf=3`, `random_state=42` | Fixed ensemble |
| Test reporting | Only chosen winning model per task | Avoid repeated test-set selection |
| Classification metrics | Accuracy, balanced accuracy, precision, recall, positive-class F1, macro-F1, ROC-AUC, confusion matrix | Class imbalance |
| Regression metrics | MAE, RMSE, R² | Original rating scale |
| Tunings | **None in 02–04** | Final tuning reserved for 05 |

**Important:** Fixed hyperparameters improve *comparability*, not prove the models are optimal. The three notebooks will differ in predictors and hence estimated performance. Treatment of ordinal variables as numeric is an explicit approximation; review against survey codebook.

Never include the target `Q11`, `high_satisfaction`, respondent `ID`, survey weights, or target-proximal `Q4_*`, `Q10_*`, `Q14` in a core predictor matrix.
