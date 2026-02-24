import csv
import random
import time
from datetime import datetime

import mysql.connector
from mysql.connector import errorcode
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

import kbt_funtions
from consts import global_consts as gc


# =========================
# GLOBAL CONFIG
# =========================

TOMORROW_DATE = gc.TOMORROW_YMD
CSV_FILE = gc.BASKETBALL_CSV
COUNTRIES = gc.COUNTRIES

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
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


# =========================
# HELPERS
# =========================

def get_random_headers():
    return {**random.choice(HEADERS_LIST), **EXTRA_HEADERS}


def get_country_name_from_code(img_code):
    for country in COUNTRIES:
        if img_code.lower() in (
            country["2_code"].lower(),
            country["3_code"].lower(),
        ):
            return country["name"]
    return ""


# =========================
# SCRAPER
# =========================

def scrape_basketball_data():
    rows = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,   # set False if debugging
            slow_mo=50
        )

        headers = get_random_headers()

        context = browser.new_context(
            user_agent=headers.get("User-Agent"),
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            extra_http_headers=headers,
        )

        # Hide webdriver flag
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        page = context.new_page()
        url = f"https://www.forebet.com/en/basketball/predictions/{TOMORROW_DATE}"
        page.goto(url, wait_until="networkidle", timeout=90000)

        # IMPORTANT: wait for actual content
        page.wait_for_selector(".rcnt", timeout=90000)

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    games = soup.select(".rcnt")

    print(f"✅ Found {len(games)} games")

    for i, game in enumerate(games[:50]):  # limit to 50
        try:
            league = game.select_one(".shortTag")
            home = game.select_one(".homeTeam span")
            away = game.select_one(".awayTeam span")
            date_tag = game.select_one(".date_bah")
            pred_div = game.select_one("div.predict")

            pred = pred_div.get_text(strip=True) if pred_div else "N/A"

            result = "N/A"
            if pred_div and "class" in pred_div.attrs:
                if "predict_y" in pred_div["class"]:
                    result = "Won"
                elif "predict_no" in pred_div["class"]:
                    result = "Lost"

            score = game.select_one(".ex_sc b")
            avg_points = game.select_one(".avg_sc")

            img_tag = game.select_one("div.shortagDiv img")
            img_code = img_tag["src"].split("/")[-1].split(".")[0] if img_tag else ""
            flag_name = get_country_name_from_code(img_code)

            a_tag = game.select_one("a.tnmscn")
            fixtures_link = f"https://www.forebet.com{a_tag['href']}" if a_tag else ""
            league_slug = a_tag["href"].split("/")[3] if a_tag else ""

            # Date & time parsing
            date_only, time_only = "N/A", "N/A"
            if date_tag:
                try:
                    dt = datetime.strptime(date_tag.text.strip(), "%d/%m/%Y %H:%M")
                    date_only = dt.strftime("%d-%m-%Y")
                    time_only = dt.strftime("%H:%M")
                except ValueError:
                    pass

            score_text = score.text.strip() if score else "N/A"
            avg_points = avg_points.text.strip() if avg_points else "N/A"
            code = kbt_funtions.get_code(8)

            rows.append([
                league.text.strip() if league else "",
                f"{home.text.strip()} vs {away.text.strip()}",
                pred,
                "",
                time_only,
                score_text,
                date_only,
                f"{flag_name} - {img_code}",
                result,
                code,
                "fb_basketball",
                "",
                avg_points,
                score_text,
                fixtures_link,
                league_slug,
            ])

        except Exception as e:
            print("⚠️ Error parsing game:", e)

    return rows


# =========================
# CSV
# =========================

def save_to_csv(rows):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "league", "fixtures", "tip", "odd", "match_time", "score", "date",
            "flag", "result", "code", "source", "rate",
            "avg_point", "correct_score", "fixtures_link", "league_slug"
        ])
        writer.writerows(rows)

    print(f"✅ Saved {len(rows)} rows to {CSV_FILE}")


# =========================
# MYSQL
# =========================

def post_to_mysql():
    try:
        connection = kbt_funtions.db_connection()
        cursor = connection.cursor()

        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO basketball
                    (league, fixtures, tip, odd, match_time, score, date, flag,
                     result, code, source, rate, avg_point, correct_score,
                     fixtures_link, league_slug)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    row
                )

        # remove duplicates
        cursor.execute("""
            DELETE t1 FROM basketball t1
            INNER JOIN basketball t2
            WHERE t1.id < t2.id
            AND t1.fixtures = t2.fixtures
            AND t1.source = t2.source
        """)

        connection.commit()
        print("✅ MySQL insert & cleanup done")

    except mysql.connector.Error as err:
        print("❌ MySQL error:", err)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# =========================
# MAIN
# =========================

def main():
    rows = scrape_basketball_data()
    if rows:
        save_to_csv(rows)
        post_to_mysql()
    else:
        print("❌ No games found")


if __name__ == "__main__":
    main()