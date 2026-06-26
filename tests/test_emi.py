from src.emi_calculator import (
    calculate_emi,
    calculate_total_payment,
    calculate_total_interest,
    calculate_salary_ratio,
)

loan_amount = 1000000
interest = 8.3
tenure = 10
salary = 12

emi = calculate_emi(
    loan_amount,
    interest,
    tenure,
)

total_payment = calculate_total_payment(
    emi,
    tenure,
)

interest_paid = calculate_total_interest(
    total_payment,
    loan_amount,
)

ratio = calculate_salary_ratio(
    emi,
    salary,
)

print(f"Monthly EMI        : ₹{emi}")
print(f"Total Repayment   : ₹{total_payment}")
print(f"Interest Paid     : ₹{interest_paid}")
print(f"Salary Ratio      : {ratio}%")
from src.emi_calculator import (
    calculate_prepayment_savings,
    generate_amortization_schedule,
)

saved, months = calculate_prepayment_savings(
    loan_amount,
    interest,
    tenure,
    5000,
)

print(f"Interest Saved : ₹{saved}")
print(f"New Tenure     : {months} months")

schedule = generate_amortization_schedule(
    loan_amount,
    interest,
    tenure,
)

print("\nFirst 5 Months")

for row in schedule[:5]:
    print(row)