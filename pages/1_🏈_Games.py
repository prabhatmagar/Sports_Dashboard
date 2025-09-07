# pages/1_🏈_Games.py

import streamlit as st
from datetime import datetime, timedelta, timezone
import requests
import pandas as pd

from api_client import APISportsClient
from config import Config
from models import Game as GameModel  # your dataclass (with parsed_date property)

st.set_page_config(page_title="🏈 Games & Odds", layout="wide")
st.title("🏈 Games & Odds")
st.write("View NFL/NCAA games, live scores, schedules, stats, and betting odds")


# ----------------- Helpers -----------------
def _to_iso_from_section(date_section):
    """Return an ISO Zulu string from different possible date_section shapes."""
    if not date_section:
        return ""
    if isinstance(date_section, dict):
        ts = date_section.get("timestamp")
        if ts:
            try:
                return datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                pass
        d = date_section.get("date")
        t = date_section.get("time")
        if d and t:
            if len(t.split(":")) == 2:
                t = f"{t}:00"
            return f"{d}T{t}Z"
        if d:
            return f"{d}T00:00:00Z"
        for v in date_section.values():
            if isinstance(v, str):
                try:
                    dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
                    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                except Exception:
                    continue
        return ""
    if isinstance(date_section, (int, float)):
        try:
            return datetime.fromtimestamp(int(date_section), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            return ""
    if isinstance(date_section, str):
        try:
            dt = datetime.fromisoformat(date_section.replace("Z", "+00:00"))
            return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            try:
                dt = datetime.strptime(date_section, "%Y-%m-%d %H:%M")
                return dt.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                return date_section
    return ""


def attach_game_id(game_obj: GameModel, raw: dict) -> None:
    """
    Attach API game id to the Game object so we can fetch odds with /odds?game=ID.
    Looks for raw['game']['id'] or raw['id'] or raw['fixture']['id'].
    """
    gid = None
    if isinstance(raw.get("game"), dict):
        gid = raw["game"].get("id")
    if gid is None:
        gid = raw.get("id") or raw.get("fixture", {}).get("id")
    setattr(game_obj, "game_id", gid)


@st.cache_data(show_spinner=False)
def fetch_odds_cached(game_id: int, base_url: str, headers_items: tuple):
    """
    Cached request to GET /odds?game=<id>
    headers_items must be a tuple(list(dict.items())) to be hashable; function rebuilds headers.
    Returns:
      - None if empty response
      - {"errors": ...} if API returned errors
      - {"_error": "..."} on request exception
      - dict payload for that game otherwise
    """
    if not game_id:
        return None
    headers = dict(headers_items)
    url = base_url.rstrip("/") + "/odds"
    params = {"game": game_id}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=12)
        resp.raise_for_status()
        data = resp.json()
        if data.get("errors"):
            return {"errors": data.get("errors")}
        arr = data.get("response", [])
        return arr[0] if arr else None
    except requests.RequestException as e:
        return {"_error": str(e)}


def format_dt(game: GameModel) -> str:
    dt = game.parsed_date
    if dt:
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")
    return "TBD"


# ----------------- Parsing -----------------
def parse_games(api_response):
    """
    Robust parsing of various API shapes. Returns list of GameModel instances.
    """
    games = []
    for raw in api_response:
        try:
            teams = raw.get("teams") or {}
            home = teams.get("home", {}) if isinstance(teams, dict) else {}
            away = teams.get("away", {}) if isinstance(teams, dict) else {}
            scores = raw.get("scores") or raw.get("score") or {}

            venue_section = (raw.get("game") or {}).get("venue") or raw.get("venue") or {}
            venue = ""
            if isinstance(venue_section, dict):
                venue = f"{venue_section.get('name', 'Unknown')}, {venue_section.get('city','')}".strip(", ")
            elif isinstance(venue_section, str):
                venue = venue_section

            date_section = (raw.get("game") or {}).get("date") or raw.get("date") or raw.get("fixture", {}).get("date")
            iso_date = _to_iso_from_section(date_section)

            status = (raw.get("game") or {}).get("status", {}) or raw.get("status", {})
            if isinstance(status, dict):
                status_short = status.get("short") or status.get("long") or "N/A"
            else:
                status_short = str(status or "N/A")

            home_name = home.get("name") or home.get("team", {}).get("name") or "N/A"
            away_name = away.get("name") or away.get("team", {}).get("name") or "N/A"
            home_logo = home.get("logo") or home.get("team", {}).get("logo")
            away_logo = away.get("logo") or away.get("team", {}).get("logo")

            home_total = None
            away_total = None
            try:
                home_total = scores.get("home", {}).get("total") if isinstance(scores, dict) else None
            except Exception:
                pass
            try:
                away_total = scores.get("away", {}).get("total") if isinstance(scores, dict) else None
            except Exception:
                pass

            game_obj = GameModel(
                home_team=home_name,
                away_team=away_name,
                home_score=home_total,
                away_score=away_total,
                venue=venue or "Unknown",
                date=iso_date or "",
                status=(status_short or "N/A"),
                scores=scores or {},
                home_logo=home_logo,
                away_logo=away_logo,
            )

            attach_game_id(game_obj, raw)
            games.append(game_obj)
        except Exception as e:
            st.error(f"Error parsing game data: {e}")
            continue
    return games


