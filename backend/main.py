# from pathlib import Path
# from io import BytesIO
# import json


# from fastapi import FastAPI, HTTPException, UploadFile, File
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse

# from fastapi.middleware.cors import CORSMiddleware

# from pydantic import BaseModel

# from typing import Dict

# import pandas as pd
# import numpy as np

# from backend.predictor import predict_attack, predict_batch
# from backend.feature_normalizer import prepare_features


# # ==========================================================
# # APPLICATION
# # ==========================================================

# app = FastAPI(
#     title="Cyber Threat Intelligence API",
#     description="Network attack detection using Random Forest",
#     version="1.0.0"
# )


# # ==========================================================
# # FRONTEND
# # ==========================================================

# FRONTEND_DIR = (
#     Path(__file__).resolve().parent.parent / "frontend" / "dist"
# )


# # ==========================================================
# # CORS
# # ==========================================================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "http://127.0.0.1:5173",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ==========================================================
# # REQUEST MODEL
# # ==========================================================

# class PredictionRequest(BaseModel):

#     features: Dict[str, float]


# # ==========================================================
# # ROOT
# # ==========================================================

# @app.get("/")
# def root():

#     return FileResponse(
#         FRONTEND_DIR / "index.html"
#     )


# # ==========================================================
# # HEALTH
# # ==========================================================

# @app.get("/health")
# def health():

#     return {
#         "status": "healthy",
#         "model": "random_forest_multiclass",
#         "features": 36,
#         "classes": 15
#     }


# # ==========================================================
# # SINGLE FLOW PREDICTION
# # ==========================================================

# @app.post("/predict")
# def predict(request: PredictionRequest):

#     try:

#         clean_features = {}

#         for key, value in request.features.items():

#             value = float(value)

#             if not np.isfinite(value):
#                 value = 0.0

#             clean_features[key] = value

#         return predict_attack(
#             clean_features
#         )

#     except ValueError as e:

#         raise HTTPException(
#             status_code=400,
#             detail=str(e)
#         )

#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )


# # ==========================================================
# # READ UPLOADED FILE
# # ==========================================================

# async def read_uploaded_file(
#     file: UploadFile
# ):

#     filename = (
#         file.filename or ""
#     ).lower()

#     extension = Path(
#         filename
#     ).suffix.lower()


#     # ------------------------------------------------------
#     # CSV
#     # ------------------------------------------------------

#     if extension == ".csv":

#         return pd.read_csv(
#             file.file
#         )


#     # ------------------------------------------------------
#     # TSV
#     # ------------------------------------------------------

#     if extension == ".tsv":

#         return pd.read_csv(
#             file.file,
#             sep="\t"
#         )


#     # ------------------------------------------------------
#     # EXCEL
#     # ------------------------------------------------------

#     if extension in [".xlsx", ".xls"]:

#         content = await file.read()

#         return pd.read_excel(
#             BytesIO(content)
#         )


#     # ------------------------------------------------------
#     # JSON
#     # ------------------------------------------------------

#     if extension == ".json":

#         content = await file.read()

#         try:

#             data = json.loads(
#                 content.decode("utf-8")
#             )

#         except Exception:

#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid JSON file."
#             )

#         if isinstance(data, list):

#             return pd.DataFrame(data)

#         if isinstance(data, dict):

#             return pd.DataFrame(data)


#         raise HTTPException(
#             status_code=400,
#             detail="Unsupported JSON structure."
#         )


#     # ------------------------------------------------------
#     # UNSUPPORTED
#     # ------------------------------------------------------

#     raise HTTPException(
#         status_code=400,
#         detail=(
#             "Unsupported file format. "
#             "Supported formats: "
#             "CSV, TSV, XLS, XLSX, JSON."
#         )
#     )


# # ==========================================================
# # MULTI-FORMAT NETWORK TRAFFIC ANALYSIS
# # ==========================================================

