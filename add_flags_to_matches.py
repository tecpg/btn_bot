# -----------------------------
# Helper functions
# -----------------------------
import csv
import re
import traceback
import unicodedata
from collections import defaultdict
from consts import global_consts as gc

from consts import global_consts as gc
import kbt_funtions
# -----------------------------
# Helper functions
# -----------------------------
def normalize_team(name):
    name = name.lower()
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
    name = re.sub(r'[^a-z\s]', ' ', name)
    name = re.sub(r'\b(b|ii|ad|fc|sc|cf|club|rs|rj)\b', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    words = set(w for w in name.split() if len(w) > 2)
    return words

def partial_match(db_home, db_away, api_home, api_away):
    db_home_words = normalize_team(db_home)
    db_away_words = normalize_team(db_away)
    api_home_words = normalize_team(api_home)
    api_away_words = normalize_team(api_away)

    match1 = bool(db_home_words & api_home_words) and bool(db_away_words & api_away_words)
    match2 = bool(db_home_words & api_away_words) and bool(db_away_words & api_home_words)
    return match1 or match2


import csv
from collections import defaultdict

def combine_csvs_and_add_flags(csv_files, api_csv_file, output_csv_file):
    api_data = []
    league_flag_map = defaultdict(str)
    league_logo_map = defaultdict(str)

    # -----------------------------
    # Load API CSV
    # -----------------------------
    with open(api_csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            api_data.append(row)

            league = row.get("League", "")
            if league:
                league_flag_map.setdefault(league, row.get("League Flag", ""))
                league_logo_map.setdefault(league, row.get("League Logo", ""))

    output_rows = []
    header_written = False

    for db_csv_file in csv_files:
        with open(db_csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)

            if not header_written:
                # ensure header has league_logo column
                if "League Logo" not in header:
                    header.insert(9, "League Logo")
                output_rows.append(header)
                header_written = True

            for row in reader:
                while len(row) < 17:
                    row.append("")

                db_league = row[0]
                db_fixture = row[1]
                db_home, db_away = (
                    [x.strip() for x in db_fixture.split(" vs ")]
                    if " vs " in db_fixture else ("", "")
                )

                league_logo = ""
                league_flag = ""
                home_flag = ""
                away_flag = ""

                for api in api_data:
                    if partial_match(
                        db_home,
                        db_away,
                        api["Home Team"],
                        api["Away Team"]
                    ):
                        league_logo = api.get("League Flag", "")
                        league_flag  = api.get("League Logo", "")
                        home_flag    = api.get("Home Logo", "")
                        away_flag    = api.get("Away Logo", "")
                        break

                # Fallbacks
                league_logo = league_logo or league_logo_map.get(db_league, "")
                league_flag = league_flag or league_flag_map.get(db_league, "")
                home_flag   = home_flag or league_flag
                away_flag   = away_flag or league_flag

                # Replace columns
                row[8]  = league_logo
                row[9] = league_flag
                row[10] = home_flag
                row[11] = away_flag

                output_rows.append(row)

    with open(output_csv_file, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(output_rows)

    print(f"✅ CSV aligned perfectly → {output_csv_file}")


def insert_predictions_from_csv(csv_file_path):
    predictions = []

    # ------------------ READ CSV ------------------
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  # skip header
            for row in reader:
                if row:
                    # Ensure exactly 16 columns
                    row = row[:17]              # truncate if too long
                    while len(row) < 17:       # fill if too short
                        row.append("")
                    predictions.append(row)
    except Exception as e:
        print(f"❌ Failed to read CSV {csv_file_path}: {e}")
        return

    if not predictions:
        print("⚠️ No predictions found in CSV")
        return

    connection = None
    cursor = None

    try:
        connection = kbt_funtions.db_connection()
        cursor = connection.cursor()

        insert_sql = """
        INSERT IGNORE INTO soccerpunt
        (league, fixtures, tip, odd, match_time, score, date, match_date,
          league_logo, league_flag, home_flag, away_flag, flag, result, code, source, protip)
        VALUES (%s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(insert_sql, predictions)
        connection.commit()
        print(f"✅ Inserted predictions (INSERT IGNORE may skip duplicates)")

        # DELETE duplicates
        cleanup_sql = """
        DELETE t1 FROM soccerpunt AS t1
        INNER JOIN soccerpunt AS t2
        ON t1.fixtures = t2.fixtures
        AND t1.source = t2.source
        AND t1.id < t2.id
        """
        cursor.execute(cleanup_sql)
        connection.commit()
        print(f"🧹 Duplicate cleanup done")

    except Exception:
        print("❌ DB ERROR during insert or cleanup")
        traceback.print_exc()

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("🔒 MySQL connection closed")


# -----------------------------
# Main run function
# -----------------------------
def run():
    csv_files = [
        gc.VIP_CSV,
        gc.VIP_CSV_2,
        gc.PRIMA_CSV,
        gc.PRIMA_LOW_CSV,
        gc.SAFE_BET_OVERGOALS_CSV
    ]

    output_csv_file = "add_match_flags.csv"

    # Combine CSVs and add flags
    combine_csvs_and_add_flags(
        csv_files=csv_files,
        api_csv_file="api_match.csv",
        output_csv_file=output_csv_file
    )

    # Insert into DB
    insert_predictions_from_csv(output_csv_file)


if __name__ == "__main__":
    run()
