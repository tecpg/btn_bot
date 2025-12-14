import random
import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://primatips.com/tips/2025-11-12"

headers_list = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/91.0.4472.124 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                   "Version/14.0.3 Safari/605.1.15"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G970F) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/90.0.4430.212 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/90.0.4430.212 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) "
                   "Gecko/20100101 Firefox/91.0"},
]

additional_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com",
    "Connection": "keep-alive",
}


def get_random_headers():
    return {**random.choice(headers_list), **additional_headers}


def scrape_tipsomatic(date=None):
    """Scrape Primatips for given date (or today if None)."""
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

        match["time"] = game.select_one(".tm").text.strip() if game.select_one(".tm") else None
        match["league"] = game.select_one(".cn").text.strip() if game.select_one(".cn") else None
        match["country"] = game.select_one(".fl img")["title"] if game.select_one(".fl img") else None

        teams = game.select(".nms .nm")
        if len(teams) == 2:
            match["home_team"] = teams[0].text.strip()
            match["away_team"] = teams[1].text.strip()

        match["tip"] = game.select_one(".to .tip").text.strip() if game.select_one(".to .tip") else None
        match["odd"] = game.select_one(".to .odd").text.strip() if game.select_one(".to .odd") else None

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


        # ✅ Result
        result_parts = game.select(".res .r")
        if len(result_parts) == 2:
            match["result"] = f"{result_parts[0].text.strip()} - {result_parts[1].text.strip()}"
        else:
            match["result"] = None

        matches.append(match)

    return matches


# ---------- MAIN EXECUTION ----------
if __name__ == "__main__":
    today_matches = scrape_tipsomatic()

    print(f"\n✅ Found {len(today_matches)} qualified matches today.\n")
    for match in today_matches[:5]:
        print(f"{match['home_team']} vs {match['away_team']} | Tip: {match['tip']} | Odd: {match['odd']}")

    with open("tipsomatic_filtered.json", "w", encoding="utf-8") as f:
        json.dump(today_matches, f, indent=2, ensure_ascii=False)

    print("\n💾 Saved to tipsomatic_filtered.json\n")
