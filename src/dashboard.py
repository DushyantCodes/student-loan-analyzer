import pandas as pd
import plotly.express as px
import streamlit as st
from typing import Any


def _fmt_currency(amount: float) -> str:
    return f"₹{amount:,.2f}"


def _fmt_lpa(amount: float) -> str:
    return f"{amount:.2f} LPA"


def show_metrics(
    emi: float, total_payment: float, total_interest: float, salary_ratio: float
) -> None:
    """Display the four KPI cards."""

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💳 Monthly EMI", _fmt_currency(emi))

    with col2:
        st.metric("💰 Interest Paid", _fmt_currency(total_interest))

    with col3:
        st.metric("📈 Total Repayment", _fmt_currency(total_payment))

    with col4:
        st.metric("📊 EMI / Salary", f"{salary_ratio:.2f}%")


def show_salary_risk(ratio: float) -> None:
    """Display salary burden indicator."""

    st.subheader("Salary Burden")

    if ratio < 25:
        st.success("🟢 Low Risk")
    elif ratio < 40:
        st.warning("🟡 Medium Risk")
    else:
        st.error("🔴 High Risk")


def show_pie_chart(principal: float, interest: float) -> None:
    """Show principal vs interest chart."""

    df = pd.DataFrame({"Type": ["Principal", "Interest"], "Amount": [principal, interest]})

    fig = px.pie(
        df,
        names="Type",
        values="Amount",
        hole=0.55,
        color="Type",
        color_discrete_map={"Principal": "#4CAF50", "Interest": "#F44336"},
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")

    st.plotly_chart(fig, use_container_width=True)


def show_loan_summary(
    loan_amount: float,
    bank: str,
    interest_rate: float,
    tenure: int,
    salary_lpa: float,
    college: str,
) -> None:
    """Display loan summary."""

    st.subheader("📋 Loan Summary")

    summary = pd.DataFrame(
        {
            "Field": ["College", "Loan Amount", "Bank", "Interest Rate", "Tenure", "Expected Salary"],
            "Value": [
                college,
                _fmt_currency(loan_amount),
                bank,
                f"{interest_rate:.2f}%",
                f"{tenure} Years",
                _fmt_lpa(salary_lpa),
            ],
        }
    )

    st.dataframe(summary, use_container_width=True, hide_index=True)


def show_bank_comparison(df: pd.DataFrame) -> None:
    """Display comparison table."""

    st.subheader("🏦 Bank Comparison")

    cheapest = df["Monthly EMI (₹)"].idxmin()

    styled = df.style.highlight_min(subset=["Monthly EMI (₹)"], color="#90EE90")

    st.dataframe(styled, use_container_width=True, hide_index=True)

    st.success(f"✅ Recommended Bank: {df.iloc[cheapest]['Bank']}")


def section() -> None:
    st.divider()


def page_title() -> None:
    st.title("🎓 Student Loan EMI Analyzer")

    st.caption("Education Loan Intelligence Platform")