# ----------------- Utility to render HTML table w/out index -----------------
def show_table_no_index(df: pd.DataFrame):
    """
    Render a pandas DataFrame as HTML with no index so Streamlit displays no index column.
    We use DataFrame.to_html(index=False) and st.markdown(unsafe_allow_html=True).
    """
    # Fill NaN so it looks clean
    df = df.fillna("-")
    html = df.to_html(index=False, classes="table table-sm", justify="left")
    st.markdown(html, unsafe_allow_html=True)


# ----------------- Display single game -----------------
def display_game(game: GameModel, now_utc: datetime, show_odds=False, client: APISportsClient = None):
    st.markdown("---")
    col1, col2, col3 = st.columns([3, 1, 3])

    with col1:
        if game.home_logo:
            st.image(game.home_logo, width=80)
        st.markdown(f"### {game.home_team}")
        if (game.status or "").upper() not in ("NS",) and game.home_score is not None:
            st.markdown(f"**Score: {game.home_score}**")

    with col2:
        st.markdown("### VS")
        st.markdown(f"**{(game.status or 'NS')}**")

    with col3:
        if game.away_logo:
            st.image(game.away_logo, width=80)
        st.markdown(f"### {game.away_team}")
        if (game.status or "").upper() not in ("NS",) and game.away_score is not None:
            st.markdown(f"**Score: {game.away_score}**")

    st.markdown(f"📍 **Venue:** {game.venue}  |  🕒 **Date (UTC):** {format_dt(game)}")

    # Quarter scores for LIVE/FT (if present)
    if (game.status or "").upper() in ("LIVE", "FT"):
        home_q = [str(game.scores.get("home", {}).get(f"quarter_{i}", 0)) for i in range(1, 5)]
        away_q = [str(game.scores.get("away", {}).get(f"quarter_{i}", 0)) for i in range(1, 5)]
        st.markdown(f"🏈 **Quarter Scores:** {', '.join(home_q)} — {', '.join(away_q)}")

    # Odds section (lazy load on expand)
    if show_odds and hasattr(game, "game_id") and client is not None:
        with st.expander("💰 Odds", expanded=False):
            try:
                # Fetch only once (cached)
                with st.spinner("Fetching odds..."):
                    headers_items = tuple(sorted(client.headers.items()))
                    odds_payload = fetch_odds_cached(getattr(game, "game_id"), client.base_url, headers_items)

                if isinstance(odds_payload, dict) and odds_payload.get("_error"):
                    st.warning(f"Error fetching odds: {odds_payload['_error']}")
                    st.markdown("💰 **Odds:** Not yet released / API error")
                    return
                if isinstance(odds_payload, dict) and odds_payload.get("errors"):
                    st.warning(f"Odds API returned errors: {odds_payload.get('errors')}")
                    st.markdown("💰 **Odds:** Not yet released / API returned errors")
                    return
                if not odds_payload:
                    st.markdown("💰 **Odds:** Not yet released by bookmakers")
                    return

                # Game-time window checks
                dt = game.parsed_date
                if (game.status or "").upper() == "FT":
                    st.markdown("💰 **Odds:** Not Available (game finished)")
                    return
                if not dt:
                    st.markdown("💰 **Odds:** Not Available (invalid date)")
                    return
                if dt > now_utc + timedelta(days=7):
                    st.markdown("💰 **Odds:** Not Available (pre-match window is 1–7 days before game)")
                    return

                bookmakers = odds_payload.get("bookmakers", []) or []
                if not bookmakers:
                    st.markdown("💰 **Odds:** Not yet released by bookmakers")
                    return

                # Build mapping bet_name -> {bookmaker -> {option: odd}}
                bets_by_name = {}
                bookies_order = []
                for bm in bookmakers:
                    bm_name = bm.get("name", "Unknown")
                    bookies_order.append(bm_name)
                    for bet in bm.get("bets", []) or []:
                        bet_name = bet.get("name", "Bet")
                        if bet_name not in bets_by_name:
                            bets_by_name[bet_name] = {}
                        bets_by_name[bet_name][bm_name] = {
                            v.get("value", ""): v.get("odd", "N/A")
                            for v in (bet.get("values", []) or [])
                        }

                # UI controls
                compare_label = "Compare (All bookmakers)"
                bookie_options = [compare_label] + bookies_order
                selected_bookie = st.selectbox("Choose view", options=bookie_options, key=f"bm_{game.game_id}")

                bet_names = sorted(list(bets_by_name.keys()))
                bet_select_choices = ["All categories"] + bet_names
                selected_bet = st.selectbox("Bet Category", options=bet_select_choices, key=f"bet_{game.game_id}")

                # Render comparison
                def render_comparison_table_for_bet(bet_name):
                    bm_data = bets_by_name.get(bet_name, {})
                    all_options = set()
                    for odds_map in bm_data.values():
                        all_options.update(odds_map.keys())
                    all_options = sorted(all_options, key=lambda x: str(x))

                    rows = []
                    for opt in all_options:
                        row = {"Option": opt}
                        for bm in bookies_order:
                            row[bm] = bm_data.get(bm, {}).get(opt, "-")
                        rows.append(row)

                    if rows:
                        df = pd.DataFrame(rows)
                        st.markdown(f"**{bet_name}**")
                        show_table_no_index(df)
                    else:
                        st.markdown("_No options available for this market._")

                def render_bookmaker_markets(bm_name):
                    bm_block = next((b for b in bookmakers if b.get("name") == bm_name), None)
                    if not bm_block:
                        st.markdown("_Bookmaker data not found._")
                        return
                    for bet in bm_block.get("bets", []) or []:
                        bet_name = bet.get("name", "Bet")
                        rows = [{"Option": v.get("value", ""), "Odds": v.get("odd", "N/A")}
                                for v in (bet.get("values", []) or [])]
                        if rows:
                            df = pd.DataFrame(rows)
                            st.markdown(f"**{bet_name} — {bm_name}**")
                            show_table_no_index(df)

                if selected_bookie == compare_label:
                    if selected_bet == "All categories":
                        for bnm in bet_names:
                            render_comparison_table_for_bet(bnm)
                    else:
                        render_comparison_table_for_bet(selected_bet)
                else:
                    render_bookmaker_markets(selected_bookie)

                st.markdown("---")
                st.markdown("**Bookmakers present:** " + ", ".join(bookies_order))

            except Exception as e:
                st.error(f"Error fetching odds: {e}")