# @app.post("/predict-csv")
# async def predict_csv(
#     file: UploadFile = File(...)
# ):

#     try:

#         # --------------------------------------------------
#         # Validate filename
#         # --------------------------------------------------

#         if not file.filename:

#             raise HTTPException(
#                 status_code=400,
#                 detail="Filename is missing."
#             )


#         # --------------------------------------------------
#         # Read file
#         # --------------------------------------------------

#         df = await read_uploaded_file(
#             file
#         )


#         # --------------------------------------------------
#         # Validate dataframe
#         # --------------------------------------------------

#         if df.empty:

#             raise HTTPException(
#                 status_code=400,
#                 detail="The uploaded file is empty."
#             )


#         # --------------------------------------------------
#         # Prepare features
#         # --------------------------------------------------

#         X = prepare_features(
#             df
#         )


#         # --------------------------------------------------
#         # Clean invalid values
#         # --------------------------------------------------

#         X = X.replace(
#             [np.inf, -np.inf],
#             np.nan
#         )

#         X = X.fillna(0)

#         X = X.clip(
#             lower=-1e30,
#             upper=1e30
#         )


#         # --------------------------------------------------
#         # Batch prediction
#         # --------------------------------------------------

#         predictions = predict_batch(
#             X
#         )


#         # --------------------------------------------------
#         # Statistics
#         # --------------------------------------------------

#         total_flows = len(
#             predictions
#         )

#         attacks = sum(
#             result["is_attack"]
#             for result in predictions
#         )

#         benign = (
#             total_flows - attacks
#         )


#         attack_rate = (

#             attacks /
#             total_flows *
#             100

#             if total_flows > 0

#             else 0
#         )


#         # --------------------------------------------------
#         # Attack type distribution
#         # --------------------------------------------------

#         attack_types = {}


#         for result in predictions:

#             threat_type = (
#                 result["threat_type"]
#             )

#             if threat_type != "BENIGN":

#                 attack_types[
#                     threat_type
#                 ] = (

#                     attack_types.get(
#                         threat_type,
#                         0
#                     ) + 1

#                 )


#         attack_types = dict(
#             sorted(
#                 attack_types.items(),
#                 key=lambda item: item[1],
#                 reverse=True
#             )
#         )


#         # --------------------------------------------------
#         # Detailed results
#         # --------------------------------------------------

#         results = []


#         for index, prediction in enumerate(
#             predictions
#         ):

#             results.append({

#                 "flow": index + 1,

#                 "prediction":
#                     prediction["prediction"],

#                 "label":
#                     prediction["label"],

#                 "threat_type":
#                     prediction["threat_type"],

#                 "confidence":
#                     prediction["probability"]

#             })


#         # --------------------------------------------------
#         # Response
#         # --------------------------------------------------

#         return {

#             "filename":
#                 file.filename,

#             "file_type":
#                 Path(
#                     file.filename
#                 ).suffix.lower(),

#             "total_flows":
#                 total_flows,

#             "attacks":
#                 attacks,

#             "benign":
#                 benign,

#             "attack_rate":
#                 round(
#                     attack_rate,
#                     4
#                 ),

#             "attack_types":
#                 attack_types,

#             "results":
#                 results

#         }


#     except HTTPException:

#         raise


#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )


# # ==========================================================
# # FRONTEND STATIC FILES
# # ==========================================================

# app.mount(
#     "/",
#     StaticFiles(
#         directory=FRONTEND_DIR,
#         html=True
#     ),
#     name="frontend"
# )








































# from pathlib import Path
# from io import BytesIO
# import json
# import time

# from fastapi import FastAPI, HTTPException, UploadFile, File
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Dict

# import pandas as pd
# import numpy as np

# from backend.predictor import (
#     predict_attack,
#     predict_batch,
#     get_model_config,
# )
# from backend.feature_normalizer import prepare_features


# # ==========================================================
# # APPLICATION
# # ==========================================================

