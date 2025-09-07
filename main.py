import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Sports Dashboard",
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
    st.markdown('<h1 class="main-header">🏈 Sports Dashboard</h1>', unsafe_allow_html=True)

    # Check if API key is configured
    api_key = os.getenv('API_SPORTS_KEY') or os.getenv('RAPIDAPI_KEY')
    if not api_key:
        st.error("⚠️ No API key configured. Please set API_SPORTS_KEY or RAPIDAPI_KEY in your .env file")
        return

    # Home page content
    st.markdown("## Welcome to the Sports Dashboard! 🏈")
    st.markdown("Your comprehensive source for NFL and NCAA football data, statistics, and insights.")

    # Quick stats overview
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏈 Leagues", "2", help="NFL and NCAA coverage")
    col2.metric("📊 Data Points", "10+", help="Games, standings, teams, players, odds")
    col3.metric("⚡ Real-time", "Live", help="Live scores and updates")
    col4.metric("📈 Analytics", "Advanced", help="Comprehensive statistics and visualizations")

    st.markdown("---")

# ----- Features overview without Teams -----
    st.markdown("### 🚀 Features")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🏈 Games & Schedule**
        - Live scores and game status
        - Schedule by date and week
        - Game details and venue info
        - Real-time updates
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
        st.markdown("""
        **💰 Odds & Betting**
        - Moneyline, spread, and totals
        - Multiple bookmaker comparison
        - Market analysis
        - Real-time odds updates
        """)

    st.markdown("---")

    # Quick start guide
    st.markdown("### 🎯 Quick Start")
    st.markdown("""
    1. **Select a League**: Choose between NFL or NCAA  
    2. **Pick a Season**: View current or historical seasons  
    3. **Explore Data**: Navigate through different sections using the sidebar  
    4. **Filter & Search**: Use filters to find specific information  
    5. **Analyze**: View charts, tables, and detailed statistics  
    """)

if __name__ == "__main__":
    main()
