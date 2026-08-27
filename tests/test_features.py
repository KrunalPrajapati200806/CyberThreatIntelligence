import pandas as pd

from backend.feature_normalizer import prepare_features
from backend.feature_schema import FINAL_FEATURES


def test_final_feature_count():
    assert len(FINAL_FEATURES) == 36


def test_feature_names_are_unique():
    assert len(FINAL_FEATURES) == len(set(FINAL_FEATURES))


def test_prepare_features():
    data = {
        feature: [0.0]
        for feature in FINAL_FEATURES
    }

    df = pd.DataFrame(data)

    X = prepare_features(df)

    assert list(X.columns) == FINAL_FEATURES
    assert X.shape == (1, 36)