# app = FastAPI(
#     title="Cyber Threat Intelligence API",
#     description="Network attack detection using Random Forest",
#     version="1.0.0"
# )

# @app.middleware("http")
# async def log_requests(request, call_next):
#     start_time = time.time()

#     print(
#         f"REQUEST START: {request.method} {request.url.path}",
#         flush=True
#     )

#     try:
#         response = await call_next(request)

#         elapsed = time.time() - start_time

#         print(
#             f"REQUEST END: {request.method} {request.url.path} "
#             f"STATUS={response.status_code} "
#             f"TIME={elapsed:.2f}s",
#             flush=True
#         )

#         return response

#     except Exception as e:

#         elapsed = time.time() - start_time

#         print(
#             f"REQUEST ERROR: {request.method} {request.url.path} "
#             f"TIME={elapsed:.2f}s ERROR={repr(e)}",
#             flush=True
#         )

#         raise

# # ==========================================================
# # FRONTEND
# # ==========================================================

# FRONTEND_DIR = (
#     Path(__file__).resolve().parent.parent / "frontend" / "dist"
# )


# # ==========================================================
# # CORS
# # ==========================================================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "http://127.0.0.1:5173",
#         "https://cyberthreatintellige   nce-frontend.onrender.com",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ==========================================================
# # REQUEST MODEL
# # ==========================================================

# class PredictionRequest(BaseModel):
#     features: Dict[str, float]


# # ==========================================================
# # ROOT
# # ==========================================================

# @app.get("/")
# def root():

#     index_file = FRONTEND_DIR / "index.html"

#     if not index_file.exists():
#         raise HTTPException(
#             status_code=503,
#             detail="Frontend build not found."
#         )

#     return FileResponse(index_file)


# # ==========================================================
# # HEALTH
# # ==========================================================

# @app.get("/health")
# def health():

#     multiclass_config = get_model_config("multiclass")
#     binary_config = get_model_config("binary")

#     return {
#         "status": "healthy",
#         "models": {
#             "multiclass": {
#                 "name": "random_forest_multiclass",
#                 "features": len(multiclass_config["features"]),
#                 "classes": len(
#                     multiclass_config["model"].classes_
#                 ),
#             },
#             "binary": {
#                 "name": "random_forest_binary",
#                 "features": len(binary_config["features"]),
#                 "classes": len(
#                     binary_config["model"].classes_
#                 ),
#             },
#         },
#     }


# # ==========================================================
# # SINGLE FLOW PREDICTION
# # ==========================================================

# @app.post("/predict")
# def predict(
#     request: PredictionRequest,
#     model_type: str = "multiclass"
# ):

#     try:

#         if model_type not in ["binary", "multiclass"]:
#             raise HTTPException(
#                 status_code=400,
#                 detail=(
#                     "Invalid model_type. "
#                     "Use 'binary' or 'multiclass'."
#                 )
#             )

#         clean_features = {}

#         for key, value in request.features.items():

#             value = float(value)

#             if not np.isfinite(value):
#                 value = 0.0

#             clean_features[key] = value

#         return predict_attack(
#             clean_features,
#             model_type
#         )

#     except HTTPException:
#         raise

#     except ValueError as e:

#         raise HTTPException(
#             status_code=400,
#             detail=str(e)
#         )

#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )


# # ==========================================================
# # READ UPLOADED FILE
# # ==========================================================

# async def read_uploaded_file(
#     file: UploadFile
# ):

#     filename = (
#         file.filename or ""
#     ).lower()

#     extension = Path(
#         filename
#     ).suffix.lower()


#     # ------------------------------------------------------
#     # CSV
#     # ------------------------------------------------------

#     if extension == ".csv":

#         return pd.read_csv(
#             file.file
#         )


#     # ------------------------------------------------------
#     # TSV
#     # ------------------------------------------------------

#     if extension == ".tsv":

