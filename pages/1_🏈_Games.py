import streamlit as st
from datetime import datetime, timedelta, timezone
from api_client import APISportsClient
from models import Game
from config import Config

def main():
    st.title("🏈 Games & Schedule")
    st.markdown("View NFL and NCAA games, live scores, and schedules")

    api_client = APISportsClient()

    # --- Sidebar Filters ---
    with st.sidebar:
        st.header("Filters")
        league_options = {"NFL": Config.NFL_LEAGUE_ID, "NCAA": Config.NCAA_LEAGUE_ID}
        selected_league = st.selectbox("League", list(league_options.keys()))
        league_id = league_options[selected_league]

        current_season = api_client.get_current_season()
        seasons = list(range(current_season - 2, current_season + 1))
        selected_season = st.selectbox("Season", seasons, index=len(seasons)-1)

        date_option = st.radio("Date Range", ["Today", "This Week", "Custom Range"])
        today = datetime.now(timezone.utc)
        if date_option == "Today":
            start_date = end_date = today.strftime("%Y-%m-%d")
        elif date_option == "This Week":
            start_date = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
            end_date = (today + timedelta(days=6-today.weekday())).strftime("%Y-%m-%d")
        else:
            start_date = st.date_input("Start Date", today).strftime("%Y-%m-%d")
            end_date = st.date_input("End Date", today + timedelta(days=7)).strftime("%Y-%m-%d")
        st.button("Apply Filters")

    # --- Load Games ---
    with st.spinner("Loading games..."):
        games_data = api_client.get_games(league_id, selected_season, start_date)
        if not games_data:
            st.warning("No games found for the selected criteria.")
            return
        games = [Game.from_api_data(g) for g in games_data]

    if not games:
        st.warning("No games found for this date range.")
        return

    now = datetime.now(timezone.utc)  # Offset-aware datetime

    # --- Categorize Games ---
    live_games = []
    upcoming_games = []
    recent_games = []

    for g in games:
        game_time = datetime.fromisoformat(g.date.replace('Z', '+00:00'))
        if g.status == 'LIVE':
            live_games.append(g)
        elif g.status in ['NS', 'POST']:
            if now <= game_time <= now + timedelta(days=7):
                upcoming_games.append(g)
        elif g.status == 'FT':
            if now - timedelta(days=7) <= game_time <= now:
                recent_games.append(g)

    # --- Helper to render games in neutral container ---
    def render_game_card(game):
        with st.container():
            st.markdown("<div style='background-color:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:10px; box-shadow: 1px 1px 5px #ddd;'>", unsafe_allow_html=True)
            cols = st.columns([2, 1, 1, 2])
            away_col, away_score_col, home_score_col, home_col = cols

            away_col.write(f"**{game.away_team.get('name','TBD')}**")
            if game.away_team.get("logo"):
                away_col.image(game.away_team["logo"], width=50)
            away_score_col.metric("", game.away_score if game.away_score is not None else "--")

            home_col.write(f"**{game.home_team.get('name','TBD')}**")
            if game.home_team.get("logo"):
                home_col.image(game.home_team["logo"], width=50)
            home_score_col.metric("", game.home_score if game.home_score is not None else "--")

            info_cols = st.columns(3)
            info_cols[0].write(f"📅 {api_client.format_datetime(game.date, Config.DEFAULT_TIMEZONE)}")
            status_emoji = {'NS':'⏰','LIVE':'🔴','FT':'✅','POST':'📝'}
            info_cols[1].write(f"{status_emoji.get(game.status,'❓')} {game.status}")
            info_cols[2].write(f"🏟️ {game.venue.get('name','TBD')}" if game.venue else "")
            if game.status == 'LIVE' and game.clock:
                st.write(f"⏱️ {game.clock}' - {game.period}Q")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- Sections ---
    if live_games:
        st.subheader("🔴 Live Games")
        for g in live_games:
            render_game_card(g)
    else:
        st.info("No live games currently.")

    if upcoming_games:
        st.subheader("⏰ Upcoming Games (Next 7 Days)")
        for g in upcoming_games:
            render_game_card(g)
    else:
        st.info("No upcoming games in the next week.")

    if recent_games:
        st.subheader("✅ Recent Games (Last 7 Days)")
        for g in recent_games:
            render_game_card(g)
    else:
        st.info("No recent games in the last week.")

if __name__ == "__main__":
    main()
