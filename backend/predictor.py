# import pandas as pd

# from backend.feature_schema import FINAL_FEATURES
# from backend.model_loader import model


# def predict_attack(features: dict):

#     received_features = set(features.keys())
#     expected_features = set(FINAL_FEATURES)

#     missing_features = expected_features - received_features
#     extra_features = received_features - expected_features

#     if missing_features:
#         raise ValueError(
#             f"Missing features: {sorted(missing_features)}"
#         )

#     if extra_features:
#         raise ValueError(
#             f"Unexpected features: {sorted(extra_features)}"
#         )

#     X = pd.DataFrame(
#         [[features[name] for name in FINAL_FEATURES]],
#         columns=FINAL_FEATURES
#     )

#     prediction = model.predict(X)[0]

#     probabilities = model.predict_proba(X)[0]

#     class_index = list(model.classes_).index(prediction)

#     probability = float(probabilities[class_index])

#     is_attack = prediction != "BENIGN"

#     return {
#         "prediction": prediction,
#         "label": "ATTACK" if is_attack else "BENIGN",
#         "threat_type": str(prediction),
#         "is_attack": bool(is_attack),
#         "probability": probability
#     }


# def predict_batch(X: pd.DataFrame):

#     X = X[FINAL_FEATURES]

#     predictions = model.predict(X)

#     probabilities = model.predict_proba(X)

#     class_indices = {
#         cls: index
#         for index, cls in enumerate(model.classes_)
#     }

#     results = []

#     for i, prediction in enumerate(predictions):

#         prediction = str(prediction)

#         probability = float(
#             probabilities[i][class_indices[prediction]]
#         )

#         is_attack = prediction != "BENIGN"

#         results.append({
#             "prediction": prediction,
#             "label": "ATTACK" if is_attack else "BENIGN",
#             "threat_type": prediction,
#             "is_attack": bool(is_attack),
#             "probability": probability
#         })

#     return results

# import pandas as pd

# from backend.feature_schema import FINAL_FEATURES
# from backend.model_loader import model


# def predict_attack(features: dict):

#     received_features = set(features.keys())
#     expected_features = set(FINAL_FEATURES)

#     missing_features = expected_features - received_features
#     extra_features = received_features - expected_features

#     if missing_features:
#         raise ValueError(
#             f"Missing features: {sorted(missing_features)}"
#         )

#     if extra_features:
#         raise ValueError(
#             f"Unexpected features: {sorted(extra_features)}"
#         )

#     X = pd.DataFrame(
#         [[features[name] for name in FINAL_FEATURES]],
#         columns=FINAL_FEATURES
#     )

#     prediction = model.predict(X)[0]

#     probabilities = model.predict_proba(X)[0]

#     class_index = list(model.classes_).index(prediction)

#     probability = float(probabilities[class_index])

#     is_attack = prediction != "BENIGN"

#     return {
#         "prediction": prediction,
#         "label": "ATTACK" if is_attack else "BENIGN",
#         "threat_type": str(prediction),
#         "is_attack": bool(is_attack),
#         "probability": probability
#     }


# def predict_batch(X: pd.DataFrame):

#     X = X[FINAL_FEATURES]

#     predictions = model.predict(X)

#     probabilities = model.predict_proba(X)

#     class_indices = {
#         cls: index
#         for index, cls in enumerate(model.classes_)
#     }

#     results = []

#     for i, prediction in enumerate(predictions):

#         prediction = str(prediction)

#         probability = float(
#             probabilities[i][class_indices[prediction]]
#         )

#         is_attack = prediction != "BENIGN"

#         results.append({
#             "prediction": prediction,
#             "label": "ATTACK" if is_attack else "BENIGN",
#             "threat_type": prediction,
#             "is_attack": bool(is_attack),
#             "probability": probability
#         })

#     return results



import pandas as pd

from backend.feature_schema import (
    MULTICLASS_FEATURES,
    BINARY_FEATURES,
)

from backend.model_loader import (
    multiclass_model,
    binary_model,
)


# ==========================================================
# MODEL CONFIGURATION
# ==========================================================

MODEL_CONFIG = {
    "multiclass": {
        "model": multiclass_model,
        "features": MULTICLASS_FEATURES,
    },
    "binary": {
        "model": binary_model,
        "features": BINARY_FEATURES,
    },
}


# ==========================================================
# GET MODEL CONFIG
# ==========================================================

def get_model_config(model_type: str):

    model_type = str(model_type).lower().strip()

    if model_type not in MODEL_CONFIG:
        raise ValueError(
            f"Unknown model_type: {model_type}. "
            "Use 'binary' or 'multiclass'."
        )

    return MODEL_CONFIG[model_type]


# ==========================================================
# SINGLE PREDICTION
# ==========================================================

def predict_attack(
    features: dict,
    model_type: str = "multiclass"
):

    config = get_model_config(model_type)

    model = config["model"]
    expected_features = config["features"]

    received_features = set(features.keys())
    expected_features_set = set(expected_features)

    missing_features = (
        expected_features_set - received_features
    )

    extra_features = (
        received_features - expected_features_set
    )

    if missing_features:
        raise ValueError(
            f"Missing features: {sorted(missing_features)}"
        )

    if extra_features:
        raise ValueError(
            f"Unexpected features: {sorted(extra_features)}"
        )

    X = pd.DataFrame(
        [[features[name] for name in expected_features]],
        columns=expected_features
    )

    prediction = model.predict(X)[0]

    probabilities = model.predict_proba(X)[0]

    class_indices = {
        cls: index
        for index, cls in enumerate(model.classes_)
    }

    probability = float(
        probabilities[class_indices[prediction]]
    )

    if model_type == "binary":
        is_attack = bool(int(prediction) == 1)

        prediction_name = (
            "ATTACK"
            if is_attack
            else "BENIGN"
        )

        threat_type = prediction_name

    else:
        prediction_name = str(prediction)

        is_attack = (
            prediction_name != "BENIGN"
        )

        threat_type = prediction_name

    return {
        "model_type": model_type,
        "prediction": prediction_name,
        "label": (
            "ATTACK"
            if is_attack
            else "BENIGN"
        ),
        "threat_type": threat_type,
        "is_attack": bool(is_attack),
        "probability": probability,
    }


# ==========================================================
# BATCH PREDICTION
# ==========================================================

def predict_batch(
    X: pd.DataFrame,
    model_type: str = "multiclass"
):

    config = get_model_config(model_type)

    model = config["model"]
    expected_features = config["features"]

    X = X[expected_features]

    predictions = model.predict(X)

    probabilities = model.predict_proba(X)

    class_indices = {
        cls: index
        for index, cls in enumerate(model.classes_)
    }

    results = []

    for i, prediction in enumerate(predictions):

        probability = float(
            probabilities[i][
                class_indices[prediction]
            ]
        )

        if model_type == "binary":

            is_attack = bool(
                int(prediction) == 1
            )

            prediction_name = (
                "ATTACK"
                if is_attack
                else "BENIGN"
            )

            threat_type = prediction_name

        else:

            prediction_name = str(
                prediction
            )

            is_attack = (
                prediction_name != "BENIGN"
            )

            threat_type = prediction_name

        results.append({
            "model_type": model_type,
            "prediction": prediction_name,
            "label": (
                "ATTACK"
                if is_attack
                else "BENIGN"
            ),
            "threat_type": threat_type,
            "is_attack": bool(is_attack),
            "probability": probability,
        })

    return results
