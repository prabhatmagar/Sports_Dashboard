import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from api_client import APISportsClient
from models import Standing, DataProcessor
from config import Config

# Load environment variables
load_dotenv()

def main():
    st.title("📊 League Standings")
    st.markdown("View **team rankings**, wins/losses, and performance metrics with clean visuals.")

    api_client = APISportsClient()

    # Sidebar filters
    with st.sidebar:
        st.header("⚙️ Filters")
        league_options = {"NFL": Config.NFL_LEAGUE_ID, "NCAA": Config.NCAA_LEAGUE_ID}
        selected_league = st.selectbox("Select League", list(league_options.keys()))
        league_id = league_options[selected_league]

        current_season = api_client.get_current_season()
        seasons = list(range(current_season - 2, current_season + 1))
        selected_season = st.selectbox("Select Season", seasons, index=len(seasons) - 1)

    # Load standings
    with st.spinner("Fetching standings..."):
        standings_data = api_client.get_standings(league_id, selected_season)
        standings = [Standing.from_api_data(s) for s in standings_data] if standings_data else []

    if not standings:
        st.warning("⚠️ No standings data available for this selection.")
        return

    st.subheader(f"{selected_league} Standings - {selected_season}")
    st.info("💡 **Tip:** Click on Teams page for detailed rosters and player statistics.")

    # Summary Metrics
    total_teams = len(standings)
    total_games = sum(s.all_played for s in standings) // 2
    total_goals = sum(s.all_goals_for for s in standings)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Teams", total_teams)
    col2.metric("Games Played", total_games)
    best_team = max(standings, key=lambda x: x.points)
    col3.metric("Best Team", f"{best_team.team_name}", f"{best_team.all_win}-{best_team.all_lose}")
    col4.metric("Goals Scored", total_goals)

    st.markdown("---")

    # Organize by conference
    conferences = {}
    for s in standings:
        conferences.setdefault(s.conference or "Other", []).append(s)

    for conference, conf_standings in conferences.items():
        st.markdown(f"### 🏆 {conference}")

        conf_standings.sort(key=lambda x: (-x.points, -x.goals_diff))

        # --------------------------
        # Table header row
        # --------------------------
        header_cols = st.columns([0.5, 3, 1, 1, 1, 1, 1, 1, 1, 1])
        headers = ["Rank", "Team", "P", "W", "D", "L", "GF", "GA", "GD", "Pts"]
        for col, text in zip(header_cols, headers):
            col.markdown(f"**{text}**")
        st.divider()

        # --------------------------
        # Table body rows
        # --------------------------
        for i, s in enumerate(conf_standings, start=1):
            row_cols = st.columns([0.5, 3, 1, 1, 1, 1, 1, 1, 1, 1])

            # Rank
            row_cols[0].markdown(f"**{i}**")

            # Team (logo + name inline)
            with row_cols[1]:
                team_col1, team_col2 = st.columns([1, 5])
                with team_col1:
                    if s.team_logo:
                        st.image(s.team_logo, width=28)
                with team_col2:
                    st.markdown(f"**{s.team_name}**")

            # Stats
            row_cols[2].write(s.all_played)
            row_cols[3].write(s.all_win)
            row_cols[4].write(s.all_draw)
            row_cols[5].write(s.all_lose)
            row_cols[6].write(s.all_goals_for)
            row_cols[7].write(s.all_goals_against)
            row_cols[8].write(s.goals_diff)
            row_cols[9].markdown(f"**{s.points}**")

        st.divider()

    # --------------------------
    # Visualizations
    # --------------------------
    st.subheader("📈 Standings Visualizations")

    if len(standings) > 1:
        team_names = [s.team_name for s in standings]

        col1, col2 = st.columns(2)

        with col1:
            fig_points = px.bar(
                x=team_names,
                y=[s.points for s in standings],
                title="Total Points by Team",
                labels={"x": "Team", "y": "Points"},
                text_auto=True,
            )
            fig_points.update_xaxes(tickangle=45)
            st.plotly_chart(fig_points, use_container_width=True)

        with col2:
            win_pct = [(s.all_win / s.all_played * 100) if s.all_played else 0 for s in standings]
            fig_win = px.bar(
                x=team_names,
                y=win_pct,
                title="Win % by Team",
                labels={"x": "Team", "y": "Win %"},
                text_auto=".1f",
            )
            fig_win.update_xaxes(tickangle=45)
            st.plotly_chart(fig_win, use_container_width=True)

        fig_scatter = px.scatter(
            x=[s.all_goals_for for s in standings],
            y=[s.all_goals_against for s in standings],
            text=team_names,
            size=[s.points for s in standings],
            title="Goals For vs Goals Against (Bubble Size = Points)",
            labels={"x": "Goals For", "y": "Goals Against"},
        )
        fig_scatter.update_traces(textposition="top center")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Expandable detailed table
    with st.expander("🔍 Show Detailed Standings Table"):
        df = DataProcessor.standings_to_dataframe(standings)
        st.dataframe(df, use_container_width=True, height=500)


if __name__ == "__main__":
    main()
