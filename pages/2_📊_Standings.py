import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from api_client import APISportsClient
from models import Standing, DataProcessor
from config import Config

def main():
    st.set_page_config(page_title="Standings", page_icon="📊", layout="wide")
    
    st.title("📊 League Standings")
    st.markdown("View team rankings, wins, losses, and performance metrics")
    
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
    
    # Load standings data
    with st.spinner("Loading standings..."):
        standings_data = api_client.get_standings(league_id, selected_season)
        
        if not standings_data:
            st.warning("No standings data found.")
            return
        
        # Convert to Standing objects
        standings = [Standing.from_api_data(standing) for standing in standings_data]
    
    if not standings:
        st.warning("No standings data available.")
        return
    
    st.subheader(f"{selected_league} Standings - {selected_season}")
    
    # Overall standings summary
    total_teams = len(standings)
    total_games = sum(s.all_played for s in standings) // 2 if standings else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Teams", total_teams)
    with col2:
        st.metric("Total Games Played", total_games)
    with col3:
        if standings:
            best_team = max(standings, key=lambda x: x.points)
            st.metric("Best Record", f"{best_team.team_name} ({best_team.all_win}-{best_team.all_lose})")
    with col4:
        if standings:
            total_goals = sum(s.all_goals_for for s in standings)
            st.metric("Total Goals Scored", total_goals)
    
    # Conference/Division breakdown
    conferences = {}
    for standing in standings:
        conf = standing.conference or "Other"
        if conf not in conferences:
            conferences[conf] = []
        conferences[conf].append(standing)
    
    # Display standings by conference/division
    for conference, conf_standings in conferences.items():
        st.subheader(f"{conference}")
        
        # Sort by points (descending) then by goal difference
        conf_standings.sort(key=lambda x: (-x.points, -x.goals_diff))
        
        # Create standings table
        standings_df = pd.DataFrame([
            {
                'Rank': i + 1,
                'Team': s.team_name,
                'P': s.all_played,
                'W': s.all_win,
                'D': s.all_draw,
                'L': s.all_lose,
                'GF': s.all_goals_for,
                'GA': s.all_goals_against,
                'GD': s.goals_diff,
                'Pts': s.points,
                'Form': s.form
            }
            for i, s in enumerate(conf_standings)
        ])
        
        # Display with team logos
        for i, standing in enumerate(conf_standings):
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
            
            with col1:
                st.write(f"**{i + 1}**")
            
            with col2:
                if standing.team_logo:
                    st.image(standing.team_logo, width=30)
                st.write(standing.team_name)
            
            with col3:
                st.write(standing.all_played)
            
            with col4:
                st.write(standing.all_win)
            
            with col5:
                st.write(standing.all_draw)
            
            with col6:
                st.write(standing.all_lose)
            
            with col7:
                st.write(standing.all_goals_for)
            
            with col8:
                st.write(standing.all_goals_against)
            
            with col9:
                st.write(standing.goals_diff)
            
            with col10:
                st.write(f"**{standing.points}**")
        
        st.divider()
    
    # Visualizations
    st.subheader("Standings Visualizations")
    
    # Points distribution
    if len(standings) > 1:
        col1, col2 = st.columns(2)
        
        with col1:
            points_data = [s.points for s in standings]
            team_names = [s.team_name for s in standings]
            
            fig = px.bar(
                x=team_names,
                y=points_data,
                title="Points by Team",
                labels={'x': 'Team', 'y': 'Points'}
            )
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Win percentage
            win_pct = []
            for s in standings:
                if s.all_played > 0:
                    pct = (s.all_win / s.all_played) * 100
                else:
                    pct = 0
                win_pct.append(pct)
            
            fig = px.bar(
                x=team_names,
                y=win_pct,
                title="Win Percentage by Team",
                labels={'x': 'Team', 'y': 'Win %'}
            )
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # Goals for vs against scatter plot
    if len(standings) > 1:
        fig = px.scatter(
            x=[s.all_goals_for for s in standings],
            y=[s.all_goals_against for s in standings],
            text=[s.team_name for s in standings],
            title="Goals For vs Goals Against",
            labels={'x': 'Goals For', 'y': 'Goals Against'}
        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed standings table
    if st.checkbox("Show detailed standings table"):
        df = DataProcessor.standings_to_dataframe(standings)
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()

