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
    show_amortization,
)
from src.college_lookup import get_college_names, get_college_details
from src.emi_calculator import (
    calculate_emi,
    calculate_salary_ratio,
    calculate_total_interest,
    calculate_total_payment,
    calculate_prepayment_savings,
)
from src.custom_style import inject_css

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="Student Loan EMI Analyzer",
    page_icon="🎓",
    layout="wide",
)

inject_css()
page_title()

# -------------------------------------------------------
# Sidebar
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
    st.caption(f"Interest Rate: **{interest_rate}%** p.a.")

    tenure = st.slider("Loan Tenure (Years)", 1, 20, 10)

    # ---- College ----
    st.header("🏫 College")

    college = st.selectbox("Select College", get_college_names())
    college_info = get_college_details(college)
    salary = college_info["salary"]

    if salary is not None:
        c1, c2 = st.columns(2)
        with c1:
            st.metric("🏆 Rank", college_info["rank"])
        with c2:
            st.metric("💼 Median Pkg", f"{salary:.1f} LPA")
        st.caption(f"📍 {college_info['location']}")
    else:
        st.warning("⚠️ Salary data unavailable for this college.")

    st.divider()

    # ---- Risk Inputs ----
    st.header("🤖 Risk Inputs")

    age = st.slider("Age", 18, 40, 22)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    education = st.selectbox(
        "Education",
        ["High School", "Associate", "Bachelor", "Master", "Doctorate"],
    )
    experience = st.slider("Work Experience (Years)", 0, 20, 1)
    credit_score = st.slider("Credit Score", 300, 900, 750)
    credit_history_length = st.slider("Credit History (Years)", 0, 30, 2)
    home_ownership = st.selectbox("Home Ownership", ["RENT", "OWN", "MORTGAGE", "OTHER"])
    loan_intent = st.selectbox(
        "Loan Purpose",
        ["EDUCATION", "PERSONAL", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"],
    )
    previous_default = st.selectbox("Previous Default", ["No", "Yes"])

    st.divider()

    calculate_clicked = st.button("🔍 Calculate EMI", use_container_width=True)

    if "results" in st.session_state:
        if st.button("🔄 Reset", use_container_width=True):
            del st.session_state.results
            st.rerun()

# -------------------------------------------------------
# Calculation
# -------------------------------------------------------

if calculate_clicked:
    if not validate_inputs(loan_amount, interest_rate, tenure, salary):
        st.stop()

    loan_warning(loan_amount, salary)

    try:
        with st.spinner("⚙️ Analyzing your loan profile..."):
            emi = calculate_emi(loan_amount, interest_rate, tenure)
            total_payment = calculate_total_payment(emi, tenure)
            total_interest = calculate_total_interest(total_payment, loan_amount)
            salary_ratio = calculate_salary_ratio(emi, salary)
            loan_percent_income = salary_ratio / 100
            annual_income_rupees = salary * 100_000

            risk, confidence = predict_risk(
                age=age,
                gender=gender.lower(),
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

            # Prepayment savings (extra ₹5000/month scenario)
            interest_saved, new_tenure = calculate_prepayment_savings(
                loan_amount, interest_rate, tenure, 5000
            )

            # Bank comparison
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
                "interest_saved": interest_saved,
                "new_tenure": new_tenure,
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
# Results
# -------------------------------------------------------

if "results" in st.session_state:
    r = st.session_state.results

    section()
    show_metrics(r["emi"], r["total_payment"], r["total_interest"], r["salary_ratio"])

    section()
    col_left, col_right = st.columns(2)
    with col_left:
        show_loan_summary(
            r["loan_amount"], r["selected_bank"], r["interest_rate"],
            r["tenure"], r["salary"], r["college"],
        )
    with col_right:
        show_pie_chart(r["loan_amount"], r["total_interest"])

    section()
    show_salary_risk(r["salary_ratio"])

    section()
    st.subheader("🤖 Loan Repayment Risk Prediction")

    risk_col1, risk_col2 = st.columns([1, 1])
    with risk_col1:
        if r["risk"] == "Low Risk":
            st.success(f"🟢 {r['risk']}")
            st.success("Your profile indicates a good chance of repaying the loan comfortably.")
        elif r["risk"] == "Medium Risk":
            st.warning(f"🟡 {r['risk']}")
            st.warning("Moderate risk. Consider lower loan amount or longer tenure.")
        else:
            st.error(f"🔴 {r['risk']}")
            st.error("High risk. Reduce loan amount or improve financial stability first.")

    with risk_col2:
        st.metric("Prediction Confidence", f"{r['confidence']:.1f}%")

        st.subheader("⭐ Affordability Score")
        score_col1, score_col2 = st.columns(2)
        with score_col1:
            st.metric("Score", f"{r['score']}/100")
            st.progress(r["score"] / 100)
        with score_col2:
            st.metric("Verdict", r["affordability_label"])

    section()

    # Prepayment tip
    st.subheader("💡 Prepayment Tip")
    orig_months = r["tenure"] * 12
    saved_months = orig_months - r["new_tenure"]
    st.info(
        f"Paying an extra **₹5,000/month** saves you **₹{r['interest_saved']:,.2f}** in interest "
        f"and closes your loan **{saved_months} months earlier** "
        f"({r['new_tenure']} months instead of {orig_months})."
    )

    section()
    show_bank_comparison(r["comparison_df"])

    section()
    show_amortization(r["loan_amount"], r["interest_rate"], r["tenure"])

else:
    st.info("👈 Fill in the loan details in the sidebar and click **Calculate EMI**.")

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.divider()
st.markdown("""
<div style="text-align:center;padding:1rem 0;color:#64748B;font-size:0.85rem;">
    🎓 <strong>Student Loan EMI Analyzer v1.0</strong> &nbsp;|&nbsp;
    Developed by <strong>Dushyant Jindal</strong> &nbsp;|&nbsp;
    LNMIIT Jaipur &nbsp;|&nbsp; © 2026
</div>
""", unsafe_allow_html=True)

st.info("""
**Disclaimer** — Median package values are sourced from publicly available college placement reports.
Salary figures are historical and do not guarantee future earnings.
Bank interest rates may change over time.
This tool is for educational and financial planning purposes only — not financial advice.
""")