#         return pd.read_csv(
#             file.file,
#             sep="\t"
#         )


#     # ------------------------------------------------------
#     # EXCEL
#     # ------------------------------------------------------

#     if extension in [".xlsx", ".xls"]:

#         content = await file.read()

#         return pd.read_excel(
#             BytesIO(content)
#         )


#     # ------------------------------------------------------
#     # JSON
#     # ------------------------------------------------------

#     if extension == ".json":

#         content = await file.read()

#         try:

#             data = json.loads(
#                 content.decode("utf-8")
#             )

#         except Exception:

#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid JSON file."
#             )

#         if isinstance(data, list):

#             return pd.DataFrame(data)

#         if isinstance(data, dict):

#             return pd.DataFrame(data)

#         raise HTTPException(
#             status_code=400,
#             detail="Unsupported JSON structure."
#         )


#     # ------------------------------------------------------
#     # UNSUPPORTED
#     # ------------------------------------------------------

#     raise HTTPException(
#         status_code=400,
#         detail=(
#             "Unsupported file format. "
#             "Supported formats: "
#             "CSV, TSV, XLS, XLSX, JSON."
#         )
#     )


# # ==========================================================
# # MULTI-FORMAT NETWORK TRAFFIC ANALYSIS
# # ==========================================================

# @app.post("/predict-csv")
# async def predict_csv(
#     file: UploadFile = File(...),
#     model_type: str = "multiclass"
# ):

#     try:

#         # --------------------------------------------------
#         # Validate model
#         # --------------------------------------------------

#         if model_type not in ["binary", "multiclass"]:
#             raise HTTPException(
#                 status_code=400,
#                 detail=(
#                     "Invalid model_type. "
#                     "Use 'binary' or 'multiclass'."
#                 )
#             )


#         # --------------------------------------------------
#         # Validate filename
#         # --------------------------------------------------

#         if not file.filename:

#             raise HTTPException(
#                 status_code=400,
#                 detail="Filename is missing."
#             )


#         # --------------------------------------------------
#         # Read file
#         # --------------------------------------------------

#         df = await read_uploaded_file(
#             file
#         )


#         # --------------------------------------------------
#         # Validate dataframe
#         # --------------------------------------------------

#         if df.empty:

#             raise HTTPException(
#                 status_code=400,
#                 detail="The uploaded file is empty."
#             )


#         # --------------------------------------------------
#         # Prepare features
#         # --------------------------------------------------

#         X = prepare_features(
#             df,
#             model_type
#         )


#         # --------------------------------------------------
#         # Clean invalid values
#         # --------------------------------------------------

#         X = X.replace(
#             [np.inf, -np.inf],
#             np.nan
#         )

#         X = X.fillna(0)

#         X = X.clip(
#             lower=-1e30,
#             upper=1e30
#         )


#         # --------------------------------------------------
#         # Batch prediction
#         # --------------------------------------------------

#         predictions = predict_batch(
#             X,
#             model_type
#         )


#         # --------------------------------------------------
#         # Statistics
#         # --------------------------------------------------

#         total_flows = len(
#             predictions
#         )

#         attacks = sum(
#             result["is_attack"]
#             for result in predictions
#         )

#         benign = (
#             total_flows - attacks
#         )

#         attack_rate = (

#             attacks /
#             total_flows *
#             100

#             if total_flows > 0

#             else 0
#         )


#         # --------------------------------------------------
#         # Attack type distribution
#         # --------------------------------------------------

#         attack_types = {}

#         for result in predictions:

#             threat_type = (
#                 result["threat_type"]
#             )

#             if threat_type != "BENIGN":

#                 attack_types[
#                     threat_type
#                 ] = (

#                     attack_types.get(
#                         threat_type,
#                         0
#                     ) + 1

#                 )


#         attack_types = dict(
#             sorted(
#                 attack_types.items(),
#                 key=lambda item: item[1],
#                 reverse=True
#             )
#         )


