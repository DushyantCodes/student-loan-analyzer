import joblib
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "loan_risk_model.pkl"
ENCODER_PATH = PROJECT_ROOT / "models" / "label_encoders.pkl"

# Load model and encoders once
model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODER_PATH)


def encode(column, value):
    """
    Encode a categorical value using the fitted LabelEncoder.
    """
    return encoders[column].transform([value])[0]


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
    Predict loan repayment risk.
    """

    data = pd.DataFrame([{
        "person_age": age,
        "person_gender": encode("person_gender", gender),
        "person_education": encode("person_education", education),
        "person_income": income,
        "person_emp_exp": employment_experience,
        "person_home_ownership": encode("person_home_ownership", home_ownership),
        "loan_amnt": loan_amount,
        "loan_intent": encode("loan_intent", loan_intent),
        "loan_int_rate": interest_rate,
        "loan_percent_income": loan_percent_income,
        "cb_person_cred_hist_length": credit_history_length,
        "credit_score": credit_score,
        "previous_loan_defaults_on_file": encode(
            "previous_loan_defaults_on_file",
            previous_default,
        ),
    }])

    prediction = model.predict(data)[0]
    probabilities = model.predict_proba(data)[0]

    confidence = round(max(probabilities) * 100, 2)

    risk = "🟢 Low Risk" if prediction == 0 else "🔴 High Risk"

    return risk, confidence