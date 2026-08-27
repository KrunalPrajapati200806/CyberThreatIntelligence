from pathlib import Path
from io import BytesIO
import json


from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from typing import Dict

import pandas as pd
import numpy as np

from backend.predictor import predict_attack, predict_batch
from backend.feature_normalizer import prepare_features


# ==========================================================
# APPLICATION
# ==========================================================

app = FastAPI(
    title="Cyber Threat Intelligence API",
    description="Network attack detection using Random Forest",
    version="1.0.0"
)


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

    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


# ==========================================================
# HEALTH
# ==========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model": "random_forest_multiclass",
        "features": 36,
        "classes": 15
    }


# ==========================================================
# SINGLE FLOW PREDICTION
# ==========================================================

@app.post("/predict")
def predict(request: PredictionRequest):

    try:

        clean_features = {}

        for key, value in request.features.items():

            value = float(value)

            if not np.isfinite(value):
                value = 0.0

            clean_features[key] = value

        return predict_attack(
            clean_features
        )

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
# READ UPLOADED FILE
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
    # CSV
    # ------------------------------------------------------

    if extension == ".csv":

        return pd.read_csv(
            file.file
        )


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
# MULTI-FORMAT NETWORK TRAFFIC ANALYSIS
# ==========================================================

@app.post("/predict-csv")
async def predict_csv(
    file: UploadFile = File(...)
):

    try:

        # --------------------------------------------------
        # Validate filename
        # --------------------------------------------------

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="Filename is missing."
            )


        # --------------------------------------------------
        # Read file
        # --------------------------------------------------

        df = await read_uploaded_file(
            file
        )


        # --------------------------------------------------
        # Validate dataframe
        # --------------------------------------------------

        if df.empty:

            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )


        # --------------------------------------------------
        # Prepare features
        # --------------------------------------------------

        X = prepare_features(
            df
        )


        # --------------------------------------------------
        # Clean invalid values
        # --------------------------------------------------

        X = X.replace(
            [np.inf, -np.inf],
            np.nan
        )

        X = X.fillna(0)

        X = X.clip(
            lower=-1e30,
            upper=1e30
        )


        # --------------------------------------------------
        # Batch prediction
        # --------------------------------------------------

        predictions = predict_batch(
            X
        )


        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        total_flows = len(
            predictions
        )

        attacks = sum(
            result["is_attack"]
            for result in predictions
        )

        benign = (
            total_flows - attacks
        )


        attack_rate = (

            attacks /
            total_flows *
            100

            if total_flows > 0

            else 0
        )


        # --------------------------------------------------
        # Attack type distribution
        # --------------------------------------------------

        attack_types = {}


        for result in predictions:

            threat_type = (
                result["threat_type"]
            )

            if threat_type != "BENIGN":

                attack_types[
                    threat_type
                ] = (

                    attack_types.get(
                        threat_type,
                        0
                    ) + 1

                )


        attack_types = dict(
            sorted(
                attack_types.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )


        # --------------------------------------------------
        # Detailed results
        # --------------------------------------------------

        results = []


        for index, prediction in enumerate(
            predictions
        ):

            results.append({

                "flow": index + 1,

                "prediction":
                    prediction["prediction"],

                "label":
                    prediction["label"],

                "threat_type":
                    prediction["threat_type"],

                "confidence":
                    prediction["probability"]

            })


        # --------------------------------------------------
        # Response
        # --------------------------------------------------

        return {

            "filename":
                file.filename,

            "file_type":
                Path(
                    file.filename
                ).suffix.lower(),

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
                results

        }


    except HTTPException:

        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# FRONTEND STATIC FILES
# ==========================================================

app.mount(
    "/",
    StaticFiles(
        directory=FRONTEND_DIR,
        html=True
    ),
    name="frontend"
)
