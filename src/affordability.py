def calculate_affordability_score(
    salary_lpa,
    emi,
    risk,
):
    """
    Returns:
        score (0-100)
        label
    """

    monthly_salary = salary_lpa * 100000 / 12

    emi_ratio = (emi / monthly_salary) * 100

    score = 100

    # -----------------------
    # EMI Burden
    # -----------------------

    if emi_ratio <= 10:
        score -= 0
    elif emi_ratio <= 20:
        score -= 10
    elif emi_ratio <= 30:
        score -= 25
    elif emi_ratio <= 40:
        score -= 40
    else:
        score -= 60

    # -----------------------
    # ML Risk
    # -----------------------

    if risk == "Low Risk":
        score -= 0
    elif risk == "Medium Risk":
        score -= 15
    else:
        score -= 35

    score = max(0, min(100, score))

    if score >= 80:
        label = "Excellent"
    elif score >= 60:
        label = "Good"
    elif score >= 40:
        label = "Average"
    else:
        label = "Poor"

    return score, label