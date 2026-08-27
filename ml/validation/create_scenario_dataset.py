from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "CIC-IDS2017"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "validation"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


CHUNK_SIZE = 50_000


# --------------------------------------------------
# Scenario mapping
# --------------------------------------------------

SCENARIOS = {

    "Monday": [
        "Monday-WorkingHours.pcap_ISCX.csv"
    ],

    "Tuesday": [
        "Tuesday-WorkingHours.pcap_ISCX.csv"
    ],

    "Wednesday": [
        "Wednesday-workingHours.pcap_ISCX.csv"
    ],

    "Thursday": [
        "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
        "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv"
    ],

    "Friday": [
        "Friday-WorkingHours-Morning.pcap_ISCX.csv",
        "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
        "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"
    ]
}


# --------------------------------------------------
# ML feature names
# --------------------------------------------------

ML_COLUMNS = [
    "Destination Port",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Fwd Packet Length Max",
    "Fwd Packet Length Min",
    "Fwd Packet Length Mean",
    "Fwd Packet Length Std",
    "Bwd Packet Length Max",
    "Bwd Packet Length Min",
    "Bwd Packet Length Mean",
    "Bwd Packet Length Std",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Flow IAT Mean",
    "Flow IAT Std",
    "Flow IAT Max",
    "Flow IAT Min",
    "Fwd IAT Total",
    "Fwd IAT Mean",
    "Fwd IAT Std",
    "Fwd IAT Max",
    "Fwd IAT Min",
    "Bwd IAT Total",
    "Bwd IAT Mean",
    "Bwd IAT Std",
    "Bwd IAT Max",
    "Bwd IAT Min",
    "Fwd PSH Flags",
    "Bwd PSH Flags",
    "Fwd URG Flags",
    "Bwd URG Flags",
    "Fwd Header Length",
    "Bwd Header Length",
    "Fwd Packets/s",
    "Bwd Packets/s",
    "Min Packet Length",
    "Max Packet Length",
    "Packet Length Mean",
    "Packet Length Std",
    "Packet Length Variance",
    "FIN Flag Count",
    "SYN Flag Count",
    "RST Flag Count",
    "PSH Flag Count",
    "ACK Flag Count",
    "URG Flag Count",
    "CWE Flag Count",
    "ECE Flag Count",
    "Down/Up Ratio",
    "Average Packet Size",
    "Avg Fwd Segment Size",
    "Avg Bwd Segment Size",
    "Fwd Header Length.1",
    "Fwd Avg Bytes/Bulk",
    "Fwd Avg Packets/Bulk",
    "Fwd Avg Bulk Rate",
    "Bwd Avg Bytes/Bulk",
    "Bwd Avg Packets/Bulk",
    "Bwd Avg Bulk Rate",
    "Subflow Fwd Packets",
    "Subflow Fwd Bytes",
    "Subflow Bwd Packets",
    "Subflow Bwd Bytes",
    "Init_Win_bytes_forward",
    "Init_Win_bytes_backward",
    "act_data_pkt_fwd",
    "min_seg_size_forward",
    "Active Mean",
    "Active Std",
    "Active Max",
    "Active Min",
    "Idle Mean",
    "Idle Std",
    "Idle Max",
    "Idle Min"
]


# --------------------------------------------------
# Function
# --------------------------------------------------

def process_scenario(
    scenario_name,
    filenames
):

    output_path = (
        OUTPUT_DIR
        / f"{scenario_name.lower()}_binary.csv"
    )

    print()
    print("=" * 70)
    print(
        f"Creating scenario: {scenario_name}"
    )
    print("=" * 70)

    first_write = True

    total_rows = 0
    benign_rows = 0
    attack_rows = 0

    for filename in filenames:

        file_path = RAW_DIR / filename

        print()
        print(
            f"Processing: {filename}"
        )

        for chunk_number, chunk in enumerate(
            pd.read_csv(
                file_path,
                chunksize=CHUNK_SIZE,
                low_memory=False
            ),
            start=1
        ):

            chunk.columns = (
                chunk.columns
                .str.strip()
            )

            # ------------------------------------------
            # Keep only ML columns + Label
            # ------------------------------------------

            required_columns = (
                ML_COLUMNS + ["Label"]
            )

            chunk = chunk[
                required_columns
            ]

            # ------------------------------------------
            # Clean labels
            # ------------------------------------------

            chunk["Label"] = (
                chunk["Label"]
                .astype(str)
                .str.strip()
            )

            # ------------------------------------------
            # Binary label
            # ------------------------------------------

            chunk["Attack"] = (
                chunk["Label"]
                .str.upper()
                .ne("BENIGN")
                .astype("int8")
            )

            # Remove original label
            chunk = chunk.drop(
                columns=["Label"]
            )

            # ------------------------------------------
            # Numeric conversion
            # ------------------------------------------

            for column in ML_COLUMNS:

                chunk[column] = pd.to_numeric(
                    chunk[column],
                    errors="coerce"
                )

            # ------------------------------------------
            # Remove invalid values
            # ------------------------------------------

            chunk = chunk.replace(
                [float("inf"), float("-inf")],
                pd.NA
            )

            chunk = chunk.dropna()

            # ------------------------------------------
            # Statistics
            # ------------------------------------------

            rows = len(chunk)

            attacks = int(
                chunk["Attack"].sum()
            )

            benign = rows - attacks

            total_rows += rows
            attack_rows += attacks
            benign_rows += benign

            # ------------------------------------------
            # Write incrementally
            # ------------------------------------------

            chunk.to_csv(
                output_path,
                mode="w" if first_write else "a",
                header=first_write,
                index=False
            )

            first_write = False

            if chunk_number % 10 == 0:

                print(
                    f"Processed {chunk_number} chunks | "
                    f"Rows: {total_rows:,}"
                )

    print()
    print(
        f"{scenario_name} complete."
    )

    print(
        f"Total rows: {total_rows:,}"
    )

    print(
        f"BENIGN: {benign_rows:,}"
    )

    print(
        f"ATTACK: {attack_rows:,}"
    )

    print(
        f"Saved: {output_path}"
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    for scenario_name, filenames in SCENARIOS.items():

        process_scenario(
            scenario_name,
            filenames
        )

    print()
    print("=" * 70)
    print("ALL SCENARIOS CREATED")
    print("=" * 70)