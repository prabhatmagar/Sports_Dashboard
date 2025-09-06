import requests
import streamlit as st
from typing import Dict, List, Optional, Any
import time
from datetime import datetime, timedelta
import pytz
from config import Config
from dummy_data import DUMMY_DATA

class APISportsClient:
    """Client for API-Sports American Football API"""
    
    def __init__(self, use_rapidapi=False):
        self.use_rapidapi = use_rapidapi
        self.base_url = Config.get_base_url(use_rapidapi)
        self.headers = Config.get_headers(use_rapidapi)
        self.session = requests.Session()
        if self.headers:
            self.session.headers.update(self.headers)
        
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make API request with error handling and rate limiting - using dummy data"""
        # Use dummy data instead of real API calls
        if endpoint in DUMMY_DATA:
            generator_func = DUMMY_DATA[endpoint]
            
            # Extract parameters for dummy data generation
            league_id = params.get('league', 1) if params else 1
            season = params.get('season', 2024) if params else 2024
            date = params.get('date') if params else None
            team_id = params.get('team') if params else None
            week = params.get('week') if params else None
            player_id = params.get('player') if params else None
            country = params.get('country', 'US') if params else 'US'
            
            # Generate dummy data based on endpoint
            if endpoint == 'games':
                return generator_func(league_id, season, date, team_id, week)
            elif endpoint == 'standings':
                return generator_func(league_id, season)
            elif endpoint == 'teams':
                return generator_func(league_id, season)
            elif endpoint == 'players':
                return generator_func(league_id, season, team_id, player_id)
            elif endpoint == 'odds':
                return generator_func(league_id, season, date, team_id)
            elif endpoint == 'leagues':
                return generator_func(country)
            elif endpoint == 'injuries':
                return generator_func(league_id, season, team_id)
            elif endpoint == 'teams/statistics':
                return generator_func(league_id, season, team_id)
            elif endpoint == 'games/events':
                game_id = params.get('fixture') if params else 1000
                return generator_func(game_id)
            elif endpoint == 'games/players':
                game_id = params.get('fixture') if params else 1000
                return generator_func(game_id)
            else:
                return generator_func()
        
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
            
        return _self._make_request("games", params) or []
    
    @st.cache_data(ttl=60)  # Shorter cache for live data
    def get_game_events(_self, game_id: int) -> List[Dict]:
        """Get events for a specific game"""
        params = {"fixture": game_id}
        return _self._make_request("games/events", params) or []
    
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_team_statistics(_self, league: int, season: int, team: int) -> Dict:
        """Get team statistics for a season"""
        params = {"league": league, "season": season, "team": team}
        result = _self._make_request("teams/statistics", params)
        # Handle both dict and list responses
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        elif isinstance(result, dict):
            return result
        else:
            return {}
    
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
        return _self._make_request("games/players", params) or {}
    
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
