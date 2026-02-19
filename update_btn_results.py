import csv
import mysql.connector
from mysql.connector import errorcode
import kbt_funtions
import re
import unicodedata


# =========================
# Determine bet result
# =========================
def determine_result(tip, home_score, away_score):
    try:
        home_score = int(home_score)
        away_score = int(away_score)
    except (ValueError, TypeError):
        return "?:?"

    tip = tip.upper().replace(" ", "").strip()
    total_goals = home_score + away_score

    if tip in ("HOMEDC", "HOME"):
        return "Won" if home_score >= away_score else "Lost"

    if tip in ("AWAYDC", "AWAY"):
        return "Won" if away_score >= home_score else "Lost"

    if tip == "1":
        return "Won" if home_score > away_score else "Lost"

    if tip == "X":
        return "Won" if home_score == away_score else "Lost"

    if tip == "2":
        return "Won" if away_score > home_score else "Lost"

    if tip == "1X":
        return "Won" if home_score >= away_score else "Lost"

    if tip in ("X2", "2X"):
        return "Won" if away_score >= home_score else "Lost"

    if tip == "12":
        return "Won" if home_score != away_score else "Lost"

    if tip in ("OVER1.5", "O1.5"):
        return "Won" if total_goals >= 2 else "Lost"

    return "?:?"


# =========================
# Team normalization
# =========================
def normalize_team(name):
    name = name.lower()
    name = unicodedata.normalize("NFD", name)
    name = "".join(c for c in name if unicodedata.category(c) != "Mn")
    name = re.sub(r"[-']", " ", name)
    name = re.sub(r"[^a-z\s]", " ", name)
    name = re.sub(r"\b(b|ii|ad|fc|sc|united|cf|club|rs|rj|dubai)\b", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return set(w for w in name.split() if len(w) > 2)


def partial_match(db_home, db_away, api_home, api_away):
    return (
        normalize_team(db_home) & normalize_team(api_home)
        and normalize_team(db_away) & normalize_team(api_away)
    ) or (
        normalize_team(db_home) & normalize_team(api_away)
        and normalize_team(db_away) & normalize_team(api_home)
    )


# =========================
# CSV Processing
# =========================
def process_csvs(db_csv, api_csv, output_csv):
    api_fixtures = []
    with open(api_csv, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            api_fixtures.append({
                "home": row["Home Team"].lower(),
                "away": row["Away Team"].lower(),
                "home_score": row["Home Score"],
                "away_score": row["Away Score"],
                "score": f"{row['Home Score']}-{row['Away Score']}"
            })

    with open(db_csv, encoding="utf-8") as f:
        db_matches = list(csv.DictReader(f))

    updated = 0
    for match in db_matches:
        if " vs " not in match["Fixture"]:
            continue

        db_home, db_away = map(str.strip, match["Fixture"].split(" vs "))

        for api in api_fixtures:
            if partial_match(db_home, db_away, api["home"], api["away"]):
                match["Score"] = api["score"]
                match["Result"] = determine_result(
                    match.get("Tip", ""),
                    api["home_score"],
                    api["away_score"]
                )
                updated += 1
                break

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=db_matches[0].keys())
        writer.writeheader()
        writer.writerows(db_matches)

    print(f"✅ CSV updated: {updated} matches")
    return output_csv


# =========================
# MySQL Update
# =========================
def update_mysql_from_csv(csv_file):
    try:
        connection = kbt_funtions.db_connection()
        cursor = connection.cursor()
        updated = 0

        with open(csv_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row["Code"] or row["Score"] == "?:?":
                    continue

                cursor.execute(
                    """
                    UPDATE soccerpunt
                    SET score = %s, result = %s
                    WHERE code = %s
                    """,
                    (row["Score"], row["Result"], row["Code"])
                )

                if cursor.rowcount:
                    updated += 1

        connection.commit()
        print(f"✅ Database updated: {updated} rows")

    except mysql.connector.Error as err:
        print("MySQL Error:", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# =========================
# RUN
# =========================
def run():
    DB_CSV = "btn_match_results.csv"
    API_CSV = "api_match_result.csv"
    OUTPUT_CSV = "btn_match_results_updated.csv"

    updated_csv = process_csvs(DB_CSV, API_CSV, OUTPUT_CSV)
    update_mysql_from_csv(updated_csv)


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    run()
