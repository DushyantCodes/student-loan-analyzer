# Student Loan EMI Analyzer

Lightweight Streamlit app to compare education loan EMIs, estimate total interest and repayment, and predict repayment risk using a trained ML model.

Features
- EMI calculation and amortization helpers
- Bank comparison of monthly EMI and total repayment
- College selection (NIRF data) with median package and rank
- Salary burden indicator, affordability score, and ML-based repayment risk prediction

Prerequisites
- Python 3.10+ recommended
- Git

Quick install

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate     # Windows (PowerShell)
pip install -r requirements.txt
```

Run locally

```bash
streamlit run app.py
```

Deployment (Streamlit Community Cloud)
- Ensure repository contains any required small model files under `models/` and the essential CSVs in `data/`.
- If large raw datasets or trained models are not included, the app will fall back to safe defaults but predictions will be unavailable.
- From the Streamlit dashboard, connect your GitHub repo and deploy the main branch.

Notes for deployment
- `requirements.txt` contains the runtime dependencies. Streamlit Cloud uses it to build the environment.
- Avoid committing very large raw data and models; instead upload small models required for inference or host them externally and update the app to download them at startup.

Troubleshooting
- If the app shows "No colleges available", add `data/colleges.csv` (NIRF/processed sample) to the repo.
- If model predictions show as "Medium Risk" with 0.0% confidence, the ML model or encoders are missing; place `models/loan_risk_model.pkl` and `models/label_encoders.pkl` in the `models/` folder.

Maintainer
- Dushyant Jindal
