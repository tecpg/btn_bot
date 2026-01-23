import requests
import csv
from consts import global_consts as gc

API_KEY = "c45c4f7d3cf56a3173d13c30180aa40a"
DATE = gc.YESTERDAY_DATE 


URL = f"https://v3.football.api-sports.io/fixtures?date={DATE}&status=FT"

headers = {
    "x-apisports-key": API_KEY
}

csv_file = "api_match_results.csv"  # Output file

try:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    fixtures = response.json()["response"]

    print(f"Total finished matches on {DATE}: {len(fixtures)}\n")

    # Open CSV file for writing
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(["League", "Home Team", "Away Team", "Home Score", "Away Score"])

        # Write match data
        for match in fixtures:
            league_name = match["league"]["name"]
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            score_home = match["goals"]["home"]
            score_away = match["goals"]["away"]
            
            # Write row to CSV
            writer.writerow([league_name, home, away, score_home, score_away])

            # Optional: print to console
            print(f"{league_name} | {home} {score_home} - {score_away} {away}")

    print(f"\nAll matches saved to {csv_file}")

except requests.exceptions.RequestException as e:
    print("API request failed:", e)
