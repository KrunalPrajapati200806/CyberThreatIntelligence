from pathlib import Path
import joblib


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "random_forest_multiclass.joblib"
)


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Multiclass model not found: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    return model


model = load_model()