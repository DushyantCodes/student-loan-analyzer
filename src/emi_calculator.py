"""
emi_calculator.py

Core financial calculations for the Student Loan EMI Analyzer.
"""

from math import pow


def validate_inputs(
    loan_amount: float,
    annual_interest_rate: float,
    tenure_years: int,
) -> None:
    """
    Validate EMI calculation inputs.

    Raises:
        ValueError: If any input is invalid.
    """

    if loan_amount <= 0:
        raise ValueError("Loan amount must be greater than 0.")

    if annual_interest_rate <= 0:
        raise ValueError("Interest rate must be greater than 0.")

    if tenure_years <= 0:
        raise ValueError("Loan tenure must be greater than 0.")


def calculate_emi(
    loan_amount: float,
    annual_interest_rate: float,
    tenure_years: int,
) -> float:
    """
    Calculate monthly EMI.

    Formula:
        EMI = P × R × (1+R)^N / ((1+R)^N − 1)

    Returns:
        Monthly EMI rounded to 2 decimal places.
    """

    validate_inputs(
        loan_amount,
        annual_interest_rate,
        tenure_years,
    )

    monthly_rate = annual_interest_rate / (12 * 100)

    number_of_months = tenure_years * 12

    emi = (
        loan_amount
        * monthly_rate
        * pow(1 + monthly_rate, number_of_months)
    ) / (
        pow(1 + monthly_rate, number_of_months) - 1
    )

    return round(emi, 2)
def calculate_total_payment(
    emi: float,
    tenure_years: int,
) -> float:
    """
    Calculate total repayment amount.
    """

    return round(
        emi * tenure_years * 12,
        2,
    )
def calculate_total_interest(
    total_payment: float,
    loan_amount: float,
) -> float:
    """
    Calculate total interest paid.
    """

    return round(
        total_payment - loan_amount,
        2,
    )
def calculate_salary_ratio(
    monthly_emi: float,
    annual_salary_lpa: float,
) -> float:
    """
    Returns EMI as a percentage of monthly salary.
    """

    if annual_salary_lpa <= 0:
        raise ValueError("Salary must be greater than zero.")

    monthly_salary = (annual_salary_lpa * 100000) / 12

    ratio = (monthly_emi / monthly_salary) * 100

    return round(ratio, 2)
