"""
Dummy data for Sports Dashboard
This file contains mock data for all API endpoints used in the dashboard
"""

from datetime import datetime, timedelta
import random

# Dummy data for NFL teams
NFL_TEAMS = [
    {"id": 1, "name": "Kansas City Chiefs", "code": "KC", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png", "conference": "AFC", "division": "West"},
    {"id": 2, "name": "Buffalo Bills", "code": "BUF", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/buf.png", "conference": "AFC", "division": "East"},
    {"id": 3, "name": "Philadelphia Eagles", "code": "PHI", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/phi.png", "conference": "NFC", "division": "East"},
    {"id": 4, "name": "Dallas Cowboys", "code": "DAL", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/dal.png", "conference": "NFC", "division": "East"},
    {"id": 5, "name": "San Francisco 49ers", "code": "SF", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png", "conference": "NFC", "division": "West"},
    {"id": 6, "name": "Miami Dolphins", "code": "MIA", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/mia.png", "conference": "AFC", "division": "East"},
    {"id": 7, "name": "Baltimore Ravens", "code": "BAL", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/bal.png", "conference": "AFC", "division": "North"},
    {"id": 8, "name": "Cincinnati Bengals", "code": "CIN", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/cin.png", "conference": "AFC", "division": "North"},
    {"id": 9, "name": "Jacksonville Jaguars", "code": "JAX", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/jax.png", "conference": "AFC", "division": "South"},
    {"id": 10, "name": "Detroit Lions", "code": "DET", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/det.png", "conference": "NFC", "division": "North"},
    {"id": 11, "name": "Tampa Bay Buccaneers", "code": "TB", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/tb.png", "conference": "NFC", "division": "South"},
    {"id": 12, "name": "Green Bay Packers", "code": "GB", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/gb.png", "conference": "NFC", "division": "North"},
    {"id": 13, "name": "Los Angeles Rams", "code": "LAR", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png", "conference": "NFC", "division": "West"},
    {"id": 14, "name": "Seattle Seahawks", "code": "SEA", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/sea.png", "conference": "NFC", "division": "West"},
    {"id": 15, "name": "Pittsburgh Steelers", "code": "PIT", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/pit.png", "conference": "AFC", "division": "North"},
    {"id": 16, "name": "Cleveland Browns", "code": "CLE", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/cle.png", "conference": "AFC", "division": "North"},
    {"id": 17, "name": "Houston Texans", "code": "HOU", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/hou.png", "conference": "AFC", "division": "South"},
    {"id": 18, "name": "Indianapolis Colts", "code": "IND", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/ind.png", "conference": "AFC", "division": "South"},
    {"id": 19, "name": "Tennessee Titans", "code": "TEN", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/ten.png", "conference": "AFC", "division": "South"},
    {"id": 20, "name": "New York Giants", "code": "NYG", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/nyg.png", "conference": "NFC", "division": "East"},
    {"id": 21, "name": "Washington Commanders", "code": "WAS", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/was.png", "conference": "NFC", "division": "East"},
    {"id": 22, "name": "New York Jets", "code": "NYJ", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/nyj.png", "conference": "AFC", "division": "East"},
    {"id": 23, "name": "New England Patriots", "code": "NE", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/ne.png", "conference": "AFC", "division": "East"},
    {"id": 24, "name": "Las Vegas Raiders", "code": "LV", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/lv.png", "conference": "AFC", "division": "West"},
    {"id": 25, "name": "Denver Broncos", "code": "DEN", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/den.png", "conference": "AFC", "division": "West"},
    {"id": 26, "name": "Los Angeles Chargers", "code": "LAC", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/lac.png", "conference": "AFC", "division": "West"},
    {"id": 27, "name": "Arizona Cardinals", "code": "ARI", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/ari.png", "conference": "NFC", "division": "West"},
    {"id": 28, "name": "Chicago Bears", "code": "CHI", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/chi.png", "conference": "NFC", "division": "North"},
    {"id": 29, "name": "Minnesota Vikings", "code": "MIN", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/min.png", "conference": "NFC", "division": "North"},
    {"id": 30, "name": "Atlanta Falcons", "code": "ATL", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/atl.png", "conference": "NFC", "division": "South"},
    {"id": 31, "name": "Carolina Panthers", "code": "CAR", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/car.png", "conference": "NFC", "division": "South"},
    {"id": 32, "name": "New Orleans Saints", "code": "NO", "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/no.png", "conference": "NFC", "division": "South"}
]

# Dummy data for NCAA teams
NCAA_TEAMS = [
    {"id": 101, "name": "Alabama Crimson Tide", "code": "ALA", "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/333.png", "conference": "SEC", "division": "West"},
    {"id": 102, "name": "Georgia Bulldogs", "code": "UGA", "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/333.png", "conference": "SEC", "division": "East"},
    {"id": 103, "name": "Ohio State Buckeyes", "code": "OSU", "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png", "conference": "Big Ten", "division": "East"},
    {"id": 104, "name": "Michigan Wolverines", "code": "MICH", "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/130.png", "conference": "Big Ten", "division": "East"},
    {"id": 105, "name": "Clemson Tigers", "code": "CLEM", "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/228.png", "conference": "ACC", "division": "Atlantic"},
    {"id": 106, "name": "Notre Dame Fighting Irish", "code": "ND", "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/87.png", "conference": "Independent", "division": "Independent"},
    {"id": 107, "name": "Oklahoma Sooners", "code": "OU", "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/201.png", "conference": "Big 12", "division": "Big 12"},
    {"id": 108, "name": "Texas Longhorns", "code": "TEX", "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/251.png", "conference": "Big 12", "division": "Big 12"},
    {"id": 109, "name": "USC Trojans", "code": "USC", "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/30.png", "conference": "Pac-12", "division": "South"},
    {"id": 110, "name": "Oregon Ducks", "code": "ORE", "logo": "https://a.espncdn.com/i/teamlogos/ncaa/500/2483.png", "conference": "Pac-12", "division": "North"}
]

# Dummy data for players
PLAYERS = [
    {"id": 1, "name": "Patrick Mahomes", "firstname": "Patrick", "lastname": "Mahomes", "age": 28, "birth_date": "1995-09-17", "nationality": "USA", "height": "6'3\"", "weight": "230 lbs", "position": "QB", "number": 15, "team_id": 1, "team_name": "Kansas City Chiefs", "team_logo": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png", "injured": False, "photo": "https://a.espncdn.com/i/headshots/nfl/players/full/3139477.png"},
    {"id": 2, "name": "Josh Allen", "firstname": "Josh", "lastname": "Allen", "age": 27, "birth_date": "1996-05-21", "nationality": "USA", "height": "6'5\"", "weight": "237 lbs", "position": "QB", "number": 17, "team_id": 2, "team_name": "Buffalo Bills", "team_logo": "https://a.espncdn.com/i/teamlogos/nfl/500/buf.png", "injured": False, "photo": "https://a.espncdn.com/i/headshots/nfl/players/full/3918297.png"},
    {"id": 3, "name": "Jalen Hurts", "firstname": "Jalen", "lastname": "Hurts", "age": 25, "birth_date": "1998-08-07", "nationality": "USA", "height": "6'1\"", "weight": "223 lbs", "position": "QB", "number": 1, "team_id": 3, "team_name": "Philadelphia Eagles", "team_logo": "https://a.espncdn.com/i/teamlogos/nfl/500/phi.png", "injured": False, "photo": "https://a.espncdn.com/i/headshots/nfl/players/full/4362627.png"},
    {"id": 4, "name": "Dak Prescott", "firstname": "Dak", "lastname": "Prescott", "age": 30, "birth_date": "1993-07-29", "nationality": "USA", "height": "6'2\"", "weight": "238 lbs", "position": "QB", "number": 4, "team_id": 4, "team_name": "Dallas Cowboys", "team_logo": "https://a.espncdn.com/i/teamlogos/nfl/500/dal.png", "injured": False, "photo": "https://a.espncdn.com/i/headshots/nfl/players/full/2577417.png"},
    {"id": 5, "name": "Brock Purdy", "firstname": "Brock", "lastname": "Purdy", "age": 24, "birth_date": "1999-12-27", "nationality": "USA", "height": "6'1\"", "weight": "220 lbs", "position": "QB", "number": 13, "team_id": 5, "team_name": "San Francisco 49ers", "team_logo": "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png", "injured": False, "photo": "https://a.espncdn.com/i/headshots/nfl/players/full/4362627.png"},
    {"id": 6, "name": "Travis Kelce", "firstname": "Travis", "lastname": "Kelce", "age": 34, "birth_date": "1989-10-05", "nationality": "USA", "height": "6'5\"", "weight": "260 lbs", "position": "TE", "number": 87, "team_id": 1, "team_name": "Kansas City Chiefs", "team_logo": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png", "injured": False, "photo": "https://a.espncdn.com/i/headshots/nfl/players/full/15847.png"},
    {"id": 7, "name": "Tyreek Hill", "firstname": "Tyreek", "lastname": "Hill", "age": 29, "birth_date": "1994-03-01", "nationality": "USA", "height": "5'10\"", "weight": "185 lbs", "position": "WR", "number": 10, "team_id": 6, "team_name": "Miami Dolphins", "team_logo": "https://a.espncdn.com/i/teamlogos/nfl/500/mia.png", "injured": False, "photo": "https://a.espncdn.com/i/headshots/nfl/players/full/2330.png"},
    {"id": 8, "name": "Cooper Kupp", "firstname": "Cooper", "lastname": "Kupp", "age": 30, "birth_date": "1993-06-15", "nationality": "USA", "height": "6'2\"", "weight": "208 lbs", "position": "WR", "number": 10, "team_id": 13, "team_name": "Los Angeles Rams", "team_logo": "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png", "injured": False, "photo": "https://a.espncdn.com/i/headshots/nfl/players/full/2577417.png"},
    {"id": 9, "name": "Derrick Henry", "firstname": "Derrick", "lastname": "Henry", "age": 29, "birth_date": "1994-01-04", "nationality": "USA", "height": "6'3\"", "weight": "247 lbs", "position": "RB", "number": 22, "team_id": 19, "team_name": "Tennessee Titans", "team_logo": "https://a.espncdn.com/i/teamlogos/nfl/500/ten.png", "injured": False, "photo": "https://a.espncdn.com/i/headshots/nfl/players/full/2330.png"},
    {"id": 10, "name": "Aaron Donald", "firstname": "Aaron", "lastname": "Donald", "age": 32, "birth_date": "1991-05-23", "nationality": "USA", "height": "6'1\"", "weight": "280 lbs", "position": "DT", "number": 99, "team_id": 13, "team_name": "Los Angeles Rams", "team_logo": "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png", "injured": False, "photo": "https://a.espncdn.com/i/headshots/nfl/players/full/15847.png"}
]

# Dummy data for venues
VENUES = [
    {"id": 1, "name": "Arrowhead Stadium", "city": "Kansas City", "state": "MO", "capacity": 76416},
    {"id": 2, "name": "Highmark Stadium", "city": "Orchard Park", "state": "NY", "capacity": 71608},
    {"id": 3, "name": "Lincoln Financial Field", "city": "Philadelphia", "state": "PA", "capacity": 69596},
    {"id": 4, "name": "AT&T Stadium", "city": "Arlington", "state": "TX", "capacity": 80000},
    {"id": 5, "name": "Levi's Stadium", "city": "Santa Clara", "state": "CA", "capacity": 68500},
    {"id": 6, "name": "Hard Rock Stadium", "city": "Miami Gardens", "state": "FL", "capacity": 65326},
    {"id": 7, "name": "M&T Bank Stadium", "city": "Baltimore", "state": "MD", "capacity": 71008},
    {"id": 8, "name": "Paul Brown Stadium", "city": "Cincinnati", "state": "OH", "capacity": 65515},
    {"id": 9, "name": "TIAA Bank Field", "city": "Jacksonville", "state": "FL", "capacity": 69132},
    {"id": 10, "name": "Ford Field", "city": "Detroit", "state": "MI", "capacity": 65000}
]

def generate_dummy_games(league_id, season, date=None, team_id=None, week=None):
    """Generate dummy games data"""
    games = []
    teams = NFL_TEAMS if league_id == 1 else NCAA_TEAMS
    
    # Generate games for the current week
    current_week = 8  # Mid-season
    if week:
        current_week = week
    
    # Generate 8-16 games per week
    num_games = random.randint(8, 16)
    
    for i in range(num_games):
        # Randomly select teams
        home_team = random.choice(teams)
        away_team = random.choice([t for t in teams if t['id'] != home_team['id']])
        
        # Generate game date
        if date:
            game_date = datetime.fromisoformat(date)
        else:
            # Generate date for current week
            game_date = datetime.now() + timedelta(days=random.randint(-7, 7))
        
        # Generate game time
        game_time = game_date.replace(hour=random.randint(13, 20), minute=0, second=0)
        
        # Generate scores and status
        statuses = ['NS', 'LIVE', 'FT', 'POST']
        status = random.choice(statuses)
        
        home_score = None
        away_score = None
        if status in ['LIVE', 'FT', 'POST']:
            home_score = random.randint(0, 45)
            away_score = random.randint(0, 45)
        
        # Generate venue
        venue = random.choice(VENUES)
        
        game = {
            "fixture": {
                "id": 1000 + i,
                "date": game_time.isoformat() + "Z",
                "timezone": "UTC",
                "status": {
                    "short": status,
                    "elapsed": random.randint(0, 60) if status == 'LIVE' else None
                },
                "periods": {
                    "first": random.randint(1, 4) if status == 'LIVE' else None
                },
                "venue": venue
            },
            "league": {
                "id": league_id,
                "season": season,
                "round": f"Week {current_week}"
            },
            "teams": {
                "home": home_team,
                "away": away_team
            },
            "goals": {
                "home": home_score,
                "away": away_score
            },
            "score": {
                "fulltime": {
                    "home": home_score,
                    "away": away_score
                }
            }
        }
        
        games.append(game)
    
    return games

def generate_dummy_standings(league_id, season):
    """Generate dummy standings data"""
    standings = []
    teams = NFL_TEAMS if league_id == 1 else NCAA_TEAMS
    
    for i, team in enumerate(teams):
        # Generate random stats
        played = random.randint(8, 12)
        wins = random.randint(2, played)
        losses = played - wins
        draws = 0  # NFL doesn't have draws
        
        goals_for = random.randint(150, 350)
        goals_against = random.randint(100, 300)
        goals_diff = goals_for - goals_against
        
        # Calculate points (NFL: 2 points per win)
        points = wins * 2
        
        # Generate form (last 5 games)
        form = ''.join(random.choices(['W', 'L'], k=5))
        
        standing = {
            "rank": i + 1,
            "team": team,
            "points": points,
            "goalsDiff": goals_diff,
            "form": form,
            "description": "Champions" if i == 0 else "Playoffs" if i < 8 else "Eliminated",
            "all": {
                "played": played,
                "win": wins,
                "draw": draws,
                "lose": losses,
                "goals": {
                    "for": goals_for,
                    "against": goals_against
                }
            },
            "home": {
                "played": played // 2,
                "win": wins // 2,
                "draw": 0,
                "lose": losses // 2,
                "goals": {
                    "for": goals_for // 2,
                    "against": goals_against // 2
                }
            },
            "away": {
                "played": played - (played // 2),
                "win": wins - (wins // 2),
                "draw": 0,
                "lose": losses - (losses // 2),
                "goals": {
                    "for": goals_for - (goals_for // 2),
                    "against": goals_against - (goals_against // 2)
                }
            },
            "group": {
                "name": team.get('conference', 'Unknown')
            }
        }
        
        standings.append(standing)
    
    # Sort by points
    standings.sort(key=lambda x: x['points'], reverse=True)
    
    # Update ranks
    for i, standing in enumerate(standings):
        standing['rank'] = i + 1
    
    return standings

def generate_dummy_teams(league_id, season):
    """Generate dummy teams data"""
    teams = NFL_TEAMS if league_id == 1 else NCAA_TEAMS
    
    team_data = []
    for team in teams:
        team_info = {
            "team": team,
            "conference": team.get('conference'),
            "division": team.get('division')
        }
        team_data.append(team_info)
    
    return team_data

def generate_dummy_players(league_id, season, team_id=None, player_id=None):
    """Generate dummy players data"""
    players = []
    
    if team_id:
        # Filter players by team
        team_players = [p for p in PLAYERS if p['team_id'] == team_id]
    else:
        team_players = PLAYERS
    
    for player in team_players:
        player_data = {
            "player": player,
            "team": {
                "id": player['team_id'],
                "name": player['team_name'],
                "logo": player['team_logo']
            },
            "statistics": [{
                "games": {
                    "position": player['position'],
                    "number": player['number']
                }
            }]
        }
        players.append(player_data)
    
    return players

def generate_dummy_odds(league_id, season, date=None, game_id=None):
    """Generate dummy odds data"""
    odds = []
    
    # Generate odds for 5-10 games
    num_games = random.randint(5, 10)
    
    for i in range(num_games):
        game_odds = {
            "fixture": {
                "id": 1000 + i
            },
            "bookmakers": [{
                "name": random.choice(["DraftKings", "FanDuel", "BetMGM", "Caesars", "PointsBet"]),
                "logo": f"https://example.com/logo{i}.png",
                "last_update": datetime.now().isoformat() + "Z",
                "bets": [
                    {
                        "name": "Match Winner",
                        "values": [
                            {"value": "Home", "odd": round(random.uniform(1.5, 3.0), 2)},
                            {"value": "Away", "odd": round(random.uniform(1.5, 3.0), 2)}
                        ]
                    },
                    {
                        "name": "Over/Under",
                        "values": [
                            {"value": "Over 45.5", "odd": round(random.uniform(1.8, 2.2), 2)},
                            {"value": "Under 45.5", "odd": round(random.uniform(1.8, 2.2), 2)}
                        ]
                    }
                ]
            }]
        }
        odds.append(game_odds)
    
    return odds

def generate_dummy_leagues(country="US"):
    """Generate dummy leagues data"""
    leagues = [
        {
            "id": 1,
            "name": "NFL",
            "country": "USA",
            "logo": "https://a.espncdn.com/i/teamlogos/leagues/500/nfl.png",
            "flag": "https://flagcdn.com/w40/us.png",
            "season": 2024,
            "type": "League"
        },
        {
            "id": 2,
            "name": "NCAA",
            "country": "USA",
            "logo": "https://a.espncdn.com/i/teamlogos/leagues/500/ncaa.png",
            "flag": "https://flagcdn.com/w40/us.png",
            "season": 2024,
            "type": "League"
        }
    ]
    return leagues

def generate_dummy_seasons():
    """Generate dummy seasons data"""
    current_year = datetime.now().year
    seasons = []
    for year in range(current_year - 2, current_year + 1):
        seasons.append({"year": year})
    return seasons

def generate_dummy_countries():
    """Generate dummy countries data"""
    return [
        {"name": "United States", "code": "US", "flag": "https://flagcdn.com/w40/us.png"}
    ]

def generate_dummy_timezones():
    """Generate dummy timezones data"""
    return [
        {"name": "America/New_York", "offset": "-05:00"},
        {"name": "America/Chicago", "offset": "-06:00"},
        {"name": "America/Denver", "offset": "-07:00"},
        {"name": "America/Los_Angeles", "offset": "-08:00"}
    ]

def generate_dummy_injuries(league_id, season, team_id=None):
    """Generate dummy injuries data"""
    injuries = []
    teams = NFL_TEAMS if league_id == 1 else NCAA_TEAMS
    
    # Generate 5-15 injuries
    num_injuries = random.randint(5, 15)
    
    for i in range(num_injuries):
        team = random.choice(teams)
        if team_id and team['id'] != team_id:
            continue
            
        injury_types = ['Knee', 'Ankle', 'Shoulder', 'Hamstring', 'Concussion', 'Groin', 'Back', 'Foot']
        severity = random.choice(['Minor', 'Moderate', 'Severe'])
        
        injury = {
            "player": {
                "id": 1000 + i,
                "name": f"Player {i+1}",
                "photo": f"https://example.com/player{i}.png"
            },
            "team": team,
            "fixture": {
                "id": 1000 + i,
                "date": (datetime.now() + timedelta(days=random.randint(-30, 30))).isoformat() + "Z"
            },
            "league": {
                "id": league_id,
                "season": season
            },
            "type": random.choice(injury_types),
            "reason": f"{severity} {random.choice(injury_types)} injury",
            "date": (datetime.now() + timedelta(days=random.randint(-30, 30))).isoformat() + "Z"
        }
        injuries.append(injury)
    
    return injuries

def generate_dummy_team_statistics(league_id, season, team_id):
    """Generate dummy team statistics data"""
    teams = NFL_TEAMS if league_id == 1 else NCAA_TEAMS
    team = next((t for t in teams if t['id'] == team_id), teams[0])
    
    # Generate random stats
    played = random.randint(8, 12)
    wins = random.randint(2, played)
    losses = played - wins
    draws = 0
    
    goals_for = random.randint(150, 350)
    goals_against = random.randint(100, 300)
    
    return {
        "league": {
            "id": league_id,
            "season": season
        },
        "team": team,
        "form": ''.join(random.choices(['W', 'L'], k=5)),
        "fixtures": {
            "played": {"total": played},
            "wins": {"total": wins},
            "draws": {"total": draws},
            "loses": {"total": losses}
        },
        "goals": {
            "for": {
                "total": {"total": goals_for},
                "average": {"total": round(goals_for / played, 2)},
                "failed_to_score": random.randint(0, 3)
            },
            "against": {
                "total": {"total": goals_against, "clean_sheet": random.randint(0, 5)},
                "average": {"total": round(goals_against / played, 2)}
            }
        },
        "penalty": {
            "scored": {"total": random.randint(0, 10)},
            "missed": {"total": random.randint(0, 5)}
        }
    }

def generate_dummy_game_events(game_id):
    """Generate dummy game events data"""
    events = []
    
    # Generate 10-20 events per game
    num_events = random.randint(10, 20)
    
    for i in range(num_events):
        event_types = ['Goal', 'Card', 'Subst', 'Var']
        event_type = random.choice(event_types)
        
        event = {
            "time": {
                "elapsed": random.randint(1, 90),
                "extra": random.randint(0, 10) if random.random() > 0.8 else None
            },
            "team": {
                "id": random.choice([1, 2]),
                "name": f"Team {random.choice([1, 2])}",
                "logo": f"https://example.com/team{random.choice([1, 2])}.png"
            },
            "player": {
                "id": random.randint(1000, 9999),
                "name": f"Player {i+1}"
            },
            "assist": {
                "id": random.randint(1000, 9999),
                "name": f"Assist Player {i+1}"
            } if random.random() > 0.7 else None,
            "type": event_type,
            "detail": f"{event_type} event",
            "comments": f"Event {i+1} comment" if random.random() > 0.5 else None
        }
        events.append(event)
    
    return events

def generate_dummy_game_player_statistics(game_id):
    """Generate dummy game player statistics data"""
    players = []
    
    # Generate 20-40 players per game
    num_players = random.randint(20, 40)
    
    for i in range(num_players):
        player = {
            "player": {
                "id": 1000 + i,
                "name": f"Player {i+1}",
                "photo": f"https://example.com/player{i}.png"
            },
            "statistics": [{
                "games": {
                    "minutes": random.randint(0, 90),
                    "number": random.randint(1, 99),
                    "position": random.choice(['QB', 'RB', 'WR', 'TE', 'OL', 'DL', 'LB', 'DB', 'K', 'P']),
                    "rating": round(random.uniform(6.0, 10.0), 1)
                },
                "offsides": random.randint(0, 3),
                "shots": {
                    "total": random.randint(0, 10),
                    "on": random.randint(0, 5)
                },
                "goals": {
                    "total": random.randint(0, 3),
                    "conceded": random.randint(0, 2),
                    "assists": random.randint(0, 2),
                    "saves": random.randint(0, 5)
                },
                "passes": {
                    "total": random.randint(0, 50),
                    "key": random.randint(0, 10),
                    "accuracy": random.randint(70, 100)
                },
                "tackles": {
                    "total": random.randint(0, 15),
                    "blocks": random.randint(0, 5),
                    "interceptions": random.randint(0, 3)
                },
                "duels": {
                    "total": random.randint(0, 20),
                    "won": random.randint(0, 15)
                },
                "dribbles": {
                    "attempts": random.randint(0, 10),
                    "success": random.randint(0, 8),
                    "past": random.randint(0, 5)
                },
                "fouls": {
                    "drawn": random.randint(0, 5),
                    "committed": random.randint(0, 3)
                },
                "cards": {
                    "yellow": random.randint(0, 2),
                    "red": random.randint(0, 1)
                },
                "penalty": {
                    "won": random.randint(0, 2),
                    "committed": random.randint(0, 1),
                    "scored": random.randint(0, 2),
                    "missed": random.randint(0, 1),
                    "saved": random.randint(0, 1)
                }
            }]
        }
        players.append(player)
    
    return players

# Dummy data endpoints
DUMMY_DATA = {
    "games": generate_dummy_games,
    "standings": generate_dummy_standings,
    "teams": generate_dummy_teams,
    "players": generate_dummy_players,
    "odds": generate_dummy_odds,
    "leagues": generate_dummy_leagues,
    "seasons": generate_dummy_seasons,
    "countries": generate_dummy_countries,
    "timezone": generate_dummy_timezones,
    "injuries": generate_dummy_injuries,
    "teams/statistics": generate_dummy_team_statistics,
    "games/events": generate_dummy_game_events,
    "games/players": generate_dummy_game_player_statistics
}
