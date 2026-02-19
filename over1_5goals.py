import csv
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import traceback

from consts import global_consts as gc
import kbt_funtions

# CSV file path
csv_f = gc.SAFE_BET_OVERGOALS_CSV

# Headers for requests
my_headers = gc.MY_HEARDER

# Today's date in Y-m-d format
p_date = gc.PRESENT_DAY_YMD

# -----------------------------
# Set up logging for errors
# -----------------------------
logging.basicConfig(
    filename='error_log.txt',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -----------------------------
# Function to scrape today's predictions
# -----------------------------
def get_today_prediction(set_date):
    url = "https://www.safertip.com/over-25"
    predictions = []

    try:
        response = requests.get(url, headers=my_headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Fetch failed: {e}")
        return predictions

    bs = BeautifulSoup(response.content, "html.parser")
    tables = bs.find_all("div", class_="col-md-9")[:4]  # Limit to first 4 tables

    for table_box in tables:
        table = table_box.find("table")
        if not table:
            continue

        for row in table.find_all("tr")[1:10]:  # Skip header, limit to 10 rows per table
            cells = row.find_all("td")
            if len(cells) < 5:
                continue

            league_raw = cells[0].get_text(strip=True)
            time_raw = cells[1].get_text(strip=True)
            fixtures = cells[2].get_text(strip=True).replace("Vs", " vs ")
            odd_text = cells[4].get_text(strip=True)

            try:
                odd = float(odd_text)
                if odd < 1.15:  # Skip very low odds
                    continue
            except ValueError:
                continue

            adjusted_time = kbt_funtions.adjust_to_gmt(time_raw)

            # Prepare row for CSV
            predictions.append([
                league_raw,
                fixtures,
                "Over 1.5",
                kbt_funtions.get_random_odd_over_15(),  # random odd function
                adjusted_time,
                "?:?",       # score
                set_date,    # date
                set_date,    # match_date
                "",          # flag
                "N/A",       # league_flag
                "N/A",       # league_flag
                "",          # home_flag
                "",          # away_flag
                "?",   # result
                kbt_funtions.get_code(8),  # code
                "safertip_over_15",  # source
                0            # protip
            ])

    return predictions

# -----------------------------
# Function to save predictions to CSV
# -----------------------------
def save_predictions_to_csv(predictions, csv_file):
    if not predictions:
        print("⚠️ No predictions to save")
        return

    try:
        with open(csv_file, mode="w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow([
                "League",
                "Fixtures",
                "Tip",
                "Odd",
                "Match Time",
                "Score",
                "Date",
                "Match Date",
                
                "League Logo",
                "League Flag",
                "Home Flag",
                "Away Flag",
                "Flag",
                "Result",
                "Code",
                "Source",
                "Protip"
            ])
            # Write all rows
            writer.writerows(predictions)

        print(f"✅ Predictions saved to {csv_file}")

    except Exception as e:
        logging.error(f"Failed to write CSV: {e}")
        traceback.print_exc()


# -----------------------------
# Main run function
# -----------------------------
def run():
    predictions = get_today_prediction(p_date)
    save_predictions_to_csv(predictions, csv_f)


if __name__ == "__main__":
    run()
