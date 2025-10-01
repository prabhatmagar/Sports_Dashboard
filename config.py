import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

class Config:
    # API Configuration
    API_SPORTS_KEY = os.getenv("6a0f7b7a1a47216c3c085080c82b406e")
    API_SPORTS_BASE_URL = os.getenv(
        "API_SPORTS_BASE_URL",
        "https://v1.american-football.api-sports.io/"
    )

    # Force trailing slash
    if not API_SPORTS_BASE_URL.endswith("/"):
        st.warning(f"⚠️ API_SPORTS_BASE_URL missing trailing slash, auto-fixing → {API_SPORTS_BASE_URL}/")
        API_SPORTS_BASE_URL += "/"

    # App Configuration
    APP_TITLE = os.getenv("APP_TITLE", "Sports Dashboard")
    DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "US/Eastern")
    CACHE_DURATION = int(os.getenv("CACHE_DURATION", 300))

    NFL_LEAGUE_ID = 1
    NCAA_LEAGUE_ID = 2

    @classmethod
    def get_headers(cls):
        if cls.API_SPORTS_KEY and cls.API_SPORTS_KEY != "your_api_here":
            return {"x-apisports-key": cls.API_SPORTS_KEY}
        else:
            st.error("No API key configured. Please set API_SPORTS_KEY in your .env file")
            return None

    @classmethod
    def get_base_url(cls):
        return cls.API_SPORTS_BASE_URL
    
