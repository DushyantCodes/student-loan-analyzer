import streamlit as st
import pandas as pd
from src.bank_rates import get_all_bank_rates
from src.emi_calculator import (
    calculate_emi,
    calculate_total_interest,
    calculate_total_payment,
    calculate_salary_ratio,
)

st.set_page_config(
    page_title="Student Loan EMI Analyzer",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Student Loan EMI Analyzer")
st.write("Calculate your education loan EMI and repayment details.")

bank_rates = get_all_bank_rates()

loan_amount = st.number_input(
    "Loan Amount (₹)",
    min_value=10000,
    value=1000000,
    step=10000,
)

selected_bank = st.selectbox(
    "Select Bank",
    list(bank_rates.keys())
)

interest_rate = bank_rates[selected_bank]

tenure = st.slider(
    "Loan Tenure (Years)",
    min_value=1,
    max_value=20,
    value=10,
)

salary = st.number_input(
    "Expected Starting Salary (LPA)",
    min_value=1.0,
    value=12.0,
    step=0.5,
)

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

    ratio = calculate_salary_ratio(
        emi,
        salary,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Monthly EMI",
            f"₹{emi:,.2f}"
        )

        st.metric(
            "Total Repayment",
            f"₹{total_payment:,.2f}"
        )

    with col2:
        st.metric(
            "Interest Paid",
            f"₹{total_interest:,.2f}"
        )

        st.metric(
            "EMI / Monthly Salary",
            f"{ratio}%"
        )

comparison_data = []

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

    comparison_data.append(
        {
            "Bank": bank,
            "Interest Rate (%)": rate,
            "Monthly EMI (₹)": round(bank_emi, 2),
            "Interest Paid (₹)": round(interest, 2),
            "Total Repayment (₹)": round(repayment, 2),
        }
    )

comparison_df = pd.DataFrame(comparison_data)

st.divider()

st.subheader("🏦 Bank Comparison")

st.dataframe(
    comparison_df,
    use_container_width=True,
)

