import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from api_client import APISportsClient
from models import Odds, Game
from config import Config

def main():
    st.set_page_config(page_title="Odds & Betting", page_icon="💰", layout="wide")
    
    st.title("💰 Odds & Betting Markets")
    st.markdown("View betting odds, moneyline, spread, and totals for NFL and NCAA games")
    
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
    
    # Date selection
    date_option = st.sidebar.radio("Date Range", ["Today", "This Week", "Custom Date"])
    
    if date_option == "Today":
        selected_date = datetime.now().strftime("%Y-%m-%d")
    elif date_option == "This Week":
        today = datetime.now()
        start_date = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
        end_date = (today + timedelta(days=6-today.weekday())).strftime("%Y-%m-%d")
        selected_date = None
    else:
        selected_date = st.sidebar.date_input("Select Date", datetime.now())
        selected_date = selected_date.strftime("%Y-%m-%d")
    
    # Load odds data
    with st.spinner("Loading odds data..."):
        if selected_date:
            odds_data = api_client.get_odds(league_id, selected_season, selected_date)
        else:
            odds_data = api_client.get_odds(league_id, selected_season)
        
        if not odds_data:
            st.warning("No odds data found.")
            return
    
    st.subheader(f"{selected_league} Betting Odds - {selected_season}")
    
    # Odds overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Games", len(odds_data))
    with col2:
        bookmakers = set()
        for odds in odds_data:
            for bookmaker in odds.get('bookmakers', []):
                bookmakers.add(bookmaker.get('name', ''))
        st.metric("Bookmakers", len(bookmakers))
    with col3:
        total_markets = sum(len(odds.get('bookmakers', [{}])[0].get('bets', [])) for odds in odds_data)
        st.metric("Total Markets", total_markets)
    with col4:
        st.metric("Date", selected_date if selected_date else "This Week")
    
    # Display odds for each game
    for odds in odds_data:
        game_info = odds.get('fixture', {})
        teams = odds.get('teams', {})
        bookmakers = odds.get('bookmakers', [])
        
        if not game_info or not teams or not bookmakers:
            continue
        
        # Game header
        st.subheader(f"{teams.get('away', {}).get('name', 'TBD')} vs {teams.get('home', {}).get('name', 'TBD')}")
        
        # Game details
        col1, col2, col3 = st.columns(3)
        with col1:
            game_date = api_client.format_datetime(game_info.get('date', ''), Config.DEFAULT_TIMEZONE)
            st.write(f"📅 {game_date}")
        with col2:
            st.write(f"🏟️ {game_info.get('venue', {}).get('name', 'TBD')}")
        with col3:
            status = game_info.get('status', {}).get('short', 'NS')
            status_emoji = {'NS': '⏰', 'LIVE': '🔴', 'FT': '✅'}.get(status, '❓')
            st.write(f"{status_emoji} {status}")
        
        # Display odds from each bookmaker
        for bookmaker in bookmakers:
            bookmaker_name = bookmaker.get('name', 'Unknown')
            bookmaker_logo = bookmaker.get('logo', '')
            last_update = bookmaker.get('last_update', '')
            bets = bookmaker.get('bets', [])
            
            with st.expander(f"📊 {bookmaker_name}", expanded=False):
                if bookmaker_logo:
                    st.image(bookmaker_logo, width=100)
                
                if last_update:
                    st.write(f"Last Update: {last_update}")
                
                # Display different bet types
                for bet in bets:
                    bet_name = bet.get('name', '')
                    bet_values = bet.get('values', [])
                    
                    if not bet_values:
                        continue
                    
                    st.write(f"**{bet_name}**")
                    
                    # Create columns for bet values
                    if len(bet_values) <= 3:
                        cols = st.columns(len(bet_values))
                        for i, value in enumerate(bet_values):
                            with cols[i]:
                                st.write(f"{value.get('value', '')}")
                                st.write(f"**{value.get('odd', 'N/A')}**")
                    else:
                        # For more than 3 values, display in a table
                        bet_df = pd.DataFrame([
                            {
                                'Option': val.get('value', ''),
                                'Odds': val.get('odd', 'N/A')
                            }
                            for val in bet_values
                        ])
                        st.dataframe(bet_df, use_container_width=True)
                    
                    st.divider()
        
        st.divider()
    
    # Odds comparison
    st.subheader("Odds Comparison")
    
    # Get all unique games
    games = []
    for odds in odds_data:
        game_info = odds.get('fixture', {})
        teams = odds.get('teams', {})
        if game_info and teams:
            games.append({
                'game_id': game_info.get('id'),
                'home_team': teams.get('home', {}).get('name', 'TBD'),
                'away_team': teams.get('away', {}).get('name', 'TBD'),
                'date': game_info.get('date', ''),
                'bookmakers': odds.get('bookmakers', [])
            })
    
    if games:
        # Game selection for comparison
        game_options = [f"{game['away_team']} vs {game['home_team']}" for game in games]
        selected_game = st.selectbox("Select a game for odds comparison:", game_options)
        
        if selected_game:
            selected_game_data = games[game_options.index(selected_game)]
            
            # Extract moneyline odds
            moneyline_data = []
            for bookmaker in selected_game_data['bookmakers']:
                bookmaker_name = bookmaker.get('name', 'Unknown')
                for bet in bookmaker.get('bets', []):
                    if 'moneyline' in bet.get('name', '').lower() or 'match winner' in bet.get('name', '').lower():
                        for value in bet.get('values', []):
                            moneyline_data.append({
                                'Bookmaker': bookmaker_name,
                                'Team': value.get('value', ''),
                                'Odds': value.get('odd', 'N/A')
                            })
            
            if moneyline_data:
                st.write("**Moneyline Odds Comparison**")
                moneyline_df = pd.DataFrame(moneyline_data)
                st.dataframe(moneyline_df, use_container_width=True)
                
                # Moneyline chart
                if len(moneyline_data) > 0:
                    fig = px.bar(
                        moneyline_df,
                        x='Team',
                        y='Odds',
                        color='Bookmaker',
                        title="Moneyline Odds Comparison",
                        barmode='group'
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    # Bookmaker analysis
    st.subheader("Bookmaker Analysis")
    
    # Count games per bookmaker
    bookmaker_counts = {}
    for odds in odds_data:
        for bookmaker in odds.get('bookmakers', []):
            bookmaker_name = bookmaker.get('name', 'Unknown')
            bookmaker_counts[bookmaker_name] = bookmaker_counts.get(bookmaker_name, 0) + 1
    
    if bookmaker_counts:
        bookmaker_df = pd.DataFrame([
            {'Bookmaker': name, 'Games Covered': count}
            for name, count in bookmaker_counts.items()
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(bookmaker_df, use_container_width=True)
        
        with col2:
            fig = px.pie(
                bookmaker_df,
                values='Games Covered',
                names='Bookmaker',
                title="Games Coverage by Bookmaker"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Market analysis
    st.subheader("Market Analysis")
    
    # Count different bet types
    bet_types = {}
    for odds in odds_data:
        for bookmaker in odds.get('bookmakers', []):
            for bet in bookmaker.get('bets', []):
                bet_name = bet.get('name', 'Unknown')
                bet_types[bet_name] = bet_types.get(bet_name, 0) + 1
    
    if bet_types:
        bet_types_df = pd.DataFrame([
            {'Bet Type': name, 'Count': count}
            for name, count in bet_types.items()
        ]).sort_values('Count', ascending=False)
        
        fig = px.bar(
            bet_types_df,
            x='Count',
            y='Bet Type',
            title="Most Popular Bet Types",
            orientation='h'
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
