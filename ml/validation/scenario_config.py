from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "CIC-IDS2017"
)


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