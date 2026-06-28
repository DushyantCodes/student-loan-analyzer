## 🎓 Student Loan EMI Analyzer

A full-stack financial decision support application that helps students 
evaluate whether an education loan is affordable based on their expected 
post-graduation salary.

### The Problem
Most students take education loans without understanding the actual 
repayment burden relative to their expected salary. This tool makes 
that analysis instant, visual, and data-driven.

### Features
- **EMI Calculator** — Standard reducing-balance formula with full 
  amortization schedule
- **300+ College Dataset** — NIRF ranks and median placement packages 
  from official placement reports
- **Multi-Bank Comparison** — SBI, HDFC Credila, Axis Bank, Bank of India
- **ML Risk Prediction** — Random Forest classifier predicts repayment 
  risk with confidence score
- **Affordability Score** — 0–100 composite score combining salary ratio, 
  EMI burden, and ML risk
- **Prepayment Estimator** — Shows interest saved and months reduced by 
  paying extra monthly
- **Salary Burden Indicator** — Visual gauge showing EMI as % of monthly salary

### Tech Stack
| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python 3.11 |
| ML Model | Scikit-learn (Random Forest) |
| Data | Pandas, NumPy |
| Charts | Plotly |
| Deployment | Streamlit Community Cloud |

### Project Structure
src/
├── emi_calculator.py      # Core financial calculations
├── college_lookup.py      # College dataset loader
├── affordability.py       # Affordability scoring engine
├── risk_predictor.py      # ML model inference
├── dashboard.py           # UI components
├── validators.py          # Input validation
├── bank_rates.py          # Bank interest rate config
└── custom_style.py        # CSS theming
