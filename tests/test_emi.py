from src.emi_calculator import calculate_emi

loan_amount = 1000000
interest = 8.3
tenure = 10

emi = calculate_emi(
    loan_amount,
    interest,
    tenure,
)

print(f"Monthly EMI: ₹{emi}")