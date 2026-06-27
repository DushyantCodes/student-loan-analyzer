import pandas as pd
import streamlit as st
from pathlib import Path
from typing import List, Dict, Any


DATA_PATH = Path("data") / "colleges.csv"


@st.cache_data
def _load_colleges() -> pd.DataFrame:
    """Load the colleges CSV once and cache the DataFrame.

    Returns an empty DataFrame if the file is missing or cannot be read.
    """
    try:
        df = pd.read_csv(DATA_PATH, encoding="utf-8")
        return df
    except Exception:
        return pd.DataFrame()


def get_college_names() -> List[str]:
    df = _load_colleges()
    if df.empty or "College Name" not in df.columns:
        # Return a single placeholder so Streamlit selectbox has an option
        return ["No colleges available"]

    names = sorted(df["College Name"].dropna().astype(str).tolist())
    if not names:
        return ["No colleges available"]
    return names


def get_college_details(college: str) -> Dict[str, Any]:
    """Return details for a given college. Gracefully handles missing data."""
    df = _load_colleges()

    if df.empty or college not in df.get("College Name", []):
        return {"rank": None, "location": "Unknown", "salary": None}

    row = df[df["College Name"] == college].iloc[0]

    rank = row.get("Rank / Band") if "Rank / Band" in row else None
    location = row.get("City / State") if "City / State" in row else "Unknown"

    salary = row.get("Median Package") if "Median Package" in row else None

    # Normalize salary to LPA (lakhs per annum)
    if pd.isna(salary) or salary is None:
        salary_val = None
    else:
        salary_str = str(salary).replace(",", "")
        try:
            salary_val = float(salary_str) / 100000
        except Exception:
            salary_val = None

    return {"rank": rank, "location": location, "salary": salary_val}