# CyberIntel - Network Threat Intelligence & Attack Detection

> An AI-powered network security analytics platform for detecting and classifying network attacks using machine learning.

## Overview

**CyberIntel** is a full-stack cybersecurity analytics platform designed to analyze network traffic and identify malicious activity using a machine-learning-based network attack detection pipeline.

The platform combines a **React + Vite frontend** with a **FastAPI backend** and a trained **Random Forest multiclass classifier** developed using network-flow features from the **CIC-IDS2017 dataset**.

Users can upload network traffic datasets, automatically normalize network-flow feature names, run batch predictions, inspect attack distributions, analyze detection results, view prediction confidence, maintain detection history, and export generated reports.

The project is designed as an end-to-end demonstration of applying machine learning to practical network security analytics.

---

## Key Features

- Network traffic analysis
- Machine-learning-based network attack detection
- Binary threat identification: `BENIGN` vs `ATTACK`
- Multiclass attack classification
- 15-class threat classification
- Random Forest multiclass classifier
- 36-feature production inference schema
- Automatic feature-name normalization
- Batch network-flow prediction
- Prediction confidence scores
- Threat distribution analysis
- Interactive analytics dashboard
- Detection history
- Report generation and export
- CSV, TSV, XLS, XLSX and JSON input support
- REST API for model inference
- Backend health monitoring
- Model validation and evaluation
- Feature-selection experiments
- Reproducible ML training and validation scripts

---

## System Architecture

