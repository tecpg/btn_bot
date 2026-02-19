import csv
import logging
import random
import traceback
import requests
from bs4 import BeautifulSoup
import time
import mysql.connector
from mysql.connector import errorcode
import kbt_funtions
from consts import global_consts as gc

BASE_URL = "https://primatips.com/tips/"

date_ = gc.PRESENT_DAY_DATE
p_date = gc.PRESENT_DAY_YMD
csv_f = gc.PRIMA_CSV  # CSV file path

headers_list = [
   {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/91.0.864.59", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/92.0.902.55", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/93.0.961.38", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.818.62 Safari/537.36 Edg/90.0.818.62"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:88.0) Gecko/20100101 Firefox/88.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Android 10; Mobile; rv:88.0) Gecko/88.0 Firefox/88.0" },
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1" },
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}

   
]

additional_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com",
    "Connection": "keep-alive"
}

def get_random_headers():
    return {**random.choice(headers_list), **additional_headers}

# ---------- SCRAPER FUNCTION ----------
def scrape_tipsomatic(date=None, limit=25):
    url = f"{BASE_URL}/tips"
    if date:
        url = f"{BASE_URL}/tips/{date}"

    headers = get_random_headers()
    print(f"🔍 Fetching {url} with {headers['User-Agent']}")

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    matches = []
    for game in soup.select("a.game"):
        match = {}
        match["url"] = BASE_URL + game.get("href", "")
        match["match_time"] = game.select_one(".tm").text.strip() if game.select_one(".tm") else None
        match["date"] = p_date
        match["match_date"] = p_date
        match["source"] = "prima_tips"
        match["flag"] = ""
        match["protip"] = ""
        match["code"] = kbt_funtions.get_code(8)
        match["league"] = game.select_one(".fl img")["title"] if game.select_one(".fl img") else None

        teams = game.select(".nms .nm")
        if len(teams) == 2:
            match["home_team"] = teams[0].text.strip()
            match["away_team"] = teams[1].text.strip()

        match["fixtures"] = f'{match["home_team"]} vs {match["away_team"]}'

        # Extract tip, odd, and result status
        to_span = game.select_one(".data .to")
        if to_span:
            match["tip"] = to_span.select_one(".tip").text.strip() if to_span.select_one(".tip") else None
            match["odd"] = to_span.select_one(".odd").text.strip() if to_span.select_one(".odd") else None

            if "wn" in to_span.get("class", []):
                match["result"] = "Won"
            elif "ls" in to_span.get("class", []):
                match["result"] = "Lost"
            else:
                match["result"] = "?"
        else:
            match["tip"] = None
            match["odd"] = None
            match["result"] = "?"

          # ✅ Extract home/draw/away percentages
        percents = [t.text.strip() for t in game.select(".data .tos .ts .t")]
        if len(percents) == 3:
            match["home_percent"], match["draw_percent"], match["away_percent"] = percents
        else:
            match["home_percent"] = match["draw_percent"] = match["away_percent"] = None

   # ✅ Filter: Only include matches where odd < 1.50 AND home% < 40 AND away% < 40
        try:
            odd_val = float(match["odd"]) if match["odd"] else 0
            home_p = int(match["home_percent"]) if match["home_percent"] else 0
            away_p = int(match["away_percent"]) if match["away_percent"] else 0

            if not (odd_val < 1.50 and home_p < 40 and away_p < 40):
                continue
        except ValueError:
            continue

        # Extract score
        result_parts = game.select(".res .r")
        if len(result_parts) == 2:
            match["score"] = f"{result_parts[0].text.strip()} - {result_parts[1].text.strip()}"
        else:
            match["score"] = None

        matches.append(match)
        if len(matches) >= limit:
            break

    return matches


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
            header = [
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
            ]
            writer.writerow(header)

            # Convert dicts to row lists
            for match in predictions:
                row = [
                    match.get("league", ""),
                    match.get("fixtures", ""),
                    match.get("tip", ""),
                    match.get("odd", ""),
                    match.get("match_time", ""),
                    match.get("score", ""),
                    match.get("date", ""),
                    match.get("match_date", ""),
                    match.get("flag", ""),
                    match.get("league_logo", ""),
                    match.get("league_flag", ""),
                    match.get("home_flag", ""),
                    match.get("away_flag", ""),
                    match.get("result", ""),
                    match.get("code", ""),
                    match.get("source", ""),
                    match.get("protip", "")
                ]
                writer.writerow(row)

        print(f"✅ Predictions saved to {csv_file}")

    except Exception as e:
        logging.error(f"Failed to write CSV: {e}")
        traceback.print_exc()




def run():
    today_matches = scrape_tipsomatic(limit=25)
    save_predictions_to_csv(today_matches, csv_f)
    


if __name__ == "__main__":
     run()