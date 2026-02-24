import csv
import random
import time
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import kbt_funtions
from consts import global_consts as gc


# =========================================================
# CONFIG
# =========================================================
PRESENT_DATE = gc.PRESENT_DAY_DATE
TARGET_DATE = gc.YESTERDAY_DATE
CSV_FILE = gc.BASKETBALL_CSV
COUNTRIES = gc.COUNTRIES


# =========================================================
# HEADERS
# =========================================================
HEADERS_LIST = [
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


EXTRA_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com",
}


def get_random_headers():
    return {**random.choice(HEADERS_LIST), **EXTRA_HEADERS}


# =========================================================
# HELPERS
# =========================================================
def get_country_name_from_code(code: str) -> str:
    for c in COUNTRIES:
        if code.lower() in (c["2_code"].lower(), c["3_code"].lower()):
            return c["name"]
    return ""


def parse_date_time(text):
    try:
        dt = datetime.strptime(text, "%d/%m/%Y %H:%M")
        return dt.strftime("%d-%m-%Y"), dt.strftime("%H:%M")
    except Exception:
        return "N/A", "N/A"


# =========================================================
# SCRAPER
# =========================================================
def scrape_basketball_data(date_str):
    rows = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        headers = get_random_headers()

        context = browser.new_context(
            user_agent=headers["User-Agent"],
            extra_http_headers=headers,
            locale="en-US"
        )

        page = context.new_page()
        page.goto(f"https://www.forebet.com/en/basketball/predictions/{date_str}")
        page.wait_for_selector("h1.frontH", timeout=60000)

        soup = BeautifulSoup(page.content(), "html.parser")
        browser.close()

    games = soup.select(".rcnt")
    print(f"Found {len(games)} games")

    for i, game in enumerate(games[:50]):
        try:
            league = game.select_one(".shortTag")
            home = game.select_one(".homeTeam span")
            away = game.select_one(".awayTeam span")
            date_el = game.select_one(".date_bah")

            predict = game.select_one("div[class^='predict']")
            pred_text = predict.get_text(strip=True) if predict else "N/A"

            result = "N/A"
            if predict:
                classes = predict.get("class", [])
                if "predict_y" in classes:
                    result = "Won"
                elif "predict_no" in classes:
                    result = "Lost"

            score_div = game.select_one("div.lscr_td > div.fj_column")
            spans = score_div.find_all("span") if score_div else []
            score1 = spans[0].text if len(spans) > 0 else "N/A"
            score2 = spans[1].text if len(spans) > 1 else "N/A"
            final_score = f"{score1} - {score2}"

            prob = game.select(".fprc span")
            prob1 = prob[0].text if len(prob) > 0 else "N/A"
            prob2 = prob[1].text if len(prob) > 1 else "N/A"

            avg_point = game.select_one(".avg_sc")
            avg_point = avg_point.text if avg_point else "N/A"

            img = game.select_one("div.shortagDiv img")
            img_code = img["src"].split("/")[-1].split(".")[0] if img else ""
            flag_name = get_country_name_from_code(img_code)

            link = game.select_one("a.tnmscn")
            fixtures_link = f"https://www.forebet.com{link['href']}" if link else ""
            league_slug = link["href"].split("/")[3] if link else ""

            date_only, time_only = parse_date_time(date_el.text if date_el else "")

            rows.append([
                league.text if league else "",
                f"{home.text if home else ''} vs {away.text if away else ''}",
                pred_text,
                "",
                time_only,
                final_score,
                date_only,
                f"{flag_name} - {img_code}",
                result,
                kbt_funtions.get_code(8),
                "fb_basketball",
                f"{prob1} - {prob2}",
                avg_point,
                final_score,
                fixtures_link,
                league_slug,
            ])

        except Exception as e:
            print("Error parsing game:", e)

    return rows


# =========================================================
# CSV
# =========================================================
def save_to_csv(rows):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "league", "fixtures", "tip", "odd", "match_time", "score",
            "date", "flag", "result", "code", "source", "rate",
            "avg_point", "correct_score", "fixtures_link", "league_slug"
        ])
        writer.writerows(rows)

    print(f"Saved {len(rows)} rows to {CSV_FILE}")


# =========================================================
# DATABASE
# =========================================================
def post_to_mysql():
    try:
        connection = kbt_funtions.db_connection()
        cursor = connection.cursor()

        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                if len(row) == 16:
                    cursor.execute(
                        """INSERT INTO basketball
                        (league, fixtures, tip, odd, match_time, score, date, flag,
                         result, code, source, rate, avg_point, correct_score,
                         fixtures_link, league_slug)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """,
                        row
                    )

        cursor.execute("""
            DELETE t1 FROM basketball t1
            INNER JOIN basketball t2
            WHERE t1.id < t2.id
            AND t1.fixtures = t2.fixtures
            AND t1.source = t2.source
        """)

        connection.commit()
        print("Database updated successfully")

    except mysql.connector.Error as err:
        print("MySQL Error:", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# =========================================================
# MAIN
# =========================================================
def main():
    print("Fetching games for:", TARGET_DATE)
    rows = scrape_basketball_data(TARGET_DATE)

    if rows:
        save_to_csv(rows)
        post_to_mysql()
    else:
        print("No games found.")


if __name__ == "__main__":
    main()