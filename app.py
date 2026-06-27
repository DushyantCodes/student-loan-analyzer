import pandas as pd
import streamlit as st
from src.risk_predictor import predict_risk
from src.affordability import calculate_affordability_score
from src.validators import validate_inputs, loan_warning
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
from src.college_lookup import get_college_names, get_college_details
from src.emi_calculator import (
    calculate_emi,
    calculate_salary_ratio,
    calculate_total_interest,
    calculate_total_payment,
)

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="Student Loan EMI Analyzer",
    page_icon="🎓",
    layout="wide",
)

page_title()
st.caption(
    "Compare education loan EMIs, analyze repayment burden, "
    "and predict repayment risk using Machine Learning."
)

# -------------------------------------------------------
# Sidebar — all user inputs + Calculate button
# -------------------------------------------------------

bank_rates = get_all_bank_rates()

with st.sidebar:

    st.header("🎓 Loan Details")

    loan_amount = st.number_input(
        "Loan Amount (₹)",
        min_value=10000,
        value=1000000,
        step=10000,
    )

    selected_bank = st.selectbox("Bank", list(bank_rates.keys()))
    interest_rate = bank_rates[selected_bank]

    tenure = st.slider("Loan Tenure (Years)", 1, 20, 10)

    # ---- College ----
    st.header("🏫 College")

    college = st.selectbox("Select College", get_college_names())
    college_info = get_college_details(college)

    # salary is LPA (e.g. 17.3 means ₹17.3 lakhs per annum)
    salary = college_info["salary"]

    if salary is not None:
        st.success(f"🎓 {college}")
        sidebar_col1, sidebar_col2 = st.columns(2)
        with sidebar_col1:
            st.metric("🏆 Rank", college_info["rank"])
        with sidebar_col2:
            st.metric("💼 Median Package", f"{salary:.2f} LPA")
        st.caption(f"📍 {college_info['location']}")
    else:
        st.warning("⚠️ Salary data unavailable for this college.")

    st.divider()

    # ---- Risk Inputs ----
    st.header("🤖 Risk Prediction")

    age = st.slider("Age", 18, 40, 22)

    # Encoder knows only 'female' and 'male' — Other maps to default
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    education = st.selectbox(
        "Education",
        ["High School", "Associate", "Bachelor", "Master", "Doctorate"],
    )

    experience = st.slider("Employment Experience (Years)", 0, 20, 1)

    credit_score = st.slider("Credit Score", 300, 900, 750)

    credit_history_length = st.slider("Credit History Length (Years)", 0, 30, 2)

    home_ownership = st.selectbox(
        "Home Ownership", ["RENT", "OWN", "MORTGAGE", "OTHER"]
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

    previous_default = st.selectbox("Previous Default", ["No", "Yes"])

    st.divider()
    calculate_clicked = st.button("Calculate EMI", use_container_width=True)

# -------------------------------------------------------
# Calculation — runs on button click, stores in session_state
# -------------------------------------------------------

if calculate_clicked:
    if not validate_inputs(loan_amount, interest_rate, tenure, salary):
        st.stop()

    loan_warning(loan_amount, salary)

    try:
        emi = calculate_emi(loan_amount, interest_rate, tenure)
        total_payment = calculate_total_payment(emi, tenure)
        total_interest = calculate_total_interest(total_payment, loan_amount)

        # salary_ratio: percentage (e.g. 35.0 = 35%)
        salary_ratio = calculate_salary_ratio(emi, salary)

        # model expects a ratio 0.0–1.0
        loan_percent_income = salary_ratio / 100

        # model expects annual income in rupees (salary is LPA)
        annual_income_rupees = salary * 100_000

        risk, confidence = predict_risk(
            age=age,
            gender=gender.lower(),        # encoder knows 'male'/'female'
            education=education,
            income=annual_income_rupees,
            employment_experience=experience,
            home_ownership=home_ownership,
            loan_amount=loan_amount,
            loan_intent=loan_intent,
            interest_rate=interest_rate,
            loan_percent_income=loan_percent_income,
            credit_history_length=credit_history_length,
            credit_score=credit_score,
            previous_default=previous_default,
        )

        score, affordability_label = calculate_affordability_score(salary, emi, risk)

        # Build bank comparison table
        comparison = []
        for bank, rate in bank_rates.items():
            b_emi = calculate_emi(loan_amount, rate, tenure)
            b_total = calculate_total_payment(b_emi, tenure)
            b_interest = calculate_total_interest(b_total, loan_amount)
            comparison.append({
                "Bank": bank,
                "Interest Rate (%)": rate,
                "Monthly EMI (₹)": b_emi,
                "Interest Paid (₹)": b_interest,
                "Total Repayment (₹)": b_total,
            })

        # Persist everything — survives all Streamlit reruns
        st.session_state.results = {
            "emi": emi,
            "total_payment": total_payment,
            "total_interest": total_interest,
            "salary_ratio": salary_ratio,
            "risk": risk,
            "confidence": confidence,
            "score": score,
            "affordability_label": affordability_label,
            "comparison_df": pd.DataFrame(comparison),
            "loan_amount": loan_amount,
            "selected_bank": selected_bank,
            "interest_rate": interest_rate,
            "tenure": tenure,
            "salary": salary,
            "college": college,
        }

    except Exception as e:
        st.error(f"Calculation failed: {e}")
        st.stop()

# -------------------------------------------------------
# Results — rendered from session_state so they persist
# -------------------------------------------------------

if "results" in st.session_state:
    r = st.session_state.results

    section()
    show_metrics(r["emi"], r["total_payment"], r["total_interest"], r["salary_ratio"])

    section()
    show_loan_summary(
        r["loan_amount"],
        r["selected_bank"],
        r["interest_rate"],
        r["tenure"],
        r["salary"],
        r["college"],
    )

    section()
    show_pie_chart(r["loan_amount"], r["total_interest"])

    section()
    show_salary_risk(r["salary_ratio"])

    st.divider()
    st.subheader("🤖 Loan Repayment Risk Prediction")

    if r["risk"] == "Low Risk":
        st.success(f"🟢 {r['risk']}")
        st.success("Your profile indicates a good chance of repaying the loan comfortably.")
    elif r["risk"] == "Medium Risk":
        st.warning(f"🟡 {r['risk']}")
        st.warning(
            "Your repayment ability is moderate. "
            "Consider a lower loan amount or a longer tenure."
        )
    else:
        st.error(f"🔴 {r['risk']}")
        st.error(
            "High repayment risk. Consider reducing the loan amount or "
            "improving financial stability before borrowing."
        )

    st.metric("Prediction Confidence", f"{r['confidence']:.1f}%")

    st.subheader("⭐ Loan Affordability Score")
    score_col1, score_col2 = st.columns(2)
    with score_col1:
        st.metric("Score", f"{r['score']}/100")
        st.progress(r["score"] / 100)
    with score_col2:
        st.metric("Recommendation", r["affordability_label"])

    section()
    show_bank_comparison(r["comparison_df"])
    st.success("✅ Loan analysis completed successfully.")

else:
    st.info("👈 Fill the loan details in the sidebar and click **Calculate EMI**.")

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.divider()
st.caption(
    """
🎓 Student Loan EMI Analyzer v1.0
Developed by Dushyant Jindal | LNMIIT Jaipur | © 2026
"""
)
st.info(
    """
**Disclaimer**

• Median package values are sourced from publicly available college placement reports.
• Salary figures are historical and do not guarantee future earnings.
• Bank interest rates may change over time.
• This tool is intended for educational and financial planning purposes only \
and should not be treated as financial advice.
"""
)