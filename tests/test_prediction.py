from backend.predictor import predict_attack
from backend.feature_schema import FINAL_FEATURES


def test_single_prediction():
    features = {
        feature: 0.0
        for feature in FINAL_FEATURES
    }

    result = predict_attack(features)

    assert "prediction" in result
    assert "label" in result
    assert "threat_type" in result
    assert "is_attack" in result
    assert "probability" in result

    assert result["label"] in ["BENIGN", "ATTACK"]
    assert isinstance(result["is_attack"], bool)
    assert 0.0 <= result["probability"] <= 1.0
