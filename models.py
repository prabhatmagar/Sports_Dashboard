from dataclasses import dataclass
from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime

@dataclass
class Game:
    home_team: str
    away_team: str
    home_score: Optional[int]
    away_score: Optional[int]
    venue: str
    date: str  # raw API date string (e.g., "2025-09-07T17:00Z")
    status: str
    scores: Dict
    home_logo: Optional[str] = None
    away_logo: Optional[str] = None

    @staticmethod
    def from_api_data(data):
        home = data.get("teams", {}).get("home", {})
        away = data.get("teams", {}).get("away", {})
        scores = data.get("scores", {})
        date_info = data.get("date", {})

        # API usually returns separate date + time
        if date_info.get("date") and date_info.get("time"):
            game_date = f"{date_info.get('date')}T{date_info.get('time')}Z"
        else:
            game_date = ""

        venue_info = data.get("venue", {})
        venue = f"{venue_info.get('name', 'Unknown')}, {venue_info.get('city', '')}"

        return Game(
            home_team=home.get("name", "N/A"),
            away_team=away.get("name", "N/A"),
            home_score=scores.get("home", {}).get("total", 0),
            away_score=scores.get("away", {}).get("total", 0),
            venue=venue,
            date=game_date,
            status=data.get("status", {}).get("short", "N/A"),
            scores=scores,
            home_logo=home.get("logo"),
            away_logo=away.get("logo")
        )

    @property
    def parsed_date(self) -> Optional[datetime]:
        """Safely parse ISO date with Zulu UTC support."""
        if not self.date:
            return None
        try:
            return datetime.fromisoformat(self.date.replace("Z", "+00:00"))
        except ValueError:
            return None
        

@dataclass
class Standing:
    team_name: str
    rank: int
    points: int
    all_played: int
    all_win: int
    all_draw: int
    all_lose: int
    all_goals_for: int
    all_goals_against: int
    goals_diff: int
    conference: Optional[str] = None
    team_logo: Optional[str] = None

    @classmethod
    def from_api_data(cls, data: dict) -> 'Standing':
        team_info = data.get("team", {}) or {}
        points_info = data.get("points", {}) or {}

        # --- Safely get values, default to 0 if None ---
        won = data.get("won") or 0
        lost = data.get("lost") or 0
        ties = data.get("ties") or 0

        goals_for = points_info.get("for") or 0
        goals_against = points_info.get("against") or 0
        goals_diff = points_info.get("difference") or 0

        all_played = won + lost + ties

        return cls(
            team_name=team_info.get("name", "N/A"),
            rank=data.get("position") or 0,
            points=goals_diff,
            all_played=all_played,
            all_win=won,
            all_draw=ties,
            all_lose=lost,
            all_goals_for=goals_for,
            all_goals_against=goals_against,
            goals_diff=goals_diff,
            conference=data.get("conference") or "-",
            team_logo=team_info.get("logo")
        )



# models.py

class Player:
    def __init__(self, id, name, team_name=None, position=None, photo=None, age=None, height=None, weight=None):
        self.id = id
        self.name = name
        self.team_name = team_name
        self.position = position
        self.photo = photo or "https://via.placeholder.com/100"
        self.age = age
        self.height = height
        self.weight = weight
        self.stats = []
        self.injured = False

    @classmethod
    def from_api_data(cls, data):
        """Convert API response to Player object."""
        player_info = data.get("player") or {}
        team_info = data.get("team") or {}
        return cls(
            id=player_info.get("id"),
            name=player_info.get("name"),
            team_name=team_info.get("name"),
            position=player_info.get("position"),
            photo=player_info.get("photo"),
            age=player_info.get("age"),
            height=player_info.get("height"),
            weight=player_info.get("weight")
        )


class DataProcessor:
    @staticmethod
    def games_to_dataframe(games: List[Game]) -> pd.DataFrame:
        return pd.DataFrame([{
            "Home Team": g.home_team,
            "Away Team": g.away_team,
            "Home Score": g.home_score,
            "Away Score": g.away_score,
            "Date": g.date,
            "Venue": g.venue,
            "Status": g.status
        } for g in games])

    @staticmethod
    def standings_to_dataframe(standings: List[Standing]) -> pd.DataFrame:
        return pd.DataFrame([{
            "Rank": s.rank,
            "Team": s.team_name,
            "Conference": s.conference,
            "Played": s.all_played,
            "Wins": s.all_win,
            "Draws": s.all_draw,
            "Losses": s.all_lose,
            "GF": s.all_goals_for,
            "GA": s.all_goals_against,
            "GD": s.goals_diff,
            "Points": s.points
        } for s in standings])