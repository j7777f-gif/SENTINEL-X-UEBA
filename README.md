# SENTINEL-X-UEBA
## User and Entity Behavior Analytics

A Python pipeline for SSH log behavioral analysis, anomaly detection, and risk scoring.

## Pipeline
1. Feature extraction: event counts, unique event types, failed authentication, invalid users, and failure rates.
2. Anomaly detection: StandardScaler and Isolation Forest.
3. Dynamic risk scoring: weighted score from 0 to 100, categorized as Low, Medium, or High.

## Project Files
- src/feature_baseline.py
- src/isolation_forest.py
- src/dynamic_risk_scoring.py
- requirements.txt

## Installation
Create a virtual environment and install dependencies:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Usage
Run the scripts in pipeline order. Pass the relevant input file path as an argument.
Review the configured output paths in each script before running.

## Notes
Anomaly flags indicate behavior for investigation; they do not prove malicious activity.

## Security
Do not upload raw authentication logs, sensitive datasets, credentials, or tokens.
Analyze only logs you are authorized to access.

For educational purposes and authorized security analysis.
