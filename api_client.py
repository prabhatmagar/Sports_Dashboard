import requests
from datetime import datetime
import pytz
from config import Config
import streamlit as st

DEFAULT_TIMEZONE = Config.DEFAULT_TIMEZONE

class APISportsClient:
    def __init__(self):
        self.base_url = Config.get_base_url()
        self.headers = Config.get_headers()
        if not self.headers:
            st.error("API client not initialized: missing headers.")
            raise ValueError("API key missing")

    def get_current_season(self):
        return datetime.now().year

    def get_standings(self, league_id, season):
        url = f"{self.base_url}standings"
        params = {"league": league_id, "season": season}
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            resp = data.get("response", [])
            return [d for d in resp if isinstance(d, dict)]
        except requests.RequestException as e:
            st.error(f"Error fetching standings: {e}")
            return []

    def get_games(self, league: int, season: int, date_from: str = None, date_to: str = None):
        url = f"{self.base_url}games"
        params = {"league": league, "season": season}
        if date_from: params["from"] = date_from
        if date_to: params["to"] = date_to
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            return response.json().get("response", [])
        except requests.RequestException as e:
            st.error(f"Error fetching games: {e}")
            return []

    def format_datetime(self, dt_str, tz=DEFAULT_TIMEZONE):
        try:
            dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            local_tz = pytz.timezone(tz)
            dt_local = dt.astimezone(local_tz)
            return dt_local.strftime("%Y-%m-%d %H:%M %Z")
        except Exception:
            return dt_str

    def get_teams(self, league: int, season: int):
        url = f"{self.base_url}/teams"
        params = {"league": league, "season": season}
        response = requests.get(url, headers=self.headers, params=params)
        data = response.json()
        if data.get("errors"):
            raise Exception(f"API Error: {data['errors']}")
        return data.get("response", [])

    def get_players(self, team: int, season: int):
        url = f"{self.base_url}/players"
        params = {"team": team, "season": season}
        response = requests.get(url, headers=self.headers, params=params)
        data = response.json()
        if data.get("errors"):
            raise Exception(f"API Error: {data['errors']}")
        return data.get("response", [])

    def get_player_statistics(self, player_id: int, season: int):
        url = f"{self.base_url}/players/statistics"
        params = {"id": player_id, "season": season}
        response = requests.get(url, headers=self.headers, params=params)
        data = response.json()
        if data.get("errors"):
            raise Exception(f"API Error: {data['errors']}")
        return data.get("response", [])

    # ----- New method for Odds -----
    def get_odds(self, league_id: int, season: int, date: str = None):
        """
        Fetch pre-match odds for games. Optional date filter.
        """
        url = f"{self.base_url}/odds"
        params = {"league": league_id, "season": season}
        if date:
            params["date"] = date
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            if data.get("errors"):
                st.warning(f"Odds API returned errors: {data['errors']}")
                return []
            return data.get("response", [])
        except requests.RequestException as e:
            st.error(f"Error fetching odds: {e}")
            return []
