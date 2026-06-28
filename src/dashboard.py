import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def _fmt_currency(amount: float) -> str:
    return f"₹{amount:,.2f}"


def _fmt_lpa(amount: float) -> str:
    return f"{amount:.2f} LPA"


def show_metrics(
    emi: float, total_payment: float, total_interest: float, salary_ratio: float
) -> None:
    """Display four KPI cards."""
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
    """
    Display EMI-to-salary burden with context.
    Renamed label to avoid duplication with Risk Prediction section.
    """
    st.subheader("📊 EMI Affordability Indicator")

    col1, col2 = st.columns([1, 2])

    with col1:
        if ratio < 25:
            st.success("🟢 Comfortable")
            verdict = "Your EMI is well within safe limits."
        elif ratio < 40:
            st.warning("🟡 Moderate")
            verdict = "EMI is manageable but leaves less room for savings."
        else:
            st.error("🔴 High Burden")
            verdict = "EMI is high relative to salary. Consider longer tenure or lower loan."

    with col2:
        st.caption(verdict)
        # Visual gauge bar
        color = "#10B981" if ratio < 25 else "#F59E0B" if ratio < 40 else "#EF4444"
        st.markdown(f"""
        <div style="background:#E2E8F0;border-radius:99px;height:12px;margin-top:8px;">
            <div style="width:{min(ratio, 100):.1f}%;background:{color};
                        height:12px;border-radius:99px;transition:width 0.5s ease;">
            </div>
        </div>
        <p style="color:#64748B;font-size:0.75rem;margin-top:4px;">
            {ratio:.1f}% of monthly salary goes toward EMI
            &nbsp;|&nbsp; Safe zone: &lt;25%
        </p>
        """, unsafe_allow_html=True)


def show_pie_chart(principal: float, interest: float) -> None:
    """Donut chart — transparent background, light theme friendly."""
    df = pd.DataFrame({
        "Type": ["Principal", "Interest"],
        "Amount": [principal, interest]
    })

    fig = px.pie(
        df,
        names="Type",
        values="Amount",
        hole=0.55,
        color="Type",
        color_discrete_map={"Principal": "#4F46E5", "Interest": "#F59E0B"},
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(size=13, color="white"),
        marker=dict(line=dict(color="white", width=2)),
    )

    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#1E293B", family="Inter"),
        legend=dict(
            font=dict(color="#1E293B", size=13),
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(t=20, b=20, l=20, r=20),
        annotations=[dict(
            text=f"<b>₹{(principal+interest)/100000:.1f}L</b><br>Total",
            x=0.5, y=0.5,
            font=dict(size=14, color="#1E293B"),
            showarrow=False,
        )],
    )

    st.subheader("🥧 Loan Breakdown")
    st.plotly_chart(fig, use_container_width=True)


def show_loan_summary(
    loan_amount: float,
    bank: str,
    interest_rate: float,
    tenure: int,
    salary_lpa: float,
    college: str,
) -> None:
    """Display loan summary as styled HTML table — no dark dataframe."""
    st.subheader("📋 Loan Summary")

    rows = [
        ("🏫 College", college),
        ("💰 Loan Amount", _fmt_currency(loan_amount)),
        ("🏦 Bank", bank),
        ("📈 Interest Rate", f"{interest_rate:.2f}%"),
        ("📅 Tenure", f"{tenure} Years"),
        ("💼 Expected Salary", _fmt_lpa(salary_lpa)),
    ]

    html = """
    <style>
    .summary-table {width:100%;border-collapse:collapse;font-family:Inter,sans-serif;}
    .summary-table td {padding:10px 16px;border-bottom:1px solid #E2E8F0;font-size:0.9rem;}
    .summary-table tr:last-child td {border-bottom:none;}
    .summary-table td:first-child {color:#64748B;font-weight:500;width:35%;}
    .summary-table td:last-child {color:#1E293B;font-weight:600;}
    .summary-table tr:hover td {background:#F8FAFF;}
    </style>
    <table class="summary-table">
    """
    for field, value in rows:
        html += f"<tr><td>{field}</td><td>{value}</td></tr>"
    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)


