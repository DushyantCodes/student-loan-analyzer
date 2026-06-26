"""
bank_rates.py

Stores education loan interest rates for supported banks.

Update the values every 3–6 months if bank rates change.
"""

from typing import Dict

BANK_RATES: Dict[str, float] = {
    "SBI": 8.30,
    "HDFC Credila": 9.95,
    "Axis Bank": 9.15,
    "Bank of India": 9.50
}


def get_interest_rate(bank_name: str) -> float:
    """
    Returns the annual interest rate for a bank.

    Parameters
    ----------
    bank_name : str

    Returns
    -------
    float
    """
    if bank_name not in BANK_RATES:
        raise ValueError(f"Unsupported bank: {bank_name}")

    return BANK_RATES[bank_name]


def get_all_bank_rates() -> Dict[str, float]:
    """
    Returns all supported bank rates.
    """
    return BANK_RATES.copy()