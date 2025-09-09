import streamlit as st
import os

# Load secrets (from .streamlit/secrets.toml on Streamlit Cloud)
API_KEY = st.secrets.get("API_SPORTS_KEY", None)
BASE_URL = st.secrets.get("API_SPORTS_BASE_URL", "https://v1.american-football.api-sports.io/")

# App config values
APP_TITLE = st.secrets.get("APP_TITLE", "Sports Dashboard")
DEFAULT_TIMEZONE = st.secrets.get("DEFAULT_TIMEZONE", "US/Eastern")
CACHE_DURATION = st.secrets.get("CACHE_DURATION", 300)

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f4e79, #2e8b57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2e8b57;
    }
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main header
    st.markdown(f'<h1 class="main-header">🏈 {APP_TITLE}</h1>', unsafe_allow_html=True)

    # Check if API key is configured
    if not API_KEY:
        st.error("⚠️ No API key configured. Please set API_SPORTS_KEY in your Streamlit secrets.")
        return

    # Home page content
    st.markdown("## Welcome to the Sports Dashboard! 🏈")
    st.markdown("Your comprehensive source for NFL and NCAA football data, live scores, player insights, standings, and betting odds.")

    # Quick stats overview
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏈 Leagues", "2", help="NFL and NCAA coverage")
    col2.metric("📊 Data Points", "10+", help="Games, standings, players, odds")
    col3.metric("⚡ Real-time", "Live", help="Live scores and updates")
    col4.metric("📈 Analytics", "Advanced", help="Comprehensive statistics and visualizations")

    st.markdown("---")

    # Features overview
    st.markdown("### 🚀 Features")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🏈 Games & Odds**
        - Live scores and game status
        - Schedule by date and week
        - Venue and timing info
        - Real-time **betting odds** (compare bookmakers)
        """)
        st.markdown("""
        **📊 Standings**
        - Conference and division rankings
        - Win/loss records
        - Goal differentials
        - Recent form analysis
        """)
    with col2:
        st.markdown("""
        **👥 Players**
        - Player profiles and statistics
        - Position-based analysis
        - Injury reports
        - Performance metrics
        """)

    st.markdown("---")

    # Quick start guide
    st.markdown("### 🎯 Quick Start")
    st.markdown(f"""
    1. **Select a League**: Choose between NFL or NCAA  
    2. **Pick a Season**: View current or historical seasons  
    3. **Navigate**: Use the sidebar to switch between *Games*, *Players*, and *Standings*  
    4. **Explore**: Filter and search for detailed insights  
    5. **Analyze**: Use charts, tables, and odds comparisons for deeper understanding  

    ⚙️ *Default timezone: {DEFAULT_TIMEZONE}, Cache duration: {CACHE_DURATION}s*
    """)

if __name__ == "__main__":
    main()
