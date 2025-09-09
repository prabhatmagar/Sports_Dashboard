# standings.py

import streamlit as st
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv
from api_client import APISportsClient
from models import Standing, DataProcessor
from config import Config

load_dotenv()


def main():
    st.title("📊 League Standings")
    st.markdown(
        "View **team rankings**, wins/losses, and performance metrics with clean visuals."
    )

    client = APISportsClient()

    # --- Sidebar filters ---
    with st.sidebar:
        st.header("⚙️ Filters")
        leagues = {"NFL": Config.NFL_LEAGUE_ID, "NCAA": Config.NCAA_LEAGUE_ID}
        selected_league = st.selectbox("Select League", list(leagues.keys()))
        league_id = leagues[selected_league]

        current_season = client.get_current_season()
        seasons = list(range(current_season - 2, current_season + 1))
        selected_season = st.selectbox(
            "Select Season", seasons, index=len(seasons) - 1
        )

    # --- Fetch standings ---
    with st.spinner("Fetching standings..."):
        raw_data = client.get_standings(league_id, selected_season)

    # --- Parse safely ---
    standings = []
    for entry in raw_data:
        if not isinstance(entry, dict):
            continue
        try:
            standings.append(Standing.from_api_data(entry))
        except Exception as e:
            st.error(f"Error parsing standing: {e}")

    if not standings or all((s.points or 0) == 0 for s in standings):
        st.warning("⚠️ Standings data not yet available for this season.")
        return

    # --- Display summary ---
    st.subheader(f"{selected_league} Standings - {selected_season}")
    st.info("💡 Tip: Click on Teams page for detailed rosters and player statistics.")

    total_teams = len(standings)
    total_games = sum(s.all_played or 0 for s in standings) // 2
    total_goals = sum(s.all_goals_for or 0 for s in standings)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Teams", total_teams)
    col2.metric("Games Played", total_games)

    try:
        best_team = max(standings, key=lambda s: s.points or 0)
        col3.metric(
            "Best Team",
            f"{best_team.team_name}",
            f"{best_team.all_win}-{best_team.all_lose}"
        )
    except Exception:
        col3.metric("Best Team", "N/A")

    col4.metric("Goals Scored", total_goals)
    st.markdown("---")

    # --- Tabs by Conference ---
    if selected_league == "NFL":
        conference_tabs = ["American Football Conference", "National Football Conference"]
    else:
        conference_tabs = sorted(set(s.conference for s in standings if s.conference))

    tab_objects = st.tabs(conference_tabs)

    for i, conf in enumerate(conference_tabs):
        with tab_objects[i]:
            conf_standings = [s for s in standings if s.conference == conf]
            if not conf_standings:
                st.warning(f"No data for {conf} conference.")
                continue

            df = DataProcessor.standings_to_dataframe(conf_standings)

            # --- Sort by Points descending ---
            if "Points" in df.columns:
                df = df.sort_values(by="Points", ascending=False)

            # --- Add Rank column if not exists ---
            if "Rank" not in df.columns:
                df.insert(0, "Rank", range(1, len(df) + 1))

            # --- Remove default index completely ---
            df_display = df.copy()
            df_display.index = [""] * len(df_display)  # blank index

            st.subheader(f"{conf} Conference Standings")
            st.table(df_display)  # table completely hides index

            # --- Charts ---
            if len(conf_standings) > 1:
                teams = df["Team"].tolist()

                col1, col2 = st.columns(2)
                with col1:
                    fig = px.bar(
                        x=teams,
                        y=df["Points"],
                        title="Total Points by Team",
                        labels={"x": "Team", "y": "Points"},
                        text_auto=True,
                    )
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    win_pct = [
                        (s.all_win / s.all_played * 100) if s.all_played else 0
                        for s in conf_standings
                    ]
                    fig2 = px.bar(
                        x=teams,
                        y=win_pct,
                        title="Win % by Team",
                        labels={"x": "Team", "y": "Win %"},
                        text_auto=".1f",
                    )
                    fig2.update_xaxes(tickangle=45)
                    st.plotly_chart(fig2, use_container_width=True)

                fig3 = px.scatter(
                    x=[s.all_goals_for for s in conf_standings],
                    y=[s.all_goals_against for s in conf_standings],
                    size=[max(s.points, 0) for s in conf_standings],
                    text=teams,
                    title="Goals For vs Goals Against (Bubble Size = Points)",
                    labels={"x": "Goals For", "y": "Goals Against"},
                )
                fig3.update_traces(textposition="top center")
                st.plotly_chart(fig3, use_container_width=True)


if __name__ == "__main__":
    main()
