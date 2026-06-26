import pandas as pd
import plotly.express as px
import streamlit as st


def show_metrics(emi, total_payment, total_interest, salary_ratio):
    """Display the four KPI cards."""

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💳 Monthly EMI",
            f"₹{emi:,.2f}"
        )

    with col2:
        st.metric(
            "💰 Interest Paid",
            f"₹{total_interest:,.2f}"
        )

    with col3:
        st.metric(
            "📈 Total Repayment",
            f"₹{total_payment:,.2f}"
        )

    with col4:
        st.metric(
            "📊 EMI / Salary",
            f"{salary_ratio:.2f}%"
        )


def show_salary_risk(ratio: float):
    """Display salary burden indicator."""

    st.subheader("Salary Burden")

    if ratio < 25:
        st.success("🟢 Low Risk")
    elif ratio < 40:
        st.warning("🟡 Medium Risk")
    else:
        st.error("🔴 High Risk")


def show_pie_chart(principal: float, interest: float):
    """Show principal vs interest chart."""

    df = pd.DataFrame(
        {
            "Type": ["Principal", "Interest"],
            "Amount": [principal, interest],
        }
    )

    fig = px.pie(
        df,
        names="Type",
        values="Amount",
        hole=0.55,
        color="Type",
        color_discrete_map={
            "Principal": "#4CAF50",
            "Interest": "#F44336",
        },
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


def show_loan_summary(
    loan_amount: float,
    bank: str,
    interest_rate: float,
    tenure: int,
    salary_lpa: float,
):
    """Display loan summary."""

    st.subheader("📋 Loan Summary")

    summary = pd.DataFrame(
        {
            "Field": [
                "Loan Amount",
                "Bank",
                "Interest Rate",
                "Tenure",
                "Expected Salary",
            ],
            "Value": [
                f"₹{loan_amount:,.0f}",
                bank,
                f"{interest_rate:.2f}%",
                f"{tenure} Years",
                f"{salary_lpa:.2f} LPA",
            ],
        }
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
    )


def show_bank_comparison(df: pd.DataFrame):
    """Display comparison table."""

    st.subheader("🏦 Bank Comparison")

    cheapest = df["Monthly EMI (₹)"].idxmin()

    styled = (
        df.style
        .highlight_min(
            subset=["Monthly EMI (₹)"],
            color="#90EE90",
        )
    )

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
    )

    st.success(
        f"✅ Recommended Bank: {df.iloc[cheapest]['Bank']}"
    )


def section():
    st.divider()


def page_title():
    st.title("🎓 Student Loan EMI Analyzer")

    st.caption(
        "Education Loan Intelligence Platform"
    )
