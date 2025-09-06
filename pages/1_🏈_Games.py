# pages/1_🏈_Games.py

import streamlit as st
from datetime import datetime, timedelta, timezone
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
        self.date = date  # datetime object (UTC)
        self.status = status
        self.scores = scores
        self.home_logo = home_logo
        self.away_logo = away_logo

    @staticmethod
    def from_api_data(data):
        home = data.get("teams", {}).get("home", {})
        away = data.get("teams", {}).get("away", {})
        scores = data.get("scores", {})
        date_info = data.get("game", {}).get("date", {})
        date_str = date_info.get("date", "1970-01-01")
        time_str = date_info.get("time", "00:00")
        dt = datetime.fromisoformat(f"{date_str}T{time_str}:00+00:00")  # UTC aware
        venue_data = data.get("game", {}).get("venue") or {}
        venue = f"{venue_data.get('name', 'Unknown')}, {venue_data.get('city', '')}" if venue_data else "Unknown"
        status_info = data.get("game", {}).get("status", {})
        status = status_info.get("short", "N/A")

        return Game(
            home_team=home.get("name", "N/A"),
            away_team=away.get("name", "N/A"),
            home_score=scores.get("home", {}).get("total", 0),
            away_score=scores.get("away", {}).get("total", 0),
            venue=venue,
            date=dt,
            status=status,
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

def display_game(game: Game, upcoming=False):
    """
    Display a single game in a clean layout.
    upcoming: True for games not started yet (no scores)
    """
    import streamlit as st

    st.markdown("---")
    
    col1, col2, col3 = st.columns([3, 1, 3])
    
    # Home team
    with col1:
        if game.home_logo:
            st.image(game.home_logo, width=80)
        st.markdown(f"### {game.home_team}")
        if not upcoming and game.home_score is not None:
            st.markdown(f"**Score: {game.home_score}**")
    
    # VS + status
    with col2:
        st.markdown("### VS")
        st.markdown(f"**{game.status or 'NS'}**")
    
    # Away team
    with col3:
        if game.away_logo:
            st.image(game.away_logo, width=80)
        st.markdown(f"### {game.away_team}")
        if not upcoming and game.away_score is not None:
            st.markdown(f"**Score: {game.away_score}**")
    
    # Venue & Date
    st.markdown(f"📍 **Venue:** {game.venue}  |  🕒 **Date (UTC):** {game.date.strftime('%Y-%m-%d %H:%M')}")
    
    if not upcoming:
        # Only show quarter scores for live/finished games
        home_quarters = [str(game.scores.get("home", {}).get(f"quarter_{i}", 0)) for i in range(1, 5)]
        away_quarters = [str(game.scores.get("away", {}).get(f"quarter_{i}", 0)) for i in range(1, 5)]
        st.markdown(f"🏈 **Quarter Scores:** {', '.join(home_quarters)} — {', '.join(away_quarters)}")
    else:
        # Show odds or placeholder for upcoming games
        if hasattr(game, "odds") and game.odds:
            st.markdown(f"💰 **Odds:** {game.odds}")
        else:
            st.markdown("💰 **Odds:** N/A")



# --- Main App ---
def main():
    client = APISportsClient()

    # Sidebar filters
    with st.sidebar:
        st.header("⚙️ Filters")
        leagues = {"NFL": 1, "NCAA": 2}  # adjust IDs
        selected_league = st.selectbox("Select League", list(leagues.keys()))
        league_id = leagues[selected_league]

        current_season = client.get_current_season()
        selected_season = st.selectbox("Select Season", list(range(current_season - 2, current_season + 1)), index=2)

        st.markdown("---")
        st.subheader("Search by Date Range")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        custom_search = st.button("Search by Date")

    # Fetch all games for the season
    api_response = client.get_games(league=league_id, season=selected_season)
    all_games = parse_games(api_response)
    now = datetime.now(timezone.utc)

    # Live / upcoming / recent
    live_games = [g for g in all_games if g.status.upper() == "LIVE"]
    upcoming_games = [g for g in all_games if g.date > now and g.status.upper() != "FT"]
    recent_games = [g for g in all_games if g.date <= now]

    # Custom date range
    if custom_search:
        start_dt = datetime.combine(start_date, datetime.min.time()).replace(tzinfo=timezone.utc)
        end_dt = datetime.combine(end_date, datetime.max.time()).replace(tzinfo=timezone.utc)
        custom_games = [g for g in all_games if start_dt <= g.date <= end_dt]

    # Tabs
    if custom_search:
        tabs = st.tabs(["Custom Date Range"])
        with tabs[0]:
            if custom_games:
                for g in custom_games:
                    display_game(g)
            else:
                st.info("No games found in this date range.")
    else:
        tabs = st.tabs(["Live Games", "Upcoming (7 days)", "Recent (7 days)"])
        with tabs[0]:
            if live_games:
                for g in live_games:
                    display_game(g)
            else:
                st.info("No live games currently.")
        with tabs[1]:
            upcoming_7 = [g for g in upcoming_games if g.date <= now + timedelta(days=7)]
            if upcoming_7:
                for g in upcoming_7:
                    display_game(g)
            else:
                st.info("No upcoming games in the next 7 days.")
        with tabs[2]:
            recent_7 = [g for g in recent_games if g.date >= now - timedelta(days=7)]
            if recent_7:
                for g in recent_7:
                    display_game(g)
            else:
                st.info("No recent games in the last 7 days.")

if __name__ == "__main__":
    main()
