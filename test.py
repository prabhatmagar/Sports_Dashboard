# test_player_stats.py
import pprint
from api_client import APISportsClient

def main():
    api_client = APISportsClient()

    # Replace with a real player ID and season
    player_id = 8          # Example: Sincere McCormick
    season = 2024          # Example: current season

    try:
        stats = api_client.get_players(player_id,season)
        
        if stats:
            print(f"Statistics for player ID {player_id} (Season {season}):")
            pprint.pprint(stats)
        else:
            print(f"No statistics found for player ID {player_id} in season {season}.")
    except Exception as e:
        print(f"Error fetching stats: {e}")

if __name__ == "__main__":
    main()
