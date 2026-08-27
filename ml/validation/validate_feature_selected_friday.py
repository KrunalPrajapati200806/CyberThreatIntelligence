from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)


# ============================================================
# PATHS
# ============================================================

MODEL_PATH = Path(
    "models/random_forest_top_36.joblib"
)

DATA_PATH = Path(
    "data/validation/unseen_friday_test.csv"
)

IMPORTANCE_PATH = Path(
    "reports/baseline/random_forest_feature_importance.csv"
)

REPORT_DIR = Path(
    "reports/validation"
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


TARGET = "Attack"


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("RANDOM FOREST — TOP 36 FEATURES — UNSEEN FRIDAY")
print("=" * 70)


# ============================================================
# LOAD MODEL
# ============================================================

print("\nLoading model...")

rf_model = joblib.load(
    MODEL_PATH
)

print("Model loaded.")


# ============================================================
# LOAD FEATURE IMPORTANCE
# ============================================================

importance_df = pd.read_csv(
    IMPORTANCE_PATH
)

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
).reset_index(drop=True)


selected_features = (
    importance_df
    .head(36)["Feature"]
    .tolist()
)

print(
    f"\nSelected features: "
    f"{len(selected_features)}"
)


# ============================================================
# LOAD FRIDAY DATA
# ============================================================

print("\nLoading unseen Friday dataset...")

df = pd.read_csv(
    DATA_PATH
)

print(
    f"Dataset shape: {df.shape}"
)


# ============================================================
# NORMALIZE FEATURE NAMES
# ============================================================

def normalize_feature_name(name):

    return (
        str(name)
        .strip()
        .replace(" ", "_")
        .replace("/", "_per_")
    )


normalized_columns = {
    column: normalize_feature_name(column)
    for column in df.columns
}

df = df.rename(
    columns=normalized_columns
)

selected_features_normalized = [
    normalize_feature_name(feature)
    for feature in selected_features
]


# ============================================================
# CHECK TARGET
# ============================================================

if TARGET not in df.columns:

    raise ValueError(
        f"Target column '{TARGET}' not found."
    )


# ============================================================
# CHECK FEATURES
# ============================================================

missing_features = [
    feature
    for feature in selected_features_normalized
    if feature not in df.columns
]

if missing_features:

    raise ValueError(
        "\nMissing selected features:\n"
        + "\n".join(missing_features)
    )


# ============================================================
# PREPARE DATA
# ============================================================

X = df[
    selected_features_normalized
]

y = df[TARGET]


print(
    f"\nFeatures: {X.shape}"
)

print(
    f"Target: {y.shape}"
)


# ============================================================
# FEATURE ORDER
# ============================================================

model_features = [
    normalize_feature_name(feature)
    for feature in rf_model.feature_names_in_
]

if model_features != selected_features_normalized:

    raise ValueError(
        "\nFeature order mismatch between "
        "model and selected feature list."
    )

print(
    "\nFeature names and order verified."
)


# ============================================================
# CLASS DISTRIBUTION
# ============================================================

print("\nActual class distribution:")

print(
    y.value_counts()
)

print("\nActual percentages:")

print(
    y.value_counts(
        normalize=True
    ).mul(100).round(2)
)


# ============================================================
# PREDICTION
# ============================================================

print("\nRunning prediction...")

y_pred = rf_model.predict(
    X
)

print("Prediction complete.")


# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(
    y,
    y_pred
)

precision = precision_score(
    y,
    y_pred
)

recall = recall_score(
    y,
    y_pred
)

f1 = f1_score(
    y,
    y_pred
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y,
    y_pred
)

tn, fp, fn, tp = cm.ravel()

false_positive_rate = (
    fp / (fp + tn)
)

false_negative_rate = (
    fn / (fn + tp)
)


# ============================================================
# RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("TOP-36 UNSEEN FRIDAY RESULTS")
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


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

report = classification_report(
    y,
    y_pred,
    target_names=[
        "BENIGN",
        "ATTACK"
    ],
    digits=4
)

print("\nClassification Report:")

print(report)


# ============================================================
# SAVE REPORT
# ============================================================

report_path = (
    REPORT_DIR /
    "random_forest_top_36_unseen_friday.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "Random Forest — Top 36 Features — "
        "Unseen Friday Validation\n"
    )

    f.write("=" * 60 + "\n\n")

    f.write(
        "Test dataset: unseen_friday_test.csv\n"
    )

    f.write(
        "Model: random_forest_top_36.joblib\n"
    )

    f.write(
        "Selected features: 36\n"
    )

    f.write(
        f"Dataset size: {len(df):,}\n\n"
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

    f.write("-" * 30 + "\n")

    f.write(
        str(cm) + "\n\n"
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

    f.write("-" * 30 + "\n")

    f.write(report)


print(
    f"\nReport saved to:\n{report_path}"
)

print("\n" + "=" * 70)
print("TOP-36 UNSEEN FRIDAY VALIDATION COMPLETE")
print("=" * 70)