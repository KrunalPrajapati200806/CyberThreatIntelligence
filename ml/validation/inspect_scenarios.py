from pathlib import Path
import pandas as pd


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "CIC-IDS2017"
)

CHUNK_SIZE = 50_000


# --------------------------------------------------
# Find CSV files
# --------------------------------------------------

files = sorted(
    RAW_DIR.glob("*.csv")
)

print("Found files:")
print()

for file in files:
    print(file.name)


print("\n" + "=" * 70)
print("SCENARIO INSPECTION")
print("=" * 70)


# --------------------------------------------------
# Inspect every file
# --------------------------------------------------

for file in files:

    print("\n")
    print("=" * 70)
    print(file.name)
    print("=" * 70)

    total_rows = 0
    label_counts = {}

    first_chunk = True

    for chunk_number, chunk in enumerate(
        pd.read_csv(
            file,
            chunksize=CHUNK_SIZE,
            low_memory=False
        ),
        start=1
    ):

        # Clean column names
        chunk.columns = (
            chunk.columns
            .str.strip()
        )

        # Find label column
        label_column = None

        for column in chunk.columns:

            if column.lower() == "label":
                label_column = column
                break

        if label_column is None:

            raise ValueError(
                f"Label column not found in {file.name}"
            )

        # Print columns only once
        if first_chunk:

            print("\nColumns:")
            print(
                list(chunk.columns)
            )

            print(
                "\nLabel column:",
                label_column
            )

            first_chunk = False

        # Count rows
        total_rows += len(chunk)

        # Count labels
        counts = (
            chunk[label_column]
            .astype(str)
            .str.strip()
            .value_counts()
        )

        for label, count in counts.items():

            label_counts[label] = (
                label_counts.get(
                    label,
                    0
                )
                + int(count)
            )

        if chunk_number % 10 == 0:

            print(
                f"Processed "
                f"{chunk_number} chunks..."
            )

    # --------------------------------------------------
    # Final results for file
    # --------------------------------------------------

    print("\nTotal rows:")
    print(
        f"{total_rows:,}"
    )

    print("\nLabel distribution:")

    for label, count in sorted(
        label_counts.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        percentage = (
            count / total_rows
        ) * 100

        print(
            f"{label}: "
            f"{count:,} "
            f"({percentage:.2f}%)"
        )