import csv
from mysql.connector import pooling
import kbt_funtions
import kbt_load_env
from consts import global_consts as gc


# =========================
# Fetch matches for a given date
# =========================
def fetch_matches_by_date(match_date: str):
    results = []
    connection = None

    try:
        connection = kbt_funtions.db_connection()
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT id, league, fixtures, tip, score,
                       match_date, result, code
                FROM soccerpunt
                WHERE match_date = %s
                ORDER BY id ASC
            """
            cursor.execute(query, (match_date,))
            results = cursor.fetchall()

        print(f"[INFO] Fetched {len(results)} matches for {match_date}")

    except Exception as e:
        print("[ERROR] Failed to fetch matches:", e)

    finally:
        if connection:
            connection.close()  # return to pool
            print("[INFO] Connection returned to pool")

    return results


# =========================
# Export matches to CSV
# =========================
def export_matches_to_csv(matches: list, csv_file: str):
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # CSV header
        writer.writerow([
            "ID",
            "League",
            "Fixture",
            "Tip",
            "Score",
            "Match Date",
            "Result",
            "Code"
        ])

        for m in matches:
            writer.writerow([
                m.get("id", ""),
                m.get("league", ""),
                m.get("fixtures", ""),
                m.get("tip", ""),
                m.get("score", ""),
                m.get("match_date", ""),
                m.get("result", ""),
                m.get("code", "")
            ])

            print(
                f"{m.get('league')} | "
                f"{m.get('fixtures')} → Score: {m.get('score')}"
            )

    print(f"\n[INFO] All matches saved to {csv_file}")


# =========================
# Runner
# =========================
def run():
    date_to_fetch = gc.YESTERDAY_YMD
    csv_file_path = "btn_match_results.csv"

    matches = fetch_matches_by_date(date_to_fetch)

    if matches:
        export_matches_to_csv(matches, csv_file_path)
    else:
        print(f"[INFO] No matches found for {date_to_fetch}")


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    run()
