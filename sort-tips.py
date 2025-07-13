import json
from datetime import datetime
from collections import defaultdict

# === Step 1: Load predictions from tips.json ===
with open('smart_odds_2025-07-07.json', 'r') as file:
    predictions = json.load(file)

# === Step 2: Parse and sort by datetime ===
for match in predictions:
    # Clean `.utc` and convert to datetime
    match_datetime = datetime.strptime(match['date'].replace('.utc', ''), "%b %d, %H:%M")
    match['parsed_date'] = match_datetime
    match['date_key'] = match_datetime.strftime('%b_%d')  # e.g. "Jun_29"

# Sort all matches by full datetime
predictions.sort(key=lambda x: x['parsed_date'])

# === Step 3: Group by date ===
grouped = defaultdict(list)
for match in predictions:
    grouped[match['date_key']].append(match)

# === Step 4: Save each group to a JSON file ===
for date_key, matches in grouped.items():
    # Clean up temporary keys
    for m in matches:
        m.pop('parsed_date', None)
        m.pop('date_key', None)

    filename = f"{date_key}.json"
    with open(filename, 'w') as f:
        json.dump(matches, f, indent=4)

    print(f"Saved {filename} with {len(matches)} matches.")
