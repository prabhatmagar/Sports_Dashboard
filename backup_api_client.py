import requests
import streamlit as st
from typing import Dict, List, Optional, Any
from datetime import datetime
import pytz
from config import Config


class APISportsClient:
    """Client for API-Sports American Football API"""

    def __init__(self, use_rapidapi: bool = False):
        self.use_rapidapi = use_rapidapi
        self.base_url = Config.get_base_url(use_rapidapi)  # e.g., "https://v1.american-football.api-sports.io/"
        self.headers = Config.get_headers(use_rapidapi)    # must include "x-apisports-key"
        self.session = requests.Session()
        if self.headers:
            self.session.headers.update(self.headers)

    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        try:
            # Always normalize base + endpoint
            base = self.base_url.rstrip("/")
            ep = endpoint.lstrip("/")
            url = f"{base}/{ep}"

            st.write(f"🔍 Debug Request → {url} | Params: {params}")
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json().get("response", [])
        except requests.RequestException as e:
            st.error(f"API request failed: {e}")
            return None



    # ------------------------------
    # API Methods
    # ------------------------------
    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_timezones(_self) -> List[Dict]:
        return _self._make_request("timezone") or []

    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_seasons(_self) -> List[Dict]:
        return _self._make_request("seasons") or []

    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_countries(_self) -> List[Dict]:
        return _self._make_request("countries") or []

    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_leagues(_self, country: str = "US") -> List[Dict]:
        params = {"country": country}
        return _self._make_request("leagues", params) or []

    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_teams(_self, league: int, season: int) -> List[Dict]:
        params = {"league": league, "season": season}
        return _self._make_request("teams", params) or []

    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_standings(_self, league: int, season: int) -> List[Dict]:
        params = {"league": league, "season": season}
        return _self._make_request("standings", params) or []

    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_games(_self, league: int, season: int, date: str = None,
                  team: int = None, week: int = None) -> List[Dict]:
        params = {"league": league, "season": season}
        if date:
            params["date"] = date
        if team:
            params["team"] = team
        if week:
            params["week"] = week
        return _self._make_request("games", params) or []

    @st.cache_data(ttl=60)
    def get_game_events(_self, game_id: int) -> List[Dict]:
        params = {"fixture": game_id}
        return _self._make_request("games/events", params) or []

    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_team_statistics(_self, league: int, season: int, team: int) -> Dict:
        params = {"league": league, "season": season, "team": team}
        return _self._make_request("teams/statistics", params) or {}

    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_player_statistics(_self, league: int, season: int,
                              team: int = None, player: int = None) -> List[Dict]:
        params = {"league": league, "season": season}
        if team:
            params["team"] = team
        if player:
            params["player"] = player
        return _self._make_request("players", params) or []

    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_game_player_statistics(_self, game_id: int) -> Dict:
        params = {"fixture": game_id}
        return _self._make_request("games/players", params) or {}

    @st.cache_data(ttl=Config.CACHE_DURATION)
    def get_injuries(_self, league: int, season: int, team: int = None) -> List[Dict]:
        params = {"league": league, "season": season}
        if team:
            params["team"] = team
        return _self._make_request("injuries", params) or []

    @st.cache_data(ttl=300)
    def get_odds(_self, league: int, season: int, date: str = None,
                 game_id: int = None) -> List[Dict]:
        params = {"league": league, "season": season}
        if date:
            params["date"] = date
        if game_id:
            params["fixture"] = game_id
        return _self._make_request("odds", params) or []

    # ------------------------------
    # Utility
    # ------------------------------
    def get_current_season(self) -> int:
        current_year = datetime.now().year
        current_month = datetime.now().month
        return current_year if current_month >= 9 else current_year - 1

    def format_datetime(self, dt_string: str, timezone: str = None) -> str:
        if not dt_string:
            return ""
        try:
            dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
            if timezone:
                tz = pytz.timezone(timezone)
                dt = dt.astimezone(tz)
            return dt.strftime("%Y-%m-%d %I:%M %p %Z")
        except Exception as e:
            st.warning(f"Error formatting datetime: {e}")
            return dt_string
