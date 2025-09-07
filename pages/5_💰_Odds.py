import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from dotenv import load_dotenv
from api_client import APISportsClient
from config import Config

load_dotenv()

def main():
    st.title("💰 Odds & Betting Markets")
    st.markdown("View betting odds, moneyline, spread, and totals for NFL and NCAA games")

    api_client = APISportsClient()

    # --- Sidebar Filters ---
    with st.sidebar:
        st.header("Filters")
        league_options = {"NFL": Config.NFL_LEAGUE_ID, "NCAA": Config.NCAA_LEAGUE_ID}
        selected_league = st.selectbox("League", list(league_options.keys()))
        league_id = league_options[selected_league]

        current_season = api_client.get_current_season()
        seasons = list(range(current_season - 2, current_season + 1))
        selected_season = st.selectbox("Season", seasons, index=len(seasons)-1)

        date_option = st.radio("Date Range", ["Today", "This Week", "Custom Date"])
        today = datetime.now()
        selected_date = None
        if date_option == "Today":
            selected_date = today.strftime("%Y-%m-%d")
        elif date_option == "Custom Date":
            selected_date = st.date_input("Select Date", today).strftime("%Y-%m-%d")
        st.button("Apply Filters")

    # --- Load Odds Data ---
    with st.spinner("Loading odds data..."):
        odds_data = api_client.get_odds(league_id, selected_season, selected_date) if selected_date else api_client.get_odds(league_id, selected_season)
        if not odds_data:
            st.warning("No odds data found.")
            return

    # --- Top Metrics ---
    st.subheader("📊 Odds Overview")
    total_games = len(odds_data)
    bookmakers_set = {b.get('name') for o in odds_data for b in o.get('bookmakers', [])}
    total_markets = sum(len(o.get('bookmakers', [{}])[0].get('bets', [])) for o in odds_data)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Games", total_games)
    col2.metric("Bookmakers", len(bookmakers_set))
    col3.metric("Total Markets", total_markets)
    col4.metric("Date", selected_date if selected_date else "This Week")

    # --- Game Odds Section ---
    st.subheader("🎮 Game Odds")
    for odds in odds_data:
        game_info = odds.get('fixture', {})
        teams = odds.get('teams', {})
        bookmakers = odds.get('bookmakers', [])

        if not game_info or not teams or not bookmakers:
            continue

        with st.container():
            st.markdown(
                "<div style='background-color:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:15px; box-shadow:1px 1px 5px #ddd;'>",
                unsafe_allow_html=True
            )
            st.write(f"**{teams.get('away', {}).get('name','TBD')} vs {teams.get('home', {}).get('name','TBD')}**")
            cols = st.columns(3)
            cols[0].write(f"📅 {api_client.format_datetime(game_info.get('date',''), Config.DEFAULT_TIMEZONE)}")
            cols[1].write(f"🏟️ {game_info.get('venue', {}).get('name','TBD')}")
            status = game_info.get('status', {}).get('short','NS')
            status_emoji = {'NS':'⏰','LIVE':'🔴','FT':'✅'}.get(status,'❓')
            cols[2].write(f"{status_emoji} {status}")

            # Bookmakers odds
            for bookmaker in bookmakers:
                name = bookmaker.get('name','Unknown')
                bets = bookmaker.get('bets', [])
                with st.expander(f"📊 {name}", expanded=False):
                    for bet in bets:
                        bet_name = bet.get('name','')
                        values = bet.get('values',[])
                        if not values:
                            continue
                        st.write(f"**{bet_name}**")
                        if len(values) <= 3:
                            cols_bet = st.columns(len(values))
                            for i, val in enumerate(values):
                                with cols_bet[i]:
                                    st.write(val.get('value',''))
                                    st.write(f"**{val.get('odd','N/A')}**")
                        else:
                            df = pd.DataFrame([{'Option':v.get('value',''),'Odds':v.get('odd','N/A')} for v in values])
                            st.table(df)

            st.markdown("</div>", unsafe_allow_html=True)

    # --- Analytics Section ---
    st.subheader("📈 Analytics")
    # Bookmaker coverage
    bookmaker_counts = {}
    for odds in odds_data:
        for b in odds.get('bookmakers', []):
            name = b.get('name','Unknown')
            bookmaker_counts[name] = bookmaker_counts.get(name,0)+1
    if bookmaker_counts:
        df_bookmakers = pd.DataFrame([{'Bookmaker':k,'Games Covered':v} for k,v in bookmaker_counts.items()])
        col1, col2 = st.columns(2)
        col1.table(df_bookmakers)
        fig1 = px.pie(df_bookmakers, values='Games Covered', names='Bookmaker', title="Games Coverage by Bookmaker")
        col2.plotly_chart(fig1, use_container_width=True)

    # Popular bet types
    bet_types = {}
    for odds in odds_data:
        for b in odds.get('bookmakers', []):
            for bet in b.get('bets', []):
                bet_types[bet.get('name','Unknown')] = bet_types.get(bet.get('name','Unknown'),0)+1
    if bet_types:
        df_bets = pd.DataFrame([{'Bet Type':k,'Count':v} for k,v in bet_types.items()]).sort_values('Count',ascending=False)
        fig2 = px.bar(df_bets, x='Count', y='Bet Type', orientation='h', title="Most Popular Bet Types")
        st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()
