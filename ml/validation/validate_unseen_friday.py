from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ==================================================
# PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "random_forest_binary.joblib"
)

TEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "validation"
    / "unseen_friday_test.csv"
)

REPORT_DIR = (
    PROJECT_ROOT
    / "reports"
    / "validation"
)

REPORT_PATH = (
    REPORT_DIR
    / "random_forest_unseen_friday.txt"
)


# ==================================================
# CONFIGURATION
# ==================================================

TARGET = "Attack"


# ==================================================
# HEADER
# ==================================================

print("=" * 70)
print("RANDOM FOREST — UNSEEN FRIDAY VALIDATION")
print("=" * 70)


# ==================================================
# CHECK FILES
# ==================================================

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"Model not found:\n{MODEL_PATH}"
    )

if not TEST_PATH.exists():

    raise FileNotFoundError(
        f"Unseen Friday test set not found:\n{TEST_PATH}"
    )


# ==================================================
# LOAD MODEL
# ==================================================

print("\nLoading Random Forest model...")

rf_model = joblib.load(
    MODEL_PATH
)

print("Model loaded.")


# ==================================================
# LOAD UNSEEN FRIDAY DATA
# ==================================================

print("\nLoading unseen Friday test set...")

df = pd.read_csv(
    TEST_PATH
)

print(
    f"Dataset shape: {df.shape}"
)


# ==================================================
# SPLIT FEATURES / TARGET
# ==================================================

# ==================================================
# SPLIT FEATURES / TARGET
# ==================================================

X_friday = df.drop(
    columns=[TARGET]
)

y_friday = df[TARGET]


# ==================================================
# MATCH TRAINING FEATURE NAMES
# ==================================================

# ==================================================
# MATCH TRAINING FEATURE SCHEMA
# ==================================================

# Normalize Friday feature names in the same general
# style used by the training preprocessing.

X_friday.columns = (
    X_friday.columns
    .str.strip()
    .str.replace(" ", "_", regex=False)
    .str.replace("/", "_per_", regex=False)
)


# --------------------------------------------------
# Explicit CICIDS feature-name normalization
# --------------------------------------------------

rename_map = {
    "Flow_Bytes_s": "Flow_Bytes_per_s",
    "Flow_Packets_s": "Flow_Packets_per_s",
    "Fwd_Packets_s": "Fwd_Packets_per_s",
    "Bwd_Packets_s": "Bwd_Packets_per_s",
    "Down_Up_Ratio": "Down_per_Up_Ratio",
}


X_friday = X_friday.rename(
    columns=rename_map
)


# ==================================================
# USE EXACT FEATURES EXPECTED BY MODEL
# ==================================================

expected_features = list(
    rf_model.feature_names_in_
)


missing_features = [
    feature
    for feature in expected_features
    if feature not in X_friday.columns
]


if missing_features:

    raise ValueError(
        "\nThe Friday dataset is missing features "
        "required by the trained model:\n"
        + "\n".join(
            f"- {feature}"
            for feature in missing_features
        )
    )


# Keep ONLY the features used during training
X_friday = X_friday[
    expected_features
]


# ==================================================
# FINAL SCHEMA VERIFICATION
# ==================================================

if list(X_friday.columns) != expected_features:

    raise ValueError(
        "Final feature schema does not match "
        "the trained Random Forest."
    )


print(
    f"\nFeature schema verified: "
    f"{X_friday.shape[1]} features."
)

print(
    "Feature order matches trained model."
)

# ==================================================
# VERIFY FEATURE COMPATIBILITY
# ==================================================

expected_features = list(
    rf_model.feature_names_in_
)

actual_features = list(
    X_friday.columns
)

if actual_features != expected_features:

    missing_features = [
        feature
        for feature in expected_features
        if feature not in actual_features
    ]

    extra_features = [
        feature
        for feature in actual_features
        if feature not in expected_features
    ]

    raise ValueError(
        "\nFeature mismatch after normalization!\n\n"
        f"Missing features: {missing_features}\n\n"
        f"Extra features: {extra_features}\n\n"
        f"Expected feature count: {len(expected_features)}\n"
        f"Actual feature count: {len(actual_features)}"
    )

