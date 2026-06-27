import pandas as pd
import streamlit as st
from pathlib import Path
from typing import List, Dict, Any


DATA_PATH = Path("data") / "colleges.csv"


@st.cache_data
def _load_colleges() -> pd.DataFrame:
    """
    Load colleges CSV once and cache it.
    - encoding='utf-8-sig' strips the UTF-8 BOM added by Excel/Windows
    - Drops trailing unnamed columns from extra commas in the CSV
    """
    try:
        df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
        return df
    except Exception:
        return pd.DataFrame()


def get_college_names() -> List[str]:
    df = _load_colleges()
    if df.empty or "College Name" not in df.columns:
        return ["No colleges available"]
    names = sorted(df["College Name"].dropna().astype(str).tolist())
    return names if names else ["No colleges available"]


def get_college_details(college: str) -> Dict[str, Any]:
    """
    Return rank, location, and salary (LPA) for a college.

    Fixes vs original:
    1. df.get("College Name", []) returned a Series — index lookup not value
       lookup — so `college in series` always returned False → salary=None.
       Fixed: use df["College Name"].values for correct value membership check.
    2. row.get(...) doesn't exist on a pandas Series — use `in row.index`.
    3. Median Package in CSV is in rupees → divided by 100000 to get LPA.
    """
    df = _load_colleges()

    if df.empty or "College Name" not in df.columns:
        return {"rank": None, "location": "Unknown", "salary": None}

    if college not in df["College Name"].values:
        return {"rank": None, "location": "Unknown", "salary": None}

    row = df[df["College Name"] == college].iloc[0]

    rank = row["Rank / Band"] if "Rank / Band" in row.index else None
    location = row["City / State"] if "City / State" in row.index else "Unknown"
    raw_salary = row["Median Package"] if "Median Package" in row.index else None

    if raw_salary is None or pd.isna(raw_salary):
        salary_lpa = None
    else:
        try:
            salary_lpa = round(float(str(raw_salary).replace(",", "")) / 100000, 2)
        except (ValueError, TypeError):
            salary_lpa = None

    return {
        "rank": int(rank) if rank is not None and not pd.isna(rank) else "N/A",
        "location": str(location) if location and not pd.isna(location) else "Unknown",
        "salary": salary_lpa,
    }