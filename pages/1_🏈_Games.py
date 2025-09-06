# pages/1_🏈_Games.py

import streamlit as st
from datetime import datetime, timedelta
from api_client import APISportsClient

st.set_page_config(page_title="🏈 Games & Schedule", layout="wide")
st.title("🏈 Games & Schedule")
st.write("View NFL/NCAA games, live scores, schedules, stats, and betting odds")

# --- Game class ---
class Game:
    def __init__(self, home_team, away_team, home_score, away_score, venue, date, status, scores, home_logo=None, away_logo=None):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.venue = venue
        self.date = date
        self.status = status
        self.scores = scores
        self.home_logo = home_logo
        self.away_logo = away_logo

    @staticmethod
    def from_api_data(data):
        home = data.get("teams", {}).get("home", {})
        away = data.get("teams", {}).get("away", {})
        scores = data.get("scores", {})
        game_date = data.get("date", {}).get("date", "")
        venue_data = data.get("venue") or {}
        venue = f"{venue_data.get('name', 'Unknown')}, {venue_data.get('city', '')}" if venue_data else "Unknown"

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

# --- Helper functions ---
def parse_games(api_response):
    games = []
    for g in api_response:
        try:
            games.append(Game.from_api_data(g))
        except Exception as e:
            st.error(f"Error parsing game data: {e}")
    return games

def filter_games(games, start_date, end_date):
    filtered = []
    for game in games:
        try:
            game_time = datetime.fromisoformat(game.date.replace("Z", "+00:00"))
            if start_date <= game_time <= end_date:
                filtered.append(game)
        except Exception:
            continue
    return filtered

def display_game(game: Game):
    st.markdown(f"**{game.home_team} ({game.home_score}) vs {game.away_team} ({game.away_score})**")
    st.text(f"Venue: {game.venue} | Date: {game.date}")

    if game.scores:
        home_quarters = [str(game.scores.get("home", {}).get(f"quarter_{i}", 0)) for i in range(1, 5)]
        away_quarters = [str(game.scores.get("away", {}).get(f"quarter_{i}", 0)) for i in range(1, 5)]
        st.text(f"Quarter Scores: {home_quarters} — {away_quarters}")

    st.markdown("---")

# --- Main App ---
def main():
    client = APISportsClient()
    api_response = client.get_games(league=1, season=2023)
    all_games = parse_games(api_response)
    now = datetime.utcnow()

    live_games = [g for g in all_games if g.status and g.status.upper() == "LIVE"]

    upcoming_games = filter_games(all_games, now, now + timedelta(days=7))
    recent_games = filter_games(all_games, now - timedelta(days=7), now)

    tabs = st.tabs(["Live Games", "Upcoming (7 days)", "Recent (7 days)"])

    with tabs[0]:
        if live_games:
            for game in live_games:
                display_game(game)
        else:
            st.info("No live games currently.")

    with tabs[1]:
        if upcoming_games:
            for game in upcoming_games:
                display_game(game)
        else:
            st.info("No upcoming games in the next week.")

    with tabs[2]:
        if recent_games:
            for game in recent_games:
                display_game(game)
        else:
            st.info("No recent games in the last week.")

if __name__ == "__main__":
    main()
