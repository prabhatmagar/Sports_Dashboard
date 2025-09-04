import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

class Config:
    # API Configuration
    API_SPORTS_KEY = os.getenv('API_SPORTS_KEY')
    API_SPORTS_BASE_URL = os.getenv('API_SPORTS_BASE_URL', 'https://v1.american-football.api-sports.io')
    
    # RapidAPI Configuration (alternative)
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
    RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST', 'api-football-v1.p.rapidapi.com')
    
    # App Configuration
    APP_TITLE = os.getenv('APP_TITLE', 'Sports Dashboard')
    DEFAULT_TIMEZONE = os.getenv('DEFAULT_TIMEZONE', 'US/Eastern')
    CACHE_DURATION = int(os.getenv('CACHE_DURATION', 300))  # 5 minutes
    
    # NFL/NCAA Configuration
    NFL_LEAGUE_ID = 1
    NCAA_LEAGUE_ID = 2
    
    @classmethod
    def get_headers(cls, use_rapidapi=False):
        """Get API headers based on configuration"""
        if use_rapidapi and cls.RAPIDAPI_KEY:
            return {
                'X-RapidAPI-Key': cls.RAPIDAPI_KEY,
                'X-RapidAPI-Host': cls.RAPIDAPI_HOST
            }
        elif cls.API_SPORTS_KEY:
            return {
                'X-RapidAPI-Key': cls.API_SPORTS_KEY,
                'X-RapidAPI-Host': 'v1.american-football.api-sports.io'
            }
        else:
            st.error("No API key configured. Please set API_SPORTS_KEY or RAPIDAPI_KEY in your .env file")
            return None
    
    @classmethod
    def get_base_url(cls, use_rapidapi=False):
        """Get base URL based on configuration"""
        if use_rapidapi:
            return f"https://{cls.RAPIDAPI_HOST}"
        else:
            return cls.API_SPORTS_BASE_URL