print(
    f"\nFeature names verified: "
    f"{len(X_friday.columns)} features match the trained model."
)


print(
    f"Features: {X_friday.shape}"
)

print(
    f"Target: {y_friday.shape}"
)


# ==================================================
# CLASS DISTRIBUTION
# ==================================================

print("\nActual class distribution:")

print(
    y_friday.value_counts()
)

print("\nActual percentages:")

print(
    y_friday
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)


# ==================================================
# PREDICTION
# ==================================================

print("\nRunning Random Forest prediction...")

y_pred = rf_model.predict(
    X_friday
)

print("Prediction complete.")


# ==================================================
# METRICS
# ==================================================

accuracy = accuracy_score(
    y_friday,
    y_pred
)

precision = precision_score(
    y_friday,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_friday,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_friday,
    y_pred,
    zero_division=0
)


# ==================================================
# CONFUSION MATRIX
# ==================================================

cm = confusion_matrix(
    y_friday,
    y_pred
)

tn, fp, fn, tp = cm.ravel()


# ==================================================
# ERROR RATES
# ==================================================

false_positive_rate = (
    fp / (fp + tn)
    if (fp + tn) > 0
    else 0
)

false_negative_rate = (
    fn / (fn + tp)
    if (fn + tp) > 0
    else 0
)


# ==================================================
# CLASSIFICATION REPORT
# ==================================================

report = classification_report(
    y_friday,
    y_pred,
    target_names=[
        "BENIGN",
        "ATTACK"
    ],
    digits=4,
    zero_division=0
)


# ==================================================
# PRINT RESULTS
# ==================================================

print("\n" + "=" * 70)
print("UNSEEN FRIDAY RESULTS")
print("=" * 70)

print(
    f"\nAccuracy : {accuracy:.4f}"
)

print(
    f"Precision: {precision:.4f}"
)

print(
    f"Recall   : {recall:.4f}"
)

print(
    f"F1 Score : {f1:.4f}"
)

print("\nConfusion Matrix:")

print(cm)

print(
    f"\nTrue Negatives : {tn}"
)

print(
    f"False Positives: {fp}"
)

print(
    f"False Negatives: {fn}"
)

print(
    f"True Positives : {tp}"
)

print(
    f"\nFalse Positive Rate: "
    f"{false_positive_rate:.6f}"
)

print(
    f"False Negative Rate: "
    f"{false_negative_rate:.6f}"
)

print("\nClassification Report:")

print(report)


# ==================================================
# SAVE REPORT
# ==================================================

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    REPORT_PATH,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "Random Forest — Unseen Friday Validation\n"
    )

    f.write(
        "=" * 60 + "\n\n"
    )

    f.write(
        f"Test dataset: {TEST_PATH.name}\n"
    )

    f.write(
        f"Dataset size: {len(df):,}\n"
    )

    f.write(
        f"Model: {MODEL_PATH.name}\n\n"
    )

    f.write(
        f"Accuracy : {accuracy:.4f}\n"
    )

    f.write(
        f"Precision: {precision:.4f}\n"
    )

    f.write(
        f"Recall   : {recall:.4f}\n"
    )

    f.write(
        f"F1 Score : {f1:.4f}\n\n"
    )

    f.write(
        "Confusion Matrix\n"
    )

    f.write(
        "-" * 30 + "\n"
    )

    f.write(
        str(cm)
        + "\n\n"
    )

    f.write(
        f"True Negatives : {tn}\n"
    )

    f.write(
        f"False Positives: {fp}\n"
    )

    f.write(
        f"False Negatives: {fn}\n"
    )

    f.write(
        f"True Positives : {tp}\n\n"
    )

    f.write(
        f"False Positive Rate: "
        f"{false_positive_rate:.6f}\n"
    )

    f.write(
        f"False Negative Rate: "
        f"{false_negative_rate:.6f}\n\n"
    )

    f.write(
        "Classification Report\n"
    )

    f.write(
        "-" * 30 + "\n"
    )

    f.write(report)


print(
    f"\nReport saved to:\n{REPORT_PATH}"
)

print("\n" + "=" * 70)
print("UNSEEN FRIDAY VALIDATION COMPLETE")
print("=" * 70) 