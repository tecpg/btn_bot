import csv
import time
import mysql.connector
from mysql.connector import errorcode
import kbt_funtions

def determine_result(tip, home_score, away_score):
    """Determine Won/Lost based on Tip and API score"""
    try:
        home_score = int(home_score)
        away_score = int(away_score)
    except ValueError:
        return "Not Yet"

    tip = tip.upper().strip()
    if tip == "HOME DC":
        return "Won" if home_score >= away_score else "Lost"
    elif tip == "AWAY DC":
        return "Won" if away_score >= home_score else "Lost"
    elif tip == "HOME":
        return "Won" if home_score > away_score else "Lost"
    elif tip == "AWAY":
        return "Won" if away_score > home_score else "Lost"
    else:
        return "Not Yet"

# -----------------------------
# Utility functions for matching
# -----------------------------
import re

import re

import re

import re
import unicodedata

def normalize_team(name):
    """
    Normalize team names for matching:
    - lowercase
    - remove accents (é -> e)
    - replace punctuation with spaces
    - remove minor words like B, II, AD, FC, SC, CF, CLUB, RJ, RS
    - only keep words longer than 2 letters
    """
    # lowercase
    name = name.lower()
    # remove accents
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
    # replace punctuation with space
    name = re.sub(r'[^\w\s]', ' ', name)
    # remove minor words
    name = re.sub(r'\b(b|ii|ad|fc|sc|cf|club|rs|rj)\b', '', name)
    # split into words and keep words longer than 2 letters
    words = set(w for w in name.split() if len(w) > 2)
    return words

def partial_match(db_home, db_away, api_home, api_away):
    """
    Return True if DB fixture matches API fixture based on normalized word overlap
    Checks both home-home/away-away and home-away/away-home
    """
    db_home_words = normalize_team(db_home)
    db_away_words = normalize_team(db_away)
    api_home_words = normalize_team(api_home)
    api_away_words = normalize_team(api_away)

    # home-home & away-away
    match1 = bool(db_home_words & api_home_words) and bool(db_away_words & api_away_words)
    # home-away & away-home
    match2 = bool(db_home_words & api_away_words) and bool(db_away_words & api_home_words)

    return match1 or match2

# -----------------------------
# File paths
# -----------------------------
db_csv_file = "btn_match_results.csv"
api_csv_file = "api_match_results.csv"
output_csv_file = "btn_match_results_updated.csv"

# Step 1: Read API CSV
api_fixtures = []
with open(api_csv_file, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        api_fixtures.append({
            "league": row["League"].strip().lower(),
            "home": row["Home Team"].strip().lower(),
            "away": row["Away Team"].strip().lower(),
            "home_score": row["Home Score"],
            "away_score": row["Away Score"],
            "score": f"{row['Home Score']}-{row['Away Score']}"
        })

print(f"Loaded {len(api_fixtures)} API fixtures")

# Step 2: Read DB CSV
db_matches = []
with open(db_csv_file, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        db_matches.append(row)

print(f"Loaded {len(db_matches)} DB fixtures from CSV")

# Step 3: Loop through DB matches and match with API fixtures
updated_count = 0
for match in db_matches:
    db_fixture = match["Fixture"]
    if " vs " not in db_fixture:
        continue
    db_home, db_away = map(str.strip, db_fixture.split(" vs "))
    db_code = match["Code"]

    for api in api_fixtures:
        if partial_match(db_home, db_away, api["home"], api["away"]):
            # Update score
            match["Score"] = api["score"]
            # Update Result based on Tip
            match["Result"] = determine_result(match.get("Tip", ""), api["home_score"], api["away_score"])

            updated_count += 1
            print(f"Updated League: {match['League']}, Fixture: {match['Fixture']}, Code: {db_code} → "
                  f"Score: {api['score']}, Result: {match['Result']}")
            break  # Stop searching API once matched

# Step 4: Write updated CSV
fieldnames = list(db_matches[0].keys())  # Includes Result now
with open(output_csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(db_matches)

print(f"\nTotal matches updated: {updated_count}")
print(f"Updated CSV saved as {output_csv_file}")

# -----------------------------
# Step 5: Update MySQL DB from CSV
# -----------------------------
def update_mysql_from_csv(csv_f):
    """
    Update soccerpunt scores/results using CSV data matched by code
    """
    try:
        connection = kbt_funtions.db_connection()

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version:", db_Info)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("You're connected to database:", record)

        updated_rows = 0

        with open(csv_f, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                code = row.get("Code", "").strip()
                score = row.get("Score", "").strip()
                result = row.get("Result", "").strip()

                if not code or score == "Not Yet":
                    continue

                cursor.execute(
                    """
                    UPDATE soccerpunt
                    SET score = %s,
                        result = %s
                    WHERE code = %s
                    """,
                    (score, result, code)
                )

                if cursor.rowcount > 0:
                    updated_rows += 1
                    print(f"Updated Code: {code} → Score: {score}, Result: {result}")

        connection.commit()
        print(f"\n✅ Total records updated: {updated_rows}")

    except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Access denied (check username/password):", err)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist:", err)
            else:
                print("MySQL error:", err)

    finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")

update_mysql_from_csv(output_csv_file)
