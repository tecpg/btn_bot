import requests
import json
import random  # For demo Logistic Regression

API_KEY = "c45c4f7d3cf56a3173d13c30180aa40a"
fixture_id = 1394642 # Replace with actual fixture ID

headers = {"x-apisports-key": API_KEY}

result_json = {}

# --- 1️⃣ Fetch Lineups ---
lineup_url = f"https://v3.football.api-sports.io/fixtures/lineups?fixture={fixture_id}"
lineup_response = requests.get(lineup_url, headers=headers).json()

lineups = []
if lineup_response['response']:
    for team_lineup in lineup_response['response']:
        team_data = {
            "team_name": team_lineup['team']['name'],
            "formation": team_lineup['formation'],
            "coach": team_lineup['coach']['name'],
            "starters": [player['player']['name'] for player in team_lineup['startXI']],
            "substitutes": [player['player']['name'] for player in team_lineup['substitutes']]
        }
        lineups.append(team_data)
result_json["lineups"] = lineups

# --- 2️⃣ Fetch Fixture Details ---
fixture_url = f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
fixture_data = requests.get(fixture_url, headers=headers).json()

if fixture_data['response']:
    fixture = fixture_data['response'][0]
    league_id = fixture['league']['id']
    season = fixture['league']['season']
    home_id = fixture['teams']['home']['id']
    away_id = fixture['teams']['away']['id']

    result_json["fixture"] = {
        "fixture_id": fixture_id,
        "home_team": fixture['teams']['home']['name'],
        "away_team": fixture['teams']['away']['name'],
        "date": fixture['fixture']['date'],
        "status": fixture['fixture']['status']['short'],
        "score": fixture['goals']
    }

    # --- 3️⃣ Fetch League Standings ---
    standings_url = f"https://v3.football.api-sports.io/standings?league={league_id}&season={season}"
    standings_response = requests.get(standings_url, headers=headers).json()

    standings = standings_response['response'][0]['league']['standings'][0]
    home_team = next(t for t in standings if t['team']['id'] == home_id)
    away_team = next(t for t in standings if t['team']['id'] == away_id)

    result_json["standings"] = {
        "home_team": {"rank": home_team['rank'], "points": home_team['points']},
        "away_team": {"rank": away_team['rank'], "points": away_team['points']}
    }

    # --- 4️⃣ Fetch H2H ---
    h2h_url = f"https://v3.football.api-sports.io/fixtures/headtohead?h2h={home_id}-{away_id}"
    h2h_response = requests.get(h2h_url, headers=headers).json()

    h2h_list = []
    if h2h_response['response']:
        for match in h2h_response['response'][:5]:
            h2h_list.append({
                "date": match['fixture']['date'],
                "home_team": match['teams']['home']['name'],
                "away_team": match['teams']['away']['name'],
                "home_goals": match['goals']['home'],
                "away_goals": match['goals']['away']
            })
    result_json["h2h"] = h2h_list

    # --- 5️⃣ Fetch Pre-match Odds ---
    odds_url = f"https://v3.football.api-sports.io/odds?fixture={fixture_id}&bookmaker=1"
    odds_response = requests.get(odds_url, headers=headers).json()

    if odds_response['response']:
        odds_data = odds_response['response'][0]['bookmakers'][0]['bets'][0]['values']
        result_json["odds"] = {
            "home": odds_data[0]['odd'],
            "draw": odds_data[1]['odd'],
            "away": odds_data[2]['odd']
        }
    else:
        result_json["odds"] = {"home": None, "draw": None, "away": None}

    # --- 6️⃣ Fetch Fixture Statistics ---
    stats_url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"
    stats_response = requests.get(stats_url, headers=headers).json()

    stats_json = {}
    if stats_response['response']:
        for team_stats in stats_response['response']:
            team_name = team_stats['team']['name']
            stats_json[team_name] = {s['type']: s['value'] for s in team_stats['statistics']}
    result_json["statistics"] = stats_json

    # --- 7️⃣ 1X2 Logistic Regression Prediction (Demo) ---
    home_prob = random.uniform(0.4, 0.7)
    draw_prob = random.uniform(0.1, 0.3)
    away_prob = 1 - home_prob - draw_prob

    result_json["prediction_1x2"] = {
        "1": round(home_prob, 2),
        "X": round(draw_prob, 2),
        "2": round(away_prob, 2)
    }

# --- 8️⃣ Output JSON ---
print(json.dumps(result_json, indent=2))