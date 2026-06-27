import streamlit as st


def validate_inputs(
    loan_amount,
    interest_rate,
    tenure,
    salary,
):
    """
    Validate user inputs before calculations.
    Returns True if inputs are valid.
    """

    if loan_amount <= 0:
        st.error("Loan amount must be greater than ₹0.")
        return False

    if interest_rate <= 0:
        st.error("Interest rate must be greater than 0%.")
        return False

    if tenure <= 0:
        st.error("Loan tenure must be at least 1 year.")
        return False

    if salary is None:
        st.error("Median package is unavailable for the selected college.")
        return False

    if salary <= 0:
        st.error("Invalid salary data found for this college.")
        return False

    return True
def loan_warning(
    loan_amount,
    salary,
):
    """
    Display warnings for unusually large loans.
    """

    annual_salary = salary * 100000

    if loan_amount > annual_salary * 2:
        st.warning(
            "⚠️ The loan amount is more than twice the expected annual salary."
        )

    elif loan_amount > annual_salary:
        st.info(
            "ℹ️ The loan amount exceeds the expected first-year salary."
        )
        