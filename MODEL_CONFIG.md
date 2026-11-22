# Fixed Model Configuration (First Benchmark)

All 02–05 notebooks share these settings; model tuning, class weighting, and alternative thresholds must be separate training-only exploratory studies.

```python
RANDOM_STATE = 42
CV_FOLDS = 5
N_JOBS = 1
REGRESSION_TARGET = 'Q11'
CLASSIFICATION_TARGET = 'high_satisfaction'  # Q11 >= 8
```

| Task | Candidate | Fixed hyperparameters |
|---|---|---|
| Regression | DummyMean | `strategy='mean'` |
| Regression | LinearRegression | sklearn defaults |
| Regression | SVR_RBF | `kernel='rbf', C=1.0, epsilon=0.1, gamma='scale'` |
| Regression | RandomForest | `n_estimators=200, max_depth=8, min_samples_leaf=3, random_state=42, n_jobs=1` |
| Classification | DummyMostFrequent | `strategy='most_frequent'` |
| Classification | LogisticRegression | `C=1.0, max_iter=2000, solver='lbfgs', random_state=42` |
| Classification | SVC_RBF | `kernel='rbf', C=1.0, gamma='scale', probability=False` (decision scores for ROC-AUC) |
| Classification | RandomForest | `n_estimators=200, max_depth=8, min_samples_leaf=3, random_state=42, n_jobs=1` |

All candidate models are full pipelines with training-fold-only `ColumnTransformer` preprocessing. CV: shuffled 5-fold `KFold` for regression, shuffled 5-fold `StratifiedKFold` for classification. Winner: minimum mean CV RMSE / maximum mean CV macro-F1. Test evaluation is only *after* winner selection. Class 1 = high satisfaction. Do not use test-based importances for feature selection. The secondary integrated test score is exploratory because the same test IDs were already inspected in thematic analyses.
