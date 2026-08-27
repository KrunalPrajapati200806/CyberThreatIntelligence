from pathlib import Path
import pandas as pd
import numpy as np


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "CIC-IDS2017"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

def load_csv(file_path):
    print(f"\nLoading: {file_path.name}")

    df = pd.read_csv(file_path)

    print(f"Original shape: {df.shape}")

    return df


# --------------------------------------------------
# Clean column names
# --------------------------------------------------

def clean_column_names(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("/", "_per_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
    )

    return df


# --------------------------------------------------
# Clean labels
# --------------------------------------------------

def clean_labels(df):

    if "Label" not in df.columns:
        raise ValueError("Label column not found.")

    df["Label"] = df["Label"].astype(str).str.strip()

    return df


# --------------------------------------------------
# Replace infinite values
# --------------------------------------------------

def handle_infinite_values(df):

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    df[numeric_columns] = df[numeric_columns].replace(
        [np.inf, -np.inf],
        np.nan
    )

    return df


# --------------------------------------------------
# Handle missing values
# --------------------------------------------------

def handle_missing_values(df):

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    # Median is more robust than mean for highly
    # skewed network traffic features.
    for column in numeric_columns:

        if df[column].isnull().any():

            median_value = df[column].median()

            df[column] = df[column].fillna(
                median_value
            )

    return df


# --------------------------------------------------
# Remove duplicate rows
# --------------------------------------------------

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    print(
        f"Removed duplicates: {before - after}"
    )

    return df


# --------------------------------------------------
# Complete cleaning pipeline
# --------------------------------------------------

def clean_dataset(file_path):

    df = load_csv(file_path)

    print("\nCleaning column names...")
    df = clean_column_names(df)

    print("Cleaning labels...")
    df = clean_labels(df)

    print("Handling infinite values...")
    df = handle_infinite_values(df)

    print("Handling missing values...")
    df = handle_missing_values(df)

    print("Removing duplicate rows...")
    df = remove_duplicates(df)

    print(f"\nFinal shape: {df.shape}")

    return df


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    csv_files = sorted(RAW_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            "No CSV files found in CIC-IDS2017 folder."
        )

    print(f"Found {len(csv_files)} CSV files.")

    cleaned_datasets = []

    for file_path in csv_files:

        try:
            cleaned_df = clean_dataset(file_path)

            cleaned_datasets.append(cleaned_df)

        except Exception as e:

            print(
                f"\nERROR processing {file_path.name}:"
            )

            print(e)

    if not cleaned_datasets:
        raise RuntimeError(
            "No datasets were successfully processed."
        )

    print("\nCombining datasets...")

    unified_df = pd.concat(
        cleaned_datasets,
        ignore_index=True
    )

    print(
        f"Unified dataset shape: "
        f"{unified_df.shape}"
    )

    output_file = (
        PROCESSED_DIR /
        "cic_ids2017_unified.csv"
    )

    unified_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nUnified dataset saved to:\n"
        f"{output_file}"
    )

    print("\nFinal class distribution:")

    print(
        unified_df["Label"]
        .value_counts()
    )