import streamlit as st
from streamlit_option_menu import option_menu
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
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
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
        st.info("Create a .env file with your API key from API-Sports or RapidAPI")
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/2e8b57/ffffff?text=Sports+Dashboard", width=200)
        
        selected = option_menu(
            menu_title="Navigation",
            options=["🏠 Home", "🏈 Games", "📊 Standings", "🏟️ Teams", "👥 Players", "💰 Odds"],
            icons=["house", "football", "bar-chart", "building", "people", "currency-dollar"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#2e8b57", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee"
                },
                "nav-link-selected": {"background-color": "#2e8b57"},
            }
        )
    
    # Home page
    if selected == "🏠 Home":
        st.markdown("## Welcome to the Sports Dashboard! 🏈")
        st.markdown("Your comprehensive source for NFL and NCAA football data, statistics, and insights.")
        
        # Quick stats overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🏈 Leagues",
                value="2",
                help="NFL and NCAA coverage"
            )
        
        with col2:
            st.metric(
                label="📊 Data Points",
                value="10+",
                help="Games, standings, teams, players, odds"
            )
        
        with col3:
            st.metric(
                label="⚡ Real-time",
                value="Live",
                help="Live scores and updates"
            )
        
        with col4:
            st.metric(
                label="📈 Analytics",
                value="Advanced",
                help="Comprehensive statistics and visualizations"
            )
        
        st.markdown("---")
        
        # Features overview
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
            **🏟️ Teams**
            - Team statistics and performance
            - Season records and metrics
            - Team comparison tools
            - Historical data
            """)
            
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
        
        # API status
        st.markdown("### 🔧 API Status")
        if api_key:
            st.success("✅ API connection configured")
            st.info(f"Using API key: {api_key[:8]}...")
        else:
            st.error("❌ API key not configured")
    
    # Redirect to other pages
    elif selected == "🏈 Games":
        st.switch_page("pages/1_🏈_Games.py")
    elif selected == "📊 Standings":
        st.switch_page("pages/2_📊_Standings.py")
    elif selected == "🏟️ Teams":
        st.switch_page("pages/3_🏟️_Teams.py")
    elif selected == "👥 Players":
        st.switch_page("pages/4_👥_Players.py")
    elif selected == "💰 Odds":
        st.switch_page("pages/5_💰_Odds.py")

if __name__ == "__main__":
    main()
