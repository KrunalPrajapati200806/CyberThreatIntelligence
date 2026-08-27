from pathlib import Path
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ml_binary_dataset.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "binary_training_sample.csv"
)

CHUNK_SIZE = 50_000

TARGET = "Attack"

# We want approximately 300,000 rows
# This is safer for an 8 GB RAM laptop.
SAMPLE_SIZE = 300_000

RANDOM_STATE = 42


# --------------------------------------------------
# First pass: count each class
# --------------------------------------------------

print("PASS 1: Counting classes...")

class_counts = {
    0: 0,
    1: 0
}

for chunk_number, chunk in enumerate(
    pd.read_csv(
        INPUT_PATH,
        chunksize=CHUNK_SIZE,
        usecols=[TARGET]
    ),
    start=1
):

    counts = chunk[TARGET].value_counts()

    for label in [0, 1]:

        class_counts[label] += int(
            counts.get(label, 0)
        )

    if chunk_number % 10 == 0:
        print(
            f"Scanned {chunk_number} chunks..."
        )


total_rows = sum(class_counts.values())

print("\nComplete class counts:")

print(
    f"BENIGN: {class_counts[0]:,}"
)

print(
    f"ATTACK: {class_counts[1]:,}"
)

print(
    f"TOTAL: {total_rows:,}"
)


# --------------------------------------------------
# Calculate sampling ratio
# --------------------------------------------------

sample_ratio = min(
    1.0,
    SAMPLE_SIZE / total_rows
)

print(
    f"\nSampling ratio: "
    f"{sample_ratio:.4f}"
)


# --------------------------------------------------
# Calculate expected samples per class
# --------------------------------------------------

target_samples = {}

for label in [0, 1]:

    target_samples[label] = min(
        class_counts[label],
        round(
            class_counts[label]
            * sample_ratio
        )
    )

print("\nTarget samples:")

print(
    f"BENIGN: "
    f"{target_samples[0]:,}"
)

print(
    f"ATTACK: "
    f"{target_samples[1]:,}"
)


# --------------------------------------------------
# PASS 2
# Randomly sample each chunk
# --------------------------------------------------

print("\nPASS 2: Creating sample...")

sample_parts = []

for chunk_number, chunk in enumerate(
    pd.read_csv(
        INPUT_PATH,
        chunksize=CHUNK_SIZE
    ),
    start=1
):

    for label in [0, 1]:

        class_chunk = chunk[
            chunk[TARGET] == label
        ]

        if len(class_chunk) == 0:
            continue

        # Proportional sample from this chunk
        n = round(
            len(class_chunk)
            * sample_ratio
        )

        n = min(
            n,
            len(class_chunk)
        )

        if n > 0:

            sampled = class_chunk.sample(
                n=n,
                random_state=(
                    RANDOM_STATE
                    + chunk_number
                    + label
                )
            )

            sample_parts.append(
                sampled
            )

    if chunk_number % 10 == 0:

        current_rows = sum(
            len(part)
            for part in sample_parts
        )

        print(
            f"Processed {chunk_number} chunks | "
            f"Sample rows: {current_rows:,}"
        )


# --------------------------------------------------
# Combine sampled chunks
# --------------------------------------------------

sample_df = pd.concat(
    sample_parts,
    ignore_index=True
)


# --------------------------------------------------
# Shuffle final sample
# --------------------------------------------------

sample_df = sample_df.sample(
    frac=1,
    random_state=RANDOM_STATE
).reset_index(drop=True)


# --------------------------------------------------
# Limit to requested size if necessary
# --------------------------------------------------

if len(sample_df) > SAMPLE_SIZE:

    sample_df = sample_df.sample(
        n=SAMPLE_SIZE,
        random_state=RANDOM_STATE
    ).reset_index(drop=True)


# --------------------------------------------------
# Save
# --------------------------------------------------

sample_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# Final information
# --------------------------------------------------

print("\n====================================")
print("Sampling complete!")
print("====================================")

print(
    f"Sample shape: {sample_df.shape}"
)

print(
    f"Saved to:\n{OUTPUT_PATH}"
)

print("\nClass distribution:")

print(
    sample_df[TARGET]
    .value_counts()
)

print("\nClass percentages:")

print(
    sample_df[TARGET]
    .value_counts(
        normalize=True
    ).mul(100).round(2)
)