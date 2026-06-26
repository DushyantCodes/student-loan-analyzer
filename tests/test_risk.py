from src.risk_predictor import predict_risk

risk, confidence = predict_risk(
    age=22,
    gender="Male",
    education="Bachelor",
    income=1200000,
    employment_experience=1,
    home_ownership="RENT",
    loan_amount=1000000,
    loan_intent="EDUCATION",
    interest_rate=8.3,
    loan_percent_income=0.12,
    credit_history_length=4,
    credit_score=720,
    previous_default="No",
)

print(risk)
print(confidence)