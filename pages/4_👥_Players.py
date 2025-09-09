import streamlit as st
import pandas as pd
from api_client import APISportsClient
from config import Config

# ----- Caching -----
@st.cache_resource
def get_api_client():
    return APISportsClient()

@st.cache_data(show_spinner=False)
def fetch_teams(_api_client, league, season):
    # try:
        teams_data = _api_client.get_teams(league=league, season=season)
        return {t["id"]: t["name"] for t in teams_data}
    # except Exception as e:
    #     st.error(f"Error fetching teams: {e}")
    #     return {}

@st.cache_data(show_spinner=False)
def fetch_players(_api_client, teams_dict, season, selected_team_id=None, search_name=None):
    players = []
    try:
        # Filter by team
        team_ids = [selected_team_id] if selected_team_id else [list(teams_dict.keys())[0]]
        for team_id in team_ids:
            team_players = _api_client.get_players(team=team_id, season=season)
            for p in team_players:
                p["team_name"] = teams_dict.get(team_id, "")
            players.extend(team_players)
        # Filter by name
        if search_name:
            players = [p for p in players if search_name.lower() in p["name"].lower()]
        return players
    except Exception as e:
        st.error(f"Error fetching players: {e}")
        return []

@st.cache_data(show_spinner=False)
def fetch_player_stats(_api_client, player_id, season):
    try:
        stats = _api_client.get_player_statistics(player_id, season)
        return stats
    except Exception as e:
        st.error(f"Error fetching stats for player {player_id}: {e}")
        return []

# ----- Player Profile -----
def render_profile(player, season):
    if st.button("⬅️ Back to Directory"):
        del st.session_state["selected_player"]
        st.rerun()

    st.subheader("👤 Player Profile")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(player.get("image", ""), width=200)
    with col2:
        st.write(f"**Name:** {player.get('name')}")
        st.write(f"**Position:** {player.get('position', 'N/A')}")
        st.write(f"**Team:** {player.get('team_name', 'N/A')}")
        st.write(f"**Age:** {player.get('age', 'N/A')}")
        st.write(f"**Height:** {player.get('height', 'N/A')}")
        st.write(f"**Weight:** {player.get('weight', 'N/A')}")
        st.write(f"**Status:** {'🚨 Injured' if player.get('injured') else '✅ Healthy'}")

    st.markdown("---")
    st.subheader("📊 Player Insights")

    api_client = get_api_client()
    stats_data = fetch_player_stats(api_client, player["id"], season)

    if stats_data:
        for player_entry in stats_data:
            teams = player_entry.get("teams", [])
            for team in teams:
                groups = team.get("groups", [])
                
                if not groups:
                    st.info("No statistics available.")
                    continue

                # Dynamically create columns for horizontal alignment
                num_groups = len(groups)
                cols = st.columns(num_groups)

                for i, group in enumerate(groups):
                    group_name = group.get("name", "Stats")
                    combined_stats = {stat['name']: stat['value'] for stat in group.get("statistics", [])}

                    if combined_stats:
                        # Convert to two-column dataframe (Stat, Value)
                        df = pd.DataFrame(list(combined_stats.items()), columns=["Stat", "Value"])
                        cols[i].markdown(f"**{group_name}**")
                        # Use st.table instead of st.dataframe to remove scrollbars
                        cols[i].table(df)
    else:
        st.info("No statistics available.")


# ----- Player Directory -----
def render_directory(players, teams_dict, season):
    st.subheader("📂 Player Directory")

    # Team dropdown (full list)
    team_options = ["All Teams"] + list(teams_dict.values())
    default_team = list(teams_dict.values())[0]
    selected_team_name = st.selectbox("Filter by Team", team_options, index=team_options.index(default_team))
    selected_team_id = None
    if selected_team_name != "All Teams":
        selected_team_id = [k for k,v in teams_dict.items() if v == selected_team_name][0]

    # Name search
    search_name = st.text_input("🔍 Search by player name")

    # Fetch filtered players
    filtered_players = fetch_players(get_api_client(), teams_dict, season, selected_team_id, search_name)

    # Display player cards in rows
    row_size = 4
    for i in range(0, len(filtered_players), row_size):
        cols = st.columns(row_size)
        for j, player in enumerate(filtered_players[i:i+row_size]):
            with cols[j]:
                img_url = player.get("image") or "https://via.placeholder.com/100?text=No+Image"
                st.image(img_url, width=100)
                st.write(player.get("name"))
                st.write(f"{player.get('position', 'N/A')} · {player.get('team_name', '')}")
                if st.button("View Profile", key=f"profile_{player['id']}"):
                    st.session_state["selected_player"] = player
                    st.rerun()

# ----- Main -----
def main():
    st.title("👥 Players & Statistics")
    st.markdown("Explore real player profiles, stats, and insights.")

    api_client = get_api_client()

    st.sidebar.header("Filters")
    league_options = {"NFL": Config.NFL_LEAGUE_ID, "NCAA": Config.NCAA_LEAGUE_ID}
    selected_league = st.sidebar.selectbox("League", list(league_options.keys()))
    league_id = league_options[selected_league]

    current_season = api_client.get_current_season()
    seasons = list(range(current_season - 2, current_season + 1))
    selected_season = st.sidebar.selectbox("Season", seasons, index=len(seasons) - 1)

    # --- Fetch teams safely ---
    teams_dict = fetch_teams(api_client, league_id, selected_season)

    if not teams_dict:
        if selected_season > 2000:
            selected_season -= 1
            teams_dict = fetch_teams(api_client, league_id, selected_season)


    # --- Player profile or directory ---
    if "selected_player" in st.session_state:
        render_profile(st.session_state["selected_player"], selected_season)
    else:
        players = fetch_players(api_client, teams_dict, selected_season)
        if not players:
            st.info(f"No players available for season {selected_season}.")
        else:
            render_directory(players, teams_dict, selected_season)


if __name__ == "__main__":
    main()
