import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
from api_client import APISportsClient
from models import Game, DataProcessor
from config import Config

def main():
    st.set_page_config(page_title="Games & Schedule", page_icon="🏈", layout="wide")
    
    st.title("🏈 Games & Schedule")
    st.markdown("View NFL and NCAA games, live scores, and schedules")
    
    # Initialize API client
    api_client = APISportsClient()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # League selection
    league_options = {
        "NFL": Config.NFL_LEAGUE_ID,
        "NCAA": Config.NCAA_LEAGUE_ID
    }
    selected_league = st.sidebar.selectbox("League", list(league_options.keys()))
    league_id = league_options[selected_league]
    
    # Season selection
    current_season = api_client.get_current_season()
    seasons = list(range(current_season - 2, current_season + 1))
    selected_season = st.sidebar.selectbox("Season", seasons, index=len(seasons)-1)
    
    # Date range selection
    date_option = st.sidebar.radio("Date Range", ["Today", "This Week", "Custom Range"])
    
    if date_option == "Today":
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = start_date
    elif date_option == "This Week":
        today = datetime.now()
        start_date = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
        end_date = (today + timedelta(days=6-today.weekday())).strftime("%Y-%m-%d")
    else:
        start_date = st.sidebar.date_input("Start Date", datetime.now())
        end_date = st.sidebar.date_input("End Date", datetime.now() + timedelta(days=7))
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")
    
    # Load games data
    with st.spinner("Loading games..."):
        games_data = api_client.get_games(league_id, selected_season, start_date)
        
        if not games_data:
            st.warning("No games found for the selected criteria.")
            return
        
        # Convert to Game objects
        games = [Game.from_api_data(game) for game in games_data]
        
        # Filter by date range if custom range selected
        if date_option == "Custom Range":
            filtered_games = []
            for game in games:
                game_date = datetime.fromisoformat(game.date.replace('Z', '+00:00')).date()
                if start_date <= game_date.strftime("%Y-%m-%d") <= end_date:
                    filtered_games.append(game)
            games = filtered_games
    
    if not games:
        st.warning("No games found for the selected date range.")
        return
    
    # Display games
    st.subheader(f"{selected_league} Games - {selected_season}")
    
    # Game status summary
    status_counts = {}
    for game in games:
        status = game.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    if status_counts:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Games", len(games))
        with col2:
            st.metric("Scheduled", status_counts.get('NS', 0))
        with col3:
            st.metric("Live", status_counts.get('LIVE', 0))
        with col4:
            st.metric("Finished", status_counts.get('FT', 0))
    
    # Games display
    for game in games:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
            
            with col1:
                st.write(f"**{game.away_team.get('name', 'TBD')}**")
                if game.away_team.get('logo'):
                    st.image(game.away_team['logo'], width=50)
            
            with col2:
                if game.away_score is not None:
                    st.metric("", game.away_score)
                else:
                    st.write("--")
            
            with col3:
                if game.home_score is not None:
                    st.metric("", game.home_score)
                else:
                    st.write("--")
            
            with col4:
                st.write(f"**{game.home_team.get('name', 'TBD')}**")
                if game.home_team.get('logo'):
                    st.image(game.home_team['logo'], width=50)
            
            # Game details
            col1, col2, col3 = st.columns(3)
            with col1:
                formatted_date = api_client.format_datetime(game.date, Config.DEFAULT_TIMEZONE)
                st.write(f"📅 {formatted_date}")
            
            with col2:
                status_emoji = {
                    'NS': '⏰',
                    'LIVE': '🔴',
                    'FT': '✅',
                    'POST': '📝'
                }
                emoji = status_emoji.get(game.status, '❓')
                st.write(f"{emoji} {game.status}")
            
            with col3:
                if game.venue:
                    st.write(f"🏟️ {game.venue.get('name', 'TBD')}")
            
            if game.status == 'LIVE' and game.clock:
                st.write(f"⏱️ {game.clock}' - {game.period}Q")
            
            st.divider()
    
    # Games table view
    if st.checkbox("Show detailed table"):
        df = DataProcessor.games_to_dataframe(games)
        st.dataframe(df, use_container_width=True)
    
    # Games by week chart
    if len(games) > 1:
        st.subheader("Games by Week")
        week_counts = {}
        for game in games:
            week = game.week or 'TBD'
            week_counts[week] = week_counts.get(week, 0) + 1
        
        if week_counts:
            fig = px.bar(
                x=list(week_counts.keys()),
                y=list(week_counts.values()),
                title="Number of Games by Week",
                labels={'x': 'Week', 'y': 'Number of Games'}
            )
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()

