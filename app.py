import pandas as pd
import streamlit as st

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

# -----------------------------------------------------
# User Inputs
# -----------------------------------------------------

bank_rates = get_all_bank_rates()

loan_amount = st.number_input(
    "Loan Amount (₹)",
    min_value=10000,
    value=1000000,
    step=10000,
)

selected_bank = st.selectbox(
    "Select Bank",
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
    "Expected Starting Salary (LPA)",
    min_value=1.0,
    value=12.0,
    step=0.5,
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