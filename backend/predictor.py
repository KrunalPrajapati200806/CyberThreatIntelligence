import pandas as pd

from backend.feature_schema import FINAL_FEATURES
from backend.model_loader import model


def predict_attack(features: dict):

    received_features = set(features.keys())
    expected_features = set(FINAL_FEATURES)

    missing_features = expected_features - received_features
    extra_features = received_features - expected_features

    if missing_features:
        raise ValueError(
            f"Missing features: {sorted(missing_features)}"
        )

    if extra_features:
        raise ValueError(
            f"Unexpected features: {sorted(extra_features)}"
        )

    X = pd.DataFrame(
        [[features[name] for name in FINAL_FEATURES]],
        columns=FINAL_FEATURES
    )

    prediction = model.predict(X)[0]

    probabilities = model.predict_proba(X)[0]

    class_index = list(model.classes_).index(prediction)

    probability = float(probabilities[class_index])

    is_attack = prediction != "BENIGN"

    return {
        "prediction": prediction,
        "label": "ATTACK" if is_attack else "BENIGN",
        "threat_type": str(prediction),
        "is_attack": bool(is_attack),
        "probability": probability
    }


def predict_batch(X: pd.DataFrame):

    X = X[FINAL_FEATURES]

    predictions = model.predict(X)

    probabilities = model.predict_proba(X)

    class_indices = {
        cls: index
        for index, cls in enumerate(model.classes_)
    }

    results = []

    for i, prediction in enumerate(predictions):

        prediction = str(prediction)

        probability = float(
            probabilities[i][class_indices[prediction]]
        )

        is_attack = prediction != "BENIGN"

        results.append({
            "prediction": prediction,
            "label": "ATTACK" if is_attack else "BENIGN",
            "threat_type": prediction,
            "is_attack": bool(is_attack),
            "probability": probability
        })

    return results
