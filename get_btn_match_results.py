import csv
import kbt_funtions
from consts import global_consts as gc
import mysql.connector
from mysql.connector import errorcode

# Date to fetch
date_  = gc.YESTERDAY_DMY 

csv_file = "btn_match_results.csv"  # Output CSV

def fetch_matches_by_date(date):
    """
    Fetch finished matches from `soccerpunt` for a specific date.
    :param date: string in 'YYYY-MM-DD' format
    :return: list of dicts containing match info
    """
    results = []

    try:
        # Connect to database
        connection = kbt_funtions.db_connection()
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version:", db_info)
            cursor = connection.cursor(dictionary=True)  # return rows as dicts
            cursor.execute("SELECT database();")
            record = cursor.fetchone()
            print("You're connected to database:", record)

            # Select matches for the given date
            query = """
                SELECT id, league, fixtures, tip, odd, match_time, score, date, flag, result, code, source, protip
                FROM soccerpunt
                WHERE date = %s
                ORDER BY id ASC
            """
            cursor.execute(query, (date,))
            results = cursor.fetchall()
            print(f"Fetched {len(results)} matches for date {date}.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password:", err)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist:", err)
        else:
            print("Error while connecting to MySQL:", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

    return results

# Fetch matches from DB
matches = fetch_matches_by_date(date_)

# Write to CSV
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # CSV Header
    writer.writerow(["League", "Fixture", "Tip",  "Score", "Code", "Result"])
    
    for m in matches:
        writer.writerow([
            m["league"],
            m["fixtures"],
            m["tip"],
            m["score"],
            m["code"],
            m["result"],
        ])
        # Optional: print to console
        print(f"{m['league']} | {m['fixtures']} → Score: {m['score']}")

print(f"\nAll matches for {date_} saved to {csv_file}")