#         # --------------------------------------------------
#         # Detailed results
#         # --------------------------------------------------

#         results = []

#         for index, prediction in enumerate(
#             predictions
#         ):

#             results.append({

#                 "flow": index + 1,

#                 "prediction":
#                     prediction["prediction"],

#                 "label":
#                     prediction["label"],

#                 "threat_type":
#                     prediction["threat_type"],

#                 "confidence":
#                     prediction["probability"]

#             })


#         # --------------------------------------------------
#         # Response
#         # --------------------------------------------------

#         return {

#             "filename":
#                 file.filename,

#             "file_type":
#                 Path(
#                     file.filename
#                 ).suffix.lower(),

#             "model_type":
#                 model_type,

#             "total_flows":
#                 total_flows,

#             "attacks":
#                 attacks,

#             "benign":
#                 benign,

#             "attack_rate":
#                 round(
#                     attack_rate,
#                     4
#                 ),

#             "attack_types":
#                 attack_types,

#             "results":
#                 results

#         }


#     except HTTPException:

#         raise


#     except ValueError as e:

#         raise HTTPException(
#             status_code=400,
#             detail=str(e)
#         )


#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )


# # ==========================================================
# # FRONTEND STATIC FILES
# # ==========================================================

# if FRONTEND_DIR.exists():

#     app.mount(
#         "/",
#         StaticFiles(
#             directory=FRONTEND_DIR,
#             html=True
#         ),
#         name="frontend"
#     )



































from pathlib import Path
from io import BytesIO
import json
import time

from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

import pandas as pd
import numpy as np

from backend.predictor import (
    predict_attack,
    predict_batch,
    get_model_config,
)
from backend.feature_normalizer import prepare_features


# ==========================================================
# CONFIGURATION
# ==========================================================

# Number of CSV rows processed at one time.
#
# Smaller chunks use less RAM.
# Larger chunks may be faster but require more RAM.
CSV_CHUNK_SIZE = 5000

# Do not create an enormous JSON response for very large files.
#
# The API will still analyze ALL rows.
# Only the first MAX_DETAIL_RESULTS rows are returned
# in the detailed "results" array.
MAX_DETAIL_RESULTS = 10000


# ==========================================================
# APPLICATION
# ==========================================================

app = FastAPI(
    title="Cyber Threat Intelligence API",
    description="Network attack detection using Random Forest",
    version="1.0.0"
)


# ==========================================================
# REQUEST LOGGING / TIMING
# ==========================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.perf_counter()

    print(
        f"[REQUEST START] "
        f"{request.method} {request.url.path}",
        flush=True
    )

    try:

        response = await call_next(request)

        elapsed = time.perf_counter() - start_time

        print(
            f"[REQUEST END] "
            f"{request.method} {request.url.path} "
            f"-> {response.status_code} "
            f"({elapsed:.2f}s)",
            flush=True
        )

        return response

    except Exception as e:

        elapsed = time.perf_counter() - start_time

        print(
            f"[REQUEST ERROR] "
            f"{request.method} {request.url.path} "
            f"after {elapsed:.2f}s: {e}",
            flush=True
        )

        raise


# ==========================================================
# FRONTEND
# ==========================================================

