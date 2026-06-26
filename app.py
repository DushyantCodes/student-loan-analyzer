import pandas as pd
import streamlit as st
from src.risk_predictor import predict_risk
from src.bank_rates import get_all_bank_rates
from src.dashboard import (
    page_title,
    section,
    show_bank_comparison,
    show_loan_summary,
    show_metrics,
    show_pie_chart,
    show_salary_risk,
)
from src.emi_calculator import (
    calculate_emi,
    calculate_salary_ratio,
    calculate_total_interest,
    calculate_total_payment,
)

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="Student Loan EMI Analyzer",
    page_icon="🎓",
    layout="wide",
)

page_title()
st.caption(
    "Compare education loan EMIs, analyze repayment burden, and predict repayment risk using Machine Learning."
)
# -----------------------------------------------------
# User Inputs
# -----------------------------------------------------

bank_rates = get_all_bank_rates()

with st.sidebar:

    st.header("🎓 Loan Details")

    loan_amount = st.number_input(
        "Loan Amount (₹)",
        min_value=10000,
        value=1000000,
        step=10000,
    )

    selected_bank = st.selectbox(
        "Bank",
        list(bank_rates.keys()),
    )

    interest_rate = bank_rates[selected_bank]

    tenure = st.slider(
        "Loan Tenure (Years)",
        1,
        20,
        10,
    )

    salary = st.number_input(
        "Expected Salary (LPA)",
        min_value=1.0,
        value=12.0,
        step=0.5,
    )

    st.header("🤖 Risk Prediction")

    age = st.slider(
        "Age",
        18,
        40,
        22,
    )

    education = st.selectbox(
        "Education",
        [
            "High School",
            "Associate",
            "Bachelor",
            "Master",
            "Doctorate",
        ],
    )

    experience = st.slider(
        "Employment Experience",
        0,
        20,
        1,
    )

    credit_score = st.slider(
        "Credit Score",
        300,
        900,
        750,
    )

    home_ownership = st.selectbox(
        "Home Ownership",
        [
            "RENT",
            "OWN",
            "MORTGAGE",
            "OTHER",
        ],
    )

    loan_intent = st.selectbox(
        "Loan Purpose",
        [
            "EDUCATION",
            "PERSONAL",
            "MEDICAL",
            "VENTURE",
            "HOMEIMPROVEMENT",
            "DEBTCONSOLIDATION",
        ],
    )

    previous_default = st.selectbox(
        "Previous Default",
        [
            "No",
            "Yes",
        ],
    )

# -----------------------------------------------------
# Calculate
# -----------------------------------------------------

if st.button("Calculate EMI"):

    emi = calculate_emi(
        loan_amount,
        interest_rate,
        tenure,
    )

    total_payment = calculate_total_payment(
        emi,
        tenure,
    )

    total_interest = calculate_total_interest(
        total_payment,
        loan_amount,
    )

    salary_ratio = calculate_salary_ratio(
        emi,
        salary,
    )

    section()

    show_metrics(
        emi,
        total_payment,
        total_interest,
        salary_ratio,
    )

    section()

    show_loan_summary(
        loan_amount,
        selected_bank,
        interest_rate,
        tenure,
        salary,
    )

    section()

    show_pie_chart(
        loan_amount,
        total_interest,
    )

    section()

    show_salary_risk(
        salary_ratio,
    )

    risk, confidence = predict_risk(
        age=age,
        gender="male",
        education=education,
        income=salary * 100000,
        employment_experience=experience,
        home_ownership=home_ownership,
        loan_amount=loan_amount,
        loan_intent=loan_intent,
        interest_rate=interest_rate,
        loan_percent_income=salary_ratio / 100,
        credit_history_length=2,
        credit_score=credit_score,
        previous_default=previous_default,
    )

    st.divider()

    st.subheader("🤖 Loan Repayment Risk Prediction")

    if risk == "Low Risk":
        st.success(f"🟢 {risk}")
        st.info(
            "Your profile indicates a good chance of repaying the loan comfortably."
        )
    elif risk == "Medium Risk":
        st.warning(f"🟡 {risk}")
        st.warning(
            "Your repayment ability is moderate. Consider a lower loan amount or longer tenure."
        )
    else:
        st.error(f"🔴 {risk}")
        st.error(
            "High repayment risk. Consider reducing the loan amount or improving financial stability before borrowing."
        )

    st.metric(
        "Prediction Confidence",
        f"{confidence:.1f}%"
    )

    section()

    comparison = []

    for bank, rate in bank_rates.items():

        bank_emi = calculate_emi(
            loan_amount,
            rate,
            tenure,
        )

        repayment = calculate_total_payment(
            bank_emi,
            tenure,
        )

        interest = calculate_total_interest(
            repayment,
            loan_amount,
        )

        comparison.append(
            {
                "Bank": bank,
                "Interest Rate (%)": rate,
                "Monthly EMI (₹)": bank_emi,
                "Interest Paid (₹)": interest,
                "Total Repayment (₹)": repayment,
            }
        )

    comparison_df = pd.DataFrame(comparison)

    show_bank_comparison(comparison_df)