```text
                         ┌─────────────────────────┐
                         │      React + Vite       │
                         │       CyberIntel UI     │
                         └────────────┬────────────┘
                                      │
                                  REST API
                                      │
                         ┌────────────▼────────────┐
                         │         FastAPI         │
                         │         Backend         │
                         └────────────┬────────────┘
                                      │
                              Feature Processing
                                      │
                         ┌────────────▼────────────┐
                         │   Feature Normalizer    │
                         │      36 Features        │
                         └────────────┬────────────┘
                                      │
                         ┌────────────▼────────────┐
                         │     Random Forest       │
                         │   Multiclass Classifier │
                         └────────────┬────────────┘
                                      │
                         ┌────────────▼────────────┐
                         │    Threat Prediction    │
                         │       15 Classes        │
                         └─────────────────────────┘

Prediction Pipeline
Network Traffic File
        │
        ▼
CSV / TSV / XLS / XLSX / JSON
        │
        ▼
DataFrame
        │
        ▼
Feature Name Normalization
        │
        ▼
36 Production Features
        │
        ▼
Data Cleaning
        │
        ▼
Random Forest Model
        │
        ▼
Attack Classification
        │
        ├── BENIGN
        │
        └── ATTACK
              │
              ▼
       Specific Threat Type
              │
              ▼
       Confidence Score

       
Machine Learning Model

The production inference system uses a trained Random Forest multiclass classifier.

Production Model
Property	Value
Algorithm	Random Forest
Problem	Multiclass Network Attack Classification
Dataset	CIC-IDS2017
Production Features	36
Output Classes	15
Inference Format	Batch / Single Flow
Model Format	Joblib
Backend Framework	FastAPI

The production feature schema is defined in:

backend/feature_schema.py

The trained model is loaded by:

backend/model_loader.py

Predictions are handled by:

backend/predictor.py
Dataset

CyberIntel uses network-flow data derived from the CIC-IDS2017 intrusion detection dataset.

The project includes processed validation samples and evaluation artifacts, while large raw and processed datasets are intentionally excluded from version control.

Dataset Characteristics

The project uses network-flow characteristics such as:

Packet lengths
Flow timing
Forward and backward packet statistics
Header lengths
TCP flag counts
Inter-arrival times
Subflow statistics
Initial TCP window sizes
Destination port
Flow byte rate

The production inference pipeline reduces the input to 36 selected features.

Production Feature Schema

The current production model expects the following 36 features:

Bwd_Packet_Length_Std
Bwd_Packet_Length_Mean
Packet_Length_Variance
Average_Packet_Size
Total_Length_of_Bwd_Packets
Avg_Bwd_Segment_Size
Max_Packet_Length
Packet_Length_Mean
Packet_Length_Std
Bwd_Packet_Length_Max
Destination_Port
Subflow_Fwd_Packets
Total_Fwd_Packets
Total_Length_of_Fwd_Packets
Subflow_Bwd_Bytes
Subflow_Fwd_Bytes
min_seg_size_forward
Bwd_Header_Length
Fwd_Packet_Length_Max
act_data_pkt_fwd
Avg_Fwd_Segment_Size
Flow_IAT_Max
Fwd_Header_Length
Fwd_Header_Length.1
PSH_Flag_Count
Flow_IAT_Std
ACK_Flag_Count
Fwd_IAT_Min
Fwd_Packet_Length_Mean
Fwd_IAT_Std
Idle_Min
Init_Win_bytes_backward
Subflow_Bwd_Packets
Init_Win_bytes_forward
Fwd_IAT_Mean
Flow_Bytes_per_s
Backend

The backend is implemented using FastAPI.

Main API Endpoints
Health Check
GET /health

Returns the current API and model status.

Example response:

{
  "status": "healthy",
  "model": "random_forest_multiclass",
  "features": 36,
  "classes": 15
}
Single Flow Prediction
POST /predict

Accepts a JSON request containing the required network-flow features.

Example structure:

{
  "features": {
    "Bwd_Packet_Length_Std": 0.0,
    "Bwd_Packet_Length_Mean": 0.0,
    "Packet_Length_Variance": 0.0
  }
}

The complete request must contain the 36 production features.

Batch File Prediction
POST /predict-csv

Accepts uploaded network traffic data.

Supported formats:

CSV
TSV
XLS
XLSX
JSON

The endpoint:

Reads the uploaded file.
Converts it into a DataFrame.
Normalizes feature names.
Validates the required production features.
Cleans invalid numerical values.
Performs batch prediction.
Calculates attack statistics.
Generates threat-type distributions.
Returns detailed prediction results.
Example Batch Response
{
  "filename": "network_traffic.csv",
  "file_type": ".csv",
  "total_flows": 1000,
  "attacks": 120,
  "benign": 880,
  "attack_rate": 12.0,
  "attack_types": {
    "DoS Hulk": 60,
    "PortScan": 35,
    "DDoS": 25
  },
  "results": []
}
Frontend

The frontend is built using:

React
Vite
JavaScript
CSS

The interface provides a dashboard for interacting with the network threat detection system.

Frontend Modules
Dashboard
Traffic Analysis
Threat Detection
Analytics
Reports
History

Additional frontend functionality includes:

File upload
Prediction result visualization
Threat distribution visualization
Detection history
Report export
API communication
Result formatting
Project Structure
CyberThreatIntelligence/
│
├── backend/
│   ├── feature_normalizer.py
│   ├── feature_schema.py
│   ├── main.py
│   ├── model_loader.py
│   ├── predictor.py
│   └── train_multiclass.py
│
├── data/
│   └── validation/
│       ├── multiclass_test.csv
│       └── test_1000.csv
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       └── utils/
│
├── frontend_old/
│   ├── app.js
│   ├── index.html
│   └── style.css
│
├── ml/
│   ├── evaluation/
│   ├── preprocessing/
│   ├── training/
│   └── validation/
│
├── models/
│   └── [trained model artifacts]
│
├── notebooks/
│   ├── 01_dataset_inspection.ipynb
│   ├── 02_feature_audit.ipynb
│   ├── 03_build_ml_dataset.ipynb
│   └── 04_binary_baseline.ipynb
│
├── reports/
│   ├── baseline/
│   ├── feature_selection/
│   └── validation/
│
├── .gitignore
├── README.md
└── ...
Technology Stack
Machine Learning
Python
Pandas
NumPy
Scikit-learn
Joblib
Backend
FastAPI
Pydantic
Uvicorn
Frontend
React
Vite
JavaScript
CSS
Data Science
Jupyter Notebook
Feature engineering
Feature selection
Model evaluation
Network-flow analysis
Development Tools
Git
GitHub
VS Code
Python Virtual Environment
Installation
1. Clone the Repository
git clone https://github.com/KrunalPrajapati200806/CyberThreatIntelligence.git
cd CyberThreatIntelligence
2. Create a Virtual Environment

Windows PowerShell:

python -m venv .venv

Activate it:

.\.venv\Scripts\Activate.ps1
3. Install Backend Dependencies

If a requirements.txt file is available:

pip install -r requirements.txt

Otherwise install the required backend packages:

pip install fastapi uvicorn pandas numpy scikit-learn joblib python-multipart openpyxl
Running the Backend

From the project root:

uvicorn backend.main:app --reload

The API will normally be available at:

http://127.0.0.1:8000
API Documentation

FastAPI automatically provides interactive API documentation at:

http://127.0.0.1:8000/docs

Alternative documentation:

http://127.0.0.1:8000/redoc
Running the Frontend

Open a second terminal.

Navigate to the frontend:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will normally be available at:

http://localhost:5173

The frontend communicates with the FastAPI backend through the REST API.

Model Evaluation

The project contains scripts and reports for:

Binary classification
Multiclass classification
Random Forest evaluation
Feature importance analysis
Feature-selection experiments
Validation dataset generation
Unseen dataset evaluation

Evaluation artifacts are stored under:

reports/

ML scripts are organized under:

ml/
Validation

The repository includes small validation datasets suitable for testing the inference pipeline without requiring the complete CIC-IDS2017 dataset.

Example validation files:

data/validation/multiclass_test.csv
data/validation/test_1000.csv

Large validation datasets and raw/processed datasets are excluded from Git tracking to keep the repository lightweight.

Security and Repository Hygiene

The repository intentionally excludes:

.venv/
node_modules/
.env
data/raw/
data/processed/
models/*.joblib
models/*.pkl
large validation datasets
frontend/dist/
frontend/build/

This prevents large datasets, virtual environments, generated build files, and environment secrets from being committed to the repository.

Never commit API keys, passwords, credentials, tokens, or other secrets to GitHub.

Current Project Status
Completed
 CIC-IDS2017 data preprocessing
 Dataset inspection
 Feature auditing
 Binary classification experiments
 Random Forest training
 Feature-selection experiments
 Multiclass Random Forest model
 36-feature production schema
 FastAPI backend
 Batch prediction API
 Multi-format file input
 Feature normalization
 React + Vite frontend
 Threat detection dashboard
 Analytics
 Detection history
 Report/export functionality
 Backend health monitoring
 Git repository
 GitHub repository
Planned
 Automated backend tests
 Frontend testing
 Dockerized deployment
 Docker Compose configuration
 CI/CD with GitHub Actions
 Cloud deployment
 Public live demo
 Production monitoring
 Model versioning
Future Improvements

Potential future development includes:

Real-time network traffic ingestion
Streaming threat detection
Model explainability
Advanced anomaly detection
Threat intelligence feed integration
Automated alert generation
Network visualization
Model monitoring and drift detection
MLOps pipeline
Containerized production deployment
Cloud-based inference
Role-based access control
Limitations

CyberIntel is a machine-learning research and demonstration platform and should not be treated as a replacement for a production Security Information and Event Management (SIEM) or Intrusion Detection System (IDS).

Model performance depends on:

Input feature quality
Dataset distribution
Network environment
Feature compatibility
Similarity between production traffic and training data

The model should therefore be evaluated and retrained when deployed against substantially different network environments.

Disclaimer

This project is intended for educational, research, defensive cybersecurity, and network-security analytics purposes.

Only use the system on network traffic and systems for which you have appropriate authorization.

Author

Krunal Prajapati

Artificial Intelligence & Machine Learning

GitHub:

https://github.com/KrunalPrajapati200806

License

This project is currently provided for educational and research purposes.