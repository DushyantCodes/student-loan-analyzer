import joblib
import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "loan_risk_model.pkl"

# Load model only once
model = joblib.load(MODEL_PATH)


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
):
    """
    Predict repayment risk using the trained ML model.
    """

    gender_map = {
        "Male": 1,
        "Female": 0,
    }

    education_map = {
        "High School": 0,
        "Bachelor": 1,
        "Master": 2,
        "Doctorate": 3,
    }

    home_map = {
        "RENT": 0,
        "MORTGAGE": 1,
        "OWN": 2,
        "OTHER": 3,
    }

    intent_map = {
        "EDUCATION": 0,
        "MEDICAL": 1,
        "VENTURE": 2,
        "PERSONAL": 3,
        "HOMEIMPROVEMENT": 4,
        "DEBTCONSOLIDATION": 5,
    }

    previous_map = {
        "No": 0,
        "Yes": 1,
    }

    data = pd.DataFrame([{
        "person_age": age,
        "person_gender": gender_map[gender],
        "person_education": education_map[education],
        "person_income": income,
        "person_emp_exp": employment_experience,
        "person_home_ownership": home_map[home_ownership],
        "loan_amnt": loan_amount,
        "loan_intent": intent_map[loan_intent],
        "loan_int_rate": interest_rate,
        "loan_percent_income": loan_percent_income,
        "cb_person_cred_hist_length": credit_history_length,
        "credit_score": credit_score,
        "previous_loan_defaults_on_file": previous_map[previous_default],
    }])

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0]

    confidence = max(probability) * 100

    if prediction == 0:
        risk = "🟢 Low Risk"
    else:
        risk = "🔴 High Risk"

    return risk, round(confidence, 2)