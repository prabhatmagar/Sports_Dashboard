import requests
import streamlit as st
from typing import Dict, List, Optional, Any
import time
from datetime import datetime, timedelta
import pytz
from config import Config

class APISportsClient:
    """Client for API-Sports American Football API"""
    
    def __init__(self, use_rapidapi=False):
        self.use_rapidapi = use_rapidapi
        self.base_url = Config.get_base_url(use_rapidapi)
        self.headers = Config.get_headers(use_rapidapi)
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make API request with error handling and rate limiting"""
        if not self.headers:
            return None
            
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Handle API-Sports response format
            if 'response' in data:
                return data['response']
            elif 'results' in data:
                return data['results']
            else:
                return data
                
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_timezones(_self) -> List[Dict]:
        """Get list of supported timezones"""
        return _self._make_request("timezone") or []
    
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_seasons(_self) -> List[Dict]:
        """Get available seasons/years"""
        return _self._make_request("seasons") or []
    
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_countries(_self) -> List[Dict]:
        """Get country metadata"""
        return _self._make_request("countries") or []
    
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_leagues(_self, country: str = "US") -> List[Dict]:
        """Get leagues (NFL, NCAA, etc.)"""
        params = {"country": country}
        return _self._make_request("leagues", params) or []
    
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_teams(_self, league: int, season: int) -> List[Dict]:
        """Get teams for a specific league and season"""
        params = {"league": league, "season": season}
        return _self._make_request("teams", params) or []
    
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_standings(_self, league: int, season: int) -> List[Dict]:
        """Get standings for a league and season"""
        params = {"league": league, "season": season}
        return _self._make_request("standings", params) or []
    
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_games(_self, league: int, season: int, date: str = None, 
                  team: int = None, week: int = None) -> List[Dict]:
        """Get games/schedule"""
        params = {"league": league, "season": season}
        if date:
            params["date"] = date
        if team:
            params["team"] = team
        if week:
            params["week"] = week
            
        return _self._make_request("fixtures", params) or []
    
    @st.cache_data(ttl=60)  # Shorter cache for live data
    def get_game_events(_self, game_id: int) -> List[Dict]:
        """Get events for a specific game"""
        params = {"fixture": game_id}
        return _self._make_request("fixtures/events", params) or []
    
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_team_statistics(_self, league: int, season: int, team: int) -> Dict:
        """Get team statistics for a season"""
        params = {"league": league, "season": season, "team": team}
        result = _self._make_request("teams/statistics", params)
        return result[0] if result else {}
    
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_player_statistics(_self, league: int, season: int, 
                             team: int = None, player: int = None) -> List[Dict]:
        """Get player statistics"""
        params = {"league": league, "season": season}
        if team:
            params["team"] = team
        if player:
            params["player"] = player
            
        return _self._make_request("players", params) or []
    
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_game_player_statistics(_self, game_id: int) -> Dict:
        """Get player statistics for a specific game"""
        params = {"fixture": game_id}
        return _self._make_request("fixtures/players", params) or {}
    
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_injuries(_self, league: int, season: int, team: int = None) -> List[Dict]:
        """Get injury reports"""
        params = {"league": league, "season": season}
        if team:
            params["team"] = team
            
        return _self._make_request("injuries", params) or []
    
    @st.cache_data(ttl=300)  # 5 minute cache for odds
    def get_odds(_self, league: int, season: int, date: str = None, 
                 game_id: int = None) -> List[Dict]:
        """Get betting odds"""
        params = {"league": league, "season": season}
        if date:
            params["date"] = date
        if game_id:
            params["fixture"] = game_id
            
        return _self._make_request("odds", params) or []
    
    def get_current_season(self) -> int:
        """Get current NFL season year"""
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # NFL season typically starts in September
        if current_month >= 9:
            return current_year
        else:
            return current_year - 1
    
    def format_datetime(self, dt_string: str, timezone: str = None) -> str:
        """Format datetime string to specified timezone"""
        if not dt_string:
            return ""
            
        try:
            # Parse the datetime string
            dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
            
            # Convert to specified timezone
            if timezone:
                tz = pytz.timezone(timezone)
                dt = dt.astimezone(tz)
            
            return dt.strftime("%Y-%m-%d %I:%M %p %Z")
        except Exception as e:
            st.warning(f"Error formatting datetime: {e}")
            return dt_string