# ----------------- Main -----------------
def main():
    client = APISportsClient()

    # Sidebar filters
    with st.sidebar:
        st.header("⚙️ Filters")
        leagues = {"NFL": Config.NFL_LEAGUE_ID, "NCAA": Config.NCAA_LEAGUE_ID}
        selected_league = st.selectbox("Select League", list(leagues.keys()))
        league_id = leagues[selected_league]

        current_season = client.get_current_season()
        seasons = list(range(current_season - 2, current_season + 1))
        selected_season = st.selectbox("Select Season", seasons, index=len(seasons) - 1)

        st.markdown("---")
        st.subheader("Search by Date Range")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        custom_search = st.button("Search by Date")

    # Fetch all games (use 'league' param as your client expects)
    try:
        api_response = client.get_games(league=league_id, season=selected_season)
    except TypeError as e:
        st.error(f"Error fetching games: {e}")
        return
    except Exception as e:
        st.error(f"Unexpected error fetching games: {e}")
        return

    if not api_response:
        st.info("No games found for the selected league/season.")
        return

    # Parse games robustly
    games = parse_games(api_response)
    now = datetime.now(timezone.utc)

    # Buckets
    live_games = [g for g in games if (g.status or "").upper() == "LIVE"]
    upcoming_games = [g for g in games if g.parsed_date and g.parsed_date > now and (g.status or "").upper() != "FT"]
    recent_games = [g for g in games if g.parsed_date and g.parsed_date <= now]

    # Custom date filter
    if custom_search:
        start_dt = datetime.combine(start_date, datetime.min.time()).replace(tzinfo=timezone.utc)
        end_dt = datetime.combine(end_date, datetime.max.time()).replace(tzinfo=timezone.utc)
        custom_games = [g for g in games if g.parsed_date and start_dt <= g.parsed_date <= end_dt]
        tabs = st.tabs(["Custom Date Range"])
        with tabs[0]:
            if custom_games:
                for g in custom_games:
                    show_odds = (g.status or "").upper() == "LIVE" or (g.parsed_date and g.parsed_date <= now + timedelta(days=7))
                    display_game(g, now, show_odds=show_odds, client=client)
            else:
                st.info("No games found in this date range.")
        return

    # Default tabs
    tabs = st.tabs(["Live Games", "Upcoming (7 days)", "Recent (7 days)"])

    with tabs[0]:
        if live_games:
            for g in live_games:
                display_game(g, now, show_odds=True, client=client)
        else:
            st.info("No live games currently.")

    with tabs[1]:
        upcoming_7 = [g for g in upcoming_games if g.parsed_date and g.parsed_date <= now + timedelta(days=7)]
        if upcoming_7:
            for g in upcoming_7:
                display_game(g, now, show_odds=True, client=client)
        else:
            st.info("No upcoming games in the next 7 days.")

    with tabs[2]:
        recent_7 = [g for g in recent_games if g.parsed_date and g.parsed_date >= now - timedelta(days=7)]
        if recent_7:
            for g in recent_7:
                display_game(g, now, show_odds=False, client=client)
        else:
            st.info("No recent games in the last 7 days.")


if __name__ == "__main__":
    main()
