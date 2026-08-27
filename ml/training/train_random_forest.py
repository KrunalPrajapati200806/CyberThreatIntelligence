from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
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

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "binary_training_sample.csv"
)

MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "reports" / "baseline"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("LOADING TRAINING DATA")
print("=" * 70)

df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")

X = df.drop(
    columns=["Attack"]
)

y = df["Attack"]


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"\nTraining shape: {X_train.shape}")
print(f"Testing shape : {X_test.shape}")


# ============================================================
# RANDOM FOREST
# ============================================================

print("\n" + "=" * 70)
print("CREATING RANDOM FOREST")
print("=" * 70)

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_leaf=2,
    class_weight=None,
    random_state=42,
    n_jobs=2
)

print("Training Random Forest...")

rf_model.fit(
    X_train,
    y_train
)

print("Training complete.")


# ============================================================
# INTERNAL TEST SET
# ============================================================

print("\n" + "=" * 70)
print("EVALUATING INTERNAL TEST SET")
print("=" * 70)

y_pred = rf_model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred
)

recall = recall_score(
    y_test,
    y_pred
)

f1 = f1_score(
    y_test,
    y_pred
)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "BENIGN",
            "ATTACK"
        ],
        digits=4
    )
)

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix:")
print(cm)


# ============================================================
# SAVE MODEL
# ============================================================

MODEL_PATH = (
    MODEL_DIR
    / "random_forest_binary.joblib"
)

joblib.dump(
    rf_model,
    MODEL_PATH
)

print(
    f"\nModel saved to:\n{MODEL_PATH}"
)


# ============================================================
# SAVE FEATURE IMPORTANCE
# ============================================================

feature_importance = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": rf_model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

FEATURE_PATH = (
    REPORT_DIR
    / "random_forest_feature_importance.csv"
)

feature_importance.to_csv(
    FEATURE_PATH,
    index=False
)

print(
    f"Feature importance saved to:\n{FEATURE_PATH}"
)


# ============================================================
# SAVE INTERNAL REPORT
# ============================================================

REPORT_PATH = (
    REPORT_DIR
    / "random_forest_internal_test.txt"
)

with open(
    REPORT_PATH,
    "w"
) as f:

    f.write(
        "Random Forest Binary Classification\n"
    )

    f.write(
        "=" * 60 + "\n\n"
    )

    f.write(
        f"Dataset size: {len(df):,}\n"
    )

    f.write(
        f"Training size: {len(X_train):,}\n"
    )

    f.write(
        f"Testing size: {len(X_test):,}\n\n"
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
        classification_report(
            y_test,
            y_pred,
            target_names=[
                "BENIGN",
                "ATTACK"
            ],
            digits=4
        )
    )

print(
    f"Internal report saved to:\n{REPORT_PATH}"
)

print("\n" + "=" * 70)
print("TRAINING COMPLETE")
print("=" * 70)