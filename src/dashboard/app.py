import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Nifty 100 Fundamental & Valuation Analytics")
st.markdown("""
Welcome to the **Nifty 100 Fundamental Analytics Platform**. 
Use the sidebar on the left to navigate between the 8 core analytics modules:

1. **🏠 Home**: Executive KPI overview, sector breakdown, and top compounders.
2. **👤 Company Profile**: Detailed 10-year financial breakdown, charts, and pros/cons.
3. **🔍 Screener**: Interactive 10-metric filter engine with preset screeners and CSV export.
4. **⚔️ Peer Comparison**: Radar charts and side-by-side metric comparison vs sector peers.
5. **📈 Trend Analysis**: Multi-metric 10-year historical trends with YoY growth overlays.
6. **🏭 Sector Analysis**: Interactive bubble chart and sector median benchmarks.
7. **🗺️ Capital Allocation Map**: Treemap of corporate capital allocation strategies.
8. **📑 Annual Reports**: Repository of corporate disclosures and BSE links.
""")

st.info("👈 Select a module from the left sidebar to begin exploring.")
