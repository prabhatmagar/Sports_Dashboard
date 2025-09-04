import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from api_client import APISportsClient
from models import Player, DataProcessor
from config import Config

def main():
    st.set_page_config(page_title="Players", page_icon="👥", layout="wide")
    
    st.title("👥 Players & Statistics")
    st.markdown("View player information, statistics, and performance metrics")
    
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
    
    # Team selection
    teams_data = api_client.get_teams(league_id, selected_season)
    team_options = {team['team']['name']: team['team']['id'] for team in teams_data} if teams_data else {}
    selected_team_name = st.sidebar.selectbox("Team (optional)", ["All Teams"] + list(team_options.keys()))
    selected_team_id = team_options.get(selected_team_name) if selected_team_name != "All Teams" else None
    
    # Position filter
    position_options = ["All", "QB", "RB", "WR", "TE", "OL", "DL", "LB", "DB", "K", "P"]
    selected_position = st.sidebar.selectbox("Position", position_options)
    
    # Load players data
    with st.spinner("Loading players..."):
        players_data = api_client.get_player_statistics(league_id, selected_season, selected_team_id)
        
        if not players_data:
            st.warning("No players found.")
            return
        
        # Convert to Player objects
        players = [Player.from_api_data(player) for player in players_data]
    
    if not players:
        st.warning("No players data available.")
        return
    
    # Filter by position if selected
    if selected_position != "All":
        players = [p for p in players if p.position == selected_position]
    
    st.subheader(f"{selected_league} Players - {selected_season}")
    
    # Players overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Players", len(players))
    with col2:
        injured_players = sum(1 for p in players if p.injured)
        st.metric("Injured Players", injured_players)
    with col3:
        positions = set(p.position for p in players if p.position)
        st.metric("Positions", len(positions))
    with col4:
        teams = set(p.team_name for p in players)
        st.metric("Teams", len(teams))
    
    # Position distribution
    if len(players) > 1:
        position_counts = {}
        for player in players:
            pos = player.position or 'Unknown'
            position_counts[pos] = position_counts.get(pos, 0) + 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                values=list(position_counts.values()),
                names=list(position_counts.keys()),
                title="Players by Position"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                x=list(position_counts.keys()),
                y=list(position_counts.values()),
                title="Players by Position",
                labels={'x': 'Position', 'y': 'Count'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Age distribution
    if len(players) > 1:
        ages = [p.age for p in players if p.age and p.age > 0]
        if ages:
            fig = px.histogram(
                x=ages,
                title="Age Distribution",
                labels={'x': 'Age', 'y': 'Count'},
                nbins=20
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Player search and selection
    st.subheader("Player Search")
    
    # Search by name
    search_name = st.text_input("Search by player name:", "")
    if search_name:
        filtered_players = [p for p in players if search_name.lower() in p.name.lower()]
    else:
        filtered_players = players
    
    # Display players
    if filtered_players:
        # Pagination
        players_per_page = 20
        total_pages = (len(filtered_players) - 1) // players_per_page + 1
        page = st.selectbox("Page", range(1, total_pages + 1))
        
        start_idx = (page - 1) * players_per_page
        end_idx = start_idx + players_per_page
        page_players = filtered_players[start_idx:end_idx]
        
        # Display players in cards
        cols = st.columns(4)
        for i, player in enumerate(page_players):
            with cols[i % 4]:
                with st.container():
                    if player.photo:
                        st.image(player.photo, width=100)
                    else:
                        st.write("📷 No Photo")
                    
                    st.write(f"**{player.name}**")
                    st.write(f"Position: {player.position}")
                    st.write(f"Team: {player.team_name}")
                    st.write(f"Age: {player.age}")
                    st.write(f"Number: {player.number or 'N/A'}")
                    
                    if player.injured:
                        st.error("🚨 Injured")
                    
                    # Player details button
                    if st.button(f"View Details", key=f"details_{player.id}"):
                        st.session_state[f"selected_player_{player.id}"] = True
                    
                    st.divider()
        
        # Player details modal
        for player in page_players:
            if st.session_state.get(f"selected_player_{player.id}", False):
                with st.expander(f"Player Details: {player.name}", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Full Name:** {player.firstname} {player.lastname}")
                        st.write(f"**Position:** {player.position}")
                        st.write(f"**Team:** {player.team_name}")
                        st.write(f"**Age:** {player.age}")
                        st.write(f"**Jersey Number:** {player.number or 'N/A'}")
                        st.write(f"**Nationality:** {player.nationality}")
                        st.write(f"**Height:** {player.height or 'N/A'}")
                        st.write(f"**Weight:** {player.weight or 'N/A'}")
                    
                    with col2:
                        if player.birth_date:
                            st.write(f"**Birth Date:** {player.birth_date}")
                        if player.birth_place:
                            st.write(f"**Birth Place:** {player.birth_place}")
                        if player.birth_country:
                            st.write(f"**Birth Country:** {player.birth_country}")
                        st.write(f"**Injured:** {'Yes' if player.injured else 'No'}")
                    
                    # Close button
                    if st.button(f"Close", key=f"close_{player.id}"):
                        st.session_state[f"selected_player_{player.id}"] = False
                        st.rerun()
    else:
        st.warning("No players found matching your search criteria.")
    
    # Top players by position
    st.subheader("Top Players by Position")
    
    # Group players by position
    position_groups = {}
    for player in players:
        pos = player.position or 'Unknown'
        if pos not in position_groups:
            position_groups[pos] = []
        position_groups[pos].append(player)
    
    # Display top players for each position
    for position, pos_players in position_groups.items():
        if len(pos_players) > 0:
            st.write(f"**{position}**")
            
            # Sort by age (youngest first) as a simple ranking
            pos_players.sort(key=lambda x: x.age if x.age else 999)
            
            # Display top 5 players
            top_players = pos_players[:5]
            for i, player in enumerate(top_players, 1):
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.write(f"{i}.")
                with col2:
                    st.write(f"{player.name} ({player.team_name})")
                with col3:
                    st.write(f"Age: {player.age}")
            st.divider()
    
    # Players table
    if st.checkbox("Show players table"):
        df = DataProcessor.players_to_dataframe(players)
        st.dataframe(df, use_container_width=True)
    
    # Team comparison
    if len(teams) > 1:
        st.subheader("Team Comparison")
        
        team_stats = {}
        for team_name in teams:
            team_players = [p for p in players if p.team_name == team_name]
            team_stats[team_name] = {
                'Total Players': len(team_players),
                'Injured Players': sum(1 for p in team_players if p.injured),
                'Average Age': sum(p.age for p in team_players if p.age) / len([p for p in team_players if p.age]) if team_players else 0,
                'Positions': len(set(p.position for p in team_players if p.position))
            }
        
        team_df = pd.DataFrame(team_stats).T
        st.dataframe(team_df, use_container_width=True)
        
        # Team comparison charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                x=team_df.index,
                y=team_df['Total Players'],
                title="Total Players by Team"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                x=team_df.index,
                y=team_df['Average Age'],
                title="Average Age by Team"
            )
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
