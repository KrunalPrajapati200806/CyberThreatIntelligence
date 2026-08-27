from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)


# ============================================================
# PATHS
# ============================================================

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

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 70)
print("LOADING RANDOM FOREST")
print("=" * 70)

model = joblib.load(
    MODEL_PATH
)

print(
    f"Model loaded from:\n{MODEL_PATH}"
)


# ============================================================
# LOAD UNSEEN FRIDAY DATA
# ============================================================

print("\n" + "=" * 70)
print("LOADING UNSEEN FRIDAY TEST SET")
print("=" * 70)

df = pd.read_csv(
    TEST_PATH
)

print(
    f"Dataset shape: {df.shape}"
)


# ============================================================
# FEATURES / TARGET
# ============================================================

X = df.drop(
    columns=["Attack"]
)

y = df["Attack"]


print("\nClass distribution:")
print(
    y.value_counts()
)


# ============================================================
# FEATURE ALIGNMENT CHECK
# ============================================================

print("\nChecking feature compatibility...")

expected_features = list(
    model.feature_names_in_
)

actual_features = list(
    X.columns
)

if expected_features != actual_features:

    print("\nERROR: Feature mismatch!")

    missing = [
        col
        for col in expected_features
        if col not in actual_features
    ]

    extra = [
        col
        for col in actual_features
        if col not in expected_features
    ]

    print("Missing features:", missing)
    print("Extra features:", extra)

    raise ValueError(
        "Training and validation features do not match."
    )

print("Feature compatibility: OK")


# ============================================================
# PREDICTION
# ============================================================

print("\nRunning predictions...")

y_pred = model.predict(
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
# RESULTS
# ============================================================

print("\n" + "=" * 70)
print("UNSEEN FRIDAY RESULTS")
print("=" * 70)

print(
    f"Accuracy : {accuracy:.4f}"
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
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y,
    y_pred
)

print("Confusion Matrix:")
print(cm)


tn, fp, fn, tp = cm.ravel()

false_positive_rate = (
    fp / (fp + tn)
)

false_negative_rate = (
    fn / (fn + tp)
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
# SAVE REPORT
# ============================================================

REPORT_PATH = (
    REPORT_DIR
    / "random_forest_unseen_friday.txt"
)

with open(
    REPORT_PATH,
    "w"
) as f:

    f.write(
        "Random Forest — Unseen Friday Validation\n"
    )

    f.write(
        "=" * 60 + "\n\n"
    )

    f.write(
        f"Dataset size: {len(df):,}\n"
    )

    f.write(
        "Class distribution:\n"
    )

    f.write(
        str(y.value_counts())
        + "\n\n"
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

    f.write(report)

    f.write(
        "\nConfusion Matrix:\n"
    )

    f.write(
        str(cm)
    )

    f.write(
        f"\n\nFalse Positive Rate: "
        f"{false_positive_rate:.6f}\n"
    )

    f.write(
        f"False Negative Rate: "
        f"{false_negative_rate:.6f}\n"
    )

print(
    f"\nReport saved to:\n{REPORT_PATH}"
)