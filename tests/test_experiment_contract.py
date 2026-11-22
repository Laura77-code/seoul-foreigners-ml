"""Dataset-independent scientific-contract smoke tests."""
import numpy as np
import pandas as pd
import pytest
from seoul_foreigners_ml.team_experiments import (
    RANDOM_STATE, CV_FOLDS, candidates, validate_features,
    preprocessing,
)


def test_common_settings():
    assert RANDOM_STATE == 42
    assert CV_FOLDS == 5
    assert set(candidates('regression', ['SQ1'], [], ['age'])) == {'DummyMean','LinearRegression','SVR_RBF','RandomForest'}
    assert set(candidates('classification', ['SQ1'], [], ['age'])) == {'DummyMostFrequent','LogisticRegression','SVC_RBF','RandomForest'}


def test_excluded_targets_and_near_targets():
    frame = pd.DataFrame({'Q11':[7], 'ID':[100], 'Q20_1':[3], 'Q10_1':[4]})
    validate_features(frame, [], ['Q20_1'], [])
    with pytest.raises(ValueError):
        validate_features(frame, [], ['Q10_1'], [])
    with pytest.raises(ValueError):
        validate_features(frame, ['ID'], [], [])


def test_fold_preprocessing_handles_missing_and_unseen_categories():
    train = pd.DataFrame({'SQ1':[1, np.nan, 1, 2], 'age':[20,30,np.nan,50]})
    test = pd.DataFrame({'SQ1':[99, np.nan], 'age':[np.nan, 35]})
    pp = preprocessing(['SQ1'], [], ['age'])
    pp.fit(train)
    transformed = pp.transform(test)
    assert np.isfinite(transformed).all()
    assert transformed.shape[0] == len(test)
