# import re
# import pandas as pd

# from backend.feature_schema import FINAL_FEATURES


# def normalize_feature_name(name: str) -> str:

#     name = str(name).strip()

#     # Replace slash with _per_
#     name = name.replace("/s", "_per_s")
#     name = name.replace("/Up", "_per_Up")
#     name = name.replace("/", "_")

#     # Replace spaces with underscores
#     name = re.sub(r"\s+", "_", name)

#     # Remove problematic characters
#     name = re.sub(r"[^A-Za-z0-9_.]", "", name)

#     return name


# def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:

#     df = df.copy()

#     rename_map = {
#         column: normalize_feature_name(column)
#         for column in df.columns
#     }

#     df = df.rename(columns=rename_map)

#     return df


# def prepare_features(df: pd.DataFrame) -> pd.DataFrame:

#     df = normalize_dataframe(df)

#     missing = [
#         feature
#         for feature in FINAL_FEATURES
#         if feature not in df.columns
#     ]

#     if missing:
#         raise ValueError(
#             f"Missing required features after normalization: {missing}"
#         )

#     return df[FINAL_FEATURES]






import re
import pandas as pd

from backend.feature_schema import MULTICLASS_FEATURES, BINARY_FEATURES


def normalize_feature_name(name: str) -> str:
    name = str(name).strip()

    name = name.replace("/s", "_per_s")
    name = name.replace("/Up", "_per_Up")
    name = name.replace("/", "_")

    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^A-Za-z0-9_.]", "", name)

    return name


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    rename_map = {
        column: normalize_feature_name(column)
        for column in df.columns
    }

    return df.rename(columns=rename_map)


def prepare_features(
    df: pd.DataFrame,
    feature_set="multiclass"
) -> pd.DataFrame:

    df = normalize_dataframe(df)

    if feature_set == "binary":
        required_features = BINARY_FEATURES
    elif feature_set == "multiclass":
        required_features = MULTICLASS_FEATURES
    else:
        raise ValueError(
            f"Unknown feature_set: {feature_set}. "
            "Use 'binary' or 'multiclass'."
        )

    missing = [
        feature
        for feature in required_features
        if feature not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required features after normalization: {missing}"
        )

    return df[required_features]