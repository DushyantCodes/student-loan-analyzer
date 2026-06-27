import joblib
import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "loan_risk_model.pkl"
ENCODER_PATH = PROJECT_ROOT / "models" / "label_encoders.pkl"


def _safe_load(path):
    try:
        return joblib.load(path)
    except Exception:
        return None


@st.cache_resource
def _get_model():
    return _safe_load(MODEL_PATH)


@st.cache_resource
def _get_encoders():
    return _safe_load(ENCODER_PATH)


def _encode(encoders, column: str, value):
    """Encode a categorical value using the fitted LabelEncoder.

    If encoders are missing or encoding fails, returns a safe default (0).
    """
    if not encoders or column not in encoders:
        return 0

    try:
        return encoders[column].transform([value])[0]
    except Exception:
        return 0


def predict_risk(
    age,
    gender,
    education,
    income,
    employment_experience,
    home_ownership,
    loan_amount,
    loan_intent,
    interest_rate,
    loan_percent_income,
    credit_history_length,
    credit_score,
    previous_default,
) -> Tuple[str, float]:
    """Predict loan repayment risk.

    Returns a tuple of (risk_label, confidence_percent).
    If the model or encoders are not available, returns ("Medium Risk", 0.0)
    to avoid crashing the app.
    """

    model = _get_model()
    encoders = _get_encoders()

    if model is None or encoders is None:
        return "Medium Risk", 0.0

    data = pd.DataFrame([
        {
            "person_age": age,
            "person_gender": _encode(encoders, "person_gender", gender),
            "person_education": _encode(encoders, "person_education", education),
            "person_income": income,
            "person_emp_exp": employment_experience,
            "person_home_ownership": _encode(encoders, "person_home_ownership", home_ownership),
            "loan_amnt": loan_amount,
            "loan_intent": _encode(encoders, "loan_intent", loan_intent),
            "loan_int_rate": interest_rate,
            "loan_percent_income": loan_percent_income,
            "cb_person_cred_hist_length": credit_history_length,
            "credit_score": credit_score,
            "previous_loan_defaults_on_file": _encode(
                encoders,
                "previous_loan_defaults_on_file",
                previous_default,
            ),
        }
    ])

    try:
        prediction = model.predict(data)[0]
        probabilities = model.predict_proba(data)[0]
        confidence = round(max(probabilities) * 100, 2)
        risk = "Low Risk" if int(prediction) == 0 else "High Risk"
        return risk, confidence
    except Exception:
        return "Medium Risk", 0.0