FRONTEND_DIR = (
    Path(__file__).resolve().parent.parent / "frontend" / "dist"
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://cyberthreatintelligence-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# REQUEST MODEL
# ==========================================================

class PredictionRequest(BaseModel):
    features: Dict[str, float]


# ==========================================================
# ROOT
# ==========================================================

@app.get("/")
def root():

    index_file = FRONTEND_DIR / "index.html"

    if not index_file.exists():

        raise HTTPException(
            status_code=503,
            detail="Frontend build not found."
        )

    return FileResponse(index_file)


# ==========================================================
# HEALTH
# ==========================================================

@app.get("/health")
def health():

    multiclass_config = get_model_config("multiclass")
    binary_config = get_model_config("binary")

    return {
        "status": "healthy",
        "models": {

            "multiclass": {
                "name": "random_forest_multiclass",
                "features": len(
                    multiclass_config["features"]
                ),
                "classes": len(
                    multiclass_config["model"].classes_
                ),
            },

            "binary": {
                "name": "random_forest_binary",
                "features": len(
                    binary_config["features"]
                ),
                "classes": len(
                    binary_config["model"].classes_
                ),
            },

        },
    }


# ==========================================================
# SINGLE FLOW PREDICTION
# ==========================================================

@app.post("/predict")
def predict(
    request: PredictionRequest,
    model_type: str = "multiclass"
):

    try:

        if model_type not in [
            "binary",
            "multiclass"
        ]:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid model_type. "
                    "Use 'binary' or 'multiclass'."
                )
            )

        clean_features = {}

        for key, value in request.features.items():

            value = float(value)

            if not np.isfinite(value):

                value = 0.0

            clean_features[key] = value

        return predict_attack(
            clean_features,
            model_type
        )

    except HTTPException:

        raise

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# READ NON-CSV UPLOADED FILE
# ==========================================================

async def read_uploaded_file(
    file: UploadFile
):

    filename = (
        file.filename or ""
    ).lower()

    extension = Path(
        filename
    ).suffix.lower()


    # ------------------------------------------------------
    # TSV
    # ------------------------------------------------------

    if extension == ".tsv":

        return pd.read_csv(
            file.file,
            sep="\t"
        )


    # ------------------------------------------------------
    # EXCEL
    # ------------------------------------------------------

    if extension in [".xlsx", ".xls"]:

        content = await file.read()

        return pd.read_excel(
            BytesIO(content)
        )


    # ------------------------------------------------------
    # JSON
    # ------------------------------------------------------

    if extension == ".json":

        content = await file.read()

        try:

            data = json.loads(
                content.decode("utf-8")
            )

        except Exception:

            raise HTTPException(
                status_code=400,
                detail="Invalid JSON file."
            )

        if isinstance(data, list):

            return pd.DataFrame(data)

        if isinstance(data, dict):

            return pd.DataFrame(data)

        raise HTTPException(
            status_code=400,
            detail="Unsupported JSON structure."
        )


    # ------------------------------------------------------
    # UNSUPPORTED
    # ------------------------------------------------------

    raise HTTPException(
        status_code=400,
        detail=(
            "Unsupported file format. "
            "Supported formats: "
            "CSV, TSV, XLS, XLSX, JSON."
        )
    )


# ==========================================================
# PREPARE + PREDICT ONE DATAFRAME CHUNK
# ==========================================================

def process_prediction_chunk(
    df: pd.DataFrame,
    model_type: str
):

    if df.empty:

        return []

    # ------------------------------------------------------
    # Prepare features
    # ------------------------------------------------------

    X = prepare_features(
        df,
        model_type
    )

    # ------------------------------------------------------
    # Clean invalid values
    # ------------------------------------------------------

    X = X.replace(
        [np.inf, -np.inf],
        np.nan
    )

    X = X.fillna(0)

    X = X.clip(
        lower=-1e30,
        upper=1e30
    )

    # ------------------------------------------------------
    # Batch prediction
    # ------------------------------------------------------

    predictions = predict_batch(
        X,
        model_type
    )

    return predictions


# ==========================================================
# CONVERT PREDICTIONS TO SUMMARY
# ==========================================================