def show_bank_comparison(df: pd.DataFrame) -> None:
    """
    Bank comparison with formatted currency columns.
    Fixes raw float display (20420.270000 → ₹20,420.27).
    """
    st.subheader("🏦 Bank Comparison")

    cheapest_idx = df["Monthly EMI (₹)"].idxmin()
    best_bank = df.iloc[cheapest_idx]["Bank"]

    # Format all currency columns properly
    display_df = df.copy()
    for col in ["Monthly EMI (₹)", "Interest Paid (₹)", "Total Repayment (₹)"]:
        display_df[col] = display_df[col].apply(lambda x: f"₹{x:,.2f}")
    display_df["Interest Rate (%)"] = display_df["Interest Rate (%)"].apply(
        lambda x: f"{x:.2f}%"
    )

    # Highlight best bank row with custom HTML
    html = """
    <style>
    .bank-table {width:100%;border-collapse:collapse;font-family:Inter,sans-serif;font-size:0.88rem;}
    .bank-table th {background:#4F46E5;color:white;padding:10px 14px;text-align:left;font-weight:600;}
    .bank-table td {padding:10px 14px;border-bottom:1px solid #E2E8F0;color:#1E293B;}
    .bank-table tr:last-child td {border-bottom:none;}
    .bank-table tr.best td {background:#EEF2FF;font-weight:600;color:#4F46E5;}
    .bank-table tr:hover td {background:#F8FAFF;}
    </style>
    <table class="bank-table">
    <thead><tr>
    """
    for col in display_df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    for i, row in display_df.iterrows():
        cls = "best" if row["Bank"] == best_bank else ""
        html += f"<tr class='{cls}'>"
        for val in row:
            html += f"<td>{val}</td>"
        if row["Bank"] == best_bank:
            html += ""
        html += "</tr>"
    html += "</tbody></table>"

    st.markdown(html, unsafe_allow_html=True)
    st.success(f"✅ Best Rate: **{best_bank}** has the lowest EMI")


def show_amortization(loan_amount: float, annual_rate: float, tenure: int) -> None:
    """Show amortization schedule with light-theme HTML table."""
    from src.emi_calculator import generate_amortization_schedule

    with st.expander("📅 View Full Amortization Schedule", expanded=False):
        schedule = generate_amortization_schedule(loan_amount, annual_rate, tenure)

        html = """
        <style>
        .amort-table {
            width: 100%; border-collapse: collapse;
            font-family: Inter, sans-serif; font-size: 0.85rem;
            background: #FFFFFF;
        }
        .amort-table th {
            background: #4F46E5; color: white;
            padding: 8px 12px; text-align: right; font-weight: 600;
        }
        .amort-table th:first-child { text-align: center; }
        .amort-table td {
            padding: 7px 12px; border-bottom: 1px solid #F1F5F9;
            text-align: right; color: #1E293B;
        }
        .amort-table td:first-child { text-align: center; color: #64748B; font-weight: 500; }
        .amort-table tr:hover td { background: #F8FAFF; }
        .amort-table tr:last-child td { border-bottom: none; }
        .amort-wrap {
            max-height: 320px; overflow-y: auto;
            border-radius: 12px; border: 1px solid #E2E8F0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        </style>
        <div class="amort-wrap">
        <table class="amort-table">
        <thead><tr>
            <th>Month</th><th>EMI</th><th>Principal</th><th>Interest</th><th>Balance</th>
        </tr></thead><tbody>
        """

        for row in schedule:
            html += f"""<tr>
                <td>{row['Month']}</td>
                <td>₹{row['EMI']:,.2f}</td>
                <td>₹{row['Principal']:,.2f}</td>
                <td>₹{row['Interest']:,.2f}</td>
                <td>₹{row['Balance']:,.2f}</td>
            </tr>"""

        html += "</tbody></table></div>"
        st.markdown(html, unsafe_allow_html=True)
        st.caption(f"📋 {len(schedule)} monthly payments over {tenure} years")


def section() -> None:
    st.divider()


def page_title() -> None:
    st.markdown("""
    <div style="padding: 1rem 0 0.5rem 0;">
        <h1 style="margin:0;padding:0;">🎓 Student Loan EMI Analyzer</h1>
        <p style="color:#64748B;margin:4px 0 0 0;font-size:0.95rem;">
            Education Loan Intelligence Platform — powered by ML
        </p>
    </div>
    """, unsafe_allow_html=True)