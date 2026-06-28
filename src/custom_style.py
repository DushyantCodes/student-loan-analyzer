import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1E293B !important;
    }

    /* ── App background ── */
    .stApp {
        background: linear-gradient(135deg, #F0F4FF 0%, #FAF5FF 50%, #FFF7ED 100%) !important;
    }

    /* ── Main title ── */
    h1 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #4F46E5, #7C3AED, #EC4899);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }

    /* ── Section headers ── */
    h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        color: #4F46E5 !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E1B4B 0%, #312E81 60%, #4C1D95 100%) !important;
        border-right: none !important;
    }

    [data-testid="stSidebar"] * {
        color: #E0E7FF !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* Slider thumb only — amber, clean */
    [data-testid="stSidebar"] div[role="slider"] {
        background: #F59E0B !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
    }

    /* FIX 4: Metric cards in sidebar — dark text, visible */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        padding: 0.8rem !important;
    }

    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #C7D2FE !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
    }

    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* ── Main area metric cards ── */
    [data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 1.2rem 1.4rem !important;
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.08) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(79, 70, 229, 0.15) !important;
    }

    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }

    [data-testid="stMetricValue"] {
        color: #4F46E5 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
    }

    /* ── Primary button ── */
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.5) !important;
    }

    /* ── Divider ── */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, #4F46E5, #7C3AED, #EC4899) !important;
        border-radius: 2px !important;
        margin: 1.5rem 0 !important;
        opacity: 0.3 !important;
    }

    /* ── Progress bar ── */
    [data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #4F46E5, #7C3AED) !important;
        border-radius: 99px !important;
    }

    /* FIX 2: Expander — white background, dark text, no black */
    [data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    [data-testid="stExpander"] summary {
        background: #F8FAFF !important;
        color: #4F46E5 !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        padding: 0.8rem 1rem !important;
    }

    [data-testid="stExpander"] summary:hover {
        background: #EEF2FF !important;
    }

    /* FIX 2: Dataframe inside expander — white bg */
    [data-testid="stExpander"] [data-testid="stDataFrame"] {
        background: #FFFFFF !important;
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    }

    /* ── Info box ── */
    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    /* ── Caption ── */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #64748B !important;
    }

    /* FIX 1: Page title area — ensure visible on load */
    .stApp > div:first-child {
        min-height: 80px !important;
    }

    </style>
    """, unsafe_allow_html=True)