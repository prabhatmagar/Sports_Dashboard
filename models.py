from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime
import pandas as pd

@dataclass
class Game:
    """Game/Fixture data model"""
    id: int
    league_id: int
    season: int
    week: Optional[int]
    date: str
    timezone: str
    status: str
    period: Optional[int]
    clock: Optional[str]
    venue: Optional[Dict]
    home_team: Dict
    away_team: Dict
    home_score: Optional[int]
    away_score: Optional[int]
    home_score_periods: Optional[List[int]]
    away_score_periods: Optional[List[int]]
    
    @classmethod
    def from_api_data(cls, data: Dict) -> 'Game':
        """Create Game object from API response"""
        return cls(
            id=data.get('fixture', {}).get('id', 0),
            league_id=data.get('league', {}).get('id', 0),
            season=data.get('league', {}).get('season', 0),
            week=data.get('league', {}).get('round'),
            date=data.get('fixture', {}).get('date', ''),
            timezone=data.get('fixture', {}).get('timezone', 'UTC'),
            status=data.get('fixture', {}).get('status', {}).get('short', ''),
            period=data.get('fixture', {}).get('periods', {}).get('first'),
            clock=data.get('fixture', {}).get('status', {}).get('elapsed'),
            venue=data.get('fixture', {}).get('venue'),
            home_team=data.get('teams', {}).get('home', {}),
            away_team=data.get('teams', {}).get('away', {}),
            home_score=data.get('goals', {}).get('home'),
            away_score=data.get('goals', {}).get('away'),
            home_score_periods=data.get('score', {}).get('fulltime', {}).get('home'),
            away_score_periods=data.get('score', {}).get('fulltime', {}).get('away')
        )

@dataclass
class Team:
    """Team data model"""
    id: int
    name: str
    code: str
    logo: str
    country: str
    founded: Optional[int]
    national: bool
    league_id: int
    season: int
    conference: Optional[str]
    division: Optional[str]
    
    @classmethod
    def from_api_data(cls, data: Dict, league_id: int, season: int) -> 'Team':
        """Create Team object from API response"""
        return cls(
            id=data.get('team', {}).get('id', 0),
            name=data.get('team', {}).get('name', ''),
            code=data.get('team', {}).get('code', ''),
            logo=data.get('team', {}).get('logo', ''),
            country=data.get('team', {}).get('country', ''),
            founded=data.get('team', {}).get('founded'),
            national=data.get('team', {}).get('national', False),
            league_id=league_id,
            season=season,
            conference=data.get('conference'),
            division=data.get('division')
        )

@dataclass
class Standing:
    """Standings data model"""
    team_id: int
    team_name: str
    team_logo: str
    rank: int
    conference: Optional[str]
    division: Optional[str]
    points: int
    goals_diff: int
    form: str
    description: Optional[str]
    all_played: int
    all_win: int
    all_draw: int
    all_lose: int
    all_goals_for: int
    all_goals_against: int
    home_played: int
    home_win: int
    home_draw: int
    home_lose: int
    home_goals_for: int
    home_goals_against: int
    away_played: int
    away_win: int
    away_draw: int
    away_lose: int
    away_goals_for: int
    away_goals_against: int
    
    @classmethod
    def from_api_data(cls, data: Dict) -> 'Standing':
        """Create Standing object from API response"""
        team = data.get('team', {})
        all_stats = data.get('all', {})
        home_stats = data.get('home', {})
        away_stats = data.get('away', {})
        
        return cls(
            team_id=team.get('id', 0),
            team_name=team.get('name', ''),
            team_logo=team.get('logo', ''),
            rank=data.get('rank', 0),
            conference=data.get('group', {}).get('name'),
            division=data.get('group', {}).get('name'),
            points=data.get('points', 0),
            goals_diff=data.get('goalsDiff', 0),
            form=data.get('form', ''),
            description=data.get('description'),
            all_played=all_stats.get('played', 0),
            all_win=all_stats.get('win', 0),
            all_draw=all_stats.get('draw', 0),
            all_lose=all_stats.get('lose', 0),
            all_goals_for=all_stats.get('goals', {}).get('for', 0),
            all_goals_against=all_stats.get('goals', {}).get('against', 0),
            home_played=home_stats.get('played', 0),
            home_win=home_stats.get('win', 0),
            home_draw=home_stats.get('draw', 0),
            home_lose=home_stats.get('lose', 0),
            home_goals_for=home_stats.get('goals', {}).get('for', 0),
            home_goals_against=home_stats.get('goals', {}).get('against', 0),
            away_played=away_stats.get('played', 0),
            away_win=away_stats.get('win', 0),
            away_draw=away_stats.get('draw', 0),
            away_lose=away_stats.get('lose', 0),
            away_goals_for=away_stats.get('goals', {}).get('for', 0),
            away_goals_against=away_stats.get('goals', {}).get('against', 0)
        )

