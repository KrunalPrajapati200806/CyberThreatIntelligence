from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "validation"
    / "friday_binary.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "validation"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "unseen_friday_test.csv"
)


# ============================================================
# SETTINGS
# ============================================================

CHUNK_SIZE = 50_000

BENIGN_TARGET = 30_000
ATTACK_TARGET = 30_000

RANDOM_SEED = 42


# ============================================================
# PASS 1
# Count classes
# ============================================================

print("=" * 70)
print("PASS 1: COUNTING FRIDAY CLASSES")
print("=" * 70)

benign_count = 0
attack_count = 0

for chunk_number, chunk in enumerate(
    pd.read_csv(
        INPUT_FILE,
        chunksize=CHUNK_SIZE
    ),
    start=1
):

    benign_count += int(
        (chunk["Attack"] == 0).sum()
    )

    attack_count += int(
        (chunk["Attack"] == 1).sum()
    )

    if chunk_number % 10 == 0:

        print(
            f"Scanned {chunk_number} chunks..."
        )


print()
print("Complete counts:")
print(
    f"BENIGN: {benign_count:,}"
)
print(
    f"ATTACK: {attack_count:,}"
)


# ============================================================
# Validate targets
# ============================================================

if benign_count < BENIGN_TARGET:

    raise ValueError(
        "Not enough BENIGN rows."
    )


if attack_count < ATTACK_TARGET:

    raise ValueError(
        "Not enough ATTACK rows."
    )


# ============================================================
# PASS 2
# Reservoir sampling
# ============================================================

print()
print("=" * 70)
print("PASS 2: RAM-SAFE RESERVOIR SAMPLING")
print("=" * 70)

rng = np.random.default_rng(
    RANDOM_SEED
)


benign_reservoir = []
attack_reservoir = []


benign_seen = 0
attack_seen = 0


for chunk_number, chunk in enumerate(
    pd.read_csv(
        INPUT_FILE,
        chunksize=CHUNK_SIZE
    ),
    start=1
):

    # --------------------------------------------------------
    # BENIGN
    # --------------------------------------------------------

    benign_rows = chunk[
        chunk["Attack"] == 0
    ]

    for row in benign_rows.itertuples(
        index=False,
        name=None
    ):

        benign_seen += 1

        if len(benign_reservoir) < BENIGN_TARGET:

            benign_reservoir.append(row)

        else:

            position = rng.integers(
                0,
                benign_seen
            )

            if position < BENIGN_TARGET:

                benign_reservoir[position] = row


    # --------------------------------------------------------
    # ATTACK
    # --------------------------------------------------------

    attack_rows = chunk[
        chunk["Attack"] == 1
    ]

    for row in attack_rows.itertuples(
        index=False,
        name=None
    ):

        attack_seen += 1

        if len(attack_reservoir) < ATTACK_TARGET:

            attack_reservoir.append(row)

        else:

            position = rng.integers(
                0,
                attack_seen
            )

            if position < ATTACK_TARGET:

                attack_reservoir[position] = row


    if chunk_number % 10 == 0:

        print(
            f"Processed {chunk_number} chunks | "
            f"BENIGN sample: {len(benign_reservoir):,} | "
            f"ATTACK sample: {len(attack_reservoir):,}"
        )


# ============================================================
# Convert to DataFrames
# ============================================================

columns = pd.read_csv(
    INPUT_FILE,
    nrows=0
).columns.tolist()


benign_df = pd.DataFrame(
    benign_reservoir,
    columns=columns
)


attack_df = pd.DataFrame(
    attack_reservoir,
    columns=columns
)


# ============================================================
# Combine
# ============================================================

test_df = pd.concat(
    [
        benign_df,
        attack_df
    ],
    ignore_index=True
)


# Shuffle
test_df = test_df.sample(
    frac=1,
    random_state=RANDOM_SEED
).reset_index(
    drop=True
)


# ============================================================
# Save
# ============================================================

test_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# Results
# ============================================================

print()
print("=" * 70)
print("UNSEEN FRIDAY TEST SET CREATED")
print("=" * 70)

print(
    f"Shape: {test_df.shape}"
)

print()
print("Distribution:")

print(
    test_df["Attack"].value_counts()
)

print()
print("Percentages:")

print(
    test_df["Attack"]
    .value_counts(
        normalize=True
    )
    .mul(100)
)


print()
print(
    f"Saved to:\n{OUTPUT_FILE}"
)