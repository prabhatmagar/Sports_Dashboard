# test_games_api.py

from api_client import APISportsClient
import json
from datetime import datetime, timezone

def main():
    client = APISportsClient()

    # Replace league and season as needed
    league_id = 1  # NFL
    season = 2025  # current season

    print(f"Fetching games for league={league_id}, season={season}...\n")

    raw_data = client.get_games(league=league_id, season=season)

    if not raw_data:
        print("No games returned by API.")
        return

    print(f"Total games returned: {len(raw_data)}\n")

    # Print the first 5 raw game entries
    for i, game in enumerate(raw_data[:5], 1):
        print(f"--- Game {i} ---")
        print(json.dumps(game, indent=4))
        print("\n")

    # Optional: list all game dates to check recent/upcoming
    print("Game dates (UTC):")
    for game in raw_data:
        date_str = game.get("date", {}).get("date", "N/A")
        status = game.get("status", {}).get("short", "N/A")
        print(f"{date_str} | Status: {status}")

if __name__ == "__main__":
    main()
