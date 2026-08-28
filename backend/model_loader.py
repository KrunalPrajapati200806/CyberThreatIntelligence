# from pathlib import Path
# import joblib


# MODEL_PATH = (
#     Path(__file__).resolve().parent.parent
#     / "models"
#     / "random_forest_multiclass.joblib"
# )


# def load_model():
#     if not MODEL_PATH.exists():
#         raise FileNotFoundError(
#             f"Multiclass model not found: {MODEL_PATH}"
#         )

#     model = joblib.load(MODEL_PATH)

#     return model


# model = load_model()







from pathlib import Path
import joblib


MODELS_DIR = (
    Path(__file__).resolve().parent.parent / "models"
)


MULTICLASS_MODEL_PATH = (
    MODELS_DIR / "random_forest_multiclass.joblib"
)

BINARY_MODEL_PATH = (
    MODELS_DIR / "random_forest_binary.joblib"
)


def load_model(path: Path):
    if not path.exists():
        raise FileNotFoundError(
            f"Model not found: {path}"
        )

    return joblib.load(path)


multiclass_model = load_model(MULTICLASS_MODEL_PATH)
binary_model = load_model(BINARY_MODEL_PATH)


# Backward compatibility
model = multiclass_model