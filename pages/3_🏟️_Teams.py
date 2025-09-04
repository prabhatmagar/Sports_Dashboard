import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from api_client import APISportsClient
from models import Team, TeamStatistics, DataProcessor
from config import Config

def main():
    st.set_page_config(page_title="Teams", page_icon="🏟️", layout="wide")
    
    st.title("🏟️ Teams & Statistics")
    st.markdown("View team information, statistics, and performance metrics")
    
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
    
    # Load teams data
    with st.spinner("Loading teams..."):
        teams_data = api_client.get_teams(league_id, selected_season)
        
        if not teams_data:
            st.warning("No teams found.")
            return
        
        # Convert to Team objects
        teams = [Team.from_api_data(team, league_id, selected_season) for team in teams_data]
    
    if not teams:
        st.warning("No teams data available.")
        return
    
    st.subheader(f"{selected_league} Teams - {selected_season}")
    
    # Teams overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Teams", len(teams))
    with col2:
        national_teams = sum(1 for team in teams if team.national)
        st.metric("National Teams", national_teams)
    with col3:
        conferences = set(team.conference for team in teams if team.conference)
        st.metric("Conferences", len(conferences))
    with col4:
        divisions = set(team.division for team in teams if team.division)
        st.metric("Divisions", len(divisions))
    
    # Team selection for detailed view
    team_names = [team.name for team in teams]
    selected_team_name = st.selectbox("Select a team for detailed statistics:", team_names)
    selected_team = next(team for team in teams if team.name == selected_team_name)
    
    # Display selected team info
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if selected_team.logo:
            st.image(selected_team.logo, width=150)
    
    with col2:
        st.subheader(selected_team.name)
        st.write(f"**Code:** {selected_team.code}")
        st.write(f"**Country:** {selected_team.country}")
        if selected_team.founded:
            st.write(f"**Founded:** {selected_team.founded}")
        if selected_team.conference:
            st.write(f"**Conference:** {selected_team.conference}")
        if selected_team.division:
            st.write(f"**Division:** {selected_team.division}")
        st.write(f"**National Team:** {'Yes' if selected_team.national else 'No'}")
    
    with col3:
        st.metric("Team ID", selected_team.id)
    
    # Load team statistics
    with st.spinner("Loading team statistics..."):
        team_stats_data = api_client.get_team_statistics(league_id, selected_season, selected_team.id)
        
        if team_stats_data:
            team_stats = TeamStatistics.from_api_data(
                team_stats_data, selected_team.id, selected_team.name, league_id, selected_season
            )
            
            # Team statistics display
            st.subheader("Team Statistics")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Games Played", team_stats.fixtures_played)
            with col2:
                st.metric("Wins", team_stats.fixtures_win)
            with col3:
                st.metric("Draws", team_stats.fixtures_draw)
            with col4:
                st.metric("Losses", team_stats.fixtures_lose)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Goals For", team_stats.goals_for)
            with col2:
                st.metric("Goals Against", team_stats.goals_against)
            with col3:
                st.metric("Avg Goals For", f"{team_stats.goals_avg_for:.2f}")
            with col4:
                st.metric("Avg Goals Against", f"{team_stats.goals_avg_against:.2f}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Clean Sheets", team_stats.clean_sheet)
            with col2:
                st.metric("Failed to Score", team_stats.failed_to_score)
            with col3:
                st.metric("Penalties Scored", team_stats.penalty_scored)
            with col4:
                st.metric("Penalties Missed", team_stats.penalty_missed)
            
            # Form display
            if team_stats.form:
                st.subheader("Recent Form")
                form_colors = {'W': '🟢', 'D': '🟡', 'L': '🔴'}
                form_display = " ".join([form_colors.get(result, '⚪') for result in team_stats.form[-5:]])
                st.write(form_display)
        else:
            st.warning("No statistics available for this team.")
    
    # Teams grid view
    st.subheader("All Teams")
    
    # Conference/Division grouping
    conferences = {}
    for team in teams:
        conf = team.conference or "Other"
        if conf not in conferences:
            conferences[conf] = []
        conferences[conf].append(team)
    
    for conference, conf_teams in conferences.items():
        st.subheader(f"{conference}")
        
        # Create columns for team grid
        cols = st.columns(4)
        for i, team in enumerate(conf_teams):
            with cols[i % 4]:
                with st.container():
                    if team.logo:
                        st.image(team.logo, width=80)
                    st.write(f"**{team.name}**")
                    st.write(f"Code: {team.code}")
                    if team.division:
                        st.write(f"Division: {team.division}")
                    st.write(f"Founded: {team.founded or 'N/A'}")
    
    # Teams comparison
    st.subheader("Teams Comparison")
    
    # Select teams for comparison
    selected_teams = st.multiselect(
        "Select teams to compare:",
        team_names,
        default=team_names[:3] if len(team_names) >= 3 else team_names
    )
    
    if len(selected_teams) >= 2:
        comparison_data = []
        for team_name in selected_teams:
            team = next(team for team in teams if team.name == team_name)
            team_stats_data = api_client.get_team_statistics(league_id, selected_season, team.id)
            
            if team_stats_data:
                team_stats = TeamStatistics.from_api_data(
                    team_stats_data, team.id, team.name, league_id, selected_season
                )
                comparison_data.append({
                    'Team': team.name,
                    'Games Played': team_stats.fixtures_played,
                    'Wins': team_stats.fixtures_win,
                    'Draws': team_stats.fixtures_draw,
                    'Losses': team_stats.fixtures_lose,
                    'Goals For': team_stats.goals_for,
                    'Goals Against': team_stats.goals_against,
                    'Win %': (team_stats.fixtures_win / team_stats.fixtures_played * 100) if team_stats.fixtures_played > 0 else 0
                })
        
        if comparison_data:
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)
            
            # Comparison charts
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    comparison_df,
                    x='Team',
                    y='Wins',
                    title="Wins Comparison",
                    color='Wins',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    comparison_df,
                    x='Team',
                    y='Goals For',
                    title="Goals For Comparison",
                    color='Goals For',
                    color_continuous_scale='Greens'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Teams table
    if st.checkbox("Show teams table"):
        teams_df = pd.DataFrame([
            {
                'ID': team.id,
                'Name': team.name,
                'Code': team.code,
                'Country': team.country,
                'Founded': team.founded or 'N/A',
                'Conference': team.conference or 'N/A',
                'Division': team.division or 'N/A',
                'National': 'Yes' if team.national else 'No'
            }
            for team in teams
        ])
        st.dataframe(teams_df, use_container_width=True)

if __name__ == "__main__":
    main()