@dataclass
class Player:
    """Player data model"""
    id: int
    name: str
    firstname: str
    lastname: str
    age: int
    birth_date: str
    birth_place: Optional[str]
    birth_country: str
    nationality: str
    height: Optional[str]
    weight: Optional[str]
    injured: bool
    photo: str
    team_id: int
    team_name: str
    team_logo: str
    position: str
    number: Optional[int]
    
    @classmethod
    def from_api_data(cls, data: Dict) -> 'Player':
        """Create Player object from API response"""
        team = data.get('team', {})
        
        return cls(
            id=data.get('player', {}).get('id', 0),
            name=data.get('player', {}).get('name', ''),
            firstname=data.get('player', {}).get('firstname', ''),
            lastname=data.get('player', {}).get('lastname', ''),
            age=data.get('player', {}).get('age', 0),
            birth_date=data.get('player', {}).get('birth', {}).get('date', ''),
            birth_place=data.get('player', {}).get('birth', {}).get('place'),
            birth_country=data.get('player', {}).get('birth', {}).get('country', ''),
            nationality=data.get('player', {}).get('nationality', ''),
            height=data.get('player', {}).get('height'),
            weight=data.get('player', {}).get('weight'),
            injured=data.get('player', {}).get('injured', False),
            photo=data.get('player', {}).get('photo', ''),
            team_id=team.get('id', 0),
            team_name=team.get('name', ''),
            team_logo=team.get('logo', ''),
            position=data.get('statistics', [{}])[0].get('games', {}).get('position', ''),
            number=data.get('statistics', [{}])[0].get('games', {}).get('number')
        )

@dataclass
class TeamStatistics:
    """Team statistics data model"""
    team_id: int
    team_name: str
    league_id: int
    season: int
    form: str
    fixtures_played: int
    fixtures_win: int
    fixtures_draw: int
    fixtures_lose: int
    goals_for: int
    goals_against: int
    goals_avg_for: float
    goals_avg_against: float
    clean_sheet: int
    failed_to_score: int
    penalty_scored: int
    penalty_missed: int
    
    @classmethod
    def from_api_data(cls, data: Dict, team_id: int, team_name: str, 
                     league_id: int, season: int) -> 'TeamStatistics':
        """Create TeamStatistics object from API response"""
        return cls(
            team_id=team_id,
            team_name=team_name,
            league_id=league_id,
            season=season,
            form=data.get('form', ''),
            fixtures_played=data.get('fixtures', {}).get('played', {}).get('total', 0),
            fixtures_win=data.get('fixtures', {}).get('wins', {}).get('total', 0),
            fixtures_draw=data.get('fixtures', {}).get('draws', {}).get('total', 0),
            fixtures_lose=data.get('fixtures', {}).get('loses', {}).get('total', 0),
            goals_for=data.get('goals', {}).get('for', {}).get('total', {}).get('total', 0),
            goals_against=data.get('goals', {}).get('against', {}).get('total', {}).get('total', 0),
            goals_avg_for=data.get('goals', {}).get('for', {}).get('average', {}).get('total', 0.0),
            goals_avg_against=data.get('goals', {}).get('against', {}).get('average', {}).get('total', 0.0),
            clean_sheet=data.get('goals', {}).get('against', {}).get('total', {}).get('clean_sheet', 0),
            failed_to_score=data.get('goals', {}).get('for', {}).get('total', {}).get('failed_to_score', 0),
            penalty_scored=data.get('penalty', {}).get('scored', {}).get('total', 0),
            penalty_missed=data.get('penalty', {}).get('missed', {}).get('total', 0)
        )

@dataclass
class Odds:
    """Betting odds data model"""
    game_id: int
    bookmaker: str
    bookmaker_logo: str
    last_update: str
    markets: List[Dict]
    
    @classmethod
    def from_api_data(cls, data: Dict) -> 'Odds':
        """Create Odds object from API response"""
        return cls(
            game_id=data.get('fixture', {}).get('id', 0),
            bookmaker=data.get('bookmakers', [{}])[0].get('name', ''),
            bookmaker_logo=data.get('bookmakers', [{}])[0].get('logo', ''),
            last_update=data.get('bookmakers', [{}])[0].get('last_update', ''),
            markets=data.get('bookmakers', [{}])[0].get('bets', [])
        )

class DataProcessor:
    """Utility class for processing and formatting data"""
    
    @staticmethod
    def games_to_dataframe(games: List[Game]) -> pd.DataFrame:
        """Convert list of Game objects to DataFrame"""
        data = []
        for game in games:
            data.append({
                'ID': game.id,
                'Date': game.date,
                'Home Team': game.home_team.get('name', ''),
                'Away Team': game.away_team.get('name', ''),
                'Home Score': game.home_score or 0,
                'Away Score': game.away_score or 0,
                'Status': game.status,
                'Week': game.week or '',
                'Venue': game.venue.get('name', '') if game.venue else ''
            })
        return pd.DataFrame(data)
    
    @staticmethod
    def standings_to_dataframe(standings: List[Standing]) -> pd.DataFrame:
        """Convert list of Standing objects to DataFrame"""
        data = []
        for standing in standings:
            data.append({
                'Rank': standing.rank,
                'Team': standing.team_name,
                'Points': standing.points,
                'Played': standing.all_played,
                'Wins': standing.all_win,
                'Draws': standing.all_draw,
                'Losses': standing.all_lose,
                'Goals For': standing.all_goals_for,
                'Goals Against': standing.all_goals_against,
                'Goal Diff': standing.goals_diff,
                'Form': standing.form,
                'Conference': standing.conference or '',
                'Division': standing.division or ''
            })
        return pd.DataFrame(data)
    
    @staticmethod
    def players_to_dataframe(players: List[Player]) -> pd.DataFrame:
        """Convert list of Player objects to DataFrame"""
        data = []
        for player in players:
            data.append({
                'ID': player.id,
                'Name': player.name,
                'Position': player.position,
                'Team': player.team_name,
                'Age': player.age,
                'Nationality': player.nationality,
                'Height': player.height or '',
                'Weight': player.weight or '',
                'Number': player.number or '',
                'Injured': 'Yes' if player.injured else 'No'
            })
        return pd.DataFrame(data)

