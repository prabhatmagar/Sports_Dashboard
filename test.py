import os
import requests
from datetime import datetime

API_KEY = os.getenv("API_SPORTS_KEY")
BASE_URL = "https://v1.american-football.api-sports.io/"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "v1.american-football.api-sports.io"
}

def get_games(league: int = 1, season: int = 2023, date: str = None):
    """Fetch NFL/NCAA games from API-Sports and return list of game dicts"""
    url = f"{BASE_URL}games"
    params = {"league": league, "season": season}
    if date:
        params["date"] = date

    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()
        return [item["game"] for item in data.get("response", []) if "game" in item]
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return []
