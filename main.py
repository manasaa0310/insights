import streamlit as st

st.set_page_config(
    page_title="Insights - Automated Data Visualizations",
    layout="wide"
)

st.title("📊 Insights — Automated Data Visualizations Platform")

st.markdown("""
Welcome! Use the sidebar to explore the **Dashboard** or **Generate a Report**.

---

### Features:
- Upload `.csv` or `.xlsx` datasets
- Instantly view interactive visualizations
- Auto-generated insights without code
- Download professional reports as PDF
- Optional deep-dive views: Sankey, Sunburst, and more
""")
