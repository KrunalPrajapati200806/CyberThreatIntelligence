from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split


# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = Path(
    "data/processed/binary_training_sample.csv"
)

IMPORTANCE_PATH = Path(
    "reports/baseline/random_forest_feature_importance.csv"
)

MODEL_DIR = Path("models")
REPORT_DIR = Path("reports/feature_selection")

MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

TARGET = "Attack"
RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("RANDOM FOREST — FEATURE SELECTION EXPERIMENT")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")


X = df.drop(columns=[TARGET])
y = df[TARGET]


# ============================================================
# LOAD FEATURE IMPORTANCE
# ============================================================

print("\nLoading feature importance...")

importance_df = pd.read_csv(
    IMPORTANCE_PATH
)

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
).reset_index(drop=True)

print(
    f"Total available features: "
    f"{len(importance_df)}"
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print("\nCreating internal train/test split...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)

print(
    f"Training rows: {len(X_train):,}"
)

print(
    f"Testing rows : {len(X_test):,}"
)


# ============================================================
# FEATURE SETS
# ============================================================

feature_counts = [
    20,
    26,
    36,
    70
]


# ============================================================
# EXPERIMENT
# ============================================================

results = []

for n_features in feature_counts:

    print("\n" + "=" * 70)

    print(
        f"TRAINING RANDOM FOREST "
        f"WITH TOP {n_features} FEATURES"
    )

    print("=" * 70)

    selected_features = (
        importance_df
        .head(n_features)["Feature"]
        .tolist()
    )

    print("\nSelected features:")

    for rank, feature in enumerate(
        selected_features,
        start=1
    ):
        print(
            f"{rank:02d}. {feature}"
        )

    X_train_selected = X_train[
        selected_features
    ]

    X_test_selected = X_test[
        selected_features
    ]

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_leaf=2,
        class_weight=None,
        random_state=RANDOM_STATE,
        n_jobs=2
    )

    print("\nTraining...")

    rf_model.fit(
        X_train_selected,
        y_train
    )

    print("Training complete.")

    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    y_pred = rf_model.predict(
        X_test_selected
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

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

    print("\nResults:")

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

    # --------------------------------------------------------
    # SAVE MODEL
    # --------------------------------------------------------

    model_path = (
        MODEL_DIR /
        f"random_forest_top_{n_features}.joblib"
    )

    joblib.dump(
        rf_model,
        model_path
    )

    print(
        f"\nModel saved to:\n{model_path}"
    )

    # --------------------------------------------------------
    # SAVE FEATURE LIST
    # --------------------------------------------------------

    feature_path = (
        REPORT_DIR /
        f"top_{n_features}_features.txt"
    )

    with open(
        feature_path,
        "w",
        encoding="utf-8"
    ) as f:

        for rank, feature in enumerate(
            selected_features,
            start=1
        ):

            f.write(
                f"{rank}. {feature}\n"
            )

    # --------------------------------------------------------
    # STORE RESULTS
    # --------------------------------------------------------

    results.append({
        "Features": n_features,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1": f1
    })


# ============================================================
# COMPARISON
# ============================================================

comparison = pd.DataFrame(
    results
)

comparison = comparison.sort_values(
    by="F1",
    ascending=False
)

print("\n")
print("=" * 70)
print("FEATURE SELECTION COMPARISON")
print("=" * 70)

print(
    comparison.to_string(
        index=False
    )
)


# ============================================================
# SAVE COMPARISON
# ============================================================

comparison_path = (
    REPORT_DIR /
    "feature_selection_comparison.csv"
)

comparison.to_csv(
    comparison_path,
    index=False
)

print(
    f"\nComparison saved to:\n"
    f"{comparison_path}"
)

print("\nExperiment complete.")