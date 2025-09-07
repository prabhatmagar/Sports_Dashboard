from datetime import datetime, timezone
from api_client import APISportsClient

client = APISportsClient()
season = client.get_current_season()

# Fetch all games
games = client.get_games(league=1, season=season)

now = datetime.now(timezone.utc)
live_upcoming_games = []

for g in games:
    status = g.get("game", {}).get("status", {}).get("short", "")
    date_info = g.get("game", {}).get("date", {})
    try:
        game_dt = datetime.strptime(f"{date_info['date']} {date_info['time']}", "%Y-%m-%d %H:%M")
        game_dt = game_dt.replace(tzinfo=timezone.utc)
    except Exception:
        continue
    if status == "LIVE" or (game_dt > now and status != "FT"):
        live_upcoming_games.append(g)

# Test odds for these games
for i, g in enumerate(live_upcoming_games[:5]):
    game_id = g.get("game", {}).get("id")
    if not game_id:
        print(f"Game {i+1}: no game id")
        continue

    print(f"Game {i+1} (id={game_id}) odds:")
    try:
        odds = client.get_odds(game_id, season)
        if odds:
            print(odds)
        else:
            print("💰 Odds: N/A")
    except Exception as e:
        print(f"Error fetching odds: {e}")
