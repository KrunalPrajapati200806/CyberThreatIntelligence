import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from backend.feature_schema import FINAL_FEATURES


DATA_PATH = "data/processed/ml_dataset.csv"
MODEL_PATH = "models/random_forest_multiclass.joblib"

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

RANDOM_STATE = 42

# Maximum number of BENIGN samples.
# We don't need all 2.1M benign rows for the
# multiclass classifier.
BENIGN_LIMIT = 250000

# Keep all attack classes.
# The rare classes will remain rare.
# This prevents us from inventing synthetic traffic.
ATTACK_LIMIT_PER_CLASS = None


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("=" * 70)
print("MULTICLASS RANDOM FOREST TRAINING")
print("=" * 70)

print("\nLoading dataset...")

usecols = FINAL_FEATURES + ["Label"]

df = pd.read_csv(
    DATA_PATH,
    usecols=usecols
)

print(f"Loaded rows: {len(df):,}")
print(f"Features: {len(FINAL_FEATURES)}")


# --------------------------------------------------
# CLEAN LABELS
# --------------------------------------------------

df["Label"] = (
    df["Label"]
    .astype(str)
    .str.strip()
)

print("\nOriginal class distribution:")
print(df["Label"].value_counts())


# --------------------------------------------------
# CLEAN FEATURES
# --------------------------------------------------

print("\nCleaning features...")

X = df[FINAL_FEATURES].apply(
    pd.to_numeric,
    errors="coerce"
)

X = X.replace(
    [np.inf, -np.inf],
    np.nan
)

X = X.fillna(0)

X = X.clip(
    lower=-1e30,
    upper=1e30
)

y = df["Label"]


# --------------------------------------------------
# SAMPLE BENIGN
# --------------------------------------------------

print("\nSampling dataset...")

benign_df = df[df["Label"] == "BENIGN"]

attack_df = df[df["Label"] != "BENIGN"]

print(
    f"Available BENIGN: "
    f"{len(benign_df):,}"
)

print(
    f"Available ATTACK: "
    f"{len(attack_df):,}"
)


if len(benign_df) > BENIGN_LIMIT:

    benign_sample = benign_df.sample(
        n=BENIGN_LIMIT,
        random_state=RANDOM_STATE
    )

else:

    benign_sample = benign_df


# --------------------------------------------------
# KEEP ALL ATTACK CLASSES
# --------------------------------------------------

attack_sample = attack_df.copy()


# --------------------------------------------------
# COMBINE
# --------------------------------------------------

sample_df = pd.concat(
    [
        benign_sample,
        attack_sample
    ],
    ignore_index=True
)

sample_df = sample_df.sample(
    frac=1,
    random_state=RANDOM_STATE
).reset_index(drop=True)


print("\nTraining distribution:")

print(
    sample_df["Label"]
    .value_counts()
)


# --------------------------------------------------
# CREATE X / y
# --------------------------------------------------

X = sample_df[FINAL_FEATURES].apply(
    pd.to_numeric,
    errors="coerce"
)

X = X.replace(
    [np.inf, -np.inf],
    np.nan
)

X = X.fillna(0)

X = X.clip(
    lower=-1e30,
    upper=1e30
)

y = sample_df["Label"]


# --------------------------------------------------
# TRAIN / TEST SPLIT
# --------------------------------------------------

print("\nCreating train/test split...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)

print(
    f"Training samples: {len(X_train):,}"
)

print(
    f"Testing samples: {len(X_test):,}"
)


# --------------------------------------------------
# RANDOM FOREST
# --------------------------------------------------

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    class_weight="balanced_subsample",
    n_jobs=-1,
    random_state=RANDOM_STATE
)

model.fit(
    X_train,
    y_train
)


# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

print("\nEvaluating model...")

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"\nAccuracy: "
    f"{accuracy:.4f}"
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_PATH
)

print("\n" + "=" * 70)
print("MODEL SAVED")
print("=" * 70)

print(
    f"\nPath: {MODEL_PATH}"
)

print(
    f"Classes: {len(model.classes_)}"
)

print("\nClass mapping:")

for index, name in enumerate(model.classes_):

    print(
        f"{index:2d} -> {name}"
    )

print("\nTraining complete.")