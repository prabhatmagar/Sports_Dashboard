import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from api_client import APISportsClient
from models import Player
from config import Config

# CSS for cards
st.markdown("""
<style>
.player-card {
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    background-color: #ffffff;
    max-width: 100%;
    max-height: 340px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    text-align: center;
    padding: 14px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    transition: transform 0.2s ease-in-out;
    margin-bottom: 20px;
}
.player-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.player-photo {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 10px;
}
.player-name {
    font-weight: 600;
    font-size: 15px;
    margin-bottom: 4px;
}
.player-meta {
    font-size: 13px;
    color: #666;
    margin-bottom: 12px;
}
div[data-testid="stButton"] > button {
    width: 100%;
    border-radius: 8px;
    background: linear-gradient(90deg, #007bff, #00c6ff);
    color: white;
    font-weight: 600;
    border: none;
    padding: 6px 0;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(90deg, #0056b3, #0096c7);
}
</style>
""", unsafe_allow_html=True)


def render_directory(players):
    """Render players in a grid directory view"""
    st.subheader("📂 Player Directory")

    # Search bar
    search_name = st.text_input("🔍 Search by player name")
    if search_name:
        players = [p for p in players if search_name.lower() in p.name.lower()]

    # Team filter
    team_names = sorted(set(p.team_name for p in players if p.team_name))
    selected_team = st.selectbox("Filter by Team", ["All Teams"] + team_names)
    if selected_team != "All Teams":
        players = [p for p in players if p.team_name == selected_team]

    # Grid layout
    cols = st.columns(4)
    for i, player in enumerate(players):
        with cols[i % 4]:
            # Card wrapper
            with st.container():
                st.markdown(
                    f"""
                    <div class="player-card">
                        <img src="{player.photo}" class="player-photo">
                        <div class="player-name">{player.name}</div>
                        <div class="player-meta">{player.position or 'N/A'} · {player.team_name or ''}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # ✅ Pure Streamlit button, no HTML
                if st.button("View Profile", key=f"profile_{player.id}"):
                    st.session_state["selected_player"] = player
                    st.rerun()


def render_profile(player: Player):
    """Render detailed player profile"""
    st.subheader("👤 Player Profile")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(player.photo, width=200)
    with col2:
        st.write(f"**Name:** {player.name}")
        st.write(f"**Position:** {player.position}")
        st.write(f"**Team:** {player.team_name}")
        st.write(f"**Age:** {player.age}")
        st.write(f"**Height:** {player.height or 'N/A'}")
        st.write(f"**Weight:** {player.weight or 'N/A'}")
        st.write(f"**Status:** {'🚨 Injured' if player.injured else '✅ Healthy'}")

    st.markdown("---")
    st.subheader("📊 Player Insights")

    # Dummy stats
    stats_df = pd.DataFrame({
        "Metric": ["Games", "Touchdowns", "Yards", "Interceptions"],
        "Value": [10, 15, 1200, 3]
    })
    st.dataframe(stats_df, use_container_width=True)

    if st.button("⬅️ Back to Directory"):
        del st.session_state["selected_player"]
        st.rerun()


def main():
    st.title("👥 Players & Statistics")
    st.markdown("Explore player profiles, stats, and insights.")

    api_client = APISportsClient()
    st.sidebar.header("Filters")

    league_options = {"NFL": Config.NFL_LEAGUE_ID, "NCAA": Config.NCAA_LEAGUE_ID}
    selected_league = st.sidebar.selectbox("League", list(league_options.keys()))
    league_id = league_options[selected_league]

    current_season = api_client.get_current_season()
    seasons = list(range(current_season - 2, current_season + 1))
    selected_season = st.sidebar.selectbox("Season", seasons, index=len(seasons) - 1)

    with st.spinner("Loading players..."):
        players_data = api_client.get_player_statistics(league_id, selected_season)
        if not players_data:
            st.warning("No players found.")
            return
        players = [Player.from_api_data(p) for p in players_data]

    if "selected_player" in st.session_state:
        render_profile(st.session_state["selected_player"])
    else:
        render_directory(players)


if __name__ == "__main__":
    main()