def update_prediction_summary(
    predictions,
    total_flows,
    attacks,
    benign,
    attack_types,
    detailed_results,
):

    for prediction in predictions:

        total_flows += 1

        is_attack = bool(
            prediction["is_attack"]
        )

        if is_attack:

            attacks += 1

        else:

            benign += 1

        threat_type = (
            prediction["threat_type"]
        )

        if threat_type != "BENIGN":

            attack_types[threat_type] = (
                attack_types.get(
                    threat_type,
                    0
                ) + 1
            )

        # --------------------------------------------------
        # Only keep a limited number of detailed results.
        #
        # IMPORTANT:
        # The model still predicts ALL rows.
        # We only limit the response size.
        # --------------------------------------------------

        if len(detailed_results) < MAX_DETAIL_RESULTS:

            detailed_results.append({

                "flow": total_flows,

                "prediction":
                    prediction["prediction"],

                "label":
                    prediction["label"],

                "threat_type":
                    prediction["threat_type"],

                "confidence":
                    prediction["probability"]

            })

    return (
        total_flows,
        attacks,
        benign,
    )


# ==========================================================
# CSV PREDICTION
# ==========================================================

@app.post("/predict-csv")
async def predict_csv(
    file: UploadFile = File(...),
    model_type: str = "multiclass"
):

    request_start = time.perf_counter()

    print(
        "[PREDICT-CSV] Endpoint started",
        flush=True
    )

    try:

        # ==================================================
        # Validate model
        # ==================================================

        if model_type not in [
            "binary",
            "multiclass"
        ]:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid model_type. "
                    "Use 'binary' or 'multiclass'."
                )
            )


        # ==================================================
        # Validate filename
        # ==================================================

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="Filename is missing."
            )


        filename = file.filename

        extension = (
            Path(filename)
            .suffix
            .lower()
        )

        print(
            f"[PREDICT-CSV] "
            f"File: {filename}",
            flush=True
        )

        print(
            f"[PREDICT-CSV] "
            f"Model: {model_type}",
            flush=True
        )


        # ==================================================
        # Statistics
        # ==================================================

        total_flows = 0

        attacks = 0

        benign = 0

        attack_types = {}

        detailed_results = []


        # ==================================================
        # CSV
        # ==================================================

        if extension == ".csv":

            print(
                f"[PREDICT-CSV] "
                f"Processing CSV in chunks "
                f"of {CSV_CHUNK_SIZE} rows",
                flush=True
            )

            chunk_number = 0

            csv_start = time.perf_counter()

            try:

                chunks = pd.read_csv(
                    file.file,
                    chunksize=CSV_CHUNK_SIZE
                )

                for df_chunk in chunks:

                    chunk_number += 1

                    chunk_start = time.perf_counter()

                    print(
                        f"[PREDICT-CSV] "
                        f"Starting chunk "
                        f"{chunk_number} "
                        f"({len(df_chunk)} rows)",
                        flush=True
                    )

                    predictions = (
                        process_prediction_chunk(
                            df_chunk,
                            model_type
                        )
                    )

                    (
                        total_flows,
                        attacks,
                        benign,
                    ) = update_prediction_summary(
                        predictions,
                        total_flows,
                        attacks,
                        benign,
                        attack_types,
                        detailed_results,
                    )

                    chunk_elapsed = (
                        time.perf_counter()
                        - chunk_start
                    )

                    print(
                        f"[PREDICT-CSV] "
                        f"Chunk {chunk_number} "
                        f"completed: "
                        f"{len(df_chunk)} rows "
                        f"in {chunk_elapsed:.2f}s",
                        flush=True
                    )

                    # Explicitly release references.
                    del predictions
                    del df_chunk

            except pd.errors.EmptyDataError:

                raise HTTPException(
                    status_code=400,
                    detail="The uploaded CSV file is empty."
                )

            csv_elapsed = (
                time.perf_counter()
                - csv_start
            )

            print(
                f"[PREDICT-CSV] "
                f"CSV processing completed: "
                f"{total_flows} rows "
                f"in {csv_elapsed:.2f}s",
                flush=True
            )


        # ==================================================
        # TSV
        # ==================================================

        elif extension == ".tsv":

            print(
                "[PREDICT-CSV] "
                "Processing TSV file",
                flush=True
            )

            df = await read_uploaded_file(
                file
            )

            if df.empty:

                raise HTTPException(
                    status_code=400,
                    detail="The uploaded file is empty."
                )

            predictions = (
                process_prediction_chunk(
                    df,
                    model_type
                )
            )

            (
                total_flows,
                attacks,
                benign,
            ) = update_prediction_summary(
                predictions,
                total_flows,
                attacks,
                benign,
                attack_types,
                detailed_results,
            )

            del predictions
            del df


        # ==================================================
        # EXCEL / JSON
        # ==================================================

        elif extension in [
            ".xlsx",
            ".xls",
            ".json"
        ]:

            print(
                f"[PREDICT-CSV] "
                f"Processing {extension} file",
                flush=True
            )

            df = await read_uploaded_file(
                file
            )

            if df.empty:

                raise HTTPException(
                    status_code=400,
                    detail="The uploaded file is empty."
                )

            predictions = (
                process_prediction_chunk(
                    df,
                    model_type
                )
            )

            (
                total_flows,
                attacks,
                benign,
            ) = update_prediction_summary(
                predictions,
                total_flows,
                attacks,
                benign,
                attack_types,
                detailed_results,
            )

            del predictions
            del df


        # ==================================================
        # Unsupported
        # ==================================================

        else:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported file format. "
                    "Supported formats: "
                    "CSV, TSV, XLS, XLSX, JSON."
                )
            )


        # ==================================================
        # Validate result
        # ==================================================

        if total_flows == 0:

            raise HTTPException(
                status_code=400,
                detail="The uploaded file contains no valid rows."
            )


        # ==================================================
        # Attack rate
        # ==================================================

        attack_rate = (

            attacks /
            total_flows *
            100

            if total_flows > 0

            else 0
        )


        # ==================================================
        # Attack type distribution
        # ==================================================

        attack_types = dict(
            sorted(
                attack_types.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )


        # ==================================================
        # Response
        # ==================================================

        total_elapsed = (
            time.perf_counter()
            - request_start
        )

        results_truncated = (
            total_flows > MAX_DETAIL_RESULTS
        )

        print(
            f"[PREDICT-CSV] "
            f"FINISHED: "
            f"{total_flows} flows, "
            f"{attacks} attacks, "
            f"{benign} benign, "
            f"{total_elapsed:.2f}s",
            flush=True
        )

        print(
            f"[PREDICT-CSV] "
            f"Detailed results returned: "
            f"{len(detailed_results)} "
            f"(limit={MAX_DETAIL_RESULTS})",
            flush=True
        )


        return {

            "filename":
                filename,

            "file_type":
                extension,

            "model_type":
                model_type,

            "total_flows":
                total_flows,

            "attacks":
                attacks,

            "benign":
                benign,

            "attack_rate":
                round(
                    attack_rate,
                    4
                ),

            "attack_types":
                attack_types,

            "results":
                detailed_results,

            "results_returned":
                len(detailed_results),

            "results_truncated":
                results_truncated,

            "processing_time_seconds":
                round(
                    total_elapsed,
                    2
                )

        }


    # ======================================================
    # HTTP ERROR
    # ======================================================

    except HTTPException:

        raise


    # ======================================================
    # VALUE ERROR
    # ======================================================

    except ValueError as e:

        print(
            f"[PREDICT-CSV] "
            f"ValueError: {e}",
            flush=True
        )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


    # ======================================================
    # UNEXPECTED ERROR
    # ======================================================

    except Exception as e:

        print(
            f"[PREDICT-CSV] "
            f"Unexpected error: {type(e).__name__}: {e}",
            flush=True
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# FRONTEND STATIC FILES
# ==========================================================

if FRONTEND_DIR.exists():

    app.mount(
        "/",
        StaticFiles(
            directory=FRONTEND_DIR,
            html=True
        ),
        name="frontend"
    )