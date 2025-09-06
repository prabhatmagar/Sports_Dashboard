import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from api_client import APISportsClient
from models import Team, TeamStatistics, Player
from config import Config


def main():
    st.title("🏟️ Teams & Statistics")
    st.markdown("Explore teams, rosters, and player stats in an interactive grid view.")

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
    selected_season = st.sidebar.selectbox("Season", seasons, index=len(seasons) - 1)

    # Load teams
    with st.spinner("Loading teams..."):
        teams_data = api_client.get_teams(league_id, selected_season)
        if not teams_data:
            st.warning("No teams found.")
            return
        teams = [Team.from_api_data(team, league_id, selected_season) for team in teams_data]

    if not teams:
        st.warning("No teams available.")
        return

    st.subheader(f"{selected_league} Teams - {selected_season}")
    st.info("💡 Click on a team card to expand and see roster & stats.")

    # Team grid view
    cols = st.columns(4)
    for idx, team in enumerate(teams):
        with cols[idx % 4]:
            with st.expander(f"🏈 {team.name}", expanded=False):
                # Header with logo + name
                if team.logo:
                    st.markdown(
                        f"<h4><img src='{team.logo}' width='30' style='vertical-align:middle;margin-right:8px;'> {team.name}</h4>",
                        unsafe_allow_html=True
                    )
                else:
                    st.subheader(team.name)

                # Basic team info
                st.write(f"**Code:** {team.code or 'N/A'}")
                st.write(f"**Country:** {team.country or 'N/A'}")
                if team.conference:
                    st.write(f"**Conference:** {team.conference}")
                if team.division:
                    st.write(f"**Division:** {team.division}")
                if team.founded:
                    st.write(f"**Founded:** {team.founded}")

                # Stats
                with st.spinner("Loading team statistics..."):
                    stats_data = api_client.get_team_statistics(league_id, selected_season, team.id)
                    if stats_data:
                        stats = TeamStatistics.from_api_data(stats_data, team.id, team.name, league_id, selected_season)
                        st.subheader("📊 Team Stats")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1: st.metric("Played", stats.fixtures_played)
                        with col2: st.metric("Wins", stats.fixtures_win)
                        with col3: st.metric("Losses", stats.fixtures_lose)
                        with col4: st.metric("Goals For", stats.goals_for)
                    else:
                        st.warning("No stats available.")

                # Roster
                with st.spinner("Loading roster..."):
                    players_data = api_client.get_player_statistics(league_id, selected_season, team.id)
                    if players_data:
                        players = [Player.from_api_data(p) for p in players_data]
                        st.subheader("👥 Roster")

                        for player in players:
                            st.markdown(
                                f"""
                                <div style="display:flex;align-items:center;margin-bottom:6px;">
                                    {'<img src="'+player.photo+'" width="25" style="margin-right:6px;border-radius:50%;">' if player.photo else ''}
                                    <span><b>{player.name}</b> — {player.position or 'N/A'}</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    else:
                        st.info("No roster available.")


if __name__ == "__main__":
    main()
